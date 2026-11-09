# ✍️ Módulo: Responsivas Digitales, Co-Responsables y Firmas

**Etiquetas:** `#responsivas` `#firmas-digitales` `#co-responsables` `#pdfkit` `#legal` `#sigre`  
**Referencia Requerimientos:** [RF-02.3](file:///c:/Users/erfierro/Documents/Inversion/requirements/funcionales/RF_SIGRE_Espacios_Materiales_Eventos.md#L45) | [RF-04.1](file:///c:/Users/erfierro/Documents/Inversion/requirements/funcionales/RF_SIGRE_Espacios_Materiales_Eventos.md#L53) | [RT-04](file:///c:/Users/erfierro/Documents/Inversion/requirements/tecnicos/RT_SIGRE_Arquitectura_Seguridad_Datos.md#L31)

---

## 1. Definición del Módulo
Regula y formaliza la custodia jurídica y administrativa de los espacios y materiales del CUTonalá. Toda solicitud autorizada de préstamo o uso de espacio requiere la emisión y firma de un **Acta de Responsiva Oficial** antes de que el bien o aula sea entregado físicamente.

---

## 2. Flujo de Co-Responsables (Firmas Múltiples)

Cuando un evento o préstamo involucra a un grupo de estudiantes o profesores (ej. proyecto modular, congreso o práctica de laboratorio grupal):

1. **Designación:** El solicitante principal agrega los códigos de estudiante y correos institucionales de los **Co-Responsables**.
2. **Notificación:** El sistema envía una notificación (por correo institucional y en la campana de la app) a cada co-responsable con el enlace a la solicitud.
3. **Condición de Bloqueo Estricto:**
   > **Regla RF-02.3:** El acta oficial de responsiva **NO se emite** y el almacén/laboratorio **NO puede entregar el equipo/espacio** hasta que el solicitante y el **100% de los co-responsables** hayan firmado digitalmente la aceptación de términos.
4. **Firma del Técnico/Administrador:** Una vez recabadas las firmas de los usuarios, el encargado de laboratorio firma el acta al momento de la entrega física.

---

## 3. Mecanismo de Firma Digital y Trazabilidad

Para garantizar la validez y no repudio dentro del marco universitario:
- **Captura de Firma:** Componente Canvas en el Frontend (`apps/web`) para trazo táctil o con ratón, serializado a cadena Base64 (`image/png`).
- **Huella Digital de Auditoría:** Por cada firma se captura:
  - `userId` y `codigoEstudiante`.
  - Timestamp exacto en formato ISO UTC.
  - Dirección IP del dispositivo solicitante.
  - Declaración explícita de aceptación de los reglamentos del CUTonalá.
- **Folio Criptográfico Único:** Identificador alfanumérico generado con hash SHA-256 (ej. `RESP-2026-CUT-00482`).

---

## 4. Estructura del Documento PDF Oficial (PDFKit)

El backend compila el acta en PDF con las siguientes secciones:
1. **Membrete Oficial:** Escudo de la Universidad de Guadalajara, logotipo del Centro Universitario de Tonalá e isotipo de SIGRE.
2. **Datos de los Custodios:** Nombre completo, código de estudiante, carrera y correo de todos los firmantes.
3. **Inventario Pormenorizado:** Lista de bienes entregados (número de serie, número patrimonial UdeG, marca, modelo y estado físico inicial según checklist).
4. **Declaración de Responsabilidad:** Cláusulas de conservación, plazos improrrogables de devolución y consecuencias de daño/pérdida.
5. **Bloque de Firmas Estilizado:**
   - Firma del Solicitante Principal.
   - Firmas de los Co-Responsables.
   - Firma del Encargado de Laboratorio / Almacén.
   - Sellos de tiempo, IP y código QR de verificación del documento.

---

## 5. Enlaces Relacionados
- [[Modulos/Checklists_e_Incidencias|Checklists de Entrega y Devolución]]
- [[Modulos/Reservas_y_Prestamos|Ciclo de Reservas y Préstamos]]
- [[Modulos/Notificaciones_y_PDF|Servicio de Notificaciones y PDF]]
- [[Arquitectura/Index|Arquitectura General]]
