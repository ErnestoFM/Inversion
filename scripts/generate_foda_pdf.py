# -*- coding: utf-8 -*-
"""
Generador del Documento PDF: Matriz FODA Ejecutiva de SIGRE (1 Página Landscape).
Versión Minimalista: Solo título "FODA" y la matriz 2x2 limpia y legible.
"""

import os
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
)
from reportlab.pdfgen import canvas

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "docs")
OUTPUT_PDF = os.path.join(OUTPUT_DIR, "FODA_SIGRE_CUTonala.pdf")

# ─────────────────────────────────────────────────────────────
# PALETA DE COLORES OFICIAL DE SIGRE
# ─────────────────────────────────────────────────────────────
HEX_AZUL_INSTITUCIONAL = colors.HexColor("#002B49")   # UdeG Navy
HEX_VERDE_NATURAL      = colors.HexColor("#2E7D57")   # SIGRE Green
HEX_TEAL_PROFUNDO      = colors.HexColor("#1A6B5A")   # Deep Teal
HEX_AMBAR_ALERTA       = colors.HexColor("#B45309")   # Amber / Orange
HEX_ROJO_RIESGO        = colors.HexColor("#B91C1C")   # Crimson Red

# Fondos de tarjetas
HEX_BG_FORTALEZA   = colors.HexColor("#F0FDF4") # Verde suave
HEX_BG_OPORTUNIDAD = colors.HexColor("#F0F7FF") # Azul suave
HEX_BG_DEBILIDAD   = colors.HexColor("#FFFBEB") # Ámbar suave
HEX_BG_AMENAZA     = colors.HexColor("#FEF2F2") # Rojo suave

# Bordes
HEX_BORDER_F = colors.HexColor("#86EFAC")
HEX_BORDER_O = colors.HexColor("#BAE6FD")
HEX_BORDER_D = colors.HexColor("#FDE68A")
HEX_BORDER_A = colors.HexColor("#FECACA")

# Texto
HEX_TEXT_DARK   = colors.HexColor("#0F172A")
HEX_TEXT_MUTED  = colors.HexColor("#475569")


class MinimalCanvas(canvas.Canvas):
    """Canvas minimalista para 1 sola página."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            super().showPage()
        super().save()


def build_foda_pdf():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # 792 x 612 pt (Letter Landscape)
    doc = SimpleDocTemplate(
        OUTPUT_PDF,
        pagesize=landscape(letter),
        leftMargin=24,
        rightMargin=24,
        topMargin=20,
        bottomMargin=20,
    )

    styles = getSampleStyleSheet()

    # Título simple "FODA"
    foda_title_style = ParagraphStyle(
        "SimpleFODATitle",
        fontName="Helvetica-Bold",
        fontSize=18,
        leading=22,
        textColor=HEX_AZUL_INSTITUCIONAL,
        alignment=1, # Centrado
        spaceAfter=10,
    )

    card_title_style = ParagraphStyle(
        "CardTitle",
        fontName="Helvetica-Bold",
        fontSize=9.5,
        leading=12,
        textColor=colors.white,
    )
    
    item_body_style = ParagraphStyle(
        "ItemBody",
        fontName="Helvetica",
        fontSize=7.1,
        leading=8.7,
        textColor=HEX_TEXT_MUTED,
    )

    story = []

    # 1. Título muy sencillito: solo "FODA"
    story.append(Paragraph("<b>FODA</b>", foda_title_style))
    story.append(Spacer(1, 4))

    # 2. Datos de los 4 cuadrantes
    fortalezas_data = [
        ("F1. Mecanismo Anti-Empalme con Redis Locks (TTL 900s)",
         "Garantiza atomicidad estricta y disponibilidad 99.9% en reservas de aulas y auditorios, impidiendo colisiones horarias concurrentes.",
         "[Calidad: Confiabilidad y Concurrencia]", "[Riesgo Mitigado: Doble Agendamiento y Parálisis Operativa]"),
        ("F2. Trazabilidad Digital con QR HMAC y Firma Manuscrita Base64",
         "Cadena de custodia 100% digital e inmutable para préstamos de equipo, eliminando vicios de vales en papel y pérdida de responsables.",
         "[Calidad: Integridad y Trazabilidad]", "[Riesgo Mitigado: Fraude, Extravío Patrimonial y Falsificación]"),
        ("F3. Sistema de Reputación 'Trust Score' Algorítmico (Base 100)",
         "Monitorea el cumplimiento en devoluciones; penaliza demoras y bloquea preventivamente a usuarios infractores protegiendo el inventario.",
         "[Calidad: Control de Servicio]", "[Riesgo Mitigado: Morosidad y Deterioro No Reparado de Activos]"),
        ("F4. Eficiencia Financiera Validada (CAPEX $140k / OPEX $28.8k)",
         "Retorno Payback en mes 29.6 y TIR de 21.34% frente a ERPs de $350k+. Ahorro institucional proyectado de +$100,000 MXN/año en mermas.",
         "[Calidad: Eficiencia de Costos]", "[Riesgo Mitigado: Inviabilidad Financiera y Sobrecostos de Licencia]")
    ]

    oportunidades_data = [
        ("O1. Escalamiento Natural a la Red Universitaria UdeG",
         "Capacidad de expansión modular hacia otros centros temáticos y regionales (CUCEI, CUAAD, CUCS) que padecen el mismo descontrol analógico.",
         "[Calidad: Escalabilidad Arquitectónica]", "[Riesgo Mitigado: Techo de Mercado Local y Subutilización]"),
        ("O2. Acceso a Fondos de Innovación y Microfinanciamiento",
         "Elegibilidad para capital semilla sin intereses (Kiva al 0% APR) y fondos de fomento tecnocientífico estatal (FODECIJAL / COECYTJAL).",
         "[Calidad: Sustentabilidad Económica]", "[Riesgo Mitigado: Asfixia Financiera por Deuda Bancaria Temprana]"),
        ("O3. Sustitución de Mermas Históricas por Ahorro Comprobado",
         "Argumento directivo contundente: el ahorro de $100k+ anuales en pérdidas de laptops y proyectores cubre 3.5x el OPEX anual de la plataforma.",
         "[Calidad: Retorno de Inversión Institucional]", "[Riesgo Mitigado: Rechazo Presupuestal en Secretaría Administrativa]"),
        ("O4. Alineación con Políticas Institucionales 'Cero Papel'",
         "Cumplimiento directo con la agenda de sustentabilidad UdeG 2030, digitalizando más de 12,000 actas y formatos físicos al semestre.",
         "[Calidad: Sustentabilidad y Cumplimiento]", "[Riesgo Mitigado: Descarte por Incompatibilidad Normativa]")
    ]

    debilidades_data = [
        ("D1. Dependencia de Conectividad de Red en Ventanillas de Almacén",
         "Caídas imprevistas del enlace de internet institucional pueden suspender la validación en tiempo real si no opera el caché offline.",
         "[Calidad: Continuidad Operativa]", "[Riesgo Crítico: Cuellos de Botella Físicos en Entregas Masivas]"),
        ("D2. Equipo Nuclear Reducido en Fase Semilla (Riesgo Clave)",
         "Concentración del know-how técnico en un equipo de desarrollo inicial, requiriendo manuales exhaustivos y planes de contingencia técnica.",
         "[Calidad: Mantenibilidad del Código]", "[Riesgo Crítico: Dependencia Técnica y Respuesta Lenta ante Bugs]"),
        ("D3. Inexistencia de Historial Crediticio Comercial Formal",
         "Como startup universitaria en fase temprana, carece de balances fiscales auditados de 2+ años, limitando el crédito bancario comercial tradicional.",
         "[Calidad: Madurez Corporativa]", "[Riesgo Crítico: Restricción de Liquidez Bancaria en Etapa Temprana]"),
        ("D4. Requerimiento de Hardware Físico en Mostradores (Partida P3)",
         "La agilidad del check-in depende de adquirir 3 escáneres ópticos 2D industriales y 1 tableta ($20,000 MXN) previo al arranque del ciclo escolar.",
         "[Calidad: Nivel de Servicio en Mostrador]", "[Riesgo Crítico: Dependencia de Compra de Hardware Inicial]")
    ]

    amenazas_data = [
        ("A1. Resistencia al Cambio de Almacenistas y Personal Operativo",
         "Renuencia del personal de base a transitar del libro de firmas analógico a tabletas digitales y escaneo QR en cada cambio de turno.",
         "[Calidad: Aceptación Tecnológica]", "[Riesgo Crítico: Boicot Operativo y Omisión de Checklists de Retorno]"),
        ("A2. Tiempos Burocráticos en Órdenes de Compra y Pagos UdeG",
         "Ciclos de dispersión presupuestal semestrales lentos que pueden diferir el pago de infraestructura de servidores o mantenimiento.",
         "[Calidad: Liquidez de Operación]", "[Riesgo Crítico: Suspensión de Servidores por Retraso en Facturación]"),
        ("A3. Volatilidad Cambiaria USD/MXN en Facturación Nube (GCP)",
         "Costos de Cloud Run, PostgreSQL y Redis facturados en USD sujetos a depreciación cambiaria imprevista frente al peso mexicano.",
         "[Calidad: Previsión Financiera]", "[Riesgo Crítico: Incremento de Costos Fijos por Tipo de Cambio FIX]"),
        ("A4. Daño Severo o Pérdida Extrema de Equipo por Usuarios",
         "Incidentes donde el costo del bien siniestrado (cámara de cine, proyector láser) supere la capacidad de pago inmediata del estudiante custodio.",
         "[Calidad: Resguardo Patrimonial]", "[Riesgo Crítico: Pérdida Irrecuperable sin Fianza Previa del Activo]")
    ]

    def create_quadrant_card(title_text, header_bg, card_bg, border_color, items):
        header_p = Paragraph(f"<b>{title_text}</b>", card_title_style)
        
        content_rows = []
        for title, desc, tag_c, tag_r in items:
            cell_text = (
                f"<font name='Helvetica-Bold' size='8.0' color='#0F172A'>{title}</font><br/>"
                f"<font name='Helvetica' size='7.0' color='#334155'>{desc}</font><br/>"
                f"<font name='Helvetica-Bold' size='6.3' color='{HEX_VERDE_NATURAL.hexval()}'>{tag_c}</font> "
                f"<font size='6.0' color='#94A3B8'>|</font> "
                f"<font name='Helvetica-Bold' size='6.3' color='{HEX_ROJO_RIESGO.hexval()}'>{tag_r}</font>"
            )
            p = Paragraph(cell_text, item_body_style)
            content_rows.append([p])

        inner_table = Table(content_rows, colWidths=[360])
        inner_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 4),
            ('RIGHTPADDING', (0, 0), (-1, -1), 4),
            ('TOPPADDING', (0, 0), (-1, -1), 3.5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5),
            ('LINEBELOW', (0, 0), (-1, -2), 0.4, colors.HexColor("#E2E8F0")),
        ]))

        card = Table([
            [header_p],
            [inner_table]
        ], colWidths=[368])
        
        card.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, 0), header_bg),
            ('BACKGROUND', (0, 1), (0, 1), card_bg),
            ('BOX', (0, 0), (-1, -1), 1.0, border_color),
            ('TOPPADDING', (0, 0), (0, 0), 5),
            ('BOTTOMPADDING', (0, 0), (0, 0), 5),
            ('LEFTPADDING', (0, 0), (0, 0), 8),
            ('RIGHTPADDING', (0, 0), (0, 0), 8),
            ('TOPPADDING', (0, 1), (0, 1), 3),
            ('BOTTOMPADDING', (0, 1), (0, 1), 3),
            ('LEFTPADDING', (0, 1), (0, 1), 4),
            ('RIGHTPADDING', (0, 1), (0, 1), 4),
        ]))
        return card

    card_f = create_quadrant_card(
        "💪 FORTALEZAS (F) — Factores Internos de Calidad y Control",
        HEX_VERDE_NATURAL, HEX_BG_FORTALEZA, HEX_BORDER_F, fortalezas_data
    )
    
    card_o = create_quadrant_card(
        "🚀 OPORTUNIDADES (O) — Factores Externos de Crecimiento y Ahorro",
        HEX_AZUL_INSTITUCIONAL, HEX_BG_OPORTUNIDAD, HEX_BORDER_O, oportunidades_data
    )

    card_d = create_quadrant_card(
        "⚠️ DEBILIDADES (D) — Factores Internos a Mitigar en Fase Semilla",
        HEX_AMBAR_ALERTA, HEX_BG_DEBILIDAD, HEX_BORDER_D, debilidades_data
    )

    card_a = create_quadrant_card(
        "🛡️ AMENAZAS (A) — Factores Externos y Riesgos de Entorno Institucional",
        HEX_ROJO_RIESGO, HEX_BG_AMENAZA, HEX_BORDER_A, amenazas_data
    )

    matrix_table = Table([
        [card_f, card_o],
        [card_d, card_a]
    ], colWidths=[372, 372])

    matrix_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 2),
        ('RIGHTPADDING', (0, 0), (-1, -1), 2),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))

    story.append(matrix_table)

    doc.build(story, canvasmaker=MinimalCanvas)
    print(f"✅ PDF limpio generado exitosamente: {OUTPUT_PDF}")


if __name__ == "__main__":
    build_foda_pdf()
