with open('docs/Propuesta_Inversion_SIGRE_Corregida.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if line.strip().startswith('|') and (i == 0 or not lines[i-1].strip().startswith('|')):
        # Found table start
        # look backwards for caption
        caption = "NO CAPTION"
        for k in range(max(0, i-5), i):
            if 'Tabla' in lines[k] or '**' in lines[k]:
                caption = lines[k].strip()
        print(f"Line {i+1}: Caption: {caption}")
