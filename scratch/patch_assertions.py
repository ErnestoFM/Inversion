with open('docs/Propuesta_Inversion_SIGRE_Corregida.md', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('**($95,000.00)**', '**($95,000)**')
text = text.replace('**($225,000.00)**', '**($225,000)**')
text = text.replace('**($426,000.00)**', '**($426,000)**')
text = text.replace('**($20,100.00)**', '**($20,100)**')
text = text.replace('**($127,200.00)**', '**($127,200)**')
text = text.replace('**−$32,000.00 MXN**', '**−$32,000 MXN**')
text = text.replace('**+$78,900.00 MXN**', '**+$78,900 MXN**')
text = text.replace('**+$296,800.00 MXN**', '**+$296,800 MXN**')

with open('docs/Propuesta_Inversion_SIGRE_Corregida.md', 'w', encoding='utf-8') as f:
    f.write(text)

with open(r'C:\Users\erfierro\.gemini\antigravity\brain\e6cc97b6-3756-41b7-bb5e-9b57cf267949\Propuesta_Inversion_SIGRE_Corregida.md', 'w', encoding='utf-8') as f:
    f.write(text)

print("Tabla 13 formateada.")
