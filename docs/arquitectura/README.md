# 🏛️ Documentación de Arquitectura — SIGRE

Bienvenido a la sección de arquitectura de software del **Sistema Integrado de Gestión de Recursos y Espacios (SIGRE)** para el **Centro Universitario de Tonalá (CUTonalá) — Universidad de Guadalajara**.

---

## 📑 Documentos Oficiales

- **[ARQUITECTURA_SIGRE.md](file:///c:/Users/erfierro/Documents/Inversion/docs/arquitectura/ARQUITECTURA_SIGRE.md)**:  
  Documento maestro de arquitectura del sistema. Contiene:
  - Visión general del ecosistema y actores del CUTonalá.
  - Estructura de Monorepo con Turborepo (`apps/api`, `apps/web`, `packages/database`, `packages/shared`).
  - Diagramas de contenedores y servicios en Mermaid.
  - Flujo de autenticación institucional exclusiva con Google Workspace UdG (`@alumnos.udg.mx` y `@udg.mx`).
  - Mecanismo anti-empalme y bloqueo temporal de concurrencia con Redis 7 (TTL 15 min).
  - Ciclo de vida y máquina de estados de reservaciones y préstamos.
  - Verificación criptográfica con Código QR (HMAC-SHA256) para eventos.
  - Generador de actas y responsivas en PDF oficial con firmas digitales.
  - Estrategia de despliegue en la nube mediante **Google Cloud Platform (GCP Cloud Run + Cloud SQL + Memorystore)**.
  - Integración del sistema de diseño y tokens de marca basados en la [Guía de Identidad de Marca](file:///c:/Users/erfierro/Documents/Inversion/docs/sigre_brand_identity.md).
