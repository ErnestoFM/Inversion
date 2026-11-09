# Guía de Despliegue en Producción: Google Cloud Platform (Cloud Run & CI/CD)

Este documento detalla la arquitectura de infraestructura, el aprovisionamiento paso a paso y la operación continua del sistema **SIGRE (Sistema Integrado de Gestión de Recursos y Espacios)** en **Google Cloud Platform (GCP)**.

---

## 1. Diagrama de Arquitectura en la Nube

```mermaid
flowchart TD
    subgraph Internet ["🌐 Clientes Institucionales (Red UdeG & Alumnos)"]
        User["📱💻 Usuario (cutonala.udg.mx)"]
    end

    subgraph SecurityTier ["🛡️ Seguridad Perimetral GCP"]
        Recaptcha["Google reCAPTCHA Enterprise\n(Key: 6Le4keItAAAAAP9kezXQe4kjl7kopvvoQ9gTPQuU)"]
        OAuth["Google Identity / OAuth 2.0\n(@udg.mx / @alumnos.udg.mx)"]
    end

    subgraph GitHub ["🐙 GitHub CI/CD Pipeline"]
        GHA["GitHub Actions\n(.github/workflows/ci-cd.yml)"]
        GHA_Test["🧪 Playwright E2E & Turbo Build"]
        GHA_Build["🐳 Docker Build & Push"]
        GHA --> GHA_Test --> GHA_Build
    end

    subgraph GCP ["☁️ Google Cloud Platform (leadforge-499919 / us-central1)"]
        AR["📦 Artifact Registry: sigre\n(sigre/api & sigre/web)"]
        SM["🔐 Secret Manager\n(SIGRE_DATABASE_URL, SIGRE_REDIS_URL, JWT Keys)"]
        GCS["🪣 Cloud Storage\n(gs://sigre-storage-leadforge-499919)"]

        subgraph Serverless ["⚡ Google Cloud Run (Scale to Zero)"]
            WebRun["🌐 sigre-web\n(Nginx 1.27 + Vite SPA)\nPort: 8080 | Min: 0 | Max: 5"]
            ApiRun["⚙️ sigre-api\n(Node.js 20 Express)\nPort: 8080 | Min: 0 | Max: 5"]
        end

        subgraph PrivateVPC ["🔒 Red VPC Privada (sigre-vpc-connector / 10.8.0.0/28)"]
            CloudSQL[("🐘 Cloud SQL: sigre-postgres\nPostgreSQL 16 Enterprise (SSD)")]
            Redis[("⚡ Cloud Memorystore: sigre-redis\nRedis 7 (Anti-Empalme Lock 15 min)")]
        end
    end

    User --> Recaptcha
    User --> OAuth
    User -->|HTTPS| WebRun
    User -->|HTTPS API Requests| ApiRun
    GHA_Build -->|Push Images| AR
    GHA_Build -->|Deploy Service| ApiRun
    GHA_Build -->|Deploy Service| WebRun
    AR -.->|Pull Image| WebRun
    AR -.->|Pull Image| ApiRun
    SM -.->|Inject Secrets| ApiRun
    ApiRun --> GCS
    ApiRun -->|VPC Connector / Unix Socket| CloudSQL
    ApiRun -->|VPC Connector| Redis
```

---

## 2. Ventajas y Estrategia FinOps (Ahorro de Costos)

* **Escala a Cero (`--min-instances 0`):** Cuando no hay alumnos ni personal solicitando espacios (madrugadas, fines de semana o vacaciones), los contenedores se apagan automáticamente, reduciendo el consumo a **$0 USD**.
* **Límite de Instancias (`--max-instances 5`):** Protege tu presupuesto de nube impidiendo picos inesperados.
* **Separación de Cargas:** El Frontend corre en un contenedor ultraligero Nginx Alpine (~25 MB de RAM), reservando los recursos de CPU para el backend Node.js y la generación de actas en PDF.

---

## 3. Preparación Inicial con Google Cloud CLI (`gcloud`)

Ejecuta estos comandos una única vez desde tu terminal con permisos de Administrador del proyecto GCP:

### A. Habilitar las APIs necesarias
```bash
gcloud services enable \
  run.googleapis.com \
  artifactregistry.googleapis.com \
  secretmanager.googleapis.com \
  sqladmin.googleapis.com
```

### B. Crear el repositorio en Artifact Registry
```bash
gcloud artifacts repositories create sigre \
  --repository-format=docker \
  --location=us-central1 \
  --description="Imágenes Docker de producción para SIGRE CUTonalá"
```

### C. Crear la Cuenta de Servicio (Service Account) para CI/CD
```bash
# 1. Crear la cuenta
gcloud iam service-accounts create github-sigre-deployer \
  --display-name="GitHub Actions Deployer para SIGRE"

# 2. Otorgar roles requeridos
gcloud projects add-iam-policy-binding TU_PROYECTO_ID \
  --member="serviceAccount:github-sigre-deployer@TU_PROYECTO_ID.iam.gserviceaccount.com" \
  --role="roles/run.admin"

gcloud projects add-iam-policy-binding TU_PROYECTO_ID \
  --member="serviceAccount:github-sigre-deployer@TU_PROYECTO_ID.iam.gserviceaccount.com" \
  --role="roles/artifactregistry.writer"

gcloud projects add-iam-policy-binding TU_PROYECTO_ID \
  --member="serviceAccount:github-sigre-deployer@TU_PROYECTO_ID.iam.gserviceaccount.com" \
  --role="roles/iam.serviceAccountUser"

# 3. Generar la llave en JSON para GitHub Secrets
gcloud iam service-accounts keys create sa-key.json \
  --iam-account=github-sigre-deployer@TU_PROYECTO_ID.iam.gserviceaccount.com
```

---

## 4. Secretos en Google Secret Manager

Para no exponer contraseñas en variables de entorno planas, crea los secretos en GCP:

```bash
# Database URL
echo -n "postgresql://sigre_user:PASSWORD@IP_O_PROXY:5432/sigre_prod" | \
  gcloud secrets create SIGRE_DATABASE_URL --data-file=-

# Redis URL
echo -n "redis://IP_REDIS:6379" | \
  gcloud secrets create SIGRE_REDIS_URL --data-file=-

# JWT Keys
echo -n "$(openssl rand -base64 48)" | \
  gcloud secrets create SIGRE_JWT_ACCESS_SECRET --data-file=-

echo -n "$(openssl rand -base64 48)" | \
  gcloud secrets create SIGRE_JWT_REFRESH_SECRET --data-file=-
```

Otorga permisos a la cuenta de servicio de Cloud Run para leer estos secretos:
```bash
gcloud projects add-iam-policy-binding TU_PROYECTO_ID \
  --member="serviceAccount:TU_NUMERO_PROYECTO-compute@developer.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"
```

---

## 5. Configuración de Secretos en GitHub

En tu repositorio de GitHub, ve a **Settings > Secrets and variables > Actions** y registra los siguientes valores:

| Nombre del Secreto | Descripción | Ejemplo / Valor |
| :--- | :--- | :--- |
| `GCP_PROJECT_ID` | ID de tu proyecto en Google Cloud | `sigre-cutonala-2026` |
| `GCP_REGION` | Región geográfica preferente | `us-central1` |
| `GCP_ARTIFACT_REPO` | Nombre del repositorio de imágenes | `sigre` |
| `GCP_SA_KEY` | Contenido completo del archivo `sa-key.json` | `{"type": "service_account", ...}` |
| `WEB_URL` | URL final del frontend para CORS | `https://sigre-web-xxx.a.run.app` |
| `VITE_API_BASE` | URL del backend consumida por la web | `https://sigre-api-xxx.a.run.app/api` |

---

## 6. Ejecución de Migraciones de Base de Datos en Producción

Para aplicar migraciones de esquema de base de datos (`prisma migrate deploy`) a Cloud SQL:

```bash
# Opción A: Mediante Cloud SQL Auth Proxy localmente
./cloud-sql-proxy TU_PROYECTO_ID:us-central1:sigre-postgres --port 5432 &
DATABASE_URL="postgresql://sigre_user:PASSWORD@localhost:5432/sigre_prod" pnpm --filter @inversion/database run prisma migrate deploy

# Opción B: Job de Cloud Run (Recomendado para producción)
gcloud run jobs create sigre-migrate \
  --image us-central1-docker.pkg.dev/TU_PROYECTO_ID/sigre/api:latest \
  --command "npx" \
  --args "prisma,migrate,deploy" \
  --region us-central1 \
  --set-secrets "DATABASE_URL=SIGRE_DATABASE_URL:latest"

# Ejecutar la migración
gcloud run jobs execute sigre-migrate --region us-central1
```
