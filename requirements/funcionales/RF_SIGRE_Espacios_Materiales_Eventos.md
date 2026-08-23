# Requerimientos Funcionales: SIGRE (Sistema Integrado de Gestión de Recursos y Espacios)

## 📌 Información General
- **Proyecto:** SIGRE (Sistema Integrado de Gestión de Recursos y Espacios)
- **Institución:** Centro Universitario de Tonalá (CUTonalá - Universidad de Guadalajara)
- **Enfoque Académico:** Formulación y Evaluación de Proyectos de Inversión

---

## 👥 Actores del Sistema
1. **Comunidad Estudiantil y Docente (Solicitantes / Asistentes):**
   - Registro con confirmación de correo institucional o Google OAuth.
   - Creación de propuestas de eventos (con pre-reserva de espacios y materiales).
   - Asignación de **Co-Responsables** para eventos grupales o complejos.
   - Solicitudes de préstamo de materiales con selección personalizada de fecha/hora de inicio y fin.
   - Registro a eventos públicos y privados; generación de boleto digital con código QR dinámico e intransferible.
   - Sistema de reseñas verificado (solo habilitado si el QR fue escaneado como asistente).
   - Aceptación de términos y normas, subida de firma digital y código de estudiante.
2. **Administración / Encargado de Almacén y Espacios:**
   - Evaluación y aprobación o rebote motivado de solicitudes de préstamos/eventos (ej. "Rechazado: máximo 2 días de préstamo para este equipo").
   - Consulta del historial y **Puntaje de Confiabilidad** del solicitante y co-responsables.
   - Doble Checklist Digital: Verificación en entrega física y recepción final.
   - Registro de incidencias (daños/retrasos/extravío) y apertura del flujo de **Reparación de Daños Supervisada**.
   - Validación de accesos mediante escáner de QR en puerta.
   - Firma digital de aceptación en actas de responsiva.
3. **Superadministrador / Coordinación:**
   - Acceso al **Dashboard Ejecutivo de Evaluación de Inversión** con métricas clave de impacto y aprovechamiento del patrimonio.

---

## 📋 Módulos y Requerimientos Funcionales

### RF-01: Autenticación, Verificación y Perfil con Reputación
- **RF-01.1:** Registro con correo institucional (`@alumnos.udg.mx` / `@academicos.udg.mx`) con activación vía token criptográfico o acceso directo con Google OAuth.
- **RF-01.2:** **Sistema de Puntos y Confiabilidad (Score de Reputación):**
  - Cada usuario inicia con 100 puntos.
  - Entregas puntuales y conformes mantienen/suman reputación.
  - Retrasos menores restan puntos (Advertencias).
  - Incidencias graves (daño a equipo, no-show reiterado) suspenden temporalmente las solicitudes automáticas.
- **RF-01.3:** **Flujo de Reparación de Daños Supervisado:** En caso de daño o pérdida, Almacén abre un expediente donde el usuario se compromete a la reposición o reparación con seguimiento formal en la plataforma.

### RF-02: Solicitudes Flexibles de Préstamo y Espacios con "Rebote Motivado"
- **RF-02.1:** El usuario solicita fechas y horas personalizadas para el préstamo o reserva.
- **RF-02.2:** La administración evalúa y puede **Aprobar** o **Rebotar con Motivo** (feedback específico: *“El espacio se autoriza solo hasta las 6:00 PM por cierre de edificio”*).
- **RF-02.3:** Si se solicitan co-responsables, el acta de responsiva no se emite hasta que todos firmen digitalmente desde la app o enlace en correo.

### RF-03: Cartelera, Cineteca y Reseñas Verificadas
- **RF-03.1:** Cartelera centralizada con clasificación: Público, Privado por Perfil (carrera/semestre) y Privado por Código.
- **RF-03.2:** Boleto digital con QR firmado; escaneo en puerta con cambio de estado a `ASISTIÓ`.
- **RF-03.3:** **Reseñas Verificadas:** Solo los asistentes con registro de asistencia confirmado pueden calificar (1 a 5 estrellas) y comentar sobre el evento o la proyección de la Cineteca.

### RF-04: Responsivas Oficiales y Doble Checklist
- **RF-04.1:** Generación del acta PDF con sellos criptográficos, folio oficial y firmas de las partes.
- **RF-04.2:** Doble Checklist (salida y entrada) para garantizar que los bienes se entregaron completos y funcionando.

### RF-05: Dashboard Ejecutivo de Evaluación de Inversión
- **RF-05.1:** Métricas en tiempo real de aprovechamiento del patrimonio institucional.
