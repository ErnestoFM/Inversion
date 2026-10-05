import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def create_redesigned_presentation():
    prs = Presentation()
    # Formato panorámico 16:9 (13.333 x 7.5 pulgadas)
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Paleta de Colores de Marca SIGRE (Extraída de la plantilla rediseñada)
    NAVY_DARK = RGBColor(0, 43, 73)        # #002B49 (Azul Institucional Primario)
    GREEN_BRAND = RGBColor(46, 125, 87)    # #2E7D57 (Verde Esmeralda SIGRE)
    GREEN_LIGHT = RGBColor(74, 222, 128)   # #4ADE80 (Verde Claro Acento)
    BLUE_ACCENT = RGBColor(0, 102, 153)   # #006699 (Azul Tecnológico)
    LIGHT_BG = RGBColor(232, 239, 245)    # #E8EFF5 (Gris Azulado Suave de Contenido)
    WHITE = RGBColor(255, 255, 255)
    DARK_TEXT = RGBColor(33, 37, 41)      # #212529 (Texto Principal)
    MUTED_TEXT = RGBColor(108, 117, 125)
    BORDER_COLOR = RGBColor(208, 220, 222)
    HIGHLIGHT_GREEN = RGBColor(230, 245, 235)
    
    # Rutas de imágenes de marca
    BRAND_DIR = r"C:\Users\hatue\Downloads\Inversion\docs\brand"
    IMG_DIR = os.path.join(BRAND_DIR, "extracted_images")
    
    LOGO_HEADER = os.path.join(BRAND_DIR, "sigre_logo_header.png")
    UDG_LOGO = os.path.join(BRAND_DIR, "udeg_logo.png")
    LOGO_COLOR = os.path.join(IMG_DIR, "slide_2_img_12.png")
    AVATAR_2 = os.path.join(IMG_DIR, "slide_1_img_14.png")
    
    blank_layout = prs.slide_layouts[6]
    
    def set_slide_background(slide, color):
        bg = slide.background
        fill = bg.fill
        fill.solid()
        fill.fore_color.rgb = color
        
    def add_content_header(slide, title_text, category_text="FIERRO MELÉNDEZ E. H. · FORMULACIÓN Y EVALUACIÓN DE PROYECTOS"):
        # Categoría / Breadcrumb
        cat_box = slide.shapes.add_textbox(Inches(0.60), Inches(0.35), Inches(9.0), Inches(0.28))
        tf_c = cat_box.text_frame
        tf_c.word_wrap = True
        p_c = tf_c.paragraphs[0]
        p_c.text = category_text.upper()
        p_c.font.name = "Arial"
        p_c.font.size = Pt(9.5)
        p_c.font.bold = True
        p_c.font.color.rgb = BLUE_ACCENT
        
        # Título principal de la diapositiva
        tit_box = slide.shapes.add_textbox(Inches(0.60), Inches(0.60), Inches(10.5), Inches(0.55))
        tf_t = tit_box.text_frame
        tf_t.word_wrap = True
        p_t = tf_t.paragraphs[0]
        p_t.text = title_text
        p_t.font.name = "Arial"
        p_t.font.size = Pt(20)
        p_t.font.bold = True
        p_t.font.color.rgb = NAVY_DARK
        
        # Logo institucional SIGRE en esquina superior derecha (versión a color para fondos claros)
        if os.path.exists(LOGO_COLOR):
            slide.shapes.add_picture(LOGO_COLOR, Inches(10.85), Inches(0.35), width=Inches(1.85))

    def add_content_footer(slide, current_slide, total_slides=12):
        foot_box = slide.shapes.add_textbox(Inches(0.60), Inches(6.90), Inches(12.13), Inches(0.35))
        tf_f = foot_box.text_frame
        p_f = tf_f.paragraphs[0]
        p_f.text = "Fierro Meléndez Ernesto Hatuey  ·  Formulación y Evaluación de Proyectos"
        p_f.font.name = "Arial"
        p_f.font.size = Pt(9)
        p_f.font.color.rgb = MUTED_TEXT
        
        num_box = slide.shapes.add_textbox(Inches(11.50), Inches(6.90), Inches(1.23), Inches(0.35))
        tf_n = num_box.text_frame
        p_n = tf_n.paragraphs[0]
        p_n.text = f"{current_slide} / {total_slides}"
        p_n.font.name = "Arial"
        p_n.font.size = Pt(9)
        p_n.font.bold = True
        p_n.font.color.rgb = NAVY_DARK
        p_n.alignment = PP_ALIGN.RIGHT

    def format_table_headers(table, headers):
        for col_idx, text in enumerate(headers):
            cell = table.cell(0, col_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = NAVY_DARK
            p = cell.text_frame.paragraphs[0]
            p.text = text
            p.font.name = "Arial"
            p.font.size = Pt(10)
            p.font.bold = True
            p.font.color.rgb = WHITE
            p.alignment = PP_ALIGN.CENTER

    def add_notes(slide, notes_text):
        notes_slide = slide.notes_slide
        text_frame = notes_slide.notes_text_frame
        text_frame.text = notes_text

    # =========================================================================
    # DIAPOSITIVA 1: PORTADA INSTITUCIONAL REDISEÑADA (0:00 - 0:45)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1, NAVY_DARK)
    
    # Barra lateral verde institucional (branding visual)
    stripe = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(0.25), Inches(7.5))
    stripe.fill.solid()
    stripe.fill.fore_color.rgb = GREEN_BRAND
    stripe.line.fill.background()
    
    # Logo SIGRE
    if os.path.exists(LOGO_HEADER):
        s1.shapes.add_picture(LOGO_HEADER, Inches(0.90), Inches(0.70), width=Inches(2.40))
        
    # Subtítulo institucional UdeG / CUTonalá
    box_subinst = s1.shapes.add_textbox(Inches(0.90), Inches(1.85), Inches(10.0), Inches(0.35))
    tf_si = box_subinst.text_frame
    p_si = tf_si.paragraphs[0]
    p_si.text = "UNIVERSIDAD DE GUADALAJARA  ·  CENTRO UNIVERSITARIO DE TONALÁ (CUTONALÁ)"
    p_si.font.name = "Arial"
    p_si.font.size = Pt(10.5)
    p_si.font.bold = True
    p_si.font.color.rgb = RGBColor(150, 205, 255)
    
    # Título Principal del Proyecto
    box_title = s1.shapes.add_textbox(Inches(0.90), Inches(2.20), Inches(10.50), Inches(1.20))
    tf_t = box_title.text_frame
    tf_t.word_wrap = True
    pt = tf_t.paragraphs[0]
    pt.text = "SIGRE: Sistema Integrado de Gestión de Recursos y Espacios"
    pt.font.name = "Arial"
    pt.font.size = Pt(26)
    pt.font.bold = True
    pt.font.color.rgb = WHITE
    
    # Subtítulo descriptivo de la etapa de evaluación
    box_desc = s1.shapes.add_textbox(Inches(0.90), Inches(3.45), Inches(10.50), Inches(0.60))
    tf_d = box_desc.text_frame
    tf_d.word_wrap = True
    pd = tf_d.paragraphs[0]
    pd.text = "Estimación de la Inversión Inicial, Selección de Proveedores, Estado de Resultados y Determinación de la TIR y Payback"
    pd.font.name = "Arial"
    pd.font.size = Pt(12)
    pd.font.color.rgb = RGBColor(210, 225, 240)
    
    # Línea decorativa
    div_line = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.90), Inches(4.30), Inches(10.50), Inches(0.02))
    div_line.fill.solid()
    div_line.fill.fore_color.rgb = BLUE_ACCENT
    div_line.line.fill.background()
    
    # Sección de Presentador Individual
    box_lbl = s1.shapes.add_textbox(Inches(0.90), Inches(4.55), Inches(6.00), Inches(0.28))
    tf_lbl = box_lbl.text_frame
    p_lbl = tf_lbl.paragraphs[0]
    p_lbl.text = "PRESENTADO POR"
    p_lbl.font.name = "Arial"
    p_lbl.font.size = Pt(10)
    p_lbl.font.bold = True
    p_lbl.font.color.rgb = RGBColor(150, 205, 255)
    
    # Avatar y nombre del presentador
    c_bg = s1.shapes.add_shape(MSO_SHAPE.OVAL, Inches(0.90), Inches(4.90), Inches(0.38), Inches(0.38))
    c_bg.fill.solid()
    c_bg.fill.fore_color.rgb = GREEN_BRAND
    c_bg.line.fill.background()
    
    if os.path.exists(AVATAR_2):
        s1.shapes.add_picture(AVATAR_2, Inches(0.95), Inches(4.95), width=Inches(0.28), height=Inches(0.28))
        
    t_box = s1.shapes.add_textbox(Inches(1.38), Inches(4.90), Inches(5.50), Inches(0.38))
    tf_tb = t_box.text_frame
    tf_tb.word_wrap = True
    ptb = tf_tb.paragraphs[0]
    ptb.text = "Fierro Meléndez Ernesto Hatuey"
    ptb.font.name = "Arial"
    ptb.font.size = Pt(12)
    ptb.font.bold = True
    ptb.font.color.rgb = WHITE
        
    # Recuadro de Metadatos del Curso (lado izquierdo inferior)
    box_meta = s1.shapes.add_textbox(Inches(0.90), Inches(5.65), Inches(9.20), Inches(1.20))
    tf_m = box_meta.text_frame
    tf_m.word_wrap = True
    pm1 = tf_m.paragraphs[0]
    
    r_mat1 = pm1.add_run()
    r_mat1.text = "MATERIA: "
    r_mat1.font.bold = True
    r_mat1.font.size = Pt(10)
    r_mat1.font.color.rgb = GREEN_LIGHT
    
    r_mat2 = pm1.add_run()
    r_mat2.text = "Formulación y Evaluación de Proyectos de Inversión      "
    r_mat2.font.size = Pt(10)
    r_mat2.font.color.rgb = WHITE
    
    r_doc1 = pm1.add_run()
    r_doc1.text = "DOCENTE: "
    r_doc1.font.bold = True
    r_doc1.font.size = Pt(10)
    r_doc1.font.color.rgb = GREEN_LIGHT
    
    r_doc2 = pm1.add_run()
    r_doc2.text = "Mtra. Abril Adriana Angulo Sherman\n"
    r_doc2.font.size = Pt(10)
    r_doc2.font.color.rgb = WHITE
    
    r_fec1 = pm1.add_run()
    r_fec1.text = "CARRERA: "
    r_fec1.font.bold = True
    r_fec1.font.size = Pt(10)
    r_fec1.font.color.rgb = GREEN_LIGHT
    
    r_fec2 = pm1.add_run()
    r_fec2.text = "Ingeniería en Ciencias Computacionales / Lic. en Tecnologías de la Información      "
    r_fec2.font.size = Pt(10)
    r_fec2.font.color.rgb = WHITE
    
    r_fec3 = pm1.add_run()
    r_fec3.text = "FECHA: "
    r_fec3.font.bold = True
    r_fec3.font.size = Pt(10)
    r_fec3.font.color.rgb = GREEN_LIGHT
    
    r_fec4 = pm1.add_run()
    r_fec4.text = "Octubre de 2026 — CUTonalá"
    r_fec4.font.size = Pt(10)
    r_fec4.font.color.rgb = WHITE

    # Escudo Oficial de la Universidad de Guadalajara (inferior derecha)
    if os.path.exists(UDG_LOGO):
        s1.shapes.add_picture(UDG_LOGO, Inches(10.60), Inches(4.85), width=Inches(2.00), height=Inches(2.00))

    add_notes(s1, "TIEMPO: 0:00 - 0:45 (45 segundos)\n"
                  "GUIÓN: Buen día profesora Abril Angulo y compañeros. Mi nombre es Ernesto Hatuey Fierro Meléndez y presento la segunda etapa de mi proyecto de inversión SIGRE: Sistema Integrado de Gestión de Recursos y Espacios. En esta exposición demostraré la viabilidad financiera integral del proyecto, desglosando la inversión inicial requerida, la evaluación competitiva de proveedores, las proyecciones de ingresos y el cálculo matemático riguroso del Valor Presente Neto (VPN), el Periodo de Recuperación de Inversión (Payback) y la Tasa Interna de Retorno (TIR).")

    # =========================================================================
    # DIAPOSITIVA 2: ANÁLISIS CAUSAL DE LA PROBLEMÁTICA (0:45 - 1:45)
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2, LIGHT_BG)
    add_content_header(s2, "Diagnóstico Causal de la Problemática Patrimonial")
    add_content_footer(s2, 2)
    
    causes = [
        ("1. Causa Operativa: Falta de Trazabilidad",
         "Desconexión directa entre el inventario físico del almacén y el estatus real del bien (prestado, dañado o disponible). Inexistencia de conciliación automatizada en tiempo real.",
         "Mermas superiores al 12% del inventario técnico y tiempos muertos en mostrador de 15 a 20 min en horas pico."),
        ("2. Causa Jurídica: Validez Nula en Auditoría",
         "Uso de libretas de mostrador y hojas sueltas firmadas en tinta sin validez probatoria ante Contraloría, careciendo de cadena de custodia formal o sellado criptográfico.",
         "Imposibilidad jurídica para fincar responsabilidades administrativas o económicas; costos absorbidos por la partida de gastos del plantel."),
        ("3. Causa Cultural: Ausencia de Incentivos",
         "Falta de consecuencias institucionales por entrega tardía o daño accidental. Los usuarios no cuentan con un historial o índice de cumplimiento verificable.",
         "Equipos retenidos por semanas sin sanción efectiva; colisiones en reservas de auditorios por traslape de solicitudes manuales.")
    ]
    
    col_w = Inches(3.85)
    col_gap = Inches(0.28)
    left_start = Inches(0.60)
    top_pos = Inches(1.50)
    card_h = Inches(4.50)
    
    for i, (tit, causa, efecto) in enumerate(causes):
        cur_left = left_start + i * (col_w + col_gap)
        card = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, cur_left, top_pos, col_w, card_h)
        card.fill.solid()
        card.fill.fore_color.rgb = WHITE
        card.line.color.rgb = BORDER_COLOR
        card.line.width = Pt(1.5)
        
        # Franja superior coloreada
        h_bar = s2.shapes.add_shape(MSO_SHAPE.RECTANGLE, cur_left, top_pos, col_w, Inches(0.55))
        h_bar.fill.solid()
        h_bar.fill.fore_color.rgb = NAVY_DARK if i < 2 else GREEN_BRAND
        h_bar.line.fill.background()
        
        tf_h = h_bar.text_frame
        ph = tf_h.paragraphs[0]
        ph.text = tit
        ph.font.name = "Arial"
        ph.font.size = Pt(11)
        ph.font.bold = True
        ph.font.color.rgb = WHITE
        ph.alignment = PP_ALIGN.CENTER
        
        # Contenido de la tarjeta
        tf_c = card.text_frame
        tf_c.word_wrap = True
        
        # Espacio para el header bar
        p_sp = tf_c.paragraphs[0]
        p_sp.text = ""
        p_sp.font.size = Pt(26)
        
        p_sub1 = tf_c.add_paragraph()
        p_sub1.text = "DIAGNÓSTICO ESTRUCTURAL:"
        p_sub1.font.name = "Arial"
        p_sub1.font.size = Pt(9.5)
        p_sub1.font.bold = True
        p_sub1.font.color.rgb = BLUE_ACCENT
        p_sub1.space_after = Pt(4)
        
        p_txt1 = tf_c.add_paragraph()
        p_txt1.text = causa
        p_txt1.font.name = "Arial"
        p_txt1.font.size = Pt(10)
        p_txt1.font.color.rgb = DARK_TEXT
        p_txt1.space_after = Pt(14)
        
        p_sub2 = tf_c.add_paragraph()
        p_sub2.text = "IMPACTO PATRIMONIAL:"
        p_sub2.font.name = "Arial"
        p_sub2.font.size = Pt(9.5)
        p_sub2.font.bold = True
        p_sub2.font.color.rgb = RGBColor(180, 40, 40)
        p_sub2.space_after = Pt(4)
        
        p_txt2 = tf_c.add_paragraph()
        p_txt2.text = efecto
        p_txt2.font.name = "Arial"
        p_txt2.font.size = Pt(10)
        p_txt2.font.color.rgb = DARK_TEXT
        
    add_notes(s2, "TIEMPO: 0:45 - 1:45 (60 segundos)\n"
                  "GUIÓN: Mi investigación en planteles de la Red Universitaria demuestra que la problemática de mermas y empalmes no es un accidente, sino el resultado de tres causas estructurales: en primer lugar, la falta de trazabilidad en tiempo real en los almacenes; en segundo lugar, la fragilidad jurídica de seguir firmando en libretas de papel que carecen de validez ante auditorías; y en tercer lugar, la falta de un sistema de incentivos y responsabilidad para los usuarios.")

    # =========================================================================
    # DIAPOSITIVA 3: HIPÓTESIS Y PROPUESTA DE VALOR (1:45 - 2:30)
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3, LIGHT_BG)
    add_content_header(s3, "Hipótesis Central de Solución y Métricas de Validación")
    add_content_footer(s3, 3)
    
    # Tarjeta de Hipótesis Central
    hip_card = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.60), Inches(1.50), Inches(12.10), Inches(1.60))
    hip_card.fill.solid()
    hip_card.fill.fore_color.rgb = WHITE
    hip_card.line.color.rgb = GREEN_BRAND
    hip_card.line.width = Pt(2)
    
    tf_hip = hip_card.text_frame
    tf_hip.word_wrap = True
    p_h1 = tf_hip.paragraphs[0]
    p_h1.text = "HIPÓTESIS DE IMPACTO INSTITUCIONAL:"
    p_h1.font.name = "Arial"
    p_h1.font.size = Pt(11)
    p_h1.font.bold = True
    p_h1.font.color.rgb = GREEN_BRAND
    p_h1.space_after = Pt(4)
    
    p_h2 = tf_hip.add_paragraph()
    p_h2.text = ("\"La implementación de una plataforma cloud con validación de préstamos vía QR, emisión instantánea de actas digitales "
                 "y cálculo de reputación del usuario reducirá en más del 80% las mermas no justificadas de equipo técnico en los planteles de la Red UdeG, "
                 "erradicará el 100% de los empalmes en espacios compartidos y generará ahorros operativos superiores al costo de suscripción institucional.\"")
    p_h2.font.name = "Arial"
    p_h2.font.size = Pt(11.5)
    p_h2.font.italic = True
    p_h2.font.color.rgb = NAVY_DARK
    
    # 4 Tarjetas de Métricas de Validación
    metrics = [
        ("-80%", "Reducción de Mermas", "Disminución comprobada en pérdidas de proyectores, cables HDMI, cámaras y laptops."),
        ("100%", "Eliminación de Empalmes", "Detección atómica en base de datos que bloquea dobles reservas en auditorios."),
        ("<30s", "Velocidad en Ventanilla", "Despacho automatizado escaneando el código QR personal de la credencial digital."),
        ("1.2x+", "Retorno de Inversión (ROI)", "El valor del equipo salvado supera con creces la inversión en la suscripción.")
    ]
    
    mw = Inches(2.80)
    mg = Inches(0.30)
    for i, (val, tit, desc) in enumerate(metrics):
        m_left = Inches(0.60) + i * (mw + mg)
        m_card = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, m_left, Inches(3.35), mw, Inches(2.65))
        m_card.fill.solid()
        m_card.fill.fore_color.rgb = WHITE
        m_card.line.color.rgb = BORDER_COLOR
        
        tf_m = m_card.text_frame
        tf_m.word_wrap = True
        
        pv = tf_m.paragraphs[0]
        pv.text = val
        pv.font.name = "Arial"
        pv.font.size = Pt(32)
        pv.font.bold = True
        pv.font.color.rgb = GREEN_BRAND if i in (0, 1) else BLUE_ACCENT
        pv.alignment = PP_ALIGN.CENTER
        
        ptm = tf_m.add_paragraph()
        ptm.text = tit
        ptm.font.name = "Arial"
        ptm.font.size = Pt(11)
        ptm.font.bold = True
        ptm.font.color.rgb = NAVY_DARK
        ptm.alignment = PP_ALIGN.CENTER
        ptm.space_after = Pt(6)
        
        pdm = tf_m.add_paragraph()
        pdm.text = desc
        pdm.font.name = "Arial"
        pdm.font.size = Pt(9.5)
        pdm.font.color.rgb = DARK_TEXT
        pdm.alignment = PP_ALIGN.CENTER
        
    add_notes(s3, "TIEMPO: 1:45 - 2:30 (45 segundos)\n"
                  "GUIÓN: Para resolver esta problemática formulé SIGRE, una plataforma cloud que automatiza el préstamo con QR, firma actas digitales y asigna un puntaje de confiabilidad al usuario. Mi hipótesis sostiene que al implementar SIGRE, lograré reducir al menos en un 80% la pérdida de equipo técnico y eliminar al 100% los empalmes de espacio, garantizando que el ahorro generado pague con creces la inversión.")

    # =========================================================================
    # DIAPOSITIVA 4: MERCADO META REALISTA EN 3 FASES (2:30 - 3:30)
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4, LIGHT_BG)
    add_content_header(s4, "Estrategia Pragmática de Mercado: Escalamiento en Tres Fases")
    add_content_footer(s4, 4)
    
    rows, cols = 5, 5
    table_shape = s4.shapes.add_table(rows, cols, Inches(0.60), Inches(1.50), Inches(12.10), Inches(4.30))
    t = table_shape.table
    
    headers_m = ["Fase de Escalamiento", "Plantel Objetivo y Dependencias", "Objetivo Técnico y Operativo", "Modelo de Contratación", "Ingreso Anual Proyectado"]
    format_table_headers(t, headers_m)
    
    m_data = [
        ["Fase 1: Piloto Local (Año 1)", "CUTonalá (3 almacenes: CTA, Labs Cómputo e Ingenierías)", "Validación técnica en campo con usuarios y almacenistas reales", "Convenio de prueba piloto y soporte", "$48,000 MXN"],
        ["Fase 2: Versión Pulida (Año 2)", "CUTonalá (Campus Completo) + CUCEI (Fase inicial)", "Optimización de arquitectura cloud y menor costo marginal por transacción", "Licencia anual CUT ($12k/m) + CUCEI semestral", "$216,000 MXN"],
        ["Fase 3: Consolidación (Año 3)", "CUTonalá + CUCEI + CUCEA + Prepa Tonalá (4 planteles)", "Consolidación regional del estándar de gestión en la ZMG", "Licencias de Campus completas", "$500,000 MXN"],
        ["TOTALES Y METAS (AÑO 3)", "Apenas 4 planteles de 193 dependencias de la Red UdeG (2.0%)", "Estrategia de penetración realista y disciplinada sin depender de adopción masiva", "Contratos por Adjudicación Directa", "$500,000 MXN / año"]
    ]
    
    for r_idx, row in enumerate(m_data):
        for c_idx, val in enumerate(row):
            cell = t.cell(r_idx + 1, c_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = HIGHLIGHT_GREEN if r_idx == 3 else WHITE
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.alignment = PP_ALIGN.LEFT if c_idx < 3 else PP_ALIGN.CENTER
            p.font.name = "Arial"
            p.font.size = Pt(9.5)
            if r_idx == 3 or c_idx == 0:
                p.font.bold = True
                
    box_n4 = s4.shapes.add_textbox(Inches(0.60), Inches(6.00), Inches(12.10), Inches(0.70))
    tf_n4 = box_n4.text_frame
    pn4 = tf_n4.paragraphs[0]
    pn4.text = "Estrategia Pragmática en 3 Fases: Reconociendo la dificultad burocrática de la UdeG, el modelo inicia con pruebas piloto en casa (CUTonalá), avanza a una versión pulida de menor costo en el Año 2, y consolida solo 4 planteles en el Año 3 (el 2.0% de la red de 193 dependencias)."
    pn4.font.name = "Arial"
    pn4.font.size = Pt(9.5)
    pn4.font.italic = True
    pn4.font.color.rgb = MUTED_TEXT

    add_notes(s4, "TIEMPO: 2:30 - 3:30 (60 segundos)\n"
                  "GUIÓN: Reconozco con total honestidad la realidad política y burocrática de la Universidad de Guadalajara: venderle a 193 dependencias de golpe es una fantasía irreal; conseguir que un solo centro adopte una plataforma ya es un reto mayúsculo. Por eso, mi estrategia es de escalamiento medido en tres fases: en el Año 1 me enfoco exclusivamente en hacer pruebas piloto en casa, en CUTonalá, en sus 3 almacenes clave, validando que el sistema no falle. En el Año 2, con la retroalimentación de los usuarios, despliego una versión mucho más pulida con un costo operativo menor, formalizando el contrato anual de CUTonalá y sumando a nuestro centro hermano CUCEI. Para el Año 3, consolido el servicio en 3 centros universitarios y 1 preparatoria. Conquistar solo 4 planteles en tres años representa apenas el 2% del mercado, pero genera los $500,000 pesos anuales necesarios para hacer a SIGRE plenamente autosustentable y altamente rentable.")

    # =========================================================================
    # DIAPOSITIVA 5: ANÁLISIS DE COMPETIDORES Y VALOR AGREGADO (3:30 - 4:15)
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5, LIGHT_BG)
    add_content_header(s5, "Análisis de Competidores y Propuesta de Valor Agregado")
    add_content_footer(s5, 5)
    
    rows, cols = 5, 5
    table_shape5 = s5.shapes.add_table(rows, cols, Inches(0.60), Inches(1.50), Inches(12.10), Inches(4.50))
    t5 = table_shape5.table
    
    headers_c = ["Criterio de Evaluación", "Libretas y Vales de Papel", "Módulos de SIIAU / UdeG", "Software Extranjero (SaaS)", "Propuesta de Valor: SIGRE"]
    format_table_headers(t5, headers_c)
    
    c_data = [
        ["Velocidad de Despacho", "10 a 15 min en mostrador", "5 a 8 min (sistemas lentos)", "1 a 2 min (requiere escáner)", "< 30 segundos (Escaneo QR)"],
        ["Validez Jurídica de Firma", "Nula ante auditorías", "Básica (solo registro web)", "Válida (cotizada en dólares)", "Acta digital PDF con hash criptográfico"],
        ["Incentivos y Reputación", "Inexistente", "Solo sanciones manuales", "Incentivos no aplicables a UdeG", "Scoring algorítmico por usuario"],
        ["Esquema de Contratación", "Gasto corriente en papel", "Desarrollo interno congelado", "Licitación compleja y cara", "Adjudicación directa sin burocracia"]
    ]
    
    for r_idx, row in enumerate(c_data):
        for c_idx, val in enumerate(row):
            cell = t5.cell(r_idx + 1, c_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = HIGHLIGHT_GREEN if c_idx == 4 else WHITE
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.alignment = PP_ALIGN.LEFT if c_idx == 0 else PP_ALIGN.CENTER
            p.font.name = "Arial"
            p.font.size = Pt(9.5)
            if c_idx == 4 or c_idx == 0:
                p.font.bold = True
                if c_idx == 4:
                    p.font.color.rgb = GREEN_BRAND
                    
    add_notes(s5, "TIEMPO: 3:30 - 4:15 (45 segundos)\n"
                  "GUIÓN: Frente a las alternativas actuales —como las libretas de papel, la rigidez del SIIAU o los software extranjeros cotizados en dólares— SIGRE ofrece un valor agregado único: despachos en menos de 30 segundos con QR, actas en PDF firmadas digitalmente, puntaje de reputación para los alumnos y una tarifa diseñada para contratarse mediante adjudicación directa sin burocracia.")

    # =========================================================================
    # DIAPOSITIVA 6: PLAN DE SERVICIO OPERATIVO (4:15 - 5:00)
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6, LIGHT_BG)
    add_content_header(s6, "Plan de Servicio Operativo: Flujo de 5 Pasos en Ventanilla")
    add_content_footer(s6, 6)
    
    steps = [
        ("Paso 1: Solicitud Web", "Pre-reserva y Módulo Anti-empalmes", "El alumno solicita el bien o aula desde la web. El motor verifica automáticamente que no haya empalmes de horario."),
        ("Paso 2: Token QR", "Emisión de Código Cifrado Dinámico", "Se genera un ticket digital con token QR temporal de 15 min, blindado contra capturas de pantalla apócrifas."),
        ("Paso 3: Ventanilla", "Despacho y Doble Checklist Físico", "El operador escanea el QR en ventanilla en menos de 30 s, cotejando accesorios físicos en pantalla."),
        ("Paso 4: Acta Digital", "Generación de PDF con Validez Legal", "Se compila y sella el acta responsiva en PDF con hash criptográfico y firma digitalizada en la nube."),
        ("Paso 5: Devolución", "Cierre de Folio y Scoring de Alumno", "Al retornar el bien, el folio se cierra sin libretas y el sistema actualiza la reputación del solicitante.")
    ]
    
    sw = Inches(2.26)
    sg = Inches(0.20)
    for i, (st_tit, st_sub, st_desc) in enumerate(steps):
        s_left = Inches(0.60) + i * (sw + sg)
        s_card = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, s_left, Inches(1.50), sw, Inches(4.50))
        s_card.fill.solid()
        s_card.fill.fore_color.rgb = WHITE
        s_card.line.color.rgb = BORDER_COLOR
        s_card.line.width = Pt(1.5)
        
        # Encabezado
        sh_bar = s6.shapes.add_shape(MSO_SHAPE.RECTANGLE, s_left, Inches(1.50), sw, Inches(0.60))
        sh_bar.fill.solid()
        sh_bar.fill.fore_color.rgb = NAVY_DARK if i % 2 == 0 else BLUE_ACCENT
        sh_bar.line.fill.background()
        
        tf_sh = sh_bar.text_frame
        psh = tf_sh.paragraphs[0]
        psh.text = st_tit
        psh.font.name = "Arial"
        psh.font.size = Pt(10)
        psh.font.bold = True
        psh.font.color.rgb = WHITE
        psh.alignment = PP_ALIGN.CENTER
        
        # Cuerpo
        tf_sc = s_card.text_frame
        tf_sc.word_wrap = True
        
        psp = tf_sc.paragraphs[0]
        psp.text = ""
        psp.font.size = Pt(28)
        
        psub = tf_sc.add_paragraph()
        psub.text = st_sub
        psub.font.name = "Arial"
        psub.font.size = Pt(10)
        psub.font.bold = True
        psub.font.color.rgb = GREEN_BRAND
        psub.space_after = Pt(8)
        
        pd = tf_sc.add_paragraph()
        pd.text = st_desc
        pd.font.name = "Arial"
        pd.font.size = Pt(9.5)
        pd.font.color.rgb = DARK_TEXT

    add_notes(s6, "TIEMPO: 4:15 - 5:00 (45 segundos)\n"
                  "GUIÓN: El plan de servicio se estructura en un flujo de 5 pasos automatizados: desde la pre-reserva en línea sin empalmes, pasando por el escaneo QR en mostrador con doble checklist de salida, hasta la emisión instantánea del acta responsiva en PDF y la actualización automática del puntaje de confiabilidad del alumno al devolver el bien.")

    # =========================================================================
    # DIAPOSITIVA 7: CRONOGRAMA GANTT Y RUTA CRÍTICA REALISTA (5:00 - 5:45)
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7, LIGHT_BG)
    add_content_header(s7, "Cronograma de Actividades (Gantt) y Ruta Crítica [RC]")
    add_content_footer(s7, 7)
    
    rows, cols = 9, 6
    table_shape7 = s7.shapes.add_table(rows, cols, Inches(0.60), Inches(1.50), Inches(12.10), Inches(4.50))
    t7 = table_shape7.table
    
    headers_g = ["Cód.", "Actividad del Proyecto", "Duración", "Predecesora", "Meses de Ejecución", "Ruta Crítica [RC]"]
    format_table_headers(t7, headers_g)
    
    # Secuencia lógica: Validación piloto primero, INDAUTOR hacia el final tras estabilidad
    gt_data = [
        ["A1", "Desarrollo del núcleo MVP y arquitectura cloud", "3 meses", "Ninguna", "Mes 1 a Mes 3", "SÍ [RC]"],
        ["A2", "Aviso de Privacidad y Términos de Servicio (LGPDPPSO)", "2 meses", "Ninguna", "Mes 2 y Mes 3", "NO (Holgura: 1m)"],
        ["A3", "Gestión de anuencia y acuerdo de prueba piloto CUTonalá", "2 meses", "A1, A2", "Mes 3 y Mes 4", "SÍ [RC]"],
        ["A4", "Despliegue y pruebas de campo en ventanillas CUTonalá", "3 meses", "A3", "Mes 4 a Mes 6", "SÍ [RC]"],
        ["A5", "Depuración, optimización de nube y pulido de software", "2 meses", "A4", "Mes 6 y Mes 7", "SÍ [RC]"],
        ["A6", "Formalización del contrato anual de servicio en CUTonalá", "2 meses", "A5", "Mes 7 y Mes 8", "SÍ [RC]"],
        ["A7", "Depósito formal de derechos de autor (INDAUTOR)", "3 meses", "A5", "Mes 8 a Mes 10", "NO (Holgura: 2m)"],
        ["A8", "Soporte continuo y preparación de réplica a CUCEI", "4 meses", "A6", "Mes 9 a Mes 12", "SÍ [RC]"]
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
                  "GUIÓN: El plan de ejecución de 12 meses prioriza la validación real antes de cualquier trámite formal innecesario. Primero desarrollamos el prototipo MVP y formalizamos los términos de privacidad requeridos por la ley de datos. Con eso en orden, gestionamos la anuencia de la Secretaría Administrativa de CUTonalá para desplegar el piloto en ventanilla durante los meses 4 a 6. Una vez que el sistema fue probado y afinado con retroalimentación real, formalizamos el contrato anual de CUTonalá en el Mes 8 y procedemos al depósito de derechos de autor ante el INDAUTOR del código ya estable. La Ruta Crítica enlaza A1 -> A3 -> A4 -> A5 -> A6 -> A8.")

    # =========================================================================
    # DIAPOSITIVA 8: SELECCIÓN DE PROVEEDORES (5:45 - 6:45)
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_background(s8, LIGHT_BG)
    add_content_header(s8, "Investigación y Selección de Proveedores de Insumos Clave")
    add_content_footer(s8, 8)
    
    rows, cols = 4, 5
    table_shape8 = s8.shapes.add_table(rows, cols, Inches(0.60), Inches(1.50), Inches(12.10), Inches(4.50))
    t8 = table_shape8.table
    
    headers_p = ["Insumo Requerido", "Proveedores Evaluados (Mínimo 3)", "Selección", "Criterios de Elección (No-Precio)", "Costo Estimado"]
    format_table_headers(t8, headers_p)
    
    p_data = [
        ["1. Infraestructura Cloud y Base de Datos", "• Google Cloud (GCP)\n• Amazon Web Services (AWS)\n• Microsoft Azure", "Google Cloud Platform (GCP)", "SLA del 99.9%, latencia <150 ms en México, modelo serverless Cloud Run y PostgreSQL nativo.", "$1,200 - $2,800 MXN / mes"],
        ["2. Cumplimiento Normativo y Privacidad", "• Asesoría Privacidad TI\n• Despacho Externo PI\n• Gestoría Digital", "Asesoría LGPDPPSO + Trámite Directo INDAUTOR", "Certeza jurídica en protección de datos de alumnos UdeG y titularidad oficial del software sin intermediarios.", "$12,000 MXN (Único)"],
        ["3. Hardware de Ventanilla y Pruebas", "• Dell Technologies\n• Lenovo México\n• HP Inc.", "Dell Technologies (Lectores QR + Terminal)", "Garantía de 3 años en sitio en Jalisco, lectores de uso rudo en mostrador y soporte Linux/Docker.", "$20,000 MXN (CAPEX)"]
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
                p.font.color.rgb = GREEN_BRAND
                
    add_notes(s8, "TIEMPO: 5:45 - 6:45 (60 segundos)\n"
                  "GUIÓN: En cumplimiento estricto con la rúbrica, investigué al menos tres opciones para cada insumo. Elegí Google Cloud por su SLA del 99.9% y costo flexible serverless; asesoría especializada para el Aviso de Privacidad y trámite directo ante INDAUTOR para garantizar titularidad sin intermediarios; y lectores industriales Dell para soportar el uso rudo en las ventanillas de almacén de CUTonalá. Criterios basados en confiabilidad, disponibilidad y durabilidad.")

    # =========================================================================
    # DIAPOSITIVA 9: PRESUPUESTO INVERSIÓN INICIAL (CAPEX = $140,000 MXN) (6:45 - 7:45)
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_background(s9, LIGHT_BG)
    add_content_header(s9, "Presupuesto de Inversión Inicial (CAPEX = $140,000 MXN)")
    add_content_footer(s9, 9)
    
    rows, cols = 8, 3
    table_shape9 = s9.shapes.add_table(rows, cols, Inches(0.60), Inches(1.50), Inches(12.10), Inches(4.50))
    t9 = table_shape9.table
    
    headers_cp = ["Partida de Inversión Inicial", "Destino del Gasto de Capital", "Monto Requerido (MXN)"]
    format_table_headers(t9, headers_cp)
    
    cp_data = [
        ["Desarrollo del núcleo MVP y pruebas técnicas", "Compensación de desarrollo full-stack, configuración de arquitectura y pruebas.", "$60,000 MXN"],
        ["Infraestructura cloud y servidores (Año 1)", "Hosting en Google Cloud Platform (Cloud Run, PostgreSQL y almacenamiento).", "$16,000 MXN"],
        ["Hardware de ventanilla y pruebas (CUTonalá)", "2 lectores ópticos QR industriales para mostrador y terminal de pruebas.", "$20,000 MXN"],
        ["Cumplimiento normativo y marco de privacidad", "Elaboración de Aviso de Privacidad (LGPDPPSO), convenio piloto y reserva INDAUTOR.", "$12,000 MXN"],
        ["Materiales operativos, señalética y traslados", "Placas acrílicas con QR para almacenes, manuales y viáticos de operación en CUTonalá.", "$12,000 MXN"],
        ["Fondo de reserva y contingencia operativa", "Respaldo de liquidez para eventualidades técnicas y soporte de campo.", "$20,000 MXN"],
        ["INVERSIÓN INICIAL TOTAL REQUERIDA", "Capital semilla solicitado para financiar el desarrollo, piloto y validación", "$140,000 MXN"]
    ]
    
    for r_idx, row in enumerate(cp_data):
        for c_idx, val in enumerate(row):
            cell = t9.cell(r_idx + 1, c_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = HIGHLIGHT_GREEN if r_idx == 6 else WHITE
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.alignment = PP_ALIGN.LEFT if c_idx < 2 else PP_ALIGN.RIGHT
            p.font.name = "Arial"
            p.font.size = Pt(9.5)
            if r_idx == 6 or c_idx == 0:
                p.font.bold = True
                if r_idx == 6:
                    p.font.color.rgb = GREEN_BRAND
                
    add_notes(s9, "TIEMPO: 6:45 - 7:45 (60 segundos)\n"
                  "GUIÓN: Solicito una inversión semilla de $140,000 pesos, presupuestada con estricto sentido de austeridad. El monto desglosa $60,000 en desarrollo y pruebas del MVP, $16,000 en servidores para el primer año, $20,000 en lectores ópticos de uso rudo para los mostradores de CUTonalá, $12,000 en marco de privacidad y normatividad, $12,000 en señalética y viáticos locales, y un fondo de contingencia de $20,000 pesos para respaldar el arranque.")

    # =========================================================================
    # DIAPOSITIVA 10: ESTADO DE RESULTADOS PROFORMA (7:45 - 8:45)
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_background(s10, LIGHT_BG)
    add_content_header(s10, "Estado de Resultados Proforma Trienal (Cifras en Pesos MXN)")
    add_content_footer(s10, 10)
    
    rows, cols = 10, 4
    table_shape10 = s10.shapes.add_table(rows, cols, Inches(0.60), Inches(1.50), Inches(12.10), Inches(4.50))
    t10 = table_shape10.table
    
    headers_pn = ["Rubro Contable", "Año 1 (Piloto CUTonalá)", "Año 2 (Versión Pulida CUT+CUCEI)", "Año 3 (Consolidación ZMG)"]
    format_table_headers(t10, headers_pn)
    
    pn_data = [
        ["Ingresos Totales por Servicio / Convenio", "$48,000", "$216,000", "$500,000"],
        ["Costo de Servidores y Nube GCP (Directo)", "($14,000)", "($20,000)", "($32,000)"],
        ["Utilidad Bruta", "$34,000", "$196,000", "$468,000"],
        ["Gastos de Soporte Técnico y Depuración", "($38,000)", "($76,000)", "($130,000)"],
        ["Gastos de Vinculación y Traslados Locales", "($8,000)", "($18,000)", "($30,000)"],
        ["Servicios Contables y Asesoría Legal (SAT/INDAUTOR)", "($10,000)", "($14,000)", "($22,000)"],
        ["Utilidad de Operación (EBITDA)", "($22,000)", "$88,000", "$286,000"],
        ["Impuestos Proyectados (ISR 30% con Amortización)", "$0", "($20,000)", "($86,000)"],
        ["UTILIDAD NETA DEL EJERCICIO (FEN)", "($22,000)", "$68,000", "$200,000"]
    ]
    
    for r_idx, row in enumerate(pn_data):
        for c_idx, val in enumerate(row):
            cell = t10.cell(r_idx + 1, c_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = HIGHLIGHT_GREEN if r_idx in (2, 6, 8) else WHITE
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.alignment = PP_ALIGN.LEFT if c_idx == 0 else PP_ALIGN.RIGHT
            p.font.name = "Arial"
            p.font.size = Pt(9.5)
            if r_idx in (0, 2, 6, 8) or c_idx == 0:
                p.font.bold = True
                if r_idx == 8:
                    p.font.color.rgb = GREEN_BRAND
                
    add_notes(s10, "TIEMPO: 7:45 - 8:45 (60 segundos)\n"
                   "GUIÓN: En el Estado de Resultados Proforma observamos claramente las tres fases del proyecto: un Año 1 de pruebas piloto en CUTonalá con una pérdida operativa calculada de $22,000 pesos absorbida por el capital semilla; un Año 2 donde la versión pulida optimiza los costos de nube y formaliza CUTonalá y CUCEI, generando $68,000 pesos de utilidad neta; y un Año 3 de consolidación regional con $200,000 pesos netos. El punto de equilibrio operativo se alcanza en el mes 15.")

    # =========================================================================
    # DIAPOSITIVA 11: EVALUACIÓN FINANCIERA (TIR, VPN, PAYBACK EXACTO) (8:45 - 9:30)
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    set_slide_background(s11, LIGHT_BG)
    add_content_header(s11, "Tabla Ilustrativa de Evaluación Financiera: VPN, TIR y Payback")
    add_content_footer(s11, 11)
    
    rows, cols = 8, 4
    table_shape11 = s11.shapes.add_table(rows, cols, Inches(0.60), Inches(1.40), Inches(12.10), Inches(4.50))
    t11 = table_shape11.table
    
    headers_f = ["Periodo / Indicador Financiero", "Flujo de Efectivo Neto (FEN)", "Factor Descuento (TMAR 15%)", "Valor Presente del Flujo (VP)"]
    format_table_headers(t11, headers_f)
    
    # Exactitud matemática: I0 = -140k, FEN1 = -22k, FEN2 = +68k, FEN3 = +200k -> VPN = +23,790.58, TIR = 21.34%, Payback = Mes 29.6 (~Mes 30)
    f_data = [
        ["Año 0 (Inversión Inicial CAPEX)", "($140,000.00 MXN)", "1.0000", "($140,000.00 MXN)"],
        ["Año 1 (Fase Piloto CUTonalá)", "($22,000.00 MXN)", "0.8696", "($19,130.43 MXN)"],
        ["Año 2 (Versión Pulida CUT+CUCEI)", "$68,000.00 MXN", "0.7561", "$51,417.77 MXN"],
        ["Año 3 (Consolidación ZMG: 4 planteles)", "$200,000.00 MXN", "0.6575", "$131,503.24 MXN"],
        ["VALOR PRESENTE NETO (VPN)", "Suma algebraica VP", "TMAR = 15.0% anual", "+$23,790.58 MXN"],
        ["TASA INTERNA DE RETORNO (TIR)", "Tasa donde VPN = 0", "Margen vs TMAR: +6.34%", "21.34% anual"],
        ["PERIODO DE RECUPERACIÓN (Payback)", "Saldo acumulado simple", "Payback Descontado: M34", "Mes 29.6 (~Mes 30)"]
    ]
    
    for r_idx, row in enumerate(f_data):
        for c_idx, val in enumerate(row):
            cell = t11.cell(r_idx + 1, c_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = HIGHLIGHT_GREEN if r_idx in (4, 5, 6) else WHITE
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.alignment = PP_ALIGN.LEFT if c_idx < 2 else PP_ALIGN.RIGHT
            p.font.name = "Arial"
            p.font.size = Pt(9.5)
            if r_idx in (4, 5, 6) or c_idx == 0:
                p.font.bold = True
                if r_idx in (4, 5, 6):
                    p.font.color.rgb = GREEN_BRAND
                    
    box_f11 = s11.shapes.add_textbox(Inches(0.60), Inches(6.00), Inches(12.10), Inches(0.70))
    tf_f11 = box_f11.text_frame
    pf11 = tf_f11.paragraphs[0]
    pf11.text = "Interpolación: Payback Simple = Mes 29.6 (Año 3, M6)  |  Payback Descontado = Mes 34 (Año 3, M10)  |  B/C = 1.15x (VP Flujos Positivos / Inversión Acumulada)"
    pf11.font.name = "Arial"
    pf11.font.size = Pt(9.5)
    pf11.font.bold = True
    pf11.font.color.rgb = NAVY_DARK

    add_notes(s11, "TIEMPO: 8:45 - 9:30 (45 segundos)\n"
                   "GUIÓN: Aquí presento la evaluación financiera formal con los números ajustados. Descontando los flujos a una TMAR del 15% anual (Cetes 10.5% + 4.5% prima de riesgo), el Valor Presente Neto es positivo con +$23,790.58 pesos y la TIR alcanza el 21.34% anual, superando ampliamente la tasa exigida. El Payback simple se alcanza en el Mes 29.6 —a mediados del tercer año, recuperando los $94,000 pesos faltantes en 5.6 meses— y el Payback descontado en el Mes 34. La relación Beneficio/Costo es de 1.15x. El proyecto es financieramente viable bajo supuestos reales y alcanzables.")

    # =========================================================================
    # DIAPOSITIVA 12: CONCLUSIONES, OFERTA E REFERENCIAS APA (9:30 - 10:00)
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    set_slide_background(s12, LIGHT_BG)
    add_content_header(s12, "Conclusiones, Propuesta para el Inversionista y Referencias APA")
    add_content_footer(s12, 12)
    
    card_inv = s12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.60), Inches(1.50), Inches(5.80), Inches(5.20))
    card_inv.fill.solid()
    card_inv.fill.fore_color.rgb = NAVY_DARK
    card_inv.line.color.rgb = GREEN_BRAND
    card_inv.line.width = Pt(2)
    
    tfi = card_inv.text_frame
    tfi.word_wrap = True
    pti = tfi.paragraphs[0]
    pti.text = "Propuesta Formal para el Inversionista"
    pti.font.name = "Arial"
    pti.font.bold = True
    pti.font.size = Pt(13)
    pti.font.color.rgb = RGBColor(150, 205, 255)
    pti.space_after = Pt(8)
    
    pdi = tfi.add_paragraph()
    pdi.text = ("• Inversión Requerida: $140,000 MXN en Capital Semilla.\n\n"
                "• Participación: 15% en las utilidades netas del proyecto.\n\n"
                "• Retorno de Capital: Inicio de pago de dividendos en el Mes 20; amortización total del capital en el Mes 30 (Payback simple).\n\n"
                "• Rendimiento Recurrente: Dividendo estimado de $30,000+ MXN anuales sostenibles a partir del Año 3 con solo 4 planteles consolidados.")
    pdi.font.name = "Arial"
    pdi.font.size = Pt(10)
    pdi.font.color.rgb = WHITE
    
    card_ref = s12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.70), Inches(1.50), Inches(6.00), Inches(5.20))
    card_ref.fill.solid()
    card_ref.fill.fore_color.rgb = WHITE
    card_ref.line.color.rgb = BORDER_COLOR
    
    tfr = card_ref.text_frame
    tfr.word_wrap = True
    ptr = tfr.paragraphs[0]
    ptr.text = "Referencias Bibliográficas (APA 7ma Edición)"
    ptr.font.name = "Arial"
    ptr.font.bold = True
    ptr.font.size = Pt(12)
    ptr.font.color.rgb = NAVY_DARK
    ptr.space_after = Pt(6)
    
    refs = [
        "Aldunate, E. y Córdoba, J. (2011). Formulación de programas con la metodología de marco lógico (Serie Manuales N° 68). CEPAL/ILPES.",
        "ANUIES. (2023). Anuario estadístico de la educación superior 2022-2023. https://anuies.mx/anuarios-estadisticos",
        "Baca Urbina, G. (2013). Evaluación de proyectos (7ma ed.). McGraw-Hill.",
        "Cámara de Diputados. (2017). Ley General de Protección de Datos Personales en Posesión de Sujetos Obligados. DOF 26/01/2017.",
        "CGPE. (2024). Numeralia institucional de la Red Universitaria. UdeG. https://cgpe.udg.mx/numeralia-institucional",
        "Ortegón, E., Pacheco, J. F. y Prieto, A. (2005). Metodología del marco lógico (Serie Manuales N° 42). CEPAL/ILPES.",
        "Universidad de Guadalajara. (2019). Plan de Desarrollo Institucional 2019-2025, Visión 2030. https://www.udg.mx/es/pdi",
        "Universidad de Guadalajara. (2022). Reglamento de Adquisiciones, Arrendamientos y Contratación de Servicios."
    ]
    
    for r in refs:
        p = tfr.add_paragraph()
        p.text = f"• {r}"
        p.font.name = "Arial"
        p.font.size = Pt(9.5)
        p.font.color.rgb = DARK_TEXT
        p.space_after = Pt(3)
        
    add_notes(s12, "TIEMPO: 9:30 - 10:00 (30 segundos)\n"
                   "GUIÓN: En conclusión, SIGRE es una propuesta de inversión de bajo riesgo, alta viabilidad técnica y un impacto social directo en la Universidad de Guadalajara. No dependo de proyecciones fantasiosas: con solo 4 planteles en tres años logro el retorno completo del capital en el mes 30 y un flujo atractivo y sostenido de utilidades. Agradezco su atención y quedo abierto a sus preguntas.")

    # Guardar la nueva presentación rediseñada y ajustada
    out_dir = r"C:\Users\hatue\Downloads\Inversion\docs"
    os.makedirs(out_dir, exist_ok=True)
    out_pptx = os.path.join(out_dir, "Segunda_Presentacion_Inversion_Retorno_SIGRE.pptx")
    prs.save(out_pptx)
    print(f"PRESENTACIÓN CORREGIDA Y REDISEÑADA GENERADA EN: {out_pptx}")

if __name__ == "__main__":
    create_redesigned_presentation()
