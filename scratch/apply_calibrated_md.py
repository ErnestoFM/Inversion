import os
import filecmp
import sys

sys.path.append('scratch')
import test_tune_v5

md_content = test_tune_v5.t

doc_path = 'docs/Propuesta_Inversion_SIGRE_Corregida.md'
brain_path = r'C:\Users\erfierro\.gemini\antigravity\brain\e6cc97b6-3756-41b7-bb5e-9b57cf267949\Propuesta_Inversion_SIGRE_Corregida.md'

with open(doc_path, 'w', encoding='utf-8') as f:
    f.write(md_content)

os.makedirs(os.path.dirname(brain_path), exist_ok=True)
with open(brain_path, 'w', encoding='utf-8') as f:
    f.write(md_content)

assert filecmp.cmp(doc_path, brain_path), "Error: no son idénticos"
print(f"Archivos sincronizados exitosamente. Tamaño: {len(md_content)} caracteres.")
