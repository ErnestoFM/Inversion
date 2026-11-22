import pypdf

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
    ('$46,984.47', 'VPN'),
    ('24.27%', 'TIR'),
    ('1.23', 'B/C'),
    ('29.4', 'Payback Simple'),
    ('33.1', 'Payback Descontado'),
    ('31.2', 'Liquidacion Inversionista'),
    ('15.62%', 'TIR Inversionista Base'),
    ('21.20%', 'TIR Inversionista UPES'),
    ('82.85', 'SUS Score'),
    ('$180,000', 'CAPEX'),
    ('$225,342.50', 'Umbral Viabilidad FEN'),
    ('19 planteles', 'Umbral discreto seguro')
]
for val, name in invariants:
    assert val in all_text, f"Missing financial invariant: {name} ({val})"
    print(f"Financial Invariant [{name}]: FOUND")

print("\nALL VERIFICATIONS PASSED PERFECTLY!")
