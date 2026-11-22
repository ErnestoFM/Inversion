import sys
import os
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def build_presentation():
    prs = pptx.Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Paleta de Colores SIGRE
    C_BG = RGBColor(13, 27, 42)          # #0D1B2A Deep Navy Base
    C_CARD = RGBColor(26, 26, 46)        # #1A1A2E Surface Card
    C_CARD_ELEV = RGBColor(30, 41, 59)   # #1E293B Elevated Surface
    C_BORDER = RGBColor(51, 65, 85)      # #334155 Sutil Border
    C_NAVY_UDEG = RGBColor(0, 43, 73)    # #002B49 Institutional UdeG Navy
    C_GREEN = RGBColor(46, 125, 87)      # #2E7D57 Natural Forest Green
    C_GREEN_LIGHT = RGBColor(74, 222, 128) # #4ADE80 Bright Green
    C_CYAN = RGBColor(56, 189, 248)      # #38BDF8 Bright Cyan
    C_AMBER = RGBColor(217, 119, 6)      # #D97706 Warm Gold / Amber
    C_AMBER_LIGHT = RGBColor(251, 191, 36) # #FBBF24 Light Amber
    C_RED = RGBColor(239, 68, 68)        # #EF4444 Error / Red
    C_TEXT_WHITE = RGBColor(248, 250, 252) # #F8FAFC Heading text
    C_TEXT_MUTED = RGBColor(148, 163, 184) # #94A3B8 Secondary text

    FONT_TITLE = 'Segoe UI'
    FONT_BODY = 'Segoe UI'

    def create_base_slide(category, title, subtitle, slide_num, total_slides=13):
        slide = prs.slides.add_slide(blank_layout)
        
        # Background
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = C_BG
        bg.line.fill.background()
        
        # Header Accent line at very top
        top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(0.08))
        top_bar.fill.solid()
        top_bar.fill.fore_color.rgb = C_CYAN
        top_bar.line.fill.background()

        # Category Tag / Badge
        if category:
            cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.28), Inches(10), Inches(0.35))
            tf_cat = cat_box.text_frame
            tf_cat.word_wrap = True
            tf_cat.margin_left = tf_cat.margin_top = tf_cat.margin_right = tf_cat.margin_bottom = 0
            p_cat = tf_cat.paragraphs[0]
            p_cat.text = category.upper()
            p_cat.font.name = FONT_TITLE
            p_cat.font.size = Pt(11)
            p_cat.font.bold = True
            p_cat.font.color.rgb = C_CYAN

        # Main Slide Title
        if title:
            title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.60), Inches(11), Inches(0.55))
            tf_title = title_box.text_frame
            tf_title.word_wrap = True
            tf_title.margin_left = tf_title.margin_top = tf_title.margin_right = tf_title.margin_bottom = 0
            p_title = tf_title.paragraphs[0]
            p_title.text = title
            p_title.font.name = FONT_TITLE
            p_title.font.size = Pt(22)
            p_title.font.bold = True
            p_title.font.color.rgb = C_TEXT_WHITE

        # Subtitle
        if subtitle:
            sub_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.15), Inches(11.5), Inches(0.40))
            tf_sub = sub_box.text_frame
            tf_sub.word_wrap = True
            tf_sub.margin_left = tf_sub.margin_top = tf_sub.margin_right = tf_sub.margin_bottom = 0
            p_sub = tf_sub.paragraphs[0]
            p_sub.text = subtitle
            p_sub.font.name = FONT_BODY
            p_sub.font.size = Pt(12)
            p_sub.font.color.rgb = C_TEXT_MUTED

        # Top Right Logo (Small)
        if os.path.exists('docs/brand/udeg_logo.png') and slide_num > 1:
            slide.shapes.add_picture('docs/brand/udeg_logo.png', Inches(12.1), Inches(0.35), height=Inches(0.75))

        # Footer
        if slide_num > 1:
            # Divider line
            div = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(6.85), Inches(11.733), Inches(0.02))
            div.fill.solid()
            div.fill.fore_color.rgb = C_BORDER
            div.line.fill.background()

            # Footer Left
            f_left = slide.shapes.add_textbox(Inches(0.8), Inches(6.95), Inches(5.0), Inches(0.35))
            tf_fl = f_left.text_frame
            tf_fl.margin_left = tf_fl.margin_top = tf_fl.margin_right = tf_fl.margin_bottom = 0
            p_fl = tf_fl.paragraphs[0]
            p_fl.text = "Ernesto Hatuey Fierro M. (223977036) • Equipo 4"
            p_fl.font.name = FONT_BODY
            p_fl.font.size = Pt(10)
            p_fl.font.color.rgb = C_TEXT_MUTED

            # Footer Center
            f_center = slide.shapes.add_textbox(Inches(5.0), Inches(6.95), Inches(4.5), Inches(0.35))
            tf_fc = f_center.text_frame
            tf_fc.margin_left = tf_fc.margin_top = tf_fc.margin_right = tf_fc.margin_bottom = 0
            p_fc = tf_fc.paragraphs[0]
            p_fc.alignment = PP_ALIGN.CENTER
            p_fc.text = "Docente: Dra. Abril Adriana Angulo Sherman"
            p_fc.font.name = FONT_BODY
            p_fc.font.size = Pt(10)
            p_fc.font.color.rgb = C_TEXT_MUTED

            # Footer Right
            f_right = slide.shapes.add_textbox(Inches(9.5), Inches(6.95), Inches(3.033), Inches(0.35))
            tf_fr = f_right.text_frame
            tf_fr.margin_left = tf_fr.margin_top = tf_fr.margin_right = tf_fr.margin_bottom = 0
            p_fr = tf_fr.paragraphs[0]
            p_fr.alignment = PP_ALIGN.RIGHT
            p_fr.text = f"EXPODIT 2026 • Slide {slide_num} / {total_slides}"
            p_fr.font.name = FONT_BODY
            p_fr.font.size = Pt(10)
            p_fr.font.bold = True
            p_fr.font.color.rgb = C_TEXT_MUTED

        return slide

    def add_notes(slide, timing, goal, literal_text, cues):
        notes = slide.notes_slide.notes_text_frame
        notes.text = f"⏱ TIEMPO: {timing}\n🎯 OBJETIVO: {goal}\n\n📢 GUION LITERAL:\n\"{literal_text}\"\n\n💡 CUES Y RECOMENDACIONES:\n{cues}"

    # ==========================================
    # SLIDE 1: PORTADA
    # ==========================================
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = C_BG
    bg1.line.fill.background()

    # Accent Top Line
    top_bar1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(0.1))
    top_bar1.fill.solid()
    top_bar1.fill.fore_color.rgb = C_CYAN
    top_bar1.line.fill.background()

    # Logos
    if os.path.exists('docs/brand/udeg_logo.png'):
        s1.shapes.add_picture('docs/brand/udeg_logo.png', Inches(0.8), Inches(0.6), height=Inches(1.2))
    if os.path.exists('docs/brand/sigre_logo_header.png'):
        s1.shapes.add_picture('docs/brand/sigre_logo_header.png', Inches(8.5), Inches(0.6), height=Inches(1.1))

    # Event Badge
    badge1 = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(2.1), Inches(7.5), Inches(0.42))
    badge1.fill.solid()
    badge1.fill.fore_color.rgb = C_NAVY_UDEG
    badge1.line.color.rgb = C_CYAN
    badge1.line.width = Pt(1)
    tf_b1 = badge1.text_frame
    tf_b1.vertical_anchor = MSO_ANCHOR.MIDDLE
    p_b1 = tf_b1.paragraphs[0]
    p_b1.text = "  EXPODIT 2026 • PROYECTO INTEGRADOR DE DESARROLLO DE SOFTWARE  "
    p_b1.font.name = FONT_TITLE
    p_b1.font.size = Pt(11)
    p_b1.font.bold = True
    p_b1.font.color.rgb = C_CYAN

    # Main Title
    t_box1 = s1.shapes.add_textbox(Inches(0.8), Inches(2.65), Inches(11.7), Inches(1.1))
    tf_t1 = t_box1.text_frame
    tf_t1.word_wrap = True
    p_t1 = tf_t1.paragraphs[0]
    p_t1.text = "PLATAFORMA SIGRE"
    p_t1.font.name = FONT_TITLE
    p_t1.font.size = Pt(44)
    p_t1.font.bold = True
    p_t1.font.color.rgb = C_TEXT_WHITE

    # Subtitle
    s_box1 = s1.shapes.add_textbox(Inches(0.8), Inches(3.75), Inches(11.7), Inches(1.0))
    tf_s1 = s_box1.text_frame
    tf_s1.word_wrap = True
    p_s1 = tf_s1.paragraphs[0]
    p_s1.text = "Sistema Integrado de Gestión de Recursos y Espacios: Control Patrimonial, Prevención de Colisiones de Agenda y Trazabilidad de Infraestructura Universitaria"
    p_s1.font.name = FONT_BODY
    p_s1.font.size = Pt(16)
    p_s1.font.color.rgb = C_CYAN

    # 4 Bottom Cards
    cards_data = [
        ("ESTUDIANTE / AUTOR", "Ernesto Hatuey Fierro M.", "Código: 223977036 • Equipo 4"),
        ("DOCENTE TITULAR", "Dra. Abril Sherman", "Evaluación ExpoDIT 2026"),
        ("CENTRO UNIVERSITARIO", "CUTonalá (DIIT)", "Ing. en Ciencias Computacionales"),
        ("COMPROMISO ONU 2030", "ODS 4, 9, 11, 12 y 16", "Campus Inteligente y Cero Papel")
    ]
    card_w = Inches(2.75)
    card_gap = Inches(0.24)
    card_h = Inches(1.5)
    card_top = Inches(5.1)

    for i, (label, val1, val2) in enumerate(cards_data):
        c_left = Inches(0.8) + i * (card_w + card_gap)
        card_box = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, c_left, card_top, card_w, card_h)
        card_box.fill.solid()
        card_box.fill.fore_color.rgb = C_CARD
        card_box.line.color.rgb = C_BORDER
        card_box.line.width = Pt(1)

        # Content
        tf_c = card_box.text_frame
        tf_c.word_wrap = True
        tf_c.margin_left = Inches(0.2)
        tf_c.margin_top = Inches(0.2)
        tf_c.margin_right = Inches(0.2)

        p1 = tf_c.paragraphs[0]
        p1.text = label
        p1.font.name = FONT_TITLE
        p1.font.size = Pt(9.5)
        p1.font.bold = True
        p1.font.color.rgb = C_AMBER_LIGHT

        p2 = tf_c.add_paragraph()
        p2.text = val1
        p2.font.name = FONT_TITLE
        p2.font.size = Pt(12)
        p2.font.bold = True
        p2.font.color.rgb = C_TEXT_WHITE
        p2.space_before = Pt(4)

        p3 = tf_c.add_paragraph()
        p3.text = val2
        p3.font.name = FONT_BODY
        p3.font.size = Pt(10)
        p3.font.color.rgb = C_TEXT_MUTED
        p3.space_before = Pt(2)

    add_notes(s1, "00:00 - 00:18 (18 seg)", "Apertura formal institucional y presentación de identidad",
              "Buenos días, Dra. Abril Sherman y miembros del jurado evaluador. Mi nombre es Ernesto Hatuey Fierro, estudiante de Ingeniería en Ciencias Computacionales en CUTonalá. Hoy presento la Plataforma SIGRE: Sistema Integrado de Gestión de Recursos y Espacios, una solución de software orientada a erradicar colisiones de agenda y proteger el patrimonio universitario.",
              "Postura erguida, contacto visual sostenido, proyectar voz firme y pausada. Clic a Slide 2 al segundo 18.")

    # ==========================================
    # SLIDE 2: DIAGNÓSTICO & CONTEXTO OPERATIVO
    # ==========================================
    s2 = create_base_slide(
        "Diagnóstico & Contexto Operativo",
        "Problemática en la Gestión de Espacios y Activos Universitarios",
        "Brechas patrimoniales, logísticas y ecológicas detectadas en el modelo analógico tradicional",
        2
    )
    col_w = Inches(3.68)
    col_gap = Inches(0.34)
    col_h = Inches(5.0)
    col_top = Inches(1.68)

    cards_diag = [
        {
            "icon": "📉",
            "title": "Merma Patrimonial No Deslindada",
            "desc": "El registro manual en libretas diluye la cadena de custodia cuando se devuelven cables o proyectores averiados sin checklist bilateral.",
            "badge": "Impacto: Pérdida $90k – $140k/año",
            "badge_color": C_RED,
            "bullets": [
                ("Firmas Ilegibles:", "Vales en papel sin checklist formal bilateral de entrega y recepción."),
                ("Extravío Continuo:", "15 a 30 accesorios menores (HDMI/USB-C) perdidos al año por campus."),
                ("Fricción en Ventanilla:", "Imposibilidad de deslindar responsabilidad entre alumno y laboratorista.")
            ]
        },
        {
            "icon": "⏰",
            "title": "Colisiones de Agenda y Empalmes",
            "desc": "La tramitación mediante oficios y correos aislados genera traslapes concurrentes y salas cerradas sin llave disponible.",
            "badge": "Impacto: 15 a 25 min de clase perdidos",
            "badge_color": C_AMBER,
            "bullets": [
                ("Burocracia de 5 Días:", "Trámites lentos que desembocan en 'acuerdos verbales de palabra'."),
                ("Doble Agendamiento:", "Dos docentes asignados al mismo auditorio al mismo tiempo."),
                ("Parálisis Pedagógica:", "Pérdida recurrente de tiempo lectivo por falta de llave o equipo.")
            ]
        },
        {
            "icon": "📄",
            "title": "Ceguera Directiva y Desperdicio",
            "desc": "La administración carece de telemetría de uso real, programando compras por urgencia y acumulando miles de papeles muertos.",
            "badge": "Meta: Ahorro de >12,000 actas/año",
            "badge_color": C_GREEN,
            "bullets": [
                ("Despacho Lento:", "Tiempos de 4.5 a 6.0 minutos por persona en mostrador en horas pico."),
                ("Cero Analítica:", "Desconocimiento del ciclo de vida y horas de uso de activos."),
                ("Huella Papelera:", "Consumo masivo de tóner y hojas que terminan en archivo muerto.")
            ]
        }
    ]

    for i, c in enumerate(cards_diag):
        c_left = Inches(0.8) + i * (col_w + col_gap)
        card_box = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, c_left, col_top, col_w, col_h)
        card_box.fill.solid()
        card_box.fill.fore_color.rgb = C_CARD
        card_box.line.color.rgb = C_BORDER
        card_box.line.width = Pt(1)

        tf = card_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = Inches(0.22)

        # Header icon + title
        p_hdr = tf.paragraphs[0]
        p_hdr.text = f"{c['icon']} {c['title']}"
        p_hdr.font.name = FONT_TITLE
        p_hdr.font.size = Pt(14)
        p_hdr.font.bold = True
        p_hdr.font.color.rgb = C_TEXT_WHITE

        # Description
        p_desc = tf.add_paragraph()
        p_desc.text = c['desc']
        p_desc.font.name = FONT_BODY
        p_desc.font.size = Pt(10.5)
        p_desc.font.color.rgb = C_TEXT_MUTED
        p_desc.space_before = Pt(6)

        # Badge
        p_bdg = tf.add_paragraph()
        p_bdg.text = f"▶ {c['badge']}"
        p_bdg.font.name = FONT_TITLE
        p_bdg.font.size = Pt(10.5)
        p_bdg.font.bold = True
        p_bdg.font.color.rgb = c['badge_color']
        p_bdg.space_before = Pt(8)

        # Bullets
        for b_title, b_text in c['bullets']:
            p_b = tf.add_paragraph()
            p_b.text = f"• {b_title} {b_text}"
            p_b.font.name = FONT_BODY
            p_b.font.size = Pt(10)
            p_b.font.color.rgb = C_TEXT_MUTED
            p_b.space_before = Pt(8)

    add_notes(s2, "00:18 - 00:38 (20 seg)", "Demostrar dolor operativo, costo de inacción y empatía",
              "En los almacenes del campus detectamos tres puntos críticos del registro en libretas: mermas no deslindadas de hasta 140,000 pesos anuales en accesorios y proyectores; colisiones de agenda que demoran hasta 25 minutos de clase lectiva; y ceguera directiva por falta de métricas sobre el uso del inventario.",
              "Enfatizar con tono grave las cifras clave ($140k anuales, 25 minutos). Señalar con la mirada las tres tarjetas.")

    # ==========================================
    # SLIDE 3: ALINEACIÓN ESTRATÉGICA ONU 2030
    # ==========================================
    s3 = create_base_slide(
        "Alineación Estratégica ONU 2030",
        "Justificación e Impacto en los Objetivos de Desarrollo Sostenible",
        "SIGRE como catalizador de transformación digital, transparencia patrimonial y sostenibilidad universitaria",
        3
    )

    # Left Column (ODS Cards)
    left_w = Inches(5.7)
    left_top = Inches(1.68)
    ods_data = [
        ("🎓 ODS 4: Educación de Calidad", "Garantiza instalaciones académicas y recintos especializados equipados y disponibles al 100%, eliminando la pérdida de tiempo pedagógico por falta de proyectores o aulas cerradas.", C_CYAN),
        ("☁ ODS 9 & 16: Innovación, Infraestructura y Paz", "Arquitectura cloud serverless elástica en GCP, cerrojos atómicos en Redis y auditoría criptográfica HMAC-SHA256 para total transparencia institucional.", C_AMBER_LIGHT),
        ("🌿 ODS 11 & 12: Comunidades Sostenibles y Cero Papel", "Digitalización del 100% de actas responsivas en PDF oficial con firma digital, sustituyendo más de 12,000 formatos impresos al año por plantel.", C_GREEN_LIGHT)
    ]

    for i, (ods_title, ods_desc, ods_color) in enumerate(ods_data):
        y_pos = left_top + i * Inches(1.65)
        card_ods = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), y_pos, left_w, Inches(1.52))
        card_ods.fill.solid()
        card_ods.fill.fore_color.rgb = C_CARD
        card_ods.line.color.rgb = ods_color
        card_ods.line.width = Pt(1)

        tf_o = card_ods.text_frame
        tf_o.word_wrap = True
        tf_o.margin_left = tf_o.margin_right = tf_o.margin_top = Inches(0.18)

        po1 = tf_o.paragraphs[0]
        po1.text = ods_title
        po1.font.name = FONT_TITLE
        po1.font.size = Pt(13)
        po1.font.bold = True
        po1.font.color.rgb = ods_color

        po2 = tf_o.add_paragraph()
        po2.text = ods_desc
        po2.font.name = FONT_BODY
        po2.font.size = Pt(10.5)
        po2.font.color.rgb = C_TEXT_MUTED
        po2.space_before = Pt(4)

    # Right Column (Figure 1: Matriz de Servicio y Sostenibilidad)
    right_left = Inches(6.8)
    right_w = Inches(5.733)
    right_h = Inches(4.75)
    r_card = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, right_left, left_top, right_w, right_h)
    r_card.fill.solid()
    r_card.fill.fore_color.rgb = C_CARD
    r_card.line.color.rgb = C_BORDER
    r_card.line.width = Pt(1)

    if os.path.exists('docs/graficos/figura1_diagrama_servicio_sigre.png'):
        s3.shapes.add_picture('docs/graficos/figura1_diagrama_servicio_sigre.png', right_left + Inches(0.2), left_top + Inches(0.2), width=right_w - Inches(0.4), height=Inches(4.0))

    cap_box = s3.shapes.add_textbox(right_left + Inches(0.2), left_top + Inches(4.25), right_w - Inches(0.4), Inches(0.4))
    tf_cap = cap_box.text_frame
    tf_cap.word_wrap = True
    p_cap = tf_cap.paragraphs[0]
    p_cap.alignment = PP_ALIGN.CENTER
    p_cap.text = "Figura 1: Matriz de Servicio, Trazabilidad y Sostenibilidad SIGRE (Agenda 2030)"
    p_cap.font.name = FONT_BODY
    p_cap.font.size = Pt(10)
    p_cap.font.color.rgb = C_TEXT_MUTED

    add_notes(s3, "00:38 - 00:58 (20 seg)", "Vincular el software con política universitaria y ODS",
              "SIGRE se alinea a la Agenda 2030 de la ONU: fortalece el ODS 4 garantizando aulas equipadas; cumple los ODS 9 y 16 con arquitectura en la nube y auditoría criptográfica; y avanza en los ODS 11 y 12 digitalizando más de 12,000 actas físicas al año bajo la política Cero Papel.",
              "Voz inspiradora. Destacar la cifra de '12,000 actas físicas ahorradas al año' y apuntar a la gráfica lateral.")

    # ==========================================
    # SLIDE 4: ALCANCE & DIRECTRICES TÉCNICAS
    # ==========================================
    s4 = create_base_slide(
        "Alcance & Directrices Técnicas",
        "Objetivos del Proyecto SIGRE",
        "Metas de desarrollo formal de software para la gestión patrimonial y logística de recintos",
        4
    )

    # General Objective Box (Top)
    top_w = Inches(11.733)
    obj_box = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.68), top_w, Inches(1.35))
    obj_box.fill.solid()
    obj_box.fill.fore_color.rgb = C_CARD
    obj_box.line.color.rgb = C_CYAN
    obj_box.line.width = Pt(1)

    tf_obj = obj_box.text_frame
    tf_obj.word_wrap = True
    tf_obj.margin_left = tf_obj.margin_right = tf_obj.margin_top = Inches(0.2)
    p_o1 = tf_obj.paragraphs[0]
    p_o1.text = "🎯 Objetivo General de Ingeniería"
    p_o1.font.name = FONT_TITLE
    p_o1.font.size = Pt(12)
    p_o1.font.bold = True
    p_o1.font.color.rgb = C_CYAN

    p_o2 = tf_obj.add_paragraph()
    p_o2.text = "Diseñar, construir e implementar una plataforma web distribuida para la administración, reserva y trazabilidad de espacios y bienes móviles en CUTonalá, garantizando transacciones concurrentes libres de empalmes mediante cerrojos en Redis, autenticación federada UdeG, actas responsivas con firma digitalizada HMAC-SHA256 y un ecosistema de reputación Trust Score alineado a la Agenda 2030."
    p_o2.font.name = FONT_BODY
    p_o2.font.size = Pt(10.5)
    p_o2.font.color.rgb = C_TEXT_WHITE
    p_o2.space_before = Pt(3)

    # Middle 4 Quantitative Metrics
    metrics_data = [
        ("< 30 seg", "Tiempo de Despacho", "En ventanilla con escáner QR", C_CYAN),
        ("0", "Empalmes de Agenda", "Con Redis Distributed Lock", C_GREEN_LIGHT),
        ("82.85 pts", "Usabilidad SUS (n=50)", "Grado A Nivel Excelente", C_AMBER_LIGHT),
        ("99.9%", "Disponibilidad Cloud", "En Google Cloud Run (GCP)", C_CYAN)
    ]
    m_w = Inches(2.75)
    m_gap = Inches(0.24)
    m_top = Inches(3.20)
    m_h = Inches(1.35)

    for i, (val, lbl, sub, color) in enumerate(metrics_data):
        m_left = Inches(0.8) + i * (m_w + m_gap)
        m_card = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, m_left, m_top, m_w, m_h)
        m_card.fill.solid()
        m_card.fill.fore_color.rgb = C_CARD_ELEV
        m_card.line.color.rgb = color
        m_card.line.width = Pt(1.5)

        tf_m = m_card.text_frame
        tf_m.word_wrap = True
        tf_m.margin_left = tf_m.margin_right = tf_m.margin_top = Inches(0.15)

        pm1 = tf_m.paragraphs[0]
        pm1.alignment = PP_ALIGN.CENTER
        pm1.text = val
        pm1.font.name = FONT_TITLE
        pm1.font.size = Pt(24)
        pm1.font.bold = True
        pm1.font.color.rgb = color

        pm2 = tf_m.add_paragraph()
        pm2.alignment = PP_ALIGN.CENTER
        pm2.text = lbl
        pm2.font.name = FONT_TITLE
        pm2.font.size = Pt(11)
        pm2.font.bold = True
        pm2.font.color.rgb = C_TEXT_WHITE
        pm2.space_before = Pt(2)

        pm3 = tf_m.add_paragraph()
        pm3.alignment = PP_ALIGN.CENTER
        pm3.text = sub
        pm3.font.name = FONT_BODY
        pm3.font.size = Pt(9.5)
        pm3.font.color.rgb = C_TEXT_MUTED
        pm3.space_before = Pt(2)

    # Bottom Specific Objectives
    bot_card = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(4.75), top_w, Inches(1.95))
    bot_card.fill.solid()
    bot_card.fill.fore_color.rgb = C_CARD
    bot_card.line.color.rgb = C_BORDER
    bot_card.line.width = Pt(1)

    tf_bot = bot_card.text_frame
    tf_bot.word_wrap = True
    tf_bot.margin_left = tf_bot.margin_right = tf_bot.margin_top = Inches(0.2)
    p_b1 = tf_bot.paragraphs[0]
    p_b1.text = "⚙ Objetivos Específicos de Ingeniería de Software"
    p_b1.font.name = FONT_TITLE
    p_b1.font.size = Pt(12)
    p_b1.font.bold = True
    p_b1.font.color.rgb = C_AMBER_LIGHT

    specs = [
        "1. Concurrencia y Aislamiento: Implementar cerrojos temporales con TTL de 900s en Redis 7 para blindar solicitudes.",
        "2. Trazabilidad y Cadena de Custodia: Desarrollar lectura óptica de QR WebRTC y firma en Canvas HTML5 con HMAC-SHA256.",
        "3. Autenticación y RBAC: Restringir acceso institucional exclusivo vía Google OAuth (@udg.mx) con tokens JWT firmados.",
        "4. Telemetría y Reputación: Construir panel ejecutivo con cálculo de Trust Score (base 100) para resguardo patrimonial.",
        "5. Despliegue Elástico y DevOps: Automatizar pipeline CI/CD en GitHub Actions y contenedorización Docker serverless en Cloud Run."
    ]
    for sp in specs:
        p_sp = tf_bot.add_paragraph()
        p_sp.text = sp
        p_sp.font.name = FONT_BODY
        p_sp.font.size = Pt(9.5)
        p_sp.font.color.rgb = C_TEXT_MUTED
        p_sp.space_before = Pt(2.5)

    add_notes(s4, "00:58 - 01:18 (20 seg)", "Presentar métricas cuantitativas de éxito y rigor técnico",
              "Nuestra meta fue construir una plataforma distribuida y transaccional. Fijamos cuatro métricas clave: reducir el despacho en ventanilla a menos de 30 segundos; eliminar al 100% los empalmes con cerrojos atómicos; alcanzar una usabilidad SUS de excelencia con 82.85 puntos; y sostener 99.9% de disponibilidad en Google Cloud.",
              "Voz firme y enérgica al nombrar las 4 tarjetas de números. Dar peso al 82.85 de Usabilidad SUS.")

    # ==========================================
    # SLIDE 5: INNOVACIÓN TECNOLÓGICA & VALOR DIFERENCIAL
    # ==========================================
    s5 = create_base_slide(
        "Innovación Tecnológica & Valor Diferencial",
        "Solución Propuesta: Las Genialidades del Proyecto SIGRE",
        "¿Por qué SIGRE redefine la administración de infraestructura y patrimonio en educación superior?",
        5
    )

    innovations = [
        {
            "icon": "⚡",
            "title": "1. Concurrencia con Redis Locks",
            "desc": "Pre-reserva atómica con SET NX EX 900 (15 min): bloquea temporalmente el espacio mientras el solicitante formaliza datos y co-responsables. Si abandona, el cerrojo expira solo; si confirma, persiste en PostgreSQL sin colisión.",
            "badge": "Garantía: Cero Empalmes",
            "color": C_CYAN,
            "sub": "Aislamiento transaccional estricto probado bajo alta concurrencia."
        },
        {
            "icon": "📱",
            "title": "2. Despacho Óptico QR y Firma",
            "desc": "Lectura de códigos QR dinámicos directamente desde la cámara del navegador web vía WebRTC, sin lectores propietarios. Firma táctil digitalizada sellada en actas PDF inmutables con HMAC-SHA256.",
            "badge": "Agilidad: < 30 Segundos",
            "color": C_GREEN_LIGHT,
            "sub": "Reducción de 5 minutos a 30 segundos por entrega física en mostrador."
        },
        {
            "icon": "🛡",
            "title": "3. Algoritmo Trust Score",
            "desc": "Calificación algorítmica de reputación de usuario (base 100): premia devoluciones a tiempo y penaliza demoras o mermas, bloqueando temporalmente a usuarios con adeudos. Permite adherir co-responsables.",
            "badge": "Protección Patrimonial",
            "color": C_AMBER_LIGHT,
            "sub": "Fomenta la corresponsabilidad estudiantil y previene el abandono de bienes."
        },
        {
            "icon": "☁",
            "title": "4. Serverless Cloud Run",
            "desc": "Backend en contenedores Docker desplegados sobre GCP con escalado elástico de 0 a N instancias. En vacaciones el costo es cero. Además, la PWA incorpora caché local para operar ante caídas de red del campus.",
            "badge": "Escalabilidad Elástica",
            "color": C_CYAN,
            "sub": "Alta disponibilidad 99.9% y sincronización automática al volver el enlace."
        }
    ]

    s5_col_w = Inches(2.75)
    s5_col_gap = Inches(0.24)
    s5_top = Inches(1.68)
    s5_h = Inches(5.0)

    for i, inn in enumerate(innovations):
        s5_left = Inches(0.8) + i * (s5_col_w + s5_col_gap)
        c_box = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, s5_left, s5_top, s5_col_w, s5_h)
        c_box.fill.solid()
        c_box.fill.fore_color.rgb = C_CARD
        c_box.line.color.rgb = inn['color']
        c_box.line.width = Pt(1)

        tf_in = c_box.text_frame
        tf_in.word_wrap = True
        tf_in.margin_left = tf_in.margin_right = tf_in.margin_top = Inches(0.18)

        pin1 = tf_in.paragraphs[0]
        pin1.text = f"{inn['icon']} {inn['title']}"
        pin1.font.name = FONT_TITLE
        pin1.font.size = Pt(12.5)
        pin1.font.bold = True
        pin1.font.color.rgb = inn['color']

        pin2 = tf_in.add_paragraph()
        pin2.text = inn['desc']
        pin2.font.name = FONT_BODY
        pin2.font.size = Pt(9.5)
        pin2.font.color.rgb = C_TEXT_MUTED
        pin2.space_before = Pt(8)

        pin3 = tf_in.add_paragraph()
        pin3.text = f"▶ {inn['badge']}"
        pin3.font.name = FONT_TITLE
        pin3.font.size = Pt(10)
        pin3.font.bold = True
        pin3.font.color.rgb = C_TEXT_WHITE
        pin3.space_before = Pt(14)

        pin4 = tf_in.add_paragraph()
        pin4.text = inn['sub']
        pin4.font.name = FONT_BODY
        pin4.font.size = Pt(9)
        pin4.font.color.rgb = C_TEXT_MUTED
        pin4.space_before = Pt(4)

    add_notes(s5, "01:18 - 01:40 (22 seg)", "Destacar diferenciadores técnicos y genialidades de ingeniería",
              "SIGRE aporta cuatro ventajas de ingeniería: cerrojos distribuidos en Redis con TTL de 15 minutos que bloquean empalmes concurrentes; despacho ágil con QR dinámico y firma en canvas; un algoritmo Trust Score que incentiva devoluciones puntuales; y contenedores serverless en Cloud Run que escalan a costo cero.",
              "Enfatizar la frase 'hace matemáticamente imposible el doble agendamiento'. Tono de alta seguridad técnica.")

    # ==========================================
    # SLIDE 6: DISEÑO DE INGENIERÍA DE SOFTWARE
    # ==========================================
    s6 = create_base_slide(
        "Diseño de Ingeniería de Software",
        "Arquitectura y Diagrama del Sistema SIGRE",
        "Estructura desacoplada en 5 capas de software en Monorepo Turborepo con cerrojos distribuidos",
        6
    )

    # Left: Diagram Image
    s6_left_w = Inches(5.7)
    s6_card_h = Inches(4.9)
    s6_top = Inches(1.68)
    d_card = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), s6_top, s6_left_w, s6_card_h)
    d_card.fill.solid()
    d_card.fill.fore_color.rgb = C_CARD
    d_card.line.color.rgb = C_BORDER

    if os.path.exists('docs/graficos/figura2_diagrama_arquitectura_5capas_sigre.png'):
        s6.shapes.add_picture('docs/graficos/figura2_diagrama_arquitectura_5capas_sigre.png', Inches(0.95), s6_top + Inches(0.15), width=s6_left_w - Inches(0.3), height=Inches(4.2))

    cap6 = s6.shapes.add_textbox(Inches(0.95), s6_top + Inches(4.45), s6_left_w - Inches(0.3), Inches(0.35))
    tf_c6 = cap6.text_frame
    tf_c6.word_wrap = True
    p_c6 = tf_c6.paragraphs[0]
    p_c6.alignment = PP_ALIGN.CENTER
    p_c6.text = "Figura 2: Diagrama de 5 Capas de Software SIGRE (Monorepo Turborepo)"
    p_c6.font.name = FONT_BODY
    p_c6.font.size = Pt(10)
    p_c6.font.color.rgb = C_TEXT_MUTED

    # Right: Layers Breakdown
    layers_text = [
        ("Capa 1: Interfaz Reactiva (React 18 / Vite)", "PWA responsiva para tablets de ventanilla y smartphones. 18 vistas modulares organizadas por rol, diseño UdeG Outfit y firma táctil en Canvas.", C_CYAN),
        ("Capa 2: API Gateway & Core (Express / TypeScript)", "Rutas REST modulares (/api/v1), middleware JWT con roles RBAC (Alumno, Docente, Almacén, SuperAdmin), validación estricta Zod y sanitización OWASP.", C_GREEN_LIGHT),
        ("Capa 3: Bus de Concurrencia (Redis 7 Locks)", "Cerrojos atómicos SET NX EX 900 (TTL 15 min) para bloqueo de slots de agenda, blacklist de tokens revocados y caché de catálogos en memoria.", C_AMBER_LIGHT),
        ("Capa 4: Persistencia Relacional (PostgreSQL 16)", "Esquema relacional ACID con Prisma ORM y tipos tsrange para exclusión estricta de solapamientos temporales en reservas y activos.", C_CYAN),
        ("Capa 5: Infraestructura Cloud (Google Cloud Run)", "Contenedores Docker serverless con escalado elástico a cero en GCP, integración con Google Identity OAuth 2.0 y servidor SMTP transaccional.", C_GREEN_LIGHT)
    ]

    s6_r_left = Inches(6.833)
    s6_r_w = Inches(5.7)
    s6_card_layer_h = Inches(0.90)
    s6_layer_gap = Inches(0.10)

    for i, (l_title, l_desc, l_color) in enumerate(layers_text):
        y_lay = s6_top + i * (s6_card_layer_h + s6_layer_gap)
        l_box = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, s6_r_left, y_lay, s6_r_w, s6_card_layer_h)
        l_box.fill.solid()
        l_box.fill.fore_color.rgb = C_CARD
        l_box.line.color.rgb = l_color
        l_box.line.width = Pt(1)

        tf_l = l_box.text_frame
        tf_l.word_wrap = True
        tf_l.margin_left = tf_l.margin_right = tf_l.margin_top = Inches(0.12)

        pl1 = tf_l.paragraphs[0]
        pl1.text = l_title
        pl1.font.name = FONT_TITLE
        pl1.font.size = Pt(11)
        pl1.font.bold = True
        pl1.font.color.rgb = l_color

        pl2 = tf_l.add_paragraph()
        pl2.text = l_desc
        pl2.font.name = FONT_BODY
        pl2.font.size = Pt(9)
        pl2.font.color.rgb = C_TEXT_MUTED
        pl2.space_before = Pt(2)

    add_notes(s6, "01:40 - 01:58 (18 seg)", "Explicar arquitectura en capas con solidez metodológica",
              "El sistema opera en un Monorepo Turborepo con 5 capas desacopladas: interfaz reactiva en React 18 y Vite; API Gateway en Express y TypeScript con Zod; concurrencia en Redis 7; persistencia relacional en PostgreSQL 16 con Prisma ORM y tsrange; e infraestructura elástica en Google Cloud Platform.",
              "Guiar la vista de los jueces con la mano hacia el diagrama de 5 capas en pantalla. Pausa breve entre capas.")

    # ==========================================
    # SLIDE 7: ECOSISTEMA & HERRAMIENTAS DE DESARROLLO
    # ==========================================
    s7 = create_base_slide(
        "Ecosistema & Herramientas de Desarrollo",
        "Stack Tecnológico Seleccionado",
        "Tecnologías modernas, probadas en producción e interoperables",
        7
    )

    stack_quads = [
        {
            "icon": "🎨",
            "title": "Frontend & UI",
            "subtitle": "UX Diseñado para Mostrador",
            "color": C_CYAN,
            "bullets": [
                ("React 18 & Vite:", "Carga instantánea y hot reload para terminales táctiles."),
                ("TypeScript:", "Tipado estático estricto en inventario y formularios."),
                ("Tailwind CSS:", "Design System oficial UdeG (#002B49 / Outfit)."),
                ("Canvas & WebRTC:", "Firma táctil digital y lector QR por cámara.")
            ]
        },
        {
            "icon": "⚙",
            "title": "Backend & Datos",
            "subtitle": "Microservicios & Concurrencia",
            "color": C_GREEN_LIGHT,
            "bullets": [
                ("Node.js & Express:", "API REST modular en monorepo Turborepo."),
                ("PostgreSQL 16:", "RDBMS ACID con exclusión GiST de solapes tsrange."),
                ("Prisma ORM:", "Consultas SQL tipadas y migraciones reproducibles."),
                ("Redis 7 In-Memory:", "Cerrojos atómicos distribuidos anti-empalme.")
            ]
        },
        {
            "icon": "🛡",
            "title": "Seguridad & Auth",
            "subtitle": "Cumplimiento Institucional",
            "color": C_AMBER_LIGHT,
            "bullets": [
                ("Google OAuth 2.0:", "Restricción a dominios @udg.mx y @alumnos."),
                ("JWT RS256:", "Tokens de 15m con refresh tokens de 7 días."),
                ("HMAC-SHA256:", "Sellado criptográfico de actas PDF foliadas."),
                ("Zod & Helmet:", "Validación de esquema y cabeceras OWASP.")
            ]
        },
        {
            "icon": "🚀",
            "title": "DevOps & Cloud",
            "subtitle": "Infraestructura Resiliente",
            "color": C_CYAN,
            "bullets": [
                ("GCP Cloud Run:", "Contenedores serverless con autoescalado a 0."),
                ("Docker Multi-Stage:", "Imágenes de producción livianas (<150MB)."),
                ("Turborepo & pnpm:", "Compilación incremental y caché unificado."),
                ("GitHub Actions:", "Pipeline CI/CD con pruebas de integración E2E.")
            ]
        }
    ]

    s7_col_w = Inches(2.75)
    s7_col_gap = Inches(0.24)
    s7_top = Inches(1.68)
    s7_h = Inches(5.0)

    for i, q in enumerate(stack_quads):
        s7_left = Inches(0.8) + i * (s7_col_w + s7_col_gap)
        q_box = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, s7_left, s7_top, s7_col_w, s7_h)
        q_box.fill.solid()
        q_box.fill.fore_color.rgb = C_CARD
        q_box.line.color.rgb = q['color']
        q_box.line.width = Pt(1)

        tf_q = q_box.text_frame
        tf_q.word_wrap = True
        tf_q.margin_left = tf_q.margin_right = tf_q.margin_top = Inches(0.18)

        pq1 = tf_q.paragraphs[0]
        pq1.text = f"{q['icon']} {q['title']}"
        pq1.font.name = FONT_TITLE
        pq1.font.size = Pt(13)
        pq1.font.bold = True
        pq1.font.color.rgb = q['color']

        pq2 = tf_q.add_paragraph()
        pq2.text = q['subtitle']
        pq2.font.name = FONT_TITLE
        pq2.font.size = Pt(9.5)
        pq2.font.bold = True
        pq2.font.color.rgb = C_TEXT_WHITE
        pq2.space_before = Pt(2)

        for b_t, b_d in q['bullets']:
            pb = tf_q.add_paragraph()
            pb.text = f"• {b_t} {b_d}"
            pb.font.name = FONT_BODY
            pb.font.size = Pt(9.5)
            pb.font.color.rgb = C_TEXT_MUTED
            pb.space_before = Pt(7)

    add_notes(s7, "01:58 - 02:16 (18 seg)", "Respaldar selección tecnológica bajo estándares de industria",
              "Seleccionamos herramientas probadas en producción: Tailwind CSS con la paleta oficial UdeG y fuente Outfit; PostgreSQL con transacciones ACID; seguridad OWASP Top 10 con OAuth federado @udg.mx y sellos HMAC-SHA256; y entrega continua mediante GitHub Actions con pruebas de integración automatizadas.",
              "Transmitir solvencia técnica al justificar el tipado de TypeScript y la exclusión de solapes en PostgreSQL.")

    # ==========================================
    # SLIDE 8: ASEGURAMIENTO DE CALIDAD DE SOFTWARE
    # ==========================================
    s8 = create_base_slide(
        "Aseguramiento de Calidad de Software",
        "Módulo de Seguridad, Pruebas de Humo y Autenticación UdeG",
        "Validación formal de casos de prueba según formato institucional de laboratorio",
        8
    )

    # Left: Login Screenshot
    s8_left_w = Inches(5.7)
    s8_top = Inches(1.68)
    s8_h = Inches(4.9)
    img_card8 = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), s8_top, s8_left_w, s8_h)
    img_card8.fill.solid()
    img_card8.fill.fore_color.rgb = C_CARD
    img_card8.line.color.rgb = C_BORDER

    if os.path.exists('docs/pruebas/screenshots/01_identidad_institucional.png'):
        s8.shapes.add_picture('docs/pruebas/screenshots/01_identidad_institucional.png', Inches(0.95), s8_top + Inches(0.15), width=s8_left_w - Inches(0.3), height=Inches(4.1))

    cap8 = s8.shapes.add_textbox(Inches(0.95), s8_top + Inches(4.35), s8_left_w - Inches(0.3), Inches(0.35))
    tf_c8 = cap8.text_frame
    tf_c8.word_wrap = True
    p_c8 = tf_c8.paragraphs[0]
    p_c8.alignment = PP_ALIGN.CENTER
    p_c8.text = "Figura 3: Interfaz de Acceso Institucional SIGRE con Google Workspace UdeG"
    p_c8.font.name = FONT_BODY
    p_c8.font.size = Pt(10)
    p_c8.font.color.rgb = C_TEXT_MUTED

    # Right: Test Cases Table Box (Native PPTX Table)
    s8_r_left = Inches(6.833)
    s8_r_w = Inches(5.7)

    t_box = s8.shapes.add_textbox(s8_r_left, s8_top, s8_r_w, Inches(0.35))
    tf_tb = t_box.text_frame
    tf_tb.margin_left = tf_tb.margin_top = tf_tb.margin_right = tf_tb.margin_bottom = 0
    ptb = tf_tb.paragraphs[0]
    ptb.text = "Matriz de Casos de Prueba (Smoke Testing Automatizado)"
    ptb.font.name = FONT_TITLE
    ptb.font.size = Pt(12)
    ptb.font.bold = True
    ptb.font.color.rgb = C_CYAN

    table_shape = s8.shapes.add_table(5, 4, s8_r_left, s8_top + Inches(0.38), s8_r_w, Inches(2.95))
    table = table_shape.table
    table.columns[0].width = Inches(0.85)
    table.columns[1].width = Inches(2.00)
    table.columns[2].width = Inches(1.85)
    table.columns[3].width = Inches(1.00)

    headers = ["ID", "Escenario Evaluado", "Salida Esperada", "Resultado"]
    for col_idx, h_text in enumerate(headers):
        cell = table.cell(0, col_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = C_NAVY_UDEG
        cell.margin_left = cell.margin_right = Inches(0.08)
        cell.margin_top = cell.margin_bottom = Inches(0.06)
        p = cell.text_frame.paragraphs[0]
        p.text = h_text
        p.font.name = FONT_TITLE
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = C_CYAN
        if col_idx in (0, 3):
            p.alignment = PP_ALIGN.CENTER

    tests = [
        ("CP-01", "Admin/Alumno con @udg.mx válido", "Redirección a dashboard según rol", "EXITOSO"),
        ("CP-02", "Cuenta personal externa (@gmail.com)", "Bloqueo HTTP 403 ('Solo UdeG')", "EXITOSO"),
        ("CP-03", "Reserva simultánea del mismo espacio", "Lock Redis 201 / Bloqueo 409", "EXITOSO"),
        ("CP-04", "Alumno intentando ruta /admin/config", "Denegación RBAC 403 sin fuga", "EXITOSO")
    ]

    for row_idx, (id_t, desc_t, exp_t, res_t) in enumerate(tests, start=1):
        row_bg = C_CARD if row_idx % 2 == 1 else C_CARD_ELEV
        row_data = [id_t, desc_t, exp_t, res_t]
        for col_idx, val in enumerate(row_data):
            cell = table.cell(row_idx, col_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = row_bg
            cell.margin_left = cell.margin_right = Inches(0.08)
            cell.margin_top = cell.margin_bottom = Inches(0.05)
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.name = FONT_BODY
            p.font.size = Pt(8.5)
            if col_idx == 0:
                p.font.bold = True
                p.font.color.rgb = C_CYAN
                p.alignment = PP_ALIGN.CENTER
            elif col_idx == 3:
                p.font.bold = True
                p.font.color.rgb = C_GREEN_LIGHT
                p.alignment = PP_ALIGN.CENTER
            else:
                p.font.color.rgb = C_TEXT_WHITE if col_idx == 1 else C_TEXT_MUTED

    # Right Bottom: RBAC Details
    rbac_card = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, s8_r_left, s8_top + Inches(3.45), s8_r_w, Inches(1.45))
    rbac_card.fill.solid()
    rbac_card.fill.fore_color.rgb = C_CARD_ELEV
    rbac_card.line.color.rgb = C_BORDER
    rbac_card.line.width = Pt(1)

    tf_rb = rbac_card.text_frame
    tf_rb.word_wrap = True
    tf_rb.margin_left = tf_rb.margin_right = tf_rb.margin_top = Inches(0.15)

    pr1 = tf_rb.paragraphs[0]
    pr1.text = "🛡 Mecanismo de Autorización RBAC Institucional"
    pr1.font.name = FONT_TITLE
    pr1.font.size = Pt(11)
    pr1.font.bold = True
    pr1.font.color.rgb = C_AMBER_LIGHT

    pr2 = tf_rb.add_paragraph()
    pr2.text = "El token JWT contiene claims de rol inmutables. El middleware verifica autorizaciones en memoria en cada request, impidiendo escalamiento horizontal o vertical de privilegios."
    pr2.font.name = FONT_BODY
    pr2.font.size = Pt(9.5)
    pr2.font.color.rgb = C_TEXT_MUTED
    pr2.space_before = Pt(3)

    add_notes(s8, "02:16 - 02:32 (16 seg)", "Demostrar aseguramiento de calidad con pruebas de laboratorio",
              "Validamos formalmente el sistema con pruebas de humo. El flujo de acceso institucional restringe el login exclusivamente a correos UdeG, denegando cuentas personales con HTTP 403, mientras que nuestro control de acceso RBAC blinda las rutas contables y directivas frente a cualquier escalamiento no autorizado.",
              "Apuntar a la matriz de pruebas de humo. Resaltar la exclusividad del dominio institucional.")

    # ==========================================
    # SLIDE 9: OPERACIÓN EN VENTANILLA & EXPERIENCIA DE USUARIO
    # ==========================================
    s9 = create_base_slide(
        "Operación en Ventanilla & Experiencia de Usuario",
        "Módulo de Ventanilla Ágil, Escaneo QR y Firma Digital",
        "Despacho de equipo en menos de 30 segundos con acta responsiva oficial y checklist bilateral",
        9
    )

    # Left: QR Scanner Screenshot
    s9_left_w = Inches(5.7)
    s9_top = Inches(1.68)
    s9_h = Inches(4.9)
    img_card9 = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), s9_top, s9_left_w, s9_h)
    img_card9.fill.solid()
    img_card9.fill.fore_color.rgb = C_CARD
    img_card9.line.color.rgb = C_BORDER

    if os.path.exists('docs/pruebas/screenshots/09_escaner_qr_camara.png'):
        s9.shapes.add_picture('docs/pruebas/screenshots/09_escaner_qr_camara.png', Inches(0.95), s9_top + Inches(0.15), width=s9_left_w - Inches(0.3), height=Inches(4.1))

    cap9 = s9.shapes.add_textbox(Inches(0.95), s9_top + Inches(4.35), s9_left_w - Inches(0.3), Inches(0.35))
    tf_c9 = cap9.text_frame
    tf_c9.word_wrap = True
    p_c9 = tf_c9.paragraphs[0]
    p_c9.alignment = PP_ALIGN.CENTER
    p_c9.text = "Figura 4: Despacho de Ventanilla con Escáner QR WebRTC y Validación Óptica"
    p_c9.font.name = FONT_BODY
    p_c9.font.size = Pt(10)
    p_c9.font.color.rgb = C_TEXT_MUTED

    # Right: 2 Feature boxes
    s9_r_left = Inches(6.833)
    s9_r_w = Inches(5.7)

    # Box 1: Flujo Express
    f1_card = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, s9_r_left, s9_top, s9_r_w, Inches(2.35))
    f1_card.fill.solid()
    f1_card.fill.fore_color.rgb = C_CARD
    f1_card.line.color.rgb = C_CYAN
    f1_card.line.width = Pt(1)

    tf_f1 = f1_card.text_frame
    tf_f1.word_wrap = True
    tf_f1.margin_left = tf_f1.margin_right = tf_f1.margin_top = Inches(0.18)

    pf1 = tf_f1.paragraphs[0]
    pf1.text = "⚡ Despacho Óptico Express en 3 Pasos"
    pf1.font.name = FONT_TITLE
    pf1.font.size = Pt(12)
    pf1.font.bold = True
    pf1.font.color.rgb = C_CYAN

    steps = [
        "1. Presentación QR: El usuario muestra su código dinámico desde la app o PDF.",
        "2. Lectura Inmediata: La cámara web del navegador decodifica el token en < 2 seg.",
        "3. Validación y Asignación: El sistema muestra el número de serie físico exacto."
    ]
    for st in steps:
        pst = tf_f1.add_paragraph()
        pst.text = st
        pst.font.name = FONT_BODY
        pst.font.size = Pt(10)
        pst.font.color.rgb = C_TEXT_MUTED
        pst.space_before = Pt(3)

    # Box 2: Checklist & Firma Digital
    f2_card = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, s9_r_left, Inches(4.15), s9_r_w, Inches(2.43))
    f2_card.fill.solid()
    f2_card.fill.fore_color.rgb = C_CARD
    f2_card.line.color.rgb = C_GREEN_LIGHT
    f2_card.line.width = Pt(1)

    tf_f2 = f2_card.text_frame
    tf_f2.word_wrap = True
    tf_f2.margin_left = tf_f2.margin_right = tf_f2.margin_top = Inches(0.18)

    pf2 = tf_f2.paragraphs[0]
    pf2.text = "📝 Checklist Bilateral y Acta Digital HMAC-SHA256"
    pf2.font.name = FONT_TITLE
    pf2.font.size = Pt(12)
    pf2.font.bold = True
    pf2.font.color.rgb = C_GREEN_LIGHT

    checks = [
        "• Inspección Física Rápida: Marcado bilateral de puertos, cables y accesorios.",
        "• Firma Digitalizada en Canvas: Trazo manuscrito en pantalla táctil con sellado UTC.",
        "• Acta Inmutable PDF: Generación con hash HMAC-SHA256 enviado por correo al custodio.",
        "• Cadena de Custodia: Deslinde patrimonial automático ante auditorías universitarias."
    ]
    for ch in checks:
        pch = tf_f2.add_paragraph()
        pch.text = ch
        pch.font.name = FONT_BODY
        pch.font.size = Pt(9.5)
        pch.font.color.rgb = C_TEXT_MUTED
        pch.space_before = Pt(3)

    add_notes(s9, "02:32 - 02:50 (18 seg)", "Explicar agilidad operativa de ventanilla y valor para el almacenista",
              "En mostrador, el despacho toma menos de 30 segundos. El almacenista lee el QR desde la cámara del navegador web mediante WebRTC sin lectores costosos. El alumno firma en la pantalla táctil y el sistema genera de inmediato un acta foliada en PDF con firma HMAC-SHA256 enviada por correo.",
              "Voz dinámica. Destacar que no se requiere hardware propietario, reduciendo costos de implantación.")

    # ==========================================
    # SLIDE 10: GESTIÓN DIRECTIVA & AUDITORÍA PATRIMONIAL
    # ==========================================
    s10 = create_base_slide(
        "Gestión Directiva & Auditoría Patrimonial",
        "Panel Ejecutivo, Telemetría de Espacios y Auditoría Patrimonial",
        "Control integral de activos, reportes de ocupación y bitácora criptográfica para la administración",
        10
    )

    # Left: Dashboard Screenshot
    s10_left_w = Inches(5.7)
    s10_top = Inches(1.68)
    s10_h = Inches(4.9)
    img_card10 = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), s10_top, s10_left_w, s10_h)
    img_card10.fill.solid()
    img_card10.fill.fore_color.rgb = C_CARD
    img_card10.line.color.rgb = C_BORDER

    if os.path.exists('docs/pruebas/screenshots/08_dashboard_ejecutivo.png'):
        s10.shapes.add_picture('docs/pruebas/screenshots/08_dashboard_ejecutivo.png', Inches(0.95), s10_top + Inches(0.15), width=s10_left_w - Inches(0.3), height=Inches(4.1))

    cap10 = s10.shapes.add_textbox(Inches(0.95), s10_top + Inches(4.35), s10_left_w - Inches(0.3), Inches(0.35))
    tf_c10 = cap10.text_frame
    tf_c10.word_wrap = True
    p_c10 = tf_c10.paragraphs[0]
    p_c10.alignment = PP_ALIGN.CENTER
    p_c10.text = "Figura 5: Tablero Administrativo con Telemetría de Espacios y Métricas de Ocupación"
    p_c10.font.name = FONT_BODY
    p_c10.font.size = Pt(10)
    p_c10.font.color.rgb = C_TEXT_MUTED

    # Right: 3 Management Modules
    s10_r_left = Inches(6.833)
    s10_r_w = Inches(5.7)
    mods_adm = [
        ("📦 Control y Trazabilidad de Inventario por Serie", "Monitoreo en tiempo real del ciclo de vida de cada activo (en estante, en uso, mantenimiento o baja), vinculando cada préstamo a su acta digital foliada.", C_CYAN),
        ("📊 Telemetría y Aprovechamiento de Aulas y Auditorios", "Analítica de horas de uso por edificio, tasa de ocupación pico y reportes ejecutivos exportables para planeación de compras y presupuestos.", C_GREEN_LIGHT),
        ("🛡 Gestión de Incidencias y Algoritmo Trust Score", "Deslinde de averías con evidencia fotográfica obligatoria. El Trust Score premia el cuidado de equipo y bloquea solicitudes a usuarios con adeudos activos.", C_AMBER_LIGHT)
    ]

    card_adm_h = Inches(1.52)
    card_adm_gap = Inches(0.16)

    for i, (m_tit, m_det, m_col) in enumerate(mods_adm):
        y_adm = s10_top + i * (card_adm_h + card_adm_gap)
        adm_card = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, s10_r_left, y_adm, s10_r_w, card_adm_h)
        adm_card.fill.solid()
        adm_card.fill.fore_color.rgb = C_CARD
        adm_card.line.color.rgb = m_col
        adm_card.line.width = Pt(1)

        tf_ad = adm_card.text_frame
        tf_ad.word_wrap = True
        tf_ad.margin_left = tf_ad.margin_right = tf_ad.margin_top = Inches(0.15)

        pad1 = tf_ad.paragraphs[0]
        pad1.text = m_tit
        pad1.font.name = FONT_TITLE
        pad1.font.size = Pt(11.5)
        pad1.font.bold = True
        pad1.font.color.rgb = m_col

        pad2 = tf_ad.add_paragraph()
        pad2.text = m_det
        pad2.font.name = FONT_BODY
        pad2.font.size = Pt(9.5)
        pad2.font.color.rgb = C_TEXT_MUTED
        pad2.space_before = Pt(3)

    add_notes(s10, "02:50 - 03:08 (18 seg)", "Demostrar valor para la toma de decisiones directivas y auditoría",
              "El panel administrativo provee telemetría en tiempo real: monitorea la ocupación de auditorios y laboratorios, audita la cadena de custodia por número de serie, y clasifica incidencias fotográficas asociadas al Trust Score del usuario para transparentar la rendición de cuentas ante la administración.",
              "Tono institucional. Apuntar al tablero de control en la imagen.")

    # ==========================================
    # SLIDE 11: PROPUESTA DE VALOR & MERCADO
    # ==========================================
    s11 = create_base_slide(
        "Propuesta de Valor & Mercado",
        "Ventajas Competitivas de la Plataforma SIGRE",
        "Comparativa técnica frente a libretas analógicas, sistemas centrales rígidos y software comercial extranjero",
        11
    )

    comps = [
        {
            "icon": "⚡",
            "title": "Agilidad en Ventanilla",
            "desc": "Despacho en mostrador en menos de 30 segundos mediante escaneo QR WebRTC y firma en canvas.",
            "sub": "Reduce 90% el tiempo en fila frente a libretas (4.5 a 6 min).",
            "color": C_CYAN,
            "bullets": [
                "Operación táctil ultrarrápida.",
                "Sin pistolas lectoras propietarias.",
                "Atención ágil en cambio de turno."
            ]
        },
        {
            "icon": "🔒",
            "title": "Cero Empalmes con Redis",
            "desc": "Certeza transaccional absoluta en reservas de auditorios y laboratorios especializados.",
            "sub": "Cerrojos distribuidos temporales (TTL 15 min) que previenen dobles agendamientos.",
            "color": C_GREEN_LIGHT,
            "bullets": [
                "Aislamiento concurrente atómico.",
                "Expiración automática por abandono.",
                "Integración con PostgreSQL tsrange."
            ]
        },
        {
            "icon": "💰",
            "title": "Ahorro Comprobado y ROI",
            "desc": "Sustituye mermas históricas de $115k/año por un ahorro neto estimado de $80,500 MXN.",
            "sub": "Cuota de suscripción de $24k a $48k/año, 60% inferior a ERPs foráneos.",
            "color": C_AMBER_LIGHT,
            "bullets": [
                "Payback del proyecto en Mes 29.4.",
                "Liquidación inversionista en Mes 31.2.",
                "TIR robusta del 24.27% anual."
            ]
        },
        {
            "icon": "📜",
            "title": "Validez Jurídica y Cero Papel",
            "desc": "Acta responsiva foliada en PDF con firma Canvas y hash HMAC-SHA256 conforme a la LGPDPPSO.",
            "sub": "Sustituye más de 12,000 vales de papel al año por campus universitario.",
            "color": C_CYAN,
            "bullets": [
                "Alineación con política Cero Papel.",
                "Respaldo legal ante Contraloría.",
                "Soporte local en sitio y WhatsApp."
            ]
        }
    ]

    s11_col_w = Inches(2.75)
    s11_col_gap = Inches(0.24)
    s11_top = Inches(1.68)
    s11_h = Inches(5.0)

    for i, c in enumerate(comps):
        s11_left = Inches(0.8) + i * (s11_col_w + s11_col_gap)
        c_box = s11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, s11_left, s11_top, s11_col_w, s11_h)
        c_box.fill.solid()
        c_box.fill.fore_color.rgb = C_CARD
        c_box.line.color.rgb = c['color']
        c_box.line.width = Pt(1)

        tf_c = c_box.text_frame
        tf_c.word_wrap = True
        tf_c.margin_left = tf_c.margin_right = tf_c.margin_top = Inches(0.18)

        pc1 = tf_c.paragraphs[0]
        pc1.text = f"{c['icon']} {c['title']}"
        pc1.font.name = FONT_TITLE
        pc1.font.size = Pt(13)
        pc1.font.bold = True
        pc1.font.color.rgb = c['color']

        pc2 = tf_c.add_paragraph()
        pc2.text = c['desc']
        pc2.font.name = FONT_BODY
        pc2.font.size = Pt(9.5)
        pc2.font.color.rgb = C_TEXT_WHITE
        pc2.space_before = Pt(4)

        pc3 = tf_c.add_paragraph()
        pc3.text = f"▶ {c['sub']}"
        pc3.font.name = FONT_BODY
        pc3.font.size = Pt(9)
        pc3.font.bold = True
        pc3.font.color.rgb = C_CYAN
        pc3.space_before = Pt(6)

        for b in c['bullets']:
            pb = tf_c.add_paragraph()
            pb.text = f"• {b}"
            pb.font.name = FONT_BODY
            pb.font.size = Pt(9)
            pb.font.color.rgb = C_TEXT_MUTED
            pb.space_before = Pt(4)

    add_notes(s11, "03:08 - 03:26 (18 seg)", "Posicionamiento competitivo contundente y argumentos de negocio",
              "Frente a libretas y software comercial genérico, SIGRE destaca por su velocidad de entrega, cero empalmes de horario y un ahorro neto proyectado de 80,500 pesos anuales por plantel en mermas evitables, a una tarifa de suscripción hasta 60% menor y con soporte local especializado.",
              "Enfatizar el ahorro de $80,500 pesos frente al costo de suscripción. Cero dudas en la voz.")

    # ==========================================
    # SLIDE 12: EVOLUCIÓN & ESCALABILIDAD
    # ==========================================
    s12 = create_base_slide(
        "Evolución & Escalabilidad",
        "Recomendaciones & Hoja de Ruta Tecnológica",
        "Estrategia de escalamiento comercial y evolución técnica a corto y mediano plazo (Años 1 a 5)",
        12
    )

    roadmap = [
        {
            "icon": "📱",
            "title": "1. Credencial Universitaria Digital NFC / Wallet",
            "desc": "Integración con tarjetas de identificación institucional mediante chips NFC en teléfonos móviles, permitiendo check-in presencial en mostrador y registro de acceso sin contacto físico.",
            "color": C_CYAN
        },
        {
            "icon": "🚪",
            "title": "2. Cerraduras Inteligentes IoT para Aulas y Recintos",
            "desc": "Conexión de electroimanes y chapas inteligentes vía microcontroladores ESP32 y protocolo MQTT, habilitando la apertura automática de puertas cuando el usuario presenta su QR o reserva activa.",
            "color": C_GREEN_LIGHT
        },
        {
            "icon": "🤖",
            "title": "3. Modelos Predictivos de Demanda y Mantenimiento (IA / ML)",
            "desc": "Entrenamiento de modelos de series temporales en BigQuery ML para pronosticar picos de saturación en auditorios y calendarizar mantenimientos preventivos a proyectores según horas de lámpara.",
            "color": C_AMBER_LIGHT
        },
        {
            "icon": "🌐",
            "title": "4. Expansión Multisede a Tecnológicos y UPES Estatales",
            "desc": "Habilitación de arquitectura multi-tenant completa para desplegar SIGRE en los Institutos Tecnológicos de Jalisco (UTJ, ITSZ) y las más de 60 Universidades Públicas Estatales de México.",
            "color": C_CYAN
        }
    ]

    s12_card_w = Inches(5.7)
    s12_card_h = Inches(2.35)
    s12_row1_top = Inches(1.68)
    s12_row2_top = Inches(4.25)
    s12_col1_left = Inches(0.8)
    s12_col2_left = Inches(6.833)

    s12_coords = [
        (s12_col1_left, s12_row1_top),
        (s12_col2_left, s12_row1_top),
        (s12_col1_left, s12_row2_top),
        (s12_col2_left, s12_row2_top)
    ]

    for (left, top), r in zip(s12_coords, roadmap):
        r_box = s12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, s12_card_w, s12_card_h)
        r_box.fill.solid()
        r_box.fill.fore_color.rgb = C_CARD
        r_box.line.color.rgb = r['color']
        r_box.line.width = Pt(1)

        tf_r = r_box.text_frame
        tf_r.word_wrap = True
        tf_r.margin_left = tf_r.margin_right = tf_r.margin_top = Inches(0.2)

        pr1 = tf_r.paragraphs[0]
        pr1.text = f"{r['icon']} {r['title']}"
        pr1.font.name = FONT_TITLE
        pr1.font.size = Pt(13)
        pr1.font.bold = True
        pr1.font.color.rgb = r['color']

        pr2 = tf_r.add_paragraph()
        pr2.text = r['desc']
        pr2.font.name = FONT_BODY
        pr2.font.size = Pt(10)
        pr2.font.color.rgb = C_TEXT_MUTED
        pr2.space_before = Pt(5)

    add_notes(s12, "03:26 - 03:44 (18 seg)", "Proyectar visión de futuro, innovación y escalabilidad nacional",
              "Nuestra hoja de ruta contempla cuatro etapas de crecimiento: integración de credencial digital NFC en móviles; cerraduras electrónicas IoT para aulas magnas; modelos de IA en BigQuery para mantenimiento predictivo de proyectores; y escalamiento multisede a Tecnológicos y Universidades Públicas Estatales.",
              "Voz entusiasta y de visión a largo plazo. Mostrar que el proyecto tiene un plan de vida sólido.")

    # ==========================================
    # SLIDE 13: CIERRE ACADÉMICO & RESULTADOS
    # ==========================================
    s13 = create_base_slide(
        "Cierre Académico & Resultados",
        "Conclusiones del Proyecto Integrador SIGRE",
        "Validación integral de competencias de ingeniería y compromiso social en ExpoDIT 2026",
        13
    )

    # Left: Usability SUS Chart
    s13_left_w = Inches(5.7)
    s13_top = Inches(1.68)
    s13_h = Inches(4.9)
    img_card13 = s13.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), s13_top, s13_left_w, s13_h)
    img_card13.fill.solid()
    img_card13.fill.fore_color.rgb = C_CARD
    img_card13.line.color.rgb = C_BORDER

    if os.path.exists('docs/pruebas/screenshots/10_distribucion_puntajes_sus.png'):
        s13.shapes.add_picture('docs/pruebas/screenshots/10_distribucion_puntajes_sus.png', Inches(0.95), s13_top + Inches(0.15), width=s13_left_w - Inches(0.3), height=Inches(4.1))

    cap13 = s13.shapes.add_textbox(Inches(0.95), s13_top + Inches(4.35), s13_left_w - Inches(0.3), Inches(0.35))
    tf_c13 = cap13.text_frame
    tf_c13.word_wrap = True
    p_c13 = tf_c13.paragraphs[0]
    p_c13.alignment = PP_ALIGN.CENTER
    p_c13.text = "Figura 6: Resultados Empíricos de Usabilidad SUS (Media 82.85 pts, Grado A Excelente, n=50)"
    p_c13.font.name = FONT_BODY
    p_c13.font.size = Pt(10)
    p_c13.font.color.rgb = C_TEXT_MUTED

    # Right: 3 Formal Conclusions
    s13_r_left = Inches(6.833)
    s13_r_w = Inches(5.7)
    concs = [
        ("1. Solución Tecnológica Integral y Validada en Campo", "Se cumplió el 100% de los requerimientos técnicos: transaccionalidad atómica en Redis, firma digital Canvas HMAC, control RBAC y una usabilidad empírica sobresaliente de 82.85 puntos en la escala SUS (n=50).", C_CYAN),
        ("2. Viabilidad Económica y Sustentabilidad Comprobada", "Evaluación financiera rigurosa: CAPEX de $180,000 MXN, VPN de +$46,984.47 MXN (TMAR 15%), TIR del 24.27% anual, Payback del proyecto en Mes 29.4 y ahorro de +$80,500 MXN/año en mermas evitables por plantel.", C_GREEN_LIGHT),
        ("3. Madurez de Ingeniería en ExpoDIT 2026", "La integración de patrones de software formales, despliegue cloud en GCP y cumplimiento de la Agenda ONU 2030 ('Cero Papel') demuestran la solidez formativa adquirida en el Centro Universitario de Tonalá.", C_AMBER_LIGHT)
    ]

    card_conc_h = Inches(1.52)
    card_conc_gap = Inches(0.16)

    for i, (c_tit, c_det, c_col) in enumerate(concs):
        y_c = s13_top + i * (card_conc_h + card_conc_gap)
        c_box = s13.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, s13_r_left, y_c, s13_r_w, card_conc_h)
        c_box.fill.solid()
        c_box.fill.fore_color.rgb = C_CARD
        c_box.line.color.rgb = c_col
        c_box.line.width = Pt(1)

        tf_cc = c_box.text_frame
        tf_cc.word_wrap = True
        tf_cc.margin_left = tf_cc.margin_right = tf_cc.margin_top = Inches(0.15)

        pcc1 = tf_cc.paragraphs[0]
        pcc1.text = c_tit
        pcc1.font.name = FONT_TITLE
        pcc1.font.size = Pt(11.5)
        pcc1.font.bold = True
        pcc1.font.color.rgb = c_col

        pcc2 = tf_cc.add_paragraph()
        pcc2.text = c_det
        pcc2.font.name = FONT_BODY
        pcc2.font.size = Pt(9.5)
        pcc2.font.color.rgb = C_TEXT_MUTED
        pcc2.space_before = Pt(3)

    add_notes(s13, "03:44 - 04:04 (20 seg)", "Cierre de alto impacto, conclusiones contundentes y agradecimiento",
              "Concluimos que SIGRE valida plenamente las competencias de ingeniería de ExpoDIT 2026: un software probado con 82.85 puntos SUS, financieramente viable con VPN de 46,984 pesos y Payback en el mes 29.4, y con impacto social y ambiental para la comunidad. Muchas gracias.",
              "Contacto visual formal, sonrisa segura, agradecimiento sincero y apertura inmediata a preguntas del jurado.")

    # Save Presentation
    output_path = 'docs/Presentacion_ExpoDIT_SIGRE.pptx'
    prs.save(output_path)
    print(f"Presentation saved successfully at: {output_path}")

if __name__ == '__main__':
    build_presentation()
