<#
.SYNOPSIS
    Script de aprovisionamiento automatizado en Google Cloud Platform para SIGRE (Proyecto Inversión).
.DESCRIPTION
    Habilita APIs, crea el repositorio en Artifact Registry, bucket de Cloud Storage,
    instancia de Cloud SQL (PostgreSQL 15), base de datos, usuario y secrets en Secret Manager.
#>

param (
    [string]$ProjectId = $(if ($env:GCP_PROJECT_ID) { $env:GCP_PROJECT_ID } else { "monchis-cafe-prod" }),
    [string]$Region = $(if ($env:GCP_REGION) { $env:GCP_REGION } else { "us-central1" }),
    [string]$InstanceName = "sigre-postgres",
    [string]$DbName = "sigre_db",
    [string]$DbUser = "sigre_user",
    [string]$DbPassword = $(if ($env:DB_PASSWORD) { $env:DB_PASSWORD } else { -join ((65..90) + (97..122) + (48..57) | Get-Random -Count 28 | ForEach-Object {[char]$_}) }),
    [string]$Tier = "db-f1-micro"
)

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "   SIGRE CUTonala - Aprovisionamiento de Google Cloud     " -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

# 1. Configurar proyecto y habilitar servicios
Write-Host "`n[1/6] Configurando proyecto objetivo: $ProjectId..." -ForegroundColor Yellow
gcloud config set project $ProjectId

Write-Host "`n[2/6] Habilitando APIs requeridas en GCP..." -ForegroundColor Yellow
gcloud services enable run.googleapis.com sqladmin.googleapis.com cloudbuild.googleapis.com artifactregistry.googleapis.com secretmanager.googleapis.com storage.googleapis.com --project=$ProjectId

# 2. Crear Repositorio en Artifact Registry
Write-Host "`n[3/6] Verificando / Creando repositorio Artifact Registry 'sigre'..." -ForegroundColor Yellow
$repoExists = gcloud artifacts repositories list --filter="name:sigre" --location=$Region --format="value(name)" --project=$ProjectId 2>$null
if (-not $repoExists) {
    gcloud artifacts repositories create sigre --repository-format=docker --location=$Region --description="Repositorio Docker para SIGRE CUTonala" --project=$ProjectId
    Write-Host "Repositorio 'sigre' creado con exito." -ForegroundColor Green
} else {
    Write-Host "El repositorio 'sigre' ya existe." -ForegroundColor Green
}

# 3. Crear Bucket de Cloud Storage para Documentos y Actas
$bucketName = "sigre-storage-$ProjectId"
Write-Host "`n[4/6] Verificando / Creando Bucket de Storage: gs://$bucketName..." -ForegroundColor Yellow
$bucketExists = gcloud storage buckets list --filter="name:$bucketName" --format="value(name)" --project=$ProjectId 2>$null
if (-not $bucketExists) {
    gcloud storage buckets create "gs://$bucketName" --location=$Region --project=$ProjectId 2>$null
    Write-Host "Bucket gs://$bucketName creado con exito." -ForegroundColor Green
} else {
    Write-Host "El bucket gs://$bucketName ya existe." -ForegroundColor Green
}

# 4. Crear Instancia de Cloud SQL PostgreSQL 15
Write-Host "`n[5/6] Verificando / Creando instancia Cloud SQL: $InstanceName..." -ForegroundColor Yellow
$sqlExists = gcloud sql instances list --filter="name:$InstanceName" --format="value(name)" --project=$ProjectId 2>$null
if (-not $sqlExists) {
    Write-Host "Creando instancia $InstanceName (Tier: $Tier, Region: $Region)..." -ForegroundColor Yellow
    gcloud sql instances create $InstanceName --database-version=POSTGRES_15 --tier=$Tier --region=$Region --storage-type=SSD --storage-size=10GB --authorized-networks="0.0.0.0/0" --backup --retained-backups-count=7 --project=$ProjectId
    Write-Host "Instancia de base de datos creada con exito." -ForegroundColor Green
} else {
    Write-Host "La instancia $InstanceName ya existe." -ForegroundColor Green
}

# Crear base de datos y usuario
gcloud sql databases create $DbName --instance=$InstanceName --project=$ProjectId 2>$null
gcloud sql users create $DbUser --instance=$InstanceName --password=$DbPassword --project=$ProjectId 2>$null

# Obtener IP Pública
$publicIp = gcloud sql instances describe $InstanceName --format="value(ipAddresses[0].ipAddress)" --project=$ProjectId
$connectionString = "postgresql://${DbUser}:${DbPassword}@${publicIp}:5432/${DbName}?schema=public"

# 5. Guardar Secretos en GCP Secret Manager
Write-Host "`n[6/6] Sincronizando Secrets en Google Secret Manager..." -ForegroundColor Yellow

function Set-GcpSecret($secretName, $secretValue) {
    $exists = gcloud secrets describe $secretName --project=$ProjectId 2>$null
    if (-not $exists) {
        $secretValue | gcloud secrets create $secretName --data-file=- --project=$ProjectId 2>$null
    } else {
        $secretValue | gcloud secrets versions add $secretName --data-file=- --project=$ProjectId 2>$null
    }
}

Set-GcpSecret "SIGRE_DATABASE_URL" $connectionString
Set-GcpSecret "SIGRE_JWT_ACCESS_SECRET" (-join ((65..90) + (97..122) + (48..57) | Get-Random -Count 48 | ForEach-Object {[char]$_}))
Set-GcpSecret "SIGRE_JWT_REFRESH_SECRET" (-join ((65..90) + (97..122) + (48..57) | Get-Random -Count 48 | ForEach-Object {[char]$_}))
Set-GcpSecret "SIGRE_REDIS_URL" "redis://127.0.0.1:6379"

Write-Host "`n==========================================================" -ForegroundColor Green
Write-Host "  Aprovisionamiento de SIGRE en GCP Completado con Exito  " -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Green
Write-Host "Instancia Cloud SQL: $InstanceName ($publicIp)" -ForegroundColor White
Write-Host "DATABASE_URL: $connectionString" -ForegroundColor White
Write-Host "Artifact Registry: $Region-docker.pkg.dev/$ProjectId/sigre" -ForegroundColor White
Write-Host "Storage Bucket: gs://$bucketName" -ForegroundColor White

