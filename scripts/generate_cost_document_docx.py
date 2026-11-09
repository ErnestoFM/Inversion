import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def generate_cost_docx(output_path):
    doc = docx.Document()

    # -------------------------------------------------------------------------
    # 1. Configuración de Página (Márgenes APA 2.54 cm / 1 pulgada)
    # -------------------------------------------------------------------------
    section = doc.sections[0]
    section.page_width = Inches(8.5)
    section.page_height = Inches(11.0)
    section.top_margin = Inches(1.0)
    section.bottom_margin = Inches(1.0)
    section.left_margin = Inches(1.0)
    section.right_margin = Inches(1.0)
    section.different_first_page_header_footer = True

    COLOR_NAVY = RGBColor(30, 58, 138)
    COLOR_BLUE = RGBColor(37, 99, 235)
    COLOR_DARK = RGBColor(15, 23, 42)
    COLOR_TEXT = RGBColor(30, 41, 59)
    COLOR_MUTED = RGBColor(100, 116, 139)
    COLOR_GREEN = RGBColor(16, 185, 129)

    # Estilo Normal
    style_normal = doc.styles['Normal']
    style_normal.font.name = 'Calibri'
    style_normal.font.size = Pt(11)
    style_normal.font.color.rgb = COLOR_TEXT
    style_normal.paragraph_format.line_spacing = 1.15
    style_normal.paragraph_format.space_after = Pt(6)
    style_normal.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    # Encabezado y Pie de página (desde página 2)
    header = section.header
    p_hdr = header.paragraphs[0]
    p_hdr.text = "SIGRE | Determinación del Costo de un Producto o Servicio — Red UdeG"
    p_hdr.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_hdr.runs[0].font.name = 'Calibri'
    p_hdr.runs[0].font.size = Pt(8.5)
    p_hdr.runs[0].font.color.rgb = COLOR_MUTED

    footer = section.footer
    p_ftr = footer.paragraphs[0]
    p_ftr.text = "Fierro Meléndez Ernesto Hatuey · Formulación y Evaluación de Proyectos · Docente: Mtra. Abril A. Angulo Sherman"
    p_ftr.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_ftr.runs[0].font.name = 'Calibri'
    p_ftr.runs[0].font.size = Pt(8.5)
    p_ftr.runs[0].font.color.rgb = COLOR_MUTED

    # -------------------------------------------------------------------------
    # Helpers de Formato APA 7
    # -------------------------------------------------------------------------
    def set_cell_margins(cell, top=60, bottom=60, left=80, right=80):
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
            f'<w:top w:val="single" w:sz="12" w:space="0" w:color="1E3A8A"/>'
            f'<w:bottom w:val="single" w:sz="12" w:space="0" w:color="1E3A8A"/>'
            f'<w:insideH w:val="single" w:sz="4" w:space="0" w:color="E2E8F0"/>'
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
                f'<w:bottom w:val="single" w:sz="10" w:space="0" w:color="1E3A8A"/>'
                f'</w:tcBorders>'
            )
            tcPr.append(tcBorders)

    def add_table_title(title_text):
        p_tit = doc.add_paragraph()
        p_tit.paragraph_format.space_before = Pt(12)
        p_tit.paragraph_format.space_after = Pt(4)
        p_tit.paragraph_format.keep_with_next = True
        r_tit = p_tit.add_run(title_text)
        r_tit.font.name = 'Calibri'
        r_tit.font.size = Pt(10)
        r_tit.font.bold = True
        r_tit.font.color.rgb = COLOR_NAVY

    def add_table_note(note_text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(3)
        p.paragraph_format.space_after = Pt(8)
        r_lbl = p.add_run("Nota. ")
        r_lbl.font.italic = True
        r_lbl.font.size = Pt(8.5)
        r_lbl.font.color.rgb = COLOR_MUTED
        r_txt = p.add_run(note_text)
        r_txt.font.size = Pt(8.5)
        r_txt.font.color.rgb = COLOR_MUTED

    def add_figure_caption(fig_num, title_text):
        p_num = doc.add_paragraph()
        p_num.paragraph_format.space_before = Pt(14)
        p_num.paragraph_format.space_after = Pt(2)
        p_num.paragraph_format.keep_with_next = True
        r_num = p_num.add_run(fig_num)
        r_num.font.name = 'Calibri'
        r_num.font.size = Pt(10.5)
        r_num.font.bold = True
        r_num.font.color.rgb = COLOR_NAVY
        
        p_tit = doc.add_paragraph()
        p_tit.paragraph_format.space_before = Pt(0)
        p_tit.paragraph_format.space_after = Pt(6)
        p_tit.paragraph_format.keep_with_next = True
        r_tit = p_tit.add_run(title_text)
        r_tit.font.name = 'Calibri'
        r_tit.font.size = Pt(10)
        r_tit.font.italic = True
        r_tit.font.color.rgb = COLOR_DARK

    def add_figure_note(note_text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(3)
        p.paragraph_format.space_after = Pt(10)
        r_lbl = p.add_run("Nota. ")
        r_lbl.font.italic = True
        r_lbl.font.size = Pt(8.5)
        r_lbl.font.color.rgb = COLOR_MUTED
        r_txt = p.add_run(note_text)
        r_txt.font.size = Pt(8.5)
        r_txt.font.color.rgb = COLOR_MUTED

    def add_heading_1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(18)
        p.paragraph_format.space_after = Pt(8)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Calibri'
        run.font.size = Pt(14)
        run.font.bold = True
        run.font.color.rgb = COLOR_NAVY

    def add_heading_2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(13)
        p.paragraph_format.space_after = Pt(5)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Calibri'
        run.font.size = Pt(12)
        run.font.bold = True
        run.font.color.rgb = COLOR_BLUE

    def add_heading_3(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Calibri'
        run.font.size = Pt(11)
        run.font.bold = True
        run.font.color.rgb = COLOR_DARK

    # -------------------------------------------------------------------------
    # PORTADA INSTITUCIONAL
    # -------------------------------------------------------------------------
    p_inst = doc.add_paragraph()
    p_inst.paragraph_format.space_before = Pt(15)
    p_inst.paragraph_format.space_after = Pt(4)
    p_inst.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_inst = p_inst.add_run("UNIVERSIDAD DE GUADALAJARA")
    r_inst.font.size = Pt(14)
    r_inst.font.bold = True
    r_inst.font.color.rgb = COLOR_NAVY

    p_cu = doc.add_paragraph()
    p_cu.paragraph_format.space_before = Pt(0)
    p_cu.paragraph_format.space_after = Pt(15)
    p_cu.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_cu = p_cu.add_run("CENTRO UNIVERSITARIO DE TONALÁ (CUTonalá)\nDIVISIÓN DE INGENIERÍAS E INNOVACIÓN TECNOLÓGICA")
    r_cu.font.size = Pt(11)
    r_cu.font.bold = True
    r_cu.font.color.rgb = COLOR_MUTED

    logo_path = os.path.join("docs", "graficos", "slide_2_img_12.png")
    if not os.path.exists(logo_path):
        logo_path = os.path.join("docs", "graficos", "sigre_logo_header.png")
    if os.path.exists(logo_path):
        p_logo = doc.add_paragraph()
        p_logo.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_logo.paragraph_format.space_after = Pt(20)
        r_logo = p_logo.add_run()
        r_logo.add_picture(logo_path, width=Inches(2.5))

    p_materia = doc.add_paragraph()
    p_materia.paragraph_format.space_before = Pt(10)
    p_materia.paragraph_format.space_after = Pt(4)
    p_materia.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_mat = p_materia.add_run("MATERIA: FORMULACIÓN Y EVALUACIÓN DE PROYECTOS")
    r_mat.font.size = Pt(11)
    r_mat.font.bold = True
    r_mat.font.color.rgb = COLOR_BLUE

    p_act = doc.add_paragraph()
    p_act.paragraph_format.space_before = Pt(0)
    p_act.paragraph_format.space_after = Pt(16)
    p_act.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_act = p_act.add_run("ACTIVIDAD:\nDETERMINACIÓN DEL COSTO DE UN PRODUCTO O SERVICIO\nESTUDIO TÉCNICO-FINANCIERO PRO FORMA, SENSIBILIDAD Y MARCO LÓGICO")
    r_act.font.size = Pt(13)
    r_act.font.bold = True
    r_act.font.color.rgb = COLOR_NAVY

    p_proj = doc.add_paragraph()
    p_proj.paragraph_format.space_before = Pt(4)
    p_proj.paragraph_format.space_after = Pt(25)
    p_proj.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_proj = p_proj.add_run("PROYECTO: SISTEMA INTEGRADO DE GESTIÓN DE RECURSOS Y ESPACIOS (SIGRE)\nPLATAFORMA SAAS MULTI-TENANT PARA LA RED UNIVERSITARIA")
    r_proj.font.size = Pt(11.5)
    r_proj.font.italic = True
    r_proj.font.color.rgb = COLOR_DARK

    p_meta = doc.add_paragraph()
    p_meta.paragraph_format.space_before = Pt(20)
    p_meta.paragraph_format.space_after = Pt(4)
    p_meta.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    r_m1 = p_meta.add_run("Alumno: ")
    r_m1.font.bold = True
    p_meta.add_run("Fierro Meléndez Ernesto Hatuey\n")
    
    r_m2 = p_meta.add_run("Docente: ")
    r_m2.font.bold = True
    p_meta.add_run("Mtra. Abril Adriana Angulo Sherman\n")
    
    r_m3 = p_meta.add_run("Fecha de Entrega: ")
    r_m3.font.bold = True
    p_meta.add_run("13 de octubre de 2026 | Tonalá, Jalisco, México")
    
    for r in p_meta.runs:
        r.font.size = Pt(10)
        r.font.color.rgb = COLOR_TEXT

    doc.add_page_break()

    # =========================================================================
    # SECCIÓN 1: ANTECEDENTES Y PROBLEMÁTICA / SOLUCIÓN
    # =========================================================================
    add_heading_1("1. Antecedentes del Proyecto y Planteamiento Problemática-Solución")
    
    add_heading_2("1.1. Diagnóstico de la Problemática en la Red Universitaria UdeG")
    doc.add_paragraph(
        "La Universidad de Guadalajara (UdeG) es la segunda red pública de educación superior más grande "
        "de México. Su estructura agrupa 193 dependencias académicas y administrativas, entre centros universitarios "
        "temáticos y regionales, el Sistema de Educación Media Superior (SEMS) y dependencias de la administración general "
        "(Universidad de Guadalajara, 2022). Diariamente, estos recintos gestionan préstamos de equipo especializado de cómputo, "
        "electrónica, audiovisual y talleres para atender a más de 330,000 estudiantes matriculados (ANUIES, 2023)."
    )
    doc.add_paragraph(
        "A pesar de esta envergadura institucional, las inspecciones directas realizadas en almacenes, laboratorios y talleres "
        "del Centro Universitario de Tonalá (CUTonalá) revelaron que la gestión operativa de préstamo y resguardo de instrumental "
        "opera de manera arcaica y vulnerable a fallas sistemáticas:"
    )
    
    p_b1 = doc.add_paragraph()
    r = p_b1.add_run("1. Inexistencia de trazabilidad en tiempo real: ")
    r.bold = True
    p_b1.add_run(
        "Los préstamos de proyectores, osciloscopios, cámaras de alta resolución y kits de robótica se anotan en bitácoras físicas de papel. "
        "Los coordinadores de almacén carecen de visibilidad inmediata sobre la ubicación física del bien o la identidad precisa del usuario activo, "
        "lo que imposibilita la auditoría patrimonial oportuna."
    )

    p_b2 = doc.add_paragraph()
    r2 = p_b2.add_run("2. Vulnerabilidad de vales de papel y colisiones de inventario: ")
    r2.bold = True
    p_b2.add_run(
        "Los formatos impresos firmados a mano sufren extravíos frecuentes, deterioro físico y no constituyen un registro forense auditable ante la Contraloría. "
        "Asimismo, la asignación de espacios y equipo se gestiona en hojas desconectadas, generando traslapes recurrentes en horas pico de laboratorio."
    )

    p_b3 = doc.add_paragraph()
    r3 = p_b3.add_run("3. Ausencia de incentivos de responsabilidad y riesgo de impunidad: ")
    r3.bold = True
    p_b3.add_run(
        "No existe un historial unificado que consolide las incidencias de retraso, daño o entrega incompleta. El personal de ventanilla "
        "enfrenta confrontaciones individuales al carecer de un marco paramétrico que regule la elegibilidad de préstamo del solicitante."
    )

    add_heading_2("1.2. Cuantificación Financiera del Problema y Mermas Operativas")
    doc.add_paragraph(
        "Para fundamentar el proyecto bajo el rigor de la formulación y evaluación de inversiones (Baca Urbina, 2013), "
        "se cuantificó el impacto económico que genera el esquema manual en un centro universitario promedio (caso base CUTonalá / CUCEI). "
        "En dichos planteles se tramitan aproximadamente 300 solicitudes de préstamo diarias en ventanillas de laboratorios y almacenes centrales. "
        "Considerando un calendario escolar activo de 200 días hábiles al año, el volumen transaccional asciende a 60,000 préstamos anuales."
    )
    doc.add_paragraph(
        "El cronometraje en sitio evidenció que el llenado de un vale manual de papel (búsqueda de libreta, captura manuscrita de datos, "
        "revisión de credencial física, firma autógrafa y archivo en carpeta) toma un promedio de 4.5 minutos. Con la digitalización mediante "
        "código QR institucional en SIGRE, este tiempo se reduce a 0.45 minutos (<27 segundos), lo que implica una disminución del 90.0% "
        "en los tiempos de espera y atención."
    )
    doc.add_paragraph(
        "Esta ineficiencia analógica se traduce en 4,500 horas-hombre anuales de personal técnico y operativo consumidas exclusivamente "
        "en burocracia de ventanilla por plantel. Al valorarse bajo el tabulador salarial de personal operativo de la Universidad de Guadalajara "
        "(costo horario promedio de $110.00 MXN con prestaciones de ley), representa una pérdida laboral de $495,000.00 MXN anuales. "
        "Respecto a las mermas de equipo, la tasa histórica de merma del 4% al 6% anual en instrumental rotativo menor se obtuvo a partir "
        "de un levantamiento empírico de campo directo realizado durante el ciclo escolar 2025-B/2026-A en CUTonalá. Mediante entrevistas "
        "semiestructuradas y contrastación muestral de bitácoras físicas con cuatro encargados de almacén y laboratoristas (Laboratorio de Electrónica, "
        "Almacén de Cómputo, Ciencias Básicas y Audiovisual), se cotejó el inventario registrado en libros contra los bienes efectivamente devueltos, "
        "identificándose una merma promedio de $240,000.00 MXN anuales por centro universitario en cables, multímetros, adaptadores, sensores "
        "y proyectores portátiles. Sumando $16,500.00 MXN en papelería física, la fuga operativa total por plantel alcanza $751,500.00 MXN anuales."
    )

    add_heading_3("1.2.1. Costo de Oportunidad Académico y Deterioro Formativo")
    doc.add_paragraph(
        "Más allá del quebranto estrictamente monetario, la merma y extravío no controlado de equipo acarrea un severo costo de oportunidad académico. "
        "Cuando un osciloscopio digital, un kit de microcontroladores o un proyector multimedia no son devueltos a tiempo o quedan inutilizados "
        "sin un responsable identificado, los profesores se ven forzados a modificar de emergencia sus planeaciones didácticas o suspender prácticas clave. "
        "Esto provoca que brigadas de estudiantes que deberían realizar mediciones individuales tengan que agruparse en equipos de cuatro o cinco alumnos "
        "por estación de trabajo, reduciendo drásticamente el tiempo de contacto práctico con los instrumentos, retrasando los calendarios curriculares "
        "y deteriorando directamente el desarrollo de competencias tecnológicas acreditables exigidas por organismos acreditadores nacionales e internacionales "
        "(como CACEI o CONAET)."
    )
    doc.add_paragraph(
        "Para transformar este impacto cualitativo en un indicador de gestión medible y auditable, se formalizó la métrica "
        "Tasa de Prácticas Suspendidas o Reprogramadas por Faltante de Instrumental (TPSR), calculada como el porcentaje de prácticas programadas "
        "que sufren demoras, suspensiones o adecuaciones forzadas por falta de equipo funcional. La línea base diagnóstica levantada en CUTonalá "
        "durante el ciclo 2025-B/2026-A arrojó una TPSR del 14.5% en los laboratorios de Electrónica, Computación y Ciencias Básicas. Con la implementación "
        "de SIGRE —mediante el módulo de reserva predictiva con 48 horas de anticipación, la verificación de kits completos mediante código QR "
        "y la alerta temprana de insumos en stock—, la meta operacional para el primer año de despliegue establece reducir la TPSR a menos del 1.5% semestral, "
        "disminuyendo en un 89.7% las afectaciones formativas y blindando los estándares de calidad académica requeridos en los procesos de reacreditación."
    )

    add_table_title("Cuantificación del impacto económico por gestión manual vs. ahorro con SIGRE (Centro Universitario Promedio)")
    t_quant = doc.add_table(rows=11, cols=4)
    t_quant.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_apa_table_borders(t_quant)

    headers_quant = ["Parámetro Operativo / Financiero Analizado", "Gestión Manual (Papel)", "Plataforma SIGRE", "Ahorro / Beneficio Neto"]
    for c_i, h in enumerate(headers_quant):
        cell = t_quant.rows[0].cells[c_i]
        cell.paragraphs[0].text = h
        cell.paragraphs[0].runs[0].font.bold = True
        cell.paragraphs[0].runs[0].font.size = Pt(9.5)
        cell.paragraphs[0].runs[0].font.color.rgb = COLOR_NAVY
        set_cell_margins(cell, 45, 45, 55, 55)

    rows_quant_data = [
        ("Solicitudes anuales tramitadas en ventanillas (200 días)", "60,000 préstamos", "60,000 préstamos", "Mismo volumen atendido"),
        ("Tiempo promedio por transacción en ventanilla", "4.5 minutos", "0.45 minutos", "-4.05 min (-90.0% de reducción)"),
        ("Horas-hombre consumidas al año en ventanilla", "4,500 horas", "450 horas", "4,050 horas-hombre liberadas"),
        ("Costo anual de nómina absorbido en burocracia de vales", "$495,000.00 MXN", "$49,500.00 MXN", "$445,500.00 MXN en tiempo recuperado"),
        ("Mermas y extravíos anuales de instrumental/equipo", "$240,000.00 MXN", "$12,000.00 MXN", "$228,000.00 MXN mitigados (95% control)"),
        ("Gasto anual en papelería física (vales, tóner, carpetas)", "$16,500.00 MXN", "$0.00 MXN", "$16,500.00 MXN (eliminación total)"),
        ("COSTO TOTAL ANUAL DE INEFICIENCIA POR PLANTEL", "$751,500.00 MXN", "$61,500.00 MXN", "$690,000.00 MXN ahorro bruto anual"),
        ("Tasa de Prácticas de Laboratorio Afectadas (TPSR)", "14.5% semestral (hacinamiento 4-5)", "< 1.5% semestral", "Reducción 89.7% (Blindaje CACEI)"),
        ("Costo de Adopción de Licencia Anual SIGRE (1 Almacén)", "$0.00 MXN", "$28,950.00 MXN", "-$28,950.00 MXN inversión anual"),
        ("BENEFICIO NETO ANUAL GENERADO AL CENTRO UNIVERSITARIO", "-$751,500.00 MXN", "$661,050.00 MXN", "ROI Operativo: 2,283% | Payback: 15 días")
    ]

    for r_i, r_data in enumerate(rows_quant_data, start=1):
        for c_i, val in enumerate(r_data):
            cell = t_quant.rows[r_i].cells[c_i]
            cell.paragraphs[0].text = val
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT if c_i == 0 else WD_ALIGN_PARAGRAPH.RIGHT
            if c_i in (1, 2) and r_i in (1, 2, 3, 8): p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.runs[0].font.size = Pt(9)
            if r_i in (7, 10):
                p.runs[0].font.bold = True
                p.runs[0].font.color.rgb = COLOR_NAVY
            set_cell_margins(cell, 40, 40, 50, 50)

    add_table_note("Cálculo formal con base en tabulador UdeG ($110/hora técnico operativo), mermas empíricas y registro de incidencias en CUTonalá.")

    add_heading_2("1.3. Propuesta de Solución: Plataforma SaaS SIGRE")
    doc.add_paragraph(
        "Como respuesta estructural a esta problemática se formuló SIGRE (Sistema Integrado de Gestión de Recursos y Espacios), "
        "una solución tecnológica concebida como Software como Servicio (SaaS) multi-tenant, alojada en Google Cloud Platform. "
        "SIGRE automatiza íntegramente el ciclo de préstamo institucional mediante lectura de credenciales con código QR dinámico, "
        "emisión de actas responsivas en PDF con firma digital y sellado criptográfico, y la implementación de un motor de scoring predictivo "
        "que califica la fiabilidad y puntualidad del estudiante o académico."
    )

    add_heading_2("1.4. Estudio de Mercado Breve y Benchmarking Competitivo")
    doc.add_paragraph(
        "El análisis competitivo demuestra que las opciones disponibles en el mercado tecnológico no resuelven la problemática "
        "universitaria bajo condiciones de viabilidad financiera y regulatoria:"
    )
    doc.add_paragraph(
        "1. ERPs Corporativos (SAP Ariba, Oracle NetSuite): Aunque poseen módulos avanzados de gestión de activos, su implementación "
        "demanda entre 6 y 12 meses, costos anuales de licenciamiento que superan los $220,000 - $480,000 MXN y cientos de miles de pesos en consultoría. "
        "Asimismo, su adquisición forzosa mediante Licitación Pública Nacional genera una fricción administrativa que retrasa la adopción.\n"
        "2. Software Comercial para PyMEs (Odoo, Zoho Inventory): Orientados al comercio minorista y cadenas de suministro de compra-venta. "
        "No ofrecen flujos de ventanilla rápida con credencial universitaria, carecen de scoring algorítmico y no contemplan las exigencias de privacidad "
        "de datos del sector público jalisciense.\n"
        "3. Gestión Manual / Hojas de Cálculo (Vales de papel y Google Sheets): Tienen un costo de adquisición aparentemente nulo, pero conllevan "
        "la fuga de más de $750,000 MXN anuales demostrada previamente, exponiendo además a las autoridades a sanciones legales por incumplimiento "
        "de la Ley General de Protección de Datos Personales en Posesión de Sujetos Obligados (LGPDPPSO) al dejar datos expuestos en papel."
    )

    add_table_title("Matriz de benchmarking competitivo frente a alternativas de mercado")
    t_bm = doc.add_table(rows=7, cols=5)
    t_bm.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_apa_table_borders(t_bm)

    headers_bm = ["Criterio de Evaluación", "SIGRE (Propuesta)", "ERP Corporativo (SAP/Oracle)", "Software Comercial (Odoo/Zoho)", "Gestión Manual (Papel)"]
    for c_i, h in enumerate(headers_bm):
        cell = t_bm.rows[0].cells[c_i]
        cell.paragraphs[0].text = h
        cell.paragraphs[0].runs[0].font.bold = True
        cell.paragraphs[0].runs[0].font.size = Pt(8.5)
        cell.paragraphs[0].runs[0].font.color.rgb = COLOR_NAVY
        set_cell_margins(cell, 45, 45, 45, 45)

    rows_bm_data = [
        ("Costo anual por dependencia", "$28,950.00 MXN", "$220,000 - $480,000 MXN", "$65,000 - $110,000 MXN", "$0 MXN (aparente)"),
        ("Mecanismo de contratación pública", "Adjudicación Directa (Art. 55)", "Licitación Pública Nacional", "Licitación / Invitación", "No aplica"),
        ("Tiempo de atención en ventanilla", "< 27 segundos (QR dinámico)", "2 a 3 minutos", "1 a 2 minutos", "4 a 5 minutos"),
        ("Scoring predictivo de fiabilidad", "Sí (algoritmo nativo)", "No nativo (desarrollo extra)", "No disponible", "Inexistente"),
        ("Modo contingencia offline (PWA)", "Sí (IndexedDB + AES-256)", "No (requiere red fija)", "Parcial (app móvil)", "Papel (sin trazabilidad)"),
        ("Cumplimiento normativo LGPDPPSO", "Nativo (auditoría ITEI)", "Requiere parametrización", "Parcial (enfoque privado)", "Nulo (infracción legal)")
    ]

    for r_i, r_data in enumerate(rows_bm_data, start=1):
        for c_i, val in enumerate(r_data):
            cell = t_bm.rows[r_i].cells[c_i]
            cell.paragraphs[0].text = val
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT if c_i == 0 else WD_ALIGN_PARAGRAPH.CENTER
            p.runs[0].font.size = Pt(8.5)
            if c_i == 1:
                p.runs[0].font.bold = True
                p.runs[0].font.color.rgb = COLOR_BLUE
            set_cell_margins(cell, 40, 40, 45, 45)

    add_table_note("El umbral de adjudicación directa bajo el Art. 55 de la Ley de Compras de Jalisco faculta contrataciones menores sin licitación.")

    add_heading_3("1.4.1. Estrategia de Gestión del Cambio Operativo y Protocolo Sindical (SUTUdeG)")
    doc.add_paragraph(
        "En instituciones públicas de educación superior, la principal barrera de adopción radica en la inercia cultural "
        "y la resistencia del personal operativo de base ante herramientas digitales percibidas erróneamente como fiscalización. "
        "Para asegurar una adopción armónica y participativa, se diseñó una estrategia integral sustentada en cuatro ejes:"
    )
    doc.add_paragraph(
        "• Talleres Prácticos Breves (30 minutos): Sesiones presenciales en la propia ventanilla del almacén, libres de jerga computacional, "
        "enfocadas en la mecánica directa de escaneo y entrega con equipos reales.\n"
        "• Red de 'Laboratoristas Campeones': Identificación y capacitación prioritaria de los encargados de turno con mayor liderazgo de opinión "
        "en los almacenes de CUTonalá, convirtiéndolos en mentores y promotores internos de la plataforma frente a sus compañeros.\n"
        "• Protocolo de Contención de Fricciones Sindicales (SUTUdeG): El diálogo con los delegados gremiales del Sindicato Único de Trabajadores "
        "de la Universidad de Guadalajara se estructura en torno a una premisa clara: SIGRE no es una herramienta de vigilancia punitiva ni incrementa "
        "las cargas de trabajo, sino que constituye un escudo de protección patrimonial y legal para el trabajador. Bajo el esquema analógico, "
        "cuando un equipo costoso se extravía durante una auditoría interna, el almacenista suele ser investigado administrativamente; "
        "con SIGRE, la responsabilidad civil queda formalmente transferida al solicitante mediante un acta digital inmutable con firma electrónica, "
        "deslindando al trabajador sindicalizado de cualquier responsabilidad económica injusta.\n"
        "• Sub-Hito Formal de Socialización y Visto Bueno Sindical (Mes 6): En las últimas dos semanas del Mes 6, previo a la apertura de ventanillas del piloto, "
        "se formaliza la celebración de un taller demostrativo y mesa de diálogo con los delegados seccionales del SUTUdeG en CUTonalá. En este acto se suscribe "
        "la Minuta de Concertación y Visto Bueno Sindical, donde el sindicato avala formalmente el uso de la herramienta tras constatar que el vale digital "
        "con firma electrónica protege patrimonialmente al personal operativo ante la Contraloría General y no altera perjudicialmente sus condiciones laborales, "
        "blindando la fase de marcha blanca ante cualquier fricción gremial.\n"
        "• Acompañamiento en Sitio durante la Marcha Blanca: Durante las dos primeras semanas de operación, un ingeniero de soporte permanecerá físicamente "
        "en ventanilla durante las horas pico para asistir en vivo al personal ante cualquier eventualidad o duda operativa."
    )

    add_heading_3("1.4.2. Estimación del Costo de Adquisición de Clientes (CAC) Institucional y Ratio LTV/CAC")
    doc.add_paragraph(
        "Aun cuando la comercialización en la Red Universitaria opera bajo el esquema de contratación por Adjudicación Directa "
        "(amparada en el Artículo 55 de la Ley de Compras Gubernamentales del Estado de Jalisco al no rebasar el umbral anual de compras menores), "
        "el proceso de venta institucional (B2G) exige una inversión técnica y de cabildeo directivo previa a la formalización de cada convenio. "
        "Para dotar de máximo rigor al modelo de negocio, se monetizó el Costo de Adquisición de Clientes (CAC) Institucional por centro universitario o dependencia:"
    )
    doc.add_paragraph(
        "• Horas de Ingeniería Técnica en Preventa: 25 horas dedicadas a reuniones ejecutivas, demostraciones en vivo en ventanilla y levantamiento de inventarios "
        "muestrales con secretarios administrativos, directores de división y jefes de laboratorio, valoradas a un costo técnico de $150.00 MXN/hora ($3,750.00 MXN).\n"
        "• Viáticos y Material Técnico de Difusión: Gastos de traslado intercampus en el Área Metropolitana de Guadalajara y carpetas técnicas institucionales ($1,250.00 MXN).\n"
        "• Costo de Adquisición de Clientes (CAC Institucional) Total: $5,000.00 MXN por campus o dependencia cabecera.\n"
        "• Valor de Vida del Cliente (Customer Lifetime Value - LTV): Con una cuota anual de $28,950.00 MXN y un horizonte contractual conservador de 3 años, "
        "el LTV por dependencia asciende a $86,850.00 MXN netos.\n"
        "• Ratio LTV / CAC Institucional: El cociente $86,850.00 / $5,000.00 se sitúa en 17.37x. En el análisis de inversiones de software, una razón LTV/CAC "
        "superior a 3.0x se considera financieramente atractiva y sostenible; alcanzar 17.37x ratifica que el esfuerzo de preventa técnica se amortiza por completo "
        "en los primeros 2.1 meses de operación del primer año, confirmando una alta eficiencia comercial."
    )

    add_heading_2("1.5. Matriz de Marco Lógico (MML) del Proyecto")
    doc.add_paragraph(
        "Siguiendo los lineamientos metodológicos de CEPAL e ILPES para la formulación de proyectos de inversión "
        "(Ortegón, Pacheco y Prieto, 2005), se formuló la Matriz de Marco Lógico (MML) de SIGRE, vinculando cada supuesto "
        "con su respectiva acción de mitigación implícita:"
    )

    add_table_title("Matriz de Marco Lógico (MML) del Proyecto SIGRE — Metodología CEPAL / ILPES")
    t_mml = doc.add_table(rows=5, cols=5)
    t_mml.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_apa_table_borders(t_mml)

    headers_mml = ["Nivel de Objetivo", "Resumen Narrativo", "Indicadores Verificables (IOV)", "Medios de Verificación", "Supuestos Críticos y Mitigación Implícita"]
    for c_i, h in enumerate(headers_mml):
        cell = t_mml.rows[0].cells[c_i]
        cell.paragraphs[0].text = h
        cell.paragraphs[0].runs[0].font.bold = True
        cell.paragraphs[0].runs[0].font.size = Pt(8.5)
        cell.paragraphs[0].runs[0].font.color.rgb = COLOR_NAVY
        set_cell_margins(cell, 45, 45, 45, 45)

    rows_mml_data = [
        ("FIN",
         "Contribuir a la modernización tecnológica, transparencia en la rendición de cuentas públicas y optimización del gasto en control de materiales de la Red Universitaria UdeG.",
         "1. Tasa de pérdida de activos reducida a <0.5% en centros participantes al término del Año 3.\n2. Reducción del 85% en tiempos de espera en ventanillas de laboratorios a nivel Red.\n3. Reducción de la TPSR a <1.5% semestral.",
         "Dictámenes telemétricos y reportes de discrepancia cero generados nativamente por SIGRE; actas de cierre semestral de inventario firmadas por las Coordinaciones de Laboratorio de los campus.",
         "Supuesto: La UdeG mantiene prioridad en digitalización. // Mitigación ante recortes presupuestales: El ROI acelerado ($661k de ahorro neto vs $28k de costo con payback de 15 días) convierte a SIGRE en una medida de austeridad y ahorro operativo que blinda el proyecto ante recortes."),
        ("PROPÓSITO",
         "Optimizar el proceso de solicitud, validación de riesgo, despacho y devolución de inventario en almacenes y ventanillas de centros universitarios (Piloto CUTonalá, expansión a CUCEI y red).",
         "1. Tiempo promedio de despacho por vale menor a 30 segundos en el 98% de casos.\n2. 100% de préstamos con trazabilidad criptográfica y score de riesgo al cierre del Año 1.",
         "Métricas telemétricas de Cloud SQL / BigQuery; reportes mensuales de operación de SIGRE; bitácoras de auditoría de despacho.",
         "Supuesto: Personal aplica la plataforma con disciplina. // Mitigación: La red de 'Laboratoristas Campeones', los talleres breves de 30 min y el deslinde de responsabilidades patrimoniales neutralizan la resistencia de base."),
        ("COMPONENTES",
         "C1. Plataforma SaaS en GCP (Cloud Run, PostgreSQL, Secret Manager).\nC2. Motor de Scoring de Fiabilidad.\nC3. Interfaz PWA con modo offline.\nC4. Programa de Capacitación, Gobernanza LGPDPPSO y Manuales.",
         "1. Disponibilidad de plataforma de 99.5% mensual (SLA Cloud Run).\n2. Capacidad de operación offline local de hasta 4 horas consecutivas.\n3. 100% de personal operativo de almacenes piloto acreditado.",
         "Dashboard de monitoreo Google Cloud; reportes de pruebas k6; actas de acreditación de capacitación y entrega de manuales.",
         "Supuesto: Intermitencias en la red de campus. // Mitigación: Arquitectura Offline-First con IndexedDB y Service Workers garantiza despacho ininterrumpido en <20 s sin conexión."),
        ("ACTIVIDADES",
         "A1. Arquitectura Cloud en GCP (M1-M2).\nA2. Scoring algorítmico y PWA offline (M3-M4).\nA3. QA, pruebas k6, pentesting OWASP y auditoría LGPDPPSO (M5-M6).\nA4. Registro software INDAUTOR y Visto Bueno SUTUdeG (M6).\nA5. Piloto CUTonalá y talleres (M7-M9).\nA6. KPIs y release v1.5 (M10-M12).",
         "1. Inversión ejecutada conforme a cronograma de $120,000 MXN en Año 1.\n2. 100% de hitos técnicos concluidos en fechas programadas.\n3. Certificado INDAUTOR y Dictamen de Pentesting obtenidos en Mes 6.",
         "Repositorio GitHub con tags de release firmados; comprobante oficial INDAUTOR; listas de asistencia a talleres de capacitación y minuta sindical.",
         "Supuesto: Retrasos en procesos de compra y firmas. // Mitigación: Adjudicación directa Art. 55 (<$200k) y colchón de capital semilla de $120k que absorbe hasta 4 meses de morosidad administrativa.")
    ]

    for r_i, r_data in enumerate(rows_mml_data, start=1):
        for c_i, val in enumerate(r_data):
            cell = t_mml.rows[r_i].cells[c_i]
            cell.paragraphs[0].text = val
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_i == 0 else WD_ALIGN_PARAGRAPH.LEFT
            p.runs[0].font.size = Pt(8)
            if c_i == 0:
                p.runs[0].font.bold = True
                p.runs[0].font.color.rgb = COLOR_NAVY
            set_cell_margins(cell, 35, 35, 45, 45)

    add_table_note("Elaboración formal con base en la metodología de marco lógico de CEPAL (Ortegón et al., 2005), integrando acciones de mitigación de riesgo por nivel.")

    add_heading_3("1.5.1. Mecanismo de Gobernanza y Revisión Periódica Trimestral de la MML")
    doc.add_paragraph(
        "Para garantizar que los Indicadores Objetivamente Verificables (IOV) no operen como parámetros estáticos de gabinete, se formaliza un "
        "Comité Técnico de Seguimiento Operativo integrado por el Lead Developer, el Coordinador de Soporte y el enlace administrativo del campus. "
        "Este comité sesionará con periodicidad trimestral durante el Año 1 (al cierre de Q1, Q2, Q3 y Q4) para auditar las métricas telemétricas extraídas "
        "automáticamente de Google Cloud SQL y los reportes de despacho de SIGRE. Si se detecta una desviación superior al 5.0% respecto a las metas "
        "(ej. tiempo de despacho en ventanilla superior a 30 segundos o merma mensual mayor al 0.5%), se activa un protocolo de recalibración que reordena "
        "el backlog del siguiente sprint de desarrollo y refuerza la capacitación presencial en la ventanilla afectada."
    )

    # =========================================================================
    # SECCIÓN 2: PLAN DE SERVICIO OPERATIVO Y ARQUITECTURA TECNOLÓGICA
    # =========================================================================
    add_heading_1("2. Plan de Servicio Operativo y Arquitectura Tecnológica")
    doc.add_paragraph(
        "SIGRE opera mediante un protocolo estructurado en 5 pasos que optimiza la dinámica de ventanilla "
        "y garantiza certeza operativa:"
    )

    steps_data = [
        ("Paso 1: Solicitud y Escaneo del Alumno", "El estudiante o profesor llega a la ventanilla del almacén y muestra el código QR dinámico de su credencial institucional (vía app móvil o física). El almacenista escanea el código con una cámara web o lector óptico USB."),
        ("Paso 2: Validación Instantánea y Scoring de Riesgo", "El sistema consulta de forma instantánea la base de datos y calcula el score de responsabilidad del solicitante. Si el alumno tiene préstamos vencidos o reportes de equipo dañado, el sistema bloquea el préstamo de equipo delicado o exige autorización especial del jefe de laboratorio."),
        ("Paso 3: Selección de Equipo y Firma Digital de Acta", "El encargado de ventanilla escanea el código de barras o QR adherido al equipo solicitado (ej. osciloscopio, multímetro, proyector). El sistema genera en automático un acta responsiva digital en formato PDF/A."),
        ("Paso 4: Confirmación en Móvil del Alumno", "El solicitante recibe una notificación push en su teléfono celular donde aprueba la recepción del equipo con un solo toque y firma biométrica o token temporal."),
        ("Paso 5: Devolución, Cierre y Actualización de Reputación", "Al entregar el equipo, el encargado revisa su estado físico, escanea el código y el sistema cierra el folio en menos de 10 segundos, sumando puntos de puntualidad al score del estudiante.")
    ]

    for title, desc in steps_data:
        p_step = doc.add_paragraph()
        p_step.paragraph_format.left_indent = Inches(0.25)
        p_step.paragraph_format.space_after = Pt(4)
        r_tit = p_step.add_run(f"• {title}: ")
        r_tit.bold = True
        r_tit.font.color.rgb = COLOR_NAVY
        p_step.add_run(desc)

    add_heading_2("2.2. Arquitectura Cloud Nativa y Pila Tecnológica (Tech Stack)")
    doc.add_paragraph(
        "La plataforma se implementó sobre infraestructura elástica serverless de Google Cloud Platform (GCP) en la región "
        "us-central1 (Iowa), seleccionada por ofrecer latencias menores a 65 milisegundos hacia el nodo de la Red Universitaria "
        "de Jalisco y garantizar un Acuerdo de Nivel de Servicio (SLA) de disponibilidad del 99.95%."
    )
    doc.add_paragraph(
        "• Cómputo Elástico (Google Cloud Run): Contenedores Docker de ejecución serverless que escalan de forma instantánea de 0 a 10 instancias concurrentes.\n"
        "• Persistencia de Datos (Google Cloud SQL para PostgreSQL): Instancia administrada con almacenamiento SSD en alta disponibilidad zonal y respaldos automáticos.\n"
        "• Almacenamiento de Evidencias (Google Cloud Storage): Repositorio inmutable multi-región para actas digitales en PDF y códigos QR firmados.\n"
        "• Seguridad Criptográfica (Google Secret Manager): Custodia de llaves de cifrado AES-256, tokens de autenticación JWT y credenciales institucionales."
    )

    add_heading_3("2.2.1. Pila Tecnológica (Tech Stack) de la Solución PWA")
    doc.add_paragraph(
        "Para garantizar mantenibilidad a largo plazo, tipado estático riguroso y una experiencia de usuario fluida, "
        "se seleccionó un stack tecnológico moderno de estándar empresarial:\n"
        "• Frontend y Aplicación de Ventanilla (PWA): React 18 con TypeScript y Vite como empaquetador de alto rendimiento; "
        "TailwindCSS para maquetación responsiva; Service Workers con Workbox para control de caché; persistencia reactiva en IndexedDB "
        "mediante Dexie.js y SQLite compilado a WebAssembly (Wasm) con cifrado local AES-256 (Web Crypto API nativa).\n"
        "• Backend y Microservicios: Node.js 20 LTS con TypeScript bajo arquitectura modular y endpoints RESTful/GraphQL, containerizado en Docker sobre Cloud Run.\n"
        "• Persistencia y Seguridad: PostgreSQL 15 en Cloud SQL con extensiones criptográficas (pgcrypto) y políticas de seguridad a nivel de fila (Row Level Security)."
    )

    add_heading_2("2.3. Cumplimiento Normativo y Privacidad de Datos (LGPDPPSO)")
    doc.add_paragraph(
        "Al tratarse de una institución pública descentralizada del Estado de Jalisco, la Universidad de Guadalajara "
        "está sujeta a la Ley General de Protección de Datos Personales en Posesión de Sujetos Obligados (LGPDPPSO; DOF, 2017) "
        "y supervisada por el Instituto de Transparencia, Información Pública y Protección de Datos Personales del Estado de Jalisco (ITEI). "
        "SIGRE incorpora cifrado en tránsito (TLS 1.3), cifrado en reposo (AES-256), anonimización de identificadores en bitácoras telemétricas "
        "y módulos nativos para el ejercicio de derechos ARCO."
    )

    add_heading_3("2.3.1. Prerrequisito de Ciberseguridad: Auditoría Ligera y Prueba de Penetración (Pentesting) OWASP Top 10")
    doc.add_paragraph(
        "Dado que la plataforma gestiona datos de filiación de la comunidad estudiantil y académica protegidos por la LGPDPPSO (DOF, 2017), "
        "se definió como condición obligatoria previa al encendido de la Marcha Blanca en el Mes 7 la ejecución de una auditoría de ciberseguridad "
        "ligera y un análisis de penetración ético (pentesting) enfocado en las vulnerabilidades críticas del estándar OWASP Top 10. "
        "El procedimiento se programa durante el Mes 6 y contempla: (a) análisis estático de código fuente (SAST) mediante SonarQube para identificar "
        "patrones de inyección SQL, validación deficiente de entradas y cross-site scripting (XSS); (b) pruebas dinámicas de intrusión (DAST) automatizadas "
        "con OWASP ZAP sobre los endpoints REST de Google Cloud Run para evaluar la robustez de los tokens JWT y la mitigación de ataques CSRF; "
        "y (c) verificación forense del motor criptográfico local AES-256 en IndexedDB para comprobar la inmutabilidad de los vales offline. "
        "La liberación a producción exige la emisión de un Dictamen Técnico de No Vulnerabilidad Crítica, garantizando a la Secretaría Administrativa "
        "del CUTonalá que la plataforma no expone vectores de filtración de información institucional."
    )

    add_heading_2("2.4. Protocolo de Recuperación ante Desastres (DRP) y Contingencia en Ventanilla")
    doc.add_paragraph(
        "Una de las contingencias operativas más severas en los campus universitarios radica en las interrupciones de conectividad "
        "o saturación de la Red Universitaria (RIUdeG) durante las horas pico de cambio de clase (entre las 10:00 y las 12:00 hrs "
        "y entre las 16:00 y las 18:00 hrs). Para garantizar que la ventanilla no se paralice bajo ninguna circunstancia, SIGRE incorpora "
        "un diseño arquitectónico Offline-First de alta resiliencia:"
    )
    doc.add_paragraph(
        "1. Caché Cifrado Local PWA: La aplicación de ventanilla funciona como una Progressive Web App (PWA) habilitada con Service Workers. "
        "En el navegador del operador se mantiene un repositorio local en IndexedDB cifrado con AES-256 con el catálogo de inventario activo "
        "y la base local de alumnos vigentes con su respectivo score de fiabilidad.\n"
        "2. Vales Digitales de Emergencia (VDE): Si se pierde la conectividad a internet, el sistema conmuta de forma transparente al 'Modo Contingencia Local'. "
        "El operador escanea el código del equipo y la credencial institucional; el sistema valida el préstamo contra la base local, emite la salida "
        "y genera un vale sellado criptográficamente con marca de tiempo (timestamp) y un hash SHA-256 inmutable en la cola de salida local. "
        "El proceso se completa en menos de 20 segundos sin red.\n"
        "3. Sincronización Asíncrona Bidireccional: Al detectar el restablecimiento del enlace de datos, la API de Sincronización en Segundo Plano "
        "(Background Sync API) remite los paquetes encolados hacia Cloud Run en lotes ordenados cronológicamente.\n"
        "4. Política de Resolución de Conflictos: Se aplica la regla 'First-Scanned, First-Assigned' con registro inmutable en PostgreSQL. "
        "En caso de colisión extraordinaria de inventario, el sistema asigna el bien a la transacción con timestamp previo y emite una alerta prioritaria "
        "en la pantalla del segundo operador para sustituir el número de serie de inmediato.\n"
        "5. Métricas DRP en la Nube: El sistema garantiza un Objetivo de Punto de Recuperación (RPO) < 15 minutos mediante respaldos continuos "
        "point-in-time en Cloud SQL, y un Objetivo de Tiempo de Recuperación (RTO) < 30 minutos frente a caídas masivas de centros de datos en GCP."
    )

    add_heading_3("2.4.1. Requerimientos Técnicos Mínimos de Hardware y Software en Ventanilla")
    doc.add_paragraph(
        "Para asegurar que el motor criptográfico local AES-256 y la base de datos IndexedDB operen sin latencia perceptible "
        "durante el modo de contingencia offline, se definieron los requerimientos mínimos de los equipos de cómputo en ventanilla, "
        "garantizando plena compatibilidad con el parque tecnológico actualmente instalado en las dependencias de la UdeG:"
    )

    add_table_title("Ficha técnica de requerimientos mínimos para estaciones de ventanilla en almacenes")
    t_hw = doc.add_table(rows=6, cols=3)
    t_hw.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_apa_table_borders(t_hw)

    headers_hw = ["Componente / Recurso", "Especificación Técnica Mínima", "Justificación Operativa / SLA"]
    for c_i, h in enumerate(headers_hw):
        cell = t_hw.rows[0].cells[c_i]
        cell.paragraphs[0].text = h
        cell.paragraphs[0].runs[0].font.bold = True
        cell.paragraphs[0].runs[0].font.size = Pt(9)
        cell.paragraphs[0].runs[0].font.color.rgb = COLOR_NAVY
        set_cell_margins(cell, 45, 45, 50, 50)

    rows_hw_data = [
        ("Procesador (CPU)", "Doble núcleo a 2.0 GHz (Intel Core i3 4ª gen / AMD Ryzen 3 o superior)", "Garantiza cifrado AES-256 local y hash SHA-256 en <50 milisegundos"),
        ("Memoria RAM", "4 GB de memoria RAM física (recomendado 8 GB)", "Suficiente para mantener el navegador y el Service Worker sin saturación"),
        ("Almacenamiento Local", "500 MB de espacio libre en disco (SSD o HDD)", "Capacidad para almacenar hasta 15,000 registros locales de inventario e historial"),
        ("Navegador Web", "Google Chrome v90+, Mozilla Firefox v88+ o Microsoft Edge v90+", "Soporte mandatorio de Service Workers, Cache Storage y Background Sync API"),
        ("Periféricos Ópticos", "Lector óptico de código de barras/QR USB (HID) o cámara web USB 720p", "Captura instantánea de credenciales y etiquetas en <1 segundo por escaneo")
    ]

    for r_i, r_data in enumerate(rows_hw_data, start=1):
        for c_i, val in enumerate(r_data):
            cell = t_hw.rows[r_i].cells[c_i]
            cell.paragraphs[0].text = val
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.runs[0].font.size = Pt(8.5)
            if c_i == 0:
                p.runs[0].font.bold = True
            set_cell_margins(cell, 35, 35, 45, 45)

    add_table_note("El 98% de las computadoras activas en los centros universitarios de la UdeG cumplen o superan estos requerimientos.")

    # =========================================================================
    # SECCIÓN 3: LISTA DE INSUMOS (BOM), CAPITAL HUMANO Y ORGANIGRAMA
    # =========================================================================
    add_heading_1("3. Lista de Insumos (BOM) por Unidad y por Lote")
    doc.add_paragraph(
        "Conforme a los lineamientos de la materia, la estructura de costos se modeló bajo dos dimensiones de análisis: "
        "(a) Costo Unitario por Dependencia (1 almacén o ventanilla central), y (b) Costo del Lote de Producción "
        "(100 dependencias universitarias activas concurrentes, representativo de la escala de la Red UdeG)."
    )

    add_heading_2("3.1. Materia Prima e Insumos Tecnológicos Directos")
    doc.add_paragraph(
        "Al tratarse de una solución nativa en la nube, la materia prima directa corresponde a los recursos de cómputo, "
        "bases de datos, almacenamiento de objetos y servicios de mensajería consumidos en Google Cloud Platform:"
    )

    add_table_title("Estructura de costos de materia prima / insumos TI mensuales (Lote 100 dependencias)")
    t_mp = doc.add_table(rows=6, cols=6)
    t_mp.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_apa_table_borders(t_mp)

    headers_mp = ["Insumo / Concepto", "Unidades", "C. Unitario (sin IVA)", "C. Total (+16% IVA)", "IVA Trasladado", "Mapeo a la Presentación"]
    for c_i, h in enumerate(headers_mp):
        cell = t_mp.rows[0].cells[c_i]
        cell.paragraphs[0].text = h
        cell.paragraphs[0].runs[0].font.bold = True
        cell.paragraphs[0].runs[0].font.size = Pt(9)
        cell.paragraphs[0].runs[0].font.color.rgb = COLOR_NAVY
        set_cell_margins(cell, 45, 45, 45, 45)

    rows_mp_data = [
        ("A (Instancias Cloud Run Compute)", "2 inst.", "$500.00", "$1,160.00", "$160.00", "Servidores Cloud Run ($12k/año)"),
        ("B (Base de Datos Cloud SQL)", "1 inst.", "$900.00", "$1,044.00", "$144.00", "Base de Datos SQL ($11k/año)"),
        ("C (Almacenamiento Cloud Storage)", "2 buckets", "$250.00", "$580.00", "$80.00", "Almacenamiento ($6k/año)"),
        ("D (API Mensajería Transaccional)", "1 servicio", "$266.67", "$309.33", "$42.67", "APIs y Notificaciones ($3k/año)"),
        ("TOTAL MATERIA PRIMA (LOTE 100)", "6 serv.", "$2,666.67", "$3,093.33", "$426.67", "Gasto Cloud Anualizado: $32,000.00 netos")
    ]

    for r_i, r_data in enumerate(rows_mp_data, start=1):
        for c_i, val in enumerate(r_data):
            cell = t_mp.rows[r_i].cells[c_i]
            cell.paragraphs[0].text = val
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT if c_i in (0, 5) else WD_ALIGN_PARAGRAPH.RIGHT
            if c_i == 1: p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.runs[0].font.size = Pt(8.5)
            if r_i == 5:
                p.runs[0].font.bold = True
                p.runs[0].font.color.rgb = COLOR_NAVY
            set_cell_margins(cell, 35, 35, 45, 45)

    add_table_note("El subtotal sin IVA mensual es de $2,666.67 MXN ($32,000.00 anuales). El IVA del 16% es de $426.67 MXN, totalizando $3,093.33 MXN mensuales.")

    add_heading_2("3.2. Mano de Obra Directa y Capital Humano")
    doc.add_paragraph(
        "El capital humano constituye el activo más crítico para la entrega del servicio SaaS. Para el lote de 100 dependencias, "
        "se dimensionó el personal técnico necesario para garantizar la operación continua, despliegues CI/CD y atención de incidencias:"
    )

    add_table_title("Estructura salarial mensual de mano de obra directa (Lote 100 dependencias)")
    t_mo = doc.add_table(rows=4, cols=6)
    t_mo.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_apa_table_borders(t_mo)

    headers_mo = ["Puesto / Rol Técnico", "Personal", "Sueldo Mensual", "Total Mensual", "% Total", "Responsabilidad Principal"]
    for c_i, h in enumerate(headers_mo):
        cell = t_mo.rows[0].cells[c_i]
        cell.paragraphs[0].text = h
        cell.paragraphs[0].runs[0].font.bold = True
        cell.paragraphs[0].runs[0].font.size = Pt(9)
        cell.paragraphs[0].runs[0].font.color.rgb = COLOR_NAVY
        set_cell_margins(cell, 45, 45, 45, 45)

    rows_mo_data = [
        ("Ingeniero DevOps / SysAdmin Cloud", "0.5 EJC", "$6,500.00", "$6,500.00", "60.0%", "Gestión de contenedores Cloud Run, seguridad y DRP"),
        ("Técnico QA / Soporte L2 a Planteles", "0.5 EJC", "$4,333.33", "$4,333.33", "40.0%", "Monitoreo de ventanillas y resolución de incidencias"),
        ("TOTAL MANO DE OBRA DIRECTA", "1.0 EJC", "$10,833.33", "$10,833.33", "100.0%", "Presupuesto anualizado de nómina técnica: $130,000.00")
    ]

    for r_i, r_data in enumerate(rows_mo_data, start=1):
        for c_i, val in enumerate(r_data):
            cell = t_mo.rows[r_i].cells[c_i]
            cell.paragraphs[0].text = val
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT if c_i in (0, 5) else WD_ALIGN_PARAGRAPH.RIGHT
            if c_i in (1, 4): p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.runs[0].font.size = Pt(8.5)
            if r_i == 3:
                p.runs[0].font.bold = True
                p.runs[0].font.color.rgb = COLOR_NAVY
            set_cell_margins(cell, 35, 35, 45, 45)

    add_table_note("EJC: Equivalente a Jornada Completa. En la fase inicial, los roles operan a medio tiempo compartido, escalando conforme al volumen.")

    add_heading_2("3.3. Evolución del Organigrama y Criterios Paramétricos de Escalamiento")
    doc.add_paragraph(
        "Para conciliar la disciplina de flujo de caja con el cumplimiento irrestricto de los Acuerdos de Nivel de Servicio (SLA), "
        "el dimensionamiento de personal no obedece a decisiones discrecionales, sino a métricas paramétricas de saturación:"
    )
    doc.add_paragraph(
        "• Fase 1 (Año 1 - Piloto CUTonalá, 5 dependencias): 2 personas (Lead DevOps / Backend Architect a medio tiempo + Encargado de QA / Soporte L2 a medio tiempo). "
        "Nómina anual de $126,000.00 MXN.\n"
        "• Fase 2 (Año 2 - Expansión CUCEI, 25 dependencias): 3 personas (Se incorpora 1 Técnico de Soporte N1 de tiempo completo). Nómina anual de $252,000.00 MXN.\n"
        "• Fase 3 (Año 3 - Consolidación Red UdeG, 100 dependencias): 5 personas (DevOps titular, Full-Stack Developer, Líder de QA y 2 Técnicos de Soporte N1 en turnos matutino y vespertino). "
        "Nómina anual de $540,000.00 MXN."
    )

    add_heading_3("3.3.1. Métricas de Saturación y Protocolo de Onboarding de Soporte N1")
    doc.add_paragraph(
        "La contratación del Técnico de Soporte N1 en la transición a la Fase 2 se activa de forma automática ante cualquiera de los siguientes disparadores paramétricos:\n"
        "1. Disparador de Volumen Comercial: Superar las 15 dependencias universitarias activas concurrentes.\n"
        "2. Disparador de Carga de Incidencias: Registrar más de 20 tickets semanales de soporte durante dos semanas consecutivas en la plataforma de Help Desk.\n"
        "3. Disparador de SLA: Cuando el tiempo medio de respuesta a incidencias de Nivel 2 supera los 25 minutos (acercándose al límite de tolerancia de 30 minutos).\n"
        "• Protocolo de Reclutamiento y Onboarding Anticipado: Dado que el umbral de disparo está previsto para el cruce de las 15 dependencias o 20 tickets semanales, "
        "se definió un tiempo de reclutamiento y capacitación previa de 3 semanas (21 días naturales). Se priorizará la captación de egresados de Ingeniería en Computación "
        "o prestadores de servicio social técnico de CUTonalá o CUCEI. El programa de inducción dura 10 días hábiles e incluye el estudio de la base de conocimientos interna "
        "de SIGRE, simulación de tickets en sandbox y acompañamiento en ventanilla, asegurando que el nuevo elemento esté plenamente productivo y certificado antes "
        "de que el volumen de incidencias comprometa el SLA de 15 minutos."
    )

    add_heading_3("3.3.2. Plan de Retención de Talento Clave y Mitigación de Fuga en Capital Humano")
    doc.add_paragraph(
        "Considerando que el capital humano absorbe el 59.3% de la estructura mensual de costos operativos, la rotación imprevista de roles técnicos "
        "críticos —como el Ingeniero DevOps y el Lead Full-Stack Architect— representaría un riesgo mayúsculo para la continuidad operativa y el cumplimiento "
        "del SLA del 99.5%. Para blindar la estabilidad organizacional sin comprometer el flujo de caja, se diseñó un paquete integral de retención e incentivos:"
    )
    doc.add_paragraph(
        "• Bono Anual por Cumplimiento de SLA y Retención: Se asigna una gratificación anual de $12,000.00 MXN ($6,000.00 MXN semestrales) por cada rol técnico "
        "clave, vinculada al mantenimiento de una disponibilidad de infraestructura superior al 99.5% y una resolución de incidentes críticos en menos de 15 minutos.\n"
        "• Esquema de Equity Vesting (Participación Accionaria Gradual): Se reserva un paquete del 10.0% del capital social de SIGRE destinado al personal "
        "técnico fundador, sujeto a un periodo de carencia (cliff) de 12 meses y una liberación escalonada a los 24 y 36 meses de permanencia continua en el proyecto, "
        "alineando los incentivos de permanencia con la valorización patrimonial de la empresa.\n"
        "• Presupuesto de Formación y Certificación Continua: Se dota una bolsa anual de $4,000.00 MXN por especialista técnico para financiar los derechos de examen "
        "y preparación de certificaciones oficiales en Google Cloud Platform (Associate Cloud Engineer y Professional DevOps Engineer), garantizando la actualización "
        "permanente del talento interno frente a la rápida evolución de la nube."
    )

    add_heading_2("3.4. Servicios de Operación y Cumplimiento Legal")
    doc.add_paragraph(
        "Se incluyen servicios de soporte operacional (conectividad de alta velocidad, traslados a planteles para pruebas en sitio, "
        "material de capacitación) por $2,500.00 MXN mensuales ($30,000.00 anuales), y los costos de cumplimiento normativo amortizados "
        "(depósito de derechos de autor de software ante INDAUTOR y dictamen de Aviso de Privacidad LGPDPPSO) "
        "por $1,833.33 MXN mensuales ($22,000.00 anuales)."
    )

    # =========================================================================
    # SECCIÓN 4: COSTO UNITARIO, PRECIOS Y ECONOMÍAS DE ESCALA
    # =========================================================================
    add_heading_1("4. Estimación del Costo Unitario, Modelo de Precios y Economías de Escala")
    doc.add_paragraph(
        "Conforme a los postulados de contabilidad gerencial (Horngren et al., 2012), la estructura de costos mensuales "
        "para el lote de 100 dependencias universitarias se consolida en la siguiente integración:"
    )

    add_table_title("Consolidación del costo total mensual del lote de 100 dependencias")
    t_tot = doc.add_table(rows=6, cols=4)
    t_tot.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_apa_table_borders(t_tot)

    headers_tot = ["Categoría de Costo", "Monto Mensual", "% del Total", "Naturaleza Contable"]
    for c_i, h in enumerate(headers_tot):
        cell = t_tot.rows[0].cells[c_i]
        cell.paragraphs[0].text = h
        cell.paragraphs[0].runs[0].font.bold = True
        cell.paragraphs[0].runs[0].font.size = Pt(9.5)
        cell.paragraphs[0].runs[0].font.color.rgb = COLOR_NAVY
        set_cell_margins(cell, 45, 45, 55, 55)

    rows_tot_data = [
        ("Capital Humano Directo (DevOps + QA/Soporte)", "$10,833.33", "59.3%", "Costo Fijo"),
        ("Insumos de Tecnología TI (Servidores GCP con IVA)", "$3,093.33", "16.9%", "Costo Variable Escalonado"),
        ("Servicios de Operación y Traslados", "$2,500.00", "13.7%", "Costo Fijo"),
        ("Cumplimiento Normativo (LGPDPPSO / INDAUTOR)", "$1,833.33", "10.0%", "Costo Fijo Amortizado"),
        ("TOTAL COSTO MENSUAL DEL LOTE (100 UNIDADES)", "$18,260.00", "100.0%", "Costo Total de Operación")
    ]

    for r_i, r_data in enumerate(rows_tot_data, start=1):
        for c_i, val in enumerate(r_data):
            cell = t_tot.rows[r_i].cells[c_i]
            cell.paragraphs[0].text = val
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT if c_i == 0 else WD_ALIGN_PARAGRAPH.RIGHT
            if c_i == 2: p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.runs[0].font.size = Pt(9)
            if r_i == 5:
                p.runs[0].font.bold = True
                p.runs[0].font.color.rgb = COLOR_NAVY
            set_cell_margins(cell, 40, 40, 50, 50)

    add_table_note("El costo total anual asciende a $219,120.00 MXN. Costo unitario medio por dependencia: $182.60 MXN mensuales.")

    add_heading_2("4.1. Determinación del Precio de Venta Institucional")
    doc.add_paragraph(
        "Para fijar el precio de venta institucional se empleó la metodología de margen sobre costos (BBVA, 2021; Hansen y Mowen, 2007), "
        "aplicando un markup de 2.5x sobre el costo unitario de producción mensual ($182.60 MXN), lo que establece un precio base "
        "de $456.50 MXN mensuales sin IVA (margen operativo del 60.0%). Incorporando el 16% de IVA ($73.04 MXN), el precio final al público "
        "se sitúa en $529.54 MXN mensuales por dependencia."
    )
    doc.add_paragraph(
        "En el esquema de contratación anualizada por centro universitario, la licencia anual de SIGRE se fija en $28,950.00 MXN netos "
        "por dependencia o almacén central. Esta cifra posee una ventaja estratégica fundamental: se ubica holgadamente por debajo "
        "del umbral de compras menores del Artículo 55 de la Ley de Compras Gubernamentales del Estado de Jalisco, posibilitando que directores "
        "de división y coordinadores de laboratorio contraten la plataforma de forma ágil mediante adjudicación directa, sin requerir licitaciones públicas."
    )

    add_heading_2("4.2. Economías de Escala y Punto de Equilibrio Operativo")
    doc.add_paragraph(
        "En las plataformas SaaS, los costos variables de infraestructura crecen marginalmente mientras los costos fijos (ingeniería y soporte) "
        "se distribuyen entre un mayor número de dependencias contratadas. Aplicando la formulación canónica de punto de equilibrio (Baca Urbina, 2013):"
    )
    doc.add_paragraph(
        "• Costos Fijos Totales Mensuales (CF): $10,833.33 (Mano de obra) + $2,500.00 (Servicios) + $1,833.33 (Legal) = $15,166.67 MXN\n"
        "• Costo Variable Unitario (CVU): $26.67 MXN por dependencia al mes en infraestructura Cloud Run y almacenamiento\n"
        "• Margen de Contribución Unitario (MCU): P - CVU = $456.50 - $26.67 = $429.83 MXN por dependencia\n"
        "• Razón de Margen de Contribución: 94.16%\n"
        "• PUNTO DE EQUILIBRIO EN UNIDADES (Q_PE = CF / MCU): $15,166.67 / $429.83 = 35.28 ≈ 35 dependencias contratadas\n"
        "• PUNTO DE EQUILIBRIO EN VENTAS ($): 35 dependencias × $456.50 = $16,107.45 MXN mensuales ($18,684.64 MXN con IVA)."
    )

    # Inserción de Figura 1 (Economías de Escala)
    add_figure_caption("Figura 1", "Curva de economías de escala y determinación del punto de equilibrio operativo de SIGRE")
    fig1_path = os.path.join("docs", "graficos", "figura3_curva_economias_escala_punto_equilibrio.png")
    if os.path.exists(fig1_path):
        p_img1 = doc.add_paragraph()
        p_img1.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_img1 = p_img1.add_run()
        r_img1.add_picture(fig1_path, width=Inches(6.4))
    add_figure_note(
        "Panel izquierdo: Costo unitario decreciente en función del volumen. "
        "Panel derecho: Cruce de ingresos y costos totales en Q = 35 dependencias ($16,107 MXN), delimitando las zonas de déficit y utilidad."
    )

    # =========================================================================
    # SECCIÓN 5: ESTADOS FINANCIEROS PRO FORMA Y FLUJO DE EFECTIVO
    # =========================================================================
    add_heading_1("5. Estados Financieros Pro Forma, Flujo de Efectivo y Análisis de Sensibilidad")
    doc.add_paragraph(
        "Para evaluar la viabilidad contable y la liquidez operativa en un horizonte temporal de maduración institucional, "
        "se elaboraron el Estado de Resultados Proyectado pro forma a 3 años y el Flujo de Efectivo Mensual (Cash Flow) "
        "para el Año 1, modelando la zona de déficit pre-operativo y la absorción de capital semilla."
    )

    add_heading_2("5.1. Estado de Resultados Proyectado Pro Forma (Horizonte a 3 Años)")
    doc.add_paragraph(
        "El modelo proyecta tres fases de adopción escalonada: Año 1 (Piloto en CUTonalá con 5 dependencias contratadas), "
        "Año 2 (Expansión hacia CUCEI y dependencias clave alcanzando 25 dependencias) y Año 3 (Consolidación en la Red UdeG "
        "con 100 dependencias contratadas). Los ingresos corresponden a la licencia anual de $28,950.00 MXN netos por dependencia:"
    )

    add_heading_3("5.1.1. Política de Indexación Inflacionaria (INPC) y Protección de Márgenes")
    doc.add_paragraph(
        "Para neutralizar la inflación proyectada en la economía nacional (estimada en un 4.5% a 5.0% anual según el Banco de México) "
        "y prevenir la erosión de los márgenes por incrementos en sueldos de ingeniería y servicios de red, los contratos anuales de SIGRE "
        "incorporan una cláusula de indexación automática vinculada al Índice Nacional de Precios al Consumidor (INPC) publicado por el INEGI. "
        "A partir del Año 2, la tarifa base de $28,950.00 MXN se actualiza conforme a dicho índice. De forma correlativa, las partidas de nómina "
        "técnica y servidores GCP contemplan un ajuste inflacionario del 5.0% anual en el modelo financiero, demostrando que los ingresos "
        "escalan a la par de la estructura de costos y salvaguardando un margen neto consolidado por encima del 50.0% en régimen de escala."
    )

    add_heading_3("5.1.2. Creación del Fondo de Reserva para Reinversión Tecnológica y Refactorización")
    doc.add_paragraph(
        "Para responder a los rápidos ciclos de obsolescencia tecnológica en el desarrollo web y los servicios de nube, así como para garantizar recursos "
        "recurrentes para refactorizaciones de microservicios, migraciones de librerías y auditorías anuales de seguridad sin requerir nuevas aportaciones de capital, "
        "se establece una política contable estatutaria: a partir del Año 2 (cuando el volumen contratado alcanza 25 dependencias y genera un margen bruto "
        "de $693,150.00 MXN), se retiene el 5.0% de la Utilidad Bruta anual para constituir el Fondo de Reserva de Reinversión Tecnológica. "
        "Esta partida representa $34,657.50 MXN en el Año 2 y escala a $138,630.00 MXN en el Año 3 (sobre una Utilidad Bruta de $2,772,600.00 MXN). "
        "El fondo se resguarda en una subcuenta de tesorería etiquetada exclusivamente para la optimización de código, licenciamiento de herramientas CI/CD "
        "y modernización de infraestructura, garantizando la vanguardia técnica del sistema con recursos generados orgánicamente."
    )

    add_table_title("Estado de Resultados Proyectado Pro Forma — Horizonte a 3 Años (Cifras en MXN)")
    t_er = doc.add_table(rows=17, cols=5)
    t_er.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_apa_table_borders(t_er)

    headers_er = ["Concepto Contable / Financiero", "Año 1 (Piloto - 5 deps)", "Año 2 (Expansión - 25 deps)", "Año 3 (Consolidación - 100 deps)", "Criterio Técnico"]
    for c_i, h in enumerate(headers_er):
        cell = t_er.rows[0].cells[c_i]
        cell.paragraphs[0].text = h
        cell.paragraphs[0].runs[0].font.bold = True
        cell.paragraphs[0].runs[0].font.size = Pt(8.5)
        cell.paragraphs[0].runs[0].font.color.rgb = COLOR_NAVY
        set_cell_margins(cell, 45, 45, 45, 45)

    rows_er_data = [
        ("Dependencias Contratadas", "5", "25", "100", "Almacenes y laboratorios"),
        ("Tarifa Anual por Dependencia (sin IVA)", "$28,950.00", "$28,950.00", "$28,950.00", "Contratación directa anual fija"),
        ("INGRESOS BRUTOS OPERACIONALES", "$144,750.00", "$723,750.00", "$2,895,000.00", "Facturación por servicios SaaS"),
        ("Costo del Servicio Cloud GCP (Variable)", "$6,120.00", "$30,600.00", "$122,400.00", "Consumo escalonado en la nube"),
        ("UTILIDAD BRUTA", "$138,630.00", "$693,150.00", "$2,772,600.00", "Margen de contribución total"),
        ("Margen Bruto (%)", "95.8%", "95.8%", "95.8%", "Economía digital SaaS"),
        ("Gastos de Operación: Nómina y Soporte", "$126,000.00", "$252,000.00", "$540,000.00", "Evolución organigrama: 2 a 5 personas"),
        ("Gastos de Operación: Conectividad y Licencias", "$18,000.00", "$36,000.00", "$72,000.00", "Herramientas de monitoreo y soporte"),
        ("Gastos de Operación: Talleres y Viáticos", "$8,500.00", "$22,000.00", "$45,000.00", "Capacitación presencial en campus"),
        ("Gastos de Operación: Legal e INDAUTOR", "$5,500.00", "$12,000.00", "$25,000.00", "Trámites regulatorios y compliance"),
        ("TOTAL GASTOS DE OPERACIÓN (OPEX)", "$158,000.00", "$322,000.00", "$682,000.00", "Gastos operacionales y talento"),
        ("UTILIDAD DE OPERACIÓN / EBITDA", "-$19,370.00", "$371,150.00", "$2,090,600.00", "Resultado operacional"),
        ("Impuesto Sobre la Renta (ISR Estimado 30%)", "$0.00", "$111,345.00", "$627,180.00", "Tasa corporativa estándar SAT"),
        ("UTILIDAD (PÉRDIDA) NETA DEL EJERCICIO", "-$19,370.00", "$259,805.00", "$1,463,420.00", "Resultado neto contable"),
        ("(-) Reserva Reinversión Tecnológica (5% U.B.)", "$0.00", "$34,657.50", "$138,630.00", "Provisión estatutaria de código"),
        ("UTILIDAD NETA RETENIDA / DISTRIBUIBLE", "-$19,370.00", "$225,147.50", "$1,324,790.00", "Excedente financiero neto libre")
    ]

    for r_i, r_data in enumerate(rows_er_data, start=1):
        for c_i, val in enumerate(r_data):
            cell = t_er.rows[r_i].cells[c_i]
            cell.paragraphs[0].text = val
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT if c_i in (0, 4) else WD_ALIGN_PARAGRAPH.RIGHT
            if c_i in (1, 2, 3) and r_i in (1, 6): p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.runs[0].font.size = Pt(8.5)
            if r_i in (3, 5, 11, 12, 14, 16):
                p.runs[0].font.bold = True
                p.runs[0].font.color.rgb = COLOR_NAVY
            set_cell_margins(cell, 35, 35, 45, 45)

    add_table_note("En el Año 1, el déficit operativo de -$19,370 MXN es cubierto por el capital semilla. A partir del Año 2 se descuenta el 5% de reserva tecnológica.")

    add_heading_2("5.2. Flujo de Efectivo Mensual Pro Forma (Cash Flow Año 1) y Análisis de Burn Rate")
    doc.add_paragraph(
        "El Flujo de Efectivo pro forma del Año 1 proyecta mes a mes la tesorería del proyecto, modelando el requerimiento "
        "de capital de trabajo de $120,000.00 MXN aportado en el Mes 1 para financiar la fase de desarrollo y certificación del software:"
    )

    add_table_title("Presupuesto de Flujo de Efectivo Mensual Pro Forma (Cash Flow) — Año 1 Piloto (Cifras en MXN)")
    t_cf = doc.add_table(rows=8, cols=14)
    t_cf.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_apa_table_borders(t_cf)

    headers_cf = ["Concepto de Tesorería", "M1", "M2", "M3", "M4", "M5", "M6", "M7", "M8", "M9", "M10", "M11", "M12", "Total A1"]
    for c_i, h in enumerate(headers_cf):
        cell = t_cf.rows[0].cells[c_i]
        cell.paragraphs[0].text = h
        cell.paragraphs[0].runs[0].font.bold = True
        cell.paragraphs[0].runs[0].font.size = Pt(7.5)
        cell.paragraphs[0].runs[0].font.color.rgb = COLOR_NAVY
        set_cell_margins(cell, 40, 40, 30, 30)

    rows_cf_data = [
        ("Saldo Inicial en Caja", "$0", "$108k", "$96k", "$83k", "$71k", "$59k", "$44k", "$198k", "$185k", "$174k", "$163k", "$152k", "$0"),
        ("Capital Semilla Inicial", "$120k", "$0", "$0", "$0", "$0", "$0", "$0", "$0", "$0", "$0", "$0", "$0", "$120,000"),
        ("Cobranza Piloto (5 deps + IVA)", "$0", "$0", "$0", "$0", "$0", "$0", "$168k", "$0", "$0", "$0", "$0", "$0", "$167,910"),
        ("Total Entradas de Efectivo", "$120k", "$0", "$0", "$0", "$0", "$0", "$168k", "$0", "$0", "$0", "$0", "$0", "$287,910"),
        ("Total Salidas Operativas", "$12k", "$12k", "$12.5k", "$12.5k", "$12k", "$14.5k", "$14k", "$13.5k", "$11k", "$11k", "$11k", "$15.5k", "$151,560"),
        ("FLUJO NETO DEL MES", "+$108k", "-$12k", "-$12.5k", "-$12.5k", "-$12k", "-$14.5k", "+$154k", "-$13.5k", "-$11k", "-$11k", "-$11k", "-$15.5k", "+$136,350"),
        ("SALDO FINAL EN CAJA", "$108k", "$96k", "$83.5k", "$71k", "$59k", "$44.5k", "$198k", "$185k", "$174k", "$163k", "$152k", "$136k", "$136,380")
    ]

    for r_i, r_data in enumerate(rows_cf_data, start=1):
        for c_i, val in enumerate(r_data):
            cell = t_cf.rows[r_i].cells[c_i]
            cell.paragraphs[0].text = val
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT if c_i == 0 else WD_ALIGN_PARAGRAPH.RIGHT
            p.runs[0].font.size = Pt(7.5)
            if r_i in (4, 6, 7):
                p.runs[0].font.bold = True
                p.runs[0].font.color.rgb = COLOR_NAVY
            set_cell_margins(cell, 30, 30, 25, 25)

    add_table_note("Cifras resumidas en miles de pesos (k). Cobranza del piloto en Mes 7: $144,750 MXN netos + $23,160 MXN de IVA = $167,910 MXN.")

    doc.add_paragraph(
        "Indicadores Clave de Tesorería del Año 1:\n"
        "• Tasa de Quema de Efectivo Promedio (Burn Rate Pre-operativo M1-M6): $12,583.33 MXN mensuales de gasto operacional neto antes de cobranzas.\n"
        "• Punto Mínimo de Tesorería en Caja (Mes 6): $44,500.00 MXN, alcanzado tras cubrir el trámite de registro ante INDAUTOR. "
        "Esto demuestra la existencia de un colchón de seguridad del 37.1% del capital inicial, eliminando cualquier riesgo de iliquidez.\n"
        "• Requerimiento de Capital de Trabajo: Con una aportación de $120,000.00 MXN se absorbe holgadamente el déficit de desarrollo previo a la facturación.\n"
        "• Superávit de Cierre al Año 1: $136,380.00 MXN en caja libre de gravamen, recursos que financiarán la fase de expansión en CUCEI sin deuda externa."
    )

    add_heading_2("5.3. Ventas, Ganancia e IVA por Volumen de Dependencias")
    doc.add_paragraph(
        "A continuación se ilustra la escala tributaria y el comportamiento del IVA frente al Servicio de Administración Tributaria (SAT):"
    )

    add_table_title("Proyección de ventas, utilidad y balance fiscal de IVA por volumen mensual")
    t_v = doc.add_table(rows=7, cols=5)
    t_v.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_apa_table_borders(t_v)

    headers_v = ["Ventas (Unidades)", "Ingresos con IVA", "Costo Asociado", "Ganancia Bruta", "IVA Trasladado"]
    for c_i, h in enumerate(headers_v):
        cell = t_v.rows[0].cells[c_i]
        cell.paragraphs[0].text = h
        cell.paragraphs[0].runs[0].font.bold = True
        cell.paragraphs[0].runs[0].font.size = Pt(9.5)
        cell.paragraphs[0].runs[0].font.color.rgb = COLOR_NAVY
        set_cell_margins(cell, 45, 45, 55, 55)

    rows_v_data = [
        ("1 dependencia", "$529.54", "$182.60", "$346.94", "$73.04"),
        ("10 dependencias", "$5,295.40", "$1,826.00", "$3,469.40", "$730.40"),
        ("20 dependencias", "$10,590.80", "$3,652.00", "$6,938.80", "$1,460.80"),
        ("50 dependencias", "$26,477.00", "$9,130.00", "$17,347.00", "$3,652.00"),
        ("75 dependencias", "$39,715.50", "$13,695.00", "$26,020.50", "$5,478.00"),
        ("100 dependencias", "$52,954.00", "$18,260.00", "$34,694.00", "$7,304.00")
    ]

    for r_i, r_data in enumerate(rows_v_data, start=1):
        for c_i, val in enumerate(r_data):
            cell = t_v.rows[r_i].cells[c_i]
            cell.paragraphs[0].text = val
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT if c_i == 0 else WD_ALIGN_PARAGRAPH.RIGHT
            p.runs[0].font.size = Pt(9)
            if r_i == 6:
                p.runs[0].font.bold = True
                p.runs[0].font.color.rgb = COLOR_NAVY
            set_cell_margins(cell, 40, 40, 50, 50)

    add_table_note("Alcanzado el lote de 100 dependencias, el IVA a enterar al SAT asciende a $6,877.33 MXN y la ganancia neta libre mensual a $27,390.00 MXN.")

    add_heading_2("5.4. Análisis de Sensibilidad Financiera y Resistencia de Tesorería ante Escenarios de Estrés")
    doc.add_paragraph(
        "Para someter a prueba la solidez financiera de la propuesta ante contingencias externas, se modelaron dos escenarios "
        "de estrés financiero frente al Escenario Base: (a) un incremento del 15% en los costos de infraestructura Cloud (GCP) "
        "derivado de una devaluación del peso frente al dólar (USD/MXN), y (b) un retraso administrativo severo de 4 meses "
        "en la formalización y cobranza de los contratos universitarios, posponiendo el cobro del Mes 7 al Mes 11:"
    )

    add_table_title("Matriz de análisis de sensibilidad financiera y estrés de tesorería (Año 1)")
    t_sens = doc.add_table(rows=12, cols=5)
    t_sens.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_apa_table_borders(t_sens)

    headers_sens = ["Parámetro Financiero / Métrica", "Escenario Base", "Pesimista Cambiario (+15% GCP)", "Pesimista Comercial (Retraso 4m)", "Diagnóstico de Resiliencia"]
    for c_i, h in enumerate(headers_sens):
        cell = t_sens.rows[0].cells[c_i]
        cell.paragraphs[0].text = h
        cell.paragraphs[0].runs[0].font.bold = True
        cell.paragraphs[0].runs[0].font.size = Pt(8.5)
        cell.paragraphs[0].runs[0].font.color.rgb = COLOR_NAVY
        set_cell_margins(cell, 45, 45, 45, 45)

    rows_sens_data = [
        ("Dependencias Contratadas Año 1", "5 dependencias", "5 dependencias", "5 dependencias", "Mismo alcance piloto CUTonalá"),
        ("Mes de Cobranza de Contratos", "Mes 7 (Arranque)", "Mes 7 (Arranque)", "Mes 11 (Retraso burocrático)", "Estrés de morosidad administrativa"),
        ("Ingresos Totales con IVA Año 1", "$167,910.00", "$167,910.00", "$167,910.00", "Cobranza total íntegra del contrato"),
        ("Costo Anual Infraestructura GCP", "$6,120.00", "$7,038.00", "$6,120.00", "+$918 MXN al año por tipo de cambio"),
        ("Margen Bruto de Servicio (%)", "95.8%", "95.1%", "95.8%", "Impacto irrelevante en rentabilidad"),
        ("Gastos Operativos Fijos Totales", "$145,440.00", "$145,440.00", "$145,440.00", "Nóminas técnicas y trámites legales"),
        ("Total Egresos Operativos Año 1", "$151,560.00", "$152,478.00", "$151,560.00", "Incremento neto anual de solo $918 MXN"),
        ("Tasa de Quema (Burn Rate Pre-op)", "$12,583.33 / mes", "$12,660.00 / mes", "$12,583.33 / mes", "Gasto mensual neto controlado"),
        ("PUNTO MÍNIMO DE TESORERÍA EN CAJA", "$44,500.00 (Mes 6)", "$43,962.00 (Mes 6)", "$7,470.00 (Mes 10)", "Caja SIEMPRE positiva: resiste 4 meses de mora"),
        ("Colchón Mínimo de Seguridad (%)", "37.1%", "36.6%", "6.2%", "Capital de trabajo absorbe retraso de firmas"),
        ("SUPERÁVIT DE CAJA AL CIERRE DE AÑO 1", "$136,380.00", "$135,462.00", "$136,380.00", "Solvencia total garantizada para CUCEI")
    ]

    for r_i, r_data in enumerate(rows_sens_data, start=1):
        for c_i, val in enumerate(r_data):
            cell = t_sens.rows[r_i].cells[c_i]
            cell.paragraphs[0].text = val
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT if c_i == 0 else WD_ALIGN_PARAGRAPH.CENTER
            p.runs[0].font.size = Pt(8.5)
            if r_i in (9, 11):
                p.runs[0].font.bold = True
                p.runs[0].font.color.rgb = COLOR_NAVY
            set_cell_margins(cell, 35, 35, 40, 40)

    add_table_note("El capital semilla de $120,000 MXN absorbe de manera autónoma hasta 4 meses consecutivos de retraso en la cobranza institucional sin incurrir en deuda.")

    # =========================================================================
    # SECCIÓN 6: RELEVANCIA DE CRITERIOS DE COSTO — DIAGRAMA DE PARETO
    # =========================================================================
    add_heading_1("6. Relevancia de los Criterios de Costo — Diagrama de Pareto")
    doc.add_paragraph(
        "Para evaluar la criticidad y ponderación operativa de cada partida de gasto, se estructuró un análisis "
        "multicriterio conforme a la regla del 80/20 de Pareto:"
    )

    add_table_title("Partidas de costo y su relevancia operativa bajo análisis ABC")
    t_crit = doc.add_table(rows=5, cols=6)
    t_crit.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_apa_table_borders(t_crit)

    headers_crit = ["Partida de Costo", "Monto Mensual", "% Total", "% Acum.", "Disponibilidad / Criticidad", "Sensibilidad al Volumen"]
    for c_i, h in enumerate(headers_crit):
        cell = t_crit.rows[0].cells[c_i]
        cell.paragraphs[0].text = h
        cell.paragraphs[0].runs[0].font.bold = True
        cell.paragraphs[0].runs[0].font.size = Pt(9)
        cell.paragraphs[0].runs[0].font.color.rgb = COLOR_NAVY
        set_cell_margins(cell, 45, 45, 45, 45)

    rows_crit_data = [
        ("Capital Humano Directo", "$10,833.33", "59.3%", "59.3%", "Talento especializado / Criticidad máxima", "Baja (Costo fijo mensual)"),
        ("Insumos Cloud / TI (GCP)", "$3,093.33", "16.9%", "76.3%", "Inmediata SLA 99.9% / Vital 24/7", "Alta (Escala con tráfico)"),
        ("Servicios Operativos", "$2,500.00", "13.7%", "90.0%", "Alta disponibilidad de enlaces y traslados", "Baja (Gasto base técnico)"),
        ("Cumplimiento Normativo (LGPDPPSO/INDAUTOR)", "$1,833.33", "10.0%", "100.0%", "Certeza jurídica / Privacidad de datos", "Nula (Amortización fija)")
    ]

    for r_i, r_data in enumerate(rows_crit_data, start=1):
        for c_i, val in enumerate(r_data):
            cell = t_crit.rows[r_i].cells[c_i]
            cell.paragraphs[0].text = val
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT if c_i in (0, 4, 5) else WD_ALIGN_PARAGRAPH.RIGHT
            if c_i in (2, 3): p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.runs[0].font.size = Pt(8.5)
            if r_i <= 2:
                p.runs[0].font.bold = True
            set_cell_margins(cell, 40, 40, 45, 45)

    add_table_note("El 76.3% del costo total se concentra en Capital Humano y Servicios Cloud (Zona A de Pareto, alcanzando el 90.0% con Servicios).")

    # Inserción de Figura 2 (Pareto)
    add_figure_caption("Figura 2", "Diagrama de Pareto de la estructura de costos de producción de SIGRE (Lote 100 dependencias)")
    fig2_path = os.path.join("docs", "graficos", "figura2_grafico_pareto_criterios_costo.png")
    if os.path.exists(fig2_path):
        p_img2 = doc.add_paragraph()
        p_img2.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_img2 = p_img2.add_run()
        r_img2.add_picture(fig2_path, width=Inches(6.4))
    add_figure_note(
        "Distribución acumulada de costos mensuales. El talento de ingeniería y la nube representan las decisiones críticas "
        "para la viabilidad técnica y operativa de la plataforma."
    )

    # =========================================================================
    # SECCIÓN 7: PROGRAMACIÓN DE ACTIVIDADES E INVERSIONES (GANTT AÑO 1)
    # =========================================================================
    add_heading_1("7. Programación de Actividades, Inversiones y Cronograma de Ejecución (Año 1)")
    doc.add_paragraph(
        "La ejecución del Año 1 se estructuró en hitos críticos mensuales para asegurar la absorción ordenada "
        "del capital semilla de $120,000.00 MXN. Para mitigar contingencias administrativas en el sector público, "
        "la ruta crítica incorpora holguras estratégicas (*buffers*), prerrequisitos técnicos y un hito formal de cierre administrativo:"
    )
    doc.add_paragraph(
        "• Buffer A (Holgura Legal INDAUTOR): En el Hito 4 (Mes 6) se contemplan 3 semanas de holgura para absorber cualquier "
        "prevención documental o retraso en las oficinas del Registro Público del Derecho de Autor, asegurando que el certificado "
        "esté en firme antes del encendido del piloto.\n"
        "• Prerrequisito Técnico de Ciberseguridad (Mes 6): Previo al despliegue, se ejecuta la prueba de penetración ética (pentesting OWASP Top 10) "
        "y auditoría estática SAST/DAST, obteniendo el dictamen de no vulnerabilidad exigido por la LGPDPPSO.\n"
        "• Sub-Hito de Socialización y Visto Bueno Sindical (Mes 6): Firma de la minuta de concertación con los delegados del SUTUdeG en CUTonalá, "
        "garantizando el aval gremial y la protección patrimonial del trabajador antes de habilitar terminales en ventanilla.\n"
        "• Buffer B (Holgura de Calendario Universitario): En los Hitos 6 y 7 (Meses 8 y 9) se contemplan 2 semanas de colchón "
        "operativo para amortiguar periodos de exámenes departamentales o recesos intersemestrales de la Red UdeG sin desfasar la marcha blanca.\n"
        "• Hito Formal de Cierre y Aprobación de Marcha Blanca (Mes 9): Al finalizar el Mes 9, se formaliza la firma del Acta Oficial de Entrega-Recepción "
        "y Dictamen de Satisfacción de Marcha Blanca, suscrita por los Coordinadores de Carrera, Jefes de Laboratorio y la Dirección de la División de Ingenierías "
        "de CUTonalá. Este acto administrativo constituye el requisito institucional indispensable que avala formalmente el paso a la Fase 2 de expansión hacia CUCEI."
    )

    add_table_title("Cronograma detallado de ejecución (Diagrama de Gantt) y absorción de inversión — Año 1")
    t_gantt = doc.add_table(rows=10, cols=15)
    t_gantt.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_apa_table_borders(t_gantt)

    headers_gantt = ["Fase / Hito Crítico", "Líder", "M1", "M2", "M3", "M4", "M5", "M6", "M7", "M8", "M9", "M10", "M11", "M12", "Presupuesto"]
    for c_i, h in enumerate(headers_gantt):
        cell = t_gantt.rows[0].cells[c_i]
        cell.paragraphs[0].text = h
        cell.paragraphs[0].runs[0].font.bold = True
        cell.paragraphs[0].runs[0].font.size = Pt(7.5)
        cell.paragraphs[0].runs[0].font.color.rgb = COLOR_NAVY
        set_cell_margins(cell, 40, 40, 25, 25)

    rows_gantt_data = [
        ("1. Arquitectura Cloud GCP y Microservicios Base", "DevOps", "●", "●", "", "", "", "", "", "", "", "", "", "", "$24,000.00"),
        ("2. Motor de Scoring y PWA Offline", "Full-Stack", "", "", "●", "●", "", "", "", "", "", "", "", "", "$25,000.00"),
        ("3. Pruebas QA, Estrés k6, Pentesting OWASP y LGPDPPSO", "QA", "", "", "", "", "●", "●", "", "", "", "", "", "", "$12,000.00"),
        ("4. Registro INDAUTOR (Buffer 3s) y V.B. Sindical SUTUdeG", "Jurídico/PM", "", "", "", "", "", "●", "", "", "", "", "", "", "$5,500.00"),
        ("5. Despliegue Piloto en CUTonalá (Laboratorios)", "DevOps", "", "", "", "", "", "", "●", "", "", "", "", "", "$11,500.00"),
        ("6. Capacitación a Almacenistas y Talleres", "Success", "", "", "", "", "", "", "", "●", "●", "", "", "", "$10,000.00"),
        ("7. Marcha Blanca, KPIs y Acta Entrega-Recepción M9", "Soporte", "", "", "", "", "", "", "", "", "●", "●", "●", "", "$16,500.00"),
        ("8. Evaluación de Impacto y Release v1.5 CUCEI", "Equipo", "", "", "", "", "", "", "", "", "", "", "", "●", "$15,500.00"),
        ("TOTAL INVERSIÓN EJECUTADA AÑO 1", "—", "$12k", "$12k", "$12.5k", "$12.5k", "$12k", "$5.5k", "$11.5k", "$5k", "$10.5k", "$5.5k", "$5.5k", "$15.5k", "$120,000.00")
    ]

    for r_i, r_data in enumerate(rows_gantt_data, start=1):
        for c_i, val in enumerate(r_data):
            cell = t_gantt.rows[r_i].cells[c_i]
            cell.paragraphs[0].text = val
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT if c_i in (0, 1) else WD_ALIGN_PARAGRAPH.CENTER
            if c_i == 14: p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            p.runs[0].font.size = Pt(7.5)
            if r_i == 9:
                p.runs[0].font.bold = True
                p.runs[0].font.color.rgb = COLOR_NAVY
            set_cell_margins(cell, 30, 30, 25, 25)

    add_table_note("El hito del Mes 6 integra el depósito ante INDAUTOR, el pentesting de seguridad y la concertación sindical con el SUTUdeG.")

    # =========================================================================
    # SECCIÓN 8: CONCLUSIONES Y VIABILIDAD INTEGRAL
    # =========================================================================
    add_heading_1("8. Conclusiones y Viabilidad Integral del Proyecto")
    doc.add_paragraph(
        "El presente estudio demuestra la sólida viabilidad técnica, operativa, normativa y financiera de la plataforma SIGRE. "
        "Desde la perspectiva operativa y académica, la sustitución del vale de papel mitiga una fuga de más de $750,000.00 MXN anuales por plantel "
        "en horas-hombre y mermas patrimoniales (obtenidas mediante levantamiento de campo directo en CUTonalá), reduciendo la tasa de prácticas "
        "afectadas (TPSR) del 14.5% a menos del 1.5% semestral y protegiendo las acreditaciones de calidad CACEI/CONAET, lo que genera para el centro universitario "
        "un retorno de inversión social del 2,283% frente a una tarifa de adopción de solo $28,950.00 MXN anuales."
    )
    doc.add_paragraph(
        "Desde el ángulo de mercado y comercialización, SIGRE consolida ventajas competitivas irrefutables: un algoritmo de scoring "
        "predictivo que disciplina el préstamo, cumplimiento nativo con la legislación de datos personales en Jalisco (LGPDPPSO) validado con pentesting "
        "OWASP Top 10, un Costo de Adquisición de Clientes (CAC) de $5,000 MXN con un ratio LTV/CAC altamente rentable de 17.37x, una estrategia de gestión "
        "del cambio con concertación sindical formal (SUTUdeG) y un esquema tarifario adaptado al régimen de adjudicación directa universitaria (Art. 55). "
        "La arquitectura offline garantiza la continuidad del servicio en horas pico ante contingencias de red."
    )
    doc.add_paragraph(
        "Financieramente, la propuesta opera con un costo unitario medio de $182.60 MXN y un punto de equilibrio accesible en solo 35 dependencias. "
        "El análisis de sensibilidad demuestra que, ante choques cambiarios del +15% en costos de nube o retrasos burocráticos de hasta 4 meses "
        "en la formalización de contratos de compra, el capital semilla de $120,000.00 MXN mantiene la liquidez en terreno positivo en todo momento. "
        "La indexación de tarifas y costos al INPC, junto con la retención del 5% para el fondo de reserva de reinversión tecnológica a partir del Año 2, "
        "garantiza márgenes netos retenidos superiores al 45%, consolidando en el Año 3 un excedente neto distribuible de $1,324,790.00 MXN y ratificando "
        "su condición de proyecto de inversión autosustentable, resiliente y de alto impacto para la Red Universitaria."
    )

    # =========================================================================
    # SECCIÓN 9: REFERENCIAS BIBLIOGRÁFICAS (APA 7ma Edición)
    # =========================================================================
    add_heading_1("9. Referencias Bibliográficas")
    
    apa_refs = [
        ("ANUIES. (2023). ", "Anuario estadístico de la educación superior 2022-2023: Matrícula y personal docente en instituciones públicas. ", "Asociación Nacional de Universidades e Instituciones de Educación Superior. http://www.anuies.mx/informacion-y-servicios/informacion-estadistica-de-educacion-superior"),
        ("Baca Urbina, G. (2013). ", "Evaluación de proyectos ", "(7.ª ed.). McGraw-Hill Interamericana."),
        ("BBVA. (2021). ", "¿Cómo se determina el precio de un producto? Guía práctica para emprendedores. ", "BBVA Empresas. https://www.bbva.com/es/pe/empresas/como-se-determina-el-precio-de-un-producto-guia-practica-para-emprendedores/"),
        ("Cámara de Diputados del H. Congreso de la Unión. (2017). ", "Ley General de Protección de Datos Personales en Posesión de Sujetos Obligados. ", "Diario Oficial de la Federación, 26 de enero de 2017."),
        ("Congreso del Estado de Jalisco. (2019). ", "Ley de Compras Gubernamentales, Enajenaciones y Contratación de Servicios del Estado de Jalisco y sus Municipios. ", "Periódico Oficial El Estado de Jalisco."),
        ("Hansen, D. R., & Mowen, M. M. (2007). ", "Administración de costos: Contabilidad y control ", "(5.ª ed.). Cengage Learning."),
        ("Horngren, C. T., Datar, S. M., & Rajan, M. V. (2012). ", "Contabilidad de costos: Un enfoque gerencial ", "(14.ª ed.). Pearson Educación."),
        ("Ortegón, E., Pacheco, J. F., & Prieto, A. (2005). ", "Metodología del marco lógico para la planificación, el seguimiento y la evaluación de proyectos y programas. ", "Serie Manuales N.° 42, CEPAL / ILPES."),
        ("Universidad de Guadalajara. (2022). ", "Numeralia institucional: Red Universitaria de Jalisco 2022-2023. ", "Coordinación General de Planeación y Evaluación, Universidad de Guadalajara.")
    ]

    for author_year, title, pub in apa_refs:
        p_ref = doc.add_paragraph()
        p_ref.paragraph_format.left_indent = Inches(0.5)
        p_ref.paragraph_format.first_line_indent = Inches(-0.5)
        p_ref.paragraph_format.space_after = Pt(6)
        
        r1 = p_ref.add_run(author_year)
        r1.font.size = Pt(9.5)
        r1.font.color.rgb = COLOR_TEXT
        
        r2 = p_ref.add_run(title)
        r2.font.size = Pt(9.5)
        r2.font.italic = True
        r2.font.color.rgb = COLOR_TEXT
        
        r3 = p_ref.add_run(pub)
        r3.font.size = Pt(9.5)
        r3.font.color.rgb = COLOR_TEXT

    # Guardar documento Word
    doc.save(output_path)
    print(f"Documento Word generado con éxito: {output_path}")

if __name__ == "__main__":
    out_docx = os.path.join("docs", "Determinacion_Costos_Producto_Servicio_SIGRE.docx")
    generate_cost_docx(out_docx)
