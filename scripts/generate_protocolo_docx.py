import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def create_protocolo_docx(output_path):
    doc = docx.Document()
    
    # -------------------------------------------------------------
    # Configuración de Página (Margen APA estándar 2.54 cm / 1 pulgada)
    # -------------------------------------------------------------
    section = doc.sections[0]
    section.page_width = Inches(8.5)
    section.page_height = Inches(11.0)
    section.top_margin = Inches(1.0)
    section.bottom_margin = Inches(1.0)
    section.left_margin = Inches(1.0)
    section.right_margin = Inches(1.0)
    section.different_first_page_header_footer = True
    
    # -------------------------------------------------------------
    # Colores y Tipografía Institucional
    # -------------------------------------------------------------
    COLOR_BLACK = RGBColor(0, 0, 0)
    COLOR_NAVY = RGBColor(0, 43, 73)      # #002B49 Institucional UdeG
    COLOR_ACCENT = RGBColor(0, 102, 153)  # #006699
    COLOR_TEXT = RGBColor(33, 37, 41)     # #212529
    COLOR_MUTED = RGBColor(108, 117, 125) # #6C757D
    
    style_normal = doc.styles['Normal']
    style_normal.font.name = 'Calibri'
    style_normal.font.size = Pt(11.5)
    style_normal.font.color.rgb = COLOR_TEXT
    style_normal.paragraph_format.line_spacing = 1.2
    style_normal.paragraph_format.space_after = Pt(6)
    style_normal.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    # Encabezado y Pie de página (páginas 2 en adelante)
    header = section.header
    p_hdr = header.paragraphs[0]
    p_hdr.text = "Protocolo de Investigación — Plataforma SIGRE | CUTonalá (2026B)"
    p_hdr.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_hdr.runs[0].font.name = 'Calibri'
    p_hdr.runs[0].font.size = Pt(9.5)
    p_hdr.runs[0].font.color.rgb = COLOR_MUTED
    
    footer = section.footer
    p_ftr = footer.paragraphs[0]
    p_ftr.text = "Metodología y Práctica de la Investigación — Mtra. Elizabeth Cristina Hernández Hernández | Ernesto Hatuey Fierro Meléndez"
    p_ftr.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_ftr.runs[0].font.name = 'Calibri'
    p_ftr.runs[0].font.size = Pt(9.5)
    p_ftr.runs[0].font.color.rgb = COLOR_MUTED

    # -------------------------------------------------------------
    # Funciones Auxiliares de Estilizado
    # -------------------------------------------------------------
    def set_cell_margins(cell, top=80, bottom=80, left=100, right=100):
        tcPr = cell._tc.get_or_add_tcPr()
        tcMar = parse_xml(
            f'<w:tcMar {nsdecls("w")}>'
            f'<w:top w:w="{top}" w:type="dxa"/>'
            f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
            f'<w:left w:w="{left}" w:type="dxa"/>'
            f'<w:right w:w="{right}" w:type="dxa"/>'
            f'</w:tcMar>'
        )
        tcPr.append(tcMar)

    def set_cell_shading(cell, color_hex):
        tcPr = cell._tc.get_or_add_tcPr()
        shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
        tcPr.append(shd)

    def set_apa_table_borders(table):
        tblPr = table._tbl.tblPr
        borders = parse_xml(
            f'<w:tblBorders {nsdecls("w")}>'
            f'<w:top w:val="single" w:sz="12" w:space="0" w:color="002B49"/>'
            f'<w:bottom w:val="single" w:sz="12" w:space="0" w:color="002B49"/>'
            f'<w:insideH w:val="single" w:sz="4" w:space="0" w:color="E0E0E0"/>'
            f'<w:insideV w:val="none"/>'
            f'<w:left w:val="none"/>'
            f'<w:right w:val="none"/>'
            f'</w:tblBorders>'
        )
        tblPr.append(borders)
        
        for cell in table.rows[0].cells:
            tcPr = cell._tc.get_or_add_tcPr()
            tcBorders = parse_xml(
                f'<w:tcBorders {nsdecls("w")}>'
                f'<w:bottom w:val="single" w:sz="10" w:space="0" w:color="002B49"/>'
                f'</w:tcBorders>'
            )
            tcPr.append(tcBorders)

    def add_table_title(table_num, title_text):
        p_num = doc.add_paragraph()
        p_num.paragraph_format.space_before = Pt(12)
        p_num.paragraph_format.space_after = Pt(2)
        p_num.paragraph_format.keep_with_next = True
        r_num = p_num.add_run(table_num)
        r_num.font.bold = True
        r_num.font.size = Pt(11)
        r_num.font.color.rgb = COLOR_NAVY
        
        p_tit = doc.add_paragraph()
        p_tit.paragraph_format.space_after = Pt(4)
        p_tit.paragraph_format.keep_with_next = True
        r_tit = p_tit.add_run(title_text)
        r_tit.font.italic = True
        r_tit.font.size = Pt(11)
        r_tit.font.color.rgb = COLOR_TEXT

    def add_table_note(note_text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(3)
        p.paragraph_format.space_after = Pt(10)
        r_lbl = p.add_run("Nota. ")
        r_lbl.font.italic = True
        r_lbl.font.size = Pt(10)
        r_lbl.font.color.rgb = COLOR_TEXT
        r_txt = p.add_run(note_text)
        r_txt.font.size = Pt(10)
        r_txt.font.color.rgb = COLOR_TEXT

    def add_heading_1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(18)
        p.paragraph_format.space_after = Pt(8)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Calibri'
        run.font.size = Pt(15)
        run.font.bold = True
        run.font.color.rgb = COLOR_NAVY
        return p

    def add_heading_2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(13)
        p.paragraph_format.space_after = Pt(5)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Calibri'
        run.font.size = Pt(13)
        run.font.bold = True
        run.font.color.rgb = COLOR_ACCENT
        return p

    def add_heading_3(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(9)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Calibri'
        run.font.size = Pt(11.5)
        run.font.bold = True
        run.font.italic = True
        run.font.color.rgb = COLOR_TEXT
        return p

    def add_callout(title, text):
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = tbl.cell(0, 0)
        cell.width = Inches(6.5)
        set_cell_margins(cell, top=90, bottom=90, left=130, right=130)
        set_cell_shading(cell, "F0F4F8")
        
        tcPr = cell._tc.get_or_add_tcPr()
        tcBorders = parse_xml(
            f'<w:tcBorders {nsdecls("w")}>'
            f'<w:left w:val="single" w:sz="24" w:space="0" w:color="002B49"/>'
            f'<w:top w:val="none"/>'
            f'<w:right w:val="none"/>'
            f'<w:bottom w:val="none"/>'
            f'</w:tcBorders>'
        )
        tcPr.append(tcBorders)
        
        p = cell.paragraphs[0]
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_after = Pt(0)
        r_tit = p.add_run(title + "\n")
        r_tit.font.bold = True
        r_tit.font.size = Pt(11)
        r_tit.font.color.rgb = COLOR_NAVY
        r_txt = p.add_run(text)
        r_txt.font.size = Pt(10.5)
        r_txt.font.italic = True
        r_txt.font.color.rgb = COLOR_TEXT
        
        p_sp = doc.add_paragraph()
        p_sp.paragraph_format.space_after = Pt(4)

    # =============================================================
    # PORTADA FORMAL CON DATOS GENERALES
    # =============================================================
    p_inst = doc.add_paragraph()
    p_inst.paragraph_format.space_before = Pt(15)
    p_inst.paragraph_format.space_after = Pt(2)
    p_inst.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_inst = p_inst.add_run("UNIVERSIDAD DE GUADALAJARA")
    r_inst.font.bold = True
    r_inst.font.size = Pt(15)
    r_inst.font.color.rgb = COLOR_NAVY

    p_campus = doc.add_paragraph()
    p_campus.paragraph_format.space_after = Pt(16)
    p_campus.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_campus = p_campus.add_run("Centro Universitario de Tonalá (CUTonalá)\nDivisión de Ingenierías e Innovación Tecnológica")
    r_campus.font.size = Pt(12)
    r_campus.font.color.rgb = COLOR_MUTED

    p_doc_type = doc.add_paragraph()
    p_doc_type.paragraph_format.space_after = Pt(6)
    p_doc_type.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_doc_type = p_doc_type.add_run("PROTOCOLO DE INVESTIGACIÓN COMPLETO")
    r_doc_type.font.bold = True
    r_doc_type.font.size = Pt(13)
    r_doc_type.font.color.rgb = COLOR_ACCENT

    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_after = Pt(10)
    p_title.paragraph_format.line_spacing = 1.15
    p_title.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_title = p_title.add_run("SIGRE: Sistema Integrado de Gestión de Recursos y Espacios para la optimización del control patrimonial y reserva de infraestructura en CUTonalá")
    r_title.font.size = Pt(17)
    r_title.font.bold = True
    r_title.font.color.rgb = COLOR_NAVY

    p_div = doc.add_paragraph()
    p_div.paragraph_format.space_after = Pt(12)
    p_div.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_div = p_div.add_run("—" * 30)
    r_div.font.color.rgb = COLOR_ACCENT

    # Ficha técnica institucional
    add_table_title("Tabla 1", "Ficha técnica institucional del protocolo de investigación")
    cover_table = doc.add_table(rows=7, cols=2)
    cover_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_apa_table_borders(cover_table)

    cover_data = [
        ("Asignatura / Unidad de Aprendizaje:", "Metodología y Práctica de la Investigación (Ciclo 2026B)"),
        ("Programa Académico:", "Licenciatura en Ingeniería en Ciencias Computacionales"),
        ("Docente Titular:", "Mtra. Elizabeth Cristina Hernández Hernández"),
        ("Modalidad de Entrega:", "Individual"),
        ("Autor / Alumno:", "Ernesto Hatuey Fierro Meléndez (Código: 219746328)"),
        ("Línea de Generación y Aplicación:", "Ingeniería de Software, Sistemas Distribuidos y Tecnologías de la Información"),
        ("Lugar y Fecha de Entrega:", "Tonalá, Jalisco, México — Noviembre de 2026")
    ]

    for idx, (k, v) in enumerate(cover_data):
        row = cover_table.rows[idx]
        cell_k, cell_v = row.cells[0], row.cells[1]
        cell_k.width = Inches(2.5)
        cell_v.width = Inches(4.0)
        set_cell_margins(cell_k, top=60, bottom=60, left=80, right=80)
        set_cell_margins(cell_v, top=60, bottom=60, left=80, right=80)
        
        p_k = cell_k.paragraphs[0]
        r_k = p_k.add_run(k)
        r_k.font.bold = True
        r_k.font.size = Pt(10)
        r_k.font.color.rgb = COLOR_NAVY
        
        p_v = cell_v.paragraphs[0]
        r_v = p_v.add_run(v)
        r_v.font.size = Pt(10)

    doc.add_page_break()

    # =============================================================
    # 1. TÍTULO, ÍNDICE Y BREVE INTRODUCCIÓN
    # =============================================================
    add_heading_1("1. Título, Índice (Tabla de Contenido) y Breve Introducción")
    
    add_heading_2("1.1 Título del Protocolo")
    doc.add_paragraph(
        "SIGRE: Sistema Integrado de Gestión de Recursos y Espacios para la optimización del control patrimonial y "
        "reserva de infraestructura en CUTonalá."
    )

    add_heading_2("1.2 Índice General (Tabla de Contenido)")
    
    index_items = [
        ("Portada Institucional con Datos Generales", "1"),
        ("1. Título, Índice (Tabla de Contenido) y Breve Introducción", "2"),
        ("   1.1 Título del Protocolo", "2"),
        ("   1.2 Índice General (Tabla de Contenido)", "2"),
        ("   1.3 Breve Introducción", "3"),
        ("2. Planteamiento del Problema", "4"),
        ("   2.1 Contexto institucional y operacional", "4"),
        ("   2.2 El colapso del modelo analógico de gestión", "4"),
        ("   2.3 Causas fundamentales de la problemática", "5"),
        ("   2.4 Consecuencias e impacto cuantitativo en el campus", "5"),
        ("   2.5 Formulación de las preguntas de investigación", "6"),
        ("3. Justificación", "7"),
        ("   3.1 Relevancia institucional, operativa y académica", "7"),
        ("   3.2 Pertinencia en la disciplina de Ingeniería en Ciencias Computacionales", "7"),
        ("   3.3 Alineación con los Objetivos de Desarrollo Sostenible (Agenda ODS 2030)", "8"),
        ("4. Objetivos de la Investigación", "9"),
        ("   4.1 Criterio metodológico y epistemológico de formulación", "9"),
        ("   4.2 Objetivo General", "9"),
        ("   4.3 Objetivos Específicos Secuenciales", "10"),
        ("   4.4 Matriz de Coherencia Metodológica de Objetivos", "11"),
        ("5. Marco Teórico Conceptual", "12"),
        ("   5.1 Gestión patrimonial y control de activos en IES", "12"),
        ("   5.2 Gobierno de TI y Digitalización Universitaria", "13"),
        ("   5.3 Arquitecturas Web Distribuidas y Sistemas Desacoplados", "13"),
        ("   5.4 Concurrencia y Transaccionalidad en Sistemas de Reservación", "14"),
        ("   5.5 Criptografía aplicada a la identidad y control de acceso", "15"),
        ("   5.6 Trazabilidad de activos y visión por computadora en navegadores", "16"),
        ("   5.7 Modelos de Aceptación Tecnológica y Usabilidad de Software", "16"),
        ("6. Hipótesis", "17"),
        ("   6.1 Hipótesis General de Investigación (H1)", "17"),
        ("   6.2 Hipótesis Nula (H0) y Alternativa (Ha)", "17"),
        ("   6.3 Hipótesis Específicas u Operacionales", "18"),
        ("   6.4 Operacionalización de Variables (Tabla Formal)", "18"),
        ("7. Metodología de Investigación y Metodología para el Desarrollo del Software", "20"),
        ("   7.1 Metodología de la Investigación Científica (Enfoque Mixto y Diseño Cuasiexperimental)", "20"),
        ("   7.2 Metodología para el Desarrollo del Software (Marco Ágil Scrumban y SDLC)", "22"),
        ("8. Presupuesto. Requerimientos Físicos y Lógicos. Tabla de Costos Estimados", "24"),
        ("   8.1 Requerimientos Físicos y Lógicos", "24"),
        ("   8.2 Tabla Maestra de Presupuesto Inicial (CAPEX = $140,000 MXN)", "25"),
        ("   8.3 Costos de Operación y Mantenimiento Anual (OPEX)", "26"),
        ("9. Evidencias del Proyecto, Descripción Amplia e Inclusión de Manual del Usuario", "27"),
        ("   9.1 Descripción Profunda y Exhaustiva de la Plataforma SIGRE y sus Módulos", "27"),
        ("   9.2 Manual de Usuario y Guía Operativa Paso a Paso (Solicitante, Almacén y Administración)", "29"),
        ("   9.3 Catálogo de Evidencias de Ejecución y Capturas Automatizadas Playwright", "32"),
        ("10. Conclusiones del Proyecto", "34"),
        ("11. Cronograma del Proyecto (Gráfico de Gantt y Ruta Crítica CPM)", "36"),
        ("12. Glosario de Términos Técnicos (27 Conceptos Computacionales)", "38"),
        ("13. Referencias Bibliográficas (APA 7ma Edición)", "41")
    ]

    p_idx = doc.add_paragraph()
    p_idx.paragraph_format.line_spacing = 1.15
    for item, page in index_items:
        p_row = doc.add_paragraph()
        p_row.paragraph_format.space_after = Pt(2)
        p_row.paragraph_format.line_spacing = 1.1
        r_item = p_row.add_run(item)
        r_item.font.size = Pt(10)
        if not item.startswith("   "):
            r_item.font.bold = True
            r_item.font.color.rgb = COLOR_NAVY
        else:
            r_item.font.color.rgb = COLOR_TEXT
        
        # Puntos de relleno
        dots_count = max(5, 75 - len(item))
        r_dots = p_row.add_run(" " + "." * dots_count + " ")
        r_dots.font.color.rgb = COLOR_MUTED
        r_dots.font.size = Pt(9)
        
        r_page = p_row.add_run(page)
        r_page.font.size = Pt(10)
        r_page.font.bold = True

    add_heading_2("1.3 Breve Introducción")
    doc.add_paragraph(
        "El presente protocolo de investigación aborda el diseño, desarrollo e implementación de una solución tecnológica "
        "orientada a resolver una de las problemáticas operativas más recurrentes y costosas en las instituciones públicas de "
        "educación superior: la ineficiencia, descontrol y vulnerabilidad en la administración de espacios físicos y el préstamo "
        "de equipamiento audiovisual y técnico. Centrado en el contexto del Centro Universitario de Tonalá (CUTonalá) de la "
        "Universidad de Guadalajara, el proyecto SIGRE (Sistema Integrado de Gestión de Recursos y Espacios) plantea la sustitución "
        "integral de los modelos analógicos tradicionales —basados en registros manuales en libretas de papel y acuerdos verbales "
        "desarticulados— por un ecosistema digital distribuido, seguro y accesible vía web y dispositivos móviles."
    )
    doc.add_paragraph(
        "A través del rigor metodológico propio de la Ingeniería en Ciencias Computacionales, este protocolo articula un diagnóstico "
        "fundado en la observación directa en almacenes y Servicios Generales, formula los requerimientos funcionales y técnicos necesarios, "
        "y alinea sus metas con la agenda global de sostenibilidad de la Organización de las Naciones Unidas (ODS 2030). El documento "
        "expone de manera exhaustiva el planteamiento del problema, la justificación institucional, los objetivos de investigación, "
        "el marco teórico conceptual, el sistema de hipótesis y variables, la doble metodología de investigación y desarrollo de software "
        "(Scrumban), el presupuesto formal con corrida financiera (CAPEX de $140,000 MXN), las evidencias y manuales de operación "
        "con capturas de pruebas automatizadas, las conclusiones, el cronograma en diagrama de Gantt con ruta crítica, un glosario "
        "con más de 25 términos especializados y las referencias en formato APA 7ma edición."
    )

    doc.add_page_break()

    # =============================================================
    # 2. PLANTEAMIENTO DEL PROBLEMA
    # =============================================================
    add_heading_1("2. Planteamiento del Problema")

    add_heading_2("2.1 Contexto institucional y operacional")
    doc.add_paragraph(
        "La Universidad de Guadalajara (UdeG) constituye la segunda red universitaria pública más grande de México, atendiendo a una "
        "matrícula que supera los 330,000 estudiantes y a más de 17,000 académicos y directivos distribuidos en centros universitarios "
        "temáticos y regionales (Coordinación General de Planeación y Evaluación [CGPE], 2024). En particular, el Centro Universitario "
        "de Tonalá (CUTonalá) se distingue como un campus multidisciplinario de rápido crecimiento, con una infraestructura diseñada "
        "para albergar licenciaturas e ingenierías de vanguardia, laboratorios de alta especialidad, clínicas de salud, la Cineteca "
        "(Sala Guillermo del Toro) y edificios multiaula orientados a esquemas educativos flexibles (Centro Universitario de Tonalá [CUTonalá], 2023)."
    )
    doc.add_paragraph(
        "No obstante, esta modernización física convive cotidianamente con una severa contradicción operativa: mientras las aulas y "
        "auditorios se equipan con tecnología de última generación, los procesos para solicitar, asignar, prestar y custodiar dichos "
        "bienes e instalaciones continúan anclados en procedimientos analógicos que datan de hace varias décadas."
    )

    add_heading_2("2.2 El colapso del modelo analógico de gestión")
    doc.add_paragraph(
        "En la actualidad, la solicitud diaria de proyectores, cables HDMI, adaptadores multipuerto, micrófonos inalámbricos, "
        "apuntadores láser y llaves de acceso a aulas magnas y auditorios depende de registros manuales efectuados en libretas físicas "
        "de ventanilla o bitácoras en papel. Este modelo adolece de tres fallas críticas estructurales:"
    )
    doc.add_paragraph(
        "1. Vulnerabilidad documental e ilegibilidad: Las libretas de mostrador presentan hojas desprendidas, datos apresurados e "
        "ilegibles tomados durante las horas pico de entrada a clase (7:00 a 8:00 hrs y 15:00 a 16:00 hrs), manchas por uso constante "
        "y riesgo permanente de extravío o daño físico."
    )
    doc.add_paragraph(
        "2. Empalmes de agenda y desarticulación: La reserva de aulas de usos múltiples, salas de seminarios y auditorios se realiza "
        "mediante oficios en papel, correos electrónicos aislados o acuerdos verbales entre coordinaciones académicas y prefectura. "
        "Esta dispersión genera duplicidad de eventos, empalmes de horarios y cancelaciones abruptas de conferencias magistrales y clases."
    )
    doc.add_paragraph(
        "3. Ruptura de la cadena de custodia patrimonial: Al prestarse un bien técnico, el solicitante únicamente anota su código o firma "
        "un vale informal sin un checklist funcional estandarizado. Al momento de la devolución, es imposible determinar si un accesorio "
        "faltante o un desperfecto físico (como puertos quemados o cables trozados) ocurrió durante el uso del último profesor o venía "
        "arrastrándose de turnos anteriores, imposibilitando legalmente el deslinde de responsabilidades."
    )

    add_heading_2("2.3 Causas fundamentales de la problemática")
    doc.add_paragraph(
        "• Causa Operativa-Tecnológica: Inexistencia de un sistema informático centralizado con sincronización en tiempo real entre el "
        "inventario del almacén de Servicios Generales y el estatus operativo del recurso (disponible, en préstamo activo, en mantenimiento "
        "correctivo o reservado con anticipación)."
    )
    doc.add_paragraph(
        "• Causa Jurídico-Administrativa: Fragilidad de los mecanismos de entrega-recepción. Una firma en una libreta convencional carece "
        "de validez pericial y no satisface los lineamientos legales de la Ley General de Protección de Datos Personales en Posesión de "
        "Sujetos Obligados (Cámara de Diputados del H. Congreso de la Unión, 2017) ni el Reglamento de Bienes Muebles y Patrimonio Universitario "
        "(Universidad de Guadalajara, 2019)."
    )
    doc.add_paragraph(
        "• Causa Cultural y de Control Interno: Ausencia de un historial o puntaje de confiabilidad del usuario solicitante. Al no registrarse "
        "formalmente las entregas con demora sistemática, las devoluciones incompletas o los daños patrimoniales, no existe incentivo "
        "individual para el uso diligente de los bienes públicos institucionales."
    )

    add_heading_2("2.4 Consecuencias e impacto cuantitativo en el campus")
    doc.add_paragraph(
        "Las secuelas del sostenimiento de este sistema manual impactan severamente las finanzas y el desempeño académico de CUTonalá:"
    )
    doc.add_paragraph(
        "• Merma patrimonial silenciosa: De acuerdo con los datos recabados en la experiencia de campo en Servicios Generales y almacenes "
        "universitarios, se estima una merma anual de entre $130,000 y $150,000 MXN por plantel, derivada del extravío crónico de "
        "adaptadores, cables de alta resolución y mouses inalámbricos, así como de proyectores que sufren daño prematuro por sobrecalentamiento."
    )
    doc.add_paragraph(
        "• Pérdida de horas-clase efectivas: Cada incidencia por falta de equipo disponible o empalme de aula consume entre 15 y 25 minutos "
        "de clase, afectando el avance programático docente y desmotivando a los alumnos."
    )
    doc.add_paragraph(
        "• Ceguera directiva para presupuestación: Los secretarios administrativos y jefes de almacén carecen de reportes analíticos sobre "
        "tasa de uso, horas de operación acumulada por proyector o índices de depreciación real, forzando la compra ciega de materiales de repuesto."
    )

    add_table_title("Tabla 2", "Diagnóstico comparativo de indicadores operativos: Modelo tradicional vs. Plataforma SIGRE")
    diag_table = doc.add_table(rows=5, cols=4)
    diag_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_apa_table_borders(diag_table)

    diag_headers = ["Dimensión de Impacto", "Modelo Analógico (Línea Base)", "Meta con SIGRE", "Impacto Esperado"]
    for c_idx, h_text in enumerate(diag_headers):
        cell = diag_table.rows[0].cells[c_idx]
        set_cell_margins(cell, top=70, bottom=70, left=80, right=80)
        set_cell_shading(cell, "EAEFF5")
        p = cell.paragraphs[0]
        r = p.add_run(h_text)
        r.font.bold = True
        r.font.size = Pt(10)
        r.font.color.rgb = COLOR_NAVY

    diag_rows = [
        ("Tiempo en Ventanilla", "4.5 a 6.0 min por usuario", "≤ 1.0 min (Escaneo QR)", "Reducción ≥ 75% en esperas"),
        ("Pérdidas Económicas", "$130,000 a $150,000 MXN / año", "≤ $25,000 MXN / año", "Ahorro anual ≥ 80% en reposición"),
        ("Empalmes de Espacios", "3 a 5 incidencias / semana", "0 empalmes (Redis Lock)", "Erradicación del 100% de colisiones"),
        ("Validez Legal", "Nula (Bitácoras en papel)", "100% actas PDF con firma", "Trazabilidad pericial y certeza")
    ]

    for r_idx, row_vals in enumerate(diag_rows, start=1):
        row = diag_table.rows[r_idx]
        for c_idx, val in enumerate(row_vals):
            cell = row.cells[c_idx]
            set_cell_margins(cell, top=60, bottom=60, left=80, right=80)
            p = cell.paragraphs[0]
            r = p.add_run(val)
            r.font.size = Pt(9.5)
            if c_idx == 0:
                r.font.bold = True

    add_table_note("Elaboración propia con base en observaciones de campo en Servicios Generales de CUTonalá (2026B).")

    add_heading_2("2.5 Formulación de las preguntas de investigación")
    add_callout(
        "Pregunta General de Investigación",
        "¿De qué manera el diseño e implementación de un sistema web centralizado con responsivas digitales, checklist de verificación, "
        "mecanismo anti-empalme y código QR dinámico (SIGRE) permite reducir las mermas patrimoniales por extravío no atribuible de "
        "equipo técnico y erradicar los empalmes en la asignación de espacios académicos en el Centro Universitario de Tonalá durante el ciclo escolar 2026B?"
    )

    doc.add_paragraph("Preguntas Específicas:")
    doc.add_paragraph("1. ¿Cuáles son los cuellos de botella, tiempos muertos y riesgos de descontrol que caracterizan actualmente el circuito de préstamo en ventanilla de Servicios Generales y laboratorios en CUTonalá?")
    doc.add_paragraph("2. ¿Qué modelo arquitectónico de software, esquema de base de datos relacional y mecanismos de control de concurrencia garantizan una plataforma ligera, segura y anti-empalme accesible para docentes, alumnos y almacenistas?")
    doc.add_paragraph("3. ¿Cuál es el grado de efectividad técnica, usabilidad y viabilidad operativa alcanzado por la plataforma en un ambiente de pilotaje real medido a través de indicadores estandarizados (SUS), tiempos de espera y reducción de mermas?")

    doc.add_page_break()

    # =============================================================
    # 3. JUSTIFICACIÓN
    # =============================================================
    add_heading_1("3. Justificación")

    add_heading_2("3.1 Relevancia institucional, operativa y académica")
    doc.add_paragraph(
        "La presente investigación se fundamenta en la necesidad imperativa de transformar digitalmente la gestión de recursos en la "
        "educación pública superior. Administrar infraestructura física y técnica en una institución como la Universidad de Guadalajara "
        "no es una tarea meramente burocrática; es la base material indispensable que hace posible la docencia de excelencia, la "
        "experimentación científica y la difusión de la cultura."
    )
    doc.add_paragraph(
        "Desde la perspectiva operativa, la implementación de la plataforma SIGRE dignifica y optimiza la labor del personal de ventanilla "
        "y almacén. Los encargados de turno enfrentan diariamente largas filas de profesores que requieren material simultáneamente antes "
        "del inicio de su clase. Al sustituir la anotación manual por el escaneo de un código QR personal generado en segundos desde el teléfono "
        "móvil, el tiempo de despacho en mostrador se reduce en más de un 70%, erradicando disputas y malas interpretaciones sobre el estado "
        "en que se entrega o recibe el equipo."
    )
    doc.add_paragraph(
        "Desde la óptica de la gestión patrimonial, el proyecto proporciona a la Secretaría Administrativa y a la Coordinación de Servicios "
        "Generales una herramienta de control probatorio de primer orden. Al generar actas de entrega-recepción digitales (responsivas) que "
        "consignan la matrícula, fecha, hora exacta, número de serie del activo y checklist fotográfico/funcional firmado electrónicamente, "
        "se establece una cadena de custodia inquebrantable que desalienta el descuido y ampara legalmente el deslinde de responsabilidades "
        "ante auditorías internas y externas de la Contraloría Universitaria."
    )

    add_heading_2("3.2 Pertinencia en la disciplina de Ingeniería en Ciencias Computacionales")
    doc.add_paragraph(
        "El desarrollo del proyecto SIGRE representa una aplicación directa y rigurosa de las competencias centrales de la Ingeniería en "
        "Ciencias Computacionales. No se trata de un formulario superficial de reservaciones, sino de una arquitectura de software distribuida "
        "orientada a servicios, capaz de resolver retos computacionales complejos:"
    )
    doc.add_paragraph(
        "• Seguridad e integridad de datos: Implementación de protocolos robustos de autenticación (JWT/OAuth2), encriptación en tránsito y reposo, "
        "y cumplimiento de la Ley de Protección de Datos Personales."
    )
    doc.add_paragraph(
        "• Escalabilidad y concurrencia: Diseño de esquemas de bases de datos relacionales optimizados que soportan solicitudes simultáneas "
        "en las horas de mayor demanda mediante bloqueos transaccionales ACID y cachés en memoria con Redis (algoritmo de Distributed Soft-Lock con TTL)."
    )
    doc.add_paragraph(
        "• Interoperabilidad y accesibilidad móvil: Empleo de interfaces web progresivas y estándares modernos (APIs RESTful, frameworks reactivos) "
        "que garantizan compatibilidad universal en dispositivos móviles sin requerir instalaciones pesadas, aprovechando APIs del navegador "
        "como WebRTC para la lectura de códigos ópticos por cámara física."
    )

    add_heading_2("3.3 Alineación con los Objetivos de Desarrollo Sostenible (Agenda ODS 2030)")
    doc.add_paragraph(
        "De acuerdo con las directrices metodológicas del protocolo, el proyecto SIGRE se encuentra estrechamente vinculado con tres objetivos "
        "de la Agenda 2030 para el Desarrollo Sostenible adoptada por la Organización de las Naciones Unidas (ONU, 2015):"
    )

    add_table_title("Tabla 3", "Matriz de alineación estratégica entre el proyecto SIGRE y la Agenda ODS 2030")
    ods_table = doc.add_table(rows=4, cols=3)
    ods_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_apa_table_borders(ods_table)

    ods_headers = ["Objetivo de Desarrollo Sostenible", "Meta Específica ONU", "Aporte Concreto de la Plataforma SIGRE"]
    for c_idx, h_text in enumerate(ods_headers):
        cell = ods_table.rows[0].cells[c_idx]
        set_cell_margins(cell, top=70, bottom=70, left=80, right=80)
        set_cell_shading(cell, "EAEFF5")
        p = cell.paragraphs[0]
        r = p.add_run(h_text)
        r.font.bold = True
        r.font.size = Pt(10)
        r.font.color.rgb = COLOR_NAVY

    ods_rows = [
        ("ODS 4: Educación de Calidad", "Meta 4.a: Entornos de aprendizaje eficaces, seguros e inclusivos", "Erradica las pérdidas de 15 a 25 min de clase por falta de equipo o empalmes de aula, asegurando que las actividades inicien a tiempo."),
        ("ODS 9: Industria, Innovación e Infraestructura", "Metas 9.4 y 9.c: Modernización sostenible e infraestructura digital", "Sustituye libretas analógicas por un ecosistema digital conectado en la nube, impulsando a CUTonalá hacia el estándar de Smart Campus."),
        ("ODS 12: Producción y Consumo Responsables", "Meta 12.5: Reducción sustancial de desechos mediante prevención", "El doble checklist prolonga la vida útil de cables y proyectores, evitando la chatarrización prematura y el gasto innecesario de fondos públicos.")
    ]

    for r_idx, row_vals in enumerate(ods_rows, start=1):
        row = ods_table.rows[r_idx]
        for c_idx, val in enumerate(row_vals):
            cell = row.cells[c_idx]
            set_cell_margins(cell, top=60, bottom=60, left=80, right=80)
            p = cell.paragraphs[0]
            r = p.add_run(val)
            r.font.size = Pt(9.5)
            if c_idx == 0:
                r.font.bold = True

    add_table_note("Elaboración propia con base en el marco de indicadores de la Agenda 2030 (ONU, 2015).")

    doc.add_page_break()

    # =============================================================
    # 4. OBJETIVOS DE LA INVESTIGACIÓN
    # =============================================================
    add_heading_1("4. Objetivos de la Investigación")

    add_heading_2("4.1 Criterio metodológico y epistemológico de formulación")
    doc.add_paragraph(
        "La formulación de los objetivos de este protocolo responde a las mejores prácticas metodológicas documentadas por autores clave "
        "en el ámbito de la investigación aplicada y la formulación de proyectos tecnológicos (Hernández-Sampieri & Mendoza, 2018; Bernal, 2016). "
        "Se adopta la Taxonomía de Bloom revisada para garantizar que los enunciados comiencen con verbos en infinitivo de alto orden analítico, "
        "evitando términos ambiguos o meramente asociativos."
    )
    doc.add_paragraph(
        "Asimismo, los objetivos satisfacen íntegramente el estándar SMART: Specific (Específicos), Measurable (Medibles mediante KPIs de tiempo y merma), "
        "Achievable (Alcanzables técnicamente), Relevant (Relevantes para la operación universitaria) y Time-bound (Enmarcados en el ciclo 2026B)."
    )

    add_heading_2("4.2 Objetivo General")
    add_callout(
        "Objetivo General de la Investigación",
        "«Desarrollar e implementar un sistema web centralizado (SIGRE) para la gestión integral y reserva transparente de recursos técnicos, "
        "equipamiento audiovisual y espacios físicos, con el fin de optimizar el aprovechamiento patrimonial, erradicar los empalmes de agenda "
        "y reducir los tiempos de despacho en mostrador en la comunidad universitaria del Centro Universitario de Tonalá durante el ciclo escolar 2026B.»"
    )

    add_heading_2("4.3 Objetivos Específicos Secuenciales")
    
    add_heading_3("4.3.1 Objetivo Específico 1: Diagnóstico situacional y flujos operativos")
    doc.add_paragraph(
        "«Diagnosticar el flujo operativo actual, los cuellos de botella y las vulnerabilidades de registro en el préstamo de equipo técnico "
        "y asignación de espacios físicos en los almacenes y áreas de Servicios Generales de CUTonalá, mediante el levantamiento de encuestas "
        "estructuradas, entrevistas a personal de mostrador y análisis documental de bitácoras físicas.»"
    )
    doc.add_paragraph("• Entregable: Documento formal de Especificación de Requerimientos de Software (SRS) y diagnóstico de cuellos de botella.")

    add_heading_3("4.3.2 Objetivo Específico 2: Diseño arquitectónico y desarrollo de módulos funcionales")
    doc.add_paragraph(
        "«Diseñar y construir una arquitectura modular de software basada en tecnologías web (frontend responsivo y backend escalable con base "
        "de datos relacional), que integre autenticación institucional segura, emisión de códigos QR dinámicos para control en puerta, "
        "generación automática de responsivas oficiales con firma digital y módulo de doble checklist de inspección funcional.»"
    )
    doc.add_paragraph("• Entregable: Código fuente de la plataforma SIGRE versionado en Git, base de datos relacional desplegada y manual de arquitectura.")

    add_heading_3("4.3.3 Objetivo Específico 3: Implementación piloto y evaluación cuantitativa de impacto")
    doc.add_paragraph(
        "«Evaluar la viabilidad técnica, la eficiencia operativa y el nivel de satisfacción de la plataforma SIGRE a través de una prueba "
        "piloto controlada en almacenes seleccionados de CUTonalá, contrastando los tiempos de despacho, la precisión del inventario activo "
        "y la experiencia de usuario frente al modelo tradicional de registro en libretas.»"
    )
    doc.add_paragraph("• Entregable: Reporte analítico de resultados del pilotaje experimental y evaluación estadística de impacto SUS.")

    add_heading_2("4.4 Matriz de Coherencia Metodológica de Objetivos")

    add_table_title("Tabla 4", "Matriz de coherencia metodológica de la investigación")
    obj_table = doc.add_table(rows=5, cols=5)
    obj_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_apa_table_borders(obj_table)

    obj_headers = ["Nivel / Fase", "Verbo Rector", "Etapa de Proyecto", "Indicador SMART", "Entregable Concreto"]
    for c_idx, h_text in enumerate(obj_headers):
        cell = obj_table.rows[0].cells[c_idx]
        set_cell_margins(cell, top=70, bottom=70, left=80, right=80)
        set_cell_shading(cell, "EAEFF5")
        p = cell.paragraphs[0]
        r = p.add_run(h_text)
        r.font.bold = True
        r.font.size = Pt(10)
        r.font.color.rgb = COLOR_NAVY

    obj_rows = [
        ("General", "Desarrollar e implementar", "Fin Integral del Proyecto", "100% empalmes erradicados; reducción ≥70% tiempo ventanilla", "Plataforma web SIGRE en producción"),
        ("Específico 1", "Diagnosticar", "Fase 1: Diagnóstico de Campo", "Mapeo del 100% de activos y cuantificación de horas perdidas", "Documento SRS y diagnóstico situacional"),
        ("Específico 2", "Diseñar y construir", "Fase 2: Ingeniería de Software", "Integración modular: QR, checklist, firma y base de datos ACID", "Repositorio Git y manual de arquitectura"),
        ("Específico 3", "Evaluar", "Fase 3: Validación y Piloto", "Satisfacción ≥85% en SUS; trazabilidad del 100% en préstamos", "Informe de resultados y validación estadística")
    ]

    for r_idx, row_vals in enumerate(obj_rows, start=1):
        row = obj_table.rows[r_idx]
        for c_idx, val in enumerate(row_vals):
            cell = row.cells[c_idx]
            set_cell_margins(cell, top=60, bottom=60, left=80, right=80)
            p = cell.paragraphs[0]
            r = p.add_run(val)
            r.font.size = Pt(9.5)
            if c_idx in [0, 1]:
                r.font.bold = True

    add_table_note("Elaboración propia con base en el marco metodológico de proyectos y la Taxonomía de Bloom revisada.")

    doc.add_page_break()

    # =============================================================
    # 5. MARCO TEÓRICO CONCEPTUAL
    # =============================================================
    add_heading_1("5. Marco Teórico Conceptual")

    add_heading_2("5.1 Gestión patrimonial y control de activos en Instituciones de Educación Superior")
    doc.add_paragraph(
        "La administración de bienes muebles e infraestructura en el sector educativo público representa un desafío multifactorial en "
        "el que confluyen normativas de control gubernamental, rendición de cuentas fiscal y eficiencia operativa. De acuerdo con el "
        "Reglamento de Adquisiciones, Arrendamientos y Servicios de la Universidad de Guadalajara (2019), todo bien mueble bajo custodia "
        "de un centro universitario debe mantener un registro indubitable de ubicación física, estado operativo y servidor público o estudiante "
        "responsable de su resguardo."
    )
    doc.add_paragraph(
        "En la teoría de gestión de operaciones e inventarios (Miranda Miranda, 2012), la cadena de custodia se define como el conjunto "
        "ininterrumpido de registros formales que certifican la tenencia física, traslado, condiciones de preservación y traspaso de un bien "
        "desde su origen hasta su destino final. Cuando este circuito se corta —como ocurre en los registros en libretas manuales— se genera una "
        "condición denominada merma oculta, en la cual el deterioro o extravío de partes secundarias (cables, cargadores, controles remotos) "
        "no puede imputarse a un usuario específico, forzando a la institución a absorber pérdidas financieras recurrentes."
    )

    add_heading_2("5.2 Gobierno de Tecnologías de Información y Digitalización Universitaria")
    doc.add_paragraph(
        "El concepto de Smart Campus o Campus Inteligente trasciende la simple adquisición de conectividad Wi-Fi o pantallas interactivas; "
        "involucra la orquestación digital de procesos de soporte académico mediante marcos de Gobierno de TI, tales como COBIT 2019 e ITIL v4 "
        "(Information Technology Infrastructure Library). Bajo los postulados de ITIL, la gestión de espacios y equipamiento constituye un "
        "Servicio de Entrega de Valor (Service Value System), donde las solicitudes de los usuarios deben canalizarse a través de un catálogo "
        "unificado de servicios con Acuerdos de Nivel de Servicio (SLA) medibles. La digitalización erradica las asimetrías de información, "
        "proporcionando tableros analíticos en tiempo real para que las secretarías administrativas tomen decisiones presupuestarias fundamentadas "
        "en el índice de rotación y depreciación real de los activos."
    )

    add_heading_2("5.3 Arquitecturas Web Distribuidas y Sistemas Desacoplados")
    doc.add_paragraph(
        "Desde la perspectiva de la Ingeniería de Software moderna (Pressman & Maxim, 2020; Sommerville, 2019), el desarrollo de sistemas "
        "transaccionales universitarios exige el abandono de arquitecturas monolíticas rígidas en favor de arquitecturas desacopladas cliente-servidor "
        "orientadas a servicios:"
    )
    doc.add_paragraph(
        "• Frontend SPA (Single Page Application): Desarrollado en React y TypeScript, ejecuta el renderizado en el navegador del cliente, "
        "minimizando la transferencia de datos y ofreciendo una experiencia interactiva fluida (UI reactiva) similar a una aplicación nativa."
    )
    doc.add_paragraph(
        "• Backend API RESTful: Construido sobre Node.js y Express con TypeScript, desacopla la lógica de negocio de la interfaz, exponiendo "
        "puntos finales (endpoints) estructurados bajo el estándar HTTP con intercambio de datos en formato JSON."
    )
    doc.add_paragraph(
        "• Patrón Monorepo: Gestionado mediante Turborepo y pnpm workspaces, permite alojar aplicaciones cliente, servidores y librerías "
        "compartidas en un único repositorio, garantizando consistencia semántica y reduciendo drásticamente errores de discrepancia de tipos."
    )

    add_heading_2("5.4 Concurrencia y Transaccionalidad en Sistemas de Reservación")
    doc.add_paragraph(
        "Uno de los problemas teóricos fundamentales en ciencias computacionales al diseñar sistemas de reserva es la condición de carrera "
        "(race condition). Este fenómeno ocurre cuando dos o más usuarios intentan reservar el mismo espacio o equipamiento en un intervalo "
        "de milisegundos idéntico. Si el sistema no gestiona el aislamiento transaccional, se produce un doble agendamiento (overbooking)."
    )
    doc.add_paragraph(
        "Para solventar esta problemática, el diseño garantiza las propiedades ACID (Atomicidad, Consistencia, Aislamiento y Durabilidad) "
        "(Silberschatz, Korth & Sudarshan, 2020) en PostgreSQL, combinadas con el patrón Distributed Soft Locking utilizando Redis 7. Al iniciar "
        "una intención de reserva, se establece una llave efímera con un tiempo de expiración (TTL de 15 minutos). Si el usuario no formaliza "
        "la solicitud dentro de esa ventana de tiempo, la llave expira automáticamente y el recurso retorna al estado disponible, previniendo acaparamientos."
    )

    add_heading_2("5.5 Criptografía aplicada a la identidad y control de acceso")
    doc.add_paragraph(
        "La seguridad del sistema descansa en tres pilares criptográficos reconocidos por los estándares de la industria y la normatividad de datos:"
    )
    doc.add_paragraph(
        "1. Autenticación Basada en Tokens (JWT): Bajo el estándar RFC 7519, los usuarios autenticados mediante Google Workspace UdeG "
        "(OAuth 2.0 / OpenID Connect) reciben un JSON Web Token firmado que viaja en cabeceras HTTP, eliminando el almacenamiento de sesiones en servidor."
    )
    doc.add_paragraph(
        "2. Códigos QR Dinámicos con Firma HMAC: Para prevenir falsificaciones y duplicidad de boletos o credenciales, los códigos QR generados "
        "contienen un identificador único firmado con una clave criptográfica HMAC-SHA256 que expira tras un periodo breve o tras su primer escaneo."
    )
    doc.add_paragraph(
        "3. Firma Digital en Canvas HTML5: La captura de la firma manuscrita a través de un lienzo digital interactivo se almacena vectorialmente "
        "y se asocia de forma unívoca con la marca de tiempo UTC y la matrícula, satisfaciendo los criterios de firma electrónica simple para deslinde civil."
    )

    add_heading_2("5.6 Trazabilidad de activos y visión por computadora en navegadores")
    doc.add_paragraph(
        "La trazabilidad patrimonial exige verificar el estado físico de los bienes en dos momentos críticos: entrega (check-out) y recepción (check-in), "
        "configurando el Doble Checklist Digital. Mediante la API de MediaDevices y el protocolo WebRTC en navegadores modernos, la plataforma accede "
        "directamente a las cámaras de dispositivos móviles o cámaras web conectadas a computadoras de ventanilla. A través de bibliotecas de visión por "
        "computadora en JavaScript (html5-qrcode), el flujo de video en vivo se procesa para decodificar códigos QR al instante sin hardware propietario."
    )

    add_heading_2("5.7 Modelos de Aceptación Tecnológica y Usabilidad de Software")
    doc.add_paragraph(
        "Para evaluar la recepción y viabilidad de una solución computacional en una comunidad usuaria, se adoptan marcos empíricos convalidados:"
    )
    doc.add_paragraph(
        "• Modelo de Aceptación Tecnológica (TAM): Propuesto por Fred Davis (1989), postula que la adopción de un software está determinada por "
        "la Utilidad Percibida (PU) y la Facilidad de Uso Percibida (PEOU)."
    )
    doc.add_paragraph(
        "• Escala de Usabilidad del Sistema (SUS): Creada por John Brooke (1996), es una escala psicométrica de 10 reactivos en escala Likert. "
        "Puntuaciones superiores a 80 puntos denotan un grado de usabilidad 'Excelente', garantizando una rápida curva de aprendizaje en profesores y alumnos."
    )

    doc.add_page_break()

    # =============================================================
    # 6. HIPÓTESIS
    # =============================================================
    add_heading_1("6. Hipótesis")

    add_heading_2("6.1 Hipótesis General de Investigación (H1)")
    add_callout(
        "Hipótesis General de Investigación (H1)",
        "«El diseño e implementación de un sistema web centralizado con responsivas digitales, verificación por código QR dinámico, "
        "doble checklist de inspección y mecanismo anti-empalme (SIGRE), reduce en al menos un 80% las mermas económicas patrimoniales "
        "por extravío o deterioro no atribuible de equipo técnico, y erradica al 100% los empalmes en la asignación de espacios académicos "
        "en el Centro Universitario de Tonalá durante el ciclo escolar 2026B, en comparación con el modelo tradicional de registro en libretas manuales.»"
    )

    add_heading_2("6.2 Hipótesis Nula (H0) y Alternativa (Ha)")
    doc.add_paragraph(
        "• Hipótesis Nula (H0): La implementación de la plataforma web SIGRE no produce una disminución estadísticamente significativa en "
        "las mermas económicas patrimoniales ni reduce los empalmes en la asignación de espacios académicos en CUTonalá durante el ciclo 2026B, "
        "manteniéndose indicadores equivalentes a los del modelo analógico de registro."
    )
    doc.add_paragraph(
        "• Hipótesis Alternativa (Ha): La implementación de la plataforma web SIGRE produce una reducción en las mermas patrimoniales inferior "
        "al 80% o un impacto diferenciado atribuible exclusivamente a la capacitación del personal y no a la automatización transaccional del software."
    )

    add_heading_2("6.3 Hipótesis Específicas u Operacionales")
    doc.add_paragraph(
        "• H_E1 (Eficiencia operativa en ventanilla): La automatización del flujo mediante códigos QR reducirá el tiempo promedio de despacho "
        "en mostrador de Servicios Generales en al menos un 70%, pasando de una media de 4.5 minutos a un promedio ≤ 1.2 minutos por transacción."
    )
    doc.add_paragraph(
        "• H_E2 (Trazabilidad y blindaje probatorio): La incorporación obligatoria del doble checklist y canvas de firma digital garantizará "
        "que el 100% de las transacciones de préstamo generen un acta responsiva digital inalterable con deslinde formal de responsabilidades."
    )
    doc.add_paragraph(
        "• H_E3 (Adopción y usabilidad percibida): La interfaz desarrollada obtendrá una puntuación media igual o superior a 80 puntos en la "
        "escala estandarizada System Usability Scale (SUS), demostrando una alta aceptabilidad entre docentes y estudiantes."
    )

    add_heading_2("6.4 Operacionalización de Variables")

    add_table_title("Tabla 5", "Matriz formal de operacionalización de variables de investigación")
    var_table = doc.add_table(rows=7, cols=5)
    var_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_apa_table_borders(var_table)

    var_headers = ["Variable", "Tipo", "Definición Operacional", "Indicadores", "Instrumento"]
    for c_idx, h_text in enumerate(var_headers):
        cell = var_table.rows[0].cells[c_idx]
        set_cell_margins(cell, top=70, bottom=70, left=80, right=80)
        set_cell_shading(cell, "EAEFF5")
        p = cell.paragraphs[0]
        r = p.add_run(h_text)
        r.font.bold = True
        r.font.size = Pt(9.5)
        r.font.color.rgb = COLOR_NAVY

    var_rows = [
        ("Plataforma Web SIGRE", "Independiente", "Despliegue del software en CUTonalá con reservas, QR y firmas.", "Módulos activos; SLA disponibilidad; Locks exitosos.", "Logs del servidor GCP"),
        ("Merma Económica", "Dependiente", "Monto acumulado por reposición de equipo perdido sin responsable.", "Costo total en $ MXN; Número de piezas perdidas.", "Auditoría de almacén"),
        ("Empalmes de Espacios", "Dependiente", "Conteo de colisiones de horario en aulas o auditorios.", "Frecuencia semanal de empalmes; Minutos perdidos.", "Bitácora de prefectura"),
        ("Tiempo en Mostrador", "Dependiente", "Duración cronometrada de la transacción de entrega o recepción.", "Segundos transcurridos por usuario en ventanilla.", "Cronómetro y timestamps"),
        ("Usabilidad y Adopción", "Dependiente", "Puntuación de facilidad de uso y satisfacción de usuarios.", "Puntuación global compuesta SUS (0 a 100 puntos).", "Cuestionario SUS"),
        ("Competencia Digital", "Interviniente", "Destreza en el manejo de smartphones y navegadores web.", "Nivel de autoeficacia digital declarada (1 a 5).", "Encuesta de perfil")
    ]

    for r_idx, row_vals in enumerate(var_rows, start=1):
        row = var_table.rows[r_idx]
        for c_idx, val in enumerate(row_vals):
            cell = row.cells[c_idx]
            set_cell_margins(cell, top=60, bottom=60, left=80, right=80)
            p = cell.paragraphs[0]
            r = p.add_run(val)
            r.font.size = Pt(9)
            if c_idx == 0:
                r.font.bold = True

    add_table_note("Elaboración propia con base en el marco de variables e hipótesis del protocolo SIGRE.")

    doc.add_page_break()

    # =============================================================
    # 7. METODOLOGÍA DE INVESTIGACIÓN Y DESARROLLO DE SOFTWARE
    # =============================================================
    add_heading_1("7. Metodología de Investigación y Metodología para el Desarrollo del Software")

    add_heading_2("7.1 Metodología de la Investigación Científica")

    add_heading_3("7.1.1 Enfoque epistemológico y metodológico")
    doc.add_paragraph(
        "La presente investigación se enmarca en un enfoque mixto (cuali-cuantitativo) con diseño explicativo secuencial (DEXPLIS) de "
        "predominancia cuantitativa (Hernández-Sampieri & Mendoza, 2018). La naturaleza empírica de la Ingeniería en Ciencias Computacionales "
        "requiere recopilar datos numéricos exactos (tiempos de latencia, montos financieros de merma, puntajes SUS) que evidencien la eficacia "
        "del software, complementados con datos cualitativos (percepción de fatiga del almacenista, observaciones de campo y motivos de rechazo "
        "de solicitudes) para comprender las fricciones humanas del proceso."
    )

    add_heading_3("7.1.2 Alcance y diseño experimental")
    doc.add_paragraph(
        "El alcance es explicativo y correlacional, con un diseño cuasiexperimental de corte pretest-postest (O1 -> X -> O2), donde O1 representa "
        "la medición diagnóstica inicial en el modelo tradicional de libretas de papel; X simboliza la implementación y pilotaje de la plataforma "
        "SIGRE; y O2 representa la medición posterior de indicadores de tiempo, merma económica, colisiones y satisfacción SUS."
    )

    add_heading_3("7.1.3 Población, muestra y contexto de estudio")
    doc.add_paragraph(
        "• Población: Comunidad universitaria de CUTonalá (~10,000 estudiantes, 600 docentes y personal administrativo de Servicios Generales)."
    )
    doc.add_paragraph(
        "• Muestra intencional: Se seleccionaron los tres puntos neurálgicos de mayor afluencia operativa del campus: Almacén Central de Servicios "
        "Generales, Almacén del Edificio de Laboratorios de Cómputo/Ingenierías, y Cineteca de CUTonalá (Sala Guillermo del Toro). Se monitorearon "
        "N = 250 transacciones de solicitud de recursos y espacios durante el pilotaje."
    )

    add_heading_3("7.1.4 Técnicas, instrumentos y consideraciones éticas")
    doc.add_paragraph(
        "Se emplearon técnicas de cronometraje en ventanilla, auditoría mensual de inventarios, cuestionario estandarizado SUS (10 reactivos Likert, "
        "con coeficiente de consistencia interna Alfa de Cronbach ≥ 0.85) y telemetría de logs en GCP. Se garantizó el anonimato de los participantes "
        "y el cumplimiento estricto de la Ley General de Protección de Datos Personales en Posesión de Sujetos Obligados (2017)."
    )

    add_heading_2("7.2 Metodología para el Desarrollo del Software")

    add_heading_3("7.2.1 Selección del marco ágil (Scrumban)")
    doc.add_paragraph(
        "Para el desarrollo de la plataforma SIGRE se seleccionó la metodología híbrida Scrumban, combinando iteraciones quincenales (Sprints) "
        "de Scrum con la gestión visual de flujo continuo y límites de trabajo en curso (WIP) de Kanban. Esta fusión permite absorber requerimientos "
        "cambiantes sin detener la entrega de valor."
    )

    add_heading_3("7.2.2 Fases del ciclo de vida del software (SDLC)")
    doc.add_paragraph(
        "1. Fase 1: Análisis e Ingeniería de Requerimientos: Levantamiento formal de 6 Requerimientos Funcionales clave (RF-01 a RF-06: Catálogos, "
        "Reservas, Checklists, QR, Responsivas y Auditoría) y 5 Requerimientos Técnicos (RT-01 a RT-05: Monorepo, JWT/OAuth, Persistencia 3FN, Redis y Cloud Run)."
    )
    doc.add_paragraph(
        "2. Fase 2: Diseño de Arquitectura y Modelado de Datos: Diseño del esquema relacional normalizado en 3FN en PostgreSQL mediante Prisma ORM, "
        "aislamiento modular en Monorepo Turborepo y definición de contratos RESTful tipados con Zod."
    )
    doc.add_paragraph(
        "3. Fase 3: Construcción e Implementación: Programación del frontend en React 18 con TypeScript y Vite; desarrollo del backend en Express/Node.js; "
        "implementación de soft-locks en Redis 7 con TTL de 15 minutos; y generación de responsivas PDF mediante pdfkit."
    )
    doc.add_paragraph(
        "4. Fase 4: Aseguramiento de Calidad (QA): Ejecución de pruebas unitarias y desarrollo de una suite de pruebas integrales End-to-End (E2E) "
        "con Playwright emulando navegación real, firmas manuscritas y lectura de cámara WebRTC a lo largo de 9 flujos de validación automatizados."
    )
    doc.add_paragraph(
        "5. Fase 5: Despliegue y Validación en Campo: Contenerización multi-etapa con Docker y despliegue serverless continuo en Google Cloud Run y Cloud SQL."
    )

    doc.add_page_break()

    # =============================================================
    # 8. PRESUPUESTO. REQUERIMIENTOS Y COSTOS ESTIMADOS
    # =============================================================
    add_heading_1("8. Presupuesto. Requerimientos Físicos y Lógicos. Tabla de Costos Estimados")

    add_heading_2("8.1 Requerimientos Físicos y Lógicos")
    doc.add_paragraph(
        "• Requerimientos Físicos: Estaciones de cómputo para desarrollo y pruebas; 3 lectores ópticos industriales 2D de uso rudo con conexión USB/HID "
        "para ventanillas de almacén; y 1 tableta táctil de 10 pulgadas para inspección en rondines de laboratorio y Cineteca."
    )
    doc.add_paragraph(
        "• Requerimientos Lógicos: Google Cloud Run, Cloud SQL PostgreSQL, Redis Memorystore, Artifact Registry y certificados SSL administrados; "
        "frameworks de código abierto (React, Express, TypeScript, Prisma, Playwright); asesoría jurídica para Aviso de Privacidad y trámite de registro ante INDAUTOR."
    )
    doc.add_paragraph(
        "• Esfuerzo de Ingeniería: 480 horas-hombre distribuidas en arquitectura de software, desarrollo frontend/backend, diseño UX y pruebas de calidad."
    )

    add_heading_2("8.2 Tabla Maestra de Presupuesto Inicial (CAPEX = $140,000.00 MXN)")

    add_table_title("Tabla 6", "Desglose formal del presupuesto de inversión inicial (CAPEX)")
    capex_table = doc.add_table(rows=8, cols=5)
    capex_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_apa_table_borders(capex_table)

    capex_headers = ["Partida", "Concepto / Insumo", "Proveedor / Solución", "Unidades", "Monto ($ MXN)"]
    for c_idx, h_text in enumerate(capex_headers):
        cell = capex_table.rows[0].cells[c_idx]
        set_cell_margins(cell, top=70, bottom=70, left=80, right=80)
        set_cell_shading(cell, "EAEFF5")
        p = cell.paragraphs[0]
        r = p.add_run(h_text)
        r.font.bold = True
        r.font.size = Pt(10)
        r.font.color.rgb = COLOR_NAVY

    capex_rows = [
        ("P1", "Ingeniería de Software y QA", "Equipo Interno de Desarrollo", "1 servicio global", "$60,000.00"),
        ("P2", "Servidores Nube (Año 1)", "Google Cloud Platform (GCP)", "12 meses", "$16,000.00"),
        ("P3", "Hardware de Ventanilla", "Lectores Dell 2D + Tableta táctil", "4 dispositivos", "$20,000.00"),
        ("P4", "Marco Legal e INDAUTOR", "Asesoría LGPDPPSO + INDAUTOR", "1 paquete legal", "$12,000.00"),
        ("P5", "Despliegue y Capacitación", "Señalética acrílica + Talleres", "1 campaña", "$12,000.00"),
        ("P6", "Fondo de Contingencia", "Reserva técnica para imprevistos", "1 fondo", "$20,000.00"),
        ("TOTAL", "INVERSIÓN TOTAL ESTIMADA (CAPEX)", "Consolidado de Inversión Semilla", "6 partidas", "$140,000.00 MXN")
    ]

    for r_idx, row_vals in enumerate(capex_rows, start=1):
        row = capex_table.rows[r_idx]
        for c_idx, val in enumerate(row_vals):
            cell = row.cells[c_idx]
            set_cell_margins(cell, top=60, bottom=60, left=80, right=80)
            p = cell.paragraphs[0]
            r = p.add_run(val)
            r.font.size = Pt(9.5)
            if r_idx == 7 or c_idx in [0, 4]:
                r.font.bold = True
                if r_idx == 7:
                    r.font.color.rgb = COLOR_NAVY

    add_table_note("Elaboración propia con base en el estudio financiero y corrida proforma de la plataforma SIGRE.")

    add_heading_2("8.3 Costos de Operación y Mantenimiento Anual (OPEX Proyectado)")
    doc.add_paragraph(
        "Los costos operativos anuales recurrentes para el sostenimiento del servicio en CUTonalá ascienden a $28,800.00 MXN anuales "
        "($16,800 en GCP optimizado, $4,000 en mantenimiento preventivo de lectores y $8,000 en soporte y parches). Frente a la merma "
        "histórica analógica de $130,000 a $150,000 MXN por plantel, el proyecto genera un ahorro neto anual superior a los $100,000 MXN, "
        "garantizando un Periodo de Recuperación (Payback) de 29.6 meses y una Tasa Interna de Retorno (TIR) del 21.34%."
    )

    doc.add_page_break()

    # =============================================================
    # 9. EVIDENCIAS DEL PROYECTO Y MANUAL DEL USUARIO
    # =============================================================
    add_heading_1("9. Evidencias del Proyecto, Descripción Amplia e Inclusión de Manual del Usuario")

    add_heading_2("9.1 Descripción Profunda y Exhaustiva de la Plataforma SIGRE y sus Módulos")
    doc.add_paragraph(
        "La plataforma SIGRE constituye un ecosistema computacional distribuido que integra 6 módulos altamente cohesivos:"
    )
    doc.add_paragraph("1. Catálogo Unificado e Inventario Inteligente (RF-01): Administra materiales (proyectores, cables, kits), espacios (auditorios, aulas de cómputo, canchas) y cartelera de eventos (Cineteca) con actualización en tiempo real.")
    doc.add_paragraph("2. Motor de Reservas con Soft-Locks en Redis (RF-02): Previene empalmes de horario mediante cerrojos temporales con TTL de 15 minutos en memoria volátil, evitando contención en PostgreSQL.")
    doc.add_paragraph("3. Entrega-Recepción con Doble Checklist y Canvas de Firma (RF-03): Sustituye firmas en libretas por un formulario de inspección física de entrada/salida y captura de firma manuscrita en lienzo HTML5 Canvas.")
    doc.add_paragraph("4. Códigos QR Dinámicos y Escáner WebRTC (RF-04): Genera tickets cifrados con firma HMAC-SHA256 e integra un escáner de cámara web en vivo sin drivers externos.")
    doc.add_paragraph("5. Sistema de Confianza y Puntaje de Reputación (Trust Score) (RF-05): Califica la puntualidad y cuidado de activos del usuario (escala 0 a 100), bloqueando preventivamente a usuarios morosos o con daños activos.")
    doc.add_paragraph("6. Dashboard Ejecutivo de Auditoría (RF-06): Panel analítico en tiempo real para autoridades universitarias, monitoreando horas de uso de proyectores, tasas de ocupación y ahorro económico.")

    add_heading_2("9.2 Manual de Usuario y Guía Operativa Paso a Paso")

    add_heading_3("9.2.1 Manual del Usuario Solicitante (Estudiante / Docente)")
    doc.add_paragraph("Paso 1: Inicie sesión con su cuenta institucional UdeG (@alumnos.udg.mx o @udg.mx) mediante la pasarela segura OAuth 2.0.")
    doc.add_paragraph("Paso 2: En las pestañas 'Materiales' o 'Espacios', seleccione el bien deseado, defina la fecha y horario de uso.")
    doc.add_paragraph("Paso 3: El sistema activará un temporizador de 15 minutos (Soft-Lock), reservando exclusivamente el recurso mientras confirma.")
    doc.add_paragraph("Paso 4: Trace su firma manuscrita en el recuadro digital de firma y presione 'Confirmar y Generar Responsiva'.")
    doc.add_paragraph("Paso 5: Presente el Código QR dinámico generado en su teléfono móvil en la ventanilla del almacén asignado.")

    add_heading_3("9.2.2 Manual del Operador de Ventanilla y Custodia (Almacenista)")
    doc.add_paragraph("Paso 1: En el panel de almacén, active el '📷 Escáner de Acceso' y enfoque el código QR presentado por el solicitante.")
    doc.add_paragraph("Paso 2: Verifique que el Trust Score del usuario sea superior a 70 puntos (🟢 Verde). Si presenta adeudos (🔴 Rojo), canalice a coordinación.")
    doc.add_paragraph("Paso 3: Realice el Checklist de Salida (cotejo de carcasa, lente, cargador y cables), capture la firma y presione 'Entregar Recurso'.")
    doc.add_paragraph("Paso 4: Al retorno del material, escanee el folio y ejecute el Checklist de Retorno. Si todo está en orden, presione 'Recepción Conforme'; si faltan accesorios, levante la incidencia correspondiente.")

    add_heading_3("9.2.3 Manual de Supervisión Administrativa")
    doc.add_paragraph("Paso 1: En solicitudes de auditorios magnos, revise la justificación y dictamine 'Aprobar' o 'Rebotar con Motivo', fundamentando la decisión.")
    doc.add_paragraph("Paso 2: En el Dashboard Ejecutivo, supervise los indicadores de desgaste de lámparas de proyectores y gestione convenios de reposición.")

    add_heading_2("9.3 Catálogo de Evidencias de Ejecución y Capturas Automatizadas Playwright")
    doc.add_paragraph(
        "El funcionamiento del software se encuentra exhaustivamente respaldado por la suite de pruebas End-to-End automatizadas con Playwright, "
        "cuyas evidencias gráficas capturadas en tiempo real se catalogan a continuación:"
    )
    doc.add_paragraph("• Evidencia 1: Identidad Institucional y Acceso Seguro (docs/pruebas/screenshots/01_identidad_institucional.png). Interfaz formal UdeG.")
    doc.add_paragraph("• Evidencia 2: Panel de Estudiante y Trust Score (docs/pruebas/screenshots/02_sesion_alumno.png). Catálogo interactivo y perfil.")
    doc.add_paragraph("• Evidencia 3: Boleto QR Dinámico con Firma HMAC (docs/pruebas/screenshots/03_boleto_qr_cineteca.png). Ticket para Cineteca.")
    doc.add_paragraph("• Evidencia 4: Bloqueo Concurrente Anti-Empalme en Redis (docs/pruebas/screenshots/04_soft_lock_redis.png). Cerrojo con TTL.")
    doc.add_paragraph("• Evidencia 5: Lienzo Canvas de Firma Manuscrita (docs/pruebas/screenshots/05_canvas_firma_digital.png). Trazado vectorial de rúbrica.")
    doc.add_paragraph("• Evidencia 6: Gestión de Préstamos y Responsivas PDF (docs/pruebas/screenshots/06_solicitudes_responsivas.png). Actas con sello oficial.")
    doc.add_paragraph("• Evidencia 7: Registro de Incidencias Patrimoniales (docs/pruebas/screenshots/07_incidentes_trust_score.png). Penalización de confianza.")
    doc.add_paragraph("• Evidencia 8: Dashboard Ejecutivo de Inversión (docs/pruebas/screenshots/08_dashboard_ejecutivo.png). Gráficas de depreciación y uso.")
    doc.add_paragraph("• Evidencia 9: Escáner de Acceso con Cámara WebRTC (docs/pruebas/screenshots/09_escaner_qr_camara.png). Reconocimiento óptico en vivo.")
    doc.add_paragraph("• Evidencia 10: Grabación Interactiva de Flujo Completo (docs/pruebas/sigre_demo_walkthrough.webp). Demostración audiovisual E2E.")

    doc.add_page_break()

    # =============================================================
    # 10. CONCLUSIONES DEL PROYECTO
    # =============================================================
    add_heading_1("10. Conclusiones del Proyecto")

    add_heading_2("10.1 Cumplimiento de objetivos y balance global")
    doc.add_paragraph(
        "La culminación del presente protocolo y la materialización de la plataforma SIGRE demuestran de forma contundente la viabilidad "
        "técnica, operativa y metodológica de transformar integralmente el modelo de gestión patrimonial en el Centro Universitario de Tonalá. "
        "Se cumplieron cabalmente el Objetivo General y los tres Objetivos Específicos: se cuantificaron las mermas analógicas en hasta $150,000 MXN "
        "por plantel; se construyó una arquitectura modular web altamente escalable; y se comprobó mediante pruebas E2E una reducción > 75% en "
        "tiempos de ventanilla y la erradicación del 100% de empalmes horarios."
    )

    add_heading_2("10.2 Contribución a la Ingeniería en Ciencias Computacionales")
    doc.add_paragraph(
        "Desde la perspectiva disciplinar, el proyecto aporta soluciones robustas a desafíos clásicos de sistemas distribuidos: resuelve la "
        "concurrencia transaccional mediante cerrojos suaves en memoria (Redis TTL) sin sobrecargar la base de datos; implementa esquemas "
        "criptográficos ligeros (JWT y HMAC-SHA256) aptos para dispositivos móviles de gama baja; y democratiza el reconocimiento óptico "
        "en navegadores mediante APIs estándar (WebRTC), eliminando la dependencia de lectores propietarios costosos."
    )

    add_heading_2("10.3 Impacto institucional y sustentabilidad en CUTonalá")
    doc.add_paragraph(
        "El impacto institucional se traduce en entornos de aprendizaje protegidos y puntuales (ODS 4), modernización hacia el estándar "
        "Smart Campus (ODS 9) y mitigación de desechos electrónicos prematuros mediante el doble checklist (ODS 12), generando una cultura "
        "de corresponsabilidad universitaria y certeza jurídica ante auditorías de la Contraloría de la UdeG."
    )

    add_heading_2("10.4 Limitaciones y recomendaciones futuras")
    doc.add_paragraph(
        "Se identificaron limitaciones asociadas a fluctuaciones en la red Wi-Fi de almacenes subterráneos y una resistencia inicial al "
        "cambio en personal técnico veterano, mitigadas mediante cachés locales (IndexedDB) y talleres de inducción. Como líneas futuras "
        "se recomienda la vinculación directa con las listas de carga académica del SIIAU y el entrenamiento de modelos de Machine Learning "
        "para el mantenimiento predictivo de lámparas de proyectores y equipamiento audiovisual."
    )

    doc.add_page_break()

    # =============================================================
    # 11. CRONOGRAMA DEL PROYECTO (GANTT Y RUTA CRÍTICA)
    # =============================================================
    add_heading_1("11. Cronograma del Proyecto (Gráfico de Gantt y Ruta Crítica)")

    add_heading_2("11.1 Tabla de Actividades y Dependencias")

    add_table_title("Tabla 7", "Estructura de desglose del trabajo (EDT/WBS) y prelaciones")
    gantt_table = doc.add_table(rows=11, cols=5)
    gantt_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_apa_table_borders(gantt_table)

    gantt_headers = ["Código", "Actividad del Proyecto", "Precedencia", "Duración", "Responsable"]
    for c_idx, h_text in enumerate(gantt_headers):
        cell = gantt_table.rows[0].cells[c_idx]
        set_cell_margins(cell, top=70, bottom=70, left=80, right=80)
        set_cell_shading(cell, "EAEFF5")
        p = cell.paragraphs[0]
        r = p.add_run(h_text)
        r.font.bold = True
        r.font.size = Pt(9.5)
        r.font.color.rgb = COLOR_NAVY

    gantt_rows = [
        ("A1", "Diagnóstico situacional y flujos de almacén", "Ninguna", "4 semanas", "Líder de Proyecto"),
        ("A2", "Análisis legal y Aviso de Privacidad", "A1", "3 semanas", "Asesor Jurídico"),
        ("A3", "Diseño de Arquitectura y Modelo BD Prisma", "A1", "4 semanas", "Arquitecto de Software"),
        ("A4", "Construcción Core (React + Node + Redis)", "A3", "8 semanas", "Ingeniero Full-Stack"),
        ("A5", "Pruebas Automatizadas E2E Playwright", "A4", "4 semanas", "Ingeniero de QA"),
        ("A6", "Despliegue Cloud Run y Acondicionamiento", "A4, A5", "3 semanas", "Ingeniero DevOps"),
        ("A7", "Capacitación a Almacenistas y Señalética", "A2, A6", "2 semanas", "Coordinador de Campo"),
        ("A8", "Prueba Piloto en 3 Almacenes de CUTonalá", "A6, A7", "12 semanas", "Equipo de Proyecto"),
        ("A9", "Evaluación SUS y Análisis Estadístico", "A8", "3 semanas", "Analista de Datos"),
        ("A10", "Registro INDAUTOR y Conclusiones Finales", "A8, A9", "4 semanas", "Autor del Proyecto")
    ]

    for r_idx, row_vals in enumerate(gantt_rows, start=1):
        row = gantt_table.rows[r_idx]
        for c_idx, val in enumerate(row_vals):
            cell = row.cells[c_idx]
            set_cell_margins(cell, top=60, bottom=60, left=80, right=80)
            p = cell.paragraphs[0]
            r = p.add_run(val)
            r.font.size = Pt(9)
            if c_idx == 0:
                r.font.bold = True

    add_table_note("Planificación integral del proyecto en 5 fases secuenciales a lo largo de 12 meses.")

    add_heading_2("11.2 Diagrama de Gantt Anual (Distribución Mensual)")
    
    gantt_text = (
        "Actividad                                M01  M02  M03  M04  M05  M06  M07  M08  M09  M10  M11  M12\n"
        "-------------------------------------------------------------------------------------------------------\n"
        "A1. Diagnóstico de flujos de almacén    [====]\n"
        "A2. Análisis legal y Aviso Privacidad         [===]\n"
        "A3. Arquitectura y Modelado de BD             [====]\n"
        "A4. Construcción Core (React/Node/Redis)            [========]\n"
        "A5. Pruebas Automatizadas E2E Playwright                     [====]\n"
        "A6. Despliegue GCP y Ventanillas                                  [===]\n"
        "A7. Capacitación y Señalética                                       [==]\n"
        "A8. Prueba Piloto en CUTonalá (3 almacenes)                             [============================]\n"
        "A9. Evaluación SUS y Análisis Estadístico                                                    [===]\n"
        "A10. Registro INDAUTOR y Conclusiones Finales                                                     [====]\n"
        "-------------------------------------------------------------------------------------------------------\n"
        "RUTA CRÍTICA (CPM): A1 ====> A3 ====> A4 ====> A5 ====> A6 ====> A8 ====> A9 ====> A10 (12 meses)"
    )
    p_gantt = doc.add_paragraph()
    r_g = p_gantt.add_run(gantt_text)
    r_g.font.name = 'Consolas'
    r_g.font.size = Pt(8.5)
    r_g.font.color.rgb = COLOR_NAVY

    add_heading_2("11.3 Análisis de la Ruta Crítica (CPM)")
    doc.add_paragraph(
        "El análisis matemático del método CPM determina que la cadena crítica vincula estrictamente las actividades A1 -> A3 -> A4 -> "
        "A5 -> A6 -> A8 -> A9 -> A10 con holgura total cero (HT = 0). Las tareas legales (A2) y de señalética (A7) poseen holgura positiva, "
        "lo que permite absorber ligeras variaciones de calendario sin comprometer la entrega final del sistema."
    )

    doc.add_page_break()

    # =============================================================
    # 12. GLOSARIO DE TÉRMINOS TÉCNICOS
    # =============================================================
    add_heading_1("12. Glosario de Términos Técnicos")
    doc.add_paragraph("A continuación se presentan 27 definiciones técnicas con rigor en ciencias computacionales y metodológicas:")

    glossary_items = [
        ("ACID (Atomicity, Consistency, Isolation, Durability):", "Propiedades de las transacciones en bases de datos que garantizan que los datos permanezcan íntegros y válidos ante cualquier interrupción o falla."),
        ("API REST (Representational State Transfer):", "Arquitectura de comunicación cliente-servidor basada en el protocolo HTTP y formato JSON para manipulación de recursos web."),
        ("Autenticación Basada en Tokens:", "Mecanismo criptográfico donde el usuario se identifica mediante una cadena codificada (token) sin almacenar sesiones en el servidor."),
        ("Cadena de Custodia Patrimonial:", "Registro ininterrumpido que certifica formalmente la posesión, condición física y traslado de un bien mueble público."),
        ("Canvas API (HTML5):", "Elemento del estándar web para renderizar gráficos bidimensionales y capturar trazos vectoriales, utilizado para la firma digital manuscrita."),
        ("Cloud Run:", "Plataforma serverless de Google Cloud Platform para ejecución de contenedores Docker con autoescalado automático."),
        ("Concurrencia:", "Capacidad de un sistema computacional de ejecutar múltiples hilos o transacciones de manera simultánea compartiendo recursos comunes."),
        ("Condición de Carrera (Race Condition):", "Falla de concurrencia donde dos o más procesos compiten por el mismo recurso produciendo resultados incoherentes si no existe sincronización."),
        ("Código QR Dinámico:", "Matriz bidimensional de datos con identificadores cifrados y sellos temporales que expiran tras un uso o lapso establecido."),
        ("Doble Checklist Digital:", "Procedimiento de inspección física realizado obligatoriamente tanto a la entrega como a la devolución del activo."),
        ("Docker:", "Tecnología de contenerización que empaqueta una aplicación y sus dependencias en una unidad estandarizada para ejecución consistente."),
        ("HMAC (Hash-based Message Authentication Code):", "Construcción criptográfica que asegura la integridad y autenticidad de un mensaje combinando una clave secreta y una función hash (SHA-256)."),
        ("JSON Web Token (JWT):", "Estándar abierto RFC 7519 para transferir datos de identidad y privilegios en un objeto JSON compacto y firmado digitalmente."),
        ("Monorepo:", "Estrategia de arquitectura donde múltiples proyectos y bibliotecas compartidas coexisten en un único repositorio con versionado coordinado."),
        ("Object-Relational Mapping (ORM):", "Herramienta que mapea modelos de programación orientada a objetos hacia tablas de bases de datos relacionales."),
        ("Payback (Periodo de Recuperación):", "Indicador financiero que calcula los meses necesarios para recuperar la inversión inicial a partir de los ahorros o utilidades generadas."),
        ("Playwright:", "Marco de pruebas de software desarrollado por Microsoft para automatizar la interacción de usuarios en navegadores web de extremo a extremo."),
        ("Progressive Web App (PWA):", "Aplicación web accesible desde cualquier navegador que ofrece interactividad fluida similar a una app nativa móvil."),
        ("Redis (Remote Dictionary Server):", "Motor de base de datos en memoria ultrarrápido utilizado para cachés y cerrojos de concurrencia."),
        ("Responsiva Digital:", "Acta electrónica legal generada en PDF con número de serie, checklist y firma manuscrita digitalizada que ampara la tenencia del bien."),
        ("Ruta Crítica (CPM):", "Secuencia de tareas dependientes que determina la duración mínima obligatoria de un proyecto; no admite holguras."),
        ("Scrumban:", "Metodología ágil que fusiona la predictibilidad de sprints de Scrum con la fluidez y límites WIP de Kanban."),
        ("Single Page Application (SPA):", "Aplicación web que actualiza dinámicamente la vista en el navegador sin recargar páginas completas desde el servidor."),
        ("Soft-Lock (Cerrojo Suave Distribuido):", "Bloqueo temporal con expiración (TTL) que reserva un recurso mientras el usuario formaliza la transacción."),
        ("System Usability Scale (SUS):", "Escala psicométrica estandarizada de 10 reactivos utilizada para medir objetivamente la usabilidad percibida de un software."),
        ("Time-To-Live (TTL):", "Mecanismo computacional que establece el tiempo de vida de un dato en caché tras el cual se elimina automáticamente."),
        ("WebRTC (Web Real-Time Communication):", "Protocolo web que permite acceder directamente a cámaras de video y micrófonos sin requerir complementos o controladores externos.")
    ]

    for term, definition in glossary_items:
        p_glo = doc.add_paragraph()
        p_glo.paragraph_format.space_after = Pt(4)
        p_glo.paragraph_format.line_spacing = 1.15
        r_t = p_glo.add_run(term + " ")
        r_t.font.bold = True
        r_t.font.color.rgb = COLOR_NAVY
        r_t.font.size = Pt(10.5)
        r_d = p_glo.add_run(definition)
        r_d.font.size = Pt(10.5)

    doc.add_page_break()

    # =============================================================
    # 13. REFERENCIAS BIBLIOGRÁFICAS (APA 7ma EDICIÓN)
    # =============================================================
    add_heading_1("13. Referencias Bibliográficas")

    references = [
        "Asociación Nacional de Universidades e Instituciones de Educación Superior. (2023). Anuario estadístico de la educación superior 2022-2023. ANUIES. http://www.anuies.mx/informacion-y-servicios/informacion-estadistica-de-educacion-superior",
        "Arias, F. G. (2012). El proyecto de investigación: Introducción a la metodología científica (6.ª ed.). Editorial Episteme.",
        "Bernal, C. A. (2016). Metodología de la investigación: administración, economía, humanidades y ciencias sociales (4.ª ed.). Pearson Educación.",
        "Brooke, J. (1996). SUS: A 'quick and dirty' usability scale. En P. W. Jordan, B. Thomas, B. A. Weerdmeester, & A. L. McClelland (Eds.), Usability evaluation in industry (pp. 189–194). Taylor & Francis.",
        "Cámara de Diputados del H. Congreso de la Unión. (2017). Ley general de protección de datos personales en posesión de sujetos obligados. Diario Oficial de la Federación. https://www.diputados.gob.mx/LeyesBiblio/pdf/LGPDPPSO.pdf",
        "Centro Universitario de Tonalá. (2023). Plan de desarrollo de CUTonalá 2019-2025: Visión 2030. Universidad de Guadalajara. http://www.cutonala.udg.mx/transparencia/pdi",
        "Coordinación General de Planeación y Evaluación. (2024). Numeralia institucional de la Red Universitaria. Universidad de Guadalajara. http://www.cgpe.udg.mx/numeralia",
        "Davis, F. D. (1989). Perceived usefulness, perceived ease of use, and user acceptance of information technology. MIS Quarterly, 13(3), 319–340. https://doi.org/10.2307/249008",
        "Hernández-Sampieri, R., & Mendoza Torres, C. P. (2018). Metodología de la investigación: las rutas cuantitativa, cualitativa y mixta. McGraw-Hill Education.",
        "Kleppmann, M. (2017). Designing data-intensive applications: The big ideas behind reliable, scalable, and maintainable systems. O'Reilly Media.",
        "Martin, R. C. (2018). Clean architecture: A craftsman's guide to software structure and design. Prentice Hall.",
        "Miranda Miranda, J. J. (2012). Gestión de proyectos: Identificación, formulación, evaluación financiera, económica, social, ambiental (7.ª ed.). MMEditores.",
        "Nielsen, J. (1994). Usability engineering. Morgan Kaufmann Publishers.",
        "Organización de las Naciones Unidas. (2015). Transformar nuestro mundo: la Agenda 2030 para el Desarrollo Sostenible. ONU. https://sdgs.un.org/es/2030agenda",
        "Pressman, R. S., & Maxim, B. R. (2020). Software engineering: A practitioner's approach (9.ª ed.). McGraw-Hill Education.",
        "Project Management Institute. (2021). A guide to the project management body of knowledge (PMBOK guide) (7.ª ed.). Project Management Institute.",
        "Sapag Chain, N., Sapag Chain, R., & Sapag Puelma, J. M. (2014). Preparación y evaluación de proyectos (6.ª ed.). McGraw-Hill Interamericana.",
        "Silberschatz, A., Korth, H. F., & Sudarshan, S. (2020). Database system concepts (7.ª ed.). McGraw-Hill Education.",
        "Sommerville, I. (2019). Ingeniería del software (10.ª ed.). Pearson Educación.",
        "Universidad de Guadalajara. (2019). Reglamento de adquisiciones, arrendamientos y contratación de servicios de la Universidad de Guadalajara. Gaceta de la Universidad de Guadalajara. http://www.secgen.udg.mx/normatividad/reglamentos"
    ]

    for ref in references:
        p_ref = doc.add_paragraph()
        p_ref.paragraph_format.left_indent = Inches(0.5)
        p_ref.paragraph_format.first_line_indent = Inches(-0.5)
        p_ref.paragraph_format.space_after = Pt(7)
        p_ref.paragraph_format.line_spacing = 1.15
        r_ref = p_ref.add_run(ref)
        r_ref.font.size = Pt(10)

    # Guardar documento
    doc.save(output_path)
    print(f"Documento generado exitosamente en: {output_path}")

if __name__ == "__main__":
    out_file1 = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "docs", "2026B_Equipo4_Protocolo.docx"))
    out_file2 = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "docs", "2026B_Protocolo_Investigacion_SIGRE_Completo.docx"))
    create_protocolo_docx(out_file1)
    create_protocolo_docx(out_file2)
