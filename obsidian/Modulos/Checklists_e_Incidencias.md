# 📋 Módulo: Checklists de Inspección, Incidencias y Trust Score

**Etiquetas:** `#checklist` `#inspeccion` `#incidencias` `#trust-score` `#responsivas` `#sigre`  
**Referencia Técnica:** [ESPECIFICACION_TECNICA_APIS.md](file:///c:/Users/erfierro/Documents/Inversion/docs/tecnica/ESPECIFICACION_TECNICA_APIS.md) | [RF-04](file:///c:/Users/erfierro/Documents/Inversion/requirements/funcionales/RF_SIGRE_Espacios_Materiales_Eventos.md#L52)

---

## 1. Definición del Módulo
Garantiza la corresponsabilidad y cuidado de las instalaciones y equipo del CUTonalá mediante un sistema de inspección digital de doble vía (salida y entrada), vinculado estrechamente con el [[Modulos/Responsivas_Digitales_y_Firmas|Acta de Responsiva Oficial]] y el puntaje de confiabilidad del usuario (*Trust Score*).

---

## 2. Doble Checklist Digital (Salida y Entrada)

### A. Checklist de Salida (Entrega Física)
- Realizado en ventanilla por el técnico en conjunto con el solicitante.
- Verificación ítem por ítem: encendido, cables completos, estado estético, accesorios.
- **Condición de emisión:** La firma del checklist de salida aprueba la generación final del [[Modulos/Responsivas_Digitales_y_Firmas|Acta Responsiva]] y habilita el cambio de estado a `EN_USO`.

### B. Checklist de Entrada (Devolución Física)
- Inspección al recibir el bien o revisar el aula tras el evento.
- Si el estado coincide con el checklist de salida, se cierra la solicitud (`FINALIZADA`) y se abonan puntos de confiabilidad.
- Si hay faltantes o averías, se activa el registro de **Incidencia** con captura fotográfica obligatoria.

---

## 3. Flujo de Incidencias y Reparación Supervisada
- **Registro:** El técnico describe la anomalía, adjunta fotos y clasifica la gravedad (`LEVE`, `MODERADA`, `GRAVE`).
- **Expediente de Reparación Supervisada (RF-01.3):** Almacén abre un expediente formal donde el solicitante y co-responsables asumen el compromiso de reparación o reposición del bien con plazo estipulado.

---

## 4. Sistema de Confianza (Trust Score)
- **Base Inicial:** 100 puntos.
- **Bonificaciones (+):** Devoluciones impecables y puntuales (+2 puntos por ciclo).
- **Penalizaciones (-):**
  - Retraso menor (< 2 horas): -5 puntos.
  - Retraso grave (> 24 horas): -20 puntos.
  - No presentarse a un espacio reservado (*No-Show*): -15 puntos.
  - Daño o avería por mal uso: -30 puntos y suspensión temporal preventiva.
- **Umbral de Alerta:** Con score < 50 puntos, la cuenta queda bloqueada para auto-solicitar recursos hasta regularizar su situación.

---

## 5. Enlaces Relacionados
- [[Modulos/Responsivas_Digitales_y_Firmas|Actas de Responsiva y Co-Responsables]]
- [[Modulos/Gestion_Recursos|Módulo de Recursos e Inventario]]
- [[Modulos/Reservas_y_Prestamos|Módulo de Préstamos]]
