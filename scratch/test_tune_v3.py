import os
import re
import sys

sys.path.append('scratch')
import test_tune_deep

t = test_tune_deep.build_tightened_text()

# Additional tightenings
t = t.replace('$0 MXN nómina externa', '$0 nómina externa')
t = t.replace('Facturación $\\ge \\$200,000$', 'Facturación $\\ge \\$200k$')
t = t.replace('Salarios ($120k + $63k) + Estipendio ($57k) = $240,000 MXN', 'Salarios ($120k+$63k) + Estipendio ($57k) = $240,000 MXN')

t = t.replace('$0 (Piloto CUTonalá sin costo)', '$0 (Piloto sin costo)')
t = t.replace('$48,000 (2 prepas ciclo 2026-B)', '$48,000 (2 prepas)')
t = t.replace('$15,000 (Setup CUTonalá)', '$15,000 (Setup)')

t = t.replace('$\\ge 85\\%$ menos mermas; 70% menos espera Año 3', '$\\ge 85\\%$ menos mermas; 70% menos espera')
t = t.replace('22 contratos; $\\ge 95\\%$ préstamos registrados', '22 contratos; $\\ge 95\\%$ registros')
t = t.replace('Uptime $\\ge 99.5\\%$, despacho $\\le 25$ s, personal instruido', 'Uptime $\\ge 99.5\\%$, despacho $\\le 25$ s')
t = t.replace('CAPEX $180,000 MXN ejercido; 3 planteles ciclo 2026-B', 'CAPEX $180,000 MXN; 3 planteles ciclo 2026-B')

t = t.replace('Carga < 1.2 s, render firma < 16 ms', 'Carga < 1.2 s, firma < 16 ms')
t = t.replace('Python 3.11 + FastAPI Asíncrono', 'Python 3.11 + FastAPI')
t = t.replace('Latencia p95 < 45 ms, 50 req/s nodo', 'Latencia p95 < 45 ms, 50 req/s')
t = t.replace('Consultas < 10 ms, ACID estricto', 'Consultas < 10 ms, ACID')
t = t.replace('Actas inmutables con hash y salt', 'Actas inmutables con hash')
t = t.replace('VPS Linux Tier III con Docker', 'VPS Tier III con Docker')
t = t.replace('99.5% uptime, respaldos cada 6 h', '99.5% uptime, respaldo 6 h')

t = t.replace('3 terminales, 1,200 actas selladas', '3 terminales, 1,200 actas')
t = t.replace('2 pre-contratos y kits demo', '2 pre-contratos y demos')
t = t.replace('**3 planteles** activos (**2 contratos comerciales** prepas + CUTonalá)', '**3 planteles** (**2 contratos comerciales** prepas + CUTonalá)')

t = t.replace('$24,000 MXN ($2,000/mes)', '$24,000 MXN ($2k/m)')
t = t.replace('$48,000 MXN ($4,000/mes)', '$48,000 MXN ($4k/m)')
t = t.replace('$72,000 MXN ($6,000/mes)', '$72,000 MXN ($6k/m)')

t = t.replace('**Software** | **SIGRE** (Micro-Custodia y Registro de Préstamos para Almacenes y Laboratorios)', '**Software** | **SIGRE** (Micro-Custodia y Trazabilidad para Almacenes y Laboratorios)')
t = t.replace('Inversión pre-semilla auditada con cojín de liquidez', 'Inversión pre-semilla con liquidez')
t = t.replace('**Payback Simple: Mes 29.4** (2.45 a) | **Payback Descontado: Mes 33.1** (2.76 a)', '**Payback Simple: Mes 29.4** | **Payback Descontado: Mes 33.1**')
t = t.replace('**Trienal: $197,784 MXN (TIR 3.53%)** | **5 a Base: 15.62%** | **5 a UPES: 21.20% anual**', '**Trienal: $197,784 MXN (3.53%)** | **5a Base: 15.62%** | **5a UPES: 21.20% anual**')

t = t.replace('1. Justificación | Cuantificar inacción | Modelo de $117,310 MXN/año (Sec 1.4, Tabla 2)', '1. Justificación | Inacción | Modelo de $117,310 MXN/año (Sec 1.4, Tabla 2)')
t = t.replace('2. Burocracia B2G | Compra sin licitación | Adjudicación < 1,000 UMA ($117,310 MXN; Sec 4.1)', '2. Burocracia B2G | Sin licitación | Adjudicación < 1,000 UMA ($117,310 MXN; Sec 4.1)')
t = t.replace('3. Marco Lógico | Metas MML CEPAL/BID | 22 sedes, payback Mes 31.2 y MML (Sec 2.2, Tabla 4)', '3. Marco Lógico | Metas MML | 22 sedes, payback Mes 31.2 y MML (Sec 2.2, Tabla 4)')
t = t.replace('4. Arquitectura | Arquitectura y datos | 5 capas, HMAC-SHA256 y LGPDPPSO (Sec 5, Tabla 7)', '4. Arquitectura | 5 capas y datos | HMAC-SHA256 y LGPDPPSO (Sec 5, Tabla 7)')
t = t.replace('5. Organización | Nómina sin déficit | Fundador Único ($120k Año 2 / $240k Año 3; Sec 6.2, Tabla 8)', '5. Organización | Nómina | Fundador Único ($120k Año 2 / $240k Año 3; Sec 6.2, Tabla 8)')
t = t.replace('7. Inversionista | Retorno de capital | Cash Sweep 70%, liquidación Mes 31.2 y retorno 5 años (Sec 9.3, Tabla 16)', '7. Inversionista | Retorno | Cash Sweep 70%, liquidación Mes 31.2 y retorno 5 años (Sec 9.3, Tabla 16)')

w_regex = re.findall(r'\b[^\W_]+\b', t)
w_split = t.split()
w_no_pipes = [x for x in w_split if x != '|']

print('--- RESULTS V3 ---')
print('Chars with spaces:', len(t))
print('Split words:', len(w_split))
print('No pipes words:', len(w_no_pipes))
print('Regex words:', len(w_regex))
