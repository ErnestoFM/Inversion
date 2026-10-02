# ⚡ Módulo: Concurrencia y Bloqueo Anti-Empalme con Redis

**Etiquetas:** `#redis` `#concurrencia` `#lock` `#anti-empalme` `#sigre`  
**Referencia Técnica:** [RT_SIGRE_Arquitectura_Seguridad_Datos.md](file:///c:/Users/erfierro/Documents/Inversion/requirements/tecnicos/RT_SIGRE_Arquitectura_Seguridad_Datos.md) | [ARQUITECTURA_SIGRE.md](file:///c:/Users/erfierro/Documents/Inversion/docs/arquitectura/ARQUITECTURA_SIGRE.md)

---

## 1. Definición del Módulo
Evita el solapamiento de solicitudes y reservas sobre un mismo recurso o espacio físico cuando múltiples usuarios intentan solicitarlo simultáneamente.

## 2. Estrategia de Bloqueo en Dos Niveles

### Nivel 1: Soft Lock Distribuido en Redis (Memoria)
- Al momento de seleccionar el espacio en la interfaz, se crea una clave con TTL:
  ```bash
  SET resource:lock:<spaceId>:<timestampRange> "<userId>" NX EX 900
  ```
- **TTL:** 15 minutos (900 segundos).
- Si otro usuario intenta seleccionar el mismo rango, recibe un código `409 Conflict`.
- Si el usuario no concluye el proceso o cierra la pestaña, el candado se libera automáticamente sin bloquear permanentemente el recurso.

### Nivel 2: Hard Lock y Transacción Atómica en PostgreSQL (Disco)
- Al confirmar la reserva, la base de datos ejecuta una transacción atómica verificando solapamiento de rangos temporales (`tsrange`).
- Si la transacción es exitosa, se elimina la clave de Redis y queda la reserva en firme.

## 3. Enlaces Relacionados
- [[Modulos/Reservas_y_Prestamos|Módulo de Reservaciones]]
- [[Arquitectura/Index|Arquitectura del Sistema]]
