import re
import pypdf

print("=== VERIFICACIÓN INTEGRAL DE PROTOCOLO SIGRE ===")

# 1. Check markdown source
with open('docs/protocolo_investigacion_sigre.md', 'r', encoding='utf-8') as f:
    md_text = f.read()

checks = [
    ("Presencia de 'n = 50' (muestra calibrada)", "n = 50" in md_text),
    ("Ausencia de 'n = 78' residual", "n = 78" not in md_text and "n=78" not in md_text),
    ("Alfa de Cronbach unificado a 0.892", "0.892" in md_text and "0.884" not in md_text),
    ("Desviación estándar SUS unificada a 10.91", "10.91" in md_text and "6.42" not in md_text),
    ("Intervalo de Confianza al 95% [79.75, 85.95]", "[79.75, 85.95]" in md_text),
    ("Prueba t una muestra t(49) = 1.848", "1.848" in md_text),
    ("Cita formal Sauro y Lewis (2012)", "Sauro" in md_text and "Lewis" in md_text),
    ("Línea base catalogada como estimaciones preliminares", "estimaciones preliminares" in md_text),
    ("Fase 4 Piloto en almacén en Ciclo 2027A", "2027A" in md_text),
    ("Modelo financiero CUTonalá (+$86,200/año, Payback 19.5 meses)", "86,200" in md_text and "19.5 meses" in md_text),
    ("Modelo trienal de red (Mes 15, Mes 33.8 descontado, TIR 21.34%)", "Mes 15" in md_text and "33.8" in md_text and "21.34%" in md_text),
    ("Relación B/C dual (1.15x netos / 1.07x convencional)", "1.15x" in md_text and "1.07x" in md_text),
    ("Tabla 9.2 de 9 pruebas Playwright E2E", "Tabla 9.2" in md_text and "P01" in md_text and "P09" in md_text),
    ("Restricción de exclusión PostgreSQL (btree_gist / EXCLUDE)", "btree_gist" in md_text and "EXCLUDE USING gist" in md_text),
    ("Console log de CI Playwright (9 passed, 18.4s)", "9 passed (18.4s)" in md_text),
    ("Identidad de prueba neutral EST-2026B-01", "EST-2026B-01" in md_text),
    ("Folio de prueba INC-2026-0003", "INC-2026-0003" in md_text),
    ("Cineteca unificada a 'Macario (1960)'", "Macario" in md_text and "Pinocho" not in md_text),
    ("Precedencia ética CPM A2 -> A9 (holgura 8 sem)", "A2, A6, A7" in md_text and "8 semanas" in md_text),
    ("Nomenclatura honesta Inversion / monchis-cafe-prod", "monchis-cafe-prod" in md_text and "Inversion" in md_text),
    ("Tabla 12 Gantt con encabezados S01 a S15", "S01 | S02" in md_text and "S13 | S14 | S15" in md_text),
    ("Runtime actualizado a Node.js 22 LTS / Alpine 3.19", "Node.js 22 LTS" in md_text and "Alpine Linux 3.19" in md_text),
    ("Bibliografía APA 7 estrictamente alfabética (UdeG al final)", md_text.rfind("Universidad de Guadalajara") > md_text.rfind("Sommerville"))
]

all_passed = True
for name, passed in checks:
    status = "✅ PASS" if passed else "❌ FAIL"
    if not passed:
        all_passed = False
    print(f"{status}: {name}")

# 2. Check compiled PDF
print("\n=== VERIFICACIÓN DEL PDF COMPILADO ===")
reader = pypdf.PdfReader('docs/2026B_Equipo4_Protocolo.pdf')
page_count = len(reader.pages)
print(f"Total de páginas en PDF: {page_count}")
assert page_count in (48, 49), f"Se esperaban 48 o 49 páginas, se encontraron {page_count}"

# Check for empty pages
empty_pages = []
for idx, page in enumerate(reader.pages):
    txt = page.extract_text() or ''
    if len(txt.strip()) < 80:
        empty_pages.append(idx + 1)
        print(f"⚠️ Alerta: Página {idx+1} tiene poco texto ({len(txt.strip())} caracteres)")

assert len(empty_pages) == 0, f"Se encontraron páginas vacías o casi vacías: {empty_pages}"
print("✅ PASS: 0 páginas vacías en el PDF.")

print(f"Estado de verificación general: {'TOTALMENTE EXITOSO' if all_passed else 'REVISAR FALLOS'}")
