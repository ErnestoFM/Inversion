# Requerimientos Técnicos: SIGRE (Sistema Integrado de Gestión de Recursos y Espacios)

## 📌 Stack Tecnológico
- **Frontend:** React 18+ con TypeScript + Vite + Tailwind CSS / Vanilla CSS moderno
- **Backend:** Node.js + Express + TypeScript
- **Base de Datos:** PostgreSQL 16 + Prisma ORM
- **Caché y Tareas:** Redis 7
- **Mailing / Notificaciones:** Nodemailer con plantillas HTML responsivas (SMTP) + Campana de notificaciones en tiempo real (Polling / WebSockets)
- **Infraestructura:** Docker Compose (local) y preparado para GCP Cloud Run

---

## 🛠️ Especificaciones Técnicas y Módulos de Soporte

### RT-01: Sistema de Notificaciones Dual (Correo + Campana en App)
- **RT-01.1:** Servicio de correo transaccional (`apps/api/src/services/mail.service.ts`) con plantillas HTML para:
  - Confirmación y activación de cuenta.
  - Notificación de pre-reserva e invitaciones a co-responsables para firma de responsiva.
  - Aprobación / Rechazo de solicitud de evento o préstamo.
  - Recordatorio 1 hora antes de devolución de material o inicio de evento.
- **RT-01.2:** Sistema de notificaciones internas en base de datos (`notifications` table) con indicador de no leídas en la interfaz de React.

### RT-02: Control de Concurrencia y Pre-Reservas (Anti-Empalme)
- **RT-02.1:** Bloqueo temporal en Redis (TTL configurable de 15 minutos) durante el llenado y revisión de la solicitud para evitar empalmes.
- **RT-02.2:** Transacciones atómicas en PostgreSQL con comprobación de solapamiento de rangos temporales (`tsrange`).

### RT-03: Generación y Validación de Códigos QR
- **RT-03.1:** Generación de payloads criptográficos firmados (JWT efímero / HMAC) dentro del QR con `userId`, `eventId`, `studentCode` y `timestamp`.
- **RT-03.2:** Endpoint de escaneo para organizadores/administradores que valida y marca al usuario como `ASISTIÓ` en tiempo real, bloqueando el reuso.

### RT-04: Generador de Actas y Responsivas en PDF
- **RT-04.1:** Motor de plantillas PDF (`PDFKit`) que genera el documento oficial con número de folio, firmas digitales en base64 de todos los co-responsables y del administrador, sellos de tiempo e IP.
- **RT-04.2:** Almacenamiento seguro y trazabilidad en base de datos.
