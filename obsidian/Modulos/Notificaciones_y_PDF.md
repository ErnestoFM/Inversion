# 🔔 Módulo: Notificaciones, QR y Generador de Actas PDF

**Etiquetas:** `#notificaciones` `#email` `#qr` `#pdf` `#responsivas` `#sigre`  
**Referencia Técnica:** [RT_SIGRE_Arquitectura_Seguridad_Datos.md](file:///c:/Users/erfierro/Documents/Inversion/requirements/tecnicos/RT_SIGRE_Arquitectura_Seguridad_Datos.md)

---

## 1. Sistema Dual de Notificaciones
- **Canal 1 (Correo Transaccional):** Envíos automáticos con plantillas HTML responsivas para:
  - Notificación de pre-reserva e invitación a co-responsables.
  - Dictamen de aprobación o rechazo con motivo oficial.
  - Recordatorio 1 hora antes de devolución de material o inicio de evento.
- **Canal 2 (Campana en Plataforma):** Contador de avisos no leídos en el header de la aplicación React con marcado de lectura instantáneo.

## 2. Generación y Validación de Código QR
- Payload efímero firmado criptográficamente con HMAC-SHA256 (`userId`, `bookingId`, `timestamp`).
- Permite al personal del evento escanear y validar asistencia en tiempo real, bloqueando códigos duplicados.

## 3. Generador de Actas Oficiales y Responsivas (PDFKit)
- Crea el documento con formato oficial de la Universidad de Guadalajara.
- Integra firmas digitales en Base64, huella digital (IP + Timestamp), desglose de bienes asignados y advertencias legales de custodia.

## 4. Enlaces Relacionados
- [[Modulos/Reservas_y_Prestamos|Módulo de Reservas]]
- [[Arquitectura/Index|Arquitectura General]]
