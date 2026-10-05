import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def create_second_presentation():
    prs = Presentation()
    # Formato panorámico 16:9
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Paleta de Colores Ejecutiva
    NAVY = RGBColor(0, 43, 73)           # #002B49
    BLUE_ACCENT = RGBColor(0, 102, 153)  # #006699
    LIGHT_BG = RGBColor(248, 249, 250)   # #F8F9FA
    WHITE = RGBColor(255, 255, 255)
    DARK_TEXT = RGBColor(33, 37, 41)      # #212529
    MUTED_TEXT = RGBColor(108, 117, 125)
    GREEN_SUCCESS = RGBColor(25, 135, 84) # #198754
    CARD_BG = RGBColor(240, 244, 248)
    BORDER_COLOR = RGBColor(218, 224, 233)
    
    blank_layout = prs.slide_layouts[6]
    
    def set_slide_background(slide, color):
        bg = slide.background
        fill = bg.fill
        fill.solid()
        fill.fore_color.rgb = color
        
    def add_header(slide, title_text, category_text="FORMULACIÓN Y EVALUACIÓN DE PROYECTOS DE INVERSIÓN — 2DA PRESENTACIÓN"):
        # Categoría
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.35), Inches(11.7), Inches(0.35))
        tf_c = cat_box.text_frame
        tf_c.word_wrap = True
        p_c = tf_c.paragraphs[0]
        p_c.text = category_text.upper()
        p_c.font.name = "Arial"
        p_c.font.size = Pt(10)
        p_c.font.bold = True
        p_c.font.color.rgb = BLUE_ACCENT
        
        # Título
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.65), Inches(11.7), Inches(0.65))
        tf_t = title_box.text_frame
        tf_t.word_wrap = True
        p_t = tf_t.paragraphs[0]
        p_t.text = title_text
        p_t.font.name = "Arial"
        p_t.font.size = Pt(21)
        p_t.font.bold = True
        p_t.font.color.rgb = NAVY
        
    def add_notes(slide, timing_and_script):
        notes_slide = slide.notes_slide
        tf = notes_slide.notes_text_frame
        tf.text = timing_and_script

    def format_table_headers(table, headers):
        for j, h in enumerate(headers):
            cell = table.cell(0, j)
            cell.fill.solid()
            cell.fill.fore_color.rgb = NAVY
            p = cell.text_frame.paragraphs[0]
            p.text = h
            p.alignment = PP_ALIGN.CENTER
            p.font.name = "Arial"
            p.font.bold = True
            p.font.size = Pt(11)
            p.font.color.rgb = WHITE

    # =========================================================================
    # DIAPOSITIVA 1: PORTADA COMPLETA DE IDENTIFICACIÓN (0:00 - 0:45)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1, NAVY)
    
    # Membrete institucional
    box_inst = s1.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(11.7), Inches(0.7))
    tf_inst = box_inst.text_frame
    p_in = tf_inst.paragraphs[0]
    p_in.text = "UNIVERSIDAD DE GUADALAJARA | CENTRO UNIVERSITARIO DE TONALÁ"
    p_in.font.name = "Arial"
    p_in.font.size = Pt(13)
    p_in.font.bold = True
    p_in.font.color.rgb = RGBColor(180, 205, 230)
    
    p_div = tf_inst.add_paragraph()
    p_div.text = "División de Ingenierías e Innovación Tecnológica"
    p_div.font.size = Pt(11)
    p_div.font.color.rgb = RGBColor(200, 215, 230)
    
    # Título Principal
    box_main = s1.shapes.add_textbox(Inches(0.8), Inches(1.3), Inches(11.7), Inches(1.8))
    tf_main = box_main.text_frame
    tf_main.word_wrap = True
    p_m1 = tf_main.paragraphs[0]
    p_m1.text = "SIGRE: Sistema Integrado de Gestión de Recursos y Espacios"
    p_m1.font.name = "Arial"
    p_m1.font.size = Pt(28)
    p_m1.font.bold = True
    p_m1.font.color.rgb = WHITE
    
    p_m2 = tf_main.add_paragraph()
    p_m2.text = "Estimación de la Inversión Inicial, Selección de Proveedores, Estado de Resultados y Determinación de la TIR y Payback"
    p_m2.font.size = Pt(14)
    p_m2.font.color.rgb = RGBColor(190, 220, 255)
    p_m2.space_before = Pt(6)
    
    # Cuadro de Identificación (Cumplimiento estricto de Rúbrica)
    card_id = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(3.3), Inches(11.7), Inches(3.7))
    card_id.fill.solid()
    card_id.fill.fore_color.rgb = RGBColor(8, 55, 92)
    card_id.line.color.rgb = BLUE_ACCENT
    
    box_meta = s1.shapes.add_textbox(Inches(1.1), Inches(3.45), Inches(11.1), Inches(3.4))
    tf_meta = box_meta.text_frame
    tf_meta.word_wrap = True
    
    meta_lines = [
        ("Materia:", "Formulación y Evaluación de Proyectos de Inversión"),
        ("Docente Titular:", "Mtra. Abril Adriana Angulo Sherman"),
        ("Carrera:", "Ingeniería en Ciencias Computacionales / Lic. en Tecnologías de la Información"),
        ("Equipo:", "Equipo N° 4"),
        ("Integrantes:", "Integrante 1 (Cód: 219XXXXXX)  |  Integrante 2 (Cód: 219XXXXXX)  |  Integrante 3 (Cód: 219XXXXXX)"),
        ("Título de Entrega:", "Segunda Presentación: Proyecto hasta la estimación de la inversión y el retorno"),
        ("Fecha:", "Octubre de 2026 — CUTonalá, Jalisco")
    ]
    
    for idx, (label, val) in enumerate(meta_lines):
        p = tf_meta.paragraphs[0] if idx == 0 else tf_meta.add_paragraph()
        r1 = p.add_run()
        r1.text = f"{label} "
        r1.font.bold = True
        r1.font.size = Pt(11)
        r1.font.color.rgb = RGBColor(150, 205, 255)
        r2 = p.add_run()
        r2.text = val
        r2.font.size = Pt(11)
        r2.font.color.rgb = WHITE
        p.space_after = Pt(3)
        
    add_notes(s1, "TIEMPO: 0:00 - 0:45 (45 segundos)\n"
                  "GUIÓN: Buen día profesora Abril Angulo y compañeros. El Equipo 4 presenta la segunda etapa de nuestro proyecto de inversión SIGRE: Sistema Integrado de Gestión de Recursos y Espacios. En esta exposición demostraremos la viabilidad financiera integral del proyecto, desglosando la inversión inicial requerida, la evaluación competitiva de proveedores, las proyecciones de ingresos y el cálculo matemático riguroso del Valor Presente Neto (VPN), el Periodo de Recuperación de Inversión (Payback) y la Tasa Interna de Retorno (TIR).")

    # =========================================================================
    # DIAPOSITIVA 2: PLANTEAMIENTO DE LA PROBLEMÁTICA Y ANÁLISIS CAUSAL (0:45 - 1:45)
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2, LIGHT_BG)
    add_header(s2, "Diagnóstico Causal de la Problemática Patrimonial")
    
    # 3 Cajas Causales
    causes = [
        ("1. Causa Operativa: Falta de Trazabilidad",
         "Desconexión directa entre el inventario físico del almacén y el estatus real del bien (prestado, dañado o disponible). Inexistencia de conciliación en tiempo real.",
         BLUE_ACCENT),
        ("2. Causa Jurídica: Inexistencia de Responsivas",
         "Uso de libretas de papel y vales manuscritos que carecen de validez ante auditorías y firma electrónica vinculante (DOF, 2017; Universidad de Guadalajara, 2019).",
         NAVY),
        ("3. Causa Cultural: Cero Deslinde de Responsabilidad",
         "Inexistencia de un expediente histórico o puntaje de confiabilidad del usuario que deslinde responsabilidades ante mermas o imponga consecuencias de puntualidad.",
         BLUE_ACCENT)
    ]
    
    for i, (tit, desc, col) in enumerate(causes):
        left_pos = Inches(0.8 + i * 4.0)
        card = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left_pos, Inches(1.5), Inches(3.7), Inches(4.3))
        card.fill.solid()
        card.fill.fore_color.rgb = WHITE
        card.line.color.rgb = col
        card.line.width = Pt(2)
        
        tf = card.text_frame
        tf.word_wrap = True
        pt = tf.paragraphs[0]
        pt.text = tit
        pt.font.bold = True
        pt.font.size = Pt(13)
        pt.font.color.rgb = col
        pt.space_after = Pt(8)
        
        pd = tf.add_paragraph()
        pd.text = desc
        pd.font.size = Pt(11)
        pd.font.color.rgb = DARK_TEXT
        
    # Cita APA de pie
    box_apa = s2.shapes.add_textbox(Inches(0.8), Inches(6.0), Inches(11.7), Inches(0.8))
    tf_apa = box_apa.text_frame
    p_apa = tf_apa.paragraphs[0]
    p_apa.text = "Citas APA: (Cámara de Diputados del H. Congreso de la Unión, 2017; Coordinación General de Planeación y Evaluación, 2024; Universidad de Guadalajara, 2019)."
    p_apa.font.size = Pt(10)
    p_apa.font.italic = True
    p_apa.font.color.rgb = MUTED_TEXT

    add_notes(s2, "TIEMPO: 0:45 - 1:45 (60 segundos)\n"
                  "GUIÓN: Nuestra investigación en planteles de la Red Universitaria demuestra que la problemática de mermas y empalmes no es un accidente, sino el resultado de tres causas estructurales: en primer lugar, la falta de trazabilidad en tiempo real en los almacenes; en segundo lugar, la fragilidad jurídica de seguir firmando en libretas de papel que carecen de validez ante auditorías; y en tercer lugar, la falta de un sistema de incentivos y responsabilidad para los usuarios.")

    # =========================================================================
    # DIAPOSITIVA 3: PROPUESTA DE SOLUCIÓN E HIPÓTESIS (1:45 - 2:30)
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3, LIGHT_BG)
    add_header(s3, "Propuesta de Solución e Hipótesis Estructurada del Proyecto")
    
    # Cajas de Solución en la parte superior
    box_sol = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(11.7), Inches(1.8))
    box_sol.fill.solid()
    box_sol.fill.fore_color.rgb = WHITE
    box_sol.line.color.rgb = BORDER_COLOR
    
    tf_s = box_sol.text_frame
    tf_s.word_wrap = True
    ps_t = tf_s.paragraphs[0]
    ps_t.text = "Ecosistema Tecnológico SIGRE: Solución a la Problemática"
    ps_t.font.bold = True
    ps_t.font.size = Pt(13)
    ps_t.font.color.rgb = BLUE_ACCENT
    ps_t.space_after = Pt(4)
    
    ps_d = tf_s.add_paragraph()
    ps_d.text = "• Credencial y Boleto Digital con QR Dinámico  |  • Doble Checklist Digital (Entrada/Salida)\n• Responsiva PDF Automatizada con Firma Digital  |  • Puntaje de Confiabilidad del Usuario (Score 0-100)"
    ps_d.font.size = Pt(11)
    ps_d.font.color.rgb = DARK_TEXT
    
    # Caja de Hipótesis Destacada
    card_hyp = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(3.6), Inches(11.7), Inches(3.2))
    card_hyp.fill.solid()
    card_hyp.fill.fore_color.rgb = NAVY
    card_hyp.line.color.rgb = BLUE_ACCENT
    
    tf_h = card_hyp.text_frame
    tf_h.word_wrap = True
    ph_t = tf_h.paragraphs[0]
    ph_t.text = "HIPÓTESIS ESTRUCTURADA DEL PROYECTO"
    ph_t.font.bold = True
    ph_t.font.size = Pt(12)
    ph_t.font.color.rgb = RGBColor(150, 205, 255)
    ph_t.alignment = PP_ALIGN.CENTER
    ph_t.space_after = Pt(8)
    
    ph_b = tf_h.add_paragraph()
    ph_b.text = "«Si se implementa un sistema digital centralizado de gestión de recursos y espacios con responsivas electrónicas, doble checklist y trazabilidad en tiempo real de usuarios y activos (SIGRE), entonces se reducirán en al menos un 80% las mermas patrimoniales por extravío no atribuible de equipo técnico y se eliminarán al 100% los empalmes de agenda en espacios académicos de los planteles universitarios.»"
    ph_b.font.size = Pt(12)
    ph_b.font.color.rgb = WHITE
    ph_b.alignment = PP_ALIGN.CENTER
    ph_b.space_after = Pt(10)
    
    ph_v = tf_h.add_paragraph()
    ph_v.text = "• Variable Independiente (X): Implementación de la plataforma SIGRE.\n• Variable Dependiente (Y1): Reducción de mermas patrimoniales (≥ 80%).  |  • Variable Dependiente (Y2): Erradicación de empalmes (100%)."
    ph_v.font.size = Pt(10)
    ph_v.font.italic = True
    ph_v.font.color.rgb = RGBColor(200, 225, 255)
    ph_v.alignment = PP_ALIGN.CENTER

    add_notes(s3, "TIEMPO: 1:45 - 2:30 (45 segundos)\n"
                  "GUIÓN: Para resolver esta problemática formulamos SIGRE, una plataforma cloud que automatiza el préstamo con QR, firma actas digitales y asigna un puntaje de confiabilidad al usuario. Nuestra hipótesis sostiene que al implementar SIGRE, lograremos reducir al menos en un 80% la pérdida de equipo técnico y eliminar al 100% los empalmes de espacio, garantizando que el ahorro generado pague con creces la inversión.")

    # =========================================================================
    # DIAPOSITIVA 4: PÚBLICO OBJETIVO, MERCADO META Y NICHO (2:30 - 3:30)
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4, LIGHT_BG)
    add_header(s4, "Caracterización de Público Objetivo, Nicho y Mercado Meta")
    
    # Tabla APA de Mercado Meta
    rows, cols = 6, 5
    table_shape = s4.shapes.add_table(rows, cols, Inches(0.8), Inches(1.5), Inches(11.7), Inches(4.3))
    t = table_shape.table
    
    headers_m = ["Segmento Institucional", "Total Dependencias", "Mercado Meta (Año 3)", "Tarifa Anual Sugerida", "Ingresos Anuales Proyectados"]
    format_table_headers(t, headers_m)
    
    m_data = [
        ["Centros Univ. Temáticos (Metropolitanos)", "6 dependencias", "3 dependencias (50%)", "$48,000 MXN", "$144,000 MXN"],
        ["Centros Univ. Regionales (Interior)", "12 dependencias", "5 dependencias (42%)", "$48,000 MXN", "$240,000 MXN"],
        ["Preparatorias SEMS Metropolitanas", "30 dependencias", "8 dependencias (27%)", "$24,000 MXN", "$192,000 MXN"],
        ["Preparatorias SEMS Regionales", "145 dependencias", "6 dependencias (4%)", "$24,000 MXN", "$144,000 MXN"],
        ["UNIVERSO TOTAL Y META CERRADA", "193 dependencias", "22 dependencias (11.4%)", "Promedio ponderado", "$720,000 MXN"]
    ]
    
    for r_idx, row in enumerate(m_data):
        for c_idx, val in enumerate(row):
            cell = t.cell(r_idx + 1, c_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = RGBColor(230, 240, 250) if r_idx == 4 else WHITE
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.alignment = PP_ALIGN.LEFT if c_idx == 0 else PP_ALIGN.CENTER
            p.font.name = "Arial"
            p.font.size = Pt(10)
            if r_idx == 4 or c_idx == 0:
                p.font.bold = True
                
    # Nota de pie
    box_n4 = s4.shapes.add_textbox(Inches(0.8), Inches(6.0), Inches(11.7), Inches(0.8))
    tf_n4 = box_n4.text_frame
    pn4 = tf_n4.paragraphs[0]
    pn4.text = "Nicho Cautivo: Red Universitaria UdeG (193 planteles con normatividad, SIIAU y calendarios idénticos). Público Objetivo: Secretarios Adm., Almacenistas, Docentes y Alumnos."
    pn4.font.size = Pt(10)
    pn4.font.italic = True
    pn4.font.color.rgb = MUTED_TEXT

    add_notes(s4, "TIEMPO: 2:30 - 3:30 (60 segundos)\n"
                  "GUIÓN: Nuestro nicho de mercado es sumamente estratégico: las 193 dependencias de la Universidad de Guadalajara. Delimitamos a nuestros públicos en decisores, operadores y usuarios. Nuestra meta comercial al tercer año es captar 22 planteles (8 centros universitarios y 14 preparatorias), lo que representa apenas el 11.4% del mercado cautivo. Esto demuestra que nuestras proyecciones son conservadoras y alcanzables.")

    # =========================================================================
    # DIAPOSITIVA 5: ANÁLISIS DE COMPETIDORES Y VALOR AGREGADO (3:30 - 4:15)
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5, LIGHT_BG)
    add_header(s5, "Análisis de Competidores y Propuesta de Valor Agregado")
    
    rows, cols = 6, 5
    table_shape5 = s5.shapes.add_table(rows, cols, Inches(0.8), Inches(1.5), Inches(11.7), Inches(4.5))
    t5 = table_shape5.table
    
    headers_c = ["Criterio de Evaluación", "Libretas y Excel", "SIIAU Institucional", "SaaS Extranjero (USD)", "SIGRE (Nuestra Propuesta)"]
    format_table_headers(t5, headers_c)
    
    c_data = [
        ["Velocidad en ventanilla", "Lenta (3-5 min)", "No aplica a ventanilla", "Media (1.5 min)", "Ágil (< 30 seg con QR)"],
        ["Responsiva y firma legal", "Nula (firma ilegible)", "Sin responsivas", "Media (correo ext.)", "Alta (Firma digital + PDF)"],
        ["Score de Confiabilidad", "Inexistente", "Inexistente", "No disponible", "Integrado (0-100 pts)"],
        ["Costo anual por plantel", "Merma ($130k+)", "Incluido en nómina", "Alto ($60k - $90k MXN)", "Económico ($24k - $48k MXN)"],
        ["Contratación", "N/A", "Centralizado", "Licitación / Dólares", "Adjudicación Directa"]
    ]
    
    for r_idx, row in enumerate(c_data):
        for c_idx, val in enumerate(row):
            cell = t5.cell(r_idx + 1, c_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = RGBColor(225, 245, 235) if c_idx == 4 else WHITE
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.alignment = PP_ALIGN.LEFT if c_idx == 0 else PP_ALIGN.CENTER
            p.font.name = "Arial"
            p.font.size = Pt(10)
            if c_idx == 4:
                p.font.bold = True
                p.font.color.rgb = GREEN_SUCCESS
                
    add_notes(s5, "TIEMPO: 3:30 - 4:15 (45 segundos)\n"
                  "GUIÓN: Frente a las alternativas actuales —como las libretas de papel, la rigidez del SIIAU o los software extranjeros cotizados en dólares— SIGRE ofrece un valor agregado único: despachos en menos de 30 segundos con QR, actas en PDF firmadas digitalmente, puntaje de reputación para los alumnos y una tarifa diseñada para contratarse mediante adjudicación directa sin burocracia.")

    # =========================================================================
    # DIAPOSITIVA 6: PLAN DE OFERTA DEL SERVICIO Y DIAGRAMA DE FLUJO (4:15 - 5:00)
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6, LIGHT_BG)
    add_header(s6, "Plan de Oferta del Servicio: Diagrama de Flujo Operativo")
    
    # 5 Pasos del Flujo
    steps = [
        ("Etapa 1: Solicitud Online", "Usuario solicita pre-reserva desde app web/móvil con correo institucional @udg.mx."),
        ("Etapa 2: Validación Anti-Empalme", "Sistema ejecuta bloqueo temporal Redis (TTL 15 min) y valida disponibilidad temporal."),
        ("Etapa 3: Mostrador QR & Checklist", "Escaneo de QR en <30 s y checklist digital de estado del equipo a la entrega."),
        ("Etapa 4: Responsiva Digital PDF", "Generación de acta oficial firmada digitalmente con folio y marcas de tiempo."),
        ("Etapa 5: Devolución & Score", "Checklist de retorno; si el bien vuelve en regla, el usuario suma puntos de reputación.")
    ]
    
    for i, (st_tit, st_desc) in enumerate(steps):
        left_p = Inches(0.8 + i * 2.4)
        card = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left_p, Inches(1.8), Inches(2.1), Inches(4.2))
        card.fill.solid()
        card.fill.fore_color.rgb = WHITE
        card.line.color.rgb = BLUE_ACCENT
        
        tf = card.text_frame
        tf.word_wrap = True
        pt = tf.paragraphs[0]
        pt.text = st_tit
        pt.font.bold = True
        pt.font.size = Pt(11)
        pt.font.color.rgb = NAVY
        pt.space_after = Pt(6)
        
        pd = tf.add_paragraph()
        pd.text = st_desc
        pd.font.size = Pt(9.5)
        pd.font.color.rgb = DARK_TEXT

    add_notes(s6, "TIEMPO: 4:15 - 5:00 (45 segundos)\n"
                  "GUIÓN: El plan de servicio se estructura en un flujo de 5 pasos automatizados: desde la pre-reserva en línea sin empalmes, pasando por el escaneo QR en mostrador con doble checklist de salida, hasta la emisión instantánea del acta responsiva en PDF y la actualización automática del puntaje de confiabilidad del alumno al devolver el bien.")

    # =========================================================================
    # DIAPOSITIVA 7: CRONOGRAMA DE ACTIVIDADES (GANTT Y RUTA CRÍTICA) (5:00 - 5:45)
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7, LIGHT_BG)
    add_header(s7, "Cronograma de Actividades (Gantt) y Ruta Crítica [RC]")
    
    rows, cols = 9, 6
    table_shape7 = s7.shapes.add_table(rows, cols, Inches(0.8), Inches(1.5), Inches(11.7), Inches(4.5))
    t7 = table_shape7.table
    
    headers_g = ["Cód.", "Actividad del Proyecto", "Duración", "Predecesora", "Meses", "Ruta Crítica [RC]"]
    format_table_headers(t7, headers_g)
    
    gt_data = [
        ["A1", "Desarrollo y afinación del software", "3 meses", "Ninguna", "M1 a M3", "SÍ [RC]"],
        ["A2", "Despliegue de piloto CUTonalá", "2 meses", "A1", "M3 y M4", "SÍ [RC]"],
        ["A3", "Trámites legales IMPI/INDAUTOR", "4 meses", "A1", "M2 a M5", "NO (Holgura: 2m)"],
        ["A4", "Ajustes por retroalimentación", "1 mes", "A2", "M4 y M5", "SÍ [RC]"],
        ["A5", "Preparación de dossiers ROI", "1 mes", "A4", "M5", "NO (Holgura: 1m)"],
        ["A6", "Gira comercial con Secretarios Adm.", "4 meses", "A4", "M5 a M8", "SÍ [RC]"],
        ["A7", "Firma primeros contratos (2 planteles)", "2 meses", "A6", "M7 y M8", "SÍ [RC]"],
        ["A8", "Soporte y evaluación de avance", "4 meses", "A7", "M9 a M12", "SÍ [RC]"]
    ]
    
    for r_idx, row in enumerate(gt_data):
        for c_idx, val in enumerate(row):
            cell = t7.cell(r_idx + 1, c_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = RGBColor(255, 235, 235) if "SÍ" in row[5] else WHITE
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.alignment = PP_ALIGN.LEFT if c_idx == 1 else PP_ALIGN.CENTER
            p.font.name = "Arial"
            p.font.size = Pt(9.5)
            if c_idx == 5 and "SÍ" in val:
                p.font.bold = True
                p.font.color.rgb = RGBColor(200, 0, 0)
                
    add_notes(s7, "TIEMPO: 5:00 - 5:45 (45 segundos)\n"
                  "GUIÓN: El plan de producción se ejecutará en 12 meses. Identificamos la Ruta Crítica [RC] que abarca desde la afinación del software y la prueba piloto en CUTonalá, hasta la gira comercial con Secretarios Administrativos y la firma de los primeros contratos. Cualquier retraso en estas actividades críticas afectaría el calendario de ingresos.")

    # =========================================================================
    # DIAPOSITIVA 8: SELECCIÓN DE PROVEEDORES DE INSUMOS (5:45 - 6:45)
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_background(s8, LIGHT_BG)
    add_header(s8, "Investigación y Selección de Proveedores de Insumos Clave")
    
    rows, cols = 4, 5
    table_shape8 = s8.shapes.add_table(rows, cols, Inches(0.8), Inches(1.5), Inches(11.7), Inches(4.5))
    t8 = table_shape8.table
    
    headers_p = ["Insumo Requerido", "Proveedores Evaluados (Mínimo 3)", "Selección", "Criterios de Elección (No-Precio)", "Costo Estimado"]
    format_table_headers(t8, headers_p)
    
    p_data = [
        ["1. Infraestructura Cloud y Base de Datos", "• Google Cloud (GCP)\n• Amazon Web Services (AWS)\n• Microsoft Azure", "Google Cloud Platform (GCP)", "SLA del 99.9%, latencia <150 ms en México, modelo serverless Cloud Run y PostgreSQL nativo.", "$1,500 - $5,400 MXN / mes"],
        ["2. Registro Propiedad Intelectual", "• Tramitación Directa IMPI\n• Despacho Abogados PI\n• Gestoría Digital", "Tramitación Directa IMPI / INDAUTOR", "Validez jurídica oficial estricta sin comisiones intermedias y titularidad directa regulada.", "$25,000 MXN (Único)"],
        ["3. Hardware Dev & Pruebas", "• Dell Technologies\n• Lenovo México\n• HP Inc.", "Dell Technologies (Latitude / PowerEdge)", "Garantía de 3 años con atención en sitio en Jalisco, arquitectura certificada Linux/Docker.", "$45,000 MXN (CAPEX)"]
    ]
    
    for r_idx, row in enumerate(p_data):
        for c_idx, val in enumerate(row):
            cell = t8.cell(r_idx + 1, c_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = WHITE
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.alignment = PP_ALIGN.LEFT if c_idx in (0, 1, 3) else PP_ALIGN.CENTER
            p.font.name = "Arial"
            p.font.size = Pt(9.5)
            if c_idx == 2:
                p.font.bold = True
                p.font.color.rgb = BLUE_ACCENT
                
    add_notes(s8, "TIEMPO: 5:45 - 6:45 (60 segundos)\n"
                  "GUIÓN: En cumplimiento estricto con la rúbrica, investigamos al menos tres proveedores para cada insumo crítico. Elegimos Google Cloud por su SLA del 99.9% y latencia mínima en México; la tramitación directa ante IMPI e INDAUTOR para garantizar certeza jurídica sin sobrecostos de despachos; y equipos Dell por su garantía de 3 años en sitio en Jalisco. Criterios basados en calidad, confiabilidad y soporte técnico.")

    # =========================================================================
    # DIAPOSITIVA 9: PRESUPUESTO INVERSIÓN INICIAL (CAPEX) Y OPEX (6:45 - 7:45)
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_background(s9, LIGHT_BG)
    add_header(s9, "Presupuesto de Inversión Inicial (CAPEX) y Gastos Operativos (OPEX)")
    
    # Tabla CAPEX
    rows, cols = 7, 3
    table_shape9 = s9.shapes.add_table(rows, cols, Inches(0.8), Inches(1.5), Inches(11.7), Inches(4.3))
    t9 = table_shape9.table
    
    headers_cp = ["Partida de Inversión Inicial", "Destino del Gasto de Capital", "Monto Requerido (MXN)"]
    format_table_headers(t9, headers_cp)
    
    cp_data = [
        ["Optimización y pulido técnico del software", "Compensación para desarrollo durante piloto y afinación en ventanilla.", "$75,000 MXN"],
        ["Infraestructura cloud y servidores (Año 1)", "Alojamiento en GCP, base de datos PostgreSQL y certificados.", "$20,000 MXN"],
        ["Propiedad intelectual y trámites legales", "Registro de marca ante el IMPI y depósito de software en INDAUTOR.", "$25,000 MXN"],
        ["Materiales demostrativos y viáticos", "Dossiers ejecutivos impresos y traslados a planteles para ventas.", "$20,000 MXN"],
        ["Fondo de reserva y contingencia", "Respaldo de liquidez para amortiguar desfases en cobros institucionales.", "$40,000 MXN"],
        ["INVERSIÓN INICIAL TOTAL REQUERIDA", "Capital semilla solicitado para financiar validación y arranque", "$180,000 MXN"]
    ]
    
    for r_idx, row in enumerate(cp_data):
        for c_idx, val in enumerate(row):
            cell = t9.cell(r_idx + 1, c_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = RGBColor(230, 240, 250) if r_idx == 5 else WHITE
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.alignment = PP_ALIGN.LEFT if c_idx < 2 else PP_ALIGN.RIGHT
            p.font.name = "Arial"
            p.font.size = Pt(10)
            if r_idx == 5 or c_idx == 0:
                p.font.bold = True
                
    add_notes(s9, "TIEMPO: 6:45 - 7:45 (60 segundos)\n"
                  "GUIÓN: Solicitamos una inversión inicial de $180,000 pesos. Este presupuesto desglosa $75,000 en desarrollo y pruebas, $20,000 en servidores para el primer año, $25,000 en registro de marcas y derechos de autor, $20,000 en viáticos comerciales y $40,000 como fondo de contingencia. La estructura de operación es muy esbelta, con costos de servidor que inician en $1,500 pesos al mes.")

    # =========================================================================
    # DIAPOSITIVA 10: PROYECCIÓN INGRESOS Y ESTADO DE RESULTADOS (7:45 - 8:45)
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_background(s10, LIGHT_BG)
    add_header(s10, "Estado de Resultados Proforma Trienal (Cifras en Pesos MXN)")
    
    rows, cols = 10, 4
    table_shape10 = s10.shapes.add_table(rows, cols, Inches(0.8), Inches(1.5), Inches(11.7), Inches(4.5))
    t10 = table_shape10.table
    
    headers_pn = ["Rubro Contable", "Año 1 (Validación)", "Año 2 (Expansión)", "Año 3 (Madurez)"]
    format_table_headers(t10, headers_pn)
    
    pn_data = [
        ["Ingresos Totales por Suscripción", "$63,000", "$324,000", "$850,000"],
        ["Costo de Servidores y Nube (Directo)", "($18,000)", "($36,000)", "($65,000)"],
        ["Utilidad Bruta", "$45,000", "$288,000", "$785,000"],
        ["Gastos de Soporte Técnico y Depuración", "($50,000)", "($120,000)", "($240,000)"],
        ["Gastos de Vinculación y Traslados", "($15,000)", "($45,000)", "($85,000)"],
        ["Servicios Contables y Asesoría Legal", "($12,000)", "($24,000)", "($36,000)"],
        ["Utilidad de Operación (EBITDA)", "($32,000)", "$99,000", "$424,000"],
        ["Impuestos Proyectados (ISR 30%)", "$0", "($29,700)", "($127,200)"],
        ["UTILIDAD NETA DEL EJERCICIO", "($32,000)", "$69,300", "$296,800"]
    ]
    
    for r_idx, row in enumerate(pn_data):
        for c_idx, val in enumerate(row):
            cell = t10.cell(r_idx + 1, c_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = RGBColor(230, 245, 235) if r_idx in (2, 6, 8) else WHITE
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.alignment = PP_ALIGN.LEFT if c_idx == 0 else PP_ALIGN.RIGHT
            p.font.name = "Arial"
            p.font.size = Pt(9.5)
            if r_idx in (0, 2, 6, 8) or c_idx == 0:
                p.font.bold = True
                
    add_notes(s10, "TIEMPO: 7:45 - 8:45 (60 segundos)\n"
                   "GUIÓN: En el Estado de Resultados Proforma observamos el comportamiento típico de una empresa SaaS de alto impacto: un Año 1 de validación con una pérdida fiscal contable de $32,000 pesos absorbida por el capital semilla, seguida de un rápido despegue en el Año 2 con $69,300 de utilidad neta, y una consolidación en el Año 3 con $296,800 pesos netos. El punto de equilibrio se alcanza en el mes 14.")

    # =========================================================================
    # DIAPOSITIVA 11: TABLA ILUSTRATIVA EVALUACIÓN FINANCIERA (TIR, VPN, PAYBACK) (8:45 - 9:30)
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    set_slide_background(s11, LIGHT_BG)
    add_header(s11, "Tabla Ilustrativa de Evaluación Financiera: VPN, TIR y Payback")
    
    rows, cols = 8, 4
    table_shape11 = s11.shapes.add_table(rows, cols, Inches(0.8), Inches(1.4), Inches(11.7), Inches(4.5))
    t11 = table_shape11.table
    
    headers_f = ["Periodo / Indicador Financiero", "Flujo de Efectivo Neto (FEN)", "Factor Descuento (TMAR 15%)", "Valor Presente del Flujo (VP)"]
    format_table_headers(t11, headers_f)
    
    f_data = [
        ["Año 0 (Inversión Inicial CAPEX)", "($180,000.00 MXN)", "1.0000", "($180,000.00 MXN)"],
        ["Año 1 (Fase Piloto y Validación)", "($32,000.00 MXN)", "0.8696", "($27,826.09 MXN)"],
        ["Año 2 (Expansión a 8 planteles)", "$69,300.00 MXN", "0.7561", "$52,400.76 MXN"],
        ["Año 3 (Madurez con 22 planteles)", "$296,800.00 MXN", "0.6575", "$195,150.82 MXN"],
        ["VALOR PRESENTE NETO (VPN)", "Suma algebraica VP", "TMAR = 15.0% anual", "+$39,725.49 MXN"],
        ["TASA INTERNA DE RETORNO (TIR)", "Tasa donde VPN = 0", "Margen vs TMAR: +7.84%", "22.84% anual"],
        ["PERIODO DE RECUPERACIÓN (Payback)", "Recuperación del CAPEX", "Payback Descontado: M32", "Mes 28 (Año 3, Q2)"]
    ]
    
    for r_idx, row in enumerate(f_data):
        for c_idx, val in enumerate(row):
            cell = t11.cell(r_idx + 1, c_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = RGBColor(220, 245, 230) if r_idx in (4, 5, 6) else WHITE
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.alignment = PP_ALIGN.LEFT if c_idx < 2 else PP_ALIGN.RIGHT
            p.font.name = "Arial"
            p.font.size = Pt(9.5)
            if r_idx in (4, 5, 6) or c_idx == 0:
                p.font.bold = True
                if r_idx in (4, 5, 6):
                    p.font.color.rgb = GREEN_SUCCESS
                    
    # Fórmulas explícitas en pie
    box_f11 = s11.shapes.add_textbox(Inches(0.8), Inches(6.0), Inches(11.7), Inches(0.8))
    tf_f11 = box_f11.text_frame
    pf11 = tf_f11.paragraphs[0]
    pf11.text = "Fórmulas: VPN = ∑ FEN_t / (1+TMAR)^t  |  TIR: Tasa r tal que VPN = 0 (22.84% > 15.0%)  |  Payback Simple: Mes 28  |  B/C: 1.22"
    pf11.font.size = Pt(10)
    pf11.font.bold = True
    pf11.font.color.rgb = NAVY

    add_notes(s11, "TIEMPO: 8:45 - 9:30 (45 segundos)\n"
                   "GUIÓN: Aquí presentamos la tabla ilustrativa de cálculos exigida por la rúbrica. Descontando los flujos a una TMAR del 15% anual (Cetes más prima de riesgo), obtenemos un Valor Presente Neto (VPN) de +$39,725 pesos. La Tasa Interna de Retorno (TIR) alcanza el 22.84% anual, superando por 7.84 puntos nuestra tasa de corte. La inversión inicial se recupera completamente en el mes 28 (Payback simple) y el ratio Beneficio/Costo es de 1.22.")

    # =========================================================================
    # DIAPOSITIVA 12: CONCLUSIONES, OFERTA E REFERENCIAS APA (9:30 - 10:00)
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    set_slide_background(s12, LIGHT_BG)
    add_header(s12, "Conclusiones, Propuesta para el Inversionista y Referencias APA")
    
    # 2 Cajas: Izq Oferta Inversionista, Der Referencias APA
    card_inv = s12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.2))
    card_inv.fill.solid()
    card_inv.fill.fore_color.rgb = NAVY
    card_inv.line.color.rgb = BLUE_ACCENT
    
    tfi = card_inv.text_frame
    tfi.word_wrap = True
    pti = tfi.paragraphs[0]
    pti.text = "Propuesta Formal para el Inversionista"
    pti.font.bold = True
    pti.font.size = Pt(13)
    pti.font.color.rgb = RGBColor(150, 205, 255)
    pti.space_after = Pt(8)
    
    pdi = tfi.add_paragraph()
    pdi.text = "• Inversión Requerida: $180,000 MXN en Capital Semilla.\n\n• Participación: 15% en las utilidades netas del proyecto.\n\n• Retorno de Capital: Inicio de pago de dividendos en el Mes 20; amortización total del capital en el Mes 28.\n\n• Rendimiento Recurrente: Dividendo estimado de $44,000+ MXN anuales sostenibles a partir del Año 3."
    pdi.font.size = Pt(11)
    pdi.font.color.rgb = WHITE
    
    # Referencias APA
    card_ref = s12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.2))
    card_ref.fill.solid()
    card_ref.fill.fore_color.rgb = WHITE
    card_ref.line.color.rgb = BORDER_COLOR
    
    tfr = card_ref.text_frame
    tfr.word_wrap = True
    ptr = tfr.paragraphs[0]
    ptr.text = "Referencias Bibliográficas (APA 7ma Edición)"
    ptr.font.bold = True
    ptr.font.size = Pt(12)
    ptr.font.color.rgb = NAVY
    ptr.space_after = Pt(6)
    
    refs = [
        "ANUIES. (2023). Anuario estadístico de la educación superior 2022-2023.",
        "Baca Urbina, G. (2014). Evaluación de proyectos (7ma ed.). McGraw-Hill.",
        "Banco Interamericano de Desarrollo. (2020). Metodología del marco lógico.",
        "Cámara de Diputados. (2017). Ley general de protección de datos personales.",
        "CUTonalá. (2023). Plan de desarrollo de CUTonalá 2019-2025: Visión 2030.",
        "CEPAL. (2015). Metodología del marco lógico para proyectos (Manuales 68).",
        "CGPE. (2024). Numeralia institucional de la Red Universitaria. UdeG.",
        "Universidad de Guadalajara. (2019). Reglamento de adquisiciones y servicios."
    ]
    
    for r in refs:
        p = tfr.add_paragraph()
        p.text = f"• {r}"
        p.font.size = Pt(9.5)
        p.font.color.rgb = DARK_TEXT
        p.space_after = Pt(3)
        
    add_notes(s12, "TIEMPO: 9:30 - 10:00 (30 segundos)\n"
                   "GUIÓN: En conclusión, SIGRE representa un proyecto de inversión de bajo riesgo y alta rentabilidad con un impacto social y operativo directo en la Universidad de Guadalajara. Ofrecemos al inversionista el retorno completo de su capital en el mes 28 y un flujo recurrente de utilidades. Agradecemos su atención y quedamos abiertos a sus preguntas.")

    # Guardar presentación
    out_dir = r"C:\Users\hatue\Downloads\Inversion\docs"
    os.makedirs(out_dir, exist_ok=True)
    out_pptx = os.path.join(out_dir, "Segunda_Presentacion_Inversion_Retorno_SIGRE.pptx")
    prs.save(out_pptx)
    print(f"SEGUNDA PRESENTACIÓN CREADA EXITOSAMENTE EN: {out_pptx}")

if __name__ == "__main__":
    create_second_presentation()
