import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def create_presentation():
    prs = Presentation()
    # Configurar formato panorámico 16:9 (13.333 x 7.5 pulgadas)
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Paleta de Colores
    NAVY = RGBColor(0, 43, 73)        # #002B49
    BLUE_ACCENT = RGBColor(0, 102, 153) # #006699
    LIGHT_BG = RGBColor(248, 249, 250) # #F8F9FA
    WHITE = RGBColor(255, 255, 255)
    DARK_TEXT = RGBColor(33, 37, 41)   # #212529
    MUTED_TEXT = RGBColor(108, 117, 125)
    CARD_BG = RGBColor(240, 244, 248)
    BORDER_COLOR = RGBColor(218, 224, 233)
    
    blank_layout = prs.slide_layouts[6]
    
    def set_slide_background(slide, color):
        bg = slide.background
        fill = bg.fill
        fill.solid()
        fill.fore_color.rgb = color
        
    def add_header(slide, title_text, category_text="FORMULACIÓN Y EVALUACIÓN DE PROYECTOS DE INVERSIÓN"):
        # Categoría / Breadcrumb
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.35))
        tf_c = cat_box.text_frame
        tf_c.word_wrap = True
        p_c = tf_c.paragraphs[0]
        p_c.text = category_text.upper()
        p_c.font.name = "Arial"
        p_c.font.size = Pt(10)
        p_c.font.bold = True
        p_c.font.color.rgb = BLUE_ACCENT
        
        # Título de Diapositiva
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(11.7), Inches(0.7))
        tf_t = title_box.text_frame
        tf_t.word_wrap = True
        p_t = tf_t.paragraphs[0]
        p_t.text = title_text
        p_t.font.name = "Arial"
        p_t.font.size = Pt(22)
        p_t.font.bold = True
        p_t.font.color.rgb = NAVY
        
    def add_notes(slide, timing_and_script):
        notes_slide = slide.notes_slide
        tf = notes_slide.notes_text_frame
        tf.text = timing_and_script

    # =========================================================================
    # DIAPOSITIVA 1: PORTADA INSTITUCIONAL DE IDENTIFICACIÓN (0:00 - 0:45)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1, NAVY)
    
    # Membrete institucional
    box_inst = s1.shapes.add_textbox(Inches(1.0), Inches(0.8), Inches(11.3), Inches(0.8))
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
    box_main = s1.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(11.3), Inches(1.8))
    tf_main = box_main.text_frame
    tf_main.word_wrap = True
    p_m1 = tf_main.paragraphs[0]
    p_m1.text = "SIGRE: Sistema Integrado de Gestión de Recursos y Espacios"
    p_m1.font.name = "Arial"
    p_m1.font.size = Pt(30)
    p_m1.font.bold = True
    p_m1.font.color.rgb = WHITE
    
    p_m2 = tf_main.add_paragraph()
    p_m2.text = "Diagnóstico Causal de la Problemática en Control de Activos y Formulación de la Propuesta de Solución"
    p_m2.font.size = Pt(15)
    p_m2.font.color.rgb = RGBColor(190, 220, 255)
    p_m2.space_before = Pt(8)
    
    # Cuadro de Identificación / Datos del Equipo y Docente
    card_id = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(3.8), Inches(11.3), Inches(2.9))
    card_id.fill.solid()
    card_id.fill.fore_color.rgb = RGBColor(8, 55, 92)
    card_id.line.color.rgb = RGBColor(0, 102, 153)
    
    box_meta = s1.shapes.add_textbox(Inches(1.3), Inches(4.0), Inches(10.7), Inches(2.5))
    tf_meta = box_meta.text_frame
    tf_meta.word_wrap = True
    
    meta_lines = [
        ("Materia:", "Formulación y Evaluación de Proyectos de Inversión"),
        ("Docente Titular:", "Mtra. Abril Adriana Angulo Sherman"),
        ("Carrera:", "Ingeniería en Ciencias Computacionales / Tecnologías de Información"),
        ("Equipo:", "Equipo N° [Número de Equipo]"),
        ("Integrantes:", "[Nombre Completo 1] (Código: [Código 1]) | [Nombre Completo 2] (Código: [Código 2]) | [Nombre Completo 3] (Código: [Código 3])"),
        ("Fecha de Exposición:", "Septiembre de 2026 — CUTonalá")
    ]
    
    for idx, (label, val) in enumerate(meta_lines):
        p = tf_meta.paragraphs[0] if idx == 0 else tf_meta.add_paragraph()
        r1 = p.add_run()
        r1.text = f"{label} "
        r1.font.bold = True
        r1.font.size = Pt(12)
        r1.font.color.rgb = RGBColor(150, 205, 255)
        r2 = p.add_run()
        r2.text = val
        r2.font.size = Pt(12)
        r2.font.color.rgb = WHITE
        p.space_after = Pt(4)
        
    add_notes(s1, "TIEMPO: 0:00 - 0:45 (45 segundos)\n"
                  "GUIÓN: Buen día profesora y compañeros. El día de hoy el Equipo presenta la formulación de la problemática y la propuesta de solución para nuestro proyecto de inversión titulado SIGRE: Sistema Integrado de Gestión de Recursos y Espacios, enfocado en resolver las ineficiencias críticas de control y mermas patrimoniales en nuestra Red Universitaria.")

    # =========================================================================
    # DIAPOSITIVA 2: CONTEXTO INSTITUCIONAL (0:45 - 1:45)
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2, LIGHT_BG)
    add_header(s2, "Contexto Operativo: La Escala de la Red Universitaria")
    
    # 2 Columnas / Tarjetas
    c1 = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), Inches(5.6), Inches(4.8))
    c1.fill.solid()
    c1.fill.fore_color.rgb = WHITE
    c1.line.color.rgb = BORDER_COLOR
    
    tf1 = c1.text_frame
    tf1.word_wrap = True
    p1_t = tf1.paragraphs[0]
    p1_t.text = "🏛️ Magnitud Institucional"
    p1_t.font.bold = True
    p1_t.font.size = Pt(16)
    p1_t.font.color.rgb = NAVY
    p1_t.space_after = Pt(14)
    
    items_c1 = [
        "Red Universitaria con más de 300,000 estudiantes y 17,000 académicos activos en Jalisco (CGPE, 2024).",
        "CUTonalá como campus multidisciplinario en continua expansión de aulas magnas, laboratorios y talleres (Centro Universitario de Tonalá, 2023).",
        "Alta densidad de clases simultáneas que demandan equipo técnico y audiovisual por hora."
    ]
    for it in items_c1:
        p = tf1.add_paragraph()
        p.text = f"• {it}"
        p.font.size = Pt(13)
        p.font.color.rgb = DARK_TEXT
        p.space_after = Pt(10)
        
    c2 = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.6), Inches(5.7), Inches(4.8))
    c2.fill.solid()
    c2.fill.fore_color.rgb = WHITE
    c2.line.color.rgb = BORDER_COLOR
    
    tf2 = c2.text_frame
    tf2.word_wrap = True
    p2_t = tf2.paragraphs[0]
    p2_t.text = "⚠️ La Paradoja de Gestión Actual"
    p2_t.font.bold = True
    p2_t.font.size = Pt(16)
    p2_t.font.color.rgb = BLUE_ACCENT
    p2_t.space_after = Pt(14)
    
    items_c2 = [
        "Inversiones millonarias en proyectores, pantallas y equipo de cómputo para modernizar la enseñanza.",
        "Persistencia de métodos de hace décadas en mostrador: libretas de espiral, credenciales retenidas y notas manuscritas.",
        "Desconexión digital entre el inventario de almacén, los coordinadores de carrera y las aulas de clase."
    ]
    for it in items_c2:
        p = tf2.add_paragraph()
        p.text = f"• {it}"
        p.font.size = Pt(13)
        p.font.color.rgb = DARK_TEXT
        p.space_after = Pt(10)

    add_notes(s2, "TIEMPO: 0:45 - 1:45 (60 segundos)\n"
                  "GUIÓN: Para dimensionar el contexto, la Red Universitaria atiende a más de 300 mil alumnos. En CUTonalá el crecimiento de aulas y laboratorios es acelerado; sin embargo, existe una contradicción evidente: se invierten recursos en tecnología de aula, pero los métodos para administrar, prestar y resguardar ese equipamiento siguen basándose en libretas de papel y acuerdos de palabra.")

    # =========================================================================
    # DIAPOSITIVA 3: PROBLEMÁTICA CENTRAL (1:45 - 2:45)
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3, LIGHT_BG)
    add_header(s3, "La Problemática Central: El Colapso del Modelo Analógico")
    
    # 3 Tarjetas horizontales
    card_w = Inches(3.7)
    card_h = Inches(4.8)
    
    pains = [
        ("📋 Registro en Papel Vulnerable", 
         "El préstamo diario de cables HDMI, adaptadores y proyectores se registra en libretas físicas sin respaldo digital, expuestas a extravío, tachaduras y deterioro diario.",
         NAVY),
        ("🗓️ Empalmes de Espacios Físicos", 
         "Aulas magnas y auditorios apartados mediante oficios o mensajes verbales; provocan dobles asignaciones y clases suspendidas al inicio del bloque lectivo.",
         BLUE_ACCENT),
        ("🛡️ Ruptura de Cadena de Custodia", 
         "Falta de una responsiva electrónica oficial: ante daños o pérdidas, el mostrador carece de validez probatoria para el deslinde patrimonial (Universidad de Guadalajara, 2019).",
         NAVY)
    ]
    
    for idx, (title, desc, color) in enumerate(pains):
        x = Inches(0.8 + idx * 4.0)
        card = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(1.6), card_w, card_h)
        card.fill.solid()
        card.fill.fore_color.rgb = WHITE
        card.line.color.rgb = BORDER_COLOR
        
        tf = card.text_frame
        tf.word_wrap = True
        pt = tf.paragraphs[0]
        pt.text = title
        pt.font.bold = True
        pt.font.size = Pt(15)
        pt.font.color.rgb = color
        pt.space_after = Pt(14)
        
        pd = tf.add_paragraph()
        pd.text = desc
        pd.font.size = Pt(12.5)
        pd.font.color.rgb = DARK_TEXT
        pd.space_after = Pt(8)

    add_notes(s3, "TIEMPO: 1:45 - 2:45 (60 segundos)\n"
                  "GUIÓN: El problema central es el colapso del modelo analógico. Almacenes y prefecturas operan con bitácoras en papel que no permiten saber quién tiene qué bien en este momento. Las reservas de auditorios sufren empalmes constantes y cuando un equipo se daña o extravía, la libreta no tiene validez legal ni técnica para exigir la reposición.")

    # =========================================================================
    # DIAPOSITIVA 4: ANÁLISIS DE CAUSAS (2:45 - 4:00)
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4, LIGHT_BG)
    add_header(s4, "Análisis Causal: Raíces Estructurales del Problema")
    
    causes = [
        ("1. Causa Operativa", "Falta de Trazabilidad e Inventario Dinámico en Tiempo Real",
         "El personal de almacén no cuenta con un sistema centralizado que refleje al instante la disponibilidad, ubicación y estado físico de cada activo o espacio.",
         "Cita: (Universidad de Guadalajara, 2019)"),
        ("2. Causa Jurídica", "Inexistencia de Actas de Entrega-Recepción Vinculantes",
         "Anotar un nombre y garabatear una firma no cumple con las directrices de resguardo institucional ni estándares de firma digital oficial (Cámara de Diputados, 2017).",
         "Cita: (DOF, 2017)"),
        ("3. Causa de Gestión", "Ausencia de Co-Responsabilidad y Penalizaciones Auditables",
         "No existe un historial ni score de confiabilidad del usuario: quien entrega tarde o maltrata equipo no tiene seguimiento ni apercibimiento administrativo.",
         "Cita: (CEPAL, 2015)")
    ]
    
    for idx, (tag, c_title, desc, citation) in enumerate(causes):
        y = Inches(1.5 + idx * 1.7)
        card = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), y, Inches(11.7), Inches(1.5))
        card.fill.solid()
        card.fill.fore_color.rgb = WHITE
        card.line.color.rgb = BORDER_COLOR
        
        tf = card.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        r_tag = p.add_run()
        r_tag.text = f"{tag}: "
        r_tag.font.bold = True
        r_tag.font.size = Pt(13)
        r_tag.font.color.rgb = BLUE_ACCENT
        
        r_tit = p.add_run()
        r_tit.text = c_title
        r_tit.font.bold = True
        r_tit.font.size = Pt(13)
        r_tit.font.color.rgb = NAVY
        
        p_d = tf.add_paragraph()
        p_d.text = desc
        p_d.font.size = Pt(12)
        p_d.font.color.rgb = DARK_TEXT
        p_d.space_before = Pt(3)
        
        p_c = tf.add_paragraph()
        p_c.text = citation
        p_c.font.size = Pt(10)
        p_c.font.italic = True
        p_c.font.color.rgb = MUTED_TEXT

    add_notes(s4, "TIEMPO: 2:45 - 4:00 (75 segundos)\n"
                  "GUIÓN: Al investigar formalmente las causas raíz bajo metodología CEPAL, encontramos tres factores determinantes: Primero, la causa operativa por falta de visibilidad en tiempo real. Segundo, la fragilidad jurídica: las libretas carecen de validez como acta responsiva. Y tercero, la ausencia de un sistema de incentivos y reputación que fomente el cuidado de los bienes compartidos.")

    # =========================================================================
    # DIAPOSITIVA 5: CONSECUENCIAS E IMPACTO (4:00 - 5:15)
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5, LIGHT_BG)
    add_header(s5, "Consecuencias e Impacto: Merma Patrimonial y Afectación Docente")
    
    metrics = [
        ("$130,000 - $150,000 MXN", "Merma Silenciosa Anual por Plantel",
         "Pérdida acumulada en cables HDMI, adaptadores, apuntadores, micrófonos y fuentes de poder extraviados o devueltos dañados sin responsable directo.",
         NAVY),
        ("15 a 25 Minutos", "Tiempo de Clase Desperdiciado por Incidencia",
         "Afectación a la calidad pedagógica por resolución de empalmes en auditorios o búsqueda de reemplazos de equipo inoperante a mitad de clase.",
         BLUE_ACCENT),
        ("100% Ceguera", "Falta de Datos para Toma de Decisiones",
         "Compras y mantenimiento realizadas por intuición o urgencia al carecer de estadísticas sobre tasa de rotación y desgaste de activos.",
         NAVY)
    ]
    
    for idx, (val, tit, desc, col) in enumerate(metrics):
        x = Inches(0.8 + idx * 4.0)
        card = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(1.6), Inches(3.7), Inches(4.8))
        card.fill.solid()
        card.fill.fore_color.rgb = WHITE
        card.line.color.rgb = BORDER_COLOR
        
        tf = card.text_frame
        tf.word_wrap = True
        
        pv = tf.paragraphs[0]
        pv.text = val
        pv.font.bold = True
        pv.font.size = Pt(19)
        pv.font.color.rgb = col
        pv.space_after = Pt(8)
        
        pt = tf.add_paragraph()
        pt.text = tit
        pt.font.bold = True
        pt.font.size = Pt(13)
        pt.font.color.rgb = NAVY
        pt.space_after = Pt(12)
        
        pd = tf.add_paragraph()
        pd.text = desc
        pd.font.size = Pt(12)
        pd.font.color.rgb = DARK_TEXT

    add_notes(s5, "TIEMPO: 4:00 - 5:15 (75 segundos)\n"
                  "GUIÓN: Las consecuencias son graves y medibles. Con base en la experiencia en almacenes y Servicios Generales, se calcula una merma anual de entre 130 mil y 150 mil pesos por plantel en reposición constante de accesorios. Además, cada conflicto de espacio o equipo descompuesto arrebata de 15 a 25 minutos de clase, mientras los directivos carecen de métricas para planificar el presupuesto.")

    # =========================================================================
    # DIAPOSITIVA 6: PÚBLICO OBJETIVO (5:15 - 6:15)
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6, LIGHT_BG)
    add_header(s6, "Público Objetivo: Caracterización y Perfiles de Usuario")
    
    audiences = [
        ("👔 Decisores Institucionales", "Secretarios Administrativos, Directores de Centros Universitarios y SEMS",
         "• Necesidad: Rendición de cuentas clara en auditorías internas y externas.\n"
         "• Prioridad: Eliminar la fuga de presupuesto en reposición de equipo.\n"
         "• Rol en SIGRE: Compradores del servicio vía adjudicación directa.",
         NAVY),
        ("🧑‍💼 Operadores de Mostrador", "Encargados de Almacén, Prefectura y Coordinadores de Espacios",
         "• Necesidad: Agilizar la ventanilla y eliminar filas de profesores.\n"
         "• Prioridad: Contar con actas firmadas y respaldo formal en caso de daño.\n"
         "• Rol en SIGRE: Validación con escáner QR y doble checklist de entrega.",
         BLUE_ACCENT),
        ("🎓 Usuarios Solicitantes", "Comunidad Docente y Estudiantil (Pregrado y Posgrado)",
         "• Necesidad: Apartar espacios y proyectores desde su celular sin burocracia.\n"
         "• Prioridad: Certeza de que el aula y equipo estarán listos al llegar.\n"
         "• Rol en SIGRE: Reservas en línea, firma de responsiva y consulta de eventos.",
         NAVY)
    ]
    
    for idx, (tit, sub, pts, col) in enumerate(audiences):
        x = Inches(0.8 + idx * 4.0)
        card = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(1.6), Inches(3.7), Inches(4.8))
        card.fill.solid()
        card.fill.fore_color.rgb = WHITE
        card.line.color.rgb = BORDER_COLOR
        
        tf = card.text_frame
        tf.word_wrap = True
        
        pt = tf.paragraphs[0]
        pt.text = tit
        pt.font.bold = True
        pt.font.size = Pt(14.5)
        pt.font.color.rgb = col
        pt.space_after = Pt(4)
        
        ps = tf.add_paragraph()
        ps.text = sub
        ps.font.italic = True
        ps.font.size = Pt(11)
        ps.font.color.rgb = MUTED_TEXT
        ps.space_after = Pt(12)
        
        pp = tf.add_paragraph()
        pp.text = pts
        pp.font.size = Pt(12)
        pp.font.color.rgb = DARK_TEXT

    add_notes(s6, "TIEMPO: 5:15 - 6:15 (60 segundos)\n"
                  "GUIÓN: Nuestra solución atiende a tres audiencias bien definidas: A los Secretarios Administrativos que exigen cuentas claras y ahorro de presupuesto; a los operadores de almacén que necesitan rapidez y respaldo legal en ventanilla; y a la comunidad de profesores y alumnos que demandan apartar recursos de forma transparente desde su teléfono móvil.")

    # =========================================================================
    # DIAPOSITIVA 7: COMPARATIVA DE ALTERNATIVAS (6:15 - 7:15)
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7, LIGHT_BG)
    add_header(s7, "Propuestas de Atención: Evaluación de Alternativas de Solución")
    
    alts = [
        ("Alternativa A", "Modelo Analógico Reforzado", 
         "Incrementar libretas, formatos impresos y personal de vigilancia.",
         "❌ Ineficiente, costoso en insumos, vulnerable a pérdidas y sin trazabilidad digital.",
         MUTED_TEXT),
        ("Alternativa B", "Hojas de Cálculo Compartidas", 
         "Registros colaborativos en Google Sheets o Excel.",
         "⚠️ Vulnerable a sobreescritura accidental; no resuelve la fila ni genera actas de entrega firmadas.",
         BLUE_ACCENT),
        ("Alternativa C (Propuesta)", "Plataforma Cloud Dedicada (SIGRE)", 
         "Software especializado con responsivas electrónicas, QR y métricas.",
         "✅ Solución integral que ataca la causa raíz, automatiza el control y elimina la merma.",
         NAVY)
    ]
    
    for idx, (tag, tit, desc, crit, col) in enumerate(alts):
        y = Inches(1.5 + idx * 1.7)
        card = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), y, Inches(11.7), Inches(1.5))
        card.fill.solid()
        card.fill.fore_color.rgb = WHITE
        card.line.color.rgb = col if idx == 2 else BORDER_COLOR
        
        tf = card.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        r1 = p.add_run()
        r1.text = f"{tag}: {tit} — "
        r1.font.bold = True
        r1.font.size = Pt(13)
        r1.font.color.rgb = col
        
        r2 = p.add_run()
        r2.text = desc
        r2.font.size = Pt(12.5)
        r2.font.color.rgb = DARK_TEXT
        
        p_c = tf.add_paragraph()
        p_c.text = crit
        p_c.font.size = Pt(12)
        p_c.font.bold = (idx == 2)
        p_c.font.color.rgb = col if idx == 2 else DARK_TEXT
        p_c.space_before = Pt(4)

    add_notes(s7, "TIEMPO: 6:15 - 7:15 (60 segundos)\n"
                  "GUIÓN: Al comparar alternativas, vemos que más papel solo encarece la burocracia; las hojas de cálculo no sirven para el momento de la entrega física ni tienen validez jurídica. La única alternativa viable es una plataforma cloud especializada como SIGRE, diseñada desde la ventanilla del almacén hacia la directiva.")

    # =========================================================================
    # DIAPOSITIVA 8: PROPUESTA DE SOLUCIÓN: SIGRE (7:15 - 8:30)
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_background(s8, LIGHT_BG)
    add_header(s8, "Nuestra Propuesta de Solución: Ecosistema SIGRE")
    
    pillars = [
        ("📱 QR Dinámico e Intransferible", 
         "Validación del solicitante en ventanilla en menos de 5 segundos con credencial institucional digital."),
        ("📋 Doble Checklist Digital", 
         "Inspección guiada en salida y devolución para certificar el estado físico y accesorios completos."),
        ("⭐ Score de Confiabilidad", 
         "Puntaje de reputación por usuario: premia entregas a tiempo y suspende solicitudes a infractores recurrentes."),
        ("📑 Responsiva Electrónica Oficial", 
         "Acta digital foliada con sellos criptográficos y firma electrónica, con plena validez patrimonial.")
    ]
    
    for idx, (tit, desc) in enumerate(pillars):
        row = idx // 2
        col = idx % 2
        x = Inches(0.8 + col * 5.9)
        y = Inches(1.6 + row * 2.5)
        
        card = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, Inches(5.7), Inches(2.2))
        card.fill.solid()
        card.fill.fore_color.rgb = WHITE
        card.line.color.rgb = BORDER_COLOR
        
        tf = card.text_frame
        tf.word_wrap = True
        pt = tf.paragraphs[0]
        pt.text = tit
        pt.font.bold = True
        pt.font.size = Pt(14)
        pt.font.color.rgb = NAVY
        pt.space_after = Pt(8)
        
        pd = tf.add_paragraph()
        pd.text = desc
        pd.font.size = Pt(12)
        pd.font.color.rgb = DARK_TEXT

    add_notes(s8, "TIEMPO: 7:15 - 8:30 (75 segundos)\n"
                  "GUIÓN: SIGRE opera sobre 4 pilares: El boleto digital con QR intransferible para escanear en segundos; el doble checklist de entrega física; el score de confiabilidad que fomenta la cultura de cuidado; y la emisión de responsivas electrónicas oficiales con validez legal. Todo accesible desde cualquier navegador o teléfono móvil.")

    # =========================================================================
    # DIAPOSITIVA 9: HIPÓTESIS DEL PROYECTO (8:30 - 9:15)
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_background(s9, LIGHT_BG)
    add_header(s9, "Planteamiento Metodológico: Hipótesis de Solución")
    
    # Caja destacada para la hipótesis
    card_hyp = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), Inches(11.7), Inches(2.4))
    card_hyp.fill.solid()
    card_hyp.fill.fore_color.rgb = NAVY
    card_hyp.line.color.rgb = BLUE_ACCENT
    
    tfh = card_hyp.text_frame
    tfh.word_wrap = True
    pht = tfh.paragraphs[0]
    pht.text = "ENUNCIADO FORMAL DE LA HIPÓTESIS"
    pht.font.bold = True
    pht.font.size = Pt(12)
    pht.font.color.rgb = RGBColor(180, 215, 255)
    pht.space_after = Pt(8)
    
    phb = tfh.add_paragraph()
    phb.text = "«Si se implementa un sistema digital centralizado de gestión de recursos y espacios con responsivas electrónicas, doble checklist y trazabilidad en tiempo real de usuarios y activos (SIGRE), entonces se reducirán en al menos un 80% las mermas patrimoniales por extravío no atribuible de equipo técnico y se eliminarán al 100% los empalmes de agenda en espacios académicos de los planteles universitarios.»"
    phb.font.size = Pt(14)
    phb.font.bold = True
    phb.font.italic = True
    phb.font.color.rgb = WHITE
    
    # Desglose de Variables
    var_box = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(4.3), Inches(11.7), Inches(2.4))
    var_box.fill.solid()
    var_box.fill.fore_color.rgb = WHITE
    var_box.line.color.rgb = BORDER_COLOR
    
    tfv = var_box.text_frame
    tfv.word_wrap = True
    
    pvt = tfv.paragraphs[0]
    pvt.text = "Desglose y Operacionalización de Variables:"
    pvt.font.bold = True
    pvt.font.size = Pt(13)
    pvt.font.color.rgb = NAVY
    pvt.space_after = Pt(6)
    
    vars_list = [
        ("• Variable Independiente (Causa):", "Despliegue operativo de la plataforma SIGRE (módulos de QR, responsiva y checklist digital)."),
        ("• Variable Dependiente 1 (Efecto Económico):", "Tasa de reducción de pérdidas patrimoniales y mermas silenciosas de accesorios (Meta: >= 80%)."),
        ("• Variable Dependiente 2 (Efecto Operativo):", "Incidencia de empalmes o conflictos de agenda en espacios físicos y aulas magnas (Meta: 0%).")
    ]
    for lbl, desc in vars_list:
        p = tfv.add_paragraph()
        r1 = p.add_run()
        r1.text = f"{lbl} "
        r1.font.bold = True
        r1.font.size = Pt(12)
        r1.font.color.rgb = BLUE_ACCENT
        r2 = p.add_run()
        r2.text = desc
        r2.font.size = Pt(12)
        r2.font.color.rgb = DARK_TEXT
        p.space_after = Pt(4)

    add_notes(s9, "TIEMPO: 8:30 - 9:15 (45 segundos)\n"
                  "GUIÓN: Englobando todo nuestro razonamiento en una hipótesis formal: 'Si implementamos SIGRE con responsivas electrónicas, doble checklist y trazabilidad en tiempo real, reduciremos en al menos un 80% las mermas patrimoniales por extravío y eliminaremos al 100% los empalmes en auditorios y aulas'. Esto demuestra una relación causa-efecto perfectamente cuantificable.")

    # =========================================================================
    # DIAPOSITIVA 10: CONCLUSIÓN Y CIERRE (9:15 - 9:45)
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_background(s10, LIGHT_BG)
    add_header(s10, "Conclusiones: Viabilidad y Rentabilidad Institucional")
    
    conclusions = [
        ("💼 Viabilidad Financiera", 
         "El proyecto se autofinancia con el propio ahorro de las mermas patrimoniales evitadas; no genera un gasto oneroso para la universidad.",
         NAVY),
        ("⚙️ Factibilidad Operativa", 
         "No requiere cambiar la infraestructura física de los centros: opera en la nube y se accede desde cualquier smartphone o computadora actual.",
         BLUE_ACCENT),
        ("📈 Impacto en Calidad Educativa", 
         "Cero minutos perdidos por fallas o dobles apartados de aulas; certeza absoluta para profesores, alumnos y directivos.",
         NAVY)
    ]
    
    for idx, (tit, desc, col) in enumerate(conclusions):
        y = Inches(1.6 + idx * 1.7)
        card = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), y, Inches(11.7), Inches(1.4))
        card.fill.solid()
        card.fill.fore_color.rgb = WHITE
        card.line.color.rgb = BORDER_COLOR
        
        tf = card.text_frame
        tf.word_wrap = True
        
        pt = tf.paragraphs[0]
        pt.text = tit
        pt.font.bold = True
        pt.font.size = Pt(14)
        pt.font.color.rgb = col
        pt.space_after = Pt(4)
        
        pd = tf.add_paragraph()
        pd.text = desc
        pd.font.size = Pt(12)
        pd.font.color.rgb = DARK_TEXT

    add_notes(s10, "TIEMPO: 9:15 - 9:45 (30 segundos)\n"
                  "GUIÓN: En conclusión, SIGRE es un proyecto de inversión que protege el patrimonio institucional, dignifica la labor del personal operativo y eleva la calidad académica. Su costo de implementación es insignificante comparado con los cientos de miles de pesos que hoy se pierden en el modelo analógico. Muchas gracias.")

    # =========================================================================
    # DIAPOSITIVA 11: REFERENCIAS BIBLIOGRÁFICAS APA (9:45 - 10:00)
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    set_slide_background(s11, LIGHT_BG)
    add_header(s11, "Referencias Bibliográficas (Norma APA 7ma Edición)")
    
    ref_card = s11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(11.7), Inches(5.2))
    ref_card.fill.solid()
    ref_card.fill.fore_color.rgb = WHITE
    ref_card.line.color.rgb = BORDER_COLOR
    
    tfr = ref_card.text_frame
    tfr.word_wrap = True
    
    refs = [
        "Asociación Nacional de Universidades e Instituciones de Educación Superior. (2023). Anuario estadístico de la educación superior 2022-2023. ANUIES. http://www.anuies.mx/informacion-y-servicios/informacion-estadistica-de-educacion-superior",
        "Banco Interamericano de Desarrollo. (2020). Metodología del marco lógico para la planificación, el seguimiento y la evaluación de proyectos del BID. Sector de Conocimiento y Aprendizaje del BID. https://publications.iadb.org/es/metodologia-del-marco-logico",
        "Cámara de Diputados del H. Congreso de la Unión. (2017). Ley general de protección de datos personales en posesión de sujetos obligados. Diario Oficial de la Federación. https://www.diputados.gob.mx/LeyesBiblio/pdf/LGPDPPSO.pdf",
        "Centro Universitario de Tonalá. (2023). Plan de desarrollo de CUTonalá 2019-2025: Visión 2030. Universidad de Guadalajara. http://www.cutonala.udg.mx/transparencia/pdi",
        "Comisión Económica para América Latina y el Caribe. (2015). Metodología del marco lógico para la planificación, el seguimiento y la evaluación de proyectos y programas (Serie Manuales N° 68). CEPAL / Naciones Unidas. https://www.cepal.org/es/publicaciones/5618-metodologia-marco-logico",
        "Coordinación General de Planeación y Evaluación. (2024). Numeralia institucional de la Red Universitaria. Universidad de Guadalajara. http://www.cgpe.udg.mx/numeralia",
        "Universidad de Guadalajara. (2019). Reglamento de adquisiciones, arrendamientos y contratación de servicios de la Universidad de Guadalajara. Gaceta de la Universidad de Guadalajara. http://www.secgen.udg.mx/normatividad/reglamentos"
    ]
    
    for idx, r in enumerate(refs):
        p = tfr.paragraphs[0] if idx == 0 else tfr.add_paragraph()
        p.text = f"• {r}"
        p.font.size = Pt(10)
        p.font.color.rgb = DARK_TEXT
        p.space_after = Pt(4)

    add_notes(s11, "TIEMPO: 9:45 - 10:00 (15 segundos)\n"
                  "GUIÓN: Presentamos las fuentes formales consultadas en estricto formato APA 7ma edición que dan sustento teórico, jurídico y estadístico a nuestra investigación. Quedamos a su disposición para la sesión de preguntas.")

    # Guardar
    out_dir = r"c:\Users\erfierro\Documents\Inversion\docs"
    os.makedirs(out_dir, exist_ok=True)
    out_pptx = os.path.join(out_dir, "Presentacion_Problematica_SIGRE.pptx")
    prs.save(out_pptx)
    print(f"Presentation saved successfully at: {out_pptx}")

if __name__ == "__main__":
    create_presentation()
