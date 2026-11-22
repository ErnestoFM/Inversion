import pypdf

reader = pypdf.PdfReader('docs/Propuesta_Proyecto_Inversion_SIGRE.pdf')
print(f'Total pages: {len(reader.pages)}')
for i, p in enumerate(reader.pages):
    txt = p.extract_text().strip().split('\n')
    header_sample = [l.strip() for l in txt if l.strip() and 'Propuesta de Inversión' not in l and 'Página ' not in l][:3]
    print(f"Page {i+1}: {' | '.join(header_sample)[:80]}")
