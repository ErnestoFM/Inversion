# AGENTS.md - Directivas Globales del Espacio de Trabajo

Este archivo define las directivas y reglas de comportamiento obligatorias para todos los Agentes de IA que operan en este proyecto.

---

## 1. Gestión de Requerimientos (`requirements/`)
- **Fuente Única de Verdad para Requisitos:** Los requerimientos del proyecto redactados por el usuario se depositan en `requirements/funcionales/` y `requirements/tecnicos/`.
- **Análisis Previo:** ANTES de generar código o proponer cambios arquitectónicos, DEBES revisar los archivos contenidos en `requirements/` para alinearte con las especificaciones y prioridades del cliente.

---

## 2. Documentación y Bitácora en Obsidian (`obsidian/`)
- **Vault de Documentación para el Agente:** Toda la documentación contextual de IA, notas de arquitectura y bitácora se gestionan en `obsidian/`.
- **Bitácora Automática Diaria:** Al finalizar o realizar cambios significativos en el código o la estructura del repositorio, registra o actualiza una entrada detallada en `obsidian/Bitacora/YYYY-MM-DD.md` (utilizando la fecha actual).
- **Formato de Registro:** 
  - Clasifica los archivos modificados en una tabla con los estados (`NUEVO`, `MOD`, `ELIMINADO`).
  - Proporciona un resumen claro de los cambios y los comandos ejecutados.
  - Incluye enlaces markdown o wikilinks (`[[Notas]]`).
- **Actualización de Índices:** Asegúrate de que las nuevas notas estén vinculadas en `obsidian/Index.md` y en sus respectivos índices de subdirectorio.

---

## 3. Calidad de Código y Estándares Técnicos
- **Cero Hardcoding:** NUNCA escribas credenciales, llaves secretas o URLs fijas en el código. Utiliza variables de entorno (`.env`).
- **Documentación Técnica Paralela:** Al crear módulos o arquitecturas complejas, documenta las decisiones técnicas en `docs/tecnica/` y en `obsidian/Modulos/`.
- **Integración Continua:** Mantén la compatibilidad con los flujos de GitHub Actions definidos en `.github/workflows/`.
