# 🏛️ Índice de Arquitectura — SIGRE

Documentación arquitectónica del **Sistema Integrado de Gestión de Recursos y Espacios (SIGRE)** para el **Centro Universitario de Tonalá (CUTonalá) — Universidad de Guadalajara**:

---

## 📌 Documento Maestro
- **[ARQUITECTURA_SIGRE.md](file:///c:/Users/erfierro/Documents/Inversion/docs/arquitectura/ARQUITECTURA_SIGRE.md)**: Especificación integral con diagramas Mermaid de contenedores, flujos de autenticación institucional, anti-empalme con Redis y despliegue serverless en GCP Cloud Run.

---

## 🧩 Componentes y Patrones de Arquitectura

1. **Monorepo Turborepo (`apps/` y `packages/`):**
   - `apps/web`: Frontend SPA en React 18 + Vite con tokens de diseño basados en la [Guía de Identidad de Marca](file:///c:/Users/erfierro/Documents/Inversion/docs/sigre_brand_identity.md) (Outfit, Azul Institucional `#002B49`, Verde Natural `#2E7D57`).
   - `apps/api`: Backend Node.js + Express + TypeScript estructurado en capas (rutas, controladores, middleware, servicios).
   - `packages/database`: Capa de persistencia con PostgreSQL 16 y Prisma ORM.
   - `packages/shared`: Validaciones comunes con Zod y tipado TypeScript unificado.

2. **Seguridad y Control de Acceso:**
   - Single Sign-On (SSO) exclusivo mediante **Google Workspace UdG** (`@alumnos.udg.mx` y `@udg.mx`).
   - Emisión de JWT dual (`accessToken` de 15 minutos y `refreshToken` de 7 días).
   - Control de acceso basado en roles: `ALUMNO`, `DOCENTE`, `COORDINADOR`, `TECNICO`, `ADMIN`.

3. **Concurrencia Distribuida y Anti-Empalme:**
   - Bloqueo temporal en Redis 7 con TTL de 15 minutos (`SET NX EX 900`) durante el proceso de solicitud.
   - Transacción atómica en PostgreSQL con comprobación de solapamiento de rangos de tiempo.

4. **Infraestructura y Nube (GCP):**
   - Desarrollo local mediante Docker Compose (`infra/docker-compose.yml`) con PostgreSQL 16 y Redis 7.
   - Despliegue en producción proyectado a **Google Cloud Platform (GCP)** con **Cloud Run** (cómputo serverless en contenedores), **Cloud SQL** (PostgreSQL administrado) y **Memorystore** (Redis administrado).

---

## 🔗 Enlaces a Módulos Relacionados
- [[Modulos/Autenticacion_Google|Autenticación Google]]
- [[Modulos/Concurrencia_Redis|Concurrencia con Redis]]
- [[Modulos/Reservas_y_Prestamos|Reservas y Préstamos]]
- [[Modulos/Checklists_e_Incidencias|Checklists e Incidencias]]
- [[Modulos/Notificaciones_y_PDF|Notificaciones, QR y PDF]]
