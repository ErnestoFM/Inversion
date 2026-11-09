# 📦 Índice de Módulos del Sistema — SIGRE

Catálogo oficial de especificaciones de módulos funcionales y servicios del **Sistema Integrado de Gestión de Recursos y Espacios (SIGRE)** en CUTonalá:

- **[[Modulos/Autenticacion_Google|Autenticación y Seguridad UdG]]**: Inicio de sesión exclusivo con Google Workspace (`@alumnos.udg.mx` y `@udg.mx`), JWT dual (Access/Refresh) y control de acceso basado en roles (RBAC).
- **[[Modulos/Gestion_Espacios|Gestión de Espacios Físicos]]**: Catálogo de aulas, laboratorios y auditorios del CUTonalá, capacidades, normas y calendarios de disponibilidad.
- **[[Modulos/Gestion_Recursos|Gestión de Recursos y Materiales]]**: Inventario físico de equipo audiovisual, cómputo especializado y consumibles, trazabilidad por número de serie.
- **[[Modulos/Reservas_y_Prestamos|Reservaciones y Préstamos]]**: Máquina de estados del ciclo de solicitud, revisión por coordinadores y aprobación.
- **[[Modulos/Responsivas_Digitales_y_Firmas|Responsivas Oficiales, Co-Responsables y Firmas]]**: Bloqueo de entrega condicionado a la firma del 100% de co-responsables, firmas digitales en Base64 y generación de actas oficiales.
- **[[Modulos/Concurrencia_Redis|Control de Concurrencia y Anti-Empalme]]**: Bloqueo distribuido temporal en Redis (TTL 15 min) para evitar solicitudes duplicadas o colisiones de horario.
- **[[Modulos/Checklists_e_Incidencias|Checklists de Inspección, Incidencias y Trust Score]]**: Verificación digital en entrega y devolución (doble checklist), reporte fotográfico de averías y cálculo del score de confiabilidad del usuario.
- **[[Modulos/Notificaciones_y_PDF|Notificaciones y Generación de Actas PDF]]**: Servicio dual de correo transaccional (Nodemailer), campana web en tiempo real y generación oficial de actas con firmas criptográficas (PDFKit).
- **[[Modulos/Marco_Legal_y_Privacidad|Marco Legal, Privacidad y Cookies]]**: Cumplimiento de la LGPDPPSO (INAI/ITEI), política de cookies técnicas seguras y esquema de URLs prefirmadas en GCS.
- **[[Modulos/Despliegue_y_DevOps|Despliegue en la Nube y DevOps (GCP & CI/CD)]]**: Arquitectura serverless en Google Cloud Run, contenedores Docker multi-stage optimizados y pipeline automatizado con GitHub Actions.
