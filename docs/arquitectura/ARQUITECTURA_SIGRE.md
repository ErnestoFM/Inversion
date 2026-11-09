# 🏛️ Documento de Arquitectura de Software — SIGRE v1.0

**Proyecto:** SIGRE (Sistema Integrado de Gestión de Recursos y Espacios)  
**Institución:** Centro Universitario de Tonalá (CUTonalá) — Universidad de Guadalajara  
**Versión de Arquitectura:** 1.0  
**Fecha:** Octubre 2026  
**Estado:** Aprobado / En Implementación  

---

## 1. Visión General del Sistema y Contexto

SIGRE es una plataforma integral diseñada para resolver la problemática histórica del CUTonalá en la gestión, reserva y trazabilidad de espacios físicos (aulas, laboratorios, auditorios, cubículos) y materiales especializados (cámaras, equipo de cómputo, proyectores, kits de electrónica).

El sistema centraliza las operaciones de los diferentes actores de la comunidad universitaria:
- **Alumnos y Docentes (Solicitantes/Custodios):** Solicitan espacios y materiales con cuentas institucionales `@alumnos.udg.mx` o `@udg.mx`.
- **Coordinadores y Jefes de Departamento (Aprobadores):** Validan pertinencia académica y disponibilidad.
- **Técnicos y Operadores de Laboratorio (Entregas y Recepciones):** Verifican el estado físico del material/espacio con listas de verificación (*checklists*) digitales.
- **Administrador General (SuperAdmin):** Gestiona catálogos, políticas, auditoría de usuarios y reportes métricos.

```mermaid
graph TD
    subgraph Comunidad["Comunidad Universitaria (CUTonalá)"]
        A["Alumno / Docente\n(Solicitante)"]
        C["Coordinador / Depto\n(Aprobador)"]
        T["Técnico / Laboratorista\n(Custodia Física)"]
        Admin["SuperAdmin\n(Coordinación de Tecnologías)"]
    end

    subgraph SIGRE["Plataforma SIGRE"]
        Web["Frontend Web (React 18 + Vite)\nDesign System UdeG / Outfit"]
        API["Backend API REST (Express + TypeScript)\nMonorepo Turborepo"]
        LockService["Mecanismo Anti-Empalme\n(Redis 7 TTL Locks)"]
        DB[(Base de Datos Central\nPostgreSQL 16 + Prisma ORM)]
    end

    subgraph ServiciosExt["Servicios Externos / Nube (GCP)"]
        GoogleAuth["Google Workspace UdG\n(OAuth 2.0 / OpenID Connect)"]
        SMTP["Servidor Transaccional SMTP\n(Notificaciones por Correo)"]
        CloudRun["Google Cloud Run\n(Cómputo Serverless en Contenedores)"]
    end

    A -->|HTTPS| Web
    C -->|HTTPS| Web
    T -->|HTTPS / PWA Mobile| Web
    Admin -->|HTTPS| Web

    Web -->|REST API + Bearer JWT| API
    API --> GoogleAuth
    API --> LockService
    API --> DB
    API --> SMTP
    CloudRun -.->|Hospeda| Web
    CloudRun -.->|Hospeda| API
```

---

## 2. Arquitectura de Código: Monorepo Turborepo

El proyecto está estructurado como un **Monorepo** gestionado mediante **Turborepo** y **pnpm workspaces**, lo que garantiza consistencia de dependencias, tipado unificado y reutilización de lógica entre cliente y servidor.

```
Inversion/ (Raíz del Repositorio)
├── apps/
│   ├── api/                     # Backend Node.js + Express + TypeScript
│   │   ├── src/
│   │   │   ├── config/          # Variables de entorno validadas con Zod
│   │   │   ├── controllers/     # Controladores HTTP por módulo
│   │   │   ├── middleware/      # Auth, Roles, RateLimit, Concurrencia
│   │   │   ├── routes/          # Definición de rutas REST
│   │   │   ├── services/        # Lógica de negocio pura (Auth, Mail, QR, PDF)
│   │   │   └── utils/           # Helpers y encriptación
│   │   └── package.json
│   │
│   └── web/                     # Frontend SPA React 18 + TypeScript + Vite
│       ├── src/
│       │   ├── assets/          # Logos SVG, íconos de marca SIGRE
│       │   ├── components/      # Componentes UI basados en la Guía de Marca
│       │   ├── context/         # AuthContext, ThemeContext (Dark/Light)
│       │   ├── hooks/           # Custom hooks (useAuth, useFetch, useSocket)
│       │   ├── pages/           # Vistas organizadas por rol (18 pantallas)
│       │   ├── services/        # Clientes Axios / API Fetchers
│       │   ├── styles/          # Variables CSS (:root, design tokens)
│       │   └── types/           # Tipos de interfaz compartidos
│       └── package.json
│
├── packages/
│   ├── database/                # Acceso a datos y persistencia
│   │   ├── prisma/
│   │   │   ├── schema.prisma    # Definición declarativa de modelos PostgreSQL
│   │   │   ├── migrations/      # Historial de migraciones SQL
│   │   │   └── seed.ts          # Población inicial de catálogos y admin
│   │   └── src/index.ts         # Exportación del cliente tipado de Prisma
│   │
│   ├── shared/                  # Constantes, tipos y validadores Zod compartidos
│   └── eslint-config/           # Reglas de linter unificadas
│
├── infra/
│   ├── docker-compose.yml       # Orquestación local (PostgreSQL 16 + Redis 7)
│   └── README.md
│
└── docs/
    ├── arquitectura/            # Documentación y diagramas técnicos
    ├── brand/                   # Activos gráficos vectoriales (.svg)
    └── tecnica/                 # Especificaciones de endpoints y seguridad
```

---

## 3. Diagrama de Contenedores y Servicios

```mermaid
flowchart TB
    User([Usuario del CUTonalá]) -->|Navegador Web / HTTPS| WebApp["Frontend SPA: apps/web\n(React 18 + Vite)\nDesign System UdeG (Outfit + Tokens)"]

    subgraph BackendApp ["Servidor de Aplicación: apps/api"]
        Router["Express API Router\n(/api/v1)"]
        AuthMid["Auth Middleware\n(JWT Guard + Role Guard)"]
        LockMid["Concurrency Middleware\n(Redis Distributed Lock)"]
        
        subgraph ModulosBackend ["Módulos de Negocio"]
            AuthMod["Auth Service\n(Google OAuth / JWT)"]
            ResourceMod["Catalog Service\n(Espacios y Recursos)"]
            BookingMod["Booking Service\n(Transacciones Atómicas)"]
            ChecklistMod["Checklist & Incident Service\n(Firma e Inspección)"]
            DocMod["Document Service\n(PDFKit + QR Code Crypto)"]
            NotifyMod["Notification Service\n(Nodemailer + DB Polling)"]
        end
    end

    subgraph Almacenamiento ["Capa de Datos y Estado"]
        RedisCluster[("Redis 7 In-Memory Cache\n- Locks temporales 15 min\n- Cache de catálogos\n- Blacklist de tokens")]
        PostgresDB[("PostgreSQL 16 RDBMS\n- Tablas relacionales con llaves foráneas\n- Rangos temporales tsrange\n- Prisma ORM 5.x")]
    end

    subgraph Externos ["Servicios Terceros / GCP"]
        GoogleAPI["Google Identity Services\nOAuth 2.0 (@alumnos.udg.mx / @udg.mx)"]
        MailServer["Servidor SMTP Transaccional\n(Plantillas HTML Responsivas)"]
    end

    WebApp -->|JSON / REST| Router
    Router --> AuthMid
    AuthMid --> LockMid
    LockMid --> ModulosBackend

    AuthMod --> GoogleAPI
    BookingMod --> RedisCluster
    BookingMod --> PostgresDB
    ChecklistMod --> PostgresDB
    DocMod --> PostgresDB
    NotifyMod --> MailServer
    NotifyMod --> PostgresDB
```

---

## 4. Flujos Críticos de Negocio y Seguridad

### 4.1 Flujo de Autenticación Institucional Exclusiva (Google OAuth 2.0)

**Directiva:** Únicamente se permite el acceso a usuarios con cuentas oficiales de la Universidad de Guadalajara (`@alumnos.udg.mx` para estudiantes y `@udg.mx` para académicos y administrativos).

```mermaid
sequenceDiagram
    autonumber
    actor U as Usuario (Alumno/Docente)
    participant Front as Frontend (React / Vite)
    participant Back as API (/api/v1/auth)
    participant Google as Servidor OAuth 2.0 (Google)
    participant DB as PostgreSQL (Users Table)

    U->>Front: Clic en "Iniciar con Cuenta UdeG"
    Front->>Google: Redirección a Google OAuth Consent Screen
    Google-->>U: Solicita credenciales @udg.mx / @alumnos.udg.mx
    U->>Google: Autentica exitosamente
    Google-->>Front: Redirige con Authorization Code o ID Token
    Front->>Back: POST /api/v1/auth/google { credential / token }
    Back->>Google: Valida firma de token y extrae perfil (email, hd, name, picture)
    
    alt Dominio no institucional (diferente a udg.mx o alumnos.udg.mx)
        Back-->>Front: 403 Forbidden ("Solo se permiten cuentas institucionales UdeG")
        Front-->>U: Mensaje de error visual (Alert Semántico UdeG)
    else Dominio Válido
        Back->>DB: Busca usuario por email
        opt Usuario nuevo
            Back->>DB: Registra usuario (determina rol ALUMNO o DOCENTE por dominio)
        end
        Back->>Back: Genera Access Token (15 min) + Refresh Token (7 días)
        Back-->>Front: 200 OK { user, accessToken, refreshToken }
        Front->>Front: Almacena sesión en AuthContext y redirige al Dashboard
    end
```

---

### 4.2 Flujo Anti-Empalme: Concurrencia Distribuida con Redis (15 Minutos TTL)

**Problema:** Dos usuarios seleccionan el mismo Auditorio o Laboratorio para el mismo día y bloque de horas al mismo tiempo.  
**Solución Arquitectónica:** Se implementa un mecanismo de **Reserva Temporal (Soft Lock)** en Redis con tiempo de vida (TTL) de 15 minutos mientras el usuario llena justificación, sube responsivas o invita co-responsables.

```mermaid
sequenceDiagram
    autonumber
    actor U1 as Usuario A (Solicitante)
    actor U2 as Usuario B (Competidor)
    participant API as API Server
    participant Redis as Redis 7 (Locks)
    participant DB as PostgreSQL (Bookings)

    U1->>API: POST /api/v1/bookings/pre-reserve { spaceId, start, end }
    API->>Redis: SET resource:lock:spaceId:range "userIdA" NX EX 900
    
    alt Lock Adquirido Exitosamente
        Redis-->>API: OK (Lock activo por 15 min)
        API-->>U1: 201 Created { preReservationId, expiresAt: now + 15m }
        
        note over U2: Usuario B intenta el mismo espacio y horario
        U2->>API: POST /api/v1/bookings/pre-reserve { spaceId, start, end }
        API->>Redis: SET resource:lock:spaceId:range "userIdB" NX EX 900
        Redis-->>API: NIL (Clave ya bloqueada)
        API-->>U2: 409 Conflict ("Espacio en proceso de reserva por otro usuario. Intenta en unos minutos.")
        
        alt Usuario A completa solicitud en menos de 15 min
            U1->>API: POST /api/v1/bookings/confirm { preReservationId, datos }
            API->>DB: BEGIN TRANSACTION (Verifica solapamiento tsrange e inserta Booking PENDIENTE)
            DB-->>API: COMMIT
            API->>Redis: DEL resource:lock:spaceId:range
            API-->>U1: 200 OK (Solicitud registrada en revisión)
        else Usuario A abandona la página / Expira el tiempo (15 min)
            Redis->>Redis: Clave expira automáticamente por TTL
            note over Redis: El espacio vuelve a quedar libre inmediatamente
        end
    end
```

---

### 4.3 Ciclo de Vida y Máquina de Estados de Reservas y Préstamos

```mermaid
stateDiagram-v2
    [*] --> PRE_RESERVADA: Pre-bloqueo temporal en Redis (TTL 15 min)
    PRE_RESERVADA --> CANCELADA_TIMEOUT: Expira TTL sin confirmar
    PRE_RESERVADA --> PENDIENTE_APROBACION: Confirmación con firmas de co-responsables
    
    PENDIENTE_APROBACION --> RECHAZADA: Coordinador o Técnico deniega (con motivo obligatorio)
    PENDIENTE_APROBACION --> APROBADA: Coordinador autoriza solicitud
    
    APROBADA --> EN_USO: Entrega física + Checklist inicial aprobado + QR escaneado
    
    EN_USO --> FINALIZADA: Devolución física + Checklist final sin novedades
    EN_USO --> CON_INCIDENCIA: Daño, faltante o entrega tardía (Checklist con reporte)
    
    CON_INCIDENCIA --> PENALIZADA: Técnico o Admin aplica reducción de Trust Score
    CON_INCIDENCIA --> RESUELTA: Usuario repara o restituye el bien
    
    PENALIZADA --> [*]
    RESUELTA --> [*]
    FINALIZADA --> [*]
    RECHAZADA --> [*]
    CANCELADA_TIMEOUT --> [*]
```

---

### 4.4 Verificación de Asistencia con Código QR Criptográfico

Para eventos multitudinarios en auditorios, aulas magnas y salas de conferencias:
1. El backend genera un payload con: `userId`, `bookingId`, `timestamp`, `nonce`.
2. El payload se firma digitalmente con algoritmo **HMAC-SHA256** utilizando una clave secreta del servidor.
3. Se genera la imagen QR vectorial (`qrcode`).
4. Al momento del acceso, el staff o técnico escanea el QR desde la app web o móvil.
5. El servidor valida la firma criptográfica, la vigencia temporal y marca el registro de asistencia atómico, bloqueando reusos del mismo QR.

---

### 4.5 Flujo de Responsivas Oficiales, Co-Responsables y Doble Checklist

**Directiva (RF-02.3 / RF-04.1):** Ningún recurso o espacio es entregado sin un Acta de Responsiva formal debidamente firmada por todos los involucrados y respaldada por el checklist de salida.

```mermaid
sequenceDiagram
    autonumber
    actor Sol as Solicitante Principal
    actor Co as Co-Responsable(s)
    actor Tec as Técnico / Almacén
    participant App as Frontend SIGRE
    participant API as Backend API
    participant DB as PostgreSQL
    participant Mail as Servidor Correo UdG
    participant PDF as Motor PDFKit

    Sol->>App: Registra solicitud e incluye lista de Co-Responsables
    App->>API: POST /api/v1/bookings { ..., coResponsibles: [code1, code2] }
    API->>DB: Guarda solicitud en estado PENDIENTE_FIRMAS
    API->>Mail: Dispara invitaciones a correos @alumnos.udg.mx de co-responsables
    
    loop Cada Co-Responsable
        Co->>App: Ingresa mediante enlace seguro / campana de la app
        Co->>App: Revisa términos y traza su firma digital (Canvas / Base64)
        App->>API: POST /api/v1/responsivas/:id/sign { signatureBase64, userMeta }
        API->>DB: Registra firma individual + IP + Timestamp UTC
    end

    alt Faltan firmas de co-responsables
        note over Tec,API: Condición de Bloqueo: El sistema impide emitir el acta o entregar el bien
        Tec->>App: Consulta solicitud en ventanilla
        App-->>Tec: Alerta: "Pendiente de firmas de co-responsables (2/3)" (Botón de entrega inhabilitado)
    else Todas las firmas recabadas (100%)
        API->>DB: Actualiza estado a LISTO_PARA_ENTREGA
        Sol->>Tec: Se presenta en ventanilla de laboratorio/almacén
        Tec->>App: Abre Checklist de Salida (Inspección física del equipo/espacio)
        Tec->>App: Valida ítems + adjunta foto si hay detalle previo + firma técnico
        App->>API: POST /api/v1/checklists/salida { items, signatureTecnico }
        
        API->>PDF: Compila Acta Oficial en PDF (Membrete UdeG, bienes, firmas, IP, folio hash)
        PDF-->>API: Buffer PDF generado
        API->>DB: Guarda URL/hash del acta oficial y cambia estado a EN_USO
        API->>Mail: Envía copia del acta firmada en PDF a todos los firmantes
        Tec-->>Sol: Entrega física de los recursos/llaves
    end

    note over Sol,Tec: Al concluir el periodo de uso (Devolución)
    Sol->>Tec: Devuelve recursos en almacén
    Tec->>App: Realiza Checklist de Entrada (Cotejo contra checklist de salida)
    alt Sin novedad
        Tec->>App: Checklist conforme
        App->>API: POST /api/v1/checklists/entrada { status: "OK" }
        API->>DB: Marca solicitud como FINALIZADA y abona puntos al Trust Score
    else Daño o faltante detectado
        Tec->>App: Checklist con anomalía + Fotos de evidencia
        App->>API: POST /api/v1/incidents { photos, description, severity }
        API->>DB: Marca CON_INCIDENCIA, resta Trust Score y abre Expediente de Reparación
    end
```

#### Reglas de Integridad del Acta Responsiva:
1. **Condición de Bloqueo Estricto:** La API rechaza cualquier intento de pasar el estado a `EN_USO` o `DELIVERED` si el contador de firmas confirmadas es menor al número de custodios registrados.
2. **No Repudio:** Cada trazo de firma se almacena en Base64 junto con el Hash SHA-256 del contenido del documento, dirección IP remota y marca de tiempo en milisegundos.
3. **Copia Inmutable:** El archivo PDF resultante se almacena con nombre canónico (`actas/RESP-AÑO-FOLIO.pdf`) y se distribuye copia digital por correo a las cuentas `@alumnos.udg.mx` de todos los involucrados.


---

## 5. Estrategia de Despliegue en la Nube (GCP Cloud Run)

La arquitectura de despliegue está optimizada para **Google Cloud Platform (GCP)** aprovechando la eficiencia de costos y escalabilidad automática a cero cuando no hay tráfico:

```mermaid
flowchart LR
    subgraph GitHub["GitHub Repository"]
        Actions["GitHub Actions CI/CD\n(.github/workflows/deploy.yml)"]
    end

    subgraph GCP["Google Cloud Platform (GCP)"]
        ArtifactReg["Artifact Registry\n(Docker Containers)"]
        
        subgraph ServerlessCompute["Cómputo Serverless"]
            CR_API["Cloud Run: sigre-api\n(Node.js REST API Container)"]
            CR_Web["Cloud Run / Firebase Hosting: sigre-web\n(Nginx + React SPA Container)"]
        end

        subgraph ManagedData["Datos Persistentes Gestionados"]
            CloudSQL[("Cloud SQL\nPostgreSQL 16 Instance")]
            Memorystore[("Cloud Memorystore\nRedis 7 Instance")]
            CloudStorage["Cloud Storage (GCS)\n(Actas PDF, Evidencia fotográfica)"]
        end
    end

    Actions -->|1. Test & Build Docker Images| ArtifactReg
    ArtifactReg -->|2. Despliegue automatizado| CR_API
    ArtifactReg -->|2. Despliegue automatizado| CR_Web
    CR_API -->|VPC Connector| CloudSQL
    CR_API -->|VPC Connector| Memorystore
    CR_API -->|Cloud Storage SDK| CloudStorage
```

### Ventajas de esta arquitectura en GCP:
- **Zero Idle Cost:** Cloud Run escala a 0 instancias en noches o vacaciones escolares cuando no hay solicitudes.
- **Seguridad perimetral:** Las conexiones entre Cloud Run, Cloud SQL y Memorystore se realizan mediante VPC Privada (Serverless VPC Access Connector), sin exponer puertos de base de datos a internet público.
- **Certificados SSL automáticos:** Gestión de HTTPS transparente con dominios institucionales.

---

## 6. Sistema de Diseño e Identidad Visual (Design Tokens)

Toda la interfaz del sistema se rige estrictamente por la **Guía de Identidad de Marca** ([docs/sigre_brand_identity.md](file:///c:/Users/erfierro/Documents/Inversion/docs/sigre_brand_identity.md)):

| Token de Marca | Valor Hex | Significado Institucional |
|:---|:---|:---|
| `--color-primary` | `#002B49` | **Azul Institucional UdeG** (Seriedad, patrimonio, confianza) |
| `--color-accent` | `#2E7D57` | **Verde Natural CUTonalá** (Campus sustentable, transparencia, activos) |
| `--color-bridge` | `#1A6B5A` | **Transición Azul-Verde** (Interacciones hover, gradiente del logo "S") |
| `--bg-base` | `#FFFFFF` / `#0D1B2A` | Modo claro y modo oscuro profundo |
| `--font-family` | `'Outfit', sans-serif` | Tipografía geométrica institucional moderna |
| `--font-mono` | `'JetBrains Mono', monospace` | Para códigos de inventario, folios y firmas QR |

---

## 7. Próximos Pasos Técnicos para Completar el Sistema

1. **Infraestructura Base:** Ejecutar `docker compose up -d` en `infra/` para levantar PostgreSQL y Redis.
2. **Esquema de Datos:** Aplicar las migraciones de Prisma y poblar el catálogo de espacios y roles con `prisma db seed`.
3. **Controladores Backend:** Terminar los endpoints pendientes de acuerdo al plan maestro.
4. **Vistas Frontend:** Montar la interfaz con React 18, Vite y los tokens de diseño de SIGRE.
5. **Pipeline CI/CD:** Configurar el archivo `.github/workflows/deploy.yml` para despliegue automatizado en GCP Cloud Run.
