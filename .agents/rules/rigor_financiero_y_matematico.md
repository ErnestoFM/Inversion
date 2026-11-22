---
trigger: always_on
description: Prohibición estricta de aritmética mental en prosa. Exige cálculo y verificación obligatoria mediante Python para toda cifra financiera, tabla contable y métrica cuantitativa.
---

## Regla: Rigor Financiero, Matemático y Consistencia Tabular

Esta directiva es de cumplimiento estricto e ineludible para cualquier agente de IA que genere, edite o analice documentos, reportes, modelos o tablas en este repositorio.

### 1. Cero Aritmética "en Prosa" o de Memoria
* **Prohibición Absoluta:** Queda terminantemente prohibido calcular sumas, restas, proyecciones, factores de descuento, porcentajes, Valor Presente Neto (VPN), Tasa Interna de Retorno (TIR), o periodos de recuperación (Payback) de manera mental o mediante generación de texto predictivo.
* **Cálculo Obligatorio por Código:** Toda cifra numérica que forme parte de un reporte, tabla o estado financiero DEBE ser calculada primero ejecutando un script de Python en terminal o entorno de ejecución.

### 2. Verificación y Cuadre de Tablas
* **Sumas Verticales y Horizontales:** Antes de plasmar una tabla contable, de costos o de presupuestos, el agente debe verificar que las sumas de columnas y renglones coincidan exactamente al centavo.
* **Inclusión de Tests Automatizados:** Todo cambio en modelos financieros o tablas multi-periodo debe acompañarse de un script de verificación cruzada (`scratch/test_*.py` o `tests/`) que valide:
  - Consistencia de flujos netos ($\text{Ingresos} - \text{Egresos} = \text{Utilidad}$).
  - Suma de partidas individuales frente a los totales declarados.
  - Recálculo exacto de fórmulas financieras estándar (VAN / VPN, TIR, Payback acumulado simple y descontado).

### 3. Coherencia Integral Multi-Sección
* **Consistencia de Cifras:** Ninguna cifra puede contradecirse entre diferentes partes del documento. Si un número cambia en una tabla (ej. CAPEX, OPEX, FEN, TIR, Payback), el agente DEBE rastrear y sincronizar de inmediato:
  - El Resumen Ejecutivo / Ficha Técnica.
  - La Matriz FODA.
  - El Estado de Resultados / Flujo de Caja.
  - El Análisis de Sensibilidad.
  - Las Conclusiones y el Mecanismo de Retorno al Inversionista.

### 4. Transparencia Metodológica y Supuestos
* **Prohibido Maquillar Resultados:** Si un escenario de sensibilidad resulta inviable ($\text{VPN} < 0$ o $\text{TIR} < \text{TMAR}$), debe reportarse con total honestidad y claridad técnica, definiendo explícitamente el umbral exacto de viabilidad operativa en vez de forzar afirmaciones falsas de solvencia.
* **Separación Conceptual Estricta:** Diferenciar con rigor técnico las métricas del proyecto frente a las métricas del inversionista (ej. *Payback del Proyecto* vs. *Liquidación del Inversionista*).
