# -*- coding: utf-8 -*-
import re

# Let's inspect Part 9 (Propuesta Inversionista) - currently 738 words.
# How can Part 9 be ~420 words without losing ANY assertion?
# Required assertions for Part 9:
# '$23,670', '$55,230', '$78,900', '$124,770', '31.2', '$142,554', '$154,246', '$296,800', '$252,280', '$44,520'
# '1.21M', '1.93M', '32.0%', '387.2k', '617.6k', '$58,080', '$92,640', '21.20%'
# 'Tabla 16'
# '$180,000'

sec9_draft = """## 9. Propuesta Formal para el Inversionista de Capital Semilla

### 9.1 Tesis de inversión y oportunidad de mercado
SIGRE ofrece una oportunidad SaaS con mercado cautivo validado, márgenes operativos superiores al 45% y validación empírica. Con un ticket pre-semilla de **$180,000.00 MXN**, resuelve una merma analógica de más de $117,000 MXN anuales por plantel con un modelo B2G ágil.

### 9.2 ¿Cuál es el siguiente paso para que el proyecto siga creciendo?
El capital semilla se destinará de inmediato a: 1) Registro de marca ante el IMPI y derechos ante INDAUTOR; 2) Consolidación operativa en los 3 almacenes de CUTonalá; 3) Fabricación de 4 kits demo e inicio de visitas para concretar 2 contratos comerciales en prepas SEMS en el ciclo 2026-B.

### 9.3 Estructura formal de inversión, instrumento legal y retorno financiero
La inversión se formalizará mediante un Acuerdo de Participación con **Mecanismo de Cash Sweep del 70%** sobre los Flujos de Efectivo Netos (FEN) del proyecto hasta reintegrar el principal ($180,000 MXN), transicionando luego a una regalía patrimonial del **15% sobre las utilidades netas**:
- **Año 1:** FEN de −$32,000 MXN ($0 al inversionista).
- **Año 2:** FEN de **+$78,900 MXN**. Cash Sweep 70% entrega al inversionista **$55,230.00 MXN** y al fundador **$23,670.00 MXN** (30%). Saldo insoluto: **$124,770.00 MXN** ($180,000 − $55,230).
- **Año 3:** FEN de **+$296,800 MXN**. Liquidación total del capital en **Mes 31.2**. En Tramo 1 (M25-31.2), el inversionista recibe $124,770 MXN (70%) y el fundador $53,473 MXN (30%). En Tramo 2 (M31.3-36, 15% regalía), el inversionista percibe $17,784 MXN y el fundador $100,773 MXN. Total Año 3: Inversionista **$142,554.00 MXN** y Fundador **$154,246.00 MXN** ($142,554 + $154,246 = $296,800 MXN exacto).
- **Retorno Trienal:** **$197,784.00 MXN** ($55,230 en Año 2 + $142,554 en Año 3; TIR 3.53%).
- **Retorno Quinquenal Base:** En Años 4 y 5 (FEN de $296,800 MXN), la regalía del 15% entrega al inversionista **$44,520.00 MXN anuales** y al fundador **$252,280.00 MXN anuales**. Flujo acumulado de $286,824.00 MXN y **TIR del 15.62% anual** (superior al 15.0% TMAR).
- **Retorno Quinquenal Expansión UPES:** Ingresos de **1.21M MXN** en Año 4 y **1.93M MXN** en Año 5 con margen del **32.0%** (FEN de **387.2k MXN** y **617.6k MXN**). Regalía del 15%: **$58,080.00 MXN** en Año 4 y **$92,640.00 MXN** en Año 5. El flujo [−$180,000, $0, $55,230, $142,554, $58,080, $92,640] genera una **TIR del 21.20% anual** (1.93x retorno).

La Tabla 16 resume los flujos proyectados y el retorno para el inversionista:

| Periodo | Flujo Base Estable | Flujo Expansión UPES | Saldo Capital | Tramo de Reparto |
|---|---|---|---|---|
| **Momento 0** | **($180,000.00 MXN)** | **($180,000.00 MXN)** | $180,000.00 MXN | Desembolso de capital semilla |
| **Año 1** | $0.00 MXN | $0.00 MXN | $180,000.00 MXN | FEN negativo (−$32,000); reinversión |
| **Año 2** | **+$55,230.00 MXN** | **+$55,230.00 MXN** | **$124,770.00 MXN** | Cash Sweep 70% sobre FEN de +$78,900 |
| **Año 3** | **+$142,554.00 MXN** | **+$142,554.00 MXN** | **$0.00 MXN (Liquidado en Mes 31.2)** | Tramo 1 (70% hasta liq) + Tramo 2 (15% regalía) |
| **Año 4** | **+$44,520.00 MXN** | **+$58,080.00 MXN** | $0.00 MXN | Regalía 15% ($296.8k base / $387.2k UPES) |
| **Año 5** | **+$44,520.00 MXN** | **+$92,640.00 MXN** | $0.00 MXN | Regalía 15% ($296.8k base / $617.6k UPES) |
| **Total Flujos** | **$286,824.00 MXN** | **$348,504.00 MXN** | — | Múltiplo 1.59x (Base) y 1.93x (Expansión) |
| **TIR** | **15.62% anual** | **21.20% anual** | — | **Ambos escenarios superan TMAR (15.0%)** |

*Tabla 16. Flujos de caja proyectados y Tasa Interna de Retorno (TIR) para el inversionista privado.*
"""

print("Original Sec 9 words: 738")
print("Draft Sec 9 words:", len(sec9_draft.split()))
