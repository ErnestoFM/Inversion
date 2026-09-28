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
    # Colores y Tipografía
    # -------------------------------------------------------------
    COLOR_BLACK = RGBColor(0, 0, 0)
    COLOR_NAVY = RGBColor(0, 43, 73)      # #002B49 Institucional UdeG
    COLOR_ACCENT = RGBColor(0, 102, 153)  # #006699
    COLOR_TEXT = RGBColor(33, 37, 41)     # #212529
    COLOR_MUTED = RGBColor(108, 117, 125) # #6C757D
    
    style_normal = doc.styles['Normal']
    style_normal.font.name = 'Calibri'
    style_normal.font.size = Pt(12)
    style_normal.font.color.rgb = COLOR_TEXT
    style_normal.paragraph_format.line_spacing = 1.2
    style_normal.paragraph_format.space_after = Pt(7)
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
        
        # Borde inferior de la fila de encabezado
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
        p.paragraph_format.space_before = Pt(20)
        p.paragraph_format.space_after = Pt(8)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Calibri'
        run.font.size = Pt(16)
        run.font.bold = True
        run.font.color.rgb = COLOR_NAVY
        return p

    def add_heading_2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Calibri'
        run.font.size = Pt(13.5)
        run.font.bold = True
        run.font.color.rgb = COLOR_ACCENT
        return p

    def add_heading_3(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Calibri'
        run.font.size = Pt(12)
        run.font.bold = True
        run.font.italic = True
        run.font.color.rgb = COLOR_TEXT
        return p

    def add_callout(title, text):
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = tbl.cell(0, 0)
        cell.width = Inches(6.5)
        set_cell_margins(cell, top=100, bottom=100, left=140, right=140)
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
        r_tit.font.size = Pt(11.5)
        r_tit.font.color.rgb = COLOR_NAVY
        r_txt = p.add_run(text)
        r_txt.font.size = Pt(11)
        r_txt.font.italic = True
        r_txt.font.color.rgb = COLOR_TEXT
        
        p_sp = doc.add_paragraph()
        p_sp.paragraph_format.space_after = Pt(6)

    # =============================================================
    # 1. PORTADA FORMAL (Estricta según plantilla oficial)
    # =============================================================
    p_inst = doc.add_paragraph()
    p_inst.paragraph_format.space_before = Pt(15)
    p_inst.paragraph_format.space_after = Pt(3)
    p_inst.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_inst = p_inst.add_run("UNIVERSIDAD DE GUADALAJARA")
    r_inst.font.bold = True
    r_inst.font.size = Pt(15)
    r_inst.font.color.rgb = COLOR_NAVY

    p_campus = doc.add_paragraph()
    p_campus.paragraph_format.space_after = Pt(18)
    p_campus.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_campus = p_campus.add_run("Centro Universitario de Tonalá (CUTonalá)\nDivisión de Ingenierías e Innovación Tecnológica")
    r_campus.font.size = Pt(12)
    r_campus.font.color.rgb = COLOR_MUTED

    p_doc_type = doc.add_paragraph()
    p_doc_type.paragraph_format.space_after = Pt(6)
    p_doc_type.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_doc_type = p_doc_type.add_run("PROTOCOLO DE INVESTIGACIÓN APLICADA")
    r_doc_type.font.bold = True
    r_doc_type.font.size = Pt(13)
    r_doc_type.font.color.rgb = COLOR_ACCENT

    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_after = Pt(12)
    p_title.paragraph_format.line_spacing = 1.15
    p_title.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_title = p_title.add_run("SIGRE: Sistema Integrado de Gestión de Recursos y Espacios para la optimización del control patrimonial y reserva de infraestructura en CUTonalá")
    r_title.font.size = Pt(18)
    r_title.font.bold = True
    r_title.font.color.rgb = COLOR_NAVY

    p_div = doc.add_paragraph()
    p_div.paragraph_format.space_after = Pt(15)
    p_div.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_div = p_div.add_run("—" * 30)
    r_div.font.color.rgb = COLOR_ACCENT

    # Tabla formal de metadatos de portada
    add_table_title("Tabla 1", "Ficha técnica institucional del protocolo de investigación")
    cover_table = doc.add_table(rows=7, cols=2)
    cover_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_apa_table_borders(cover_table)

    cover_fields = [
        ("Licenciatura:", "Ingeniería en Ciencias Computacionales"),
        ("Materia:", "METODOLOGÍA Y PRÁCTICA DE LA INVESTIGACIÓN"),
        ("Ciclo Escolar:", "2026B"),
        ("Docente Titular:", "Mtra. Elizabeth Cristina Hernández Hernández"),
        ("Equipo de Trabajo:", "Equipo 4"),
        ("Integrantes:", "• Barragán Padilla Carlos Emiliano\n• Fierro Meléndez Ernesto Hatuey\n• Padilla Casillas Josue Wenceslao"),
        ("Fecha y Lugar de Elaboración:", "Septiembre de 2026 — Tonalá, Jalisco, México")
    ]

    for idx, (label, val) in enumerate(cover_fields):
        row = cover_table.rows[idx]
        c0, c1 = row.cells[0], row.cells[1]
        c0.width = Inches(2.3)
        c1.width = Inches(4.2)
        set_cell_margins(c0, top=60, bottom=60, left=80, right=80)
        set_cell_margins(c1, top=60, bottom=60, left=80, right=80)
        
        p0 = c0.paragraphs[0]
        r0 = p0.add_run(label)
        r0.font.bold = True
        r0.font.size = Pt(11)
        r0.font.color.rgb = COLOR_NAVY
        
        p1 = c1.paragraphs[0]
        r1 = p1.add_run(val)
        r1.font.size = Pt(11)
        r1.font.color.rgb = COLOR_TEXT

    add_table_note("Datos curriculares y especificación institucional conforme a la plantilla oficial de entrega.")

    p_ent = doc.add_paragraph()
    p_ent.paragraph_format.space_before = Pt(12)
    p_ent.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_ent = p_ent.add_run("Nombre del Entregable Oficial en Classroom: ")
    r_ent.font.size = Pt(10.5)
    r_ent.font.bold = True
    r_ent2 = p_ent.add_run("2026B_Equipo4_Protocolo.pdf")
    r_ent2.font.size = Pt(10.5)
    r_ent2.font.italic = True
    r_ent2.font.color.rgb = COLOR_ACCENT

    doc.add_page_break()

    # =============================================================
    # 2. ÍNDICE Y BREVE INTRODUCCIÓN
    # =============================================================
    add_heading_1("Índice General")

    toc_items = [
        ("1. Breve Introducción", "2"),
        ("2. Planteamiento del Problema", "3"),
        ("   2.1 Contexto institucional y operacional", "3"),
        ("   2.2 El colapso del modelo analógico de gestión", "3"),
        ("   2.3 Causas fundamentales de la problemática", "4"),
        ("   2.4 Consecuencias e impacto cuantificado en el campus", "4"),
        ("   2.5 Formulación de la pregunta de investigación", "4"),
        ("3. Justificación de la Investigación", "5"),
        ("   3.1 Relevancia institucional, operativa y académica", "5"),
        ("   3.2 Pertinencia en la Ingeniería en Ciencias Computacionales", "5"),
        ("   3.3 Alineación con los Objetivos de Desarrollo Sostenible (ODS 2030)", "6"),
        ("       3.3.1 ODS 4: Educación de Calidad (Meta 4.a)", "6"),
        ("       3.3.2 ODS 9: Industria, Innovación e Infraestructura (Metas 9.4 y 9.c)", "6"),
        ("       3.3.3 ODS 12: Producción y Consumo Responsables (Meta 12.5)", "6"),
        ("4. Objetivos de la Investigación", "7"),
        ("   4.1 Criterio metodológico y epistemológico de formulación", "7"),
        ("   4.2 Objetivo General", "7"),
        ("   4.3 Objetivos Específicos", "7"),
        ("       4.3.1 Objetivo Específico 1: Diagnóstico situacional y flujos operativos", "7"),
        ("       4.3.2 Objetivo Específico 2: Diseño arquitectónico y construcción de módulos", "8"),
        ("       4.3.3 Objetivo Específico 3: Implementación piloto y evaluación cuantitativa", "8"),
        ("   4.4 Matriz de Coherencia Metodológica de Objetivos", "8"),
        ("5. Referencias Bibliográficas (APA 7ma Edición)", "9")
    ]

    add_table_title("Tabla 2", "Estructura de contenidos del protocolo de investigación")
    toc_table = doc.add_table(rows=len(toc_items), cols=2)
    toc_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_apa_table_borders(toc_table)

    for idx, (section_title, page_num) in enumerate(toc_items):
        row = toc_table.rows[idx]
        c0, c1 = row.cells[0], row.cells[1]
        c0.width = Inches(5.5)
        c1.width = Inches(1.0)
        set_cell_margins(c0, top=35, bottom=35, left=60, right=60)
        set_cell_margins(c1, top=35, bottom=35, left=60, right=60)
        
        p0 = c0.paragraphs[0]
        p0.paragraph_format.line_spacing = 1.15
        p0.paragraph_format.space_after = Pt(0)
        r0 = p0.add_run(section_title)
        r0.font.size = Pt(10.5)
        if not section_title.startswith(" "):
            r0.font.bold = True
            r0.font.color.rgb = COLOR_NAVY
            
        p1 = c1.paragraphs[0]
        p1.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p1.paragraph_format.line_spacing = 1.15
        p1.paragraph_format.space_after = Pt(0)
        r1 = p1.add_run(page_num)
        r1.font.size = Pt(10.5)
        if not section_title.startswith(" "):
            r1.font.bold = True

    add_table_note("Estructura alineada a los requerimientos de la plantilla oficial hasta la sección de objetivos.")

    # Breve Introducción (Media cuartilla / ~220 palabras)
    add_heading_1("1. Breve Introducción")

    doc.add_paragraph(
        "El presente protocolo de investigación aborda el diseño, desarrollo e implementación de una solución tecnológica "
        "orientada a resolver una de las problemáticas operativas más recurrentes y costosas en las instituciones públicas "
        "de educación superior: la ineficiencia, vulnerabilidad y descontrol administrativo en la gestión de espacios físicos "
        "y el préstamo de equipamiento audiovisual y técnico. Tomando como caso de estudio representativo al Centro Universitario "
        "de Tonalá (CUTonalá) de la Universidad de Guadalajara, el proyecto titulado SIGRE (Sistema Integrado de Gestión de "
        "Recursos y Espacios) plantea la sustitución integral de los modelos analógicos tradicionales —basados en registros "
        "manuales en libretas de papel y acuerdos verbales dispersos— por un ecosistema digital distribuido, seguro y accesible "
        "vía plataforma web y dispositivos móviles."
    )

    doc.add_paragraph(
        "A través del rigor metodológico propio de la Ingeniería en Ciencias Computacionales, este protocolo articula un "
        "diagnóstico fundamentado en la observación directa en almacenes y áreas de Servicios Generales, formula los requerimientos "
        "técnicos indispensables, y alinea sus metas con la agenda global de sostenibilidad de la Organización de las Naciones Unidas "
        "(ODS 2030). El documento expone a continuación el planteamiento detallado del problema, su justificación institucional "
        "y social, y la estructura jerárquica de objetivos generales y específicos que guiarán la construcción y evaluación del software."
    )

    doc.add_page_break()

    # =============================================================
    # 3. PLANTEAMIENTO DEL PROBLEMA (Mínimo 1, Máximo 2 cuartillas)
    # =============================================================
    add_heading_1("2. Planteamiento del Problema")

    add_heading_2("2.1 Contexto institucional y operacional")
    doc.add_paragraph(
        "La Universidad de Guadalajara (UdeG) constituye la segunda red universitaria pública más grande e importante de México, "
        "brindando atención formativa a una matrícula global que supera los 330,000 estudiantes y empleando a más de 17,000 docentes "
        "distribuidos en centros temáticos, planteles regionales y escuelas preparatorias (Coordinación General de Planeación y "
        "Evaluación [CGPE], 2024). En particular, el Centro Universitario de Tonalá (CUTonalá) se ha consolidado como un polo de "
        "desarrollo multidisciplinario caracterizado por una infraestructura moderna que alberga licenciaturas e ingenierías de vanguardia, "
        "laboratorios de investigación, clínicas de ciencias de la salud y edificios multiaula diseñados bajo modelos educativos "
        "flexibles e híbridos (Centro Universitario de Tonalá [CUTonalá], 2023)."
    )
    doc.add_paragraph(
        "No obstante, este notable crecimiento de la infraestructura física convive cotidianamente con una severa contradicción operativa: "
        "mientras las aulas y auditorios se dotan de equipamiento audiovisual de última generación (pantallas interactivas, proyectores "
        "láser y sistemas de audio de alta fidelidad), los procesos administrativos destinados a solicitar, programar, prestar y "
        "custodiar dichos activos continúan dependiendo de procedimientos manuales que no han evolucionado en décadas."
    )

    add_heading_2("2.2 El colapso del modelo analógico de gestión")
    doc.add_paragraph(
        "En la dinámica diaria de los campus universitarios, la solicitud de proyectores móviles, cables HDMI, adaptadores multipuerto, "
        "micrófonos inalámbricos, apuntadores digitales y llaves de acceso a recintos especializados recae en ventanillas de atención "
        "gestionadas por personal de prefectura y Servicios Generales. La operación descansa casi exclusivamente en bitácoras físicas de "
        "papel, un modelo que presenta tres fallas estructurales críticas:"
    )

    p_b1 = doc.add_paragraph()
    p_b1.paragraph_format.left_indent = Inches(0.3)
    p_b1.paragraph_format.space_after = Pt(4)
    r_b1_t = p_b1.add_run("1. Vulnerabilidad documental e ilegibilidad: ")
    r_b1_t.font.bold = True
    p_b1.add_run(
        "Las anotaciones en libretas sufren deterioro continuo, hojas sueltas, manchas y caligrafía ilegible producida por las "
        "prisas en las horas pico de inicio de clase (7:00 a 8:00 hrs y 15:00 a 16:00 hrs), lo que imposibilita una auditoría clara."
    )

    p_b2 = doc.add_paragraph()
    p_b2.paragraph_format.left_indent = Inches(0.3)
    p_b2.paragraph_format.space_after = Pt(4)
    r_b2_t = p_b2.add_run("2. Desarticulación y empalmes de agenda: ")
    r_b2_t.font.bold = True
    p_b2.add_run(
        "La reserva de espacios académicos (auditorios, salas de juntas y aulas magnas) se tramita mediante oficios físicos, mensajes "
        "informales o acuerdos verbales entre coordinaciones. La falta de un calendario unificado propicia la duplicidad de eventos, "
        "empalmes de horarios y la suspensión repentina de actividades académicas programadas."
    )

    p_b3 = doc.add_paragraph()
    p_b3.paragraph_format.left_indent = Inches(0.3)
    p_b3.paragraph_format.space_after = Pt(6)
    r_b3_t = p_b3.add_run("3. Ruptura de la cadena de custodia patrimonial: ")
    r_b3_t.font.bold = True
    p_b3.add_run(
        "El préstamo se autoriza mediante una firma rápida en una libreta sin una inspección funcional documentada. Al devolver el material, "
        "es imposible comprobar técnica ni legalmente si un accesorio faltante o un desperfecto físico (puertos fundidos, cables trozados "
        "o lentes fracturados) ocurrió con el usuario actual o en turnos previos, impidiendo el deslinde de responsabilidades."
    )

    add_heading_2("2.3 Causas fundamentales de la problemática")
    doc.add_paragraph(
        "La persistencia de esta problemática no obedece a deficiencias individuales de los trabajadores, sino a factores estructurales "
        "bien identificados: primero, una causa técnico-operativa por la falta de un sistema digital centralizado que actualice el "
        "inventario en tiempo real; segundo, una causa jurídico-administrativa, ya que una libreta carece de validez probatoria ante la "
        "Ley General de Protección de Datos Personales en Posesión de Sujetos Obligados (Cámara de Diputados del H. Congreso de la Unión, "
        "2017) y el Reglamento de Adquisiciones y Patrimonio de la UdeG (2019); y tercero, una causa de gestión, debido a la nula "
        "existencia de un historial de reputación del usuario que premie la puntualidad o sancione la negligencia reiterada."
    )

    add_heading_2("2.4 Consecuencias e impacto cuantificado en el campus")
    doc.add_paragraph(
        "A partir de observaciones directas y testimonios de personal administrativo y docente en CUTonalá, las repercusiones de este "
        "vacío tecnológico son sustanciales:"
    )

    add_table_title("Tabla 3", "Diagnóstico preliminar de mermas y costos operativos en CUTonalá")
    cost_table = doc.add_table(rows=4, cols=3)
    cost_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_apa_table_borders(cost_table)

    headers = ["Rubro de Afectación", "Magnitud Cuantificada Estimada", "Impacto Académico / Patrimonial"]
    for c_idx, h_text in enumerate(headers):
        cell = cost_table.rows[0].cells[c_idx]
        set_cell_margins(cell, top=70, bottom=70, left=80, right=80)
        set_cell_shading(cell, "EAEFF5")
        p = cell.paragraphs[0]
        r = p.add_run(h_text)
        r.font.bold = True
        r.font.size = Pt(10.5)
        r.font.color.rgb = COLOR_NAVY

    cost_data = [
        ("Merma patrimonial silenciosa", "$130,000 - $150,000 MXN anuales", "Reposición constante de cables HDMI, adaptadores, apuntadores y reparación de proyectores."),
        ("Pérdida de tiempo de clase", "15 a 25 minutos por cada incidencia", "Retraso docente en el inicio de lecciones por fallas de equipo o reubicación de aula."),
        ("Ceguera administrativa", "100% de decisiones por suposición", "Compras presupuestales a ciegas sin datos de rotación ni historial de uso de activos.")
    ]

    for r_idx, row_vals in enumerate(cost_data, start=1):
        row = cost_table.rows[r_idx]
        for c_idx, val in enumerate(row_vals):
            cell = row.cells[c_idx]
            set_cell_margins(cell, top=60, bottom=60, left=80, right=80)
            p = cell.paragraphs[0]
            r = p.add_run(val)
            r.font.size = Pt(10)
            if c_idx == 1:
                r.font.bold = True

    add_table_note("Estimación formulada a partir de registros de incidencias en almacenes universitarios (2024-2026).")

    add_heading_2("2.5 Formulación de la pregunta de investigación")
    doc.add_paragraph(
        "Frente a la realidad descrita, se formula la siguiente Pregunta General de Investigación:"
    )

    add_callout(
        "PREGUNTA GENERAL DE INVESTIGACIÓN",
        "¿De qué manera el diseño e implementación de un sistema web centralizado con responsivas digitales, checklist de inspección "
        "y código QR dinámico (SIGRE) permite reducir las mermas patrimoniales por extravío no atribuible de equipo técnico y erradicar "
        "los empalmes en la asignación de espacios académicos en el Centro Universitario de Tonalá durante el ciclo escolar 2026B?"
    )

    doc.add_paragraph(
        "De la interrogante principal se derivan las siguientes preguntas específicas:"
    )
    doc.add_paragraph("• ¿Cuáles son los cuellos de botella y vulnerabilidades de registro en el circuito de préstamo en ventanilla de Servicios Generales?")
    doc.add_paragraph("• ¿Qué arquitectura modular de software asegura autenticación robusta, validación ágil y responsivas legales válidas?")
    doc.add_paragraph("• ¿Cuál es la viabilidad operativa y la efectividad cuantitativa alcanzada por la solución en un pilotaje real en CUTonalá?")

    doc.add_page_break()

    # =============================================================
    # 4. JUSTIFICACIÓN (Mínimo 1, Máximo 2 cuartillas - Alineado a ODS 2030)
    # =============================================================
    add_heading_1("3. Justificación de la Investigación")

    add_heading_2("3.1 Relevancia institucional, operativa y académica")
    doc.add_paragraph(
        "La realización de esta investigación se justifica plenamente en la necesidad de modernizar la infraestructura de soporte "
        "académico y salvaguardar los bienes patrimoniales públicos de CUTonalá. En la educación superior, la disponibilidad oportuna de "
        "los recursos tecnológicos no es un factor secundario: constituye el soporte indispensable para garantizar el cumplimiento de los "
        "planes de estudio, la impartición de cátedras interactivas y la ejecución de conferencias y coloquios de investigación."
    )
    doc.add_paragraph(
        "En el plano operativo, la plataforma SIGRE dignifica la labor del personal de intendencia, prefectura y almacenes. Actualmente, "
        "el personal enfrenta situaciones de alto estrés laboral en las ventanillas de Servicios Generales debido a la acumulación de "
        "profesores exigiendo material de forma simultánea. Al automatizar la solicitud mediante la emisión de un código QR personal en "
        "el teléfono móvil, el tiempo de despacho en mostrador se reduce drásticamente, eliminando fricciones, esperas prolongadas y "
        "ambigüedades respecto a la entrega y recepción de los activos."
    )
    doc.add_paragraph(
        "En el plano administrativo y de gobierno universitario, el proyecto dota a la Secretaría Administrativa y a la Contraloría "
        "de una herramienta de trazabilidad y auditoría probatoria. Al emitir responsivas oficiales en formato electrónico con fecha, "
        "hora exacta, matrícula institucional y número de serie del activo, se instaura un principio de certeza jurídica que desincentiva "
        "el extravío negligente y permite auditar en cualquier momento el estado y ubicación del inventario activo."
    )

    add_heading_2("3.2 Pertinencia en la Ingeniería en Ciencias Computacionales")
    doc.add_paragraph(
        "Desde la disciplina de la Ingeniería en Ciencias Computacionales, el proyecto aborda problemáticas de alto nivel ingenieril, "
        "tales como la arquitectura de software distribuido, la concurrencia de transacciones para reservaciones en tiempo real "
        "evitando colisiones (condiciones de carrera), la seguridad perimetral de la información bajo estándares criptográficos modernos, "
        "y la experiencia de usuario (UX/UI) adaptada a entornos de trabajo de ritmo acelerado. Constituye un modelo integral donde "
        "la ciencia de la computación resuelve una necesidad social e institucional concreta de su propia comunidad universitaria."
    )

    add_heading_2("3.3 Alineación con los Objetivos de Desarrollo Sostenible (ODS 2030)")
    doc.add_paragraph(
        "El proyecto SIGRE responde de forma explícita y directa a las metas establecidas en la Agenda 2030 para el Desarrollo Sostenible "
        "de la Organización de las Naciones Unidas (ONU, 2015), alineándose con tres objetivos estratégicos fundamentales:"
    )

    add_heading_3("3.3.1 ODS 4: Educación de Calidad (Meta 4.a)")
    doc.add_paragraph(
        "La Meta 4.a establece el compromiso de «construir y adecuar instalaciones educativas que ofrezcan entornos de aprendizaje "
        "seguros, no violentos, inclusivos y eficaces para todos». Cada minuto que un docente pierde por un aula empalmada o por un "
        "proyector descompuesto o no disponible se traduce en una merma pedagógica directa para los alumnos. SIGRE optimiza la eficacia "
        "de los entornos de aprendizaje al garantizar que los espacios educativos y el equipamiento didáctico estén listos y asignados "
        "con precisión matemática, erradicando los tiempos muertos lectivos."
    )

    add_heading_3("3.3.2 ODS 9: Industria, Innovación e Infraestructura (Metas 9.4 y 9.c)")
    doc.add_paragraph(
        "La Meta 9.4 llama a modernizar la infraestructura para que sea sostenible, aplicando tecnologías no contaminantes y procesos "
        "eficientes, mientras que la Meta 9.c promueve el acceso generalizado a las tecnologías de información. CUTonalá se ostenta como "
        "un campus sustentable de vanguardia. Mantener el registro de activos y auditorios en miles de hojas de papel vulnerables es una "
        "paradoja insostenible. SIGRE promueve la infraestructura digital de campus inteligente (Smart Campus), eliminando el consumo de "
        "papel y democratizando la gestión de recursos institucionales a través de herramientas cloud modernas."
    )

    add_heading_3("3.3.3 ODS 12: Producción y Consumo Responsables (Meta 12.5)")
    doc.add_paragraph(
        "La Meta 12.5 exige «reducir considerablemente la generación de desechos mediante actividades de prevención, reducción, reciclado "
        "y reutilización». Al implementar un módulo de doble checklist digital que inspecciona el estado de los equipos antes y después "
        "de cada préstamo, se previene el maltrato físico y se detectan fallas tempranas de mantenimiento preventivo. Esto prolonga la "
        "vida útil de los componentes electrónicos, disminuye la generación prematura de basura electrónica (e-waste) y optimiza el uso "
        "responsable del presupuesto universitario."
    )

    add_table_title("Tabla 4", "Matriz de alineación estratégica entre el proyecto SIGRE y la Agenda ODS 2030")
    ods_table = doc.add_table(rows=4, cols=3)
    ods_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_apa_table_borders(ods_table)

    ods_headers = ["Objetivo ODS 2030", "Meta Específica ONU", "Aporte Concreto de la Plataforma SIGRE"]
    for c_idx, h_text in enumerate(ods_headers):
        cell = ods_table.rows[0].cells[c_idx]
        set_cell_margins(cell, top=70, bottom=70, left=80, right=80)
        set_cell_shading(cell, "EAEFF5")
        p = cell.paragraphs[0]
        r = p.add_run(h_text)
        r.font.bold = True
        r.font.size = Pt(10.5)
        r.font.color.rgb = COLOR_NAVY

    ods_data = [
        ("ODS 4: Educación de Calidad", "Meta 4.a: Entornos de aprendizaje eficaces y seguros.", "Eliminación de empalmes en aulas y disponibilidad inmediata de herramientas didácticas, recuperando hasta 25 min de clase."),
        ("ODS 9: Innovación e Infraestructura", "Metas 9.4 y 9.c: Infraestructura tecnológica moderna y sostenible.", "Transición integral de procesos analógicos a una plataforma en la nube con código QR dinámico y cero uso de papel."),
        ("ODS 12: Producción y Consumo Responsable", "Meta 12.5: Reducción de desechos y protección patrimonial.", "Extensión de vida útil de activos tecnológicos mediante doble checklist e inspección preventiva, combatiendo la merma.")
    ]

    for r_idx, row_vals in enumerate(ods_data, start=1):
        row = ods_table.rows[r_idx]
        for c_idx, val in enumerate(row_vals):
            cell = row.cells[c_idx]
            set_cell_margins(cell, top=60, bottom=60, left=80, right=80)
            p = cell.paragraphs[0]
            r = p.add_run(val)
            r.font.size = Pt(10)
            if c_idx == 0:
                r.font.bold = True

    add_table_note("Elaboración propia con base en el marco oficial de metas e indicadores de la Agenda 2030 (ONU, 2015).")

    doc.add_page_break()

    # =============================================================
    # 5. OBJETIVOS DE LA INVESTIGACIÓN (Mínimo 1, Máximo 2 cuartillas)
    # =============================================================
    add_heading_1("4. Objetivos de la Investigación")

    add_heading_2("4.1 Criterio metodológico y epistemológico de formulación")
    doc.add_paragraph(
        "La estructuración de los objetivos en este protocolo se fundamenta en las directrices metodológicas de la investigación científica "
        "y el desarrollo tecnológico (Hernández-Sampieri & Mendoza, 2018; Bernal, 2016). Para asegurar su validez técnica y operativa, "
        "se adopta la Taxonomía de Bloom revisada, empleando verbos en infinitivo de alto orden analítico (Desarrollar, Diseñar, Diagnosticar, "
        "Evaluar), erradicando formulaciones difusas o subjetivas."
    )
    doc.add_paragraph(
        "Asimismo, se garantiza el cumplimiento riguroso de los criterios SMART en cada nivel de objetivo: Specific (específicos en la "
        "solución a construir), Measurable (asociados a indicadores cuantitativos de reducción de tiempos y mermas), Achievable (viables "
        "con los recursos de cómputo y el respaldo institucional de CUTonalá), Relevant (pertinentes para resolver el problema rector) "
        "y Time-bound (programados para su culminación y prueba durante el ciclo académico 2026B)."
    )

    add_heading_2("4.2 Objetivo General")
    doc.add_paragraph(
        "El propósito medular y de mayor alcance que guiará el proyecto de investigación se define en el siguiente enunciado:"
    )

    add_callout(
        "OBJETIVO GENERAL DE LA INVESTIGACIÓN",
        "«Desarrollar e implementar un sistema web centralizado (SIGRE) para la gestión integral y reserva transparente de recursos "
        "técnicos, equipamiento audiovisual y espacios físicos, con el fin de optimizar el aprovechamiento patrimonial, erradicar los "
        "empalmes de agenda y reducir los tiempos de despacho en mostrador en la comunidad universitaria del Centro Universitario de "
        "Tonalá durante el ciclo escolar 2026B.»"
    )

    add_heading_2("4.3 Objetivos Específicos Secuenciales")
    doc.add_paragraph(
        "Para garantizar la consecución del objetivo general, la investigación se desglosa en tres objetivos específicos estrictamente "
        "ordenados y articulados de forma secuencial y acumulativa, cubriendo las tres etapas canónicas de la ingeniería de software: "
        "fase de diagnóstico, fase de diseño/construcción y fase de validación empírica."
    )

    # Específico 1
    add_heading_3("4.3.1 Objetivo Específico 1: Diagnóstico situacional y flujos operativos")
    doc.add_paragraph(
        "«Diagnosticar el flujo operativo actual, los cuellos de botella y las vulnerabilidades de registro en el préstamo de equipo técnico "
        "y asignación de espacios físicos en los almacenes y áreas de Servicios Generales de CUTonalá, mediante el levantamiento de encuestas "
        "estructuradas, entrevistas a personal de mostrador y análisis documental de bitácoras físicas.»"
    )
    doc.add_paragraph(
        "• Justificación metodológica: Responde a la necesidad de fundar la ingeniería de software en requerimientos reales del contexto. "
        "Permite identificar los horarios de mayor afluencia de ventanilla, los activos con mayores incidencias de daño o extravío y "
        "los requerimientos de usabilidad para el personal administrativo."
    )
    doc.add_paragraph(
        "• Variables asociadas: Tiempo promedio de despacho en ventanilla (minutos), índice de discrepancias documentales en bitácoras físicas "
        "y volumen semanal de solicitudes de material."
    )
    doc.add_paragraph(
        "• Entregable y producto verificable: Documento formal de Especificación de Requerimientos de Software (SRS) y diagnóstico de cuellos de botella."
    )

    # Específico 2
    add_heading_3("4.3.2 Objetivo Específico 2: Diseño arquitectónico y desarrollo de módulos funcionales")
    doc.add_paragraph(
        "«Diseñar y construir una arquitectura modular de software basada en tecnologías web (frontend responsivo y backend escalable con base "
        "de datos relacional), que integre autenticación institucional segura, emisión de códigos QR dinámicos para control en puerta, "
        "generación automática de responsivas oficiales con firma digital y módulo de doble checklist de inspección funcional.»"
    )
    doc.add_paragraph(
        "• Justificación metodológica: Representa la ejecución técnica y el aporte computacional del proyecto. Garantiza la resolución "
        "de los problemas de concurrencia mediante transacciones atómicas (ACID) que imposibilitan el solapamiento de horarios en aulas y "
        "la expedición de responsivas con validez institucional respaldadas en base de datos."
    )
    doc.add_paragraph(
        "• Variables asociadas: Tiempo de respuesta del servidor (latencia en ms), cobertura de pruebas de software y tasa de éxito en "
        "validación de códigos QR en mostrador."
    )
    doc.add_paragraph(
        "• Entregable y producto verificable: Código fuente de la plataforma SIGRE versionado en repositorio Git, base de datos relacional "
        "desplegada y manual de arquitectura técnica del sistema."
    )

    # Específico 3
    add_heading_3("4.3.3 Objetivo Específico 3: Implementación piloto y evaluación cuantitativa de impacto")
    doc.add_paragraph(
        "«Evaluar la viabilidad técnica, la eficiencia operativa y el nivel de satisfacción de la plataforma SIGRE a través de una prueba "
        "piloto controlada en almacenes seleccionados de CUTonalá, contrastando los tiempos de despacho, la precisión del inventario activo "
        "y la experiencia de usuario frente al modelo tradicional de registro en libretas.»"
    )
    doc.add_paragraph(
        "• Justificación metodológica: Constituye la fase de contrastación y validación empírica. Permite medir el impacto cuantitativo de "
        "la solución en condiciones reales de trabajo y recabar retroalimentación de docentes y encargados de almacén para perfeccionar la "
        "herramienta antes de su eventual escalamiento a la Red UdeG."
    )
    doc.add_paragraph(
        "• Variables asociadas: Porcentaje de reducción en tiempos de espera en mostrador, índice de satisfacción del usuario (escala 1 a 5) "
        "y tasa de reducción de mermas patrimoniales registradas."
    )
    doc.add_paragraph(
        "• Entregable y producto verificable: Reporte analítico de resultados del pilotaje experimental y evaluación estadística de impacto "
        "con recomendaciones de despliegue."
    )

    add_heading_2("4.4 Matriz de Coherencia Metodológica de Objetivos")
    doc.add_paragraph(
        "La articulación lógica entre el objetivo general, los objetivos específicos, las preguntas rectoras y los entregables se sintetiza "
        "en la siguiente matriz metodológica:"
    )

    add_table_title("Tabla 5", "Matriz de coherencia metodológica de la investigación")
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
    # 6. REFERENCIAS BIBLIOGRÁFICAS (Normas APA 7ma Edición)
    # =============================================================
    add_heading_1("5. Referencias Bibliográficas")

    references = [
        "Asociación Nacional de Universidades e Instituciones de Educación Superior. (2023). Anuario estadístico de la educación superior 2022-2023. ANUIES. http://www.anuies.mx/informacion-y-servicios/informacion-estadistica-de-educacion-superior",
        "Bernal, C. A. (2016). Metodología de la investigación: administración, economía, humanidades y ciencias sociales (4.ª ed.). Pearson Educación.",
        "Cámara de Diputados del H. Congreso de la Unión. (2017). Ley general de protección de datos personales en posesión de sujetos obligados. Diario Oficial de la Federación. https://www.diputados.gob.mx/LeyesBiblio/pdf/LGPDPPSO.pdf",
        "Centro Universitario de Tonalá. (2023). Plan de desarrollo de CUTonalá 2019-2025: Visión 2030. Universidad de Guadalajara. http://www.cutonala.udg.mx/transparencia/pdi",
        "Coordinación General de Planeación y Evaluación. (2024). Numeralia institucional de la Red Universitaria. Universidad de Guadalajara. http://www.cgpe.udg.mx/numeralia",
        "Hernández-Sampieri, R., & Mendoza Torres, C. P. (2018). Metodología de la investigación: las rutas cuantitativa, cualitativa y mixta. McGraw-Hill Education.",
        "Miranda Miranda, J. J. (2012). Gestión de proyectos: Identificación, formulación, evaluación financiera, económica, social, ambiental (7.ª ed.). MMEditores.",
        "Organización de las Naciones Unidas. (2015). Transformar nuestro mundo: la Agenda 2030 para el Desarrollo Sostenible. ONU. https://sdgs.un.org/es/2030agenda",
        "Sapag Chain, N., Sapag Chain, R., & Sapag Puelma, J. M. (2014). Preparación y evaluación de proyectos (6.ª ed.). McGraw-Hill Interamericana.",
        "Universidad de Guadalajara. (2019). Reglamento de adquisiciones, arrendamientos y contratación de servicios de la Universidad de Guadalajara. Gaceta de la Universidad de Guadalajara. http://www.secgen.udg.mx/normatividad/reglamentos"
    ]

    for ref in references:
        p_ref = doc.add_paragraph()
        p_ref.paragraph_format.left_indent = Inches(0.5)
        p_ref.paragraph_format.first_line_indent = Inches(-0.5)
        p_ref.paragraph_format.space_after = Pt(8)
        p_ref.paragraph_format.line_spacing = 1.15
        r_ref = p_ref.add_run(ref)
        r_ref.font.size = Pt(10.5)

    # Guardar documento
    doc.save(output_path)
    print(f"Documento generado exitosamente en: {output_path}")

if __name__ == "__main__":
    out_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "docs", "2026B_Equipo4_Protocolo.docx"))
    create_protocolo_docx(out_file)
