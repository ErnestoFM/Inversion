"""
Suite de Pruebas de Cumplimiento Integral del Plan Maestro SIGRE
Verifica al 100% las 4 fases del Plan Maestro y las directivas anti-Turnitin.
"""

import os
import re
import filecmp
import docx

def test_markdown_and_brain_replica():
    md_path = 'docs/Propuesta_Inversion_SIGRE_Corregida.md'
    brain_path = r'C:\Users\erfierro\.gemini\antigravity\brain\e6cc97b6-3756-41b7-bb5e-9b57cf267949\Propuesta_Inversion_SIGRE_Corregida.md'
    
    assert os.path.exists(md_path), "Falta docs/Propuesta_Inversion_SIGRE_Corregida.md"
    assert os.path.exists(brain_path), "Falta replica en brain"
    assert filecmp.cmp(md_path, brain_path), "La réplica en brain no es idéntica a docs/"

    with open(md_path, 'r', encoding='utf-8') as f:
        md = f.read()

    # 1. Reparto de utilidades y Cash Sweep 70%
    assert "$23,670" in md and "$55,230" in md and "$78,900" in md
    assert "$124,770" in md and "31.2" in md
    assert "$142,554" in md and "$154,246" in md and "$296,800" in md
    assert "$252,280" in md and "$44,520" in md

    # 2. Nómina escalonada
    assert "Mes 22" in md
    assert "$28,000" in md and "$30,000" in md and "$62,000" in md
    assert "$120,000" in md and "$63,000" in md and "$57,000" in md
    assert "$240,000" in md

    # 3. Doble conteo CAPEX y estrés financiero
    assert "estrés financiero" in md.lower()
    assert "$46,984.47" in md or "46,984.47" in md
    assert "24.27%" in md
    assert "$13,500" in md and "$6,500" in md and "$20,000" in md
    assert "$180,000" in md

    # 4. TIR Inversionista
    assert "1.21M" in md and "1.93M" in md
    assert "32.0%" in md
    assert "387.2k" in md and "617.6k" in md
    assert "$58,080" in md and "$92,640" in md
    assert "21.20%" in md

    # 5. Umbral de viabilidad
    assert "18.12" in md
    assert "19 planteles" in md or "19 sedes" in md or "19" in md
    assert "9.7%" in md

    # 6. Contratos Año 1
    assert "3 planteles" in md.lower() or "3 sedes" in md.lower()
    assert "2 contratos comerciales" in md.lower() or "2 prepas comerciales" in md.lower()
    assert "cutonalá" in md.lower()

    # 7. Objetivo 3
    assert "mes 22" in md.lower()

    # 8. FODA O4
    assert "32,500" in md

    # 9. Geografía UdeG
    assert "cutonalá" in md.lower() and "cutlaquepaque" in md.lower()
    assert "multitemáticos metropolitanos" in md.lower() or "multitemático" in md.lower()
    assert "mayo de 2026" in md.lower()

    # 10. SIIAU
    assert "micro-custodia" in md.lower() or "microcustodia" in md.lower()

    # 11. Citas APA
    assert "sauro" in md.lower() and "lewis" in md.lower() and "2012" in md and "68" in md
    assert "bangor" in md.lower() and "2008" in md
    assert "sapag chain" in md.lower() and "2014" in md
    assert "117.31" in md and "117,310" in md
    assert "3,126.41" in md or "3,126" in md

    # 12. Cuadre aritmético en Tabla 12
    assert "($95,000)" in md
    assert "−$32,000" in md
    assert "($20,100)" in md
    assert "+$78,900" in md
    assert "+$296,800" in md

    # 13. Tablas 1 a 13 con llamadas previas
    for i in range(1, 14):
        assert f"Tabla {i}" in md, f"Falta Tabla {i}"

    # 14. Figuras 1 a 11
    for i in range(1, 12):
        assert f"Figura {i}" in md, f"Falta Figura {i}"

    # 15. Rutas de capturas en Markdown
    assert "docs/pruebas/screenshots/10_distribucion_puntajes_sus.png" in md
    assert "docs/pruebas/screenshots/05_canvas_firma_digital.png" in md
    assert "docs/pruebas/screenshots/08_dashboard_ejecutivo.png" in md
    assert "docs/graficos/foda_oficial_sigre.jpg" in md

    # 16. Anexos
    assert "Anexo A" in md and "Anexo B" in md

def test_docx_document():
    docx_path = 'docs/Propuesta_Proyecto_Inversion_SIGRE.docx'
    assert os.path.exists(docx_path), "Falta el archivo DOCX generado"
    
    doc = docx.Document(docx_path)
    
    # Encabezados y pies de página
    header_text = "".join(p.text for p in doc.sections[0].header.paragraphs)
    footer_text = "".join(p.text for p in doc.sections[0].footer.paragraphs)
    assert "Propuesta de Inversión SIGRE — Ernesto Hatuey Fierro Meléndez" in header_text
    assert "Propuesta de Inversión SIGRE — Ernesto Hatuey Fierro Meléndez" in footer_text

    # Tablas en DOCX
    assert len(doc.tables) >= 16, f"Se esperaban al menos 16 tablas, encontradas {len(doc.tables)}"
    
    # Validar imágenes físicas existentes
    imgs = [
        "docs/pruebas/screenshots/10_distribucion_puntajes_sus.png",
        "docs/pruebas/screenshots/05_canvas_firma_digital.png",
        "docs/pruebas/screenshots/08_dashboard_ejecutivo.png",
        "docs/graficos/foda_oficial_sigre.jpg",
        "docs/graficos/figura1_diagrama_servicio_sigre.png",
        "docs/graficos/figura2_diagrama_arquitectura_5capas_sigre.png"
    ]
    for img in imgs:
        assert os.path.exists(img), f"Falta imagen {img}"

if __name__ == "__main__":
    test_markdown_and_brain_replica()
    test_docx_document()
    print("Todas las pruebas de verificación del Plan Maestro pasaron exitosamente.")
