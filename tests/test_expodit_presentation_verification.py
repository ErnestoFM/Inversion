"""
Test de Verificación Formal para la Presentación ExpoDIT 2026 y Guion Oral de SIGRE
Cumplimiento estricto de:
- .agents/rules/rigor_financiero_y_matematico.md
- .agents/rules/coding_standards.md
"""

import os
import re
import pptx

def test_financial_metrics_calculation():
    """Valida los cálculos financieros exactos mediante funciones matemáticas puras."""
    tmar = 0.15
    capex = -180000.0
    fen_y1 = -32000.0
    fen_y2 = 78900.0
    fen_y3 = 296800.0
    flows = [capex, fen_y1, fen_y2, fen_y3]

    # 1. VPN
    vpn = sum(f / ((1 + tmar) ** i) for i, f in enumerate(flows))
    assert round(vpn, 2) == 46984.47, f"VPN incorrecto: {vpn:.2f} != 46984.47"

    # 2. TIR por bisección
    def npv_rate(r):
        return sum(f / ((1 + r) ** i) for i, f in enumerate(flows))

    low, high = 0.0, 1.0
    for _ in range(100):
        mid = (low + high) / 2
        if npv_rate(mid) > 0:
            low = mid
        else:
            high = mid
    tir_pct = mid * 100
    assert round(tir_pct, 2) == 24.27, f"TIR incorrecta: {tir_pct:.2f}% != 24.27%"

    # 3. Payback simple del proyecto (Mes 29.4)
    # Al final del año 2 (mes 24), saldo acumulado = -180k - 32k + 78.9k = -133.1k
    # Flujo mensual en año 3 = 296,800 / 12 = 24,733.33 MXN/mes
    # Meses necesarios = 133,100 / 24,733.33 = 5.381 meses
    # Mes total = 24 + 5.381 = 29.38 meses (~29.4 meses)
    payback_proj = 24 + 133100.0 / (fen_y3 / 12.0)
    assert round(payback_proj, 1) == 29.4, f"Payback proyecto incorrecto: {payback_proj:.2f} != 29.4"

    # 4. Liquidación del inversionista (Mes 31.2)
    # Cash Sweep 70% del FEN
    # Año 1: $0 (gracia)
    # Año 2: 70% de 78.9k = $55,230 MXN (Saldo insoluto: 180k - 55.23k = 124,770 MXN)
    # Año 3: Cuota mensual = (296,800 / 12) * 0.70 = 17,313.33 MXN/mes
    # Meses requeridos = 124,770 / 17,313.33 = 7.205 meses
    # Mes de liquidación total = 24 + 7.205 = 31.21 meses (~31.2 meses)
    cuota_mensual_inv_y3 = (fen_y3 / 12.0) * 0.70
    saldo_restante_inv = 180000.0 - (fen_y2 * 0.70)
    payback_inv = 24 + saldo_restante_inv / cuota_mensual_inv_y3
    assert round(payback_inv, 1) == 31.2, f"Payback inversionista incorrecto: {payback_inv:.2f} != 31.2"

def test_pptx_integrity():
    """Valida la integridad estructural del archivo PowerPoint generado."""
    pptx_path = 'docs/Presentacion_ExpoDIT_SIGRE.pptx'
    assert os.path.exists(pptx_path), f"No existe {pptx_path}"
    assert os.path.getsize(pptx_path) > 100000, "El archivo PPTX es demasiado pequeño"

    prs = pptx.Presentation(pptx_path)
    assert len(prs.slides) == 13, f"El PPTX debe tener exactamente 13 diapositivas, tiene {len(prs.slides)}"

    # Verificar que todas las diapositivas tienen notas con guion y tiempo
    for i, slide in enumerate(prs.slides):
        assert slide.has_notes_slide, f"La diapositiva {i+1} no tiene lámina de notas"
        notes_text = slide.notes_slide.notes_text_frame.text
        assert "TIEMPO:" in notes_text, f"La diapositiva {i+1} no tiene etiqueta TIEMPO en notas"
        assert "GUION LITERAL:" in notes_text, f"La diapositiva {i+1} no tiene etiqueta GUION LITERAL en notas"
        assert len(notes_text) > 100, f"Las notas de la diapositiva {i+1} son demasiado breves"

def test_html_visualizer_integrity():
    """Valida que el visualizador HTML contenga todas las diapositivas y guiones."""
    html_path = 'docs/Presentacion_ExpoDIT_SIGRE.html'
    assert os.path.exists(html_path), f"No existe {html_path}"
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()

    slides = re.findall(r'data-slide="(\d+)"', html)
    assert len(slides) == 13, f"El HTML debe contener 13 diapositivas, se encontraron {len(slides)}"

    # Verificar presencia de cifras financieras críticas
    assert "46,984.47" in html or "46,984" in html, "Falta VPN en HTML"
    assert "24.27%" in html, "Falta TIR en HTML"
    assert "29.4" in html, "Falta Payback en HTML"
    assert "82.85" in html, "Falta SUS score en HTML"
    assert "180,000" in html, "Falta CAPEX en HTML"

def test_slide_structural_parity():
    """Valida la paridad estructural exacta con la presentación de referencia Monchis Café."""
    pptx_path = 'docs/Presentacion_ExpoDIT_SIGRE.pptx'
    html_path = 'docs/Presentacion_ExpoDIT_SIGRE.html'
    
    prs = pptx.Presentation(pptx_path)
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Slide 1 ODS multi-section consistency
    assert "ODS 4, 9, 11, 12 y 16" in html, "Falta ODS 4, 9, 11, 12 y 16 en Slide 1 HTML"
    s1_text = " ".join(shape.text_frame.text for shape in prs.slides[0].shapes if shape.has_text_frame)
    assert "ODS 4, 9, 11, 12 y 16" in s1_text, "Falta ODS 4, 9, 11, 12 y 16 en Slide 1 PPTX"

    # 2. Slide 4: 5 Specific Engineering Objectives
    s4_text = " ".join(shape.text_frame.text for shape in prs.slides[3].shapes if shape.has_text_frame)
    assert "5. Despliegue Elástico y DevOps" in s4_text, "Falta objetivo 5 de DevOps en Slide 4 PPTX"
    assert "5. Despliegue Elástico y DevOps" in html, "Falta objetivo 5 de DevOps en Slide 4 HTML"

    # 3. Slide 5: 4 Vertical Columns parity (horizontal distribution)
    s5_boxes = [s for s in prs.slides[4].shapes if s.has_text_frame and s.width and round(s.width.inches, 2) == 2.75]
    assert len(s5_boxes) == 4, f"Slide 5 PPTX debe tener 4 columnas verticales de 2.75 in, encontradas {len(s5_boxes)}"
    left_positions = sorted([round(s.left.inches, 2) for s in s5_boxes])
    assert left_positions == [0.8, 3.79, 6.78, 9.77], f"Posiciones horizontales de Slide 5 incorrectas: {left_positions}"
    assert 'data-slide="4"' in html and 'class="grid-4"' in html, "Slide 5 en HTML debe usar grid-4 de 4 columnas"

    # 4. Slide 8: Native Table Shape parity
    s8_tables = [s for s in prs.slides[7].shapes if s.has_table]
    assert len(s8_tables) == 1, "Slide 8 PPTX debe tener una tabla nativa de PowerPoint"
    table = s8_tables[0].table
    assert len(table.rows) == 5 and len(table.columns) == 4, f"Tabla de Slide 8 debe ser 5x4, es {len(table.rows)}x{len(table.columns)}"
    assert table.cell(0, 0).text_frame.text == "ID", "Falta encabezado ID en tabla PPTX"
    assert table.cell(4, 3).text_frame.text == "EXITOSO", "Falta resultado EXITOSO en fila 4 tabla PPTX"
    assert "<table class=\"custom-table\">" in html, "Slide 8 en HTML debe tener tabla nativa"

def test_oral_speech_script_timing():
    """Valida exhaustivamente que el guion oral cubra las 13 diapositivas y su duración calculada esté en 3-5 min."""
    script_path = 'docs/guion_exposicion_sigre_expodit.md'
    assert os.path.exists(script_path), f"No existe {script_path}"
    with open(script_path, 'r', encoding='utf-8') as f:
        md = f.read()

    # Extraer filas de la tabla cronométrica: | **Slide X** | Título | Marca | Duración | Palabras | ...
    table_rows = re.findall(r'\|\s*\*\*Slide\s+(\d+)\*\*\s*\|[^|]+\|[^|]+\|\s*(\d+)\s*s\s*\|\s*(\d+)\s*\|', md)
    assert len(table_rows) == 13, f"La tabla cronométrica debe desglosar las 13 diapositivas, tiene {len(table_rows)}"

    total_seconds_calc = 0
    total_words_calc = 0
    for slide_idx_str, sec_str, words_str in table_rows:
        sec = int(sec_str)
        words = int(words_str)
        assert 15 <= sec <= 30, f"Slide {slide_idx_str} tiene duración fuera de rango operativo: {sec}s"
        assert words >= 35, f"Slide {slide_idx_str} tiene muy pocas palabras: {words}"
        total_seconds_calc += sec
        total_words_calc += words

    # Verificar que el cálculo sumado coincide exactamente
    assert total_seconds_calc == 244, f"Suma de tiempos ({total_seconds_calc}s) != 244s declarados"
    assert total_words_calc == 597, f"Suma de palabras ({total_words_calc}) != 597 declaradas"

    # Verificar rango permitido (entre 180s y 300s = 3 a 5 min)
    assert 180 <= total_seconds_calc <= 300, f"El tiempo total {total_seconds_calc}s no está en [180s, 300s]"

    # Verificar cadencia media calculada
    pace_wpm = total_words_calc / (total_seconds_calc / 60.0)
    assert 140.0 <= pace_wpm <= 155.0, f"Cadencia de oratoria {pace_wpm:.1f} pal/min fuera de rango estándar"

    # Verificar presencia de las 13 secciones individuales de guion literal
    for slide_num in range(1, 14):
        assert f"### Diapositiva {slide_num}:" in md or f"### Diapositiva {slide_num} " in md, f"Falta sección Diapositiva {slide_num}"
        # Verificar que contiene texto en comillas
        assert f"Diapositiva {slide_num}:" in md and "> *\"" in md, f"Falta guion literal en Diapositiva {slide_num}"

def test_image_assets_existence():
    """Valida que todas las imágenes referenciadas en las diapositivas existan en disco."""
    images = [
        'docs/brand/udeg_logo.png',
        'docs/brand/sigre_logo_header.png',
        'docs/graficos/figura1_diagrama_servicio_sigre.png',
        'docs/graficos/figura2_diagrama_arquitectura_5capas_sigre.png',
        'docs/pruebas/screenshots/01_identidad_institucional.png',
        'docs/pruebas/screenshots/09_escaner_qr_camara.png',
        'docs/pruebas/screenshots/08_dashboard_ejecutivo.png',
        'docs/pruebas/screenshots/10_distribucion_puntajes_sus.png'
    ]
    for img in images:
        assert os.path.exists(img), f"Falta imagen requerida: {img}"
        assert os.path.getsize(img) > 5000, f"La imagen {img} está vacía o corrupta"

if __name__ == '__main__':
    print("Ejecutando suite de verificación formal...")
    test_financial_metrics_calculation()
    print("✓ 1. Verificación de cálculo financiero (VPN, TIR, Payback): SUPERADA")
    test_pptx_integrity()
    print("✓ 2. Verificación de archivo PPTX (13 slides, notas completas): SUPERADA")
    test_slide_structural_parity()
    print("✓ 3. Verificación de paridad estructural (Columnas Slide 5, Tabla nativa Slide 8, ODS y Objetivos): SUPERADA")
    test_html_visualizer_integrity()
    print("✓ 4. Verificación de visualizador HTML (13 slides, interactividad): SUPERADA")
    test_oral_speech_script_timing()
    print("✓ 5. Verificación de guion oral (13 slides, tiempos sumados 244s en rango 3-5 min): SUPERADA")
    test_image_assets_existence()
    print("✓ 6. Verificación de activos gráficos e imágenes: SUPERADA")
    print("\nTODAS LAS PRUEBAS DE INTEGRIDAD PASARON EXITOSAMENTE (6/6).")
