# -*- coding: utf-8 -*-
"""
Genera el documento Word corregido: Fuentes de Financiamiento para SIGRE.
Basado estrictamente en las opciones analizadas por Merchant Maverick (Start-up Business Loan Reviews).
Opciones: Kiva, Upstart, EquityNet.
Citas parentéticas APA 7 estrictas en el texto y formato corregido.
Ejecutar: python scripts/generate_financiamiento_docx.py
"""

from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import nsdecls
from docx.oxml import parse_xml
import os

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "docs")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "Fuentes_Financiamiento_SIGRE.docx")

def set_cell_shading(cell, hex_color):
    """Aplica color de fondo a una celda."""
    shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}" w:val="clear"/>')
    cell._tc.get_or_add_tcPr().append(shading)


def add_styled_table(doc, headers, rows, col_widths=None):
    """Crea una tabla limpia con encabezados sombreados."""
    table = doc.add_table(rows=1 + len(rows), cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.style = "Table Grid"

    # Encabezados
    for i, h in enumerate(headers):
        cell = table.rows[0].cells[i]
        cell.text = ""
        p = cell.paragraphs[0]
        run = p.add_run(h)
        run.bold = True
        run.font.size = Pt(9.5)
        run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        run.font.name = "Calibri"
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        set_cell_shading(cell, "2F5496")

    # Filas
    for r_idx, row_data in enumerate(rows):
        for c_idx, val in enumerate(row_data):
            cell = table.rows[r_idx + 1].cells[c_idx]
            cell.text = ""
            p = cell.paragraphs[0]
            run = p.add_run(str(val))
            run.font.size = Pt(9)
            run.font.name = "Calibri"
            if r_idx % 2 == 1:
                set_cell_shading(cell, "F2F4F8")

    # Anchos de columna
    if col_widths:
        for r in table.rows:
            for i, w in enumerate(col_widths):
                r.cells[i].width = Cm(w)

    doc.add_paragraph("")
    return table


def heading(doc, text, level=1):
    h = doc.add_heading(text, level=level)
    for run in h.runs:
        run.font.name = "Calibri"
        run.font.color.rgb = RGBColor(0x1F, 0x38, 0x64)
    return h


def para(doc, text, bold_prefix=None):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        run_b = p.add_run(bold_prefix)
        run_b.bold = True
        run_b.font.size = Pt(11)
        run_b.font.name = "Calibri"
    run = p.add_run(text)
    run.font.size = Pt(11)
    run.font.name = "Calibri"
    return p


# ──────────────────────────────────────────────
# Construcción del Documento
# ──────────────────────────────────────────────

doc = Document()

style = doc.styles["Normal"]
style.font.name = "Calibri"
style.font.size = Pt(11)
style.paragraph_format.space_after = Pt(6)
style.paragraph_format.line_spacing = 1.15

for section in doc.sections:
    section.top_margin = Cm(2.54)
    section.bottom_margin = Cm(2.54)
    section.left_margin = Cm(2.54)
    section.right_margin = Cm(2.54)

# ═══════════════════════════════════════════════
# SECCIÓN 1
# ═══════════════════════════════════════════════

heading(doc, "1. Perfil y Características del Inversor Ideal", level=1)

para(doc, (
    "SIGRE (Sistema Integrado de Gestión de Recursos y Espacios) es un proyecto tecnológico "
    "en etapa temprana desarrollado en el Centro Universitario de Tonalá de la Universidad de Guadalajara "
    "(Universidad de Guadalajara, 2026). Como plataforma de software orientada al sector educativo e institucional, "
    "su modelo no genera flujos de efectivo explosivos inmediatos, sino que produce valor financiero mediante "
    "el ahorro institucional y la mitigación de mermas patrimoniales. Por ello, el perfil de inversor o entidad "
    "financiera adecuada no corresponde a la banca comercial tradicional —que exige garantías hipotecarias y estados "
    "financieros auditados—, sino a plataformas y esquemas alternativos de financiamiento para startups catalogados "
    "por portales especializados como Merchant Maverick (2026). Estos modelos priorizan el potencial del producto, "
    "la tracción operativa y esquemas flexibles de crédito o capital social."
))

para(doc, (
    "Para contrastar y estructurar preliminarmente los criterios crediticios aplicables a la escala del proyecto, "
    "se utilizó como apoyo analítico el modelo de lenguaje Gemini (Google, 2026). A partir de esta evaluación, se definen "
    "cinco características esenciales que debe reunir el inversor o entidad financiadora para constituir una opción viable."
))

heading(doc, "1.1 Características del Inversor Adecuado", level=2)

characteristics = [
    (
        "1. Tolerancia al riesgo en proyectos de etapa semilla sin historial crediticio comercial extenso. ",
        "SIGRE se encuentra en fase inicial de despliegue y validación operativa (Universidad de Guadalajara, 2026). "
        "No cuenta con declaraciones fiscales de ejercicios previos ni historial comercial consolidado en buró. "
        "El inversor debe operar bajo modelos de suscripción no tradicionales —como la evaluación basada en algoritmos "
        "predictivos o respaldo comunitario analizados por Merchant Maverick (2026)—, en los que la viabilidad técnica "
        "y el perfil del equipo prevalecen sobre el historial crediticio formal."
    ),
    (
        "2. Flexibilidad en esquemas de retorno y amortización (0% interés, periodos de gracia o equity crowdfunding). ",
        "El flujo de efectivo inicial del proyecto debe canalizarse prioritariamente a la adquisición de activos críticos "
        "y puesta en marcha. Por tanto, el inversor ideal debe admitir esquemas de micro-crowdfunding sin tasa de interés, "
        "como el modelo de Kiva (2026), líneas con plazos de amortización diferidos a 36 o 60 meses, o bien, instrumentos "
        "de financiamiento colectivo de capital donde la retribución se vincule al crecimiento patrimonial y no a pagos fijos inmediatos."
    ),
    (
        "3. Estructura de costos financieros transparente y competitiva. ",
        "Para un presupuesto inicial de $140,000 MXN (Universidad de Guadalajara, 2026), costos por comisiones ocultas o "
        "tasas anuales equivalentes (APR) predatorias comprometerían la viabilidad financiera del proyecto. El proveedor "
        "seleccionado debe mantener una política transparente de comisiones de apertura (origination fees) y tasas de interés "
        "claramente delimitadas desde la solicitud, criterio rigurosamente evaluado en las revisiones de Merchant Maverick (2026)."
    ),
    (
        "4. Agilidad en tiempos de aprobación y desembolso de liquidez. ",
        "El despliegue del sistema responde a un calendario académico y operativo estricto. Procesos de evaluación burocráticos "
        "que demoren más de un trimestre resultan inviables. Se requiere una entidad que procese la solicitud y transfiera los "
        "recursos en plazos de entre 48 horas y un mes calendario, permitiendo la compra oportuna de equipos y el pago de licencias."
    ),
    (
        "5. Aporte de valor estratégico y red de validación (Smart Money o difusión en red). ",
        "Más allá del suministro de capital líquido, el canal de financiamiento debe aportar tracción, visibilidad y "
        "conexión con redes de ángeles inversionistas o comunidades de usuarios, tal como ocurre en plataformas de financiamiento "
        "colectivo evaluadas por Merchant Maverick (2026), facilitando la futura expansión del sistema a otros campus universitarios."
    ),
]

for bold_part, body in characteristics:
    para(doc, body, bold_prefix=bold_part)

# ═══════════════════════════════════════════════
# SECCIÓN 2
# ═══════════════════════════════════════════════

heading(doc, "2. Análisis Comparativo: Del Financiamiento Personal al Formal según el Tamaño del Proyecto", level=1)

para(doc, (
    "El acceso a recursos financieros evoluciona de manera paralela a la madurez y dimensiones del proyecto. "
    "En la evaluación de proyectos de inversión, resulta indispensable categorizar las alternativas disponibles "
    "para seleccionar el instrumento adecuado a cada fase de desarrollo, evitando el sobreendeudamiento prematuro "
    "o la dilución innecesaria de la propiedad intelectual."
))

heading(doc, "2.1 Financiamiento Personal / Bootstrapping / FFF y Tarjetas a Meses sin Intereses", level=2)

para(doc, (
    "En la fase de concepción y prototipado rápido, el mecanismo natural de fondeo es el financiamiento personal, "
    "el capital aportado por el círculo cercano (Friends, Family & Fools) y el apalancamiento mediante tarjetas de crédito "
    "a meses sin intereses. Para SIGRE, esta modalidad posibilitó los primeros ensayos técnicos de servidores y pruebas "
    "de concepto locales (Universidad de Guadalajara, 2026). Su principal ventaja es la disponibilidad inmediata sin "
    "trámites ni comisiones; no obstante, su alcance es sumamente limitado (fondos típicamente menores a $30,000 MXN) "
    "y concentra el riesgo total en el patrimonio del estudiante o desarrollador."
))

heading(doc, "2.2 Convocatorias y Plataformas de Capital Semilla Alternativo", level=2)

para(doc, (
    "Al transitar hacia la validación del Producto Mínimo Viable (MVP), surgen esquemas especializados de capital semilla "
    "y plataformas colaborativas. Como documenta Merchant Maverick (2026), este segmento incluye modelos de financiamiento "
    "colectivo donde comunidades de prestamistas financian proyectos al 0% de interés, o plataformas de ángeles inversores "
    "que aportan recursos a cambio de participación. Su mérito radica en que eliminan la carga del servicio de deuda convencional "
    "y validan el interés del mercado antes del escalamiento, requiriendo a cambio un esfuerzo riguroso de presentación pública y plan de negocio."
))

heading(doc, "2.3 Financiamiento Formal y Líneas de Crédito Online para Startups", level=2)

para(doc, (
    "El nivel formal comprende prestamistas en línea e intermediarios evaluados bajo la metodología de Merchant Maverick (2026). "
    "Estas entidades valoran variables objetivas: puntaje crediticio mínimo, tiempo de operación del negocio, ingresos comprobables, "
    "tasas APR y velocidad de fondeo. Para proyectos jóvenes que no cumplen con los requisitos de la banca múltiple tradicional, "
    "las fintechs de préstamos estructurados ofrecen liquidez rápida mediante algoritmos de riesgo alternativos, constituyendo "
    "el puente formal para financiar adquisiciones de hardware y capital de trabajo en etapas de crecimiento."
))

# ═══════════════════════════════════════════════
# SECCIÓN 3
# ═══════════════════════════════════════════════

heading(doc, "3. Propuesta y Justificación de Tres Fuentes de Financiamiento", level=1)

para(doc, (
    "Con base estricta en el catálogo de análisis y revisiones de prestamistas e instrumentos para startups de "
    "Merchant Maverick (2026), se seleccionaron tres alternativas reales y diversificadas que se ajustan al modelo de SIGRE. "
    "Cada opción cubre un ángulo financiero distinto: micro-crowdfunding sin costo financiero, crédito personal/comercial en línea "
    "con aprobación automatizada, y levantamiento de capital social mediante plataforma de inversión."
))

# ── 3.1 Kiva ──
heading(doc, "3.1 Opción 1: Kiva (Micro-Crowdfunding al 0% de Interés)", level=2)

para(doc, (
    "Kiva es una organización y plataforma de financiamiento colectivo catalogada y analizada favorablemente por "
    "Merchant Maverick (2026) como una de las soluciones más viables para emprendedores en fase temprana. Su mecanismo "
    "opera mediante micropréstamos fondeados por una comunidad internacional de prestamistas individuales (Kiva, 2026)."
))

para(doc, (
    "De acuerdo con los criterios de evaluación de Merchant Maverick (2026), Kiva destaca por ofrecer una tasa de interés "
    "del 0% APR y ausencia absoluta de comisiones de apertura o penalizaciones. No impone requisitos de puntaje crediticio "
    "mínimo ni antigüedad operativa comercial previa, basando su elegibilidad en un esquema de suscripción social donde el "
    "emprendedor valida su compromiso inicial con aportaciones de su entorno cercano. Los montos máximos alcanzan hasta $15,000 USD "
    "(Kiva, 2026), equivalentes a aproximadamente $270,000 MXN al tipo de cambio promedio actual [VERIFICAR: tipo de cambio oficial aplicable], "
    "con plazos de pago de hasta 36 meses. El tiempo de fondeo habitual oscila entre 15 y 30 días naturales."
))

para(doc, "", bold_prefix="Justificación para SIGRE: ")
para(doc, (
    "Kiva constituye la fuente prioritaria idónea para absorber los rubros intangibles más onerosos de SIGRE: el desarrollo "
    "de ingeniería de software ($60,000 MXN) y la contratación de la infraestructura de servidores cloud en Google Cloud Platform "
    "para el primer año ($16,000 MXN) (Universidad de Guadalajara, 2026). Al no devengar intereses ni costos de apertura, "
    "permite desplegar el núcleo del sistema sin generar salidas de efectivo financieras durante la etapa de adopción institucional."
))

# ── 3.2 Upstart ──
heading(doc, "3.2 Opción 2: Upstart (Préstamo en Línea con Evaluación mediante Inteligencia Artificial)", level=2)

para(doc, (
    "Upstart es una plataforma de crédito en línea revisada por Merchant Maverick (2026) dentro de su categoría de financiamiento "
    "para startups. Su propuesta de valor se basa en un modelo de suscripción que utiliza inteligencia artificial para evaluar factores "
    "no convencionales del solicitante —como formación académica, área de estudio y potencial de ingresos— en lugar de limitarse "
    "al historial de crédito histórico (Upstart, 2026)."
))

para(doc, (
    "Bajo las métricas de Merchant Maverick (2026), Upstart ofrece montos de crédito desde $1,000 hasta $50,000 USD "
    "(aprox. $18,000 a $900,000 MXN [VERIFICAR: monto en pesos]). Su gran fortaleza radica en la velocidad de fondeo: el 99% "
    "de las solicitudes aprobadas se liquidan en 1 a 2 días hábiles (Upstart, 2026). Las tasas de interés estimadas varían en un rango "
    "de 7.80% a 35.99% APR [VERIFICAR: rango oficial aplicable según perfil], con comisiones de apertura que van del 0% al 12% "
    "[VERIFICAR: comisión aplicable]. No exige antigüedad operativa de la empresa, ya que el financiamiento se otorga al fundador para inyección en el negocio."
))

para(doc, "", bold_prefix="Justificación para SIGRE: ")
para(doc, (
    "Esta opción se destina a financiar activos físicos y trámites legales inmediatos que demandan liquidez expedita: adquisición "
    "de 3 lectores ópticos industriales y 1 tableta para almacenes ($20,000 MXN), trámites notariales y registro de propiedad "
    "intelectual ante INDAUTOR ($12,000 MXN), y materiales para el despliegue operativo en ventanillas ($12,000 MXN), totalizando "
    "$44,000 MXN (Universidad de Guadalajara, 2026). La inmediatez de desembolso de Upstart (1 a 2 días) asegura la compra oportuna "
    "del hardware sin demoras logísticas."
))

# ── 3.3 EquityNet ──
heading(doc, "3.3 Opción 3: EquityNet (Plataforma de Equity Crowdfunding y Red de Inversionistas)", level=2)

para(doc, (
    "EquityNet es una plataforma pionera de financiamiento colectivo de capital (equity crowdfunding) evaluada por "
    "Merchant Maverick (2026) como alternativa para startups que buscan respaldo financiero sin contraer obligaciones de deuda fija. "
    "La plataforma opera un software patentado de análisis empresarial y conecta a fundadores con más de 25,000 inversionistas "
    "acreditados, ángeles de negocios y fondos de capital semilla (EquityNet, 2026)."
))

para(doc, (
    "Merchant Maverick (2026) resalta que en EquityNet no aplican tasas APR ni cargos por intereses, dado que el fondeo se "
    "estructura mediante venta de participación accionaria minoritaria o notas convertibles. La plataforma cobra un esquema "
    "de suscripción por el uso de herramientas de planeación y acceso a la red de inversionistas ($0 en plan básico; $199 a $299 USD/mes "
    "en planes avanzados [VERIFICAR: vigencia de tarifas de suscripción]). Permite solicitar montos desde $10,000 hasta más de $1,000,000 USD. "
    "El periodo de captación y cierre oscila habitualmente entre 30 y 90 días, sujeto al proceso de debida diligencia de los inversores."
))

para(doc, "", bold_prefix="Justificación para SIGRE: ")
para(doc, (
    "EquityNet se selecciona para respaldar la partida P6 del proyecto: el Fondo de Reserva de Contingencia Técnica ($20,000 MXN) "
    "(Universidad de Guadalajara, 2026), y simultáneamente servir como vehículo para la posterior ronda de financiamiento en la fase "
    "de escalamiento regional a otros centros universitarios de la Red UdeG. El valor principal de esta alternativa radica en el "
    "denominado 'Smart Money': acceso a inversionistas del sector tecnológico que aportan orientación estratégica y vinculación comercial "
    "sin comprometer el flujo operativo mensual de la plataforma."
))

# ── 3.4 Tabla Comparativa ──
heading(doc, "3.4 Tabla Comparativa de Criterios (Evaluación Merchant Maverick)", level=2)

para(doc, (
    "En la Tabla 1 se presenta la comparativa formal de las tres alternativas seleccionadas, "
    "contrastadas bajo los parámetros estandarizados de Merchant Maverick (2026)."
))

comp_headers = [
    "Criterio de Evaluación",
    "Kiva\n(Crowdfunding 0%)",
    "Upstart\n(Préstamo Online IA)",
    "EquityNet\n(Equity Crowdfunding)",
]
comp_rows = [
    [
        "Tasa APR / Costo Financiero",
        "0.0% APR fijo;\nsin comisiones ni intereses (Kiva, 2026)",
        "7.80% – 35.99% APR [VERIFICAR];\ncomisión 0%–12% (Upstart, 2026)",
        "0% APR (sin deuda);\nsuscripción $0–$299 USD/mes [VERIFICAR] (EquityNet, 2026)",
    ],
    [
        "Requisitos de Puntaje Crediticio",
        "Sin puntaje mínimo;\nevaluación por respaldo social (Merchant Maverick, 2026)",
        "Flexible / Modelo IA basado en educación y empleo (Merchant Maverick, 2026)",
        "Sin puntaje crediticio mínimo;\nrequiere plan de negocio formal (Merchant Maverick, 2026)",
    ],
    [
        "Tiempo Mínimo de Operación",
        "0 meses (Startups e ideas tempranas permitidas)",
        "0 meses (Acepta fundadores en etapa pre-operativa)",
        "0 meses (Admite proyectos en fase de capital semilla)",
    ],
    [
        "Límite Máximo de Financiamiento",
        "Hasta $15,000 USD\n(~ $270,000 MXN [VERIFICAR])",
        "Hasta $50,000 USD\n(~ $900,000 MXN [VERIFICAR])",
        "Desde $10,000 hasta >$1,000,000 USD\nsegún tracción",
    ],
    [
        "Velocidad de Fondeo",
        "15 a 30 días naturales\n(fase comunitaria)",
        "1 a 2 días hábiles\n(aprobación automatizada)",
        "30 a 90 días naturales\n(negociación con ángeles)",
    ],
    [
        "Tipo de Instrumento",
        "Micropréstamo colectivo amortizable a 36 meses",
        "Línea de crédito personal/comercial amortizable a 36–60 meses",
        "Capital de riesgo / Participación accionaria minoritaria",
    ],
    [
        "Aporte de Valor Estratégico",
        "Campaña de posicionamiento comunitario y validación moral",
        "Liquidez inmediata para compras urgentes de activos",
        "Smart Money: red de mentores y contactos de inversión",
    ],
]
add_styled_table(doc, comp_headers, comp_rows, col_widths=[3.8, 4.3, 4.3, 4.3])

# ═══════════════════════════════════════════════
# SECCIÓN 4
# ═══════════════════════════════════════════════

heading(doc, "4. Destino Detallado de los Recursos: Inversión Inicial vs. Inversión Periódica", level=1)

para(doc, (
    "La asignación del capital debe guardar estricta correspondencia con el cronograma y la naturaleza técnica "
    "de los activos requeridos por SIGRE (Universidad de Guadalajara, 2026). Para garantizar una gestión prudente, "
    "se priorizan los componentes de la Inversión Inicial (CAPEX), mientras que la Inversión Periódica (OPEX) "
    "se planifica con mecanismos de autosuficiencia y absorción institucional progresiva."
))

heading(doc, "4.1 Prioridad de Inversión Inicial (CAPEX)", level=2)

para(doc, (
    "El presupuesto de capital inicial se consolida en $140,000 MXN, distribuidos en tres bloques según el perfil de cada fuente:"
))

para(doc, (
    "a) Fondeo sin costo financiero (Kiva): Asigna $76,000 MXN para sufragar el esfuerzo de desarrollo de software y aseguramiento "
    "de calidad ($60,000 MXN) y la contratación de servidores en nube por 12 meses ($16,000 MXN). Al tratarse de partidas intangibles "
    "de largo retorno, financiarlas al 0% de interés previene la asfixia por servicio de deuda."
))

para(doc, (
    "b) Liquidez rápida (Upstart): Canaliza $44,000 MXN hacia elementos físicos y normativos de adquisición inmediata: lectores ópticos "
    "industriales 2D y tableta de supervisión ($20,000 MXN), blindaje jurídico y derechos de autor INDAUTOR ($12,000 MXN), y material "
    "de ventanilla y señalética ($12,000 MXN). El desembolso en 24–48 horas garantiza el aprovisionamiento oportuno de mostrador."
))

para(doc, (
    "c) Capital semilla estratégico (EquityNet): Reserva $20,000 MXN para constituir el Fondo de Reserva de Contingencia Técnica, "
    "procurando que el capital provenga de inversionistas ángeles interesados en escalar el sistema a la Red UdeG."
))

heading(doc, "4.2 Distribución y Justificación de la Inversión Periódica (OPEX)", level=2)

para(doc, (
    "Los costos operativos anuales ascienden a $28,800 MXN ($2,400 MXN mensuales promedio) (Universidad de Guadalajara, 2026). "
    "Durante el Año 1, la partida mensual de servidores ($1,400 MXN/mes) queda completamente prepagada mediante la partida P2 "
    "cubierta por Kiva ($16,000 MXN anuales). A partir del Año 2, la operación regular (servidores, mantenimiento de lectores por "
    "$4,000 MXN/año y soporte correctivo por $8,000 MXN/año) se transferirá al presupuesto de mantenimiento de CUTonalá. Esta transferencia "
    "se justifica financieramente en el dictamen técnico del proyecto, el cual demuestra un ahorro institucional de más de $100,000 MXN anuales "
    "por concepto de reducción de mermas y extravíos de equipamiento (Universidad de Guadalajara, 2026)."
))

heading(doc, "4.3 Desglose Maestro de Asignación Presupuestal", level=2)

para(doc, (
    "La Tabla 2 detalla la correspondencia entre fuente, rubro específico, naturaleza del gasto y justificación financiera."
))

dest_headers = [
    "Fuente de\nFinanciamiento",
    "Rubro Específico a Cubrir",
    "Tipo de Gasto",
    "Monto\n(MXN)",
    "Justificación Financiera",
]
dest_rows = [
    [
        "Kiva (2026)",
        "Ingeniería de Software y QA (MVP funcional, pruebas E2E)",
        "Inversión Inicial",
        "$60,000",
        "Partida de mayor escala; el 0% de interés evita costos de financiamiento sobre trabajo de desarrollo intelectual.",
    ],
    [
        "Kiva (2026)",
        "Infraestructura Cloud Año 1 (Cloud Run, Cloud SQL, Redis, SSL)",
        "Inversión Inicial\n(prepago anual)",
        "$16,000",
        "Asegura la disponibilidad continua de servidores desde el día uno de operación sin presión de flujo mensual.",
    ],
    [
        "Upstart (2026)",
        "Hardware de Ventanilla (3 escáneres 2D de uso rudo + 1 tableta)",
        "Inversión Inicial",
        "$20,000",
        "Activos físicos críticos; la velocidad de desembolso de Upstart (24-48 hrs) permite su compra inmediata.",
    ],
    [
        "Upstart (2026)",
        "Marco Legal y Propiedad Intelectual (Aviso Privacidad e INDAUTOR)",
        "Inversión Inicial",
        "$12,000",
        "Gasto normativo para registro oficial de obra y protección de datos conforme a la legislación aplicable.",
    ],
    [
        "Upstart (2026)",
        "Despliegue Operativo y Capacitación (señalética física y talleres)",
        "Inversión Inicial",
        "$12,000",
        "Acondicionamiento físico de mostradores de almacén y capacitación del personal de guardia.",
    ],
    [
        "EquityNet (2026)",
        "Fondo de Reserva de Contingencia Técnica",
        "Inversión Inicial\n(reserva)",
        "$20,000",
        "Amortiguador ante imprevistos técnicos o incrementos de consumo en la nube; no genera deuda recurrente.",
    ],
    [
        "Kiva (2026)\n[incluido en P2]",
        "Infraestructura Cloud recurrente (cómputo y base de datos GCP)",
        "Inversión Periódica",
        "$1,400/mes\n($16,800/año)",
        "Gasto operacional cubierto íntegramente durante el Año 1 mediante la partida anual prepagada.",
    ],
    [
        "Institución\n(CUTonalá, Año 2+)",
        "Mantenimiento preventivo de hardware de almacén",
        "Inversión Periódica",
        "$4,000/año",
        "Mantenimiento y reposición de cableado USB; absorbible por la partida de mantenimiento ordinario del campus.",
    ],
    [
        "Institución\n(CUTonalá, Año 2+)",
        "Soporte técnico, actualizaciones y parches de seguridad",
        "Inversión Periódica",
        "$8,000/año",
        "Mantenimiento correctivo de software; justificado con el ahorro institucional documentado de +$100,000 MXN/año.",
    ],
]
add_styled_table(doc, dest_headers, dest_rows, col_widths=[2.8, 4.4, 2.5, 2.0, 5.0])

heading(doc, "4.4 Resumen Consolidado por Fuente de Financiamiento", level=2)

para(doc, (
    "En la Tabla 3 se sintetiza la distribución del capital entre las tres opciones evaluadas en Merchant Maverick (2026)."
))

summ_headers = [
    "Fuente de Financiamiento",
    "Inversión Inicial (CAPEX)",
    "Inversión Periódica (Año 1)",
    "Total Asignado Año 1",
]
summ_rows = [
    ["Kiva (2026) [Préstamo 0% APR]", "$76,000 MXN", "Incluida en prepago P2", "$76,000 MXN"],
    ["Upstart (2026) [Préstamo en Línea]", "$44,000 MXN", "—", "$44,000 MXN"],
    ["EquityNet (2026) [Equity Crowdfunding]", "$20,000 MXN", "—", "$20,000 MXN"],
    ["TOTAL FINANCIADO", "$140,000 MXN", "—", "$140,000 MXN"],
]
add_styled_table(doc, summ_headers, summ_rows, col_widths=[5.2, 3.8, 4.0, 3.2])

# ═══════════════════════════════════════════════
# SECCIÓN 5: REFERENCIAS BIBLIOGRÁFICAS (APA 7)
# ═══════════════════════════════════════════════

heading(doc, "5. Referencias Bibliográficas", level=1)

references = [
    "EquityNet. (2026). EquityNet crowdfunding platform: Connect with accredited investors. EquityNet. https://www.equitynet.com/ [VERIFICAR: enlace específico a sección startups]",
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
    p.paragraph_format.space_after = Pt(8)
    p.paragraph_format.line_spacing = 2.0
    run = p.add_run(ref)
    run.font.size = Pt(11)
    run.font.name = "Calibri"

os.makedirs(OUTPUT_DIR, exist_ok=True)
doc.save(OUTPUT_FILE)
print(f"✅ Documento Word regenerado y guardado en: {OUTPUT_FILE}")
