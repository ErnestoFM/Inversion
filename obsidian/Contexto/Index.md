# 🎯 Contexto del Dominio y Problemática — SIGRE

Documentación del contexto institucional y operativo del **Centro Universitario de Tonalá (CUTonalá) — Universidad de Guadalajara**:

---

## 1. Problemática Institucional Resuelta
Históricamente, la reserva de espacios (auditorios, aulas de cómputo, laboratorios de ciencias) y el préstamo de equipo audiovisual o de prácticas en CUTonalá se realizaba mediante bitácoras en papel, correos electrónicos informales o mensajes de mensajería instantánea.

Esto ocasionaba:
- **Empalmes de horarios:** Múltiples profesores o eventos agendados en el mismo auditorio a la misma hora.
- **Pérdida de trazabilidad patrimonial:** Materiales entregados sin registro formal del estado físico ni acta responsiva firmada.
- **Falta de corresponsabilidad:** Falta de consecuencias ante devoluciones tardías o maltrato de instalaciones.
- **Subutilización u ociosidad:** Espacios solicitados pero no utilizados (*No-Shows*), impidiendo que otros alumnos los aprovechen.

---

## 2. Objetivos Estratégicos de SIGRE
1. **Centralización Digital:** Un portal único con autenticación institucional de la UdG (`@alumnos.udg.mx` y `@udg.mx`).
2. **Cero Empalmes:** Bloqueo temporal distribuido con Redis y validación atómica en PostgreSQL.
3. **Custodia y Responsabilidad:** Emisión automática de actas PDF con firmas digitales y listas de verificación (checklists) fotográficas.
4. **Cultura de Cuidado:** Mecanismo de *Trust Score* que premia a los usuarios cumplidos y regula a infractores.
5. **Alineación con la Identidad UdeG:** Cumplimiento estricto de la [Guía de Identidad de Marca](file:///c:/Users/erfierro/Documents/Inversion/docs/sigre_brand_identity.md) y tokens institucionales.

---

## 3. Enlaces Relacionados
- [[Arquitectura/Index|Arquitectura Técnica de SIGRE]]
- [[Modulos/Index|Módulos del Sistema]]
