# -*- coding: utf-8 -*-
"""
Genera la versión corregida y compacta (máx. 5 páginas) del documento Word:
"Fuentes_Financiamiento_SIGRE_2.docx".
Aplica estrictamente las 5 correcciones requeridas:
1. Reconciliación de los $12,800 MXN de OPEX Año 1 (Total Año 1: $152,800 MXN).
2. Servicio de la deuda (amortización Kiva $2,111.11/mes y Upstart $1,374.74-$2,015.12/mes).
3. Precisión de plan gratuito ($0 USD/mes) en EquityNet.
4. Numeración formal de partidas P1 a P8 y ajuste de título de software en P1.
5. Nota de alcance geográfico de Merchant Maverick en la introducción de la Sección 3.
Enlace Merchant Maverick afiliado para EquityNet sin [VERIFICAR]; conservación intacta de todos los demás [VERIFICAR].
"""

from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import nsdecls
from docx.oxml import parse_xml
import os

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "docs")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "Fuentes_Financiamiento_SIGRE_2.docx")

def set_cell_shading(cell, hex_color):
    shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}" w:val="clear"/>')
    cell._tc.get_or_add_tcPr().append(shading)

def set_cell_margins(cell, top=60, bottom=60, left=100, right=100):
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

def add_styled_table(doc, headers, rows, col_widths=None):
    table = doc.add_table(rows=1 + len(rows), cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.style = "Table Grid"

    for i, h in enumerate(headers):
        cell = table.rows[0].cells[i]
        cell.text = ""
        set_cell_margins(cell, top=80, bottom=80, left=100, right=100)
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.05
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(h)
        run.bold = True
        run.font.size = Pt(8.5)
        run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        run.font.name = "Calibri"
        set_cell_shading(cell, "2F5496")

    for r_idx, row_data in enumerate(rows):
        for c_idx, val in enumerate(row_data):
            cell = table.rows[r_idx + 1].cells[c_idx]
            cell.text = ""
            set_cell_margins(cell, top=60, bottom=60, left=80, right=80)
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.05
            run = p.add_run(str(val))
            run.font.size = Pt(8.0)
            run.font.name = "Calibri"
            if r_idx % 2 == 1:
                set_cell_shading(cell, "F2F4F8")

    if col_widths:
        for r in table.rows:
            for i, w in enumerate(col_widths):
                r.cells[i].width = Cm(w)

    p_spacer = doc.add_paragraph()
    p_spacer.paragraph_format.space_before = Pt(0)
    p_spacer.paragraph_format.space_after = Pt(4)
    return table

def heading(doc, text, level=1):
    h = doc.add_heading(text, level=level)
    h.paragraph_format.keep_with_next = True
    if level == 1:
        h.paragraph_format.space_before = Pt(10)
        h.paragraph_format.space_after = Pt(3)
        for run in h.runs:
            run.font.name = "Calibri"
            run.font.size = Pt(13)
            run.font.bold = True
            run.font.color.rgb = RGBColor(0x1F, 0x38, 0x64)
    elif level == 2:
        h.paragraph_format.space_before = Pt(6)
        h.paragraph_format.space_after = Pt(2)
        for run in h.runs:
            run.font.name = "Calibri"
            run.font.size = Pt(11)
            run.font.bold = True
            run.font.color.rgb = RGBColor(0x2F, 0x54, 0x96)
    return h

def para(doc, text, bold_prefix=None):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.10
    if bold_prefix:
        run_b = p.add_run(bold_prefix)
        run_b.bold = True
        run_b.font.size = Pt(10)
        run_b.font.name = "Calibri"
    run = p.add_run(text)
    run.font.size = Pt(10)
    run.font.name = "Calibri"
    return p

# ──────────────────────────────────────────────
# Construcción del Documento
# ──────────────────────────────────────────────

doc = Document()

style = doc.styles["Normal"]
style.font.name = "Calibri"
style.font.size = Pt(10)
style.paragraph_format.space_after = Pt(4)
style.paragraph_format.line_spacing = 1.10

# Márgenes estándar compactos (2.0 cm) para asegurar ajuste perfecto en <= 5 páginas
for section in doc.sections:
    section.top_margin = Cm(2.0)
    section.bottom_margin = Cm(2.0)
    section.left_margin = Cm(2.0)
    section.right_margin = Cm(2.0)

# ═══════════════════════════════════════════════
# SECCIÓN 1: PERFIL DEL INVERSOR IDEAL
# ═══════════════════════════════════════════════

heading(doc, "1. Perfil y Características del Inversor Ideal", level=1)

para(doc, (
    "SIGRE (Sistema Integrado de Gestión de Recursos y Espacios) es un proyecto tecnológico en etapa temprana "
    "desarrollado en el Centro Universitario de Tonalá de la Universidad de Guadalajara (Universidad de Guadalajara, 2026). "
    "Como plataforma orientada al sector educativo e institucional, su modelo no genera retornos explosivos inmediatos, "
    "sino valor mediante ahorro presupuestal y mitigación de pérdidas patrimoniales. Por ello, el perfil de inversor idóneo "
    "no corresponde a la banca comercial tradicional —que exige garantías reales y balances auditados—, sino a plataformas "
    "alternativas para startups catalogadas por Merchant Maverick (2026), basadas en viabilidad técnica y esquemas flexibles. "
    "Para contrastar preliminarmente los criterios crediticios aplicables a la escala del proyecto, se utilizó como apoyo analítico "
    "el modelo de lenguaje Gemini (Google, 2026). A partir de dicha evaluación, se definen cinco características esenciales:"
))

heading(doc, "1.1 Características del Inversor Adecuado", level=2)

chars = [
    (
        "1. Tolerancia al riesgo en etapa semilla sin historial comercial extenso. ",
        "SIGRE se encuentra en fase inicial de validación operativa (Universidad de Guadalajara, 2026). El financiador "
        "debe operar bajo modelos de suscripción no tradicionales —evaluación algorítmica o respaldo social comunitario "
        "(Merchant Maverick, 2026)— donde la pertinencia técnica y el equipo prevalecen sobre el historial fiscal."
    ),
    (
        "2. Flexibilidad en esquemas de retorno y amortización. ",
        "La liquidez inicial debe concentrarse en activos críticos. El inversor debe admitir esquemas de micro-crowdfunding "
        "al 0% de interés como Kiva (2026), plazos diferidos a 36-60 meses, o financiamiento colectivo de capital donde la "
        "retribución se vincule al crecimiento patrimonial y no a pagos fijos inmediatos que ahoguen el flujo de caja."
    ),
    (
        "3. Estructura de costos financieros transparente y competitiva. ",
        "Para un presupuesto inicial externo de $140,000 MXN (Universidad de Guadalajara, 2026), comisiones ocultas o tasas APR "
        "predatorias comprometerían el proyecto. Se exigen comisiones de apertura (origination fees) y tasas de interés "
        "plenamente delimitadas desde la solicitud, estándar rigurosamente evaluado por Merchant Maverick (2026)."
    ),
    (
        "4. Agilidad en tiempos de aprobación y desembolso de liquidez. ",
        "El despliegue obedece a un calendario académico semestral estricto. Procesos burocráticos mayores a tres meses resultan "
        "inviables. Se requiere una entidad que apruebe y transfiera fondos en plazos de entre 48 horas y 30 días naturales."
    ),
    (
        "5. Aporte de valor estratégico y red de validación (Smart Money). ",
        "Más allá del capital líquido, el canal de financiamiento debe aportar tracción, visibilidad y acceso a redes de mentores "
        "e inversionistas ángeles (Merchant Maverick, 2026), facilitando el escalamiento posterior a otros campus de la Red UdeG."
    ),
]

for bold_part, body in chars:
    para(doc, body, bold_prefix=bold_part)

# ═══════════════════════════════════════════════
# SECCIÓN 2: ANÁLISIS COMPARATIVO
# ═══════════════════════════════════════════════

heading(doc, "2. Análisis Comparativo: Del Financiamiento Personal al Formal según el Tamaño del Proyecto", level=1)

para(doc, (
    "El acceso a recursos financieros evoluciona de manera paralela a la madurez del proyecto. En la formulación de proyectos "
    "de inversión, categorizar las alternativas permite seleccionar el instrumento adecuado, mitigando el sobreendeudamiento "
    "o la dilución anticipada de la propiedad intelectual."
))

heading(doc, "2.1 Financiamiento Personal / Bootstrapping / FFF y Tarjetas a Meses sin Intereses", level=2)

para(doc, (
    "En la fase de concepción, la fuente inmediata es el capital de los fundadores, el círculo cercano (Friends, Family & Fools) "
    "y tarjetas a meses sin intereses. Para SIGRE, esta modalidad posibilitó los primeros ensayos de servidores y prototipos "
    "de código (Universidad de Guadalajara, 2026). Su ventaja es la inmediatez sin burocracia, pero su alcance es limitado "
    "(montos menores a $30,000 MXN) y concentra el riesgo total en el patrimonio del estudiante o desarrollador."
))

heading(doc, "2.2 Convocatorias y Plataformas de Capital Semilla Alternativo", level=2)

para(doc, (
    "Hacia la validación del Producto Mínimo Viable (MVP), surgen esquemas de financiamiento colaborativo analizados por "
    "Merchant Maverick (2026), tales como micropréstamos comunitarios al 0% de interés o plataformas de inversión ángel. "
    "Eliminan el servicio de deuda oneroso y validan el interés de la comunidad previo al escalamiento, requiriendo un plan "
    "de negocio estructurado y validación pública."
))

heading(doc, "2.3 Financiamiento Formal y Líneas de Crédito Online para Startups", level=2)

para(doc, (
    "El nivel formal comprende prestamistas en línea evaluados por Merchant Maverick (2026). Miden variables objetivas: puntaje "
    "crediticio, antigüedad comercial, facturación e ingresos comprobables, APR y velocidad de fondeo. Para startups en fase temprana "
    "que carecen de historial bancario tradicional, las fintechs con modelos algorítmicos representan la vía formal para financiar "
    "hardware y activos indispensables de puesta en marcha."
))

# ═══════════════════════════════════════════════
# SECCIÓN 3: PROPUESTA Y JUSTIFICACIÓN DE 3 FUENTES
# ═══════════════════════════════════════════════

heading(doc, "3. Propuesta y Justificación de Tres Fuentes de Financiamiento", level=1)

para(doc, (
    "Con base estricta en el catálogo de revisiones para startups de Merchant Maverick (2026), se seleccionaron tres alternativas "
    "reales que se ajustan al modelo de SIGRE, cubriendo micro-crowdfunding sin interés, crédito en línea ágil y levantamiento "
    "de capital social. Cabe aclarar que, dado que las plataformas evaluadas en el catálogo de Merchant Maverick (Kiva U.S., "
    "Upstart y EquityNet) operan directamente para entidades y residentes en Estados Unidos, su análisis e integración en este "
    "presupuesto se realiza bajo el marco metodológico de evaluación de la asignatura (pudiendo instrumentarse en el ámbito local "
    "mediante un vehículo en EE. UU., socios locales de Kiva o fintechs mexicanas equivalentes)."
))

# ── 3.1 Kiva ──
heading(doc, "3.1 Opción 1: Kiva (Micro-Crowdfunding al 0% de Interés)", level=2)

para(doc, (
    "Kiva es una plataforma de financiamiento colectivo evaluada por Merchant Maverick (2026) para etapas iniciales. Opera mediante "
    "micropréstamos fondeados por prestamistas individuales a escala global (Kiva, 2026). Ofrece 0% APR, sin comisiones de apertura "
    "ni penalizaciones. No exige puntaje crediticio mínimo ni antigüedad comercial; su elegibilidad se basa en suscripción social "
    "(aportaciones de validación inicial del entorno del emprendedor). Otorga hasta $15,000 USD (Kiva, 2026), equivalentes a "
    "aproximadamente $270,000 MXN [VERIFICAR: tipo de cambio oficial aplicable], amortizables a 36 meses en 15-30 días de fondeo."
))

para(doc, "", bold_prefix="Justificación para SIGRE y Servicio de Deuda: ")
para(doc, (
    "Kiva financia las partidas P1 de software ($60,000 MXN) y P2 de infraestructura cloud para el Año 1 ($16,000 MXN), sumando "
    "$76,000 MXN (Universidad de Guadalajara, 2026). Al operar al 0% de interés, permite desplegar el sistema sin generar costos "
    "por intereses durante la etapa de adopción institucional. Devolver el préstamo de $76,000 MXN en 36 meses al 0% APR implica una "
    "amortización mensual fija de $2,111.11 MXN/mes ($25,333.33 MXN/año)."
))

# ── 3.2 Upstart ──
heading(doc, "3.2 Opción 2: Upstart (Préstamo en Línea con Evaluación mediante Inteligencia Artificial)", level=2)

para(doc, (
    "Upstart es una plataforma de crédito evaluada por Merchant Maverick (2026) que utiliza inteligencia artificial para analizar "
    "educación, área de especialidad y potencial de ingresos, en lugar de depender únicamente del historial crediticio (Upstart, 2026). "
    "Otorga montos de $1,000 a $50,000 USD (aprox. $18,000 a $900,000 MXN [VERIFICAR: monto en pesos]). Su ventaja es la velocidad: "
    "el 99% de los fondos se liberan en 1-2 días hábiles (Upstart, 2026). Sus tasas APR estimadas se ubican entre 7.80% y 35.99% "
    "[VERIFICAR: rango oficial aplicable según perfil], con comisiones de apertura del 0% al 12% [VERIFICAR: comisión aplicable], "
    "sin exigir tiempo en el negocio al otorgarse al fundador para inyección de capital en plazos de 36 a 60 meses."
))

para(doc, "", bold_prefix="Justificación para SIGRE y Servicio de Deuda: ")
para(doc, (
    "Upstart financia activos físicos y normativos inmediatos: P3 Hardware de Ventanilla ($20,000 MXN), P4 Marco Legal e INDAUTOR "
    "($12,000 MXN) y P5 Despliegue Operativo ($12,000 MXN), totalizando $44,000 MXN (Universidad de Guadalajara, 2026). Su desembolso "
    "en 24-48 horas asegura el aprovisionamiento oportuno. Amortizar estos $44,000 MXN a 36 meses bajo el rango de 7.80% a 35.99% APR "
    "[VERIFICAR: rango oficial aplicable según perfil] representa pagos mensuales estimados de entre $1,374.74 y $2,015.12 MXN/mes."
))

# ── 3.3 EquityNet ──
heading(doc, "3.3 Opción 3: EquityNet (Plataforma de Equity Crowdfunding y Red de Inversionistas)", level=2)

para(doc, (
    "EquityNet conecta a emprendedores con más de 25,000 inversionistas acreditados y fondos ángel mediante software patentado de análisis "
    "(EquityNet, 2026), siendo evaluada por Merchant Maverick (2026) como alternativa sin pasivos financieros. No genera intereses "
    "ni deuda fija, estructurándose mediante participación accionaria o notas convertibles. Opera con un plan básico gratuito ($0 USD/mes) "
    "y membresías avanzadas de $199 a $299 USD/mes [VERIFICAR: vigencia de tarifas de suscripción]. Permite levantar desde $10,000 hasta "
    "más de $1,000,000 USD en periodos de 30 a 90 días naturales."
))

para(doc, "", bold_prefix="Justificación para SIGRE: ")
para(doc, (
    "EquityNet respalda la partida P6: Fondo de Reserva de Contingencia Técnica ($20,000 MXN) (Universidad de Guadalajara, 2026). "
    "Para levantar estos $20,000 MXN se utilizará exclusivamente la modalidad básica sin costo ($0 USD/mes) —o bien estos $20,000 MXN "
    "constituyen la reserva inicial dentro de la preparación de una ronda semilla mayor para escalar a la Red UdeG—, evitando que el costo "
    "de una membresía mensual consuma el capital recaudado. Aporta 'Smart Money' y contactos estratégicos sin comprometer el flujo mensual."
))

# ── 3.4 Tabla Comparativa ──
heading(doc, "3.4 Tabla Comparativa de Criterios (Evaluación Merchant Maverick)", level=2)

para(doc, (
    "En la Tabla 1 se sintetizan las tres opciones contrastadas bajo los parámetros de Merchant Maverick (2026)."
))

comp_headers = [
    "Criterio",
    "Kiva (Crowdfunding 0%)",
    "Upstart (Préstamo IA)",
    "EquityNet (Equity Crowdfunding)",
]
comp_rows = [
    [
        "Tasa APR / Costo",
        "0.0% APR fijo;\nsin comisiones (Kiva, 2026)",
        "7.80%–35.99% APR [VERIFICAR: rango oficial aplicable según perfil];\ncomisión 0%–12% [VERIFICAR: comisión aplicable] (Upstart, 2026)",
        "0% APR (sin deuda);\nplan básico $0 USD/mes / avanzado $199–$299 USD/mes [VERIFICAR: vigencia de tarifas de suscripción] (EquityNet, 2026)",
    ],
    [
        "Puntaje Crediticio",
        "Sin mínimo; respaldo social (Merchant Maverick, 2026)",
        "Flexible / Modelo IA educación y empleo (Merchant Maverick, 2026)",
        "Sin puntaje mínimo; requiere plan de negocio (Merchant Maverick, 2026)",
    ],
    [
        "Antigüedad Mínima",
        "0 meses (Startups admitidas)",
        "0 meses (Fundador persona física)",
        "0 meses (Capital semilla admitido)",
    ],
    [
        "Límite Máximo",
        "Hasta $15,000 USD\n(~ $270,000 MXN [VERIFICAR: tipo de cambio oficial aplicable])",
        "Hasta $50,000 USD\n(~ $900,000 MXN [VERIFICAR: monto en pesos])",
        "Desde $10,000 hasta >$1,000,000 USD según tracción",
    ],
    [
        "Velocidad Fondeo",
        "15 a 30 días naturales",
        "1 a 2 días hábiles",
        "30 a 90 días naturales",
    ],
    [
        "Tipo Instrumento",
        "Micropréstamo (plazo 36 meses)",
        "Línea crédito (plazo 36-60 meses)",
        "Capital accionario / Notas convertibles",
    ],
    [
        "Aporte de Valor",
        "Validación moral y comunitaria",
        "Liquidez rápida para equipamiento",
        "Smart Money: mentores y contactos ángel",
    ],
]
add_styled_table(doc, comp_headers, comp_rows, col_widths=[3.5, 4.4, 4.6, 4.7])

# ═══════════════════════════════════════════════
# SECCIÓN 4: DESTINO DETALLADO DE RECURSOS
# ═══════════════════════════════════════════════

heading(doc, "4. Destino Detallado de los Recursos: Inversión Inicial vs. Inversión Periódica", level=1)

para(doc, (
    "La asignación de recursos guarda correspondencia con la estructura de costos de SIGRE (Universidad de Guadalajara, 2026), "
    "priorizando la Inversión Inicial (CAPEX) y planificando la Inversión Periódica (OPEX) con absorción institucional progresiva."
))

heading(doc, "4.1 Prioridad de Inversión Inicial (CAPEX)", level=2)

para(doc, (
    "El presupuesto de capital inicial (CAPEX) asciende a $140,000 MXN financiados externamente mediante seis partidas estructuradas:"
))

para(doc, (
    "a) Fondeo sin interés (Kiva, $76,000 MXN): Cubre la partida P1 (Finalización de módulos de producción, endurecimiento de seguridad "
    "[hardening] y pruebas E2E, $60,000 MXN), consolidando el prototipo preliminar ya desarrollado con bootstrapping, y la partida P2 "
    "(Infraestructura Cloud Año 1, prepago de $16,000 MXN)."
))

para(doc, (
    "b) Liquidez rápida (Upstart, $44,000 MXN): Cubre activos físicos y normativos inmediatos: partida P3 (Hardware de Ventanilla, $20,000 MXN: "
    "3 lectores 2D y 1 tableta), partida P4 (Marco Legal y registro INDAUTOR, $12,000 MXN) y partida P5 (Despliegue Operativo y Capacitación, $12,000 MXN)."
))

para(doc, (
    "c) Capital semilla estratégico (EquityNet, $20,000 MXN): Cubre la partida P6 (Fondo de Reserva de Contingencia Técnica, $20,000 MXN), "
    "aclarando que su único propósito es servir de reserva financiera ante imprevistos técnicos o sobrecostos de nube, y no gasto operativo ordinario."
))

heading(doc, "4.2 Distribución del OPEX y Plan de Amortización del Servicio de la Deuda", level=2)

para(doc, (
    "El costo operativo ordinario anual (OPEX) asciende a $28,800 MXN ($2,400 MXN/mes): P2 Nube ($1,400 MXN/mes = $16,800 MXN/año), "
    "P7 Mantenimiento de hardware ($4,000 MXN/año) y P8 Soporte técnico ($8,000 MXN/año) (Universidad de Guadalajara, 2026)."
))

para(doc, (
    "Reconciliación del Año 1: Kiva prepaga $16,000 MXN en P2, existiendo una diferencia de $800 MXN para completar los $16,800 anuales. "
    "Asimismo, P7 ($4,000 MXN) y P8 ($8,000 MXN) requieren cobertura en el primer ejercicio. Por ende, estos $12,800 MXN restantes del Año 1 "
    "($800 de ajuste de nube + $4,000 de mantenimiento + $8,000 de soporte) son absorbidos internamente mediante bootstrapping y apoyo operativo "
    "del laboratorio en CUTonalá, dando una Necesidad Total en el Año 1 de $152,800 MXN ($140,000 MXN de financiamiento externo + $12,800 MXN "
    "de absorción interna). A partir del Año 2, la institución (CUTonalá) absorbe los $28,800 MXN/año completos ($16,800 de nube + $4,000 "
    "de mantenimiento + $8,000 de soporte) como parte de su gasto operativo regular."
))

para(doc, (
    "Plan de Servicio de la Deuda: La amortización mensual de Kiva ($2,111.11 MXN/mes a 36 meses) sumada a la de Upstart (entre $1,374.74 "
    "y $2,015.12 MXN/mes a 36 meses) representa un servicio de deuda mensual total estimado de entre $3,485.85 y $4,126.23 MXN/mes "
    "($41,830.20 a $49,514.76 MXN/año). Durante el arranque, este compromiso se respalda con aportaciones de los fundadores/bootstrapping y, "
    "una vez en régimen operativo, se cubre con cargo al ahorro institucional generado por SIGRE en CUTonalá (que supera los $100,000 MXN anuales, "
    "es decir, más de $8,333.33 MXN/mes), cubriendo con holgura tanto el OPEX recurrente como las amortizaciones."
))

heading(doc, "4.3 Desglose Maestro de Asignación Presupuestal", level=2)

para(doc, (
    "La Tabla 2 detalla la correspondencia formal de las partidas P1 a P8, montos y esquemas de cobertura."
))

dest_headers = [
    "Partida / Fuente",
    "Rubro Específico a Cubrir",
    "Tipo de Gasto",
    "Monto (MXN)",
    "Justificación Financiera y Cobertura",
]
dest_rows = [
    [
        "P1: Kiva (2026)",
        "Finalización módulos producción, hardening y pruebas E2E",
        "Inversión Inicial",
        "$60,000",
        "Concluye el MVP para producción; 0% interés evita costos sobre desarrollo intelectual.",
    ],
    [
        "P2: Kiva (2026)",
        "Infraestructura Cloud Año 1 (prepago parcial GCP)",
        "Inversión Inicial",
        "$16,000",
        "Prepago de servidores desde el día 1; los $800 faltantes anuales se cubren con bootstrapping.",
    ],
    [
        "P3: Upstart (2026)",
        "Hardware de Ventanilla (3 escáneres 2D + 1 tableta)",
        "Inversión Inicial",
        "$20,000",
        "Activos físicos de almacén; liquidez rápida (24-48 hrs) asegura compra oportuna.",
    ],
    [
        "P4: Upstart (2026)",
        "Marco Legal y Propiedad Intelectual (INDAUTOR y Privacidad)",
        "Inversión Inicial",
        "$12,000",
        "Registro oficial de obra de software y blindaje normativo de protección de datos.",
    ],
    [
        "P5: Upstart (2026)",
        "Despliegue Operativo y Capacitación (señalética y talleres)",
        "Inversión Inicial",
        "$12,000",
        "Acondicionamiento físico de ventanillas y capacitación a personal de almacén.",
    ],
    [
        "P6: EquityNet (2026)",
        "Fondo de Reserva de Contingencia Técnica",
        "Inversión Inicial (reserva)",
        "$20,000",
        "Reserva exclusiva ante imprevistos técnicos o picos de nube; no es gasto operativo ordinario.",
    ],
    [
        "P2 Ajuste: Bootstrapping",
        "Ajuste Infraestructura Cloud Año 1 ($66.67/mes)",
        "Inversión Periódica (Año 1)",
        "$800",
        "Completa los $16,000 de Kiva para cubrir los $16,800/año ($1,400/mes) de nube en el Año 1.",
    ],
    [
        "P7: Interno (Año 1) / CUTonalá (Año 2+)",
        "Mantenimiento preventivo de hardware de almacén",
        "Inversión Periódica",
        "$4,000/año",
        "Año 1 cubierto por apoyo del laboratorio; Año 2+ absorbido por CUTonalá.",
    ],
    [
        "P8: Interno (Año 1) / CUTonalá (Año 2+)",
        "Soporte técnico, hardening y parches de seguridad",
        "Inversión Periódica",
        "$8,000/año",
        "Año 1 cubierto con bootstrapping; Año 2+ absorbido por CUTonalá (+ $100,000/año ahorro).",
    ],
]
add_styled_table(doc, dest_headers, dest_rows, col_widths=[2.8, 4.3, 2.5, 1.9, 5.7])

heading(doc, "4.4 Resumen Consolidado por Fuente de Financiamiento", level=2)

para(doc, (
    "En la Tabla 3 se sintetiza el esquema de financiamiento externo (\$140,000 MXN) y la absorción interna del Año 1 (\$12,800 MXN)."
))

summ_headers = [
    "Fuente de Financiamiento",
    "Inversión Inicial (CAPEX)",
    "Inversión Periódica (Año 1)",
    "Total Asignado Año 1",
]
summ_rows = [
    ["Kiva (2026) [Préstamo 0% APR]", "$76,000 MXN", "Prepago P2 ($16,000)", "$76,000 MXN"],
    ["Upstart (2026) [Préstamo en Línea]", "$44,000 MXN", "—", "$44,000 MXN"],
    ["EquityNet (2026) [Equity Crowdfunding]", "$20,000 MXN", "—", "$20,000 MXN"],
    ["Subtotal Financiamiento Externo (3 Fuentes)", "$140,000 MXN", "—", "$140,000 MXN"],
    ["Aportación Interna / Bootstrapping CUTonalá", "—", "$12,800 MXN", "$12,800 MXN"],
    ["NECESIDAD TOTAL AÑO 1 (CAPEX + OPEX)", "$140,000 MXN", "$12,800 MXN", "$152,800 MXN"],
]
add_styled_table(doc, summ_headers, summ_rows, col_widths=[5.5, 3.8, 4.0, 3.9])

# ═══════════════════════════════════════════════
# SECCIÓN 5: REFERENCIAS BIBLIOGRÁFICAS (APA 7)
# ═══════════════════════════════════════════════

heading(doc, "5. Referencias Bibliográficas", level=1)

references = [
    "EquityNet. (2026). EquityNet crowdfunding platform: Connect with accredited investors. EquityNet. https://merchantmaverick.go2cloud.org/aff_c?offer_id=320&aff_id=1&aff_sub=business-financing&aff_sub2=equitynet&aff_sub3=category-page&aff_sub4=cta&source=47150-review-category-start-up-business-loan-reviews",
    "Google. (2026). Gemini (Versión 1.5) [Modelo de lenguaje de gran escala]. https://gemini.google.com",
    "Kiva. (2026). How Kiva works: 0% interest crowdfunded loans for entrepreneurs. Kiva Microfunds. https://www.kiva.org/borrow",
    "Merchant Maverick. (2026). Start-up business loan reviews. Merchant Maverick. https://www.merchantmaverick.com/review-category/start-up-business-loan-reviews/",
    "Universidad de Guadalajara. (2026). SIGRE: Sistema Integrado de Gestión de Recursos y Espacios — Documento de arquitectura de software v1.0 [Documento técnico interno]. Centro Universitario de Tonalá.",
    "Upstart. (2026). Upstart loans: Fast online personal and startup financing. Upstart Network. https://www.upstart.com/ [VERIFICAR: enlace específico a financiamiento de fundadores]",
]

for ref in references:
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(1.27)
    p.paragraph_format.first_line_indent = Cm(-1.27)
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.15
    run = p.add_run(ref)
    run.font.size = Pt(9.5)
    run.font.name = "Calibri"

os.makedirs(OUTPUT_DIR, exist_ok=True)
doc.save(OUTPUT_FILE)
print(f"✅ Documento Word generado exitosamente en: {OUTPUT_FILE}")
