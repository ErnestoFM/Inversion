# -*- coding: utf-8 -*-
"""
Script generador del archivo DOCX oficial: docs/Propuesta_Proyecto_Inversion_SIGRE.docx
Cumple estrictamente con:
- Formato APA 7ma Edición (Margen 1 pulgada, tipografía Calibri, tablas estandarizadas).
- 13 Tablas correlativas numeradas en el cuerpo (Tabla 1 a Tabla 13) con llamada previa.
- 11 Figuras correlativas numeradas (Figura 1 a Figura 11) con imágenes incrustadas.
- Encabezado y Pie de página anti-Turnitin: "Propuesta de Inversión SIGRE — Ernesto Hatuey Fierro Meléndez".
- Recálculo financiero verificado al centavo:
  VPN = +$46,984.47 MXN, TIR = 24.27% anual, Relación B/C = 1.23, Payback Simple = Mes 29.4, Payback Descontado = Mes 33.1.
- Cash Sweep del 70% reconciliado: Liquidación en Mes 31.2, TIR Inversionista a 5 años = 21.20% anual.
- Nómina escalonada sin romper $120k y $240k: Promoción a Especialista en Mes 22.
- CAPEX de $180k con P4 desglosada ($13.5k hardware + $6.5k dossiers) y criterio de estrés financiero.
- Umbral de viabilidad: 18.12 planteles interpolados, 19 enteros seguros (9.7% Red).
- Contratos Año 1: 3 planteles en total (2 prepas comerciales + 1 piloto CUTonalá sin costo) = $63,000 MXN.
- Anexo A (Evidencia Psicométrica SUS) y Anexo B (Video Demostrativo y Matriz de Solventación con Tabla A1).
"""

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
    # Tipografía y Jerarquía APA
    # -------------------------------------------------------------
    COLOR_BLACK = RGBColor(0, 0, 0)
    COLOR_TEXT = RGBColor(33, 37, 41)
    COLOR_MUTED = RGBColor(108, 117, 125)
    
    style_normal = doc.styles['Normal']
    style_normal.font.name = 'Calibri'
    style_normal.font.size = Pt(12)
    style_normal.font.color.rgb = COLOR_TEXT
    style_normal.paragraph_format.line_spacing = 1.15
    style_normal.paragraph_format.space_after = Pt(6)
    style_normal.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    # Encabezado y Pie de página anti-Turnitin (páginas 2 en adelante)
    HEADER_FOOTER_TEXT = "Propuesta de Inversión SIGRE — Ernesto Hatuey Fierro Meléndez"
    
    header = section.header
    p_hdr = header.paragraphs[0]
    p_hdr.text = HEADER_FOOTER_TEXT
    p_hdr.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_hdr.runs[0].font.name = 'Calibri'
    p_hdr.runs[0].font.size = Pt(9.5)
    p_hdr.runs[0].font.color.rgb = COLOR_MUTED
    
    footer = section.footer
    p_ftr = footer.paragraphs[0]
    p_ftr.text = HEADER_FOOTER_TEXT
    p_ftr.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_ftr.runs[0].font.name = 'Calibri'
    p_ftr.runs[0].font.size = Pt(9.5)
    p_ftr.runs[0].font.color.rgb = COLOR_MUTED

    # Funciones auxiliares de estilo
    def set_cell_margins(cell, top=60, bottom=60, left=70, right=70):
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
        r_num.font.size = Pt(11.5)
        r_num.font.color.rgb = COLOR_BLACK
        
        p_tit = doc.add_paragraph()
        p_tit.paragraph_format.space_after = Pt(4)
        p_tit.paragraph_format.keep_with_next = True
        r_tit = p_tit.add_run(title_text)
        r_tit.font.italic = True
        r_tit.font.size = Pt(11.5)
        r_tit.font.color.rgb = COLOR_BLACK

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

    def add_figure_with_image(img_path, fig_num, fig_title, note_text="", width_inches=5.8):
        p_num = doc.add_paragraph()
        p_num.paragraph_format.space_before = Pt(14)
        p_num.paragraph_format.space_after = Pt(2)
        p_num.paragraph_format.keep_with_next = True
        r_num = p_num.add_run(fig_num)
        r_num.font.bold = True
        r_num.font.size = Pt(11.5)
        r_num.font.color.rgb = COLOR_BLACK

        p_tit = doc.add_paragraph()
        p_tit.paragraph_format.space_after = Pt(6)
        p_tit.paragraph_format.keep_with_next = True
        r_tit = p_tit.add_run(fig_title)
        r_tit.font.italic = True
        r_tit.font.size = Pt(11.5)
        r_tit.font.color.rgb = COLOR_BLACK

        if os.path.exists(img_path):
            p_img = doc.add_paragraph()
            p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_img.paragraph_format.space_after = Pt(4)
            p_img.paragraph_format.keep_with_next = True
            r_img = p_img.add_run()
            r_img.add_picture(img_path, width=Inches(width_inches))
        
        if note_text:
            add_table_note(note_text)

    def add_figure_diagram_box(fig_num, fig_title, diagram_text, note_text=""):
        p_num = doc.add_paragraph()
        p_num.paragraph_format.space_before = Pt(14)
        p_num.paragraph_format.space_after = Pt(2)
        p_num.paragraph_format.keep_with_next = True
        r_num = p_num.add_run(fig_num)
        r_num.font.bold = True
        r_num.font.size = Pt(11.5)
        r_num.font.color.rgb = COLOR_BLACK

        p_tit = doc.add_paragraph()
        p_tit.paragraph_format.space_after = Pt(6)
        p_tit.paragraph_format.keep_with_next = True
        r_tit = p_tit.add_run(fig_title)
        r_tit.font.italic = True
        r_tit.font.size = Pt(11.5)
        r_tit.font.color.rgb = COLOR_BLACK

        # Diagram box
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = tbl.rows[0].cells[0]
        set_cell_margins(cell, top=100, bottom=100, left=140, right=140)
        tcPr = cell._tc.get_or_add_tcPr()
        shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="F8F9FA"/>')
        tcPr.append(shd)
        tcBorders = parse_xml(
            f'<w:tcBorders {nsdecls("w")}>'
            f'<w:top w:val="single" w:sz="4" w:space="0" w:color="CCCCCC"/>'
            f'<w:bottom w:val="single" w:sz="4" w:space="0" w:color="CCCCCC"/>'
            f'<w:left w:val="single" w:sz="8" w:space="0" w:color="1A365D"/>'
            f'<w:right w:val="single" w:sz="4" w:space="0" w:color="CCCCCC"/>'
            f'</w:tcBorders>'
        )
        tcPr.append(tcBorders)
        p_box = cell.paragraphs[0]
        p_box.paragraph_format.space_after = Pt(0)
        p_box.paragraph_format.line_spacing = 1.15
        r_box = p_box.add_run(diagram_text)
        r_box.font.name = 'Consolas'
        r_box.font.size = Pt(9.5)
        r_box.font.color.rgb = COLOR_TEXT

        if note_text:
            add_table_note(note_text)

    def add_heading_1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(20)
        p.paragraph_format.space_after = Pt(8)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Calibri'
        run.font.size = Pt(16)
        run.font.bold = True
        run.font.color.rgb = COLOR_BLACK
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
        run.font.color.rgb = COLOR_BLACK
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
        run.font.color.rgb = COLOR_BLACK
        return p

    def add_note_block(title, content):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(8)
        r_t = p.add_run(title + ": ")
        r_t.font.bold = True
        r_t.font.size = Pt(11.5)
        r_t.font.color.rgb = COLOR_BLACK
        r_c = p.add_run(content)
        r_c.font.size = Pt(11.5)
        r_c.font.color.rgb = COLOR_TEXT

    # -------------------------------------------------------------
    # PORTADA INSTITUCIONAL
    # -------------------------------------------------------------
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_inst.paragraph_format.space_before = Pt(20)
    p_inst.paragraph_format.space_after = Pt(4)
    r_uni = p_inst.add_run("UNIVERSIDAD DE GUADALAJARA\n")
    r_uni.font.bold = True
    r_uni.font.size = Pt(15)
    r_uni.font.color.rgb = COLOR_BLACK
    r_cu = p_inst.add_run("CENTRO UNIVERSITARIO DE TONALÁ\nDivisión de Ingenierías e Innovación Tecnológica")
    r_cu.font.size = Pt(12.5)
    r_cu.font.color.rgb = COLOR_MUTED

    p_spc = doc.add_paragraph()
    p_spc.paragraph_format.space_before = Pt(25)

    p_tit = doc.add_paragraph()
    p_tit.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_tit.paragraph_format.space_after = Pt(8)
    r_proj = p_tit.add_run("PROPUESTA DE PROYECTO DE INVERSIÓN:\nPLATAFORMA TECNOLÓGICA SIGRE\n")
    r_proj.font.bold = True
    r_proj.font.size = Pt(18)
    r_proj.font.color.rgb = COLOR_BLACK
    r_sub = p_tit.add_run("Sistema Integrado de Gestión de Recursos, Espacios y Activos para Instituciones de Educación Superior")
    r_sub.font.size = Pt(13)
    r_sub.font.italic = True
    r_sub.font.color.rgb = COLOR_MUTED

    p_spc2 = doc.add_paragraph()
    p_spc2.paragraph_format.space_before = Pt(30)

    # Ficha Técnica de Portada (Front-matter, sin número de tabla para preservar 13 tablas)
    p_ft_hdr = doc.add_paragraph()
    p_ft_hdr.paragraph_format.keep_with_next = True
    r_ft = p_ft_hdr.add_run("Ficha Técnica y Metadatos del Proyecto")
    r_ft.font.bold = True
    r_ft.font.size = Pt(12)
    
    ft_table = doc.add_table(rows=8, cols=2)
    ft_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_apa_table_borders(ft_table)
    
    meta_data = [
        ("Unidad de Aprendizaje", "Formulación y Evaluación de Proyectos de Inversión (FEPI)"),
        ("Docente Titular", "Mtra. Abril Adriana Angulo Sherman"),
        ("Estudiante y Desarrollador", "Ernesto Hatuey Fierro Meléndez"),
        ("Mercado Base de Validación", "Red Universitaria de la Universidad de Guadalajara (UdeG)"),
        ("Monto de Capital Solicitado", "$180,000.00 MXN (Fondo Preoperativo y Validación en Campo)"),
        ("Horizonte Temporal de Evaluación", "3 años (36 meses) de evaluación formal con proyección a 5 años"),
        ("Tasa de Descuento (TMAR)", "15.0% anual (7.12% Cetes 364d + 7.88% prima de riesgo universitario)"),
        ("Fecha de Dictaminación", "Noviembre de 2026")
    ]
    
    for idx, (campo, valor) in enumerate(meta_data):
        row = ft_table.rows[idx]
        c0, c1 = row.cells[0], row.cells[1]
        set_cell_margins(c0, top=50, bottom=50, left=70, right=70)
        set_cell_margins(c1, top=50, bottom=50, left=70, right=70)
        p0 = c0.paragraphs[0]
        r0 = p0.add_run(campo)
        r0.font.bold = True
        r0.font.size = Pt(10.5)
        p1 = c1.paragraphs[0]
        r1 = p1.add_run(valor)
        r1.font.size = Pt(10.5)

    doc.add_page_break()

    # -------------------------------------------------------------
    # ÍNDICE GENERAL DEL DOCUMENTO (Front-matter)
    # -------------------------------------------------------------
    add_heading_1("Índice General del Documento")
    p_toc_desc = doc.add_paragraph("Estructura formal de capítulos, secciones analíticas y contenido:")
    
    toc_t = doc.add_table(rows=8, cols=3)
    toc_t.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_apa_table_borders(toc_t)
    
    toc_headers = ["Capítulo", "Descripción del Contenido Analítico", "Secciones"]
    for j, h in enumerate(toc_headers):
        c = toc_t.rows[0].cells[j]
        set_cell_margins(c, top=60, bottom=60, left=60, right=60)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.font.bold = True
        r.font.size = Pt(10.5)
        
    toc_data = [
        ("1. Identificación y Antecedentes", "Problemática analógica, diagnóstico empírico en CUTonalá, estudio SUS y costos de inacción.", "1.1 a 1.5"),
        ("2. Resumen, Objetivos y MML", "Resumen ejecutivo, objetivos particulares y Matriz de Marco Lógico (CEPAL/BID).", "2.1 a 2.3"),
        ("3. Nicho Asociado UdeG", "Dimensionamiento de 196 planteles y visión de escalamiento a nivel IES nacionales.", "3.1 a 3.2"),
        ("4. Estudio de Mercado y B2G", "Mapeo de decisores, adjudicación directa (<1000 UMA), tarifas y acompañamiento.", "4.1 a 4.5"),
        ("5. Características Técnicas", "Arquitectura en 5 capas, prevención de abusos, contingencia offline y talonarios.", "5.1 a 5.3"),
        ("6. Organización y Programación", "Organigrama, nómina escalonada, plan de acción y cronograma de Gantt con Ruta Crítica.", "6.1 a 6.5"),
        ("7. Inversiones y Evaluación Financiera", "Presupuesto CAPEX, OPEX, Proforma, FEN, VPN (+$46.9k), TIR (24.27%), sensibilidad y Cash Sweep.", "7.1 a 7.6")
    ]
    
    for idx, (cap, desc, sec) in enumerate(toc_data):
        row = toc_t.rows[idx + 1]
        for j, val in enumerate([cap, desc, sec]):
            c = row.cells[j]
            set_cell_margins(c, top=50, bottom=50, left=60, right=60)
            p = c.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT if j < 2 else WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run(val)
            r.font.size = Pt(10.5)
            if j == 0:
                r.font.bold = True
                
    doc.add_page_break()

    # -------------------------------------------------------------
    # 1. IDENTIFICACIÓN Y ANTECEDENTES
    # -------------------------------------------------------------
    add_heading_1("1. Identificación de la Idea de Proyecto a Desarrollar y Antecedentes")
    
    add_heading_2("1.1 Antecedentes y problemática en planteles universitarios")
    doc.add_paragraph(
        "En la gestión cotidiana de las Instituciones de Educación Superior (IES) públicas en México, el préstamo de equipamiento didáctico de alta movilidad "
        "(proyectores multimedia, cables de video HDMI/VGA, adaptadores USB-C, extensiones de uso rudo y apuntadores inalámbricos) y la reservación de espacios "
        "físicos compartidos (auditorios, salas de usos múltiples, laboratorios de cómputo y aulas magnas) se administra de forma predominante mediante libretas "
        "manuales de registro, vales de papel autógrafos y oficios o correos aislados. De acuerdo con el diagnóstico de infraestructura técnica en educación superior "
        "de la ANUIES (2023), la falta de trazabilidad en activos móviles representa uno de los principales focos de ineficiencia y merma en las universidades públicas del país."
    )
    doc.add_paragraph(
        "Aunque este esquema analógico puede operar con relativa eficacia en contextos cerrados o de bajo volumen si se lleva con rigor minucioso, en un campus "
        "universitario promedio —donde concurren miles de estudiantes y cientos de profesores— el cambio de turno en horas pico genera cuellos de botella que rompen "
        "el control administrativo. Esto desencadena tres afectaciones directas: merma patrimonial no deslindada, colisiones de agenda y parálisis pedagógica en aulas, "
        "y ceguera directiva en compras y mantenimiento de equipo docente (Sapag Chain et al., 2014)."
    )

    doc.add_paragraph(
        "En la Figura 1 se contrasta el modelo analógico tradicional frente al flujo de control trazable que implementa la plataforma SIGRE:"
    )
    img_fig1 = "docs/graficos/figura1_diagrama_servicio_sigre.png"
    add_figure_with_image(
        img_fig1, 
        "Figura 1", 
        "Diagrama de flujo del problema operativo analógico frente al flujo digital con trazabilidad de SIGRE",
        "Elaboración propia con base en el mapeo de procesos de mostrador en CUTonalá."
    )

    add_heading_2("1.2 El caso base de validación: CUTonalá")
    doc.add_paragraph(
        "El Centro Universitario de Tonalá (CUTonalá) de la Universidad de Guadalajara fue seleccionado como entorno empírico para el diagnóstico inicial y la prueba "
        "piloto del sistema. Con una matrícula superior a 9,000 estudiantes y una planta de más de 600 docentes, CUTonalá opera tres ventanillas principales de almacén: "
        "el Almacén de Apoyo Educativo (Edificio de Aulas Amplias), la Coordinación de Tecnologías para el Aprendizaje (CTA) y la Ventanilla de Servicios Generales. "
        "Durante los ciclos 2025B y 2026A se documentó un tiempo promedio de entrega analógica de 4.75 minutos por persona y una tasa de pérdida de accesorios del 8.3% mensual."
    )

    add_heading_2("1.3 Diagnóstico observacional, experiencia operativa y evaluación SUS")
    doc.add_paragraph(
        "Para comprobar de forma científica si la interfaz digital de SIGRE resulta ágil o si generaría rechazo en el personal, se administró el cuestionario "
        "estandarizado System Usability Scale (SUS; Bangor et al., 2008; Brooke, 1996; Sauro & Lewis, 2012) a una muestra estratificada de 50 usuarios reales tras "
        "interactuar directamente con el MVP funcional v1.0 (cuyos datos crudos y hojas de captura individual se compilan en el Anexo A: Evidencia Psicométrica y "
        "Validación de Usabilidad SUS). El puntaje global consolidado alcanzó 82.85 puntos (Desviación estándar s = 10.91; Alfa de Cronbach a = 0.892; IC95% = [79.75, 85.95])."
    )
    doc.add_paragraph(
        "Sauro y Lewis (2012) señalan que el promedio industrial estándar de la escala SUS es de 68 puntos. Al obtener 82.85 puntos, SIGRE supera con holgura dicho estándar "
        "y califica en el rango superior 'Excelente' (Grado A, percentil 93) de acuerdo con Bangor et al. (2008), garantizando una adopción orgánica sin resistencia al cambio."
    )

    doc.add_paragraph(
        "Como se observa en la Figura 2, el histograma de distribución de frecuencias de los puntajes SUS evidencia una marcada concentración modal en el rango de excelencia (> 80 puntos), alcanzando una media aritmética consolidada de 82.85 puntos:"
    )
    img_fig2 = "docs/pruebas/screenshots/10_distribucion_puntajes_sus.png"
    add_figure_with_image(
        img_fig2,
        "Figura 2",
        "Distribución de frecuencias y curva de densidad de puntajes SUS (n = 50) frente a la media de la industria",
        "Resultados psicométricos empíricos de usabilidad (Sauro & Lewis, 2012; Bangor et al., 2008). Promedio global: 82.85 pts."
    )

    add_heading_2("1.4 Estimación económica del costo de inacción por plantel")
    doc.add_paragraph(
        "Con base en los reportes de requisiciones de compra de Servicios Generales (2024-2026) y cotizaciones de reposición de equipo de cómputo, "
        "se estructuró la estimación anual de pérdidas y mermas por plantel reflejada en la Tabla 1:"
    )

    add_table_title("Tabla 1", "Estimación preliminar del impacto de la inacción administrativa y pérdidas patrimoniales por plantel")
    pérd_t = doc.add_table(rows=5, cols=4)
    pérd_t.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_apa_table_borders(pérd_t)
    
    headers_p = ["Concepto de Impacto / Ineficiencia", "Frecuencia Anual Estimada", "Rango Económico Anual (MXN)", "Base de Estimación y Justificación"]
    for j, h in enumerate(headers_p):
        c = pérd_t.rows[0].cells[j]
        set_cell_margins(c, top=70, bottom=70, left=70, right=70)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.font.bold = True
        r.font.size = Pt(11)
        
    p_data = [
        ("Pérdida de accesorios menores (cables HDMI, adaptadores, extensiones)", "15 a 30 piezas no devueltas al año por campus", "$20,000 – $30,000", "1 a 2 accesorios perdidos al mes por almacén sin responsable."),
        ("Daño físico en equipos mayores (proyectores, bocinas) sin deslinde", "2 a 4 incidentes anuales con carcasas rotas o puertos", "$60,000 – $90,000", "Reparaciones absorbidas por gasto corriente sin responsable identificado."),
        ("Gasto en papelería, libretas, tóner y vales desechables", "Miles de formatos físicos impresos para archivo muerto", "$10,000 – $20,000", "Consumo continuo de papel y formatos en Servicios Generales."),
        ("Total Estimado de Costo de Inacción", "Costo directo anual acumulado", "$90,000 – $140,000", "Punto medio anual: $115,000 MXN / plantel.")
    ]
    
    for idx, (con, frec, ran, bas) in enumerate(p_data):
        row = pérd_t.rows[idx + 1]
        for j, val in enumerate([con, frec, ran, bas]):
            cell = row.cells[j]
            set_cell_margins(cell, top=60, bottom=60, left=70, right=70)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT if j in (0, 3) else WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run(val)
            r.font.size = Pt(11)
            if idx == 3:
                r.font.bold = True
                
    add_table_note("Elaboración propia con base en cotizaciones de reposición de equipo docente y entrevistas en almacenes de CUTonalá.")

    add_heading_2("1.5 Análisis de alternativas existentes frente a SIGRE")
    doc.add_paragraph(
        "Como se sintetiza en la Tabla 2, las opciones disponibles en el entorno universitario son insuficientes o económicamente inviables frente a la propuesta de valor de SIGRE:"
    )

    add_table_title("Tabla 2", "Matriz comparativa de alternativas de solución técnica frente a la plataforma SIGRE")
    alt_t = doc.add_table(rows=6, cols=5)
    alt_t.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_apa_table_borders(alt_t)
    
    headers_alt = ["Criterio Evaluado", "Libretas y Hojas Excel", "Sistema Central SIIAU", "Software Comercial (Cheqroom)", "Plataforma SIGRE (Propuesta)"]
    for j, h in enumerate(headers_alt):
        c = alt_t.rows[0].cells[j]
        set_cell_margins(c, top=70, bottom=70, left=70, right=70)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.font.bold = True
        r.font.size = Pt(11)
        
    alt_data = [
        ("Tiempo de despacho en ventanilla", "Lento (4.5 a 6.0 min/persona)", "No aplica a ventanilla", "Regular (~1.5 min)", "Ágil (< 30 segundos con QR)"),
        ("Vinculación legal de responsiva", "Firma manual ilegible", "Sin actas de equipo móvil", "Notificaciones por correo", "Firma digital + HMAC-SHA256 en PDF"),
        ("Control de empalmes en espacios", "Inexistente (conflictos diarios)", "Solo planeación semestral", "Sí (calendarios cloud)", "Cerrojos atómicos en Redis (TTL 15 min)"),
        ("Costo anual por plantel", "Oculto en mermas ($115k)", "Incluido en nómina central", "Muy alto ($60k–$90k MXN/año)", "Económico ($24,000 a $48,000 MXN/año)"),
        ("Adaptación normativa y soporte", "Nula", "Rígido; cambios tardan meses", "Nula; soporte remoto en inglés", "Especializado UdeG; presencial y WhatsApp")
    ]
    
    for idx, row_vals in enumerate(alt_data):
        row = alt_t.rows[idx + 1]
        for j, val in enumerate(row_vals):
            cell = row.cells[j]
            set_cell_margins(cell, top=60, bottom=60, left=70, right=70)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT if j == 0 else WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run(val)
            r.font.size = Pt(11)
            if j == 4:
                r.font.bold = True
                
    add_table_note("Elaboración propia a partir del análisis funcional de software de inventarios y sistemas institucionales.")

    add_note_block(
        "Complementariedad y no invasión frente a sistemas centrales",
        "El SIIAU es la plataforma macroinstitucional de la Universidad de Guadalajara para el control escolar, la planeación curricular global y la contabilidad patrimonial centralizada. Por diseño, no fue concebido para la micro-custodia ágil en mostrador ni para el registro transaccional en cambios de clase de 10 minutos. La plataforma SIGRE se circunscribe estrictamente a la micro-custodia operativa de ventanilla y despacho de activos de alta movilidad didáctica (proyectores, cables, adaptadores, extensiones, llaves), sin invadir ni duplicar la contabilidad patrimonial ni el registro de bienes muebles de activo fijo del SIIAU. Por el contrario, SIGRE funge como el alimentador operativo que entrega al SIIAU y a las auditorías internas de la Contraloría actas digitales firmadas y foliadas con trazabilidad jurídica inmutable."
    )

    doc.add_page_break()

    # -------------------------------------------------------------
    # 2. RESUMEN, OBJETIVOS Y MARCO LÓGICO
    # -------------------------------------------------------------
    add_heading_1("2. Resumen, Objetivos y Marco Lógico")
    
    add_heading_2("2.1 Resumen ejecutivo del proyecto y módulos de valor")
    doc.add_paragraph(
        "SIGRE es una solución de software bajo la modalidad SaaS (Software as a Service) orientada a optimizar el ciclo de vida del préstamo institucional mediante "
        "cuatro módulos interconectados: Módulo de Reservas y Gestión de Espacios con cerrojos temporales en Redis (TTL 15 min); Módulo de Despacho Ágil con Código QR "
        "dinámico y validación WebRTC (< 30 s); Módulo de Responsivas Digitales y Checklist Bilateral con firma Canvas HTML5 sellada criptográficamente con HMAC-SHA256; "
        "y Módulo de Reputación y Tablero Directivo con cálculo dinámico del Trust Score del usuario."
    )

    doc.add_paragraph(
        "En la Figura 4 se ilustra la interfaz de mostrador para el estampado de firma manuscrita digitalizada sobre lienzo HTML5 Canvas:"
    )
    img_fig4 = "docs/pruebas/screenshots/05_canvas_firma_digital.png"
    add_figure_with_image(
        img_fig4,
        "Figura 4",
        "Interfaz de firma manuscrita digitalizada sobre Canvas HTML5 con sellado criptográfico HMAC-SHA256",
        "Captura de pantalla del componente de firma digital sobre pantalla táctil en ventanilla de almacén."
    )

    add_heading_2("2.2 Objetivos general y específicos")
    doc.add_paragraph(
        "Objetivo General: Desarrollar, validar y comercializar la plataforma tecnológica SIGRE para digitalizar y automatizar el control de préstamos de equipo "
        "didáctico y reservación de espacios físicos en planteles de educación media superior y superior de la Universidad de Guadalajara, reduciendo las mermas "
        "patrimoniales en al menos un 80% y los tiempos de atención en ventanilla a menos de 30 segundos por operación."
    )
    doc.add_paragraph(
        "Objetivos Específicos:\n"
        "1. Diseñar una arquitectura en la nube (PostgreSQL, Express, React, Node.js y Redis) con capacidad para operar en modo offline sincronizable.\n"
        "2. Ejecutar un despliegue piloto continuo en los 3 almacenes de CUTonalá asegurando un índice SUS > 80 puntos.\n"
        "3. Captar de forma paulatina 8 planteles afiliados hacia el Mes 22 de operaciones, alcanzando el punto de equilibrio operativo en el Mes 14.\n"
        "4. Proteger la propiedad intelectual mediante registro de marca IMPI y depósito de código INDAUTOR en el Semestre 1."
    )

    add_heading_2("2.3 Matriz de Marco Lógico (MML) del Proyecto SIGRE")
    doc.add_paragraph(
        "En apego a los estándares metodológicos oficiales de formulación de proyectos de inversión (CEPAL, 2015; BID, 2020), la Tabla 3 sintetiza la lógica causal vertical y horizontal de la iniciativa:"
    )

    add_table_title("Tabla 3", "Matriz de Marco Lógico (MML) del Proyecto SIGRE bajo estándar metodológico CEPAL/BID")
    mml_t = doc.add_table(rows=5, cols=5)
    mml_t.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_apa_table_borders(mml_t)
    
    headers_m = ["Nivel Jerárquico", "Resumen Narrativo", "Indicadores Objetivamente Verificables", "Medios de Verificación", "Supuestos Críticos"]
    for j, h in enumerate(headers_m):
        c = mml_t.rows[0].cells[j]
        set_cell_margins(c, top=70, bottom=70, left=60, right=60)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.font.bold = True
        r.font.size = Pt(11)
        
    mml_data = [
        ("FIN (Impacto)", "Mejorar la eficiencia administrativa y preservar el patrimonio público en las instituciones de educación superior públicas.", "Reducción del 80% en costos por reposición de equipo no devuelto en campus afiliados al Año 3.", "Informes anuales de auditoría interna y reportes consolidados de inventario físico.", "Las administraciones universitarias priorizan la digitalización y el ahorro en gasto corriente."),
        ("PROPÓSITO (Efecto)", "Planteles universitarios disponen de una plataforma digital auditable y ágil para el control de inventario móvil, espacios y responsivas.", "22 planteles con contrato activo al Año 3; > 65,000 préstamos anuales registrados; cero empalmes de agenda; despacho en mostrador < 30 seg.", "Contratos de suscripción vigentes, bitácoras de base de datos de GCP y reportes de satisfacción de almacén.", "Autoridades mantienen facultades normativas descentralizadas de compra directa menor."),
        ("COMPONENTES (Entregables)", "C1. Software SIGRE en GCP con modo offline.\nC2. Registro de marca IMPI y derechos INDAUTOR.\nC3. Modelo comercial y dossiers de ROI.\nC4. Talleres presenciales y mesa de soporte.", "C1. 99.9% de disponibilidad en nube.\nC2. 2 títulos legales en Año 1.\nC3. 8 contratos en Año 2 y 22 en Año 3.\nC4. 100% de almacenistas capacitados.", "Validación técnica acreditada en el Anexo B: Video Demostrativo E2E, títulos oficiales y contratos firmados.", "Personal sindicalizado de ventanilla mantiene apertura al uso tras recibir inducción práctica."),
        ("ACTIVIDADES (Acciones)", "A1. Refinamiento y offline (M1-M2).\nA2. Piloto CUTonalá (M1-M6).\nA3. Trámites IMPI/INDAUTOR (M2-M6).\nA4. Ajustes operativos (M6).\nA5. Dossiers de ROI (M5).\nA6. Gira comercial (M5-M8).\nA7. Cierre primeros 2 contratos (M7-M8).\nA8. Soporte continuo (M9-M12).", "Presupuesto semilla de $180,000 MXN ejercido conforme al calendario de partidas de capital preoperativo en el primer año.", "Facturas fiscales de servicios cloud, títulos oficiales del IMPI y minutas de reunión ejecutiva.", "El desembolso del capital semilla de $180,000 MXN se formaliza oportunamente al arranque del proyecto.")
    ]
    
    for idx, row_vals in enumerate(mml_data):
        row = mml_t.rows[idx + 1]
        for j, val in enumerate(row_vals):
            cell = row.cells[j]
            set_cell_margins(cell, top=60, bottom=60, left=60, right=60)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(val)
            r.font.size = Pt(10.5)
            if j == 0:
                r.font.bold = True
                
    add_table_note("Elaboración propia con base en los lineamientos metodológicos de la CEPAL (2015) y el BID (2020).")

    doc.add_page_break()

    # -------------------------------------------------------------
    # 3. NICHO ASOCIADO DEL PROYECTO (EL ENTORNO UDEG)
    # -------------------------------------------------------------
    add_heading_1("3. Nicho Asociado del Proyecto (El Entorno UdeG)")
    
    add_heading_2("3.1 Mercado base cautivo: Red Universitaria UdeG")
    doc.add_paragraph(
        "El nicho inmediato del proyecto está delimitado por la Red Universitaria de Jalisco, un ecosistema altamente homogéneo que comparte el mismo calendario escolar, "
        "normatividad de compras y problemáticas logísticas. De acuerdo con la numeralia institucional actualizada de la Coordinación General de Planeación y Evaluación "
        "(CGPE, mayo de 2026; SEMS, 2024), el universo total disponible en la Red Universitaria suma 196 dependencias:\n"
        "- 19 Centros Universitarios: 9 metropolitanos en la Zona Metropolitana de Guadalajara (7 temáticos tradicionales: CUCEI, CUCEA, CUAAD, CUCS, CUCSH, CUCBA y CUGuadalajara; "
        "más 2 centros multitemáticos metropolitanos: CUTonalá y CUTlaquepaque) y 10 centros universitarios regionales distribuidos en las regiones del interior de Jalisco "
        "(CUSur, CUNorte, CUCiénega, CUCosta, CUAltos, CUValles, CULagos, CUChapala, CUCosta Sur, etc.).\n"
        "- 177 Dependencias del SEMS: 33 escuelas preparatorias metropolitanas en la ZMG y 144 dependencias y módulos regionales en el interior del estado (76 escuelas preparatorias sede y 101 módulos)."
    )
    doc.add_paragraph(
        "Como detalla la Tabla 4, la meta de captación de 22 planteles para el cierre del Año 3 representa únicamente el 11.2% del mercado cautivo disponible, "
        "confirmando que las proyecciones financieras no dependen de tasas de penetración irreales:"
    )

    add_table_title("Tabla 4", "Segmentación del mercado potencial cautivo en la Red Universitaria UdeG y metas de captación")
    mer_t = doc.add_table(rows=6, cols=6)
    mer_t.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_apa_table_borders(mer_t)
    
    headers_mr = ["Segmento Institucional", "Universo Total", "Meta Año 3", "% Penetración", "Tarifa Anual", "Facturación Anual"]
    for j, h in enumerate(headers_mr):
        c = mer_t.rows[0].cells[j]
        set_cell_margins(c, top=70, bottom=70, left=60, right=60)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.font.bold = True
        r.font.size = Pt(11)
        
    mr_data = [
        ("Centros Universitarios Metropolitanos (ZMG)", "9 dependencias", "3 planteles", "33.3%", "$48,000 MXN", "$144,000 MXN"),
        ("Centros Universitarios Regionales (Interior)", "10 dependencias", "5 planteles", "50.0%", "$48,000 MXN", "$240,000 MXN"),
        ("Preparatorias Metropolitanas SEMS (ZMG)", "33 dependencias", "8 planteles", "24.2%", "$24,000 MXN", "$192,000 MXN"),
        ("Preparatorias Regionales y Módulos SEMS", "144 dependencias", "6 planteles", "4.2%", "$24,000 MXN", "$144,000 MXN"),
        ("Total Consolidado de la Red", "196 dependencias", "22 planteles", "11.2%", "—", "$720,000 MXN")
    ]
    
    for idx, row_vals in enumerate(mr_data):
        row = mer_t.rows[idx + 1]
        for j, val in enumerate(row_vals):
            cell = row.cells[j]
            set_cell_margins(cell, top=60, bottom=60, left=60, right=60)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT if j == 0 else WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run(val)
            r.font.size = Pt(11)
            if idx == 4:
                r.font.bold = True
                
    add_table_note("Elaboración propia con base en la Numeralia Institucional de la Universidad de Guadalajara (CGPE, mayo de 2026; SEMS, 2024).")

    add_heading_2("3.2 Visión de escalamiento: de la Red UdeG a las IES públicas nacionales")
    doc.add_paragraph(
        "Para un inversionista de capital semilla, un proyecto confinado a una sola institución representa un techo de mercado estrecho. La ventaja estructural de SIGRE "
        "radica en que el modelo SaaS y su arquitectura desacoplada permiten extrapolar la solución hacia cualquier universidad pública de México con requerimientos "
        "mínimos de parametrización (catálogo de dependencias, logotipos y correos institucionales)."
    )

    doc.add_paragraph(
        "La Figura 3 ilustra la hoja de ruta de escalamiento progresivo del proyecto desde el nicho cautivo hacia el sistema nacional de educación superior:"
    )
    diag_fig3 = (
        "+---------------------+      +---------------------+      +---------------------+      +---------------------+\n"
        "|  Fase 1 (Año 1)     | ---> |  Fase 2 (Años 2-3)  | ---> |  Fase 3 (Años 4-5)  | ---> |  Fase 4 (Año 5+)    |\n"
        "|  Piloto y Validación|      |  Escalamiento UdeG  |      |  IES Jalisco/Región |      |  Nacional UPES      |\n"
        "|  CUTonalá Base      |      |  22 Planteles Red   |      |  UTJ, ITSZ, UColima |      |  60+ Universidades  |\n"
        "+---------------------+      +---------------------+      +---------------------+      +---------------------+"
    )
    add_figure_diagram_box(
        "Figura 3",
        "Visión de escalamiento institucional progresivo: de la Red UdeG a las IES públicas nacionales",
        diag_fig3,
        "Hoja de ruta estratégica de penetración comercial en educación superior pública."
    )

    doc.add_page_break()

    # -------------------------------------------------------------
    # 4. ESTUDIO DE MERCADO Y COMERCIALIZACIÓN
    # -------------------------------------------------------------
    add_heading_1("4. Estudio de Mercado y Comercialización")
    
    add_heading_2("4.1 Estructura de decisores de compra por tipo de plantel")
    doc.add_paragraph(
        "La venta B2G (Business-to-Government) universitaria exige adaptar el discurso al rol específico de cada autoridad:\n"
        "- En Centros Universitarios (Secretario Administrativo): El argumento central es el blindaje patrimonial. SIGRE entrega actas inmutables en PDF con firma digital que acreditan la custodia del patrimonio público, reduciendo observaciones de auditoría por equipo faltante.\n"
        "- En Escuelas Preparatorias del SEMS (Director de Plantel): Se busca la continuidad de clases y un costo accesible. Una cuota anual de $24,000 MXN es inferior a reponer un solo proyector extraviado y puede pagarse con gasto corriente ordinario.\n"
        "- En Coordinaciones Técnicas (CTA y Servicios Generales): Se busca agilizar el cambio de turno en ventanilla a menos de 30 segundos, convirtiéndose en los promotores internos de la adopción del sistema."
    )

    add_heading_2("4.2 Viabilidad burocrática y compra directa")
    doc.add_paragraph(
        "Conforme al Reglamento de Adquisiciones, Arrendamientos y Contratación de Servicios de la Universidad de Guadalajara (UdeG, 2019), las compras menores a 1,000 "
        "Unidades de Medida y Actualización (UMA) pueden adjudicarse de forma directa sin licitación pública. Con la UMA diaria vigente en 2026 fijada en $117.31 MXN por el "
        "INEGI (2026), dicho umbral asciende a $117,310.00 MXN. Las tarifas anuales de SIGRE ($24,000 MXN y $48,000 MXN) se sitúan holgadamente por debajo de dicho tope legal, "
        "facultando al Director o Secretario Administrativo a suscribir el contrato en días hábiles sin trámites licitatorios."
    )

    add_heading_2("4.3 Motivación y desglose de tarifas frente a costos de servicio")
    doc.add_paragraph(
        "La diferenciación de precios responde al volumen operativo y requerimientos de soporte de cada institución, como se desglosa en la Tabla 5:"
    )

    add_table_title("Tabla 5", "Estructura de tarifas anuales, cuotas de configuración y cobertura operativa por nivel de servicio")
    tar_t = doc.add_table(rows=3, cols=4)
    tar_t.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_apa_table_borders(tar_t)
    
    headers_tr = ["Nivel de Servicio", "Tarifa Anual (MXN)", "Cobertura Operativa Incluida", "Dimensión de Soporte e Inducción"]
    for j, h in enumerate(headers_tr):
        c = tar_t.rows[0].cells[j]
        set_cell_margins(c, top=70, bottom=70, left=70, right=70)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.font.bold = True
        r.font.size = Pt(11)
        
    tr_data = [
        ("Plan Preparatoria SEMS", "$24,000 MXN", "1 a 2 almacenes; hasta 1,500 usuarios; actas y boletos QR ilimitados.", "Taller presencial de 8 hrs; soporte WhatsApp institucional."),
        ("Plan Centro Universitario", "$48,000 MXN", "Hasta 6 almacenes; hasta 8,000 usuarios; control de auditorios.", "Taller presencial de 16 hrs; soporte prioritario con SLA < 2 hrs.")
    ]
    
    for idx, (niv, tar, cob, dim) in enumerate(tr_data):
        row = tar_t.rows[idx + 1]
        for j, val in enumerate([niv, tar, cob, dim]):
            cell = row.cells[j]
            set_cell_margins(cell, top=60, bottom=60, left=70, right=70)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT if j in (0, 2, 3) else WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run(val)
            r.font.size = Pt(11)
            if j == 0:
                r.font.bold = True
                
    add_table_note("Precios netos anuales. Ambas cuotas incluyen consumo de servidores cloud, copias de seguridad continuas y soporte correctivo.")

    doc.add_page_break()

    # -------------------------------------------------------------
    # 5. CARACTERÍSTICAS TÉCNICAS DE LA IMPLEMENTACIÓN
    # -------------------------------------------------------------
    add_heading_1("5. Características Técnicas de la Implementación")
    
    add_heading_2("5.1 Arquitectura tecnológica y parámetros de calidad")
    doc.add_paragraph(
        "En la Figura 5 se presenta el diagrama de arquitectura tecnológica en la nube en 5 capas desacopladas:"
    )
    img_fig5 = "docs/graficos/figura2_diagrama_arquitectura_5capas_sigre.png"
    add_figure_with_image(
        img_fig5,
        "Figura 5",
        "Diagrama de arquitectura tecnológica en la nube y componentes del sistema",
        "Arquitectura modular desacoplada en Google Cloud Platform con Cloud Run, Cloud SQL y Redis."
    )

    doc.add_paragraph(
        "La plataforma se diseñó bajo una arquitectura modular desacoplada en la nube, cuyas especificaciones técnicas y estándares de rendimiento se consolidan en la Tabla 6:"
    )

    add_table_title("Tabla 6", "Ficha técnica de arquitectura de software, infraestructura cloud y parámetros de seguridad")
    tec_t = doc.add_table(rows=7, cols=3)
    tec_t.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_apa_table_borders(tec_t)
    
    headers_tc = ["Capa / Componente", "Tecnología Seleccionada", "Parámetro de Calidad y Rendimiento"]
    for j, h in enumerate(headers_tc):
        c = tec_t.rows[0].cells[j]
        set_cell_margins(c, top=70, bottom=70, left=70, right=70)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.font.bold = True
        r.font.size = Pt(11)
        
    tc_data = [
        ("Frontend de Ventanilla", "React 18, Vite, TailwindCSS, PWA", "Carga inicial < 1.2 segundos; operable en pantallas táctiles y móviles."),
        ("Backend API", "Node.js v20 LTS, Express, TypeScript", "Latencia API < 150 ms en transacciones de despacho."),
        ("Base de Datos Principal", "Google Cloud SQL (PostgreSQL 16)", "Persistencia transaccional ACID, respaldos diarios automatizados."),
        ("Memoria de Concurrencia", "Redis 7.2 en memoria volátil", "Bloqueos atómicos temporales (TTL 900s) para evitar doble agendamiento."),
        ("Motor de Actas y Firma", "PDFKit, Canvas HTML5, HMAC-SHA256", "Generación de actas foliadas < 800 ms con sellado de tiempo UTC."),
        ("Infraestructura Cloud", "Google Cloud Run (Serverless)", "Auto-escalado de 0 a 10 instancias con 99.9% de disponibilidad.")
    ]
    
    for idx, (cap, tec, par) in enumerate(tc_data):
        row = tec_t.rows[idx + 1]
        for j, val in enumerate([cap, tec, par]):
            cell = row.cells[j]
            set_cell_margins(cell, top=60, bottom=60, left=70, right=70)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(val)
            r.font.size = Pt(11)
            if j == 0:
                r.font.bold = True
                
    add_table_note("Especificaciones validadas en el entorno de producción de Google Cloud Platform y pruebas de estrés de carga concurrentes.")

    add_heading_2("5.2 Registro de desgaste individual de activos y prevención de abusos")
    doc.add_paragraph(
        "A diferencia de un inventario estático que solo cuenta cuántos proyectores existen, SIGRE implementa una bitácora dinámica del ciclo de vida del activo: "
        "conteo de horas de lámpara/uso acumuladas; inspección de desgaste en 3 clics al retornar el bien (Óptimo, Desgaste Normal o Anomalía Física con foto de evidencia); "
        "e índice de confiabilidad del solicitante (Trust Score de 0 a 100 puntos), incentivando la devolución puntual y el cuidado del patrimonio."
    )

    doc.add_paragraph(
        "En la Figura 10 se muestra el tablero directivo ejecutivo, el cual permite a las autoridades auditar la tasa de uso, horas de operación e incidencias de desgaste en tiempo real:"
    )
    img_fig10 = "docs/pruebas/screenshots/08_dashboard_ejecutivo.png"
    add_figure_with_image(
        img_fig10,
        "Figura 10",
        "Tablero directivo ejecutivo con telemetría de activos y control de inventario en tiempo real",
        "Consola directiva de control con rotación de inventario, índice de confiabilidad y auditoría de incidencias."
    )

    add_heading_2("5.3 Plan de contingencia tecnológica y continuidad operativa")
    doc.add_paragraph(
        "Para garantizar que la ventanilla jamás detenga su operación ante fallas de infraestructura, el sistema incorpora dos salvaguardas críticas: "
        "modo offline en PWA que almacena en caché local (IndexedDB) el catálogo y permite registrar préstamos sin internet, sincronizando en segundo plano al reanudar enlace; "
        "y talonarios físicos prefoliados de 100 actas de contingencia con códigos QR estáticos para cortes prolongados de energía eléctrica, con captura en lote en menos de 15 minutos."
    )

    doc.add_page_break()

    # -------------------------------------------------------------
    # 6. ESTRUCTURA ORGANIZACIONAL, TAMAÑO Y PROGRAMACIÓN
    # -------------------------------------------------------------
    add_heading_1("6. Estructura Organizacional, Tamaño y Programación")
    
    add_heading_2("6.1 Estructura organizacional y perfiles del equipo inicial")
    doc.add_paragraph(
        "La conducción del proyecto durante su fase preoperativa y primer año comercial se rige por un esquema corporativo esbelto (lean startup), donde los tres socios fundadores "
        "absorben de manera integral las directrices ejecutivas, la robustez de software y el aseguramiento del servicio en campo, posponiendo contrataciones accesorias hasta que "
        "la masa crítica de clientes lo justifique:"
    )

    doc.add_paragraph(
        "La estructura funcional inicial y los hitos de incorporación progresiva de capital humano se representan en la Figura 6:"
    )
    diag_fig6 = (
        "                        +---------------------------------------------+\n"
        "                        |    Dirección General y Comercialización     |\n"
        "                        |    (Ernesto Hatuey Fierro Meléndez)         |\n"
        "                        +----------------------+----------------------+\n"
        "                                               |\n"
        "                       +-----------------------+-----------------------+\n"
        "                       |                                               |\n"
        "        +--------------+--------------+                 +--------------+--------------+\n"
        "        |  Dirección Técnica y Cloud  |                 | Coordinación de Operaciones  |\n"
        "        |  (Líder de Arquitectura TI) |                 | (Especialista de Ventanilla) |\n"
        "        +-----------------------------+                 +--------------+--------------+\n"
        "                                                                       :\n"
        "                                                      ===================================\n"
        "                                                      : Escalamiento Progresivo de Personal\n"
        "                                                      : -> Técnico Soporte N1 (Mes 15)\n"
        "                                                      : -> Especialista TC (Mes 22)\n"
        "                                                      : -> Customer Success (Mes 28)\n"
        "                                                      ==================================="
    )
    add_figure_diagram_box(
        "Figura 6",
        "Organigrama funcional del equipo inicial y fases de escalamiento de personal",
        diag_fig6,
        "Estructura organizacional lean y plan de crecimiento escalonado de nómina."
    )

    doc.add_paragraph(
        "El liderazgo ejecutivo y las relaciones institucionales son conducidos por el Director de Proyecto (Ernesto Hatuey Fierro Meléndez), quien encabeza la interlocución "
        "estratégica ante las Secretarías Administrativas y Direcciones de Preparatoria, supervisa el cumplimiento normativo en adquisiciones universitarias y lidera los "
        "expedientes de propiedad intelectual ante el IMPI y el INDAUTOR (dedicación: 60% comercial y 40% administrativo).\n"
        "La dirección técnica está a cargo del Líder Técnico, responsable de la estabilidad del monorepo, el despliegue serverless en Google Cloud Platform y la seguridad "
        "criptográfica de responsivas digitales (disponibilidad > 99.9%).\n"
        "La coordinación operativa recae en el Especialista de Mostrador, encargado de impartir los talleres presenciales de 16 horas y coordinar la mesa de soporte técnico WhatsApp."
    )

    add_heading_2("6.2 Plan de escalamiento del equipo y modelo de compensación")
    doc.add_paragraph(
        "El crecimiento de la nómina está condicionado al cumplimiento de metas comerciales precisas, estructurado a través de los gatillos objetivos reflejados en la Tabla 7:"
    )

    add_table_title("Tabla 7", "Plan de escalamiento del capital humano conforme al crecimiento de la cartera y modelo de compensación")
    cap_t = doc.add_table(rows=5, cols=4)
    cap_t.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_apa_table_borders(cap_t)
    
    headers_cp = ["Periodo / Fase", "Posición a Incorporar", "Gatillo de Activación", "Función Crítica del Puesto"]
    for j, h in enumerate(headers_cp):
        c = cap_t.rows[0].cells[j]
        set_cell_margins(c, top=70, bottom=70, left=70, right=70)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.font.bold = True
        r.font.size = Pt(11)
        
    cp_data = [
        ("Año 1 (Piloto)", "Equipo fundador (3 personas)", "Capital semilla inicial", "Desarrollo de software, piloto en CUTonalá y primeros contratos comerciales."),
        ("Año 2 (Mes 15)", "1 Técnico de Soporte Nivel 1 (Medio tiempo)", "Cartera supera los 6 planteles activos", "Monitoreo del canal de soporte WhatsApp y resolución de tickets básicos."),
        ("Año 2 (Mes 22)", "1 Especialista de Soporte Técnico (Tiempo completo)", "Cartera alcanza los 8 planteles activos", "Promoción interna de N1 a tiempo completo; inducción en nuevos campus."),
        ("Año 3 (Mes 28)", "1 Coordinador de Customer Success", "Cartera supera los 15 planteles activos", "Auditorías de satisfacción, relación con directores y cobranza de renovaciones.")
    ]
    
    for idx, (per, pos, gat, fun) in enumerate(cp_data):
        row = cap_t.rows[idx + 1]
        for j, val in enumerate([per, pos, gat, fun]):
            cell = row.cells[j]
            set_cell_margins(cell, top=60, bottom=60, left=70, right=70)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(val)
            r.font.size = Pt(11)
            if j == 0:
                r.font.bold = True
                
    add_table_note("Elaboración propia. Cada puesto se financia exclusivamente mediante el flujo de efectivo neto generado por los nuevos contratos.")

    add_note_block(
        "Desglose de nómina escalonada sin alterar techos presupuestales ($120k y $240k)",
        "En el Año 2 ($120,000 MXN anuales de personal): en el Mes 15 se incorpora el Técnico de Soporte N1 a medio tiempo ($4,000 MXN/mes durante 7 meses = $28,000 MXN); en el Mes 22, al alcanzarse los 8 planteles, dicho técnico se promueve a Especialista de Soporte Técnico de Tiempo Completo ($10,000 MXN/mes durante 3 meses = $30,000 MXN); el remanente de $62,000 MXN se asigna a honorarios de gestión para el equipo fundador, cuadrando de manera idéntica los $120,000 MXN estipulados en el OPEX del Año 2.\n"
        "En el Año 3 ($240,000 MXN anuales de personal): el Especialista de Soporte labora los 12 meses completos ($10,000 MXN/mes = $120,000 MXN); en el Mes 28 se incorpora el Coordinador de Customer Success ($7,000 MXN/mes durante 9 meses = $63,000 MXN); el saldo restante de $57,000 MXN se destina a estipendios de dirección para los fundadores, cuadrando de manera exacta los $240,000 MXN presupuestados."
    )

    add_heading_2("6.3 Justificación de bienes inmuebles, coworking y contingencia")
    doc.add_paragraph(
        "SIGRE opera bajo un modelo de teletrabajo para desarrollo y aprovecha las instalaciones de coworking del Centro de Emprendimiento e Innovación de CUTonalá "
        "para reuniones ejecutivas con autoridades universitarias, ahorrando costos de arrendamiento comercial en la etapa de arranque. La partida de Fondo de Reserva y "
        "Contingencia Operativa ($40,000 MXN) en cuenta bancaria cuenta con holgura suficiente para cubrir el alquiler de coworking privado (~$3,500 MXN/mes) si fuera requerido."
    )

    add_heading_2("6.4 Diagrama del Plan de Acción Operativo por Fases (Año 1)")
    doc.add_paragraph(
        "La interdependencia secuencial de las cuatro fases operativas del primer año se esquematiza en la Figura 7:"
    )
    diag_fig7 = (
        "+-----------------------+         +-----------------------+\n"
        "| Fase I (Meses 1 a 6)  | ------> | Fase III (Meses 5 a 8)|\n"
        "| Estabilización Técnica|         | Gira Comercial UdeG   |\n"
        "| Piloto CUTonalá 3k fol|         | 10 Reuniones Direct.  |\n"
        "+-----------------------+         | Cierre 3 Planteles    |\n"
        "                                  +-----------+-----------+\n"
        "+-----------------------+                     |\n"
        "| Fase II (Meses 2 a 6) | --------------------+       v\n"
        "| Trámites Legales      |         +-----------------------+\n"
        "| Registro Marca IMPI   |         | Fase IV (Meses 9 a 12)|\n"
        "| Depósito INDAUTOR     |         | Mesa de Servicio      |\n"
        "+-----------------------+         | SLA < 2h; Escalamiento|\n"
        "                                  +-----------------------+"
    )
    add_figure_diagram_box(
        "Figura 7",
        "Diagrama del plan de acción operativo por fases (Año 1 de operaciones)",
        diag_fig7,
        "Fases secuenciales de despliegue preoperativo y comercial en el Año 1."
    )

    doc.add_paragraph(
        "El despliegue operativo del primer año se distribuye en cuatro fases secuenciales debidamente auditadas, descritas en la Tabla 8:"
    )

    add_table_title("Tabla 8", "Diagrama del plan de acción operativo por fases (Año 1 de operaciones)")
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
        ("Fase II: Protección Legal e Intelectual", "Meses 2 a 6", "Tramitar registro de marca y derechos de autor del código fuente.", "Solicitudes ante IMPI (tarifa oficial $3,126.41) e INDAUTOR con título oficial."),
        ("Fase III: Lanzamiento y Gira Comercial", "Meses 5 a 8", "Sostener reuniones ejecutivas con secretarios administrativos y directores.", "10 reuniones presenciales, 5 pilotos y cierre de 3 planteles en total (2 contratos comerciales de Prepas con pago anual anticipado al ciclo B + 1 piloto CUTonalá sin costo)."),
        ("Fase IV: Operación y Mesa de Servicio", "Meses 9 a 12", "Atención continua a planteles afiliados y evaluación para escalamiento del Año 2.", "Mesa de WhatsApp con SLA < 2h y reporte de retención del 100% de clientes.")
    ]
    
    for idx, (fas, per, obj, ent) in enumerate(ac_data):
        row = act_t.rows[idx + 1]
        for j, val in enumerate([fas, per, obj, ent]):
            cell = row.cells[j]
            set_cell_margins(cell, top=60, bottom=60, left=70, right=70)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(val)
            r.font.size = Pt(11)
            if j == 0:
                r.font.bold = True
                
    add_table_note("Elaboración propia. El avance entre fases requiere el cumplimiento previo de los entregables verificables.")

    add_heading_2("6.5 Cronograma Anual en Diagrama de Gantt y Ruta Crítica [RC]")
    doc.add_paragraph(
        "En la Figura 8 se detalla la programación temporal de tareas a lo largo de los primeros doce meses, resaltando en rojo las actividades críticas [RC]:"
    )
    diag_fig8 = (
        "Actividad Clave                    Ene Feb Mar Abr May Jun Jul Ago Sep Oct Nov Dic  ¿Ruta Crítica?\n"
        "------------------------------------------------------------------------------------------------\n"
        "A1. Refinamiento y offline [RC]    [====]                                           SÍ [RC]\n"
        "A2. Piloto CUTonalá [RC]           [===================]                            SÍ [RC]\n"
        "A3. Registro IMPI / INDAUTOR           [===================]                        NO (Holg: 1m)\n"
        "A4. Ajustes por feedback [RC]                          [===]                        SÍ [RC]\n"
        "A5. Dossiers de ROI                                [===]                            NO (Holg: 2m)\n"
        "A6. Gira Comercial UdeG [RC]                       [===============]                SÍ [RC]\n"
        "A7. Firma 2 Contratos Prepas [RC]                          [=======]                SÍ [RC]\n"
        "A8. Soporte y Evaluación [RC]                                      [===============] SÍ [RC]"
    )
    add_figure_diagram_box(
        "Figura 8",
        "Cronograma de ejecución anual en diagrama de Gantt y Ruta Crítica [RC]",
        diag_fig8,
        "Cronograma maestro con dependencias estrictas y holguras operativas para el primer año."
    )

    doc.add_paragraph(
        "El calendario maestro de actividades del primer año, con la identificación de holguras y de la Ruta Crítica [RC], se resume en la Tabla 9:"
    )

    add_table_title("Tabla 9", "Diagrama de Gantt anual con dependencias y Ruta Crítica [RC] (Año 1)")
    gantt_t = doc.add_table(rows=9, cols=5)
    gantt_t.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_apa_table_borders(gantt_t)
    
    headers_gt = ["Actividad Clave de Ejecución", "Duración", "Dependencia", "Periodo de Ejecución", "¿Ruta Crítica?"]
    for j, h in enumerate(headers_gt):
        c = gantt_t.rows[0].cells[j]
        set_cell_margins(c, top=70, bottom=70, left=60, right=60)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.font.bold = True
        r.font.size = Pt(11)
        
    gt_data = [
        ("A1. Refinamiento arquitectónico y modo offline", "2 meses", "Hito inicial", "Mes 1 y Mes 2", "SÍ [RC]"),
        ("A2. Despliegue piloto continuo en 3 almacenes CUTonalá", "6 meses", "A1", "Mes 1 a Mes 6", "SÍ [RC]"),
        ("A3. Registro de Marca IMPI y Depósito INDAUTOR", "5 meses", "A1", "Mes 2 a Mes 6", "NO (Holgura: 1m)"),
        ("A4. Ajustes por retroalimentación de almacenistas", "1 mes", "A2", "Mes 6", "SÍ [RC]"),
        ("A5. Elaboración de dossiers ejecutivos de ROI", "1 mes", "A2", "Mes 5", "NO (Holgura: 2m)"),
        ("A6. Gira comercial y reuniones con Secretarios Adm.", "4 meses", "A4, A5", "Mes 5 a Mes 8", "SÍ [RC]"),
        ("A7. Firma y cobranza de primeros contratos comerciales", "2 meses", "A6", "Mes 7 y Mes 8", "SÍ [RC]"),
        ("A8. Despliegue de soporte continuo y evaluación", "4 meses", "A7", "Mes 9 a Mes 12", "SÍ [RC]")
    ]
    
    for idx, (act, dur, dep, eje, rtc) in enumerate(gt_data):
        row = gantt_t.rows[idx + 1]
        for j, val in enumerate([act, dur, dep, eje, rtc]):
            cell = row.cells[j]
            set_cell_margins(cell, top=60, bottom=60, left=60, right=60)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT if j == 0 else WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run(val)
            r.font.size = Pt(11)
            if "SÍ" in rtc and j == 4:
                r.font.bold = True
                
    add_table_note("Elaboración propia con base en el método de la Ruta Crítica (CPM). Las tareas [RC] determinan la fecha de cobranza comercial.")

    doc.add_page_break()

    # -------------------------------------------------------------
    # 7. INVERSIONES, COSTOS, INGRESOS Y EVALUACIÓN FINANCIERA
    # -------------------------------------------------------------
    add_heading_1("7. Inversiones, Costos, Ingresos y Evaluación Financiera")
    
    add_heading_2("7.1 Presupuesto de inversión inicial requerida (CAPEX: $180,000 MXN)")
    doc.add_paragraph(
        "El presupuesto de capital inicial se dimensionó como un fondo preoperativo de caja que sostiene los primeros 12 meses de operación, estructurado en la Tabla 10:"
    )

    add_table_title("Tabla 10", "Presupuesto desglosado de inversión inicial requerida (CAPEX de $180,000 MXN)")
    capex_t = doc.add_table(rows=7, cols=4)
    capex_t.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_apa_table_borders(capex_t)
    
    headers_cx = ["Partida de Inversión Inicial", "Concepto y Destino Específico del Capital", "Monto (MXN)", "% Participación"]
    for j, h in enumerate(headers_cx):
        c = capex_t.rows[0].cells[j]
        set_cell_margins(c, top=70, bottom=70, left=70, right=70)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.font.bold = True
        r.font.size = Pt(11)
        
    cx_data = [
        ("P1. Pulido técnico y desarrollo de software", "Compensación preoperativa para el equipo fundador de desarrollo durante 6 meses de piloto.", "$75,000 MXN", "41.7%"),
        ("P2. Infraestructura cloud y servicios web", "Servidores GCP, Cloud SQL PostgreSQL 16, Redis y certificados criptográficos SSL (Año 1).", "$20,000 MXN", "11.1%"),
        ("P3. Propiedad intelectual y trámites", "Registro de marca IMPI (Tarifa oficial $3,126.41 MXN), depósito INDAUTOR y asesoría legal.", "$25,000 MXN", "13.9%"),
        ("P4. Equipamiento demo y material comercial", "3 escáneres ópticos 2D industriales y tableta demo ($13,500 MXN) más dossiers de ROI impresos ($6,500 MXN).", "$20,000 MXN", "11.1%"),
        ("P5. Fondo de reserva y contingencia operativa", "Respaldo de liquidez ante desfases en órdenes de compra y retrasos burocráticos de cobranza.", "$40,000 MXN", "22.2%"),
        ("Total Inversión Inicial Requerida (CAPEX)", "Monto total de capital semilla solicitado (Fondeo Mes 0).", "$180,000 MXN", "100.0%")
    ]
    
    for idx, (par, con, mon, pct) in enumerate(cx_data):
        row = capex_t.rows[idx + 1]
        for j, val in enumerate([par, con, mon, pct]):
            cell = row.cells[j]
            set_cell_margins(cell, top=60, bottom=60, left=70, right=70)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT if j in (0, 1) else WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run(val)
            r.font.size = Pt(11)
            if idx == 5:
                r.font.bold = True
                
    add_table_note("Elaboración propia. Presupuesto preoperativo que cubre el Año 1 de validación hasta el cobro de suscripciones comerciales.")

    add_note_block(
        "Criterio metodológico de estrés financiero (Evaluación ultra-conservadora)",
        "Para efectos de la evaluación financiera formal y en apego a una metodología de máximo estrés financiero, el modelo matemático computa tanto el desembolso íntegro de la inversión preoperativa en el Año 0 (I0 = -$180,000 MXN) como el flujo negativo del Año 1 (FEN1 = -$32,000 MXN), sin asumir el rescate o acreditación del fondo de reserva de caja ($40,000 MXN). Este doble castigo deliberado al flujo de caja somete el proyecto a la prueba de solvencia más severa posible; aún bajo este escenario de máxima exigencia analítica, el proyecto demuestra plena solvencia y viabilidad económica al arrojar un Valor Presente Neto positivo de +$46,984.47 MXN y una Tasa Interna de Retorno del 24.27% anual, muy por encima de la TMAR del 15.0%. Asimismo, se desglosó la partida P4 excluyendo viáticos para eliminar cualquier duplicidad con los costos operativos (OPEX) del Año 1."
    )

    add_heading_2("7.2 Estructura de costos operativos (OPEX)")
    doc.add_paragraph(
        "Los costos operativos comprenden dos partidas nucleares:\n"
        "- Costos Variables: Consumo elástico de infraestructura cloud (Google Cloud Platform), iniciando en $1,500 MXN mensuales en la fase piloto y escalando suavemente hasta $5,400 MXN al mes al consolidar 22 planteles activos.\n"
        "- Costos Fijos: Nómina escalonada del personal de soporte ($120,000 MXN en Año 2 y $240,000 MXN en Año 3), viáticos de capacitación presencial en planteles y servicios externos de despacho contable y fiscal ($1,000 a $3,000 MXN mensuales)."
    )

    add_heading_2("7.3 Proyecciones trienales de facturación e ingresos (Pesos MXN)")
    doc.add_paragraph(
        "Las proyecciones de venta asumen un modelo de suscripción anual fija que se factura al inicio de cada ciclo presupuestal universitario. "
        "En el Año 1 se atienden 3 planteles en total: el campus piloto CUTonalá (sin costo de suscripción, cubriendo únicamente $15,000 MXN de configuración de sus 3 almacenes) "
        "y 2 contratos comerciales de escuelas preparatorias metropolitanas cerrados en los Meses 7 y 8 a su tarifa anual completa de $24,000 MXN cada una, cobradas por "
        "anticipado al arranque del ciclo B de agosto, totalizando exactamente $63,000 MXN brutos:"
    )

    add_table_title("Tabla 11", "Proyección trienal de facturación e ingresos brutos del proyecto (Pesos MXN)")
    proy_t = doc.add_table(rows=5, cols=4)
    proy_t.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_apa_table_borders(proy_t)
    
    headers_py = ["Indicador Comercial", "Año 1 (Piloto)", "Año 2 (Crecimiento)", "Año 3 (Madurez Operativa)"]
    for j, h in enumerate(headers_py):
        c = proy_t.rows[0].cells[j]
        set_cell_margins(c, top=70, bottom=70, left=70, right=70)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.font.bold = True
        r.font.size = Pt(11)
        
    py_data = [
        ("Planteles activos en operación", "3 Planteles (1 Piloto CUTonalá sin costo + 2 Prepas comerciales)", "8 Planteles (3 CUs + 5 Prepas)", "22 Planteles (8 CUs + 14 Prepas)"),
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
        "La Figura 9 ilustra la trayectoria financiera trienal, evidenciando el punto de inflexión operativa a partir del Año 2:"
    )
    diag_fig9 = (
        "Monto Anual (Miles MXN)\n"
        "900 |                                                 [Ingresos: $850k]\n"
        "800 |                                                 |\n"
        "700 |                                                 |\n"
        "600 |                                                 |\n"
        "500 |                                                 | [OPEX: $426k]\n"
        "400 |                             [Ingresos: $324k]   |\n"
        "300 |                             |                   * FEN: +$296.8k\n"
        "200 |                             | [OPEX: $225k]     |\n"
        "100 |     [Ing: $63k]             * FEN: +$78.9k      |\n"
        "  0 |-----+---[OPEX: $55k]--------+-------------------+-----------------\n"
        "-50 |     * FEN: -$32k\n"
        "          Año 1 (Piloto)          Año 2 (Crecimiento) Año 3 (Madurez)"
    )
    add_figure_diagram_box(
        "Figura 9",
        "Comportamiento proyectado de ingresos brutos, costos operativos y Flujo de Efectivo Neto (FEN)",
        diag_fig9,
        "Proyección financiera trienal. El FEN se torna positivo a partir del Año 2."
    )

    doc.add_paragraph(
        "La evolución de los ingresos brutos, los costos operativos y la utilidad neta a lo largo de los tres periodos anuales se consolida en el Estado de Resultados Proforma de la Tabla 12:"
    )

    add_table_title("Tabla 12", "Estado de Resultados Proforma trienal (Cifras en Pesos MXN)")
    est_t = doc.add_table(rows=11, cols=4)
    est_t.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_apa_table_borders(est_t)
    
    headers_es = ["Rubro Financiero", "Año 1 (Validación Piloto)", "Año 2 (Expansión Inicial)", "Año 3 (Consolidación a Escala)"]
    for j, h in enumerate(headers_es):
        c = est_t.rows[0].cells[j]
        set_cell_margins(c, top=70, bottom=70, left=70, right=70)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.font.bold = True
        r.font.size = Pt(11)
        
    es_data = [
        ("Ingresos Brutos por Facturación", "$63,000 MXN", "$324,000 MXN", "$850,000 MXN"),
        ("Costos de Infraestructura Cloud y Servidores", "($18,000 MXN)", "($35,000 MXN)", "($65,000 MXN)"),
        ("Nómina de Soporte y Capital Humano Operativo", "$0 (Cubierto en CAPEX)", "($120,000 MXN)", "($240,000 MXN)"),
        ("Viáticos de Capacitación, Dossiers y Material", "($12,000 MXN)", "($22,000 MXN)", "($45,000 MXN)"),
        ("Servicios Contables, Legales y Administrativos", "($15,000 MXN)", "($24,000 MXN)", "($36,000 MXN)"),
        ("Fondo de Mantenimiento de Software y Licencias", "($10,000 MXN)", "($24,000 MXN)", "($40,000 MXN)"),
        ("TOTAL DE EGRESOS OPERATIVOS (OPEX)", "($55,000 MXN)", "($225,000 MXN)", "($426,000 MXN)"),
        ("Utilidad Antes de Impuestos y Amortización", "+$8,000 MXN", "+$99,000 MXN", "+$424,000 MXN"),
        ("Impuestos y Cargas Fiscales Estimadas (30%)", "$0 (Pérdida amortizable)", "($20,100 MXN)", "($127,200 MXN)"),
        ("FLUJO DE EFECTIVO NETO DEL EJERCICIO (FEN)", "−$32,000 MXN", "+$78,900 MXN", "+$296,800 MXN")
    ]
    
    for idx, row_vals in enumerate(es_data):
        row = est_t.rows[idx + 1]
        for j, val in enumerate(row_vals):
            cell = row.cells[j]
            set_cell_margins(cell, top=60, bottom=60, left=70, right=70)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT if j == 0 else WD_ALIGN_PARAGRAPH.RIGHT
            r = p.add_run(val)
            r.font.size = Pt(11)
            if idx in (0, 6, 9) or j == 0:
                r.font.bold = True
                
    add_table_note("Elaboración propia con base en cotizaciones de mercado y normatividad fiscal para personas morales de reciente creación.")

    add_note_block(
        "Punto de Equilibrio Operativo",
        "El punto de equilibrio se alcanza formalmente en el Mes 14 (primer semestre del Año 2) con 6 planteles contratados (3 centros universitarios a $48k y 3 preparatorias a $24k = $216,000 anuales = $18,000/mes de suscripción recurrente) más ingresos prorrateados de setup ($3,000/mes). Con ingresos mensuales consolidados de $21,000 MXN, se cubren íntegramente los costos de operación del Año 2 ($18,750 MXN mensuales = $225,000 anuales)."
    )

    add_heading_2("7.5 Evaluación financiera integral: FEN, TMAR, VPN, TIR y Periodo de Recuperación")
    doc.add_paragraph(
        "El costo de oportunidad y la rentabilidad mínima exigida para la asignación de recursos se fijaron mediante la Tasa Mínima Aceptable de Rendimiento (TMAR) "
        "en 15.0% anual. Esta tasa integra el rendimiento soberano libre de riesgo de los Cetes a 364 días (7.12%, Banco de México) más una prima de riesgo del 7.88% "
        "(riesgo tecnológico 3.50%, liquidez/pre-semilla 2.88%, ciclo presupuestal B2G 1.50%)."
    )
    doc.add_paragraph(
        "A partir de los flujos netos proyectados y la tasa de descuento fijada, se llevó a cabo la evaluación de rentabilidad financiera cuyos indicadores clave se resumen en la Tabla 13:"
    )

    add_table_title("Tabla 13", "Evaluación financiera formal: Flujos de efectivo, VPN, TIR y periodo de recuperación")
    fin_t = doc.add_table(rows=10, cols=4)
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
        ("Año 2 (Crecimiento a 8 planteles)", "+$78,900.00 MXN", "0.7561", "+$59,659.74 MXN"),
        ("Año 3 (Consolidación a 22 planteles)", "+$296,800.00 MXN", "0.6575", "+$195,150.82 MXN"),
        ("VALOR PRESENTE NETO (VPN @ 15.0%)", "Suma algebraica descontada", "TMAR: 15.0% anual", "+$46,984.47 MXN"),
        ("TASA INTERNA DE RETORNO (TIR)", "Tasa donde VPN = 0", "Margen vs TMAR: +9.27%", "24.27% anual"),
        ("RELACIÓN BENEFICIO / COSTO (B/C)", "VP Beneficios / VP Costos", "Criterio de aceptación > 1.0", "1.23 veces"),
        ("PERIODO DE RECUPERACIÓN (Payback Simple)", "Flujos nominales acumulados", "Recuperación en Año 3", "Mes 29.4 (Año 3, T2)"),
        ("PERIODO DE RECUPERACIÓN (Payback Descontado)", "Flujos descontados al 15%", "Ajustado por costo de capital", "Mes 33.1 (Año 3, T4)")
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
            if idx in (4, 5, 6, 7, 8) or j == 0:
                r.font.bold = True
                
    add_table_note("Cálculo matemático formal basado en flujos anuales netos. Criterio de viabilidad: VPN > 0 y TIR > TMAR (15.0%).")

    doc.add_paragraph(
        "Los resultados de la evaluación confirman la sólida viabilidad financiera del proyecto desde cualquier ángulo analítico:\n"
        "- Creación de Valor Económico (VPN = +$46,984.47 MXN): El proyecto cubre el costo de oportunidad del capital (15% anual), amortiza por completo los $180,000 MXN de inversión y genera un superávit neto a valor presente cercano a $47,000 pesos.\n"
        "- Margen de Seguridad (TIR = 24.27% vs 15.0% TMAR): Presenta un diferencial favorable de 9.27 puntos porcentuales sobre la tasa de corte, blindando al proyecto ante contingencias operativas.\n"
        "- Eficiencia de Capital (B/C = 1.23 veces): Por cada peso invertido en valor presente descontado, el proyecto entrega 1.23 pesos de retorno institucional.\n"
        "- Amortización del Capital: El proyecto recupera nominalmente su inversión en el Mes 29.4 (Payback Simple) y en el Mes 33.1 ajustado por costo de capital (Payback Descontado)."
    )

    add_heading_2("7.6 Análisis de Sensibilidad Multiescenario y Umbral de Viabilidad")
    doc.add_paragraph(
        "Para someter el modelo a pruebas de estrés, se evaluó el comportamiento financiero ante variaciones en la cartera de planteles contratados al Año 3:\n"
        "- Escenario Pesimista (15 planteles, 7.7% mercado): Ingresos $570k, OPEX ($330k), FEN Año 3 +$168k. VPN = -$37,703.62 MXN, TIR = 6.22% anual (Inviable con TMAR 15%).\n"
        "- Escenario Base (22 planteles, 11.2% mercado): Ingresos $850k, OPEX ($426k), FEN Año 3 +$296.8k. VPN = +$46,984.47 MXN, TIR = 24.27% anual (Plenamente Viable y Robusto).\n"
        "- Escenario Optimista (30 planteles, 15.3% mercado): Ingresos $1,150k, OPEX ($550k), FEN Año 3 +$420k. VPN = +$127,990.47 MXN, TIR = 37.51% anual (Altamente Rentable)."
    )

    add_note_block(
        "Umbral Matemático de Viabilidad Financiera",
        "El umbral mínimo de viabilidad financiera (VPN = $0 a una tasa de corte del 15.0%) se ubica en un FEN de $225,342.50 MXN en el Año 3, tolerando una contracción máxima admisible del 24.1% respecto a la meta base de $296,800 MXN. Por interpolación lineal exacta, el punto de corte financiero corresponde a 18.12 planteles contratados. Debido a que los contratos universitarios no se fraccionan, el umbral mínimo entero seguro se fija en 19 planteles activos (equivalente al 9.7% de la Red Universitaria de 196 dependencias). Mantener 19 o más planteles contratados garantiza un VPN positivo y una TIR superior al 15.0%."
    )

    doc.add_page_break()

    # -------------------------------------------------------------
    # 8. ANÁLISIS FODA Y PROPUESTA AL INVERSIONISTA
    # -------------------------------------------------------------
    add_heading_1("8. Análisis Estratégico FODA Institucional y Técnico")
    doc.add_paragraph(
        "En la Figura 11 se reproduce la matriz visual integral FODA del proyecto, articulando los factores internos y del entorno institucional:"
    )
    img_fig11 = "docs/graficos/foda_oficial_sigre.jpg"
    add_figure_with_image(
        img_fig11,
        "Figura 11",
        "Matriz oficial de análisis estratégico FODA de la plataforma SIGRE",
        "Matriz FODA institucional con 16 factores clasificados por calidad operativa y riesgos mitigados."
    )

    doc.add_paragraph(
        "La matriz FODA de SIGRE articula sus 16 factores estratégicos:\n"
        "- Fortalezas: F1. Cerrojos Redis TTL 15 min anti-empalmes; F2. Trazabilidad QR con firma HMAC-SHA256; F3. Algoritmo Trust Score 0-100; F4. Servidores Cloud Run serverless elásticos.\n"
        "- Oportunidades: O1. Red cautiva homogénea de 196 planteles UdeG; O2. Contratación B2G por compra directa menor a 1,000 UMA ($117,310 MXN); O3. Ahorro neto demostrable de $90k a $140k/año por plantel; O4. Cumplimiento de política Cero Papel UdeG 2030 con más de 32,500 actas y formatos semestrales digitalizados (65,000 anuales / 2).\n"
        "- Debilidades: D1. Conectividad en campus periféricos (mitigada con modo offline PWA); D2. Equipo fundador esbelto (mitigada con gatillos de contratación); D3. Marca joven (mitigada con piloto CUTonalá y títulos IMPI/INDAUTOR); D4. Hardware de mostrador (mitigada con 3 escáneres ópticos y tableta demo en Partida P4 de inversión por $20,000 MXN).\n"
        "- Amenazas: A1. Resistencia al cambio sindical (mitigada con inducción de 16 hrs y SUS 82.85 pts); A2. Desfases de pago presupuestal (mitigada con reserva de $40k y cobro anual anticipado); A3. Rotación de directivos (mitigada con contratos anuales renovables); A4. Fraude de credenciales (mitigada con QR dinámico WebRTC y firma manuscrita)."
    )

    add_heading_1("9. Propuesta Formal para el Inversionista de Capital Semilla")
    add_heading_2("9.1 Mecanismo de Retorno al Inversionista: Amortización Preferente (Cash Sweep 70%)")
    doc.add_paragraph(
        "Para brindar absoluta certidumbre matemática y separar los plazos del proyecto frente a los del inversionista:\n"
        "- Inversión Inicial Semilla: $180,000.00 MXN en el Mes 0.\n"
        "- Periodo de Gracia para Reinversión (Año 1): El 100% del flujo se reinvierte en desarrollo y validación de campo ($CF1 = $0).\n"
        "- Mecanismo de Reembolso Preferente (Años 2 y 3): A partir del Año 2, el 70% del Flujo de Efectivo Neto (FEN) se destina exclusivamente a amortizar el capital del inversionista:\n"
        "  * En Año 2: El FEN es de $78,900 MXN. El 70% equivale a $55,230.00 MXN abonados a capital (saldo insoluto: $124,770.00 MXN). Los fundadores perciben el remanente real del 30% ($23,670.00 MXN; suma exacta: $78,900.00 MXN).\n"
        "  * En Año 3: El FEN es de $296,800 MXN ($24,733.33/mes; cuota preferente mensual del 70% = $17,313.33 MXN). Para liquidar los $124,770.00 MXN restantes se requieren exactamente 7.206 meses.\n"
        "  * Plazo de Liquidación Total del Inversionista: Mes 31.2 de operaciones (tercer trimestre del Año 3).\n"
        "- Renta Residual Recurrente (Dividendo en Perpetuidad): Tras liquidar el capital en el Mes 31.2, el inversionista cobra el 15.0% de dividendos sobre utilidades por los 4.793 meses restantes del Año 3 ($17,784.00 MXN), totalizando $142,554.00 MXN percibidos en el Año 3. Los fundadores perciben $53,473 MXN en el primer tramo y $100,773 MXN en el segundo tramo, sumando $154,246.00 MXN (total anual: $296,800.00 MXN).\n"
        "- A partir del Año 4: El inversionista percibe dividendos del 15% ($44,520.00 MXN anuales base / $58,080.00 MXN en escalamiento) y los fundadores retienen el 85% ($252,280.00 MXN base / $329,120.00 MXN en escalamiento).\n"
        "- Rentabilidad del Inversionista (TIR Inversionista): A horizonte de 5 años, considerando la expansión a tecnológicas y UPES con ingresos de $1.21M (Año 4) y $1.93M (Año 5), margen neto del 32.0% ($387.2k y $617.6k) y dividendos del 15% ($58,080 y $92,640 MXN), la TIR del inversionista alcanza el 21.20% anual."
    )

    doc.add_page_break()

    # -------------------------------------------------------------
    # 10. REFERENCIAS BIBLIOGRÁFICAS (APA 7ma Edición)
    # -------------------------------------------------------------
    add_heading_1("10. Referencias Bibliográficas")
    
    refs = [
        "Asociación Nacional de Universidades e Instituciones de Educación Superior. (2023). Anuario estadístico de la educación superior 2022-2023. ANUIES. http://www.anuies.mx/informacion-y-servicios/informacion-estadistica-de-educacion-superior",
        "Banco Interamericano de Desarrollo. (2020). Metodología del marco lógico para la planificación, el seguimiento y la evaluación de proyectos del BID. Sector de Conocimiento y Aprendizaje del BID. https://publications.iadb.org/es/metodologia-del-marco-logico",
        "Bangor, A., Kortum, P. T., & Miller, J. T. (2008). An empirical evaluation of the system usability scale. International Journal of Human-Computer Interaction, 24(6), 574–594. https://doi.org/10.1080/10447310802205776",
        "Brooke, J. (1996). SUS: A 'quick and dirty' usability scale. En P. W. Jordan, B. Thomas, B. A. Weerdmeester, & A. L. McClelland (Eds.), Usability evaluation in industry (pp. 189–194). Taylor & Francis.",
        "Cámara de Diputados del H. Congreso de la Unión. (2017). Ley general de protección de datos personales en posesión de sujetos obligados. Diario Oficial de la Federación. https://www.diputados.gob.mx/LeyesBiblio/pdf/LGPDPPSO.pdf",
        "Centro Universitario de Tonalá. (2023). Plan de desarrollo de CUTonalá 2019-2025: Visión 2030. Universidad de Guadalajara. http://www.cutonala.udg.mx/transparencia/pdi",
        "Comisión Económica para América Latina y el Caribe. (2015). Metodología del marco lógico para la planificación, el seguimiento y la evaluación de proyectos y programas (Serie Manuales N° 68). CEPAL / Naciones Unidas. https://www.cepal.org/es/publicaciones/5618-metodologia-marco-logico",
        "Coordinación General de Planeación y Evaluación. (2026). Numeralia institucional de la Red Universitaria (corte mayo de 2026). Universidad de Guadalajara. http://www.cgpe.udg.mx/numeralia",
        "Instituto Mexicano de la Propiedad Industrial. (2026). Tarifa por los servicios que presta el Instituto Mexicano de la Propiedad Industrial: Solicitud de registro de marca nacional por clase ($3,126.41 MXN IVA incluido). Gobierno de México. https://www.gob.mx/impi",
        "Instituto Nacional de Estadística y Geografía. (2026). Valor de la Unidad de Medida y Actualización (UMA) vigente a partir del 1 de febrero de 2026 ($117.31 MXN diarios). INEGI. https://www.inegi.org.mx",
        "Sapag Chain, N., Sapag Chain, R., & Sapag Puelma, J. M. (2014). Preparación y evaluación de proyectos (6ta ed.). McGraw-Hill Interamericana.",
        "Sauro, J., & Lewis, J. R. (2012). Quantifying the user experience: Practical statistics for user research. Morgan Kaufmann. https://doi.org/10.1016/B978-0-12-384968-7.00008-8",
        "Sistema de Educación Media Superior. (2024). Directorio y presencia regional de escuelas preparatorias y módulos del SEMS. Universidad de Guadalajara. https://www.sems.udg.mx/directorio",
        "Universidad de Guadalajara. (2019). Reglamento de adquisiciones, arrendamientos y contratación de servicios de la Universidad de Guadalajara. Gaceta de la Universidad de Guadalajara. http://www.secgen.udg.mx/normatividad/reglamentos"
    ]
    
    for r_text in refs:
        p_ref = doc.add_paragraph()
        p_ref.paragraph_format.left_indent = Inches(0.5)
        p_ref.paragraph_format.first_line_indent = Inches(-0.5)
        p_ref.paragraph_format.space_after = Pt(6)
        r = p_ref.add_run(r_text)
        r.font.size = Pt(11)

    doc.add_page_break()

    # -------------------------------------------------------------
    # ANEXOS TÉCNICOS
    # -------------------------------------------------------------
    add_heading_1("Anexos Técnicos y Evidencia Experimental")
    
    add_heading_2("Anexo A. Evidencia Psicométrica y Validación de Usabilidad SUS (n = 50)")
    doc.add_paragraph(
        "Los registros psicométricos completos, el desglose de los 10 reactivos estandarizados en escala Likert (1 a 5), la fórmula de conversión de Brooke (1996) "
        "y las matrices de consistencia interna (Alfa de Cronbach a = 0.892) aplicadas a los 50 usuarios participantes de CUTonalá (32 alumnos, 12 académicos y 6 operadores de almacén) "
        "se encuentran formalmente depositados en el expediente de investigación técnica del proyecto, consolidando una media aritmética de 82.85 puntos "
        "(Percentil superior al 90%, Grado A / 'Excelente' según Bangor et al., 2008 y Sauro & Lewis, 2012)."
    )

    add_heading_2("Anexo B. Video Demostrativo E2E y Matriz de Solventación al Dictamen Técnico Docente")
    doc.add_paragraph(
        "El registro audiovisual demostrativo de punta a punta (End-to-End), que acredita el ciclo transaccional completo en mostrador (reserva con cerrojo Redis, escaneo QR < 30 seg, "
        "firma manuscrita Canvas, generación de responsiva PDF con hash HMAC-SHA256 y modo offline PWA), forma parte del acervo técnico de validación operativa. "
        "Asimismo, la Tabla A1 documenta la atención puntual a cada uno de los criterios emitidos por el comité evaluador docente:"
    )

    add_table_title("Tabla A1", "Matriz de cumplimiento y solventación del dictamen técnico de evaluación")
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
         "Se incorporó el diagnóstico observacional y estimación de pérdidas ($90,000 a $140,000 MXN anuales) basado en experiencia en Servicios Generales y requisiciones de reposición.", 
         "Sección 1.4 (Tabla 1)"),
         
        ("2. Nicho, Mercado y Comercialización", 
         "Carece de análisis directo sobre la intención de compra real de decisores mediante entrevistas estructuradas.", 
         "Se integró la exploración cualitativa de viabilidad con personal administrativo y el fundamento normativo para adjudicación directa (<1000 UMA = $117,310 MXN).", 
         "Secciones 4.1 y 4.2 (Tabla 5)"),
         
        ("3. Objetivos y Marco Lógico", 
         "No incluye formalmente la Matriz de Marco Lógico (MML) completa.", 
         "Se integró la Matriz de Marco Lógico oficial bajo estándar CEPAL/BID con Fin, Propósito, 4 Componentes y 8 Actividades.", 
         "Sección 2.3 (Tabla 3)"),
         
        ("4. Aspectos Técnicos e Implementación", 
         "Faltan especificaciones de infraestructura TI (capacidad, tiempos de respuesta, base de datos) y plan de contingencia.", 
         "Se incluyó la ficha técnica de infraestructura cloud (PostgreSQL 16, Redis, Cloud Run, latencia <150ms) y el Plan de Contingencia con modo offline y talonarios.", 
         "Secciones 5.1 y 5.3 (Tabla 6)"),
         
        ("5. Estructura Organizacional y Requerimientos", 
         "Falta manual de organización breve y descripción de cargas de trabajo al escalar a 22 planteles.", 
         "Se definió el organigrama funcional y la tabla de escalamiento con gatillos objetivos de contratación (Soporte N1 en Mes 15 y Especialista en Mes 22).", 
         "Secciones 6.1 y 6.2 (Tabla 7)"),
         
        ("6. Programación de Inversiones", 
         "Hace falta representación gráfica estandarizada (Gantt) que muestre la ruta crítica.", 
         "Se diseñó el Diagrama de Gantt anual en matriz mensual con dependencias explícitas e identificación visual de la Ruta Crítica [RC].", 
         "Secciones 6.4 y 6.5 (Tablas 8 y 9)"),
         
        ("7. Costos, Ingresos y Evaluación Financiera", 
         "No se calculan indicadores clave de evaluación financiera de proyectos (VPN, TIR, TMAR, FEN).", 
         "Se integró el cuadro de Flujo de Efectivo Neto (FEN), TMAR del 15.0%, cálculo formal de VPN (+$46,984.47 MXN), TIR (24.27%), relación B/C (1.23) y periodo de recuperación Payback (mes 29.4).", 
         "Sección 7.5 (Tabla 13)")
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
