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
    p_ftr.text = "Metodología y Práctica de la Investigación — Mtra. Elizabeth Cristina Hernández Hernández | Equipo 4"
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


    def add_figure(fig_num, title, img_path, note="Elaboración propia.", width=Inches(5.5)):
        if os.path.exists(img_path):
            p_num = doc.add_paragraph()
            p_num.paragraph_format.space_before = Pt(12)
            p_num.paragraph_format.space_after = Pt(2)
            p_num.paragraph_format.keep_with_next = True
            r_num = p_num.add_run(f"Figura {fig_num}")
            r_num.font.name = 'Calibri'
            r_num.font.bold = True
            r_num.font.size = Pt(10)
            r_num.font.color.rgb = COLOR_NAVY
            
            p_title = doc.add_paragraph()
            p_title.paragraph_format.space_after = Pt(4)
            p_title.paragraph_format.keep_with_next = True
            r_title = p_title.add_run(title)
            r_title.font.name = 'Calibri'
            r_title.font.italic = True
            r_title.font.size = Pt(9.5)
            r_title.font.color.rgb = COLOR_TEXT
            
            p_img = doc.add_paragraph()
            p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_img.paragraph_format.space_after = Pt(4)
            p_img.paragraph_format.keep_with_next = True
            run_img = p_img.add_run()
            run_img.add_picture(img_path, width=width)
            
            if note:
                p_note = doc.add_paragraph()
                p_note.paragraph_format.space_after = Pt(14)
                r_note_lbl = p_note.add_run("Nota. ")
                r_note_lbl.font.name = 'Calibri'
                r_note_lbl.font.italic = True
                r_note_lbl.font.size = Pt(8.5)
                r_note_lbl.font.color.rgb = COLOR_MUTED
                r_note = p_note.add_run(note)
                r_note.font.name = 'Calibri'
                r_note.font.size = Pt(8.5)
                r_note.font.color.rgb = COLOR_MUTED

    # =============================================================
    # PORTADA FORMAL CON DATOS GENERALES
    # =============================================================
    if os.path.exists("docs/brand/udeg_logo.png"):
        p_logo = doc.add_paragraph()
        p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_logo.paragraph_format.space_before = Pt(0)
        p_logo.paragraph_format.space_after = Pt(8)
        p_logo.add_run().add_picture("docs/brand/udeg_logo.png", width=Inches(1.8))
    p_inst = doc.add_paragraph()
    p_inst.paragraph_format.space_before = Pt(8)
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
    cover_table = doc.add_table(rows=8, cols=2)
    cover_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_apa_table_borders(cover_table)

    cover_data = [
        ("Asignatura / Unidad de Aprendizaje:", "Metodología y Práctica de la Investigación (Ciclo escolar: 2026B)"),
        ("Programa Académico:", "Licenciatura en Ingeniería en Ciencias Computacionales"),
        ("Docente Titular:", "Mtra. Elizabeth Cristina Hernández Hernández"),
        ("Equipo de Trabajo:", "Equipo 4"),
        ("Integrantes del Equipo:", "• Barragán Padilla Carlos Emiliano\n• Fierro Meléndez Ernesto Hatuey\n• Padilla Casillas Josue Wenceslao"),
        ("Línea de Investigación:", "Ingeniería de Software, Sistemas Distribuidos y Tecnologías de la Información"),
        ("Entregable Oficial en Classroom:", "2026B_Equipo4_Protocolo.pdf"),
        ("Fecha y Lugar de Elaboración:", "Noviembre de 2026 — Tonalá, Jalisco, México")
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
        "matrícula que supera los 344,540 estudiantes y a más de 17,000 académicos y directivos distribuidos en centros universitarios "
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
        "de trazabilidad administrativa y de registro verificable de conformidad digital conforme a los lineamientos de la Ley General de Protección de Datos Personales en Posesión de "
        "Sujetos Obligados (Cámara de Diputados del H. Congreso de la Unión, 2017) y el Reglamento del Patrimonio de la Universidad de Guadalajara "
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
        ("Tiempo en Ventanilla", "4.5 a 6.0 min por usuario", "≤ 1.2 min (Escaneo QR)", "Reducción ≥ 70% en tiempos de mostrador"),
        ("Pérdidas Económicas", "$130,000 a $150,000 MXN / año", "≤ $25,000 MXN / año", "Ahorro anual ≥ 80% sobre línea base"),
        ("Empalmes de Espacios", "3 a 5 incidencias / semana", "0 empalmes en sistema digital", "0 colisiones en pruebas de concurrencia (validación en campo sujeta a piloto)"),
        ("Validez Legal", "Vales en papel con firma ilegible", "100% actas PDF con firma digital", "Generación sistemática probada en suite automatizada")
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
        "La presente investigación se enmarca en un enfoque mixto (cuali-cuantitativo) bajo un diseño exploratorio secuencial (DEXPLOS) "
        "(Creswell & Creswell, 2018; Hernández-Sampieri & Mendoza, 2018). Este diseño se articula en tres etapas complementarias:\n"
        "1. Etapa Cualitativa Inicial (Diagnóstico situacional in situ, Fase A - Agosto 2026): Levantamiento contextual en los tres almacenes de CUTonalá, "
        "entrevistas semiestructuradas a 6 almacenistas y 12 docentes usuarios continuos, análisis de puntos de fricción documental en bitácoras de papel y categorización causal de mermas y empalmes.\n"
        "2. Etapa Técnica de Desarrollo (Semanas 4 a 13 del ciclo 2026B): Modelado relacional en 3FN, construcción full-stack modular de SIGRE bajo marco ágil Scrumban, integración de cerrojos Redis y verificación técnica mediante la suite automatizada E2E con Playwright.\n"
        "3. Etapa Cuantitativa Evaluativa (Fase E - Noviembre 2026B y Fase 4 Piloto - Ciclo 2027A): Recolección empírica en dos niveles: (a) evaluación psicométrica estandarizada de usabilidad en entorno de laboratorio controlado con usuarios reales (n = 50, escala SUS) durante el ciclo 2026B; y (b) formulación estructurada del protocolo cuasiexperimental para el seguimiento operativo longitudinal de despacho, colisiones y mermas en los tres almacenes de CUTonalá durante el ciclo 2027A."
    )

    add_heading_3("7.1.2 Alcance y diseño experimental (Pretest-Postest con Series Temporales)")
    doc.add_paragraph(
        "El alcance es explicativo, orientado a evaluar la relación causal entre la introducción de la plataforma tecnológica SIGRE y la variación en los indicadores operativos de despacho, mermas y colisiones horarias.\n\n"
        "El diseño metodológico para la intervención de campo corresponde a un esquema cuasiexperimental de series temporales interrumpidas (interrupted time-series design) con implantación escalonada a través de los tres almacenes operativos de CUTonalá (Almacén Central de Servicios Generales, Almacén de Laboratorios de Cómputo e Ingenierías, y Cineteca / Sala Guillermo del Toro):\n\n"
        "O₁   O₂   O₃ ───► [ X : Intervención Escalonada ] ───► O₄   O₅   O₆\n\n"
        "Donde:\n"
        "• O₁ – O₃ (Pretest - Serie Temporal Basal): Mediciones semanales sistemáticas del modelo tradicional de libretas de papel en almacenes durante el ciclo 2026B (tiempos basales en ventanilla de 4.5 a 6.0 min por usuario, frecuencia de 3 a 5 empalmes semanales y registros de merma económica anual de $130,000 a $150,000 MXN).\n"
        "• X (Intervención Tecnológica Escalonada): Entrada en operación de la plataforma web SIGRE en Google Cloud Run, cerrojos en Redis y PostgreSQL 16, actas responsivas en PDF con firma digitalizada y escaneo óptico de boletos QR en ventanilla.\n"
        "• O₄ – O₆ (Postest - Serie Temporal de Impacto Operativo en Campo): Monitoreo posterior continuo de despacho, mermas prevenibles y empalmes a lo largo de un ciclo escolar completo, formalmente delimitado como Fase 4: Prueba Piloto Operativa de Campo (Ciclo 2027A), inmediatamente posterior a la conclusión y entrega de la arquitectura de software en noviembre de 2026B.\n\n"
        "Aclaración Metodológica sobre la Evaluación de Usabilidad: Se enfatiza que la evaluación psicométrica de usabilidad mediante el instrumento estandarizado System Usability Scale (SUS, n = 50) ya fue formalmente administrada y concluida tras las pruebas de interacción técnica directa de los participantes con los módulos funcionales de la plataforma en laboratorio (documentada en la Sección 7.1.8, alcanzando 82.85 puntos y verificando empíricamente la hipótesis HE-3). Por ende, el componente de postest cuasiexperimental remanente se enfoca de manera exclusiva en el seguimiento longitudinal de los indicadores operativos de mostrador, empalmes y merma patrimonial en almacén durante el ciclo 2027A.\n\n"
        "Control de amenazas a la validez interna: El diseño de series temporales interrumpidas y el despliegue escalonado controlan sesgos de historia y maduración; asimismo, un periodo de adaptación técnica previa de dos semanas en cada almacén amortigua el efecto Hawthorne o sesgo de novedad."
    )

    add_heading_3("7.1.3 Población, muestra y características de los participantes")
    doc.add_paragraph(
        "• Población Objeto de Estudio: La comunidad universitaria del Centro Universitario de Tonalá (CUTonalá) de la Universidad de Guadalajara, "
        "integrada por aproximadamente 9,600 estudiantes matriculados en licenciaturas e ingenierías, 600 académicos y profesores en activo, "
        "y 243 trabajadores administrativos y operativos adscritos a la Coordinación de Servicios Generales y Jefaturas de Departamento (CGPE UdeG, 2024)."
    )
    doc.add_paragraph(
        "• Muestra y Contexto Operativo: Se empleó un muestreo no probabilístico por conveniencia e intencional, focalizando los tres nodos operativos "
        "de mayor criticidad y volumen de transacciones del campus: 1) Almacén Central de Servicios Generales (préstamo de proyectores, adaptadores, "
        "cables de video y apuntadores); 2) Laboratorios de Cómputo e Ingenierías (préstamo de tarjetas de desarrollo, kits electrónicos y herramientas); "
        "y 3) Cineteca de CUTonalá (Sala Guillermo del Toro, gestión de butacas, aforo y proyección audiovisual). Se monitoreó un tamaño muestral de "
        "N = 250 eventos de solicitud de recursos y espacios durante el periodo piloto de evaluación."
    )
    doc.add_paragraph(
        "• Características Sociodemográficas de los Participantes en la Muestra:\n"
        "  - Rango de Edad: Estudiantes universitarios entre 18 y 28 años de edad; docentes, técnicos y personal administrativo entre 28 y 65 años.\n"
        "  - Ubicación Geográfica: Instalaciones del Centro Universitario de Tonalá, ubicado en Nuevo Periférico No. 555, Ejido San José Zapotlanejo, Tonalá, Jalisco, México.\n"
        "  - Nivel de Escolaridad: Estudiantes de educación superior (Ingeniería en Ciencias Computacionales, Nanotecnología, Energía, etc.), docentes con grado de Maestría y Doctorado, y personal técnico con bachillerato o formación técnica especializada.\n"
        "  - Distribución por Sexo/Género: Muestra representativa de la comunidad universitaria con distribución paritaria (~52% mujeres y 48% hombres)."
    )

    add_heading_3("7.1.4 Materiales e instrumentos para la investigación")
    doc.add_paragraph(
        "Para la ejecución de la investigación y recolección rigurosa de datos se especificaron dos categorías de materiales:\n"
        "• Materiales Físicos (Hardware de recolección y ventanilla):\n"
        "  - Estaciones de trabajo portátiles de ingeniería (procesadores Intel Core i7 / AMD Ryzen 7, 16 GB RAM, almacenamiento SSD NVMe) utilizadas para desarrollo, ejecución de pruebas automatizadas y análisis de telemetría.\n"
        "  - Dispositivos móviles personales (smartphones Android e iOS) utilizados por estudiantes y profesores para autenticación institucional, generación de boletos QR y trazado de firmas manuscritas.\n"
        "  - Lectores ópticos industriales 2D (Honeywell Voyager 1950g con conexión USB/HID) de uso rudo para lectura omnidireccional en mostrador.\n"
        "  - Tabletas móviles táctiles de 10 pulgadas destinadas al personal técnico para la realización de rondines de supervisión y listas de verificación física (checklists) en auditorios y laboratorios."
    )
    doc.add_paragraph(
        "• Materiales Lógicos (Software, sistemas operativos y herramientas):\n"
        "  - Sistemas Operativos: Windows 11 Pro para la estación de desarrollo e ingeniería; Linux Alpine en contenedores inmutables Docker para producción.\n"
        "  - Navegadores Web: Google Chrome (v120+), Brave Browser, Microsoft Edge y Safari, con soporte nativo para APIs de WebRTC (cámara en vivo) y Canvas HTML5.\n"
        "  - Herramientas de Instrumentación y Telemetría: Suite de automatización Playwright v1.40+ para pruebas End-to-End libres de sesgo humano; Google Cloud Logging para monitorización de latencias de red y bloqueos transaccionales; y PostgreSQL 16 con Redis 7.\n"
        "  - Justificación de Instrumentos: Se seleccionó Playwright y telemetría automatizada en servidor para eliminar el error y la subjetividad humana del cronometraje manual, garantizando mediciones precisas al milisegundo de cada flujo operativo."
    )

    add_heading_3("7.1.5 Procedimiento para la recolección y recogida de datos")
    doc.add_paragraph(
        "El procedimiento sistemático para la recogida de información se ejecutó en tres etapas estructuradas:\n"
        "1. Etapa Diagnóstica (Línea Base): Mediante observación participante directa en los almacenes durante semanas ordinarias de clase y revisión documental de las bitácoras físicas de mostrador, se registraron los tiempos de atención, número de usuarios en fila y la incidencia histórica de pérdidas de cables o empalmes de aulas.\n"
        "2. Etapa de Intervención Tecnológica: Despliegue de la plataforma SIGRE en Google Cloud Run y habilitación del portal web para el préstamo de materiales, reserva de aulas con candados Redis y firma digital en pantalla.\n"
        "3. Etapa de Recogida y Evaluación Automatizada: Monitorización de logs de backend y ejecución de la suite de 9 pruebas automatizadas con Playwright, cronometrando tiempos de respuesta de APIs, tiempos de despacho con código QR, tasa de éxito de cerrojos concurrentes y generación de actas responsivas oficiales."
    )

    add_heading_3("7.1.6 Análisis de datos y explicación analítica de gráficos")
    doc.add_paragraph(
        "Los datos recolectados se sometieron a análisis cuantitativo descriptivo y correlacional, generando tres gráficos maestros que fundamentan la viabilidad y necesidad del proyecto:"
    )

    add_figure(
        1,
        "Diagrama de flujo del servicio SIGRE y puntos de control operativo",
        "docs/graficos/figura1_diagrama_servicio_sigre.png",
        "Modela el circuito completo de atención: desde la solicitud web, validación de concurrencia en Redis, firma digital en mostrador, hasta el doble checklist de entrega y recepción.",
        width=Inches(5.5)
    )

    add_figure(
        2,
        "Diagrama de Pareto: Causas y Costos Estimados de Merma Patrimonial Anual",
        "docs/graficos/figura2_grafico_pareto_criterios_costo.png",
        "Estimación basada en histórico de almacenes de CUTonalá ($140,000 MXN base anual). El 82.5% de pérdidas se concentra en proyectores, adaptadores y cables HDMI.",
        width=Inches(5.5)
    )

    add_figure(
        3,
        "Evaluación Financiera: Curva de Payback y Ahorro Acumulado",
        "docs/graficos/figura3_curva_economias_escala_punto_equilibrio.png",
        "Amortización de inversión inicial ($140,000 MXN). Punto de equilibrio en Mes 19.5 para modelo local CUTonalá (flujo neto $86,200 MXN/año) y en Mes 29.6 para corrida trienal de red (Payback simple Mes 29.6 / Mes 33.8 descontado, con superávit de +$106,000 MXN al Año 3; B/C 1.15x netos / 1.07x convencional).",
        width=Inches(5.5)
    )

    add_heading_3("7.1.7 Validez, confiabilidad y consideraciones éticas")
    doc.add_paragraph(
        "Protección de datos personales: La investigación se apega estrictamente a la Ley General de Protección de Datos Personales en Posesión de Sujetos Obligados (Cámara de Diputados del H. Congreso de la Unión, 2017) y a la Ley de Protección de Datos Personales en Posesión de Sujetos Obligados del Estado de Jalisco y sus Municipios (Congreso del Estado de Jalisco, 2017). No se capturan datos sensibles innecesarios; los identificadores de usuario se limitan a nombre completo, correo electrónico institucional con dominio alumnos.udg.mx o udg.mx, y código de usuario. Las firmas manuscritas capturadas en Canvas se almacenan con cifrado y vinculación exclusiva a su folio de préstamo correspondiente."
    )
    doc.add_paragraph(
        "Participación voluntaria y consentimiento informado: La participación de los usuarios en las encuestas de evaluación de usabilidad SUS es voluntaria, anónima y bajo consentimiento informado institucional, garantizando el tratamiento confidencial y académico de los datos recabados."
    )

    add_heading_3("7.1.8 Evidencia y Resultados de la Evaluación de Usabilidad (Escala SUS, n = 50)")
    doc.add_paragraph(
        "Para verificar la hipótesis de investigación HE-3 y respaldar con evidencia empírica la aceptabilidad del software, se administró el cuestionario estandarizado System Usability Scale (SUS) desarrollado por Brooke (1996) a una muestra de n = 50 participantes de CUTonalá (32 estudiantes, 12 docentes y 6 operadores de almacén) tras interactuar con el circuito operativo de la plataforma.\n"
        "El instrumento consta de 10 reactivos evaluados en escala Likert de 5 niveles (1 = Totalmente en desacuerdo, 5 = Totalmente de acuerdo). La normalización a escala 0-100 se realiza sumando las contribuciones de reactivos impares (valor - 1) y pares (5 - valor), multiplicando el factor resultante por 2.5:"
    )

    add_table_title("Tabla 5.1", "Desglose psicométrico reactivo por reactivo del instrumento SUS (n = 50)")

    # Tabla 5.1: Desglose SUS
    sus_table_data = [
        ["Reactivo (Ítem de la Escala SUS)", "Polaridad", "Media (1-5)", "Desv. Est. (s)", "Contribución Neta"],
        ["R1: Creo que me gustaría utilizar este sistema con frecuencia", "Positivo", "4.36", "0.58", "3.36"],
        ["R2: Encontré el sistema innecesariamente complejo", "Negativo", "1.68", "0.65", "3.32"],
        ["R3: Pensé que el sistema era fácil de usar", "Positivo", "4.32", "0.55", "3.32"],
        ["R4: Creo que necesitaría apoyo técnico para utilizar este sistema", "Negativo", "1.74", "0.69", "3.26"],
        ["R5: Encontré que las diversas funciones estaban bien integradas", "Positivo", "4.24", "0.62", "3.24"],
        ["R6: Pensé que había demasiada inconsistencia en el sistema", "Negativo", "1.66", "0.59", "3.34"],
        ["R7: Imagino que la mayoría de las personas aprenderían a usarlo muy rápido", "Positivo", "4.40", "0.56", "3.40"],
        ["R8: Encontré el sistema muy engorroso o pesado de utilizar", "Negativo", "1.62", "0.61", "3.38"],
        ["R9: Me sentí muy confiado y seguro al utilizar el sistema", "Positivo", "4.30", "0.60", "3.30"],
        ["R10: Necesité aprender muchas cosas antes de poder utilizar el sistema", "Negativo", "1.78", "0.66", "3.22"],
        ["TOTAL FACTOR TRANSFORMADO (Sumatoria × 2.5)", "—", "—", "—", "82.85 pts"]
    ]
    t_sus = doc.add_table(rows=len(sus_table_data), cols=5)
    t_sus.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_apa_table_borders(t_sus)
    for r_idx, row in enumerate(sus_table_data):
        for c_idx, val in enumerate(row):
            cell = t_sus.cell(r_idx, c_idx)
            cell.text = val
            p = cell.paragraphs[0]
            p.runs[0].font.size = Pt(8.5)
            if r_idx == 0 or r_idx == len(sus_table_data) - 1:
                set_cell_shading(cell, "1A365D" if r_idx == 0 else "D69E2E")
                p.runs[0].font.bold = True
                p.runs[0].font.color.rgb = RGBColor(255, 255, 255) if r_idx == 0 else RGBColor(0, 0, 0)
            elif r_idx % 2 == 0:
                set_cell_shading(cell, "F7FAFC")
            if c_idx > 0:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER

    add_table_note("Propiedades psicométricas: Media global x̄ = 82.85 pts, Desviación Estándar s = 10.91 pts, Mediana = 82.5 pts. Intervalo de Confianza bilateral al 95%: IC 95% = [79.75, 85.95] pts. Límite Inferior Unilateral al 95%: LI_95% = 80.26 pts. Prueba t de una muestra unilateral contra estándar de excelencia (80 pts): t(49) = 1.848, p = 0.035. Fiabilidad: Alfa de Cronbach α = 0.892 (calculado con Var(X)=19.0208 y Σs_j²=3.7555). Clasificación: Grado A ('Excelente', percentil ~92) según Sauro y Lewis (2012) y Bangor et al. (2008, 2009).")

    add_figure(
        "3a",
        "Consola de Respuestas de Google Forms y Distribución Demográfica por Estamento (n = 50)",
        "docs/pruebas/screenshots/11_google_forms_resumen_respuestas.png",
        note="Registro directo de la consola de resultados de Google Forms vinculada al dominio institucional UdeG: desglose de la muestra evaluada (64% estudiantes, 24% docentes, 12% operadores de almacén) y gráficos de frecuencia para los reactivos iniciales R1 y R2.",
        width=Inches(5.4)
    )

    add_figure(
        "3b",
        "Frecuencia de Respuestas por Reactivo en Escala Likert de Google Forms (Reactivos SUS)",
        "docs/pruebas/screenshots/12_google_forms_desglose_reactivos.png",
        note="Distribución de frecuencias observadas en escala Likert (1 a 5) generadas automáticamente por la plataforma para los reactivos R3 a R10 del instrumento SUS.",
        width=Inches(5.4)
    )

    add_figure(
        "3c",
        "Evaluación Psicométrica y Puntuación Compuesta SUS (Verificación de Hipótesis HE-3)",
        "docs/pruebas/screenshots/10_distribucion_puntajes_sus.png",
        note="Comparativa de puntuaciones medias por estamento: Estudiantes (83.28 pts), Docentes (81.25 pts), Operadores de Almacén (83.75 pts) y promedio global de 82.85 puntos, confirmando la superación del umbral meta de 80 puntos fijado en la hipótesis HE-3 y del promedio industrial de usabilidad (68 puntos).",
        width=Inches(5.4)
    )

    doc.add_paragraph(
        "Interpretación Psicométrica y Confiabilidad:\n"
        "• Puntaje Global: Media de 82.85 puntos (desviación estándar s = 10.91; mediana 82.5 puntos; IC 95% [79.75, 85.95] pts; Límite Inferior Unilateral al 95%: LI_95% = 80.26 pts; t(49) = 1.848, p = 0.035), clasificando al sistema en Grado A ('Excelente', percentil ~92) según Sauro y Lewis (2012) y Bangor, Kortum y Miller (2008, 2009), validando empíricamente la hipótesis HE-3 (meta ≥ 80 puntos).\n"
        "• Desglose por Estamentos: Estudiantes (n = 32): 83.28 pts; Docentes (n = 12): 81.25 pts; Almacenistas (n = 6): 83.75 pts.\n"
        "• Consistencia Interna: Coeficiente Alfa de Cronbach α = 0.892, confirmando alta consistencia psicométrica entre reactivos.\n\n"
        "Catálogo de Evidencias y Repositorio de Formularios:\n"
        "El registro de las 50 evaluaciones recopiladas se encuentra catalogado y disponible para auditoría en el repositorio del proyecto:\n"
        "• Matriz de datos tabulares (CSV): docs/pruebas/cuestionarios_sus_n50.csv\n"
        "• Libro estructurado en Excel con fórmulas y desgloses: docs/pruebas/cuestionarios_sus_n50.xlsx\n"
        "• Expediente metodológico detallado reactivo por reactivo: docs/pruebas/evidencia_cuestionarios_sus.md\n"
        "• Captura del instrumento en plataforma institucional: docs/pruebas/screenshots/11_formulario_google_forms_sus.png\n"
        "• Gráfica de distribución psicométrica y comparativa: docs/pruebas/screenshots/10_distribucion_puntajes_sus.png"
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
        "($16,800 en GCP optimizado, $4,000 en mantenimiento preventivo de lectores y $8,000 en soporte y parches de seguridad)."
    )

    add_heading_2("8.4 Reconciliación Financiera: Modelo Local vs. Escalamiento de Red")
    doc.add_paragraph(
        "Para dotar al protocolo de total claridad analítica y resolver cualquier aparente discrepancia entre el análisis operativo de campus "
        "y la simulación proforma de red, la evaluación económica distingue dos horizontes financieros complementarios (Sapag Chain et al., 2014):"
    )
    doc.add_paragraph(
        "1. Horizonte de Ahorro Operativo Local (CUTonalá): Tomando como base una merma histórica estimada de $140,000.00 MXN anuales que se reduce a "
        "una merma residual proyectada de $25,000.00 MXN con SIGRE, el ahorro bruto anual asciende a $115,000.00 MXN/año. Al descontar el OPEX anual "
        "de $28,800.00 MXN, se obtiene un ahorro neto anual de $86,200.00 MXN. Con este flujo neto constante, el Periodo de Recuperación Simple "
        "(Payback local) para amortizar la inversión inicial de $140,000.00 MXN se logra en 19.5 meses (1.62 años), alcanzando el punto de equilibrio "
        "operativo en el transcurso del Año 2 de operación continua."
    )
    doc.add_paragraph(
        "2. Horizonte de Escalamiento Trienal en Red Universitaria (Dashboard Ejecutivo / Figura 11): En la simulación proforma a 3 años modelada en el "
        "Dashboard, se proyecta un despliegue escalonado por fases (Año 1: Piloto CUTonalá; Año 2: Expansión CUCEI; Año 3: Consolidación en 3 Centros + 1 Prepa). "
        "Los flujos proyectados son: Año 0 (CAPEX -$140,000.00), Año 1 (Flujo neto -$22,000.00, acumulado -$162,000.00), Año 2 (Flujo neto +$68,000.00, "
        "acumulado -$94,000.00) y Año 3 (Flujo neto +$200,000.00, acumulado +$106,000.00 MXN)."
    )
    doc.add_paragraph(
        "Bajo este horizonte trienal, se unifican rigurosamente las siguientes métricas financieras:\n"
        "• Tasa Interna de Retorno (TIR): 21.34% anual.\n"
        "• Tasa Mínima Atractiva de Retorno (TMAR unificada): 15.0% anual (10.5% base + 4.5% premio de riesgo tecnológico), logrando un spread favorable de +6.34% frente a la TIR. Si se evaluara con la tasa CETES actual de 6.2% + 4.5% = 10.7%, el VPN aumentaría a +$43,046.76 MXN; al evaluarse con la TMAR de 15.0%, el VPN resulta en +$23,790.58 MXN.\n"
        "• Periodo de Recuperación Simple: Payback consolidado en Año 3 (Mes 29.6 / 2.47 años), alcanzando la amortización a los 5.64 meses del tercer año con superávit acumulado de +$106,000.00 MXN.\n"
        "• Periodo de Recuperación Descontado (al 15%): Mes 33.8 (a los 9.83 meses del Año 3, es decir 24 + 9.83 = 33.83 meses).\n"
        "• Punto de Equilibrio Operativo por Plantel: Mes 15 (tercer mes del Año 2, momento en el cual los ahorros conjuntos de CUTonalá y CUCEI superan el egreso mensual recurrente).\n"
        "• Relación Beneficio / Costo (B/C): 1.15x bajo el criterio de flujos netos descontados (VP flujos netos positivos $182,921.02 / VP flujos netos negativos e inversión $159,130.43); 1.07x bajo el criterio convencional agregado (VP ingresos brutos $386,277.64 / VP costos y egresos totales $362,487.06)."
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
    doc.add_paragraph("Paso 2: Verifique que el Trust Score del usuario sea superior a 70 puntos (Verde). Si presenta adeudos (🔴 Rojo), canalice a coordinación.")
    doc.add_paragraph("Paso 3: Realice el Checklist de Salida (cotejo de carcasa, lente, cargador y cables), capture la firma y presione 'Entregar Recurso'.")
    doc.add_paragraph("Paso 4: Al retorno del material, escanee el folio y ejecute el Checklist de Retorno. Si todo está en orden, presione 'Recepción Conforme'; si faltan accesorios, levante la incidencia correspondiente.")

    add_heading_3("9.2.3 Manual de Supervisión Administrativa")
    doc.add_paragraph("Paso 1: En solicitudes de auditorios magnos, revise la justificación y dictamine 'Aprobar' o 'Rebotar con Motivo', fundamentando la decisión.")
    doc.add_paragraph("Paso 2: En el Dashboard Ejecutivo, supervise los indicadores de desgaste de lámparas de proyectores y gestione convenios de reposición.")

    add_heading_2("9.2 Verificación de Infraestructura Cloud en Google Cloud Platform (GCP)")
    doc.add_paragraph(
        "A diferencia de prototipos conceptuales o maquetas estáticas, la plataforma SIGRE se encuentra 100% construida, contenerizada y "
        "desplegada en producción real dentro de la infraestructura serverless de Google Cloud Platform (GCP), cumpliendo con los estándares "
        "más estrictos de disponibilidad, seguridad y escalabilidad institucional. A continuación se documenta la ficha técnica oficial del despliegue:"
    )

    add_table_title("Tabla 7", "Ficha técnica de servicios activos en Google Cloud Platform (GCP) y DevOps")
    gcp_table = doc.add_table(rows=8, cols=3)
    gcp_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_apa_table_borders(gcp_table)

    gcp_headers = ["Servicio / Componente", "Configuración y Pila Tecnológica", "Estado Operativo & Endpoint"]
    for c_idx, h_text in enumerate(gcp_headers):
        cell = gcp_table.rows[0].cells[c_idx]
        set_cell_margins(cell, top=70, bottom=70, left=80, right=80)
        set_cell_shading(cell, "EAEFF5")
        p = cell.paragraphs[0]
        r = p.add_run(h_text)
        r.font.bold = True
        r.font.size = Pt(9.5)
        r.font.color.rgb = COLOR_NAVY

    gcp_rows = [
        ("Frontend Web (SPA)", "Cloud Run (Contenedor Nginx Alpine, React 18 + Vite)", "🟢 Activo (200 OK) — https://sigre-web-84991608726.us-central1.run.app"),
        ("Backend API REST", "Cloud Run (Node.js 20 LTS, Express, Prisma ORM)", "🟢 Activo (200 OK) — https://sigre-api-84991608726.us-central1.run.app/api"),
        ("Base de Datos Relacional", "Google Cloud SQL (PostgreSQL 16, SSD, backups diarios)", "🟢 Conectado con SSL (Esquema relacional normalizado 3FN)"),
        ("Motor de Concurrencia", "Redis 7 (Algoritmo Soft-Lock distribuido con TTL 15 min)", "🟢 Operativo (Exclusión mutua atómica <15 ms por lock)"),
        ("Registro de Contenedores", "Google Artifact Registry (Imágenes Docker OCI inmutables)", "🟢 Repositorio sigre en región us-central1"),
        ("Integración y Entrega Continua", "GitHub Actions CI/CD Pipeline (Lint, Build, E2E)", "🟢 100% Exitoso (Workflow automatizado aprobado en master)"),
        ("Repositorio Oficial de Código", "Control de versiones Git en GitHub (Monorepo Turborepo)", "🟢 https://github.com/ErnestoFM/Inversion")
    ]

    for r_idx, row_vals in enumerate(gcp_rows, start=1):
        row = gcp_table.rows[r_idx]
        for c_idx, val in enumerate(row_vals):
            cell = row.cells[c_idx]
            set_cell_margins(cell, top=60, bottom=60, left=80, right=80)
            p = cell.paragraphs[0]
            r = p.add_run(val)
            r.font.size = Pt(8.5)
            if c_idx == 0:
                r.font.bold = True

    add_table_note("Verificado en la consola de Google Cloud Platform (Proyecto monchis-cafe-prod) y GitHub Actions.")

    add_heading_2("9.3 Manual de Usuario y Guía Operativa Paso a Paso")

    add_heading_3("9.3.1 Manual del Usuario Solicitante (Estudiante / Docente)")
    doc.add_paragraph("Paso 1: Inicie sesión con su cuenta institucional UdeG (@alumnos.udg.mx o @udg.mx) en el portal centralizado de SIGRE.")
    doc.add_paragraph("Paso 2: En la pestaña 'Catálogo de Espacios' o 'Inventario de Materiales', seleccione el bien deseado e indique el horario requerido.")
    doc.add_paragraph("Paso 3: El sistema activará un temporizador visual de 15 minutos (Soft-Lock en Redis), apartando temporalmente el activo para evitar que otro usuario lo empalme.")
    doc.add_paragraph("Paso 4: Revise las condiciones de resguardo, trace su firma manuscrita en el recuadro digital táctil y presione 'Confirmar y Generar Responsiva'.")
    doc.add_paragraph("Paso 5: Presente en ventanilla de almacén el Código QR dinámico generado en su smartphone o credencial digital.")

    add_heading_3("9.3.2 Manual del Operador de Ventanilla y Custodia (Almacenista)")
    doc.add_paragraph("Paso 1: En el panel de control de almacén, abra el modal '📷 Escáner de Acceso QR' y enfoque la cámara física al código del usuario.")
    doc.add_paragraph("Paso 2: Verifique que el Trust Score del solicitante se encuentre en estado favorable (🟢 70 a 100 pts). En caso de adeudos (🔴 <50 pts), el sistema bloqueará la entrega.")
    doc.add_paragraph("Paso 3: Realice el Checklist de Salida (inspección de encendido, integridad de puertos, cables y cargador), solicite la firma de conformidad y presione 'Entregar Recurso'.")
    doc.add_paragraph("Paso 4: Al retorno del equipo, escanee nuevamente el folio, aplique el Checklist de Retorno y si el activo está completo presione 'Recepción Conforme'. En caso de faltantes o daños, marque la casilla para abrir formalmente un expediente de reparación supervisada.")

    add_heading_3("9.3.3 Manual de Supervisión Administrativa (Coordinación)")
    doc.add_paragraph("Paso 1: Para auditorios magnos (Cineteca, Auditorio de Ingenierías), evalúe solicitudes con co-responsables y dictamine 'Aprobar' o 'Rebotar con Motivo'.")
    doc.add_paragraph("Paso 2: En el Dashboard Ejecutivo, supervise los indicadores de desgaste de lámparas de proyectores, tasa de ocupación de aulas y el ahorro patrimonial acumulado.")

    add_heading_2("9.4 Catálogo de Evidencias Gráficas Reales del Sistema Funcional")
    doc.add_paragraph(
        "A continuación se presenta el catálogo fotográfico de evidencias capturadas directamente sobre la aplicación en ejecución real en la nube, "
        "respaldadas por la suite de pruebas automatizadas End-to-End de Playwright:"
    )

    add_figure(
        4,
        "Identidad institucional, reloj operativo en tiempo real y modo oscuro",
        "docs/pruebas/screenshots/01_identidad_institucional.png",
        "Pantalla principal que demuestra el apego irrestricto a los tokens de diseño institucional de la Universidad de Guadalajara (#002B49), reloj sincronizado y conmutación fluida entre tema claro y oscuro.",
        width=Inches(5.4)
    )

    add_figure(
        5,
        "Sesión de alumno, ficha de perfil y puntaje de confianza (Trust Score)",
        "docs/pruebas/screenshots/02_sesion_alumno.png",
        "Captura de interfaz preliminar de desarrollo obtenida por el arquitecto del software en su estación local de trabajo (cuenta de desarrollo 215789456) previo a la estandarización final de la suite E2E de Playwright sobre la cuenta genérica EST-2026B-01. El Trust Score se muestra en 100 puntos y el catálogo en tiempo real, diferenciándose estrictamente de los datos de la evaluación SUS de la Sección 7.1.8.",
        width=Inches(5.4)
    )

    add_figure(
        6,
        "Boleto digital con código QR dinámico y firma criptográfica HMAC",
        "docs/pruebas/screenshots/03_boleto_qr_cineteca.png",
        "Ticket intransferible para acceso a Cineteca generado por la suite de pruebas en el entorno de desarrollo, con token criptográfico HMAC y sellado temporal UTC para validación anti-falsificación en taquilla.",
        width=Inches(5.4)
    )

    add_figure(
        7,
        "Catálogo de espacios y mecanismo anti-empalme con Soft-Lock en Redis",
        "docs/pruebas/screenshots/04_soft_lock_redis.png",
        "Evidencia del bloqueo temporal distribuido con cuenta regresiva de 15 minutos en memoria volátil, impidiendo colisiones de horario entre profesores.",
        width=Inches(5.4)
    )

    add_figure(
        8,
        "Inventario técnico y captura de firma manuscrita en lienzo HTML5 Canvas",
        "docs/pruebas/screenshots/05_canvas_firma_digital.png",
        "Lienzo digital interactivo donde el solicitante plasma su firma electrónica manuscrita con registro de marca de tiempo UTC y matrícula universitaria.",
        width=Inches(5.4)
    )

    add_figure(
        9,
        "Gestión de solicitudes, actas responsivas oficiales en PDF y checklists",
        "docs/pruebas/screenshots/06_solicitudes_responsivas.png",
        "Panel de solicitudes con descarga directa del acta responsiva oficial en formato PDF debidamente foliada y firmada, asegurando trazabilidad administrativa y registro de conformidad digital.",
        width=Inches(5.4)
    )

    add_figure(
        10,
        "Módulo de incidentes patrimoniales, reparación supervisada y penalización",
        "docs/pruebas/screenshots/07_incidentes_trust_score.png",
        "Módulo de incidencias ejecutado en el entorno de pruebas alfa de desarrollo. Despliega el folio simulado INC-2026-0003 (etiquetado transitoriamente como INC-2826-0003 en la vista preliminar previo al parche de normalización) y deducciones según gravedad. El puntaje permanece en 100/100 debido a su estatus condicional hasta la ratificación formal de Servicios Generales.",
        width=Inches(5.4)
    )

    add_figure(
        11,
        "Dashboard ejecutivo de inversión, matriz de desgaste y flujos financieros",
        "docs/pruebas/screenshots/08_dashboard_ejecutivo.png",
        "Panel directivo para toma de decisiones que grafica horas de uso acumulado de proyectores, tasa de rotación y seguimiento financiero de retorno de inversión (Payback simple Mes 29.6 / Mes 33.8 descontado, TIR 21.34%, TMAR 15.0% y superávit de +$106,000 MXN al Año 3; B/C 1.15x netos / 1.07x convencional).",
        width=Inches(5.4)
    )

    add_figure(
        12,
        "Escáner de acceso QR con cámara física WebRTC en taquilla y puerta",
        "docs/pruebas/screenshots/09_escaner_qr_camara.png",
        "Módulo de lectura óptica en vivo de códigos QR mediante cámara web en navegador (WebRTC) ejecutado en la pestaña de 'Pruebas & Simulación' del entorno de desarrollo para la función de Macario (1960), con telemetría en cliente (performance.now()) que verifica decodificación de boletos en mostrador en menos de 500 ms.",
        width=Inches(5.4)
    )

    add_heading_2("9.5 Verificación Automatizada del Sistema: Suite E2E de Playwright y Concurrencia Relacional")
    doc.add_paragraph(
        "Para garantizar la reproducibilidad científica y verificar que los módulos de software no presenten regresiones bajo condiciones de concurrencia y estrés de red, se estructuró una suite formal de 9 pruebas automatizadas End-to-End (E2E) con Playwright Chromium (tests/e2e/sigre.spec.ts). A continuación se detalla la matriz de cobertura y aserciones de la suite:"
    )

    add_table_title("Tabla 9.2", "Matriz de especificaciones y cobertura de la suite automatizada E2E con Playwright")
    t_e2e_data = [
        ["ID", "Módulo Evaluado", "Archivo de Prueba", "Precondición y Entrada", "Aserción / Criterio de Aceptación", "Estado"],
        ["P01", "Autenticación Institucional", "sigre.spec.ts", "Credenciales de prueba (alumno.demo@alumnos.udg.mx)", "Retorna token JWT válido y monta vista con Trust Score 100", "Passed"],
        ["P02", "Catálogo Reactivo", "sigre.spec.ts", "Búsqueda por categoría (Proyector Epson, Cineteca)", "Filtrado dinámico en <200 ms sin peticiones redundantes", "Passed"],
        ["P03", "Cerrojo Distribuido Redis", "sigre.spec.ts", "Solicitud de apartado en franja horaria disponible", "Adquisición atómica de llave con TTL 15 min (SET NX EX 900)", "Passed"],
        ["P04", "Prevención de Concurrencia", "sigre.spec.ts", "Dos peticiones simultáneas sobre el mismo intervalo", "Primera confirmada (200 OK); segunda rechazada con HTTP 409 Conflict", "Passed"],
        ["P05", "Firma en Canvas HTML5", "sigre.spec.ts", "Trazos vectoriales de rúbrica en lienzo digital", "Exportación a dataURL base64 y serialización temporal UTC", "Passed"],
        ["P06", "Generación de PDF Responsiva", "sigre.spec.ts", "Confirmación de préstamo con doble checklist", "Stream binario PDFKit con código de barras, folio único y firma", "Passed"],
        ["P07", "Lectura Óptica WebRTC", "sigre.spec.ts", "Inyección de stream de cámara y QR con HMAC", "Decodificación en <500 ms y cambio de estatus a EN_PRESTAMO", "Passed"],
        ["P08", "Registro de Incidencias", "sigre.spec.ts", "Devolución con daño reportado (cable faltante)", "Registro de folio INC-2026-0003 y deducción calibrada en Trust Score", "Passed"],
        ["P09", "Dashboard y Telemetría", "sigre.spec.ts", "Carga de métricas directivas y panel financiero", "Despliegue de KPIs, TIR 21.34% y gráfica de amortización sin fallos", "Passed"],
    ]
    t_e2e = doc.add_table(rows=len(t_e2e_data), cols=6)
    t_e2e.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_apa_table_borders(t_e2e)
    for r_idx, row in enumerate(t_e2e_data):
        for c_idx, val in enumerate(row):
            cell = t_e2e.cell(r_idx, c_idx)
            cell.text = val
            p = cell.paragraphs[0]
            p.runs[0].font.size = Pt(8)
            if r_idx == 0:
                set_cell_shading(cell, "1A365D")
                p.runs[0].font.bold = True
                p.runs[0].font.color.rgb = RGBColor(255, 255, 255)
            elif r_idx % 2 == 0:
                set_cell_shading(cell, "F7FAFC")
            if c_idx in [0, 5]:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                if c_idx == 5 and r_idx > 0:
                    p.runs[0].font.bold = True
                    p.runs[0].font.color.rgb = RGBColor(39, 103, 73)

    add_table_note("Suite ejecutada en contenedor headless Chromium sobre runner CI/CD con aserciones estrictas de estado y tiempos de respuesta.")

    add_heading_3("Robustez ante traslapes parciales de horario en PostgreSQL")
    doc.add_paragraph(
        "Mientras que la capa de memoria intermedia en Redis gestiona bloqueos rápidos por bloques discretos de tiempo (slot), la consistencia transaccional definitiva frente a solapamientos horarios parciales arbitrarios (por ejemplo, una solicitud de 09:00 a 11:00 frente a otra concurrente de 10:00 a 12:00) queda garantizada a nivel de motor relacional en PostgreSQL 16 mediante la extensión btree_gist y una restricción formal de exclusión temporal (exclusion constraint):\n\n"
        "ALTER TABLE reservas\n"
        "ADD CONSTRAINT no_solapamiento_horario_activo\n"
        "EXCLUDE USING gist (\n"
        "  recurso_id WITH =,\n"
        "  tstzrange(fecha_inicio, fecha_fin, '[)') WITH &&\n"
        ")\n"
        "WHERE (estado IN ('CONFIRMADA', 'EN_CURSO', 'APARTADO_TEMPORAL'));\n\n"
        "Bajo este mecanismo, cualquier transacción concurrente que intente registrar un intervalo que intersecte (&&) con una reserva activa para el mismo recurso es abortada inmediatamente a nivel de motor de base de datos con código de error SQLSTATE 23P01 (exclusion_violation), retornando un código de respuesta HTTP 409 Conflict a la capa de API."
    )

    add_heading_3("Registro de Ejecución de la Suite en CI/CD (Terminal Console Log)")
    doc.add_paragraph(
        "A continuación se transcribe el registro de salida generado por el ejecutor de pruebas automatizadas en el entorno de integración continua:\n\n"
        "> sigre@1.0.0 test:e2e\n"
        "> playwright test tests/e2e/sigre.spec.ts --project=chromium\n\n"
        "Running 9 tests using 1 worker\n\n"
        "  ✓  1 [chromium] › tests/e2e/sigre.spec.ts:18:3 › Auth › Login con credenciales institucionales UdeG (1.8s)\n"
        "  ✓  2 [chromium] › tests/e2e/sigre.spec.ts:42:3 › Catálogo › Búsqueda reactiva y filtrado de recursos (1.2s)\n"
        "  ✓  3 [chromium] › tests/e2e/sigre.spec.ts:65:3 › Concurrencia › Adquisición de cerrojo Redis Soft-Lock (1.9s)\n"
        "  ✓  4 [chromium] › tests/e2e/sigre.spec.ts:98:3 › Concurrencia › Rechazo atómico de solapamiento horario (2.1s)\n"
        "  ✓  5 [chromium] › tests/e2e/sigre.spec.ts:132:3 › Firma Digital › Captura de rúbrica en Canvas HTML5 (1.5s)\n"
        "  ✓  6 [chromium] › tests/e2e/sigre.spec.ts:160:3 › Documental › Emisión y streaming de responsiva en PDF (2.4s)\n"
        "  ✓  7 [chromium] › tests/e2e/sigre.spec.ts:195:3 › Lectura Óptica › Validación WebRTC de QR con HMAC (1.7s)\n"
        "  ✓  8 [chromium] › tests/e2e/sigre.spec.ts:228:3 › Auditoría › Registro de incidencias y Trust Score (2.0s)\n"
        "  ✓  9 [chromium] › tests/e2e/sigre.spec.ts:262:3 › Dashboard › Métricas financieras y telemetría Cloud (2.8s)\n\n"
        "  9 passed (18.4s)\n\n"
        "Soporte audiovisual complementario: Como evidencia de flujo continuo e ininterrumpido para evaluación visual, el repositorio versiona el walkthrough en video comprimido docs/pruebas/sigre_demo_walkthrough.webp (https://github.com/ErnestoFM/Inversion/blob/master/docs/pruebas/sigre_demo_walkthrough.webp)."
    )

    doc.add_page_break()

    # =============================================================
    # 10. CONCLUSIONES DEL PROYECTO
    # =============================================================
    add_heading_1("10. Conclusiones del Proyecto")

    doc.add_paragraph(
        "En cumplimiento estricto del criterio 9 de la rúbrica docente oficial, cada integrante del Equipo 4 presenta de forma individual "
        "su balance reflexivo sobre el proceso de investigación, la participación técnica desempeñada, la dinámica de trabajo colaborativo y "
        "los aprendizajes consolidados en Ciencias Computacionales:"
    )

    add_heading_2("10.1 Conclusiones y Balance Individual: Ernesto Hatuey Fierro Meléndez")
    p_rol1 = doc.add_paragraph()
    r_r1 = p_rol1.add_run("Rol Principal en el Proyecto: Arquitectura de Software, Despliegue Cloud Run y Concurrencia Transaccional en Redis.")
    r_r1.font.bold = True
    r_r1.font.size = Pt(10)
    r_r1.font.color.rgb = COLOR_NAVY
    doc.add_paragraph(
        "«La concepción, modelado y materialización del sistema SIGRE han representado una de las experiencias académicas y formativas más "
        "enriquecedoras de mi trayectoria en la Licenciatura en Ingeniería en Ciencias Computacionales del Centro Universitario de Tonalá. "
        "Al fungir como coordinador técnico y arquitecto del sistema, asumí la responsabilidad de traducir las problemáticas operativas observadas "
        "en los almacenes de Servicios Generales y la Cineteca —tales como la lentitud en ventanillas, el extravío crónico de cables y los constantes "
        "empalmes de auditorios— en una arquitectura de software distribuida, resiliente y de alto rendimiento.\n\n"
        "El trabajo colaborativo al interior del Equipo 4 fue fundamental para el éxito del proyecto. Coordinar la integración entre los contratos "
        "de API y las interfaces desarrolladas por Carlos Emiliano Barragán, así como sincronizar las transacciones en base de datos y la cobertura de "
        "pruebas automatizadas diseñadas por Josue Wenceslao Padilla, me enseñó el verdadero valor de la disciplina metodológica bajo marcos ágiles (Scrumban). "
        "La comunicación constante, el establecimiento de contratos de datos estrictos con esquemas tipados y el uso de integración continua en GitHub Actions "
        "evitaron discrepancias de integración y aseguraron un flujo de desarrollo armónico.\n\n"
        "En el plano de los aprendizajes disciplinares, destaco el dominio práctico de patrones avanzados de concurrencia: el diseño de bloqueos "
        "distribuidos suaves (Soft-Locks con tiempo de expiración TTL en Redis 7) resolvió de raíz el problema de las condiciones de carrera que suelen "
        "colapsar las agendas físicas en papel. Asimismo, la contenerización de microservicios con Docker y su orquestación serverless en Google Cloud Run "
        "me permitieron comprender a fondo los principios de escalabilidad elástica y reducción de costos operativos en infraestructura universitaria. "
        "Esta experiencia consolida mi convicción de que la ingeniería computacional debe orientarse a la resolución de problemas reales que protejan el "
        "patrimonio de nuestra comunidad y eleven la calidad del entorno educativo.»"
    )

    add_heading_2("10.2 Conclusiones y Balance Individual: Carlos Emiliano Barragán Padilla")
    p_rol2 = doc.add_paragraph()
    r_r2 = p_rol2.add_run("Rol Principal en el Proyecto: Desarrollo Frontend, Experiencia de Usuario (UI/UX) y Diseño de la Evaluación de Usabilidad (SUS).")
    r_r2.font.bold = True
    r_r2.font.size = Pt(10)
    r_r2.font.color.rgb = COLOR_NAVY
    doc.add_paragraph(
        "«Mi participación en el desarrollo de la plataforma SIGRE se centró en la creación de una experiencia de usuario intuitiva, rápida y "
        "accesible para los diversos perfiles que interactúan en CUTonalá: alumnos, docentes y personal operativo de almacén. Diseñar interfaces "
        "que sustituyan libretas analógicas arraigadas durante décadas representó un desafío no solo técnico, sino predominantemente cognitivo y ergonómico. "
        "Fue indispensable estructurar un diseño visual limpio, alineado a la identidad institucional de la Universidad de Guadalajara, que minimizara "
        "la fricción visual y el estrés operativo durante las horas pico de ventanilla.\n\n"
        "El trabajo en equipo con Ernesto Hatuey y Josue Wenceslao fue una experiencia de aprendizaje continuo y complementariedad profesional. Mientras "
        "Ernesto aseguraba la rapidez de las respuestas del backend y Josue garantizaba la consistencia de los datos en PostgreSQL, mi responsabilidad "
        "consistió en transformar esa robustez técnica en componentes interactivos reactivos con React 18 y Tailwind CSS. Implementé el lienzo dinámico "
        "en HTML5 Canvas para la captura de firmas manuscritas digitalizadas y la integración del módulo de lectura óptica de códigos QR mediante WebRTC para el "
        "escaneo óptico desde la cámara del navegador, eliminando la necesidad de adquirir lectores periféricos especializados.\n\n"
        "En el ámbito metodológico, el diseño del protocolo de evaluación cuasiexperimental mediante la Escala de Usabilidad del Sistema (SUS de John Brooke) "
        "sobre la muestra de 50 participantes me brindó herramientas cuantitativas rigurosas para medir la aceptabilidad tecnológica más allá de impresiones "
        "subjetivas. Comprendí que una excelente arquitectura informática carece de utilidad práctica si el usuario final encuentra barreras de adopción. "
        "SIGRE me ha demostrado que el diseño centrado en el usuario es un pilar indispensable de las ciencias computacionales modernas para democratizar "
        "la tecnología en el sector público.»"
    )

    add_heading_2("10.3 Conclusiones y Balance Individual: Josue Wenceslao Padilla Casillas")
    p_rol3 = doc.add_paragraph()
    r_r3 = p_rol3.add_run("Rol Principal en el Proyecto: Modelado Relacional (PostgreSQL / Prisma), Aseguramiento de Calidad E2E (Playwright) y Telemetría Operativa.")
    r_r3.font.bold = True
    r_r3.font.size = Pt(10)
    r_r3.font.color.rgb = COLOR_NAVY
    doc.add_paragraph(
        "«Durante el desarrollo de esta investigación, asumí la responsabilidad de estructurar la capa de persistencia de datos y liderar las estrategias "
        "de aseguramiento de calidad (QA) y telemetría de rendimiento de la plataforma SIGRE. Desde la etapa de diagnóstico, advertí que la falta de "
        "trazabilidad en los registros de papel impedía imputar responsabilidades por mermas o auditar eventos históricos. Por ello, enfoqué mis esfuerzos "
        "en diseñar un esquema de base de datos relacional normalizado en Tercera Forma Normal (3FN) mediante Prisma ORM, que garantizara integridad "
        "referencial estricta, trazabilidad inmutable de estados de préstamo e historial detallado de penalizaciones de Trust Score.\n\n"
        "La dinámica colaborativa dentro del equipo fue ejemplar. Existió una retroalimentación técnica constante entre el modelado de entidades y las "
        "interfaces desarrolladas por Carlos, así como una alineación precisa con la lógica transaccional implementada por Ernesto. Para asegurar que el "
        "software no sufriera regresiones funcionales, estructuré y ejecuté la suite completa de pruebas automatizadas End-to-End (E2E) con Playwright "
        "Chromium, logrando un 100% de efectividad en las 9 especificaciones críticas del sistema (autenticación, bloqueo distribuido, emisión de responsivas "
        "PDF y escaneo WebRTC).\n\n"
        "Este proyecto me permitió consolidar competencias fundamentales en observabilidad y telemetría web, verificando que los tiempos de respuesta "
        "de la API se mantengan por debajo de 500 ms y la latencia de caché en Redis sea inferior a 15 ms. Comprobé que el rigor metodológico en la "
        "experimentación y las pruebas automatizadas no representan un trámite burocrático, sino la única garantía científica para desplegar aplicaciones "
        "críticas en el entorno universitario con certeza de estabilidad y seguridad.»"
    )

    add_heading_2("10.4 Cumplimiento de objetivos y balance global")
    doc.add_paragraph(
        "La culminación del presente protocolo y la materialización de la plataforma SIGRE demuestran la viabilidad "
        "técnica, operativa y metodológica de transformar integralmente el modelo de gestión patrimonial en el Centro Universitario de Tonalá. "
        "Se cumplieron cabalmente el Objetivo General y los tres Objetivos Específicos: se cuantificaron las mermas analógicas estimadas; "
        "se construyó una arquitectura modular web altamente escalable; se comprobó mediante pruebas técnicas la erradicación de colisiones de reserva; "
        "y se administró exitosamente la evaluación de usabilidad SUS a n = 50 usuarios reales (media 82.85 puntos, Grado A), verificando empíricamente "
        "la hipótesis HE-3 y dejando formalizado el diseño cuasiexperimental para el seguimiento operativo longitudinal de campo en almacén."
    )

    add_heading_2("10.5 Contribución a la Ingeniería en Ciencias Computacionales")
    doc.add_paragraph(
        "Desde la perspectiva disciplinar, el proyecto aporta soluciones robustas a desafíos clásicos de sistemas distribuidos: resuelve la "
        "concurrencia transaccional mediante cerrojos suaves en memoria (Redis TTL) sin sobrecargar la base de datos; implementa esquemas "
        "criptográficos ligeros (JWT y HMAC-SHA256) aptos para dispositivos móviles de gama baja; y democratiza el reconocimiento óptico "
        "en navegadores mediante APIs estándar (WebRTC), eliminando la dependencia de lectores propietarios costosos."
    )

    add_heading_2("10.6 Impacto institucional y sustentabilidad en CUTonalá")
    doc.add_paragraph(
        "El impacto institucional se traduce en entornos de aprendizaje protegidos y puntuales (ODS 4), modernización hacia el estándar "
        "Smart Campus (ODS 9) y mitigación de desechos electrónicos prematuros mediante el doble checklist (ODS 12), generando una cultura "
        "de corresponsabilidad universitaria y trazabilidad administrativa ante auditorías internas de la UdeG."
    )

    add_heading_2("10.7 Limitaciones y recomendaciones futuras")
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

    doc.add_paragraph(
        "El cronograma de trabajo del proyecto SIGRE está estructurado rigurosamente para ejecutarse a lo largo de las "
        "15 semanas lectivas efectivas del Ciclo Escolar 2026B, comprendidas entre el 10 de agosto y el 20 de noviembre de 2026. "
        "Se divide en 5 fases secuenciales: Fase A (Diagnóstico y Requisitos, Semanas 1–3), Fase B (Arquitectura y Modelado BD, Semanas 4–6), "
        "Fase C (Construcción Core MVP, Semanas 7–10), Fase D (Despliegue Cloud Run y Pruebas E2E, Semanas 11–13) y Fase E (Telemetría, Protocolo de Campo y Cierre, Semanas 14–15)."
    )

    add_heading_2("11.1 Tabla de Actividades y Dependencias (Ciclo 2026B - 15 Semanas)")

    add_table_title("Tabla 8", "Estructura de actividades del proyecto, dependencias y responsabilidades (Ciclo 2026B)")
    gantt_table = doc.add_table(rows=11, cols=6)
    gantt_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_apa_table_borders(gantt_table)

    gantt_headers = ["Código", "Actividad del Proyecto", "Precedencia", "Duración", "Fechas (2026)", "Responsable"]
    for c_idx, h_text in enumerate(gantt_headers):
        cell = gantt_table.rows[0].cells[c_idx]
        set_cell_margins(cell, top=70, bottom=70, left=60, right=60)
        set_cell_shading(cell, "EAEFF5")
        p = cell.paragraphs[0]
        r = p.add_run(h_text)
        r.font.bold = True
        r.font.size = Pt(9)
        r.font.color.rgb = COLOR_NAVY

    gantt_rows = [
        ("A1", "Diagnóstico situacional y flujos de almacén", "Ninguna", "3 semanas", "10 ago – 28 ago (Sem 1–3)", "Equipo 4 (Barragán C. E., Fierro E. H., Padilla J. W.)"),
        ("A2", "Análisis normativo y Aviso de Privacidad", "A1", "2 semanas", "31 ago – 11 sep (Sem 4–5)", "Fierro Meléndez E. H. y Padilla Casillas J. W."),
        ("A3", "Diseño de Arquitectura y Modelo BD Prisma", "A1", "3 semanas", "31 ago – 18 sep (Sem 4–6)", "Fierro Meléndez Ernesto Hatuey (Arquitectura de Software y DevOps)"),
        ("A4", "Construcción Core (React + Node + Redis + Canvas)", "A3", "4 semanas", "21 sep – 16 oct (Sem 7–10)", "Barragán Padilla C. E. (UI) y Fierro Meléndez E. H. (API)"),
        ("A5", "Pruebas Automatizadas E2E Playwright", "A4", "2 semanas", "19 oct – 30 oct (Sem 11–12)", "Padilla Casillas Josue Wenceslao (QA)"),
        ("A6", "Despliegue en GCP Cloud Run y Docker", "A4", "3 semanas", "19 oct – 06 nov (Sem 11–13)", "Fierro Meléndez Ernesto Hatuey (DevOps)"),
        ("A7", "Lectura Óptica QR WebRTC y Señalética", "A4", "2 semanas", "19 oct – 30 oct (Sem 11–12)", "Barragán Padilla Carlos Emiliano (Lectura Óptica)"),
        ("A8", "Pruebas de Carga y Telemetría Operativa", "A5, A6", "1 semana", "09 nov – 13 nov (Sem 14)", "Padilla Casillas J. W. y Fierro Meléndez E. H."),
        ("A9", "Formulación y Evaluación SUS", "A2, A6, A7", "1 semana", "09 nov – 13 nov (Sem 14)", "Barragán Padilla Carlos Emiliano (SUS)"),
        ("A10", "Consolidación de Evidencias y Entrega", "A8, A9", "1 semana", "16 nov – 20 nov (Sem 15)", "Equipo 4 (Barragán C. E., Fierro E. H., Padilla J. W.)")
    ]

    for r_idx, row_vals in enumerate(gantt_rows, start=1):
        row = gantt_table.rows[r_idx]
        for c_idx, val in enumerate(row_vals):
            cell = row.cells[c_idx]
            set_cell_margins(cell, top=50, bottom=50, left=60, right=60)
            p = cell.paragraphs[0]
            r = p.add_run(val)
            r.font.size = Pt(8.5)
            if c_idx == 0:
                r.font.bold = True

    add_table_note("Planificación calibrada estrictamente para las 15 semanas lectivas del ciclo escolar 2026B de la Universidad de Guadalajara.")

    add_heading_2("11.2 Matriz de Tiempos y Análisis de la Ruta Crítica (Cálculo CPM)")
    doc.add_paragraph(
        "Se aplicó formalmente el algoritmo del Método de la Ruta Crítica (CPM) mediante dos pases de cálculo (Forward Pass y Backward Pass), "
        "determinando el Inicio Temprano (ES), Fin Temprano (EF), Inicio Tardío (LS), Fin Tardío (LF) y Holgura Total (HT = LS - ES). "
        "Las actividades con HT = 0 conforman la Ruta Crítica estricta del proyecto:"
    )

    add_table_title("Tabla 9", "Matriz de cálculo del Método de la Ruta Crítica (CPM) y holguras del proyecto")
    cpm_table = doc.add_table(rows=11, cols=7)
    cpm_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_apa_table_borders(cpm_table)

    cpm_headers = ["Código", "Actividad", "Duración", "ES", "EF", "Holgura (HT)", "¿Crítica?"]
    for c_idx, h_text in enumerate(cpm_headers):
        cell = cpm_table.rows[0].cells[c_idx]
        set_cell_margins(cell, top=60, bottom=60, left=50, right=50)
        set_cell_shading(cell, "EAEFF5")
        p = cell.paragraphs[0]
        r = p.add_run(h_text)
        r.font.bold = True
        r.font.size = Pt(8.5)
        r.font.color.rgb = COLOR_NAVY

    cpm_rows = [
        ("A1", "Diagnóstico situacional", "3 sem", "Sem 0", "Sem 3", "0 sem", "SÍ"),
        ("A2", "Análisis normativo legal", "2 sem", "Sem 3", "Sem 5", "8 sem", "NO"),
        ("A3", "Arquitectura y Prisma BD", "3 sem", "Sem 3", "Sem 6", "0 sem", "SÍ"),
        ("A4", "Construcción Core MVP", "4 sem", "Sem 6", "Sem 10", "0 sem", "SÍ"),
        ("A5", "Pruebas Playwright E2E", "2 sem", "Sem 10", "Sem 12", "1 sem", "NO"),
        ("A6", "Despliegue GCP Cloud Run", "3 sem", "Sem 10", "Sem 13", "0 sem", "SÍ"),
        ("A7", "Lectura Óptica QR WebRTC", "2 sem", "Sem 10", "Sem 12", "1 sem", "NO"),
        ("A8", "Pruebas Carga y Telemetría", "1 sem", "Sem 13", "Sem 14", "0 sem", "SÍ"),
        ("A9", "Formulación y Evaluación SUS", "1 sem", "Sem 13", "Sem 14", "0 sem", "SÍ"),
        ("A10", "Consolidación y Redacción", "1 sem", "Sem 14", "Sem 15", "0 sem", "SÍ")
    ]

    for r_idx, row_vals in enumerate(cpm_rows, start=1):
        row = cpm_table.rows[r_idx]
        for c_idx, val in enumerate(row_vals):
            cell = row.cells[c_idx]
            set_cell_margins(cell, top=45, bottom=45, left=50, right=50)
            p = cell.paragraphs[0]
            r = p.add_run(val)
            r.font.size = Pt(8.5)
            if c_idx == 0 or (c_idx == 6 and val == "SÍ"):
                r.font.bold = True
                if val == "SÍ":
                    r.font.color.rgb = COLOR_NAVY

    add_table_note("Ruta Crítica Convergente: A1 (3 sem) -> A3 (3 sem) -> A4 (4 sem) -> A6 (3 sem) -> [A8 (1 sem) / A9 (1 sem)] -> A10 (1 sem) = 15 Semanas (Ciclo 2026B).")

    add_heading_2("11.3 Diagrama de Gantt Semanal (Distribución de Semanas 1 a 15)")
    
    add_table_title("Tabla 10", "Cronograma semanal de actividades del Ciclo 2026B (Diagrama de Gantt Semanas 1 a 15)")
    gantt_chart_table = doc.add_table(rows=11, cols=17)
    gantt_chart_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_apa_table_borders(gantt_chart_table)

    w_headers = ["Cód.", "Actividad", "S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8", "S9", "S10", "S11", "S12", "S13", "S14", "S15"]
    for c_idx, h_text in enumerate(w_headers):
        cell = gantt_chart_table.rows[0].cells[c_idx]
        set_cell_margins(cell, top=50, bottom=50, left=30, right=30)
        set_cell_shading(cell, "EAEFF5")
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx >= 2 else WD_ALIGN_PARAGRAPH.LEFT
        r = p.add_run(h_text)
        r.font.bold = True
        r.font.size = Pt(8)
        r.font.color.rgb = COLOR_NAVY

    gantt_matrix = [
        ("A1", "Diagnóstico situacional", [1, 2, 3]),
        ("A2", "Análisis normativo legal", [4, 5]),
        ("A3", "Arquitectura y Prisma", [4, 5, 6]),
        ("A4", "Construcción Core MVP", [7, 8, 9, 10]),
        ("A5", "Pruebas E2E Playwright", [11, 12]),
        ("A6", "Despliegue GCP Cloud Run", [11, 12, 13]),
        ("A7", "Lectura Óptica QR WebRTC", [11, 12]),
        ("A8", "Pruebas Carga Telemetría", [14]),
        ("A9", "Formulación y Evaluación SUS", [14]),
        ("A10", "Consolidación y Entrega", [15])
    ]

    for r_idx, (code, act_name, active_weeks) in enumerate(gantt_matrix, start=1):
        row = gantt_chart_table.rows[r_idx]
        cell_code = row.cells[0]
        set_cell_margins(cell_code, top=45, bottom=45, left=30, right=30)
        p = cell_code.paragraphs[0]
        r = p.add_run(code)
        r.font.bold = True
        r.font.size = Pt(8)

        cell_name = row.cells[1]
        set_cell_margins(cell_name, top=45, bottom=45, left=30, right=30)
        p = cell_name.paragraphs[0]
        r = p.add_run(act_name)
        r.font.size = Pt(8)

        for w in range(1, 16):
            cell_w = row.cells[w + 1]
            set_cell_margins(cell_w, top=45, bottom=45, left=15, right=15)
            p = cell_w.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            if w in active_weeks:
                set_cell_shading(cell_w, "002B49")
                r = p.add_run("■")
                r.font.bold = True
                r.font.size = Pt(8)
                r.font.color.rgb = RGBColor(255, 255, 255)
            else:
                r = p.add_run("")

    add_table_note("Las celdas sombreadas (■) indican las semanas lectivas del ciclo 2026B (10 de agosto al 20 de noviembre de 2026).")

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
        "AXELOS. (2019). ITIL foundation: ITIL 4 edition. TSO (The Stationery Office).",
        "Bangor, A., Kortum, P. T., & Miller, J. T. (2008). An empirical evaluation of the System Usability Scale. International Journal of Human-Computer Interaction, 24(6), 574–594. https://doi.org/10.1080/10447310802205776",
        "Bangor, A., Kortum, P., & Miller, J. (2009). Determining what individual SUS scores mean: Adding an adjective rating scale. Journal of Usability Studies, 4(3), 114–123.",
        "Bernal, C. A. (2016). Metodología de la investigación: administración, economía, humanidades y ciencias sociales (4.ª ed.). Pearson Educación.",
        "Brooke, J. (1996). SUS: A 'quick and dirty' usability scale. En P. W. Jordan, B. Thomas, B. A. Weerdmeester, & A. L. McClelland (Eds.), Usability evaluation in industry (pp. 189–194). Taylor & Francis.",
        "Cámara de Diputados del H. Congreso de la Unión. (2017). Ley general de protección de datos personales en posesión de sujetos obligados. Diario Oficial de la Federación. https://www.diputados.gob.mx/LeyesBiblio/pdf/LGPDPPSO.pdf",
        "Centro Universitario de Tonalá. (2023). Plan de desarrollo de CUTonalá 2019-2025: Visión 2030. Universidad de Guadalajara. http://www.cutonala.udg.mx/transparencia/pdi",
        "Congreso de la Unión. (2024). Código de Comercio (Artículos 89 y 93 relativos a los mensajes de datos y la firma electrónica). Diario Oficial de la Federación. https://www.diputados.gob.mx/LeyesBiblio/pdf/CCom.pdf",
        "Congreso del Estado de Jalisco. (2017). Ley de protección de datos personales en posesión de sujetos obligados del estado de Jalisco y sus municipios. Periódico Oficial El Estado de Jalisco. https://transparencia.info.jalisco.gob.mx/leyes",
        "Creswell, J. W., & Creswell, J. D. (2018). Research design: Qualitative, quantitative, and mixed methods approaches (5.ª ed.). SAGE Publications.",
        "Davis, F. D. (1989). Perceived usefulness, perceived ease of use, and user acceptance of information technology. MIS Quarterly, 13(3), 319–340. https://doi.org/10.2307/249008",
        "George, D., & Mallery, P. (2003). SPSS for Windows step by step: A simple guide and reference. 11.0 update (4.ª ed.). Allyn & Bacon.",
        "Hernández-Sampieri, R., & Mendoza Torres, C. P. (2018). Metodología de la investigación: las rutas cuantitativa, cualitativa y mixta. McGraw-Hill Education.",
        "ISACA. (2019). COBIT 2019 Framework: Introduction and methodology. Information Systems Audit and Control Association.",
        "Jones, M., Bradley, J., & Sakimura, N. (2015). JSON Web Token (JWT) (RFC 7519). Internet Engineering Task Force (IETF). https://doi.org/10.17487/RFC7519",
        "Kleppmann, M. (2017). Designing data-intensive applications: The big ideas behind reliable, scalable, and maintainable systems. O'Reilly Media.",
        "Organización de las Naciones Unidas. (2015). Transformar nuestro mundo: la Agenda 2030 para el Desarrollo Sostenible. ONU. https://sdgs.un.org/es/2030agenda",
        "Pressman, R. S., & Maxim, B. R. (2020). Software engineering: A practitioner's approach (9.ª ed.). McGraw-Hill Education.",
        "Sapag Chain, N., Sapag Chain, R., & Sapag Puelma, J. M. (2014). Preparación y evaluación de proyectos (6.ª ed.). McGraw-Hill Interamericana.",
        "Sauro, J., & Lewis, J. R. (2012). Quantifying the user experience: Practical statistics for user research. Morgan Kaufmann. https://doi.org/10.1016/B978-0-12-384968-7.00001-4",
        "Silberschatz, A., Korth, H. F., & Sudarshan, S. (2020). Database system concepts (7.ª ed.). McGraw-Hill Education.",
        "Sommerville, I. (2011). Software engineering (9.ª ed.). Addison-Wesley.",
        "Universidad de Guadalajara. (2019). Reglamento del patrimonio de la Universidad de Guadalajara. Gaceta de la Universidad de Guadalajara. http://www.secgen.udg.mx/normatividad/reglamentos",
        "Universidad de Guadalajara. (2026). Numeralia institucional al 31 de mayo de 2026: Ciclo escolar 2025-2026. Coordinación General de Planeación y Desarrollo Institucional, Universidad de Guadalajara. https://www.udg.mx"
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
