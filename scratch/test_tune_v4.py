import os
import re
import sys

sys.path.append('scratch')
import test_tune_v3

t = test_tune_v3.t

# Apply new tightenings
t = t.replace('4,200 trámites $\\times$ 4 min = 280 h @ $140/h', '4,200 trámites $\\times$ 4 min (280 h @ $140/h)')
t = t.replace('5 a 8 reactivos/herramientas sin responsable', '5 a 8 reactivos sin responsable')
t = t.replace('Libretas foliadas, vales impresos, carpetas', 'Libretas foliadas, vales y carpetas')
t = t.replace('140 h personal técnico en rastreo manual', '140 h personal en rastreo manual')

t = t.replace('A partir del Año 4, SIGRE escalará a Universidades Públicas Estatales (**UPES**) del Centro-Occidente (340+ planteles):', 'Hacia el Año 4, SIGRE escalará a UPES del Centro-Occidente (340+ planteles):')

t = t.replace(
    'Support[Soporte Técnico N1<br>Activación: Mes 15]',
    'Support[Soporte N1<br>Mes 15]'
)
t = t.replace(
    'Tech[Especialista Soporte TC<br>Activación: Mes 22]',
    'Tech[Especialista TC<br>Mes 22]'
)
t = t.replace(
    'CS[Customer Success<br>Activación: Mes 28]',
    'CS[Customer Success<br>Mes 28]'
)

t = t.replace(
    'El capital se instrumenta mediante Acuerdo con **Cash Sweep del 70%** sobre el FEN hasta liquidar $180,000 MXN en **Mes 31.2**, con regalía del **15% sobre utilidades netas** posterior. En Año 1 (FEN **−$32,000 MXN**), el flujo se reinvierte. En Año 2 (FEN **+$78,900 MXN**), el Cash Sweep 70% paga **$55,230.00 MXN** al inversionista y **$23,670.00 MXN** al fundador (30%), restando saldo de **$124,770.00 MXN**. En Año 3 (FEN **+$296,800 MXN**), se amortiza el saldo en Mes 31.2 (Tramo 1: inversionista $124,770 MXN, fundador $53,473 MXN) y se activa la regalía del 15% (Tramo 2: inversionista $17,784 MXN, fundador $100,773 MXN), rindiendo en el año **$142,554.00 MXN** al inversionista y **$154,246.00 MXN** al fundador ($142,554 + $154,246 = $296,800 MXN).',
    'El capital se instrumenta mediante Acuerdo con **Cash Sweep del 70%** sobre el FEN hasta liquidar $180,000 MXN en **Mes 31.2**, con regalía del **15% sobre utilidades netas** posterior. En Año 1 (FEN **−$32,000 MXN**), el flujo se reinvierte. En Año 2 (FEN **+$78,900 MXN**), el Cash Sweep 70% paga **$55,230.00 MXN** al inversionista y **$23,670.00 MXN** al fundador (30%), con saldo de **$124,770.00 MXN**. En Año 3 (FEN **+$296,800 MXN**), se liquida en Mes 31.2 (Tramo 1: inversionista $124,770 MXN, fundador $53,473 MXN) y se activa regalía 15% (Tramo 2: inversionista $17,784 MXN, fundador $100,773 MXN), rindiendo en el año **$142,554.00 MXN** al inversionista y **$154,246.00 MXN** al fundador ($142,554 + $154,246 = $296,800 MXN).'
)

t = t.replace(
    'El retorno trienal acumulado suma **$197,784.00 MXN** (TIR 3.53%). A 5 años en Escenario Base, la regalía del 15% rinde **$44,520.00 MXN anuales** al inversionista y **$252,280.00 MXN** al fundador (**TIR del 15.62% anual**; acumulado $286,824 MXN). En expansión UPES, con ingresos de **1.21M MXN** (Año 4) y **1.93M MXN** (Año 5) a margen del **32.0%** (FEN **387.2k MXN** y **617.6k MXN**), la regalía del 15% paga **$58,080.00 MXN** en Año 4 y **$92,640.00 MXN** en Año 5 (**TIR del 21.20% anual**, múltiplo 1.93x; Tabla 16):',
    'El retorno trienal suma **$197,784.00 MXN** (TIR 3.53%). A 5 años en Escenario Base, la regalía rinde **$44,520.00 MXN anuales** al inversionista y **$252,280.00 MXN** al fundador (**TIR del 15.62% anual**; acumulado $286,824 MXN). En expansión UPES, con ingresos de **1.21M MXN** (Año 4) y **1.93M MXN** (Año 5) a margen del **32.0%** (FEN **387.2k MXN** y **617.6k MXN**), la regalía paga **$58,080.00 MXN** en Año 4 y **$92,640.00 MXN** en Año 5 (**TIR del 21.20% anual**, múltiplo 1.93x; Tabla 16):'
)

# Table 3
t = t.replace('| **Despacho** | 3.5 – 5.0 min | 2.5 – 4.0 min | 1.5 – 2.5 min | **< 25 segundos** |', '| **Despacho** | 3.5 – 5.0 min | 2.5 – 4.0 min | 1.5 – 2.5 min | **< 25 s** |')
t = t.replace('| **Costo Anual** | Mermas ocultas | $300k+ prorrateado | $35k - $60k + host | **$24,000 - $48,000 MXN** |', '| **Costo Anual** | Mermas | $300k+ prorrateado | $35k - $60k + host | **$24,000 - $48,000 MXN** |')

# Table 14
t = t.replace('($180,000.00 MXN)', '($180,000.00)')
t = t.replace('($32,000.00 MXN)', '($32,000.00)')
t = t.replace('+$78,900.00 MXN', '+$78,900.00')
t = t.replace('+$296,800.00 MXN', '+$296,800.00')

# Table 16
t = t.replace('Momento 0 | **($180,000)** | **($180,000)** | $180,000 | Desembolso capital semilla', 'M0 | **($180,000)** | **($180,000)** | $180,000 | Capital semilla')
t = t.replace('Año 1 | $0 | $0 | $180,000 | FEN −$32,000 reinvertido', 'Año 1 | $0 | $0 | $180,000 | FEN −$32,000 reinversión')
t = t.replace('Año 2 | **+$55,230** | **+$55,230** | **$124,770** | Cash Sweep 70% (FEN +$78,900)', 'Año 2 | **+$55,230** | **+$55,230** | **$124,770** | Cash Sweep 70%')
t = t.replace('Año 3 | **+$142,554** | **+$142,554** | **$0 (Liquidado Mes 31.2)** | Tramo 1 (70%) + Tramo 2 (15%)', 'Año 3 | **+$142,554** | **+$142,554** | **$0 (Liquidado Mes 31.2)** | Tramo 1 + Tramo 2')
t = t.replace('Año 4 | **+$44,520** | **+$58,080** | $0 | Regalía 15% ($296.8k / $387.2k UPES)', 'Año 4 | **+$44,520** | **+$58,080** | $0 | Regalía 15%')
t = t.replace('Año 5 | **+$44,520** | **+$92,640** | $0 | Regalía 15% ($296.8k / $617.6k UPES)', 'Año 5 | **+$44,520** | **+$92,640** | $0 | Regalía 15%')
t = t.replace('**Total** | **$286,824** | **$348,504** | — | Múltiplo 1.59x (Base) y 1.93x (UPES)', '**Total** | **$286,824** | **$348,504** | — | 1.59x Base / 1.93x UPES')

# Table 10 (Ruta Crítica)
t = t.replace('**A1. Formalización legal** | Sem 1-3 | Constitución mercantil y apertura de cuenta | Sí [RC]', '**A1. Legal** | Sem 1-3 | Constitución y cuenta | Sí [RC]')
t = t.replace('**A2-A3. Nube y Registro IP** | Sem 2-8 | Despliegue VPS, derechos INDAUTOR y registro IMPI | Sí [RC]', '**A2-A3. Cloud e IP** | Sem 2-8 | VPS, INDAUTOR y registro IMPI | Sí [RC]')
t = t.replace('**A4-A6. Piloto CUTonalá** | Sem 6-17 | Kits demo, 3 almacenes y personal capacitado | Sí [RC]', '**A4-A6. Piloto CUTonalá** | Sem 6-17 | Kits demo y 3 almacenes | Sí [RC]')
t = t.replace('**A7-A9. Expansión SEMS** | Sem 18-44 | Rondas demostrativas y cobro 2 prepas | Sí [RC]', '**A7-A9. Expansión SEMS** | Sem 18-44 | Rondas y cobro 2 prepas | Sí [RC]')
t = t.replace('**A10. Cierre anual** | Sem 45-48 | Auditoría técnica y balance Año 1 | No', '**A10. Cierre anual** | Sem 45-48 | Auditoría y balance Año 1 | No')

# Table 17
t = t.replace('6. Proforma | Amortización LISR Año 2 | ISR ($20,100 MXN) amortiza pérdida −$32,000 MXN (Sec 7.3, Tabla 13)', '6. Proforma | Amortización LISR | ISR ($20,100 MXN) amortiza pérdida −$32,000 MXN (Sec 7.3, Tabla 13)')
t = t.replace('7. Inversionista | Retorno | Cash Sweep 70%, liquidación Mes 31.2 y retorno 5 años (Sec 9.3, Tabla 16)', '7. Inversionista | Retorno | Cash Sweep 70%, liquidación Mes 31.2 (Sec 9.3, Tabla 16)')

w_regex = re.findall(r'\b[^\W_]+\b', t)
w_split = t.split()
w_no_pipes = [x for x in w_split if x != '|']

print('--- RESULTS V4 ---')
print('Chars with spaces:', len(t))
print('Split words:', len(w_split))
print('No pipes words:', len(w_no_pipes))
print('Regex words:', len(w_regex))
