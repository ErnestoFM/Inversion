# -*- coding: utf-8 -*-
"""
Genera la versión Word (.docx) limpia de la Matriz FODA:
Solo título sencillo "FODA" y el cuadro 2x2.
"""

import os
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import nsdecls
from docx.oxml import parse_xml

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "docs")
OUTPUT_DOCX = os.path.join(OUTPUT_DIR, "FODA_SIGRE_CUTonala.docx")

def set_cell_shading(cell, hex_color):
    shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}" w:val="clear"/>')
    cell._tc.get_or_add_tcPr().append(shading)

def set_cell_margins(cell, top=100, bottom=100, left=120, right=120):
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

def generate_foda_docx():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    doc = Document()

    # Configurar apaisado (Landscape)
    section = doc.sections[0]
    new_width, new_height = section.page_height, section.page_width
    section.page_width = new_width
    section.page_height = new_height
    section.top_margin = Cm(1.6)
    section.bottom_margin = Cm(1.6)
    section.left_margin = Cm(1.6)
    section.right_margin = Cm(1.6)

    # Título muy sencillo: "FODA"
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(0)
    p_title.paragraph_format.space_after = Pt(8)
    run_t = p_title.add_run("FODA")
    run_t.font.name = "Calibri"
    run_t.font.size = Pt(20)
    run_t.font.bold = True
    run_t.font.color.rgb = RGBColor(0x00, 0x2B, 0x49) # Azul Institucional UdeG

    # Matriz 2x2
    foda_table = doc.add_table(rows=2, cols=2)
    foda_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    foda_table.style = 'Table Grid'

    col_w = Cm(12.7)

    quadrants = [
        # Fila 0, Col 0: Fortalezas
        (0, 0, "💪 FORTALEZAS (F) — Factores Internos de Calidad y Control", "2E7D57", "F0FDF4", [
            ("F1. Mecanismo Anti-Empalme con Redis Locks (TTL 900s)",
             "Garantiza atomicidad y disponibilidad 99.9% en reservas de aulas/auditorios, impidiendo colisiones horarias concurrentes.",
             "[Calidad: Confiabilidad y Concurrencia]", "[Riesgo Mitigado: Doble Agendamiento]"),
            ("F2. Trazabilidad Digital con QR HMAC y Firma Manuscrita Base64",
             "Cadena de custodia digital e inmutable para préstamos de equipo, eliminando vicios de vales en papel.",
             "[Calidad: Integridad y Trazabilidad]", "[Riesgo Mitigado: Extravío Patrimonial]"),
            ("F3. Sistema de Reputación 'Trust Score' Algorítmico (Base 100)",
             "Monitorea el cumplimiento en devoluciones; penaliza demoras y bloquea preventivamente a usuarios infractores.",
             "[Calidad: Control de Servicio]", "[Riesgo Mitigado: Morosidad y Daño Material]"),
            ("F4. Eficiencia Financiera Validada (CAPEX $140k / OPEX $28.8k)",
             "Retorno Payback en mes 29.6 y TIR de 21.34% frente a ERPs de $350k+. Ahorro institucional proyectado de +$100,000/año.",
             "[Calidad: Eficiencia de Costos]", "[Riesgo Mitigado: Inviabilidad Financiera]"),
        ]),
        # Fila 0, Col 1: Oportunidades
        (0, 1, "🚀 OPORTUNIDADES (O) — Factores Externos de Crecimiento y Ahorro", "002B49", "F0F7FF", [
            ("O1. Escalamiento Natural a la Red Universitaria UdeG",
             "Capacidad de expansión modular hacia otros centros temáticos y regionales (CUCEI, CUAAD, CUCS) con el mismo problema.",
             "[Calidad: Escalabilidad Arquitectónica]", "[Riesgo Mitigado: Techo de Mercado Local]"),
            ("O2. Acceso a Fondos de Innovación y Microfinanciamiento",
             "Elegibilidad para capital semilla sin intereses (Kiva al 0% APR) y fondos de fomento tecnocientífico estatal (FODECIJAL).",
             "[Calidad: Sustentabilidad Económica]", "[Riesgo Mitigado: Asfixia por Deuda Bancaria]"),
            ("O3. Sustitución de Mermas Históricas por Ahorro Comprobado",
             "El ahorro de $100k+ anuales en pérdidas de laptops y proyectores cubre 3.5x el OPEX anual de la plataforma.",
             "[Calidad: Retorno de Inversión Institucional]", "[Riesgo Mitigado: Rechazo Presupuestal]"),
            ("O4. Alineación con Políticas Institucionales 'Cero Papel'",
             "Cumplimiento directo con la agenda de sustentabilidad UdeG 2030, digitalizando más de 12,000 actas físicas al semestre.",
             "[Calidad: Sustentabilidad y Cumplimiento]", "[Riesgo Mitigado: Incompatibilidad Normativa]"),
        ]),
        # Fila 1, Col 0: Debilidades
        (1, 0, "⚠️ DEBILIDADES (D) — Factores Internos a Mitigar en Fase Semilla", "B45309", "FFFBEB", [
            ("D1. Dependencia de Conectividad de Red en Ventanillas de Almacén",
             "Caídas imprevistas del enlace institucional pueden suspender la validación en tiempo real si no opera caché offline.",
             "[Calidad: Continuidad Operativa]", "[Riesgo Crítico: Cuellos de Botella Físicos]"),
            ("D2. Equipo Nuclear Reducido en Fase Semilla (Riesgo Clave)",
             "Concentración del know-how técnico en un equipo de desarrollo inicial, requiriendo manuales y contingencias técnicas.",
             "[Calidad: Mantenibilidad del Código]", "[Riesgo Crítico: Dependencia Técnica y Cuellos de Soporte]"),
            ("D3. Inexistencia de Historial Crediticio Comercial Formal",
             "Como startup universitaria en fase temprana, carece de balances auditados de 2+ años, limitando el crédito bancario clásico.",
             "[Calidad: Madurez Corporativa]", "[Riesgo Crítico: Restricción de Liquidez Bancaria]"),
            ("D4. Requerimiento de Hardware Físico en Mostradores (Partida P3)",
             "La agilidad del check-in depende de adquirir 3 escáneres 2D y 1 tableta ($20,000 MXN) previo al arranque del ciclo.",
             "[Calidad: Nivel de Servicio en Mostrador]", "[Riesgo Crítico: Dependencia de Compra Inicial]"),
        ]),
        # Fila 1, Col 1: Amenazas
        (1, 1, "🛡️ AMENAZAS (A) — Factores Externos y Riesgos de Entorno", "B91C1C", "FEF2F2", [
            ("A1. Resistencia al Cambio de Almacenistas y Personal Operativo",
             "Renuencia del personal de base a transitar del libro de firmas analógico a tabletas digitales y escaneo QR diario.",
             "[Calidad: Aceptación Tecnológica]", "[Riesgo Crítico: Boicot y Omisión de Checklists]"),
            ("A2. Tiempos Burocráticos en Órdenes de Compra y Pagos UdeG",
             "Ciclos de dispersión presupuestal semestrales lentos que pueden diferir el pago de infraestructura cloud o soporte.",
             "[Calidad: Liquidez de Operación]", "[Riesgo Crítico: Suspensión por Facturación Tardía]"),
            ("A3. Volatilidad Cambiaria USD/MXN en Facturación Nube (GCP)",
             "Costos de Cloud Run, PostgreSQL y Redis facturados en USD sujetos a depreciación cambiaria frente al peso mexicano.",
             "[Calidad: Previsión Financiera]", "[Riesgo Crítico: Incremento de Costos por Tipo de Cambio]"),
            ("A4. Daño Severo o Pérdida Extrema de Equipo por Usuarios",
             "Incidentes donde el costo del bien siniestrado (cámara de cine, proyector láser) supere la solvencia inmediata del custodio.",
             "[Calidad: Resguardo Patrimonial]", "[Riesgo Crítico: Pérdida Irrecuperable sin Fianza Previa]"),
        ]),
    ]

    for row_idx, col_idx, card_title, head_hex, bg_hex, items in quadrants:
        cell = foda_table.rows[row_idx].cells[col_idx]
        cell.width = col_w
        set_cell_margins(cell, 80, 80, 100, 100)
        set_cell_shading(cell, bg_hex)

        p_h = cell.paragraphs[0]
        p_h.paragraph_format.space_before = Pt(0)
        p_h.paragraph_format.space_after = Pt(4)
        run_h = p_h.add_run(card_title)
        run_h.font.name = "Calibri"
        run_h.font.size = Pt(8.8)
        run_h.font.bold = True
        run_h.font.color.rgb = RGBColor.from_string(head_hex)

        for title, desc, tag_c, tag_r in items:
            p_item = cell.add_paragraph()
            p_item.paragraph_format.space_before = Pt(2)
            p_item.paragraph_format.space_after = Pt(2)
            p_item.paragraph_format.line_spacing = 1.05

            run_it = p_item.add_run(f"{title}\n")
            run_it.font.name = "Calibri"
            run_it.font.size = Pt(7.8)
            run_it.font.bold = True
            run_it.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)

            run_id = p_item.add_run(f"{desc}\n")
            run_id.font.name = "Calibri"
            run_id.font.size = Pt(7.0)
            run_id.font.color.rgb = RGBColor(0x33, 0x41, 0x55)

            run_tc = p_item.add_run(tag_c)
            run_tc.font.name = "Calibri"
            run_tc.font.size = Pt(6.5)
            run_tc.font.bold = True
            run_tc.font.color.rgb = RGBColor(0x2E, 0x7D, 0x57)

            run_pipe = p_item.add_run(" | ")
            run_pipe.font.size = Pt(6.5)
            run_pipe.font.color.rgb = RGBColor(0x94, 0xA3, 0xB8)

            run_tr = p_item.add_run(tag_r)
            run_tr.font.name = "Calibri"
            run_tr.font.size = Pt(6.5)
            run_tr.font.bold = True
            run_tr.font.color.rgb = RGBColor(0xB9, 0x1C, 0x1C)

    doc.save(OUTPUT_DOCX)
    print(f"✅ Documento Word FODA limpio generado: {OUTPUT_DOCX}")

if __name__ == "__main__":
    generate_foda_docx()
