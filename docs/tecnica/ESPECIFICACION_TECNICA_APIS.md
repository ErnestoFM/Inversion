# 🔌 Especificación Técnica de APIs — SIGRE v1.0

**Proyecto:** SIGRE (Sistema Integrado de Gestión de Recursos y Espacios)  
**Base URL:** `/api/v1`  
**Protocolo:** HTTPS / JSON REST  
**Autenticación:** HTTP Bearer Header con JSON Web Token (`Authorization: Bearer <accessToken>`)  

---

## 1. Directivas de Seguridad y Headers

- **Content-Type:** `application/json`
- **Rate Limiting:** Máximo 100 peticiones por ventana de 15 minutos por IP (configurable en Redis).
- **CORS:** Restringido a los orígenes autorizados del frontend (ej. `http://localhost:5173` en local y `https://sigre.cutonala.udg.mx` en producción).
- **Control de Acceso:** Basado en Roles (`ADMIN`, `COORDINADOR`, `TECNICO`, `DOCENTE`, `ALUMNO`).

---

## 2. Respuestas Estándar del Sistema

### Éxito (HTTP 200 / 201)
```json
{
  "success": true,
  "data": { ... },
  "message": "Operación completada con éxito"
}
```

### Error de Validación (HTTP 400 Bad Request)
```json
{
  "success": false,
  "error": "VALIDATION_ERROR",
  "details": [
    { "field": "startTime", "message": "La fecha de inicio debe ser posterior a la actual" }
  ]
}
```

### Conflicto de Concurrencia (HTTP 409 Conflict)
```json
{
  "success": false,
  "error": "RESOURCE_LOCKED",
  "message": "El espacio seleccionado se encuentra en proceso de reserva por otro usuario. Intenta más tarde."
}
```

---

## 2.1 Reglas de Validación de Negocio (Políticas CUTonalá)

Todas las solicitudes procesadas por los validadores Zod en el backend deben cumplir obligatoriamente:

1. **Horario de Operación del Campus:**
   - Días hábiles de servicio: **Lunes a Sábado**.
   - Franja horaria permitida: **08:00 hrs a 19:00 hrs** (UTC-6).
   - Domingos e intentos fuera de esta ventana retornan `400 Bad Request`.
2. **Ventana de Antelación para Espacios Físicos:**
   - **Antelación mínima obligatoria:** **3 días naturales** (72 horas) previos al evento (requerido para limpieza, montaje y habilitación técnica).
   - **Antelación máxima permitida:** **15 días naturales** previos al evento (evita acaparamiento preventivo ocioso).
3. **Plazos y Políticas de Préstamo de Materiales:**
   - **Préstamo Ordinario (Cámaras, Proyectores, Audio, Cables):** Máximo **3 días** (72 horas).
   - **Préstamo Extendido (Equipo de Cómputo / Laptops):** Para proyectos modulares, desarrollo o prácticas extendidas, se permite hasta **30 días naturales** (1 mes). Requiere flag `isExtendedLoan: true`, justificación académica y visto bueno explícito de Coordinación.
4. **Política de Archivos y URLs Prefirmadas (Google Cloud Storage):**
   - **Archivos Privados:** Actas responsivas en PDF (`/api/v1/responsivas/:id/signed-url`) y fotografías de evidencia de averías. Se generan URLs firmadas con expiración de **15 minutos**.
   - **Archivos Públicos:** Pósters de la Cineteca y fotos de aulas para renderizado instantáneo en CDN.

---

## 3. Catálogo de Endpoints por Módulo

### 3.1 Módulo: Autenticación Institucional (`/api/v1/auth`)

| Método | Endpoint | Roles Permitidos | Descripción |
|:---|:---|:---|:---|
| `POST` | `/auth/google` | Público | Autentica con ID token de Google Workspace UdG (`@alumnos.udg.mx` o `@udg.mx`). Retorna JWT. |
| `POST` | `/auth/refresh` | Público | Renueva el `accessToken` usando un `refreshToken` válido. |
| `POST` | `/auth/logout` | Autenticado | Revoca el token actual (añadiendo el JTI a la lista negra en Redis). |
| `GET` | `/auth/me` | Autenticado | Obtiene la información del perfil del usuario en sesión con su Trust Score. |

---

### 3.2 Módulo: Espacios Físicos (`/api/v1/spaces`)

| Método | Endpoint | Roles Permitidos | Descripción |
|:---|:---|:---|:---|
| `GET` | `/spaces` | Público / Todos | Lista espacios (aulas, laboratorios, auditorios) con filtros de capacidad y tipo. |
| `GET` | `/spaces/:id` | Público / Todos | Detalle de un espacio, equipamiento, capacidad, fotos y normas de uso. |
| `GET` | `/spaces/:id/availability` | Todos | Consulta calendario de disponibilidad y franjas horarias ocupadas. |
| `POST` | `/spaces` | `ADMIN` | Registra un nuevo espacio en el catálogo del CUTonalá. |
| `PUT` | `/spaces/:id` | `ADMIN` | Actualiza características o capacidad del espacio. |
| `PATCH` | `/spaces/:id/status` | `ADMIN`, `COORDINADOR` | Cambia estado (`DISPONIBLE`, `MANTENIMIENTO`, `FUERA_DE_SERVICIO`). |

---

### 3.3 Módulo: Recursos y Materiales (`/api/v1/resources`)

| Método | Endpoint | Roles Permitidos | Descripción |
|:---|:---|:---|:---|
| `GET` | `/resources` | Todos | Lista inventario de materiales (cámaras, laptops, proyectores, cables). |
| `GET` | `/resources/:id` | Todos | Ficha técnica de un recurso, número de serie y condición física actual. |
| `POST` | `/resources` | `ADMIN`, `TECNICO` | Alta de un nuevo recurso en inventario. |
| `PUT` | `/resources/:id` | `ADMIN`, `TECNICO` | Modifica datos o especificaciones técnicas del recurso. |
| `DELETE` | `/resources/:id` | `ADMIN` | Da de baja lógica un recurso obsoleto o extraviado. |

---

### 3.4 Módulo: Reservaciones de Espacios / Eventos (`/api/v1/events` / `/bookings`)

| Método | Endpoint | Roles Permitidos | Descripción |
|:---|:---|:---|:---|
| `POST` | `/bookings/pre-reserve` | `ALUMNO`, `DOCENTE` | Adquiere bloqueo temporal de 15 minutos en Redis para el espacio/horario solicitado. |
| `POST` | `/bookings/confirm` | `ALUMNO`, `DOCENTE` | Confirma la solicitud de reserva con justificación y co-responsables. |
| `GET` | `/bookings/my-bookings` | Autenticado | Historial y estado de las reservaciones del usuario activo. |
| `GET` | `/bookings/pending` | `COORDINADOR`, `ADMIN` | Bandeja de solicitudes pendientes de revisión. |
| `PATCH` | `/bookings/:id/approve` | `COORDINADOR`, `ADMIN` | Aprueba la solicitud y dispara correo transaccional de confirmación. |
| `PATCH` | `/bookings/:id/reject` | `COORDINADOR`, `ADMIN` | Rechaza la solicitud con motivo obligatorio y notifica al solicitante. |
| `GET` | `/bookings/:id/qr` | Solicitante / Admin | Genera el código QR criptográfico para control de acceso y asistencia. |
| `POST` | `/bookings/:id/attendance` | `TECNICO`, `ADMIN` | Escanea QR y registra la asistencia oficial al evento. |

---

### 3.5 Módulo: Préstamos de Materiales (`/api/v1/loans`)

| Método | Endpoint | Roles Permitidos | Descripción |
|:---|:---|:---|:---|
| `POST` | `/loans` | `ALUMNO`, `DOCENTE` | Crea una solicitud de préstamo de uno o más artículos. |
| `GET` | `/loans/my-loans` | Autenticado | Lista de préstamos activos e históricos del usuario. |
| `GET` | `/loans/active` | `TECNICO`, `ADMIN` | Tablero de control de préstamos en curso para entrega/recepción en ventanilla. |
| `PATCH` | `/loans/:id/deliver` | `TECNICO` | Entrega física de material con firma de checklist inicial y acta responsiva. |
| `PATCH` | `/loans/:id/return` | `TECNICO` | Recepción física con checklist de inspección y cierre de préstamo. |

---

### 3.6 Módulo: Checklists de Inspección e Incidencias (`/api/v1/checklists`)

| Método | Endpoint | Roles Permitidos | Descripción |
|:---|:---|:---|:---|
| `GET` | `/checklists/:targetId` | `TECNICO`, `ADMIN` | Obtiene la plantilla de checklist para el recurso o espacio específico. |
| `POST` | `/checklists/submit` | `TECNICO` | Registra el checklist de entrega o devolución con fotos de evidencia y firmas. |
| `POST` | `/incidents` | `TECNICO`, `ADMIN` | Registra una incidencia (avería, pérdida, retraso grave). |
| `PATCH` | `/incidents/:id/resolve` | `ADMIN` | Marca una incidencia como subsanada o aplica ajuste en el Trust Score. |

---

### 3.7 Módulo: Notificaciones del Sistema (`/api/v1/notifications`)

| Método | Endpoint | Roles Permitidos | Descripción |
|:---|:---|:---|:---|
| `GET` | `/notifications` | Autenticado | Obtiene las notificaciones del usuario (campana en interfaz). |
| `PATCH` | `/notifications/:id/read`| Autenticado | Marca una notificación específica como leída. |
| `PATCH` | `/notifications/read-all`| Autenticado | Marca todas las notificaciones del usuario como leídas. |
