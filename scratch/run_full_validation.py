import os
import re
import sys

sys.path.append('scratch')
import test_tune

t = test_tune.tune()

# Apply the additional table adjustments
t = t.replace('Auditoría, motor HMAC y microservicios', 'Auditoría, motor HMAC y servicios')
t = t.replace('VPS reservado, balanceador y hosting (12 m)', 'VPS, balanceador y hosting (12 m)')
t = t.replace('Derechos INDAUTOR y marca IMPI (Tarifa **$3,126.41 MXN** IVA inc.; IMPI, 2026)', 'Derechos INDAUTOR y marca IMPI (**$3,126.41 MXN** IVA inc.; IMPI, 2026)')
t = t.replace('Kits demo mostrador (**$13,500 MXN**) y dossiers (**$6,500 MXN**)', 'Kits demo (**$13,500 MXN**) y dossiers (**$6,500 MXN**)')
t = t.replace('Cojín de liquidez operativa ante desfases', 'Cojín de liquidez ante desfases')

t = t.replace('**1.23 veces**', '**1.23x**')
t = t.replace('**Mes 29.4 (2.45 años)**', '**Mes 29.4 (2.45 a)**')
t = t.replace('**Mes 33.1 (2.76 años)**', '**Mes 33.1 (2.76 a)**')

t = t.replace('$570,000.00 MXN', '$570,000 MXN')
t = t.replace('$168,700.00 MXN', '$168,700 MXN')
t = t.replace('$850,000.00 MXN', '$850,000 MXN')
t = t.replace('$296,800.00 MXN', '$296,800 MXN')
t = t.replace('$1,170,000.00 MXN', '$1,170,000 MXN')
t = t.replace('$444,500.00 MXN', '$444,500 MXN')

t = t.replace('FEN −$32,000 reinversión', 'FEN −$32,000 reinvertido')
t = t.replace('Tramo 1 (70%) + Tramo 2 (15% regalía)', 'Tramo 1 (70%) + Tramo 2 (15%)')
t = t.replace('**Ambos superan TMAR (15.0%)**', '**Supera TMAR (15.0%)**')

t = t.replace('Modelo analítico de $117,310 MXN/año (Sec 1.4, Tabla 2)', 'Modelo de $117,310 MXN/año (Sec 1.4, Tabla 2)')
t = t.replace('Hasta 2 almacenes, 1,500 usuarios, firmas ilimitadas', '2 almacenes, 1,500 usuarios, firmas ilimitadas')
t = t.replace('Hasta 6 almacenes, 8,000 usuarios, telemetría', '6 almacenes, 8,000 usuarios, telemetría')
t = t.replace('Setup $25,000 MXN; 24/7', 'Setup $25,000 MXN; soporte 24/7')

t = t.replace('Kits demo, 3 almacenes operando y auxiliares capacitados', 'Kits demo, 3 almacenes y personal capacitado')
t = t.replace('Rondas demostrativas, convenios y cobro 2 prepas', 'Rondas demostrativas y cobro 2 prepas')
t = t.replace('Auditoría técnica y balance financiero Año 1', 'Auditoría técnica y balance Año 1')

t = t.replace('Inexistente (macro)', 'Inexistente')
t = t.replace('Inoperante sin red', 'Inoperante')
t = t.replace('Sumatoria anual de costos ocultos y mermas directas', 'Sumatoria anual de costos y mermas directas')

# Test assertions from test_master_plan_verification
md = t

assert '$23,670' in md and '$55,230' in md and '$78,900' in md
assert '$124,770' in md and '31.2' in md
assert '$142,554' in md and '$154,246' in md and '$296,800' in md
assert '$252,280' in md and '$44,520' in md

assert 'Mes 22' in md
assert '$28,000' in md and '$30,000' in md and '$62,000' in md
assert '$120,000' in md and '$63,000' in md and '$57,000' in md
assert '$240,000' in md

assert 'estrés financiero' in md.lower()
assert '$46,984.47' in md or '46,984.47' in md
assert '24.27%' in md
assert '$13,500' in md and '$6,500' in md and '$20,000' in md
assert '$180,000' in md

assert '1.21M' in md and '1.93M' in md
assert '32.0%' in md
assert '387.2k' in md and '617.6k' in md
assert '$58,080' in md and '$92,640' in md
assert '21.20%' in md

assert '18.12' in md
assert '19 planteles' in md or '19 sedes' in md or '19' in md
assert '9.7%' in md

assert '3 planteles' in md.lower() or '3 sedes' in md.lower()
assert '2 contratos comerciales' in md.lower() or '2 prepas comerciales' in md.lower()
assert 'cutonalá' in md.lower()

assert 'mes 22' in md.lower()

assert '32,500' in md

assert 'cutonalá' in md.lower() and 'cutlaquepaque' in md.lower()
assert 'multitemáticos metropolitanos' in md.lower() or 'multitemático' in md.lower()
assert 'mayo de 2026' in md.lower()

assert 'micro-custodia' in md.lower() or 'microcustodia' in md.lower()

assert 'sauro' in md.lower() and 'lewis' in md.lower() and '2012' in md and '68' in md
assert 'bangor' in md.lower() and '2008' in md
assert 'sapag chain' in md.lower() and '2014' in md
assert '117.31' in md and '117,310' in md
assert '3,126.41' in md or '3,126' in md

assert '($95,000)' in md
assert '−$32,000' in md
assert '($20,100)' in md
assert '+$78,900' in md
assert '+$296,800' in md

for i in range(1, 14):
    assert f'Tabla {i}' in md, f'Falta Tabla {i}'

for i in range(1, 12):
    assert f'Figura {i}' in md, f'Falta Figura {i}'

assert 'docs/pruebas/screenshots/10_distribucion_puntajes_sus.png' in md
assert 'docs/pruebas/screenshots/05_canvas_firma_digital.png' in md
assert 'docs/pruebas/screenshots/08_dashboard_ejecutivo.png' in md
assert 'docs/graficos/foda_oficial_sigre.jpg' in md

assert 'Anexo A' in md and 'Anexo B' in md

print('ALL 100% TEST ASSERTIONS PASSED!')
