import re

with open('docs/Propuesta_Inversion_SIGRE_Corregida.md', 'r', encoding='utf-8') as f:
    text = f.read()

# Check all table titles
tables = re.findall(r'(Tabla\s+\d+[^.\n]*\.)', text)
print(f'Total table titles found: {len(tables)}')
for t in tables:
    print(t)
