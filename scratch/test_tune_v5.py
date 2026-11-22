import os
import re
import sys

sys.path.append('scratch')
import test_tune_v4

t = test_tune_v4.t

# Apply final tightenings
t = t.replace('84.10 pts | 9.85', '84.10 | 9.85')
t = t.replace('81.50 pts | 11.20', '81.50 | 11.20')
t = t.replace('81.75 pts | 12.40', '81.75 | 12.40')

t = t.replace('Auditoría, motor HMAC y servicios', 'Auditoría y motor HMAC')

t = t.replace('**Mes 29.4 (2.45 a)**', '**Mes 29.4**')
t = t.replace('**Mes 33.1 (2.76 a)**', '**Mes 33.1**')

t = t.replace('En almacenes y laboratorios de la Red UdeG, el registro manual en libretas genera demoras', 'En la Red UdeG, el registro manual en libretas genera demoras')
t = t.replace('El macro-ERP (SIIAU) gestiona inventario diferido', 'El ERP (SIIAU) gestiona inventario diferido')
t = t.replace('liderando desarrollo, operaciones cloud y comercialización B2G', 'liderando desarrollo, cloud y comercialización B2G')
t = t.replace('Los costos operativos suman **$95,000 MXN en Año 1**', 'Los costos suman **$95,000 MXN en Año 1**')
t = t.replace('Los ingresos de Año 1 totalizan **$63,000 MXN**', 'Los ingresos de Año 1 suman **$63,000 MXN**')

t = t.replace('La Tabla 15 evalúa la resiliencia del proyecto ante fluctuaciones en la adopción:', 'La Tabla 15 evalúa la sensibilidad financiera ante fluctuaciones de adopción:')
t = t.replace('mercado cautivo validado y márgenes operativos > 45%', 'mercado cautivo y márgenes operativos > 45%')
t = t.replace('resuelve una merma de más de $117,000 MXN anuales', 'resuelve mermas de más de $117,000 MXN anuales')

t = t.replace('El capital semilla se destinará de inmediato a: 1) Registro de marca ante el IMPI y derechos ante INDAUTOR; 2) Consolidación operativa en 3 almacenes de CUTonalá;', 'El capital semilla se aplicará de inmediato a: 1) Marca ante IMPI y derechos ante INDAUTOR; 2) Consolidación en 3 almacenes de CUTonalá;')

w_regex = re.findall(r'\b[^\W_]+\b', t)
w_split = t.split()
w_no_pipes = [x for x in w_split if x != '|']

print('--- RESULTS V5 ---')
print('Chars with spaces:', len(t))
print('Split words:', len(w_split))
print('No pipes words:', len(w_no_pipes))
print('Regex words:', len(w_regex))
