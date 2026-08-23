---
description: Flujo para procesar e ingestar nuevos requerimientos colocados en requirements/.
---

# Flujo: Ingesta de Requerimientos

1. **Inspección:** Escanea `requirements/funcionales/` y `requirements/tecnicos/`.
2. **Análisis:** Extrae módulos principales, entidades de datos y reglas de negocio.
3. **Documentación:** 
   - Crea/actualiza especificaciones técnicas en `docs/tecnica/`.
   - Crea notas contextuales de módulos en `obsidian/Modulos/`.
4. **Respuesta al Usuario:** Presenta el plan de arquitectura e implementación para su aprobación.
