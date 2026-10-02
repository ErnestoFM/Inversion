# 📅 Módulo: Reservas y Préstamos

**Etiquetas:** `#reservas` `#prestamos` `#flujos` `#maquina-de-estados` `#sigre`  
**Referencia Técnica:** [ARQUITECTURA_SIGRE.md](file:///c:/Users/erfierro/Documents/Inversion/docs/arquitectura/ARQUITECTURA_SIGRE.md) | [loans.routes.ts](file:///c:/Users/erfierro/Documents/Inversion/apps/api/src/routes/loans.routes.ts) | [events.routes.ts](file:///c:/Users/erfierro/Documents/Inversion/apps/api/src/routes/events.routes.ts)

---

## 1. Definición del Módulo
Maneja el ciclo de vida completo de solicitudes de espacios y recursos materiales en CUTonalá.

## 2. Flujo y Estados
1. **Pre-reserva:** El usuario selecciona el recurso/espacio y horario. Adquiere un bloqueo distribuido en Redis por **15 minutos** ([[Modulos/Concurrencia_Redis|Concurrencia]]).
2. **Confirmación:** Ingreso de justificación académica, co-responsables y confirmación. El estado pasa a `PENDIENTE`.
3. **Dictamen:** Un Coordinador o Jefe de Departamento aprueba o rechaza (con motivo documentado).
4. **Entrega y Uso:** El técnico ejecuta el checklist inicial de entrega. Pasa a `EN_USO`.
5. **Devolución:** El técnico realiza la inspección final. Si todo está en orden pasa a `FINALIZADO`; si hay anomalías, pasa a `CON_INCIDENCIA`.

## 3. Enlaces Relacionados
- [[Modulos/Concurrencia_Redis|Mecanismo Anti-Empalme con Redis]]
- [[Modulos/Checklists_e_Incidencias|Checklists e Incidencias]]
- [[Modulos/Notificaciones_y_PDF|Actas Responsivas en PDF]]
