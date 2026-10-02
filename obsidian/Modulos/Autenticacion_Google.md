# 🔐 Módulo: Autenticación Institucional UdG

**Etiquetas:** `#seguridad` `#auth` `#google-oauth` `#jwt` `#sigre`  
**Referencia Técnica:** [auth.routes.ts](file:///c:/Users/erfierro/Documents/Inversion/apps/api/src/routes/auth.routes.ts) | [ARQUITECTURA_SIGRE.md](file:///c:/Users/erfierro/Documents/Inversion/docs/arquitectura/ARQUITECTURA_SIGRE.md)

---

## 1. Definición del Módulo
Garantiza que el acceso al sistema esté restringido exclusivamente a la comunidad del **Centro Universitario de Tonalá (Universidad de Guadalajara)** mediante Single Sign-On (SSO) con Google Workspace.

## 2. Reglas de Validación
- **Dominios Permitidos:**
  - `@alumnos.udg.mx`: Rol asignado automáticamente como `ALUMNO`.
  - `@udg.mx`: Rol asignado automáticamente como `DOCENTE` (o administrativo).
  - Cualquier otro dominio personal (`@gmail.com`, `@hotmail.com`) es rechazado con código `403 Forbidden`.
- **Estructura de Tokens:**
  - `accessToken`: JWT firmado con algoritmo HS256, vigencia corta de **15 minutos**.
  - `refreshToken`: Almacenado de forma segura, vigencia de **7 días**. Permite renovación continua sin re-autenticar en Google.
  - Cierre de sesión (`logout`): Invalida el identificador único del token (`jti`) colocándolo en la lista negra en Redis.

## 3. Enlaces Relacionados
- [[Arquitectura/Index|Arquitectura General]]
- [[Modulos/Index|Volver al Índice de Módulos]]
