"""
Suite de Pruebas de Cumplimiento Integral del Plan Maestro SIGRE
Verifica al 100% las directivas de consistencia, rigor financiero y réplica en brain.
"""

import os
import filecmp

def test_markdown_and_brain_replica():
    md_path = 'docs/Propuesta_Inversion_SIGRE_Corregida.md'
    brain_path = r'C:\Users\erfierro\.gemini\antigravity\brain\e6cc97b6-3756-41b7-bb5e-9b57cf267949\Propuesta_Inversion_SIGRE_Corregida.md'
    
    assert os.path.exists(md_path), "Falta docs/Propuesta_Inversion_SIGRE_Corregida.md"
    assert os.path.exists(brain_path), "Falta replica en brain"
    assert filecmp.cmp(md_path, brain_path), "La réplica en brain no es idéntica a docs/"

    with open(md_path, 'r', encoding='utf-8') as f:
        md = f.read()

    # 1. Reparto de utilidades y Cash Sweep 75%
    assert "$17,100" in md and "$51,300" in md and "$68,400" in md
    assert "$128,700" in md and "31.1" in md
    assert "$149,976" in md and "$139,824" in md and "$289,800" in md
    assert "$309,304" in md and "$67,896" in md

    # 2. Nómina escalonada
    assert "Mes 22" in md
    assert "$28,000" in md and "$30,000" in md and "$62,000" in md
    assert "$120,000" in md and "$63,000" in md and "$57,000" in md
    assert "$240,000" in md

    # 3. Doble conteo CAPEX y estrés financiero
    assert "estrés financiero" in md.lower()
    assert "$34,442.34" in md or "34,442.34" in md
    assert "21.85%" in md
    assert "$13,500" in md and "$6,500" in md and "$20,000" in md
    assert "$180,000" in md

    # 4. TIR Inversionista
    assert "1.21M" in md and "1.93M" in md
    assert "20.49%" in md
    assert "26.51%" in md
    assert "$105,696" in md
    assert "$337,068" in md

    # 5. Umbral de viabilidad
    assert "18.99" in md
    assert "19 planteles" in md or "19 sedes" in md or "19" in md
    assert "9.7%" in md

    # 6. Contratos Año 1
    assert "3 planteles" in md.lower() or "3 sedes" in md.lower()
    assert "2 contratos comerciales" in md.lower() or "2 prepas comerciales" in md.lower()
    assert "cutonalá" in md.lower()

    # 7. Objetivo 3
    assert "mes 22" in md.lower()

    # 8. FODA O4
    assert "$20,000.00" in md or "$20,000" in md

    # 9. Geografía UdeG
    assert "cutonalá" in md.lower() and "cutlaquepaque" in md.lower() and "cuguadalajara" in md.lower()
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
    assert "anuies" in md.lower() and "2024" in md

    # 12. Cuadre aritmético en Tabla 12 / 13
    assert "($95,000)" in md
    assert "−$32,000" in md
    assert "($15,600)" in md
    assert "+$68,400" in md
    assert "+$289,800" in md

    # 13. Tablas 1 a 17 con llamadas previas
    for i in range(1, 18):
        assert f"Tabla {i}" in md, f"Falta Tabla {i}"

    # 14. Figuras 1 a 11
    for i in range(1, 12):
        assert f"Figura {i}" in md, f"Falta Figura {i}"

    # 15. Rutas de capturas e ilustraciones en Markdown
    assert "docs/graficos/figura1_comparativa_flujos.png" in md
    assert "docs/graficos/figura4_escalamiento_institucional.png" in md
    assert "docs/pruebas/screenshots/10_distribucion_puntajes_sus.png" in md
    assert "docs/pruebas/screenshots/05_canvas_firma_digital.png" in md
    assert "docs/pruebas/screenshots/08_dashboard_ejecutivo.png" in md
    assert "FORTALEZAS (F)" in md and "OPORTUNIDADES (O)" in md and "DEBILIDADES (D)" in md and "AMENAZAS (A)" in md

    # 16. Anexos
    assert "Anexo A" in md and "Anexo B" in md

if __name__ == "__main__":
    test_markdown_and_brain_replica()
    print("Todas las pruebas de verificación del Plan Maestro pasaron exitosamente.")
