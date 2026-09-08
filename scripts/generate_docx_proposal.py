import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def create_proposal_docx(output_path):
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
    # Tipografía y Jerarquía
    # Normal: 13 pt (interlineado 1.15)
    # Título Portada: 22 pt
    # Encabezado 1: 17 pt
    # Encabezado 2: 14.5 pt
    # Encabezado 3: 13 pt
    # Tablas: 11 pt ESTRICTO (Encabezados y cuerpo)
    # -------------------------------------------------------------
    COLOR_BLACK = RGBColor(0, 0, 0)
    COLOR_TEXT = RGBColor(33, 37, 41)
    COLOR_MUTED = RGBColor(108, 117, 125)
    
    style_normal = doc.styles['Normal']
    style_normal.font.name = 'Calibri'
    style_normal.font.size = Pt(13)
    style_normal.font.color.rgb = COLOR_TEXT
    style_normal.paragraph_format.line_spacing = 1.15
    style_normal.paragraph_format.space_after = Pt(7)
    style_normal.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    # Encabezado y Pie de página (páginas 2 en adelante)
    header = section.header
    p_hdr = header.paragraphs[0]
    p_hdr.text = "SIGRE | Propuesta de Proyecto de Inversión — Red Universitaria UdeG"
    p_hdr.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_hdr.runs[0].font.name = 'Calibri'
    p_hdr.runs[0].font.size = Pt(10)
    p_hdr.runs[0].font.color.rgb = COLOR_MUTED
    
    footer = section.footer
    p_ftr = footer.paragraphs[0]
    p_ftr.text = "Formulación y Evaluación de Proyectos de Inversión — Mtra. Abril Adriana Angulo Sherman"
    p_ftr.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_ftr.runs[0].font.name = 'Calibri'
    p_ftr.runs[0].font.size = Pt(10)
    p_ftr.runs[0].font.color.rgb = COLOR_MUTED

    # -------------------------------------------------------------
    # Funciones Auxiliares de Formato APA 7mo
    # -------------------------------------------------------------
    def set_cell_margins(cell, top=70, bottom=70, left=90, right=90):
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

    def set_apa_table_borders(table):
        tblPr = table._tbl.tblPr
        borders = parse_xml(
            f'<w:tblBorders {nsdecls("w")}>'
            f'<w:top w:val="single" w:sz="10" w:space="0" w:color="000000"/>'
            f'<w:bottom w:val="single" w:sz="10" w:space="0" w:color="000000"/>'
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
                f'<w:bottom w:val="single" w:sz="8" w:space="0" w:color="000000"/>'
                f'</w:tcBorders>'
            )
            tcPr.append(tcBorders)

    def add_table_title(table_num, title_text):
        p_num = doc.add_paragraph()
        p_num.paragraph_format.space_before = Pt(14)
        p_num.paragraph_format.space_after = Pt(2)
        p_num.paragraph_format.keep_with_next = True
        r_num = p_num.add_run(table_num)
        r_num.font.bold = True
        r_num.font.size = Pt(12)
        r_num.font.color.rgb = COLOR_BLACK
        
        p_tit = doc.add_paragraph()
        p_tit.paragraph_format.space_after = Pt(4)
        p_tit.paragraph_format.keep_with_next = True
        r_tit = p_tit.add_run(title_text)
        r_tit.font.italic = True
        r_tit.font.size = Pt(12)
        r_tit.font.color.rgb = COLOR_BLACK

    def add_table_note(note_text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(3)
        p.paragraph_format.space_after = Pt(10)
        r_lbl = p.add_run("Nota. ")
        r_lbl.font.italic = True
        r_lbl.font.size = Pt(10.5)
        r_lbl.font.color.rgb = COLOR_TEXT
        r_txt = p.add_run(note_text)
        r_txt.font.size = Pt(10.5)
        r_txt.font.color.rgb = COLOR_TEXT

    def add_heading_1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(22)
        p.paragraph_format.space_after = Pt(9)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Calibri'
        run.font.size = Pt(17)
        run.font.bold = True
        run.font.color.rgb = COLOR_BLACK
        return p

    def add_heading_2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(15)
        p.paragraph_format.space_after = Pt(7)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Calibri'
        run.font.size = Pt(14.5)
        run.font.bold = True
        run.font.color.rgb = COLOR_BLACK
        return p

    def add_heading_3(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(11)
        p.paragraph_format.space_after = Pt(5)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Calibri'
        run.font.size = Pt(13)
        run.font.bold = True
        run.font.italic = True
        run.font.color.rgb = COLOR_BLACK
        return p

    def add_note_block(title, content):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(9)
        p.paragraph_format.space_after = Pt(9)
        r_t = p.add_run(title + ": ")
        r_t.font.bold = True
        r_t.font.size = Pt(12.5)
        r_t.font.color.rgb = COLOR_BLACK
        r_c = p.add_run(content)
        r_c.font.italic = True
        r_c.font.size = Pt(12.5)
        r_c.font.color.rgb = COLOR_TEXT

    # -------------------------------------------------------------
    # PORTADA ACADÉMICA FORMAL (Calibri, sobria, sin fondos de color)
    # -------------------------------------------------------------
    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_before = Pt(30)
    
    p_tag = doc.add_paragraph()
    p_tag.paragraph_format.space_after = Pt(6)
    r_tag = p_tag.add_run("UNIVERSIDAD DE GUADALAJARA")
    r_tag.font.bold = True
    r_tag.font.size = Pt(14)
    r_tag.font.color.rgb = COLOR_BLACK
    
    p_tag2 = doc.add_paragraph()
    p_tag2.paragraph_format.space_after = Pt(20)
    r_tag2 = p_tag2.add_run("Centro Universitario de Tonalá | División de Ingenierías e Innovación Tecnológica")
    r_tag2.font.size = Pt(13)
    r_tag2.font.color.rgb = COLOR_MUTED
    
    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_after = Pt(10)
    p_title.paragraph_format.line_spacing = 1.15
    r_title = p_title.add_run("Propuesta de Proyecto de Inversión:\nPlataforma SIGRE para la Red Universitaria UdeG")
    r_title.font.size = Pt(22)
    r_title.font.bold = True
    r_title.font.color.rgb = COLOR_BLACK
    
    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_after = Pt(28)
    r_sub = p_sub.add_run(
        "Sistema Integrado de Gestión de Recursos, Espacios y Activos: Diagnóstico observacional de mermas patrimoniales, "
        "experiencia operativa en planteles, exploración de viabilidad institucional, Matriz de Marco Lógico, ficha de infraestructura TI, "
        "plan de contingencia operativa, dimensionamiento organizacional y evaluación financiera formal (FEN, VPN y TIR)."
    )
    r_sub.font.size = Pt(13.5)
    r_sub.font.color.rgb = COLOR_TEXT
    
    add_table_title("Tabla 1", "Ficha técnica y metadatos de la propuesta de inversión")
    meta_table = doc.add_table(rows=6, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_apa_table_borders(meta_table)
    
    meta_data = [
        ("Materia Académica:", "Formulación y Evaluación de Proyectos de Inversión"),
        ("Docente Titular:", "Mtra. Abril Adriana Angulo Sherman"),
        ("Autoría de la Propuesta:", "Equipo Promotor del Proyecto SIGRE"),
        ("Mercado Objetivo Exclusivo:", "Red Universitaria de la Universidad de Guadalajara (Centros Universitarios y SEMS)"),
        ("Inversión Inicial Solicitada:", "$180,000 MXN (Fase de Validación Piloto y Despliegue de Mercado)"),
        ("Fecha de Elaboración:", "Septiembre 2026")
    ]
    
    for idx, (label, val) in enumerate(meta_data):
        row = meta_table.rows[idx]
        c0, c1 = row.cells[0], row.cells[1]
        c0.width = Inches(2.7)
        c1.width = Inches(3.8)
        set_cell_margins(c0, top=60, bottom=60, left=80, right=80)
        set_cell_margins(c1, top=60, bottom=60, left=80, right=80)
        p0 = c0.paragraphs[0]
        r0 = p0.add_run(label)
        r0.font.bold = True
        r0.font.size = Pt(11)
        p1 = c1.paragraphs[0]
        r1 = p1.add_run(val)
        r1.font.size = Pt(11)
        
    add_table_note("Elaboración propia con base en los requerimientos académicos de la materia y el dictamen técnico de evaluación.")

    p_fn = doc.add_paragraph()
    p_fn.paragraph_format.space_before = Pt(20)
    r_fn = p_fn.add_run(
        "Nota técnica: Este documento integra de manera exhaustiva la atención al dictamen técnico emitido en la rúbrica de "
        "evaluación senior, incorporando el diagnóstico observacional y estimación de pérdidas en CUTonalá sustentado en experiencia "
        "operativa en Servicios Generales y reportes de almacén, exploración de viabilidad institucional, "
        "la Matriz de Marco Lógico (MML), especificaciones de TI y contingencia, organigrama y escalamiento, Diagrama de Gantt "
        "con ruta crítica y el cálculo riguroso de Flujo de Efectivo Neto (FEN), Valor Presente Neto (VPN) y Tasa Interna de Retorno (TIR)."
    )
    r_fn.font.size = Pt(11)
    r_fn.font.italic = True
    r_fn.font.color.rgb = COLOR_MUTED
    
    doc.add_page_break()

    # -------------------------------------------------------------
    # ÍNDICE GENERAL DEL DOCUMENTO
    # -------------------------------------------------------------
    add_heading_1("Índice General del Documento")
    
    index_items = [
        ("1. Identificación de la Idea de Proyecto a Desarrollar y Antecedentes", "3"),
        ("   1.1 Antecedentes y problemática en planteles universitarios", "3"),
        ("   1.2 El caso base de validación: CUTonalá", "4"),
        ("   1.3 Diagnóstico observacional, experiencia operativa y estimación de pérdidas", "4"),
        ("2. Resumen, Objetivos y Marco Lógico", "6"),
        ("   2.1 Resumen ejecutivo del proyecto", "6"),
        ("   2.2 Objetivos general y específicos", "6"),
        ("   2.3 Matriz de Marco Lógico (MML) del Proyecto SIGRE", "7"),
        ("3. Nicho Asociado del Proyecto (El Entorno UdeG)", "9"),
        ("4. Estudio de Mercado y Comercialización", "11"),
        ("   4.1 Definición y estructura del mercado en la UdeG", "11"),
        ("   4.2 Diagnóstico del problema y costo de la inacción", "11"),
        ("   4.3 Exploración de viabilidad y requerimientos con personal administrativo y directivo", "12"),
        ("   4.4 Análisis de alternativas existentes frente a SIGRE", "14"),
        ("   4.5 Viabilidad burocrática y mecanismos de compra directa", "15"),
        ("   4.6 Esquema tarifario en pesos MXN y comparativa de mercado", "16"),
        ("   4.7 Canales de atención y soporte técnico al cliente", "17"),
        ("   4.8 Servicios de capacitación, inducción y acompañamiento", "18"),
        ("   4.9 Estrategia de comercialización y mercadeo institucional", "19"),
        ("5. Características Técnicas de la Implementación", "20"),
        ("   5.1 Validación progresiva del Producto Mínimo Viable (MVP)", "20"),
        ("   5.2 Flujos operativos y módulos de valor", "20"),
        ("   5.3 Ficha técnica de infraestructura cloud, seguridad y desempeño", "21"),
        ("   5.4 Plan de contingencia tecnológica y continuidad operativa", "22"),
        ("6. Estructura Organizacional, Tamaño y Programación", "23"),
        ("   6.1 Capacidad operativa y dimensionamiento inicial", "23"),
        ("   6.2 Estructura organizacional y manual de perfiles inicial", "23"),
        ("   6.3 Plan de escalamiento del equipo de trabajo (Años 1 al 3)", "24"),
        ("   6.4 Justificación de bienes inmuebles, materias primas y legal", "25"),
        ("   6.5 Diagrama del Plan de Acción Operativo por Fases", "26"),
        ("   6.6 Diagrama de Gantt del Año 1 y Análisis de Ruta Crítica", "27"),
        ("7. Inversiones, Costos, Ingresos y Evaluación Financiera", "29"),
        ("   7.1 Inversión inicial requerida (CAPEX)", "29"),
        ("   7.2 Costos operativos fijos y variables (OPEX)", "30"),
        ("   7.3 Proyecciones trienales de ingresos (Pesos MXN)", "31"),
        ("   7.4 Estado de Resultados Proforma y Punto de Equilibrio", "32"),
        ("   7.5 Evaluación financiera integral: FEN, TMAR, VPN, TIR y Payback", "33"),
        ("   7.6 Condiciones de retorno y rendimientos para el inversionista", "35"),
        ("8. Conclusiones y Propuesta para el Inversionista", "36"),
        ("9. Referencias Bibliográficas (Norma APA 7ma Edición)", "37"),
        ("Anexo A. Matriz de Atención al Dictamen Técnico de Evaluación Senior", "38")
    ]
    
    add_table_title("Tabla 2", "Estructura de capítulos, secciones y paginación del documento")
    t_idx = doc.add_table(rows=len(index_items), cols=2)
    t_idx.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_apa_table_borders(t_idx)
    
    for i, (txt, pno) in enumerate(index_items):
        r_c = t_idx.rows[i]
        c0, c1 = r_c.cells[0], r_c.cells[1]
        c0.width = Inches(5.8)
        c1.width = Inches(0.7)
        set_cell_margins(c0, top=35, bottom=35, left=40, right=40)
        set_cell_margins(c1, top=35, bottom=35, left=40, right=40)
        p0 = c0.paragraphs[0]
        r0 = p0.add_run(txt)
        r0.font.size = Pt(11)
        if not txt.startswith("   "):
            r0.font.bold = True
        p1 = c1.paragraphs[0]
        p1.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        r1 = p1.add_run(pno)
        r1.font.size = Pt(11)
        r1.font.color.rgb = COLOR_MUTED
        
    add_table_note("Elaboración propia con base en el contenido desarrollado en la propuesta formal.")
    doc.add_page_break()

    # -------------------------------------------------------------
    # 1. IDENTIFICACIÓN Y ANTECEDENTES
    # -------------------------------------------------------------
    add_heading_1("1. Identificación de la Idea de Proyecto a Desarrollar y Antecedentes")
    
    doc.add_paragraph(
        "El proyecto denominado SIGRE (Sistema Integrado de Gestión de Recursos y Espacios) surge de una necesidad concreta y cotidiana "
        "en las dependencias de la Universidad de Guadalajara: la falta de una herramienta que conecte, en tiempo real y sin burocracia en papel, "
        "el préstamo de equipo técnico en almacenes, el apartado de aulas especiales y auditorios, y el control de asistencia con responsiva digital. "
        "A diferencia de un sistema administrativo general, SIGRE está pensado desde el mostrador del almacén hacia afuera, resolviendo tanto la "
        "fila del estudiante que necesita un cable para exponer como la auditoría patrimonial que debe entregar el Secretario Administrativo al final del ejercicio."
    )
    
    add_heading_2("1.1 Antecedentes y problemática en planteles universitarios")
    doc.add_paragraph(
        "Cualquiera que haya solicitado un proyector o un aula en un centro universitario conoce el circuito habitual: caminar hasta el almacén, "
        "esperar a que el encargado busque la libreta de registros, anotar a mano nombre, código y firma, y dejar una credencial como garantía informal. "
        "Este procedimiento, que se repite cientos de veces al día en cada campus, arrastra tres problemas serios que las autoridades reconocen pero no han podido frenar:"
    )
    doc.add_paragraph(
        "El primero es la merma patrimonial silenciosa. Cuando un adaptador HDMI, un apuntador láser o un micrófono se extravían, la libreta rara vez "
        "permite identificar con certeza quién fue el último usuario responsable. El registro en papel se ensucia, se traspapela o carece de la firma clara "
        "de entrega y recepción. Con el paso de los semestres, estas pérdidas acumuladas representan decenas de miles de pesos que los planteles deben reponer de su gasto corriente."
    )
    doc.add_paragraph(
        "El segundo problema es la pérdida de tiempo efectivo de clase. Cuando un profesor llega al aula y el equipo no funciona o el aula fue asignada a dos "
        "actividades al mismo tiempo por empalmes en agendas de papel, se pierden entre 15 y 25 minutos resolviendo el conflicto. En un semestre con miles de sesiones, "
        "el impacto acumulado sobre la calidad educativa es considerable."
    )
    doc.add_paragraph(
        "El tercero es la ceguera directiva. Los secretarios administrativos y directores de escuela no tienen forma de saber con certeza cuáles equipos se usan a diario, "
        "cuáles están descompuestos en un rincón del almacén o qué espacios tienen subutilización crónica. Las compras de equipamiento terminan haciéndose por intuición "
        "o presión del momento, y no con datos duros de aprovechamiento."
    )
    
    add_heading_2("1.2 El caso base de validación: CUTonalá")
    doc.add_paragraph(
        "El Centro Universitario de Tonalá (CUTonalá) representa un entorno ideal para validar esta solución. Con una matrícula superior a los 9,000 estudiantes "
        "y una infraestructura en constante expansión de ingenierías, ciencias de la salud y ciencias sociales, sus almacenes manejan a diario desde instrumental "
        "especializado de laboratorio hasta cientos de proyectores y laptops para docencia. Al ser el campus de origen del equipo promotor, se cuenta con acceso directo "
        "a los almacenes, al personal operativo de ventanilla y a las autoridades administrativas para probar la plataforma en condiciones reales sin costo de intermediación."
    )

    add_heading_2("1.3 Diagnóstico observacional, experiencia operativa y estimación de pérdidas")
    doc.add_paragraph(
        "El origen de este proyecto no proviene de un planteamiento meramente teórico, sino de la experiencia operativa directa del "
        "equipo promotor y de la convivencia cotidiana con los procesos administrativos de la Red Universitaria. Al haberse desempeñado "
        "laboralmente en el área de Servicios Generales, se experimentó de primera mano la problemática recurrente en la gestión de espacios "
        "físicos compartidos (auditorios, salas de usos múltiples, aulas magnas y laboratorios). La dinámica tradicional de tramitar el préstamo "
        "de un área mediante oficios impresos, firmas autógrafas o acuerdos verbales desemboca con frecuencia en empalmes de agenda: situaciones "
        "donde un docente, ponente o grupo estudiantil llega a un espacio formalmente apartado y se encuentra con que ya está ocupado por otra "
        "actividad, o bien que permanece cerrado y sin llave disponible debido a la falta de visibilidad en tiempo real entre almacenes, "
        "coordinaciones y personal de intendencia."
    )
    doc.add_paragraph(
        "Esta experiencia personal en ventanilla y campo coincide plenamente con los testimonios y observaciones compartidas por compañeros, "
        "amigos y colaboradores operativos que laboran en diversas áreas y almacenes de los planteles universitarios. De forma reiterada, el "
        "personal operativo señala un patrón constante de mermas silenciosas que no quedan registradas en ningún sistema. Un caso emblemático "
        "y sumamente común es la pérdida periódica de accesorios de alta rotación: en los almacenes se comenta con frecuencia que es habitual "
        "que se extravíe o dañe al menos un cable HDMI por mes por dependencia o módulo, además de adaptadores USB-C/VGA, extensiones eléctricas "
        "y apuntadores digitales que se prestan en mostrador y que, ante la prisa del cambio de clase o el descuido de la libreta, no vuelven a ser devueltos."
    )
    doc.add_paragraph(
        "Con apego al rigor y a la honestidad metodológica, es indispensable puntualizar que hasta este momento no se han aplicado encuestas "
        "estructuradas masivas ni censos estadísticos formales en los planteles. En consecuencia, el dimensionamiento de las afectaciones parte de "
        "una estimación cualitativa y empírica fundada en la observación directa en campo, en la recurrencia de estos testimonios y en los costos "
        "de reposición que asumen las dependencias:"
    )

    add_note_block(
        "Aclaración Metodológica y Estimación Preliminar",
        "«Aunque no se cuenta aún con una auditoría formal de campo, se estima —con base en los rangos de reposición reportados en la Sección 4.2 "
        "y la experiencia directa del equipo promotor como usuario del sistema actual— que las pérdidas anuales por plantel oscilan entre $130,000 "
        "y $150,000 MXN. Se recomienda que la siguiente fase del proyecto incluya una auditoría formal para validar esta cifra.»"
    )

    doc.add_paragraph(
        "A partir de la experiencia recopilada en Servicios Generales y de los costos directos de reposición en planteles, se articula el "
        "siguiente cuadro estimado del impacto de la inacción administrativa:"
    )

    add_table_title("Tabla 3", "Estimación preliminar de pérdidas patrimoniales y costos operativos por plantel")
    diag_t = doc.add_table(rows=6, cols=4)
    diag_t.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_apa_table_borders(diag_t)
    
    headers_dg = ["Concepto Evaluado / Ineficiencia", "Frecuencia Observada / Testimonial", "Base de Estimación Anual", "Rango de Impacto Económico / Operativo"]
    for j, h in enumerate(headers_dg):
        c = diag_t.rows[0].cells[j]
        set_cell_margins(c, top=70, bottom=70, left=70, right=70)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.font.bold = True
        r.font.size = Pt(11)
        
    dg_data = [
        ("Mermas y extravíos de accesorios menores (cables HDMI, adaptadores, extensiones)", "Pérdida testimonial de al menos 1 cable HDMI al mes más adaptadores por almacén", "15 a 30 accesorios no devueltos o inutilizados al año", "$20,000 a $30,000 MXN anuales en reposición directa"),
        ("Daños no deslindados en equipos mayores (proyectores, bocinas, cómputo portátil)", "2 a 4 incidencias anuales con daño físico sin responsiva digital clara ni responsable", "Reparación o sustitución urgente absorbida por gasto corriente", "$60,000 a $90,000 MXN anuales por reposición o pólizas"),
        ("Horas-clase perdidas por empalmes de áreas o demoras en ventanilla de mostrador", "Empalmes en salas y esperas de 10 a 20 minutos en horas pico de entrega de llaves/equipo", "40 a 80 horas-aula anuales de docencia interrumpida o diferida", "Afectación sustancial a la planeación académica y clima laboral"),
        ("Gasto administrativo en papelería desechable, vales y oficios de solicitud", "Expedición física de miles de formatos impresos, copias de identificación y libretas", "Consumo continuo de tóner y resmas para archivo muerto", "$10,000 a $20,000 MXN al año por dependencia"),
        ("TOTAL ESTIMADO (RANGO DE COSTO DE INACCIÓN)", "Experiencia en Servicios Generales, reportes de almacén y rangos de reposición", "Costo directo consolidado estimado por plantel", "$130,000 a $150,000 MXN anuales por plantel")
    ]
    
    for idx, row_vals in enumerate(dg_data):
        row = diag_t.rows[idx + 1]
        for j, val in enumerate(row_vals):
            cell = row.cells[j]
            set_cell_margins(cell, top=60, bottom=60, left=70, right=70)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT if j < 2 else (WD_ALIGN_PARAGRAPH.CENTER if j == 2 else WD_ALIGN_PARAGRAPH.RIGHT)
            r = p.add_run(val)
            r.font.size = Pt(11)
            if idx == 4 or j == 0:
                r.font.bold = True
                
    add_table_note("Estimación preliminar formulada a partir de la experiencia del equipo promotor en Servicios Generales, testimonios de personal de almacén y los rangos de reposición de la Sección 4.2. Pendiente de validación mediante auditoría formal de campo en la fase piloto.")

    doc.add_paragraph(
        "Como se observa en la Tabla 3, las pérdidas estimadas de $130,000 a $150,000 MXN anuales por plantel demuestran que el costo de no "
        "hacer nada supera con creces el costo de implementar SIGRE. Frente a este desembolso acumulado en reponer accesorios y reparar equipos, "
        "una suscripción anual de $24,000 a $48,000 MXN resulta financieramente viable y de amortización inmediata. La fase de prueba piloto en "
        "el Centro Universitario de Tonalá permitirá precisamente instrumentar la auditoría formal de campo recomendada para validar con datos "
        "censo-estadísticos esta estimación inicial."
    )
    
    doc.add_page_break()

    # -------------------------------------------------------------
    # 2. RESUMEN, OBJETIVOS Y MARCO LÓGICO
    # -------------------------------------------------------------
    add_heading_1("2. Resumen, Objetivos y Marco Lógico")
    
    add_heading_2("2.1 Resumen ejecutivo del proyecto")
    doc.add_paragraph(
        "SIGRE es una solución de software bajo modelo SaaS (Software as a Service) concebida para modernizar la gestión logística interna en las escuelas "
        "preparatorias y centros universitarios de la Universidad de Guadalajara. La plataforma sustituye por completo los formatos físicos de préstamo por "
        "un entorno digital que combina cuatro elementos prácticos: un sistema de reservas con validación de horario para evitar empalmes, un flujo de responsivas "
        "con firma digital y código QR intransferible, un doble checklist fotográfico al entregar y recibir material, y un tablero directivo con estadísticas "
        "de uso patrimonial. Con una inversión inicial de $180,000 MXN destinada a afinar el producto en CUTonalá, tramitar registros de propiedad intelectual y "
        "desplegar la labor comercial, el proyecto alcanza su punto de equilibrio en el mes 14 y genera una Tasa Interna de Retorno del 22.84% a tres años."
    )
    
    add_heading_2("2.2 Objetivos general y específicos")
    doc.add_paragraph(
        "El objetivo general del proyecto es implementar y comercializar una plataforma digital especializada en el control de préstamos de recursos técnicos, "
        "reserva de espacios y emisión de responsivas oficiales en los planteles de la Universidad de Guadalajara, logrando la adopción contractual de al menos "
        "22 planteles (8 centros universitarios y 14 preparatorias) al término del tercer año de operaciones, asegurando la sostenibilidad financiera de la empresa "
        "y reduciendo en más del 70% las mermas patrimoniales en los almacenes contratantes."
    )
    doc.add_paragraph("Para materializar este objetivo, se establecen cuatro metas específicas interconectadas:")
    doc.add_paragraph(
        "En primer lugar, validar y estabilizar la plataforma en CUTonalá durante los primeros seis meses, procesando al menos 3,000 solicitudes reales "
        "y logrando un índice de satisfacción superior al 90% entre almacenistas y profesores para consolidar el caso de éxito base."
    )
    doc.add_paragraph(
        "En segundo término, blindar legal e institucionalmente la solución mediante el registro marcario ante el IMPI, el depósito de derechos de autor "
        "del software ante INDAUTOR y la homologación técnica con los lineamientos de la Ley General de Protección de Datos Personales en Posesión de Sujetos Obligados."
    )
    doc.add_paragraph(
        "En tercer lugar, captar en el segundo año de operación a 8 planteles universitarios (3 Centros Universitarios metropolitanos/regionales y 5 Preparatorias "
        "del SEMS) mediante esquemas de adjudicación directa formalizados con secretarios administrativos y directores, alcanzando el punto de equilibrio operativo en el mes 14."
    )
    doc.add_paragraph(
        "Por último, consolidar en el tercer año una cartera de 22 planteles activos, estructurando un equipo de soporte escalonado y garantizando un Flujo de "
        "Efectivo Neto acumulado que permita recuperar la inversión inicial en el mes 28 y remunerar a los inversionistas con un rendimiento atractivo y recurrente."
    )

    add_heading_2("2.3 Matriz de Marco Lógico (MML) del Proyecto SIGRE")
    doc.add_paragraph(
        "Para asegurar la coherencia interna del proyecto y vincular las actividades operativas con los objetivos estratégicos y los riesgos institucionales, "
        "se diseñó la Matriz de Marco Lógico bajo el estándar metodológico oficial de formulación de proyectos. La matriz estructura los cuatro niveles causales: "
        "el Fin último al que contribuye el proyecto, el Propósito central de la iniciativa, los Componentes o bienes entregables, y las Actividades críticas de ejecución."
    )

    add_table_title("Tabla 4", "Matriz de Marco Lógico (MML) para el despliegue del proyecto SIGRE")
    mml_t = doc.add_table(rows=5, cols=4)
    mml_t.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_apa_table_borders(mml_t)
    
    headers_ml = ["Nivel Jerárquico", "Resumen Narrativo de Objetivos", "Indicadores Objetivamente Verificables", "Medios de Verificación y Supuestos"]
    for j, h in enumerate(headers_ml):
        c = mml_t.rows[0].cells[j]
        set_cell_margins(c, top=70, bottom=70, left=70, right=70)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.font.bold = True
        r.font.size = Pt(11)
        
    mml_rows = [
        ("FIN\n(Impacto Superior)", 
         "Contribuir a la eficiencia administrativa, transparencia y preservación del patrimonio público en la Red Universitaria de la Universidad de Guadalajara.",
         "Reducción acumulada del 75% en el costo por mermas y reposición de equipo técnico en planteles afiliados al término de 3 años.",
         "MV: Informes anuales de auditoría y cuentas públicas de los planteles de la UdeG.\nSupuesto: Estabilidad en la asignación presupuestal para tecnologías educativas."),
        
        ("PROPÓSITO\n(Efecto Directo)", 
         "Planteles de la UdeG cuentan con un sistema digital ágil, auditable y de bajo costo para el control de inventario móvil, reserva de espacios y firmas de responsivas.",
         "22 planteles con contrato activo al Año 3; más de 65,000 préstamos anuales registrados; cero empalmes de aula en eventos programados.",
         "MV: Contratos de suscripción vigentes, bitácoras digitales del sistema y reportes de satisfacción de almacén.\nSupuesto: Decisores mantienen facultad de compra directa sin centralización restrictiva."),
        
        ("COMPONENTES\n(Entregables)", 
         "C1. Software SIGRE desplegado en nube con módulos de almacén, checklist y QR.\nC2. Marco de propiedad intelectual registrado (IMPI e INDAUTOR).\nC3. Modelo de comercialización y atención validado con Secretarios y Directores.\nC4. Programa de capacitación y mesa de soporte técnico operativo.",
         "C1: 99.9% de disponibilidad del servicio en nube.\nC2: 2 títulos de registro obtenidos en Año 1.\nC3: Tasa de conversión de demostraciones a contratos >= 60%.\nC4: 100% de almacenistas capacitados en planteles suscritos.",
         "MV: Métricas de uptime de la nube, títulos oficiales de registro, minutas de entrega-recepción y actas de acreditación de talleres.\nSupuesto: Personal sindicalizado de almacén muestra apertura al uso de herramientas digitales asistidas."),
        
        ("ACTIVIDADES\n(Acciones Clave)", 
         "A1. Refinamiento del software y módulo de contingencia offline.\nA2. Pruebas piloto y ajustes de flujo en almacenes de CUTonalá.\nA3. Solicitud de registro marcario IMPI y depósito de software INDAUTOR.\nA4. Ronda de presentaciones ejecutivas a Secretarios Administrativos y Directores.\nA5. Instalación de módulo de atención y canal directo de WhatsApp institucional.\nA6. Impartición de talleres prácticos de 16 horas y entrega de material plastificado.\nA7. Monitoreo mensual de métricas de uso y cobranza de renovaciones.",
         "A1-A2: 6 meses de pilotaje completados con 3,000 folios generados.\nA3: Trámites ingresados en mes 2 y dictaminados en mes 8.\nA4: 25 reuniones ejecutivas sostenidas en Año 1 y 2.\nA5-A6: Mesa de ayuda operando con SLA < 2 horas en horario hábil.\nA7: Cobranza anual puntual superior al 95% de la cartera.",
         "MV: Repositorio de código con control de versiones, comprobantes de pago de derechos de trámite, minutas de reunión con secretarios y reportes de tickets de soporte.\nSupuesto: El capital semilla de $180,000 MXN se desembolsa oportunamente al inicio del proyecto.")
    ]
    
    for idx, row_vals in enumerate(mml_rows):
        row = mml_t.rows[idx + 1]
        for j, val in enumerate(row_vals):
            cell = row.cells[j]
            set_cell_margins(cell, top=60, bottom=60, left=70, right=70)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(val)
            r.font.size = Pt(11)
            if j == 0:
                r.font.bold = True
                
    add_table_note("Elaboración propia siguiendo la metodología del Marco Lógico (CEPAL/BID) adaptada al contexto institucional de la UdeG.")
    doc.add_page_break()

    # -------------------------------------------------------------
    # 3. NICHO ASOCIADO DEL PROYECTO
    # -------------------------------------------------------------
    add_heading_1("3. Nicho Asociado del Proyecto (El Entorno UdeG)")
    
    doc.add_paragraph(
        "El nicho de mercado en el que compite SIGRE no es el mercado abierto de empresas privadas ni las escuelas particulares dispersas, sino una estructura "
        "institucional específica: la Red Universitaria de la Universidad de Guadalajara. Esta delimitación no es casual ni restrictiva; por el contrario, "
        "ofrece una ventaja estratégica fundamental: todas las escuelas preparatorias y centros universitarios de la red comparten el mismo marco normativo, "
        "el mismo sistema de compras, calendarios escolares idénticos y una problemática operativa prácticamente calcada en sus almacenes."
    )
    doc.add_paragraph(
        "De acuerdo con los datos de la Coordinación General de Planeación y Evaluación (CGPE, 2024), la Red Universitaria está integrada por 18 Centros Universitarios "
        "(6 temáticos metropolitanos y 12 regionales distribuidos en Jalisco) y el Sistema de Educación Media Superior (SEMS), que agrupa 175 dependencias "
        "(73 escuelas preparatorias sede y 102 módulos en municipios del interior). En total, existen casi 200 planteles educativos que operan con relativa autonomía "
        "presupuestal y administrativa en sus gastos de operación cotidiana."
    )

    add_table_title("Tabla 5", "Dimensionamiento del mercado potencial cautivo en la Red Universitaria UdeG")
    net_t = doc.add_table(rows=6, cols=4)
    net_t.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_apa_table_borders(net_t)
    
    headers_nt = ["Segmento Institucional", "Total Dependencias", "Mercado Meta Año 3", "Tarifa Anual Sugerida"]
    for j, h in enumerate(headers_nt):
        c = net_t.rows[0].cells[j]
        set_cell_margins(c, top=70, bottom=70, left=70, right=70)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.font.bold = True
        r.font.size = Pt(11)
        
    net_d = [
        ("Centros Universitarios Temáticos (Metropolitanos: CUCEI, CUCEA, CUAAD, etc.)", "6 dependencias", "3 dependencias (50%)", "$48,000 MXN / año"),
        ("Centros Universitarios Regionales (CUNorte, CUSur, CUTonalá, CUAltos, etc.)", "12 dependencias", "5 dependencias (42%)", "$48,000 MXN / año"),
        ("Preparatorias Metropolitanas SEMS (Guadalajara, Zapopan, Tlaquepaque)", "30 dependencias", "8 dependencias (27%)", "$24,000 MXN / año"),
        ("Preparatorias Regionales y Módulos SEMS (Interior del Estado)", "145 dependencias", "6 dependencias (4%)", "$24,000 MXN / año"),
        ("UNIVERSO TOTAL POTENCIAL Y META", "193 dependencias", "22 dependencias (11.4% de la Red)", "Ingresos anuales recurrentes: $720,000 MXN")
    ]
    
    for idx, row_vals in enumerate(net_d):
        row = net_t.rows[idx + 1]
        for j, val in enumerate(row_vals):
            cell = row.cells[j]
            set_cell_margins(cell, top=60, bottom=60, left=70, right=70)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT if j == 0 else (WD_ALIGN_PARAGRAPH.CENTER if j in (1, 2) else WD_ALIGN_PARAGRAPH.RIGHT)
            r = p.add_run(val)
            r.font.size = Pt(11)
            if idx == 4 or j == 0:
                r.font.bold = True
                
    add_table_note("Elaboración propia con base en el directorio de planteles de la CGPE (2024) y el SEMS (2024).")

    doc.add_paragraph(
        "La meta de captar 22 planteles para el cierre del tercer año representa apenas el 11.4% de todo el mercado universitario disponible en Jalisco. "
        "Esto evidencia que las proyecciones financieras no se basan en supuestos de penetración agresivos ni irreales; al contrario, con captar a una décima "
        "parte de los planteles de la universidad, el negocio alcanza plena rentabilidad y genera un excedente de caja suficiente para sostener la operación y dividendos."
    )
    doc.add_page_break()

    # -------------------------------------------------------------
    # 4. ESTUDIO DE MERCADO Y COMERCIALIZACIÓN
    # -------------------------------------------------------------
    add_heading_1("4. Estudio de Mercado y Comercialización")
    
    add_heading_2("4.1 Definición y estructura del mercado en la UdeG")
    doc.add_paragraph(
        "En una institución pública como la Universidad de Guadalajara, el usuario final del sistema no es quien toma la decisión de compra. "
        "En los planteles universitarios existen dos figuras de decisión claramente delimitadas: en los Centros Universitarios, el poder de decisión recae "
        "en el Secretario Administrativo, quien coordina al personal de almacén, supervisa los inventarios de bienes muebles y autoriza las contrataciones "
        "de servicios de apoyo; en las Escuelas Preparatorias del SEMS, la autoridad recae de forma directa en el Director del Plantel con el auxilio "
        "de su Administrador de Recursos. Por lo tanto, la estrategia comercial debe dirigirse con argumentos distintos a cada perfil: al Secretario "
        "Administrativo se le ofrece orden patrimonial y blindaje ante auditorías, mientras que al Director de Preparatoria se le ofrece tranquilidad operativa "
        "y un costo anual muy por debajo de su fondo revolvente disponible."
    )
    
    add_heading_2("4.2 Diagnóstico del problema y costo de la inacción")
    doc.add_paragraph(
        "Durante años, la respuesta de los planteles ante la pérdida de proyectores o cables ha sido comprar más equipo o resignarse a la merma como un costo "
        "inevitable de la operación. Sin embargo, cuando se suman los gastos de reposición en una administración de tres años, las cifras superan fácilmente "
        "el medio millón de pesos por plantel. El costo de no hacer nada se traduce en un drenaje continuo de recursos que podrían canalizarse a investigación, "
        "becas o infraestructura estudiantil. SIGRE sustituye esa resignación por un sistema trazable que responsabiliza con amabilidad pero con firmeza al usuario."
    )

    add_heading_2("4.3 Exploración de viabilidad y requerimientos con personal administrativo y directivo")
    doc.add_paragraph(
        "Con la finalidad de evaluar la viabilidad de adopción y los requerimientos reales de los planteles universitarios, el "
        "equipo promotor sostuvo acercamientos y diálogos exploratorios con personal administrativo, encargados de servicios "
        "generales y autoridades de centros universitarios y escuelas preparatorias del SEMS."
    )
    doc.add_paragraph(
        "Estos intercambios cualitativos se centraron en clarificar cuatro aspectos indispensables para la instrumentación comercial: "
        "la prioridad asignada a las mermas de almacén, la razonabilidad del rango tarifario propuesto ($24,000 a $48,000 MXN anuales), "
        "la viabilidad de contratación mediante adjudicación directa conforme a la normativa universitaria, y las condiciones de soporte "
        "necesarias para evitar resistencia al cambio en el personal de mostrador:"
    )

    add_table_title("Tabla 6", "Criterios cualitativos de viabilidad institucional y adopción en la Red UdeG")
    val_t = doc.add_table(rows=6, cols=4)
    val_t.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_apa_table_borders(val_t)
    
    headers_vl = ["Eje de Viabilidad Evaluado", "Perspectiva en Centros Universitarios", "Perspectiva en Escuelas Preparatorias (SEMS)", "Criterio Técnico / Normativo Resultante"]
    for j, h in enumerate(headers_vl):
        c = val_t.rows[0].cells[j]
        set_cell_margins(c, top=70, bottom=70, left=70, right=70)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.font.bold = True
        r.font.size = Pt(11)
        
    vl_d = [
        ("Prioridad del control en almacén y áreas prestadas", "Alta prioridad en auditorios, aulas magnas y equipo técnico especializado", "Alta prioridad en proyectores y accesorios de alta movilidad en aulas", "Existe consenso operativo sobre la urgencia de erradicar libretas y vales manuscritos."),
        ("Razonabilidad del esquema de suscripción anual fija", "Tarifa de $48,000 MXN anuales plenamente absorbible por gasto de operación", "Cuota de $24,000 MXN anuales altamente accesible frente a fondos ordinarios", "El costo anual del sistema es marginal comparado con las mermas acumuladas por plantel."),
        ("Mecanismo normativo de contratación directa", "Facultad directa de autorización del Secretario Administrativo", "Facultad de contratación directa del Director de Preparatoria", "El monto fijado se sitúa por debajo del umbral de compras menores, agilizando el proceso."),
        ("Condiciones críticas para adopción en mostrador", "Soporte oportuno y compatibilidad total con cuentas institucionales @udg.mx", "Capacitación práctica presencial para personal operativo y sindicalizado", "La usabilidad ágil en ventanilla y el acompañamiento presencial son determinantes."),
        ("SÍNTESIS DE VIABILIDAD INSTITUCIONAL", "Favorable, con interés en resultados del piloto en CUTonalá", "Favorable, solicitando demostraciones presenciales en sitio", "Viabilidad institucional sólida; formalización de convenios programada durante la Fase 3.")
    ]
    
    for idx, row_vals in enumerate(vl_d):
        row = val_t.rows[idx + 1]
        for j, val in enumerate(row_vals):
            cell = row.cells[j]
            set_cell_margins(cell, top=60, bottom=60, left=70, right=70)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(val)
            r.font.size = Pt(11)
            if idx == 4 or j == 0:
                r.font.bold = True
                
    add_table_note("Criterios cualitativos consolidados a partir de consultas exploratorias con personal administrativo y operativo de la Red UdeG. La recolección de cartas de intención y convenios se efectuará formalmente en la fase demostrativa.")

    add_heading_2("4.4 Análisis de alternativas existentes frente a SIGRE")
    doc.add_paragraph(
        "Actualmente, los planteles intentan resolver estos problemas mediante tres vías imperfectas. La primera es el SIIAU institucional; sin embargo, "
        "el SIIAU es un sistema académico y presupuestal centralizado, rígido y sin interfaces diseñadas para operar con rapidez en la ventanilla de un almacén. "
        "La segunda alternativa son las libretas de papel y formatos de Excel compartidos en Google Drive, que no ofrecen firma digital vinculante ni "
        "previenen el empalme simultáneo de reservas. La tercera opción son los softwares comerciales extranjeros para gestión de activos (como Cheqroom o Asset Panda), "
        "los cuales cobran licencias en dólares que superan los $4,000 USD anuales, no se adaptan al flujo normativo de la UdeG y no emiten actas de responsiva formal en español."
    )

    add_table_title("Tabla 7", "Comparativa técnica y funcional de alternativas frente a la solución SIGRE")
    comp_t = doc.add_table(rows=6, cols=5)
    comp_t.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_apa_table_borders(comp_t)
    
    headers_cp = ["Criterio de Evaluación", "Libretas y Excel", "SIIAU Institucional", "SaaS Extranjero (USD)", "SIGRE (Propuesta)"]
    for j, h in enumerate(headers_cp):
        c = comp_t.rows[0].cells[j]
        set_cell_margins(c, top=70, bottom=70, left=60, right=60)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.font.bold = True
        r.font.size = Pt(11)
        
    cp_data = [
        ("Velocidad de despacho en mostrador", "Lenta (3 a 5 min/alumno)", "No aplica a mostrador", "Media (1.5 min/alumno)", "Ágil (< 30 seg con QR)"),
        ("Trazabilidad y firma de responsiva", "Nula (firma manuscrita ilegible)", "No genera responsivas de equipo", "Media (requiere correos externos)", "Alta (Firma digital y token)"),
        ("Prevención de empalme en espacios", "Inexistente (conflictos diarios)", "Solo planeación cuatrimestral", "Sí (a costo elevado)", "Total (bloqueo atómico)"),
        ("Moneda y costo anual por plantel", "Gasto oculto en mermas ($130k+)", "Incluido en nómina central", "Alto ($60,000 a $90,000 MXN)", "Económico ($24k a $48k MXN)"),
        ("Acompañamiento a almacenistas", "Ninguno", "Mesa central de TI saturada", "Soporte en inglés por correo", "Presencial y WhatsApp directo")
    ]
    
    for idx, row_vals in enumerate(cp_data):
        row = comp_t.rows[idx + 1]
        for j, val in enumerate(row_vals):
            cell = row.cells[j]
            set_cell_margins(cell, top=60, bottom=60, left=60, right=60)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT if j == 0 else WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run(val)
            r.font.size = Pt(11)
            if j == 4:
                r.font.bold = True
                
    add_table_note("Elaboración propia con base en el benchmark de mercado de software de control de inventario educativo.")

    add_heading_2("4.5 Viabilidad burocrática y mecanismos de compra directa")
    doc.add_paragraph(
        "Un aspecto crítico que suele frenar a los proyectos tecnológicos dirigidos al sector público es la tramitología de licitaciones públicas. "
        "En la Universidad de Guadalajara, el Reglamento de Adquisiciones, Arrendamientos y Contratación de Servicios (Universidad de Guadalajara, 2019) "
        "establece con claridad los montos máximos autorizados para compras menores y adjudicaciones directas sin pasar por el Comité Central de Compras. "
        "Las tarifas anuales de SIGRE ($24,000 MXN para escuelas preparatorias y $48,000 MXN para centros universitarios) se diseñaron deliberadamente "
        "para quedar por debajo de estos topes normativos. Esto significa que un Secretario Administrativo o Director puede autorizar la contratación del "
        "servicio en cuestión de días con cargo a su fondo de operación ordinario, sin necesidad de trámites engorrosos ni procesos de licitación estatal."
    )

    add_heading_2("4.6 Canales de atención y soporte técnico al cliente")
    doc.add_paragraph(
        "La atención a los planteles contratantes no puede depender de un solo canal, porque las necesidades de un Secretario Administrativo "
        "(que busca ver métricas consolidadas, justificar la inversión y firmar convenios) son radicalmente distintas a las de un almacenista que "
        "necesita ayuda inmediata a mitad de su turno. Por esta razón, el proyecto implementa tres canales con propósitos y tiempos de respuesta diferenciados."
    )
    doc.add_paragraph(
        "El primer canal es de vinculación presencial: se utiliza el espacio de incubación en el Centro de Emprendimiento e Innovación de CUTonalá "
        "como sede para celebrar juntas con directivos, sesiones de demostración y entrega de constancias. Esta sede física brinda formalidad institucional "
        "y confianza a los secretarios administrativos sin generar costos de renta de oficinas externas, aprovechando la infraestructura universitaria existente."
    )
    doc.add_paragraph(
        "Para la operación diaria del almacén, el soporte se organiza según la urgencia de la situación. Si se trata de un ajuste que puede esperar unas horas "
        "—como la reconfiguración de un catálogo de materiales, el alta de un nuevo edificio o una duda sobre reportes—, la solicitud se ingresa desde el módulo "
        "de mesa de ayuda integrado en SIGRE, donde se asigna un ticket con folio de seguimiento. En cambio, si el problema ocurre en el mostrador cuando hay una "
        "fila de estudiantes y profesores esperando equipo para entrar a clase, esperar un ticket sería inaceptable. Para esos momentos críticos, se habilita "
        "un número exclusivo de WhatsApp institucional atendido por el equipo promotor durante todo el horario de ventanilla (7:00 a 20:00 horas), "
        "permitiendo destrabar cualquier eventualidad en menos de diez minutos sin interrumpir la docencia."
    )

    add_heading_2("4.7 Servicios de capacitación, inducción y acompañamiento")
    doc.add_paragraph(
        "Muchos sistemas de software fracasan en las universidades públicas no por fallas en el código, sino porque el personal sindicalizado de ventanilla "
        "se resiste a utilizarlos o los percibe como una carga de trabajo adicional. Para evitar este riesgo, SIGRE incluye como parte del servicio de suscripción "
        "un programa integral de inducción humana que se adapta al ritmo de los trabajadores de almacén."
    )
    doc.add_paragraph(
        "La capacitación inicial consiste en un taller práctico de 16 horas en el propio mostrador del plantel, donde los almacenistas practican con lectores "
        "de código QR y tabletas utilizando casos reales de su inventario cotidiano. Además, para resolver la rotación de prestadores de servicio social o personal "
        "eventual, se entregan videocápsulas de dos minutos enfocadas en una sola acción (cómo recibir un equipo con daño, cómo autorizar un proyector de urgencia) "
        "y carteles plastificados colocados detrás del mostrador con el paso a paso gráfico, eliminando la necesidad de consultar manuales de texto extensos."
    )

    add_heading_2("4.8 Estrategia de comercialización y mercadeo institucional")
    doc.add_paragraph(
        "La prospección comercial en la Universidad de Guadalajara requiere un enfoque directo, fundamentado en resultados tangibles y no en publicidad genérica. "
        "Nuestra estrategia de comercialización se articula a través de tres acciones concretas:"
    )
    doc.add_paragraph(
        "En primer lugar, la presentación de un dossier ejecutivo de retorno de inversión ante los Secretarios Administrativos, donde se les muestra cómo las mermas "
        "de su propio campus superan el costo anual de SIGRE, demostrando que el sistema genera ahorros netos desde el primer mes. En segundo lugar, una demostración "
        "en vivo de 15 minutos en una tableta durante reuniones de consejo de directores del SEMS, simulando la entrega de un proyector con firma digital y lectura "
        "de QR en menos de veinte segundos. En tercer lugar, como mecanismo para vencer la desconfianza administrativa inicial, se otorga una prueba piloto gratuita "
        "de 30 días en el almacén más congestionado del plantel interesado, condicionando la contratación formal a que el propio personal de ventanilla apruebe la herramienta."
    )
    doc.add_page_break()

    # -------------------------------------------------------------
    # 5. CARACTERÍSTICAS TÉCNICAS DE LA IMPLEMENTACIÓN
    # -------------------------------------------------------------
    add_heading_1("5. Características Técnicas de la Implementación")
    
    add_heading_2("5.1 Validación progresiva del Producto Mínimo Viable (MVP)")
    doc.add_paragraph(
        "El desarrollo técnico de SIGRE no parte de cero. Actualmente existe un Producto Mínimo Viable (MVP) funcional que cuenta con los módulos esenciales: "
        "autenticación institucional con cuentas de correo de la UdeG, catálogo básico de materiales, calendario de apartado de espacios y generación de boletos "
        "con código QR. El financiamiento solicitado permite transformar este prototipo en un producto empresarial robusto, incorporando los requerimientos "
        "recabados en CUTonalá: firma digitalizada de responsivas en PDF oficial, checklist fotográfico en recepción y módulo de contingencia ante caídas de internet."
    )
    
    add_heading_2("5.2 Flujos operativos y módulos de valor")
    doc.add_paragraph(
        "La plataforma estructura la operación del plantel en cuatro módulos principales interconectados. El Módulo de Solicitudes y Reservas permite al profesor "
        "o estudiante consultar en tiempo real la disponibilidad de proyectores y salas, reservando el recurso desde su teléfono celular. El Módulo de Despacho en "
        "Ventanilla permite al almacenista escanear el QR del solicitante, comprobar su identidad en pantalla y registrar la salida en menos de treinta segundos. "
        "El Módulo de Recepción y Auditoría aplica un checklist visual al devolver el material; si el equipo presenta algún daño o faltante, el sistema genera "
        "automáticamente un acta de incidencia con fotografías adjuntas y notifica a la coordinación correspondiente para dar cauce a la reposición formal. "
        "Finalmente, el Módulo de Reportes Ejecutivos provee a la Secretaría Administrativa métricas consolidadas de rotación de activos y horas de uso por edificio."
    )

    add_heading_2("5.3 Ficha técnica de infraestructura cloud, seguridad y desempeño")
    doc.add_paragraph(
        "Para garantizar que los planteles no requieran adquirir servidores físicos ni contratar ingenieros de sistemas dedicados, SIGRE opera completamente "
        "en la nube bajo una arquitectura elástica y segura. A continuación se detallan las especificaciones técnicas que sustentan la fiabilidad del servicio:"
    )

    add_table_title("Tabla 8", "Ficha técnica de arquitectura de software, infraestructura y seguridad")
    tech_t = doc.add_table(rows=7, cols=3)
    tech_t.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_apa_table_borders(tech_t)
    
    headers_tc = ["Componente Tecnológico", "Especificación y Proveedor Cloud", "Parámetro de Calidad y Seguridad"]
    for j, h in enumerate(headers_tc):
        c = tech_t.rows[0].cells[j]
        set_cell_margins(c, top=70, bottom=70, left=70, right=70)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.font.bold = True
        r.font.size = Pt(11)
        
    tc_data = [
        ("Frontend y Aplicación Web", "React 18 con TypeScript, Vite y Tailwind CSS, desplegado en Google Cloud Run.", "Carga inicial < 1.2 segundos, interfaz responsive optimizada para tabletas y móviles."),
        ("Backend y Lógica de Negocio", "Node.js con Express y TypeScript, arquitectura modular con control de concurrencia atómica.", "Tiempos de respuesta de API < 150 ms en operaciones de mostrador."),
        ("Base de Datos Relacional", "PostgreSQL 16 gestionado con Prisma ORM, almacenamiento particionado por plantel.", "Integridad transaccional ACID, cifrado AES-256 en reposo y en tránsito (TLS 1.3)."),
        ("Caché y Control de Empalmes", "Redis 7 para bloqueo temporal de pre-reservas (TTL 15 min) y colas de notificación.", "Prevención estricta de reservas duplicadas o empalmes de auditorios en microsegundos."),
        ("Motor de Actas y Criptografía", "PDFKit y firmas HMAC-SHA256 con sellado de tiempo y dirección IP del firmante.", "Generación instantánea de actas de responsiva foliadas en formato PDF oficial."),
        ("Disponibilidad y Respaldos", "Infraestructura Google Cloud Platform (GCP) con balanceador de carga global.", "Disponibilidad garantizada SLA 99.9%; copias de seguridad automáticas diarias (RPO < 24h, RTO < 2h).")
    ]
    
    for idx, row_vals in enumerate(tc_data):
        row = tech_t.rows[idx + 1]
        for j, val in enumerate(row_vals):
            cell = row.cells[j]
            set_cell_margins(cell, top=60, bottom=60, left=70, right=70)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(val)
            r.font.size = Pt(11)
            if j == 0:
                r.font.bold = True
                
    add_table_note("Elaboración propia con base en el documento de especificaciones técnicas y requerimientos de arquitectura del sistema.")

    add_heading_2("5.4 Plan de contingencia tecnológica y continuidad operativa")
    doc.add_paragraph(
        "En los planteles educativos públicos es común enfrentar caídas esporádicas de internet o cortes de energía eléctrica provocados por tormentas o fallas en la red local. "
        "Si una plataforma de almacén se detiene por falta de conexión, la entrega de equipos se paralizaría y las clases se verían afectadas. "
        "Para eliminar este riesgo de raíz, SIGRE implementa un Plan de Contingencia Operativa en tres etapas coordinadas:"
    )
    doc.add_paragraph(
        "En primer término, el frontend de la plataforma incorpora capacidades de Service Workers y almacenamiento local en el navegador (IndexedDB), "
        "permitiendo que el almacenista continúe registrando salidas y entradas en su tableta o laptop durante un corte de internet temporal. Las operaciones "
        "se encolan de forma segura y se sincronizan automáticamente con el servidor en la nube en cuanto la conexión se restablece."
    )
    doc.add_paragraph(
        "En segundo término, para el escenario extremo de un corte de energía eléctrica prolongado en el edificio que impida el encendido de dispositivos, "
        "cada almacén recibe un Talonario de Contingencia Física con 100 vales oficiales prefoliados. Cada vale cuenta con un código QR estático vinculado al inventario "
        "del plantel. El almacenista anota el código del estudiante y el folio del equipo entregado, conservando la copia física. Al regresar la electricidad, "
        "el personal cuenta con un protocolo de captura rápida por lotes para ingresar los folios en menos de 15 minutos, manteniendo la trazabilidad histórica "
        "del inventario sin haber detenido la marcha del plantel."
    )
    doc.add_page_break()

    # -------------------------------------------------------------
    # 6. TAMAÑO, REQUERIMIENTOS Y PROGRAMACIÓN
    # -------------------------------------------------------------
    add_heading_1("6. Estructura Organizacional, Tamaño y Programación")
    
    add_heading_2("6.1 Capacidad operativa y dimensionamiento inicial")
    doc.add_paragraph(
        "El dimensionamiento de SIGRE responde a la filosofía de operación esbelta (lean startup). Al ser una plataforma SaaS alojada en la nube, "
        "la capacidad técnica de procesamiento de datos es prácticamente infinita y escala de forma elástica sin necesidad de invertir en hardware adicional. "
        "El factor restrictivo real del negocio no es la capacidad del servidor, sino la capacidad humana para capacitar a los almacenistas de cada nuevo "
        "plantel y dar respuesta rápida a sus dudas en ventanilla. Por ello, la empresa programa un crecimiento ordenado: 2 planteles en el Año 1 (fase de "
        "afinación técnica), 8 planteles en el Año 2 y 22 planteles en el Año 3."
    )
    
    add_heading_2("6.2 Estructura organizacional y manual de perfiles inicial")
    doc.add_paragraph(
        "Durante el primer año y medio de operaciones, el equipo fundador de tres personas asume de forma directa y coordinada las tres funciones clave "
        "del negocio, evitando gastos excesivos de nómina antes de alcanzar la madurez comercial:"
    )
    doc.add_paragraph(
        "La Dirección General y Comercialización es coordinada por el Director de Proyecto, responsable de la vinculación institucional con secretarios "
        "administrativos, la firma de convenios de suscripción, el seguimiento financiero y la supervisión de los trámites legales ante el IMPI e INDAUTOR. "
        "Dedica el 60% de su tiempo a labores de prospección presencial y el 40% a la administración ejecutiva del proyecto."
    )
    doc.add_paragraph(
        "La Dirección de Tecnología y Arquitectura de Software está a cargo del Líder Técnico, responsable de la estabilidad del código, el despliegue en Google Cloud, "
        "la seguridad criptográfica de las firmas de responsiva y la resolución de cualquier falla en la plataforma. Mantiene la disponibilidad de la nube por encima del 99.9%."
    )
    doc.add_paragraph(
        "La Coordinación de Implementación y Soporte al Cliente es asumida por el Especialista de Operaciones, quien imparte de forma presencial los talleres de 16 horas "
        "a los almacenistas, distribuye el material visual plastificado y atiende personalmente el canal de WhatsApp institucional para resolver dudas en horario de mostrador."
    )

    add_heading_2("6.3 Plan de escalamiento del equipo de trabajo (Años 1 al 3)")
    doc.add_paragraph(
        "Para atender la recomendación del dictamen técnico sobre la saturación operativa cuando la cartera escale a 22 planteles, se definió un plan de "
        "escalamiento con umbrales objetivos de contratación. En lugar de sumar personal de forma prematura, las incorporaciones se activan cuando el número de "
        "planteles activos sobrepasa la capacidad de atención de los tres fundadores, garantizando que cada nuevo sueldo esté plenamente financiado por los ingresos de suscripción:"
    )

    add_table_title("Tabla 9", "Plan de escalamiento del capital humano conforme al crecimiento de la cartera")
    org_t = doc.add_table(rows=5, cols=4)
    org_t.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_apa_table_borders(org_t)
    
    headers_og = ["Etapa y Volumen de Planteles", "Puesto a Incorporar", "Gatillo de Contratación / Condición", "Responsabilidad Principal del Puesto"]
    for j, h in enumerate(headers_og):
        c = org_t.rows[0].cells[j]
        set_cell_margins(c, top=70, bottom=70, left=70, right=70)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.font.bold = True
        r.font.size = Pt(11)
        
    og_d = [
        ("Año 1: 2 planteles (Validación)", "Equipo fundador inicial (3 personas)", "Arranque del proyecto con capital semilla", "Desarrollo del núcleo, pilotaje en CUTonalá y prospección inicial."),
        ("Año 2: Al superar 6 planteles contratados", "1 Técnico de Soporte Nivel 1 (Medio tiempo)", "Cartera supera los 6 planteles activos (Mes 15)", "Monitoreo del WhatsApp de mostrador y resolución de tickets de soporte."),
        ("Año 2: Al alcanzar 8 planteles contratados", "1 Especialista de Soporte Técnico (Tiempo completo)", "Consolidación de la meta del Año 2 (Mes 22)", "Inducción presencial en planteles nuevos y liberación de carga a fundadores."),
        ("Año 3: Al superar 15 planteles contratados", "1 Coordinador de Customer Success y Onboarding", "Expansión a preparatorias del interior (Mes 28)", "Acompañamiento a administradores, auditorías de uso y cobranza de renovaciones.")
    ]
    
    for idx, row_vals in enumerate(og_d):
        row = org_t.rows[idx + 1]
        for j, val in enumerate(row_vals):
            cell = row.cells[j]
            set_cell_margins(cell, top=60, bottom=60, left=70, right=70)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(val)
            r.font.size = Pt(11)
            if j == 0:
                r.font.bold = True
                
    add_table_note("Elaboración propia con base en el modelo operativo escalable y el presupuesto de OPEX proyectado.")

    add_heading_2("6.4 Justificación de bienes inmuebles, materias primas y legal")
    doc.add_paragraph(
        "A diferencia de una empresa tradicional de manufactura o comercio físico, SIGRE no requiere la compra ni renta de bienes inmuebles comerciales. "
        "El equipo promotor opera bajo un esquema de teletrabajo para las labores de desarrollo de software y análisis financiero, complementado con el uso formal "
        "del espacio de coworking y salas de reunión del Centro de Emprendimiento e Innovación de CUTonalá para juntas presenciales y atención institucional. "
        "Esta decisión ahorra más de $180,000 MXN anuales en arrendamientos y servicios públicos durante la etapa crítica de arranque."
    )
    doc.add_paragraph(
        "En cuanto a materias primas e insumos, el proyecto no utiliza inventarios físicos para venta, sino servicios tecnológicos de consumo mensual "
        "(servidores elásticos en Google Cloud, dominios con cifrado SSL y certificados criptográficos). En el ámbito legal y normativo, los requerimientos "
        "se concentran en el pago de derechos de registro de marca ante el IMPI ($3,126 MXN por clase) y el registro del código ante INDAUTOR ($320 MXN), "
        "además del apego estricto a las disposiciones de la Ley General de Protección de Datos Personales en Posesión de Sujetos Obligados (Cámara de Diputados, 2017)."
    )

    add_heading_2("6.5 Diagrama del Plan de Acción Operativo por Fases")
    doc.add_paragraph(
        "El plan de acción operativo se estructura en cuatro fases secuenciales que abarcan el primer año de operaciones, asegurando que cada etapa cuente "
        "con entregables medibles y criterios claros de avance antes de comprometer recursos en la siguiente fase:"
    )

    add_table_title("Tabla 10", "Diagrama del plan de acción operativo por fases (Año 1 de operaciones)")
    act_t = doc.add_table(rows=5, cols=4)
    act_t.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_apa_table_borders(act_t)
    
    headers_ac = ["Fase del Plan de Acción", "Periodo Estimado", "Objetivo Operativo Central", "Entregables Tangibles y Verificables"]
    for j, h in enumerate(headers_ac):
        c = act_t.rows[0].cells[j]
        set_cell_margins(c, top=70, bottom=70, left=70, right=70)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.font.bold = True
        r.font.size = Pt(11)
        
    ac_data = [
        ("Fase I: Pulido Técnico y Piloto Base", "Meses 1 a 4", "Estabilizar el software en los 3 almacenes de CUTonalá y levantar métricas reales.", "Código desplegado en GCP, 3,000 folios operados y reporte de satisfacción."),
        ("Fase II: Protección Legal y Propiedad Intelectual", "Meses 2 a 6", "Tramitar registro de marca y derechos de autor del código fuente.", "Solicitudes ingresadas ante IMPI e INDAUTOR con título oficial."),
        ("Fase III: Lanzamiento y Gira Comercial", "Meses 5 a 8", "Sostener reuniones ejecutivas con secretarios administrativos y directores.", "25 visitas presenciales a planteles y cierre de 2 contratos anuales."),
        ("Fase IV: Operación y Mesa de Servicio", "Meses 9 a 12", "Atención continua a planteles afiliados y evaluación para escalamiento del Año 2.", "Mesa de WhatsApp con SLA < 2h y reporte de retención del 100% de clientes.")
    ]
    
    for idx, row_vals in enumerate(ac_data):
        row = act_t.rows[idx + 1]
        for j, val in enumerate(row_vals):
            cell = row.cells[j]
            set_cell_margins(cell, top=60, bottom=60, left=70, right=70)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(val)
            r.font.size = Pt(11)
            if j == 0:
                r.font.bold = True
                
    add_table_note("Elaboración propia con base en el plan operativo de despliegue.")

    add_heading_2("6.6 Diagrama de Gantt del Año 1 y Análisis de Ruta Crítica")
    doc.add_paragraph(
        "En atención a la recomendación de la evaluadora senior, a continuación se presenta la representación gráfica estandarizada del cronograma anual "
        "en formato de Diagrama de Gantt matricial. La matriz visualiza la temporalidad mensual (M1 a M12), las dependencias e interacciones entre actividades "
        "y la identificación explícita de la Ruta Crítica [RC]. Cualquier atraso en las tareas de la Ruta Crítica desplazaría de forma automática la fecha de "
        "cobranza y el cumplimiento de las metas financieras del proyecto:"
    )

    add_table_title("Tabla 11", "Diagrama de Gantt anual con dependencias y Ruta Crítica [RC] (Año 1)")
    gantt_t = doc.add_table(rows=9, cols=5)
    gantt_t.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_apa_table_borders(gantt_t)
    
    headers_gt = ["Actividad Clave de Ejecución", "Duración", "Predecesora", "Meses Activos (M1 a M12)", "Ruta Crítica"]
    for j, h in enumerate(headers_gt):
        c = gantt_t.rows[0].cells[j]
        set_cell_margins(c, top=70, bottom=70, left=60, right=60)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.font.bold = True
        r.font.size = Pt(11)
        
    gt_data = [
        ("A1. Refinamiento de arquitectura y módulo offline", "2 meses", "Ninguna", "Mes 1 y Mes 2", "SÍ [RC]"),
        ("A2. Despliegue piloto en almacenes de CUTonalá", "3 meses", "A1", "Mes 2, Mes 3 y Mes 4", "SÍ [RC]"),
        ("A3. Trámites legales y registro ante IMPI/INDAUTOR", "4 meses", "A1", "Mes 2 a Mes 5", "NO (Holgura: 2m)"),
        ("A4. Ajustes de retroalimentación de almacenistas", "1 mes", "A2", "Mes 4 y Mes 5", "SÍ [RC]"),
        ("A5. Preparación de dossiers de ROI y demostraciones", "1 mes", "A4", "Mes 5", "NO (Holgura: 1m)"),
        ("A6. Gira comercial y visitas a Secretarios Adm. UdeG", "4 meses", "A4", "Mes 5, Mes 6, Mes 7 y Mes 8", "SÍ [RC]"),
        ("A7. Firma de primeros contratos anuales (2 planteles)", "2 meses", "A6", "Mes 7 y Mes 8", "SÍ [RC]"),
        ("A8. Despliegue de soporte y evaluación anual de avance", "4 meses", "A7", "Mes 9 a Mes 12", "SÍ [RC]")
    ]
    
    for idx, row_vals in enumerate(gt_data):
        row = gantt_t.rows[idx + 1]
        for j, val in enumerate(row_vals):
            cell = row.cells[j]
            set_cell_margins(cell, top=60, bottom=60, left=60, right=60)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT if j == 0 else WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run(val)
            r.font.size = Pt(11)
            if j == 4 and "SÍ" in val:
                r.font.bold = True
                
    add_table_note("Nota. [RC] denota actividad sobre la Ruta Crítica del proyecto. Duración total del ciclo base: 12 meses sin holguras en desarrollo ni prospección.")
    doc.add_page_break()

    # -------------------------------------------------------------
    # 7. INVERSIONES, COSTOS, INGRESOS Y EVALUACIÓN FINANCIERA
    # -------------------------------------------------------------
    add_heading_1("7. Inversiones, Costos, Ingresos y Evaluación Financiera")
    
    add_heading_2("7.1 Inversión inicial requerida (CAPEX)")
    doc.add_paragraph(
        "Para financiar los seis meses de validación técnica en CUTonalá, cubrir los trámites legales de propiedad intelectual y sostener la labor de prospección "
        "comercial durante la etapa de incubación, se solicita una inversión inicial de $180,000 MXN. Cada partida del presupuesto de capital fue dimensionada "
        "de forma austera pero suficiente para garantizar que el proyecto no sufra problemas de liquidez antes de cobrar sus primeras suscripciones:"
    )

    add_table_title("Tabla 12", "Presupuesto desglosado de inversión inicial requerida (CAPEX)")
    cap_t = doc.add_table(rows=6, cols=3)
    cap_t.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_apa_table_borders(cap_t)
    
    headers_cp2 = ["Partida de Inversión Inicial", "Destino del Gasto de Capital", "Monto Requerido (MXN)"]
    for j, h in enumerate(headers_cp2):
        c = cap_t.rows[0].cells[j]
        set_cell_margins(c, top=70, bottom=70, left=70, right=70)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.font.bold = True
        r.font.size = Pt(11)
        
    c_invest = [
        ("Optimización y pulido técnico del software", "Compensación para desarrollo durante los meses de prueba y afinación en mostrador.", "$75,000 MXN"),
        ("Infraestructura cloud y servidores (Año 1)", "Alojamiento en Google Cloud, base de datos relacional y certificados de seguridad.", "$20,000 MXN"),
        ("Propiedad intelectual y trámites legales", "Registro de marca ante el IMPI (2024) y depósito de software ante INDAUTOR.", "$25,000 MXN"),
        ("Materiales demostrativos y viáticos de venta", "Dossiers ejecutivos impresos, traslados a planteles del interior y presentaciones presenciales.", "$20,000 MXN"),
        ("Fondo de contingencia y reserva operativa", "Respaldo de liquidez para amortiguar desfases en calendarios de pago de los planteles.", "$40,000 MXN")
    ]
    
    for idx, (con, det, mon) in enumerate(c_invest):
        row = cap_t.rows[idx + 1]
        for j, val in enumerate([con, det, mon]):
            cell = row.cells[j]
            set_cell_margins(cell, top=60, bottom=60, left=70, right=70)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT if j < 2 else WD_ALIGN_PARAGRAPH.RIGHT
            r = p.add_run(val)
            r.font.size = Pt(11)
            if j == 0:
                r.font.bold = True
                
    add_table_note("Elaboración propia con base en cotizaciones formales de servicios cloud y tarifas oficiales del IMPI (2024).")

    add_heading_2("7.2 Costos operativos fijos y variables (OPEX)")
    doc.add_paragraph(
        "Al tratarse de una solución tecnológica sin instalaciones físicas propias, la estructura de costos operativos es sumamente esbelta y predecible. "
        "Los costos variables se componen principalmente del consumo de servidores en la nube, que inicia en aproximadamente $1,500 MXN mensuales y escala "
        "de forma suave hasta alcanzar los $5,400 MXN al mes cuando se tienen más de 20 planteles activos. Los costos fijos se integran por la compensación escalonada "
        "del equipo técnico y de soporte ($4,000 a $20,000 MXN mensuales según el número de clientes activos), los viáticos de visita para capacitación en mostrador "
        "y los honorarios por servicios contables y fiscales externos para mantener la empresa al día ante el SAT."
    )

    add_heading_2("7.3 Proyecciones trienales de ingresos (Pesos MXN)")
    doc.add_paragraph(
        "Las proyecciones de venta asumen un modelo de suscripción anual fija que se factura al inicio de cada ciclo presupuestal universitario. "
        "Para mantener una postura conservadora, en el Año 1 únicamente se contabilizan 2 planteles (CUTonalá y 1 Escuela Preparatoria adyacente); "
        "en el Año 2 se incorporan 6 planteles adicionales para llegar a 8; y en el Año 3 se suman 14 dependencias más, alcanzando la meta de 22 planteles activos. "
        "Adicionalmente, se contemplan ingresos por talleres de inducción inicial y personalizaciones menores de catálogos solicitadas por los planteles:"
    )

    add_table_title("Tabla 13", "Proyección trienal de ventas e ingresos en moneda nacional (MXN)")
    proy_t = doc.add_table(rows=5, cols=4)
    proy_t.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_apa_table_borders(proy_t)
    
    headers_py = ["Indicador Comercial", "Año 1 (Piloto)", "Año 2 (Expansión Cautelosa)", "Año 3 (Madurez Operativa)"]
    for j, h in enumerate(headers_py):
        c = proy_t.rows[0].cells[j]
        set_cell_margins(c, top=70, bottom=70, left=70, right=70)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.font.bold = True
        r.font.size = Pt(11)
        
    py_data = [
        ("Planteles activos contratados", "2 Planteles (CUTonalá + 1 Prepa)", "8 Planteles (3 CUs + 5 Prepas)", "22 Planteles (8 CUs + 14 Prepas)"),
        ("Ingresos por suscripciones anuales", "$48,000 MXN", "$264,000 MXN", "$720,000 MXN"),
        ("Ingresos por configuración y talleres", "$15,000 MXN", "$60,000 MXN", "$130,000 MXN"),
        ("TOTAL INGRESOS BRUTOS ANUALES", "$63,000 MXN", "$324,000 MXN", "$850,000 MXN")
    ]
    
    for idx, (met, y1, y2, y3) in enumerate(py_data):
        row = proy_t.rows[idx + 1]
        for j, val in enumerate([met, y1, y2, y3]):
            cell = row.cells[j]
            set_cell_margins(cell, top=60, bottom=60, left=70, right=70)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT if j == 0 else WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run(val)
            r.font.size = Pt(11)
            if idx == 3 or j == 0:
                r.font.bold = True
                
    add_table_note("Elaboración propia con base en el esquema tarifario de suscripciones anuales ($48,000 MXN para CUs y $24,000 MXN para Preparatorias).")

    add_heading_2("7.4 Estado de Resultados Proforma y Punto de Equilibrio")
    doc.add_paragraph(
        "A continuación se desglosa el Estado de Resultados Proforma proyectado para los primeros tres años de vida de la empresa. "
        "El ejercicio refleja la naturaleza típica de las empresas de software de alto impacto: un primer año con resultado contable negativo "
        "debido a la inversión en desarrollo y prueba piloto, financiado plenamente por el capital semilla, seguido de una rápida recuperación "
        "con márgenes de utilidad neta superiores al 30% a medida que la base instalada de planteles crece sin demandar incrementos proporcionales de costos:"
    )

    add_table_title("Tabla 14", "Estado de Resultados Proforma trienal (Cifras en Pesos MXN)")
    pnl_t = doc.add_table(rows=10, cols=4)
    pnl_t.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_apa_table_borders(pnl_t)
    
    headers_pn = ["Rubro Contable", "Año 1 (Validación)", "Año 2 (Crecimiento)", "Año 3 (Consolidación)"]
    for j, h in enumerate(headers_pn):
        c = pnl_t.rows[0].cells[j]
        set_cell_margins(c, top=70, bottom=70, left=70, right=70)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.font.bold = True
        r.font.size = Pt(11)
        
    pnl_d = [
        ("Ingresos Totales", "$63,000", "$324,000", "$850,000", True),
        ("Costo de Servidores y Nube (Directo)", "($18,000)", "($36,000)", "($65,000)", False),
        ("Utilidad Bruta", "$45,000", "$288,000", "$785,000", True),
        ("Gastos de Soporte Técnico y Depuración", "($50,000)", "($120,000)", "($240,000)", False),
        ("Gastos de Vinculación y Traslados", "($15,000)", "($45,000)", "($85,000)", False),
        ("Servicios Contables y Asesoría Legal", "($12,000)", "($24,000)", "($36,000)", False),
        ("Utilidad de Operación (EBITDA)", "($32,000)", "$99,000", "$424,000", True),
        ("Impuestos Proyectados (ISR 30%)", "$0", "($29,700)", "($127,200)", False),
        ("UTILIDAD NETA DEL EJERCICIO", "($32,000)", "$69,300", "$296,800", True)
    ]
    
    for idx, (rub, a1, a2, a3, bld) in enumerate(pnl_d):
        row = pnl_t.rows[idx + 1]
        for j, val in enumerate([rub, a1, a2, a3]):
            cell = row.cells[j]
            set_cell_margins(cell, top=55, bottom=55, left=70, right=70)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT if j == 0 else WD_ALIGN_PARAGRAPH.RIGHT
            r = p.add_run(val)
            r.font.size = Pt(11)
            if bld:
                r.font.bold = True
                
    add_table_note("Elaboración propia. En el Año 1 no se genera provisión de ISR al existir pérdida fiscal deducible para amortizar en ejercicios posteriores.")

    doc.add_paragraph(
        "El punto de equilibrio operativo se alcanza en el mes 14 al registrarse 6 planteles activos (2 centros universitarios y 4 escuelas preparatorias). "
        "A partir de ese momento, la facturación mensual recurrente cubre la totalidad de los costos de servidores, soporte y honorarios administrativos, "
        "generando un flujo de caja positivo e irreversible para la empresa."
    )

    add_heading_2("7.5 Evaluación financiera integral: FEN, TMAR, VPN, TIR y Payback")
    doc.add_paragraph(
        "En cumplimiento directo con las sugerencias metodológicas del dictamen técnico, se procedió a calcular la evaluación financiera formal del proyecto. "
        "Para descontar los flujos futuros de efectivo, se determinó una Tasa Mínima Aceptable de Rendimiento (TMAR) del 15.0% anual. Esta tasa se fundamenta "
        "en la suma de la tasa libre de riesgo de referencia en México (Cetes a 364 días en torno al 10.5%) más una prima de riesgo de mercado del 4.5%, "
        "la cual compensa adecuadamente el riesgo operativo de una iniciativa tecnológica institucional en etapa temprana."
    )
    doc.add_paragraph(
        "Tomando como base la inversión inicial de $180,000 MXN en el Año 0 y los Flujos de Efectivo Neto (FEN) generados en los tres años de proyección "
        "(-$32,000 MXN en el Año 1, +$69,300 MXN en el Año 2 y +$296,800 MXN en el Año 3), se obtuvieron los siguientes indicadores de rentabilidad financiera:"
    )

    add_table_title("Tabla 15", "Evaluación financiera formal: Flujos de efectivo, VPN, TIR y periodo de recuperación")
    fin_t = doc.add_table(rows=8, cols=4)
    fin_t.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_apa_table_borders(fin_t)
    
    headers_fn = ["Periodo / Indicador Financiero", "Flujo de Efectivo Neto (FEN)", "Factor Descuento (TMAR 15%)", "Valor Presente del Flujo (VP)"]
    for j, h in enumerate(headers_fn):
        c = fin_t.rows[0].cells[j]
        set_cell_margins(c, top=70, bottom=70, left=70, right=70)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.font.bold = True
        r.font.size = Pt(11)
        
    fn_data = [
        ("Año 0 (Inversión Inicial CAPEX)", "($180,000.00 MXN)", "1.0000", "($180,000.00 MXN)"),
        ("Año 1 (Fase Piloto y Validación)", "($32,000.00 MXN)", "0.8696", "($27,826.09 MXN)"),
        ("Año 2 (Expansión Inicial a 8 planteles)", "$69,300.00 MXN", "0.7561", "$52,400.76 MXN"),
        ("Año 3 (Madurez y 22 planteles activos)", "$296,800.00 MXN", "0.6575", "$195,150.82 MXN"),
        ("VALOR PRESENTE NETO (VPN @ 15.0%)", "Suma algebraica descontada", "TMAR: 15.0% anual", "$39,725.49 MXN"),
        ("TASA INTERNA DE RETORNO (TIR)", "Tasa donde VPN = 0", "Margen vs TMAR: +7.84%", "22.84% anual"),
        ("RELACIÓN BENEFICIO / COSTO (B/C)", "VP Ingresos / VP Costos e Inv.", "Criterio de aceptación > 1.0", "1.22 veces")
    ]
    
    for idx, row_vals in enumerate(fn_data):
        row = fin_t.rows[idx + 1]
        for j, val in enumerate(row_vals):
            cell = row.cells[j]
            set_cell_margins(cell, top=60, bottom=60, left=70, right=70)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT if j < 2 else WD_ALIGN_PARAGRAPH.RIGHT
            r = p.add_run(val)
            r.font.size = Pt(11)
            if idx in (4, 5, 6) or j == 0:
                r.font.bold = True
                
    add_table_note("Cálculo matemático formal basado en flujos anuales netos. Criterio de viabilidad: VPN > 0 y TIR > TMAR (15.0%).")

    doc.add_paragraph(
        "Los resultados de la evaluación confirman la sólida viabilidad financiera del proyecto desde cualquier ángulo analítico:"
    )
    doc.add_paragraph(
        "El Valor Presente Neto (VPN) asciende a +$39,725.49 MXN. Al ser un valor positivo descontado a una tasa exigente del 15% anual, "
        "significa que el proyecto no solamente recupera los $180,000 MXN invertidos y cubre el rendimiento del 15%, sino que genera una riqueza "
        "adicional neta equivalente a casi $40,000 pesos en moneda de hoy."
    )
    doc.add_paragraph(
        "La Tasa Interna de Retorno (TIR) se ubica en el 22.84% anual, superando ampliamente la tasa de corte (TMAR) del 15.0%. "
        "Este diferencial de 7.84 puntos porcentuales representa un margen de seguridad robusto frente a contingencias económicas o posibles atrasos "
        "en los pagos institucionales. Incluso ante un escenario de mayor costo de capital con una TMAR del 18.0%, el VPN continuaría siendo positivo (+$23,293 MXN)."
    )
    doc.add_paragraph(
        "El Periodo de Recuperación de la Inversión (Payback simple) se concreta en el mes 28 de operación (segundo trimestre del Año 3), "
        "mientras que el Payback Descontado se alcanza en el mes 32. Asimismo, la relación Beneficio/Costo de 1.22 confirma que por cada peso invertido "
        "en valor presente, el proyecto genera 1.22 pesos de beneficios netos descontados."
    )

    add_heading_2("7.6 Condiciones de retorno y rendimientos para el inversionista")
    doc.add_paragraph(
        "Para garantizar transparencia y certidumbre al inversionista de capital semilla, se establece un mecanismo contractual de retorno en dos fases:"
    )
    doc.add_paragraph(
        "Durante los primeros 19 meses, la totalidad de los flujos generados se reinvierte en la consolidación del producto y la reserva de liquidez. "
        "A partir del mes 20, una vez superado el punto de equilibrio operativo, se distribuye trimestralmente el 15% de las utilidades netas generadas "
        "por la cobranza de las suscripciones anuales."
    )
    doc.add_paragraph(
        "La amortización completa del capital aportado de $180,000 MXN se proyecta para finales del tercer año, manteniendo el inversionista su derecho a "
        "recibir el 15% de los dividendos anuales en los ejercicios subsecuentes. Esto representa un flujo recurrente superior a los $44,000 MXN anuales sostenibles "
        "a partir del Año 3, consolidando un esquema de inversión altamente atractivo con riesgo acotado al entorno universitario."
    )
    doc.add_page_break()

    # -------------------------------------------------------------
    # 8. CONCLUSIONES Y PROPUESTA AL INVERSIONISTA
    # -------------------------------------------------------------
    add_heading_1("8. Conclusiones y Propuesta para el Inversionista")
    
    doc.add_paragraph(
        "La formulación y evaluación técnica del proyecto SIGRE demuestra que nos encontramos ante una oportunidad de inversión tecnológica de alta viabilidad "
        "y bajo riesgo relativo. El proyecto resuelve un dolor operativo real, crónico y documentado en casi 200 dependencias de la Universidad de Guadalajara, "
        "donde las pérdidas patrimoniales y las horas de clase desperdiciadas superan con creces el costo de implementar la plataforma."
    )
    doc.add_paragraph(
        "Cuatro fortalezas estratégicas fundamentan la viabilidad del modelo: en primer lugar, un mercado cautivo y homogéneo regido por la misma normatividad; "
        "en segundo término, una estructura tarifaria diseñada específicamente para contratarse mediante adjudicación directa sin fricciones burocráticas; "
        "en tercer lugar, una arquitectura de costos sumamente esbelta que prescinde de inmuebles costosos y mantiene un equipo humano mínimo indispensable; "
        "y finalmente, indicadores financieros contundentes con un VPN de +$39,725 MXN y una TIR del 22.84% a tres años."
    )

    add_note_block(
        "Propuesta formal de inversión",
        "Se solicita una aportación de capital semilla de $180,000 MXN para financiar la fase de validación técnica en CUTonalá, los registros de propiedad "
        "intelectual ante el IMPI e INDAUTOR y el despliegue comercial en planteles de Jalisco, a cambio de una participación del 15% en las utilidades netas "
        "del proyecto, con inicio de pago de dividendos en el mes 20 y amortización completa de capital estimada en el mes 28 de operaciones."
    )
    
    doc.add_page_break()

    # -------------------------------------------------------------
    # 9. REFERENCIAS (APA 7MA EDICIÓN ESTRICTA)
    # -------------------------------------------------------------
    add_heading_1("9. Referencias Bibliográficas")
    
    references = [
        "Asociación Nacional de Universidades e Instituciones de Educación Superior. (2023). Anuario estadístico de la educación superior 2022-2023. ANUIES. http://www.anuies.mx/informacion-y-servicios/informacion-estadistica-de-educacion-superior",
        "Banco Interamericano de Desarrollo. (2020). Metodología del marco lógico para la planificación, el seguimiento y la evaluación de proyectos del BID. Sector de Conocimiento y Aprendizaje del BID. https://publications.iadb.org/es/metodologia-del-marco-logico",
        "Cámara de Diputados del H. Congreso de la Unión. (2017). Ley general de protección de datos personales en posesión de sujetos obligados. Diario Oficial de la Federación. Última reforma publicada el 26 de enero de 2017. https://www.diputados.gob.mx/LeyesBiblio/pdf/LGPDPPSO.pdf",
        "Centro Universitario de Tonalá. (2023). Plan de desarrollo de CUTonalá 2019-2025: Visión 2030. Universidad de Guadalajara. http://www.cutonala.udg.mx/transparencia/pdi",
        "Comisión Económica para América Latina y el Caribe. (2015). Metodología del marco lógico para la planificación, el seguimiento y la evaluación de proyectos y programas (Serie Manuales N° 68). CEPAL / Naciones Unidas. https://www.cepal.org/es/publicaciones/5618-metodologia-marco-logico",
        "Coordinación General de Planeación y Evaluación. (2024). Numeralia institucional de la Red Universitaria. Universidad de Guadalajara. http://www.cgpe.udg.mx/numeralia",
        "Instituto Mexicano de la Propiedad Industrial. (2024). Guía de tarifas por servicios del IMPI: Solicitud de registro de marca y avisos comerciales. Gobierno de México. https://www.gob.mx/impi",
        "Sistema de Educación Media Superior. (2024). Directorio y presencia regional de escuelas preparatorias y módulos del SEMS. Universidad de Guadalajara. https://www.sems.udg.mx/directorio",
        "Universidad de Guadalajara. (2019). Reglamento de adquisiciones, arrendamientos y contratación de servicios de la Universidad de Guadalajara. Gaceta de la Universidad de Guadalajara. http://www.secgen.udg.mx/normatividad/reglamentos"
    ]
    
    for ref in references:
        p_ref = doc.add_paragraph()
        p_ref.paragraph_format.left_indent = Inches(0.5)
        p_ref.paragraph_format.first_line_indent = Inches(-0.5)
        p_ref.paragraph_format.space_after = Pt(9)
        
        parts = ref.split(". ")
        if len(parts) >= 3:
            p_ref.add_run(parts[0] + ". " + parts[1] + ". ")
            r_title = p_ref.add_run(parts[2] + ". ")
            r_title.font.italic = True
            p_ref.add_run(". ".join(parts[3:]))
        else:
            p_ref.add_run(ref)

    doc.add_page_break()

    # -------------------------------------------------------------
    # ANEXO A. MATRIZ DE ATENCIÓN AL DICTAMEN TÉCNICO SENIOR
    # -------------------------------------------------------------
    add_heading_1("Anexo A. Matriz de Atención al Dictamen Técnico de Evaluación Senior")
    
    doc.add_paragraph(
        "A continuación se presenta la matriz detallada de atención a las observaciones y sugerencias emitidas en el dictamen "
        "técnico de evaluación del proyecto SIGRE, precisando las acciones implementadas y su ubicación dentro del documento:"
    )

    add_table_title("Tabla 16", "Matriz de cumplimiento y solventación del dictamen técnico de evaluación")
    dict_t = doc.add_table(rows=8, cols=4)
    dict_t.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_apa_table_borders(dict_t)
    
    headers_dc = ["Criterio de Evaluación", "Observación del Dictamen", "Acción Implementada en el Documento", "Sección y Tabla de Referencia"]
    for j, h in enumerate(headers_dc):
        c = dict_t.rows[0].cells[j]
        set_cell_margins(c, top=70, bottom=70, left=60, right=60)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.font.bold = True
        r.font.size = Pt(11)
        
    dc_rows = [
        ("1. Identificación y Justificación", 
         "Falta justificación cuantitativa con datos estadísticos históricos de pérdidas previas.", 
         "Se incorporó el diagnóstico observacional y estimación de pérdidas ($130,000 a $150,000 MXN anuales) basado en experiencia en Servicios Generales y reportes de almacén, recomendando auditoría formal en la fase piloto.",
         "Sección 1.3 (Tabla 3)"),
         
        ("2. Nicho, Mercado y Comercialización", 
         "Carece de análisis directo sobre la intención de compra real de decisores mediante entrevistas estructuradas.", 
         "Se integró la exploración cualitativa de viabilidad y requerimientos con personal administrativo y el fundamento normativo para adjudicación directa (Reglamento UdeG).",
         "Sección 4.3 (Tabla 6)"),
         
        ("3. Objetivos y Marco Lógico", 
         "No incluye formalmente la Matriz de Marco Lógico (MML) completa.", 
         "Se integró la Matriz de Marco Lógico oficial bajo estándar CEPAL/BID con Fin, Propósito, 4 Componentes y 8 Actividades, con indicadores, medios de verificación y supuestos.",
         "Sección 2.3 (Tabla 4)"),
         
        ("4. Aspectos Técnicos e Implementación", 
         "Faltan especificaciones de infraestructura TI (capacidad, tiempos de respuesta, base de datos) y plan de contingencia.", 
         "Se incluyó la ficha técnica de infraestructura cloud (PostgreSQL 16, Redis, Cloud Run, latencia <150ms) y el Plan de Contingencia con modo offline y vales de contingencia prefoliados.",
         "Secciones 5.3 y 5.4 (Tabla 8)"),
         
        ("5. Estructura Organizacional y Requerimientos", 
         "Falta manual de organización breve y descripción de cargas de trabajo al escalar a 22 planteles.", 
         "Se definió el organigrama funcional y la tabla de escalamiento con gatillos objetivos de contratación (Soporte Nivel 1 en mes 15 y Customer Success en mes 28).",
         "Secciones 6.2 y 6.3 (Tabla 9)"),
         
        ("6. Programación de Inversiones", 
         "Hace falta representación gráfica estandarizada (Gantt) que muestre la ruta crítica.", 
         "Se diseñó el Diagrama de Gantt anual en matriz mensual con dependencias explícitas e identificación visual de las tareas sobre la Ruta Crítica [RC].",
         "Sección 6.6 (Tabla 11)"),
         
        ("7. Costos, Ingresos y Evaluación Financiera", 
         "No se calculan indicadores clave de evaluación financiera de proyectos (VPN, TIR, TMAR, FEN).", 
         "Se integró el cuadro de Flujo de Efectivo Neto (FEN), TMAR del 15.0%, cálculo formal de VPN (+$39,725.49 MXN), TIR (22.84%), relación B/C (1.22) y periodo de recuperación Payback (mes 28).",
         "Sección 7.5 (Tabla 15)")
    ]
    
    for idx, row_vals in enumerate(dc_rows):
        row = dict_t.rows[idx + 1]
        for j, val in enumerate(row_vals):
            cell = row.cells[j]
            set_cell_margins(cell, top=60, bottom=60, left=60, right=60)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT if j < 3 else WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run(val)
            r.font.size = Pt(11)
            if j == 0:
                r.font.bold = True
                
    add_table_note("Elaboración propia con base en el dictamen técnico emitido por el comité evaluador senior.")

    doc.save(output_path)
    print(f"Document created successfully meeting all requirements at: {output_path}")

if __name__ == "__main__":
    out_dir = r"c:\Users\erfierro\Documents\Inversion\docs"
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, "Propuesta_Proyecto_Inversion_SIGRE.docx")
    create_proposal_docx(out_file)
