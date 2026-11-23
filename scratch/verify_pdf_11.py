import pypdf
import re

reader = pypdf.PdfReader('docs/Propuesta_Proyecto_Inversion_SIGRE.pdf')
total = len(reader.pages)
print(f"TOTAL PAGES: {total}")
assert total == 11, f"Expected 11 pages, got {total}"

# Check page 1 (Cover)
p1 = reader.pages[0].extract_text()
assert 'Página 1 de 11' not in p1, "Page 1 should NOT have page number"
assert 'UNIVERSIDAD DE GUADALAJARA' in p1, "Page 1 should have UdeG"
assert 'Ernesto Hatuey Fierro Meléndez' in p1, "Page 1 should have author"
print("Page 1 (Cover): VERIFIED CLEAN")

# Check pages 2 to 11
for i in range(1, total):
    ptxt = reader.pages[i].extract_text()
    expected_footer = f"Página {i+1} de 11"
    expected_header = "Propuesta de Inversión SIGRE — Ernesto Hatuey Fierro Meléndez"
    assert expected_footer in ptxt, f"Page {i+1} missing footer {expected_footer}"
    assert expected_header in ptxt, f"Page {i+1} missing header"
    print(f"Page {i+1}: Header & Footer '{expected_footer}' VERIFIED")

# Check last page content
p11 = reader.pages[10].extract_text()
assert 'Tabla 17' in p11, "Page 11 should contain Tabla 17 (Anexo B)"
print("Page 11 (Last Page): Ends cleanly with Anexo B / Tabla 17")

# Check financial invariants across PDF text
all_text = " ".join(page.extract_text() for page in reader.pages)
invariants = [
    ('$34,442.34', 'VPN'),
    ('21.85%', 'TIR'),
    ('1.17', 'B/C'),
    ('29.9', 'Payback Simple'),
    ('33.8', 'Payback Descontado'),
    ('31.1', 'Liquidacion Inversionista'),
    ('20.49%', 'TIR Inversionista Base'),
    ('26.51%', 'TIR Inversionista UPES'),
    ('82.85', 'SUS Score'),
    ('$180,000', 'CAPEX'),
    ('$237,417.50', 'Umbral Viabilidad FEN'),
    ('9.7%', 'Porcentaje Red UdeG')
]
for val, name in invariants:
    assert val in all_text, f"Missing financial invariant: {name} ({val})"
    print(f"Financial Invariant [{name}]: FOUND")

assert re.search(r'19\s+planteles', all_text) is not None, "Missing: 19 planteles"
print("Financial Invariant [19 planteles]: FOUND")

print("\nALL 11-PAGE PDF VERIFICATIONS PASSED PERFECTLY!")
