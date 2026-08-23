---
trigger: always_on
description: Mantener actualizada la bitácora diaria y el Vault de Obsidian tras cada modificación de código o documentación.
---

## Regla: Documentación Continua en Obsidian

Este proyecto utiliza el Vault `obsidian/` como memoria persistente del Agente.

### Directivas:
1. **Registro Obligatorio:** Tras cada sesión donde se cree, modifique o depure código o archivos del proyecto, se DEBE actualizar `obsidian/Bitacora/YYYY-MM-DD.md`.
2. **Uso de Wikilinks:** Utiliza sintaxis wikilink (`[[Modulo]]`, `[[Arquitectura]]`) para enlazar las notas relacionadas.
3. **Mantenimiento del Índice:** Revisa que todas las notas nuevas tengan referencia en `obsidian/Index.md`.
