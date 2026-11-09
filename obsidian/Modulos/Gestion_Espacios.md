# 🏢 Módulo: Gestión de Espacios Físicos

**Etiquetas:** `#espacios` `#infraestructura` `#aulas` `#laboratorios` `#sigre`  
**Referencia Técnica:** [ESPECIFICACION_TECNICA_APIS.md](file:///c:/Users/erfierro/Documents/Inversion/docs/tecnica/ESPECIFICACION_TECNICA_APIS.md)

---

## 1. Definición del Módulo
Administra el inventario de infraestructura física del CUTonalá disponible para la comunidad:
- **Tipos de Espacio:** Aulas magnas, laboratorios de cómputo, laboratorios de ciencias, cubículos de asesoría, canchas y auditorios.
- **Atributos:** Capacidad máxima, equipamiento fijo (proyector, aire acondicionado, número de contactos), edificio/módulo, reglas particulares de uso y fotografías representativas.

## 2. Estados de Operación
- `DISPONIBLE`: Espacio apto para reservaciones.
- `MANTENIMIENTO`: Bloqueado temporalmente por reparaciones o limpieza.
- `FUERA_DE_SERVICIO`: Inhabilitado indefinidamente por remodelación o siniestro.

## 3. Enlaces Relacionados
- [[Modulos/Reservas_y_Prestamos|Módulo de Reservaciones]]
- [[Modulos/Concurrencia_Redis|Bloqueo Anti-Empalme con Redis]]
