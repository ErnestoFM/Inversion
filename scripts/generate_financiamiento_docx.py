# -*- coding: utf-8 -*-
"""
Genera el documento Word: Fuentes de Financiamiento para SIGRE.
Entrega académica — Formulación y Evaluación de Proyectos de Inversión.
Ejecutar: python scripts/generate_financiamiento_docx.py
"""

from docx import Document
from docx.shared import Pt, Inches, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn, nsdecls
from docx.oxml import parse_xml
import os

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "docs")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "Fuentes_Financiamiento_SIGRE.docx")

# ──────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────

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
        run.font.size = Pt(9)
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
            # Sombreado alterno
            if r_idx % 2 == 1:
                set_cell_shading(cell, "D6E4F0")

    # Anchos de columna
    if col_widths:
        for r in table.rows:
            for i, w in enumerate(col_widths):
                r.cells[i].width = Cm(w)

    doc.add_paragraph("")  # Espaciador
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
# Documento
# ──────────────────────────────────────────────

doc = Document()

# Estilos base del documento
style = doc.styles["Normal"]
style.font.name = "Calibri"
style.font.size = Pt(11)
style.paragraph_format.space_after = Pt(6)
style.paragraph_format.line_spacing = 1.15

# Configurar márgenes
for section in doc.sections:
    section.top_margin = Cm(2.54)
    section.bottom_margin = Cm(2.54)
    section.left_margin = Cm(2.54)
    section.right_margin = Cm(2.54)

# ═══════════════════════════════════════════════
# SECCIÓN 1: PERFIL Y CARACTERÍSTICAS DEL INVERSOR IDEAL
# ═══════════════════════════════════════════════

heading(doc, "1. Perfil y Características del Inversor Ideal", level=1)

para(doc, (
    "SIGRE (Sistema Integrado de Gestión de Recursos y Espacios) es un proyecto tecnológico "
    "en etapa temprana desarrollado en el Centro Universitario de Tonalá de la Universidad de Guadalajara. "
    "Como plataforma de software orientada al sector público-educativo, su modelo de negocio no genera "
    "flujos de efectivo explosivos a corto plazo, sino que produce valor a través del ahorro institucional "
    "y la eficiencia operativa. Esto significa que el perfil de inversor que mejor se alinea con el proyecto "
    "no es el especulador que busca retornos rápidos, sino un actor —público o privado— que entienda la "
    "dinámica del capital semilla tecnológico, los ciclos largos de adopción en instituciones educativas "
    "y el potencial de escalamiento a otros centros universitarios de la Red UdeG."
))

para(doc, (
    "En concreto, el inversor ideal puede ser un fondo de innovación estatal, una incubadora universitaria "
    "con programas de aceleración, o un organismo de fomento que otorgue recursos no reembolsables o créditos "
    "blandos. También puede tratarse de un inversionista ángel con experiencia en GovTech o EdTech que valore "
    "la tracción institucional por encima de las métricas financieras puras. A continuación se describen "
    "las cinco características que debe cumplir."
))

heading(doc, "1.1 Características del Inversor Adecuado", level=2)

characteristics = [
    (
        "1. Tolerancia al riesgo en proyectos de etapa semilla sin historial crediticio extenso. ",
        "SIGRE no cuenta con estados financieros de varios ejercicios ni con un flujo de ingresos recurrente "
        "probado en el mercado. Cualquier inversor debe aceptar que la validación del modelo se basa en "
        "indicadores de impacto institucional (horas de equipo recuperadas, reducción de merma patrimonial) "
        "más que en estados de resultados convencionales. Un fondo que solo financie empresas con al menos "
        "dos años de operación o con historial BURÓ positivo simplemente no aplica para esta etapa."
    ),
    (
        "2. Flexibilidad en esquemas de retorno: capital no reembolsable, amortización diferida o equity mínimo. ",
        "Dado que SIGRE opera dentro de una universidad pública, el concepto de \"dilución de propiedad\" "
        "tiene matices distintos a los de una startup privada. El inversor ideal ofrece esquemas como "
        "subvenciones a fondo perdido (convocatorias gubernamentales), créditos con periodo de gracia de al menos "
        "6-12 meses, o bien, participa con equity minoritario sin exigir control operativo. Esto permite que "
        "el equipo se enfoque en la adopción del sistema en lugar de presionarse por pagos inmediatos."
    ),
    (
        "3. Costos financieros competitivos: tasas APR bajas o nulas y comisiones de apertura mínimas. ",
        "El presupuesto total del proyecto asciende a $140,000 MXN de inversión inicial y $28,800 MXN anuales "
        "de operación. Son montos moderados para un fondo de inversión, pero significativos para un equipo "
        "universitario. Tasas de interés superiores al 15-20% anual harían que el costo del financiamiento "
        "consuma una parte desproporcionada del presupuesto operativo. Las mejores opciones son préstamos "
        "al 0% (como los de Kiva), convocatorias sin costo financiero o líneas con tasa preferencial para "
        "emprendedores."
    ),
    (
        "4. Agilidad en tiempos de aprobación y desembolso de liquidez. ",
        "El proyecto tiene un calendario académico con fechas límite semestrales. Un financiamiento que "
        "tome 6-8 meses en aprobarse no sirve si el piloto institucional debe estar desplegado para el "
        "ciclo 2027A. El inversor ideal tiene procesos de evaluación y desembolso que no excedan "
        "8-12 semanas, o bien, ofrece un primer desembolso parcial rápido mientras se completa la "
        "documentación formal del resto."
    ),
    (
        "5. Aporte de valor más allá del capital: mentoría, networking y validación institucional (Smart Money). ",
        "Para SIGRE, el valor de un inversor no se limita al cheque. Un fondo como FODECIJAL o un programa "
        "como Santander X aportan visibilidad mediática, acceso a redes de contactos con directivos de otras "
        "universidades, mentoría en modelos de licenciamiento de software y credibilidad ante las autoridades "
        "universitarias que deben aprobar la adopción del sistema. Este tipo de respaldo institucional "
        "puede ser incluso más determinante que el monto financiado."
    ),
]

for bold_part, body in characteristics:
    para(doc, body, bold_prefix=bold_part)


# ═══════════════════════════════════════════════
# SECCIÓN 2: ANÁLISIS COMPARATIVO DE FINANCIAMIENTO
# ═══════════════════════════════════════════════

heading(doc, "2. Análisis Comparativo: Del Financiamiento Personal al Formal según el Tamaño del Proyecto", level=1)

para(doc, (
    "No todas las fuentes de financiamiento son iguales ni se adaptan a todos los momentos del ciclo de vida "
    "de un proyecto. Un error común en proyectos de inversión universitarios es asumir que la única opción "
    "es el crédito bancario formal, cuando en realidad existen mecanismos previos que pueden cubrir "
    "necesidades específicas con menor costo y menor burocracia. Esta sección analiza tres niveles "
    "de financiamiento, desde el más informal hasta el estructurado, y ubica a SIGRE dentro de ellos."
))

heading(doc, "2.1 Financiamiento Personal / Bootstrapping / FFF", level=2)

para(doc, (
    "En las etapas más tempranas de cualquier proyecto —cuando apenas se tiene una idea y un prototipo—, "
    "la fuente más común de recursos es el bolsillo propio del emprendedor, el apoyo de familiares y amigos "
    "(conocido como Friends, Family & Fools o FFF), y en el contexto mexicano, el uso de tarjetas de crédito "
    "empresariales o personales con promociones a meses sin intereses."
))

para(doc, (
    "Para SIGRE, este mecanismo cubrió las primeras fases de desarrollo: la compra de dominios, el pago "
    "de créditos de prueba en Google Cloud Platform durante la fase de prototipado, y algunos periféricos "
    "menores. La ventaja principal es la inmediatez: no hay solicitudes, comités evaluadores ni plazos de espera. "
    "El emprendedor simplemente utiliza los recursos y arranca."
))

para(doc, (
    "Sin embargo, las desventajas son claras. El monto disponible es limitado (típicamente menos de $30,000-$50,000 MXN "
    "en este segmento), no existe respaldo legal estructurado entre las partes, y si el proyecto falla, el riesgo "
    "recae completamente sobre el patrimonio personal. Para un proyecto que requiere $140,000 MXN de inversión "
    "inicial, el bootstrapping por sí solo no alcanza, pero sí es útil como complemento para gastos operativos "
    "inmediatos y de prototipado rápido."
))

heading(doc, "2.2 Convocatorias Públicas y Privadas de Capital Semilla", level=2)

para(doc, (
    "El segundo nivel corresponde a fondos concursables de innovación, premios de emprendimiento y programas "
    "de subvención. En México, y particularmente en Jalisco, existen opciones muy relevantes como FODECIJAL "
    "(Fondo de Desarrollo Científico y Tecnológico de Jalisco), las convocatorias del CONAHCYT para proyectos "
    "de base tecnológica, y programas sectoriales de la Secretaría de Innovación, Ciencia y Tecnología del "
    "estado de Jalisco."
))

para(doc, (
    "La ventaja principal de este nivel es que los recursos suelen ser no reembolsables: el emprendedor "
    "recibe el dinero, ejecuta el proyecto, entrega reportes de avance y resultados, y no tiene que devolver "
    "el monto. No se genera deuda ni se diluye la propiedad intelectual. A cambio, los procesos de selección "
    "son competitivos, los plazos de evaluación pueden extenderse de 2 a 4 meses, y las convocatorias tienen "
    "ventanas específicas de recepción que no siempre coinciden con el calendario del proyecto."
))

para(doc, (
    "Para SIGRE, este nivel es particularmente atractivo porque el proyecto tiene un componente de innovación "
    "tecnológica aplicada (sistema de gestión con QR dinámicos, concurrencia Redis, firma digital) y un impacto "
    "social directo en una institución pública. Estos dos factores son exactamente lo que priorizan las "
    "convocatorias de fondos de innovación en Jalisco."
))

heading(doc, "2.3 Financiamiento Formal: Líneas de Crédito para Startups", level=2)

para(doc, (
    "El tercer nivel corresponde a las líneas de crédito estructuradas que evalúan plataformas como Merchant Maverick. "
    "Aquí entran prestamistas como Kiva, Bluevine, Fundbox, OnDeck y Kabbage, entre otros. Cada uno tiene criterios "
    "distintos de elegibilidad que incluyen: puntaje crediticio mínimo (FICO score o su equivalente), tiempo mínimo "
    "de operación del negocio, ingresos anuales mínimos, tasa APR ofrecida, montos máximos de línea de crédito "
    "y comisiones de apertura (origination fees)."
))

para(doc, (
    "La ventaja del financiamiento formal es la predictibilidad: las condiciones del préstamo están claras desde "
    "el inicio, los montos pueden ser significativamente mayores ($50,000 a $250,000 USD en algunos casos), y el "
    "acceso al crédito puede ser rápido si se cumplen los requisitos. La desventaja para un proyecto como SIGRE "
    "es que muchos de estos prestamistas exigen al menos 6-12 meses de operación, ingresos anuales mínimos de "
    "$100,000 USD, y puntajes crediticios por encima de 600-650. Un proyecto universitario en etapa semilla "
    "difícilmente cumple todos estos criterios."
))

para(doc, (
    "No obstante, hay excepciones diseñadas precisamente para startups sin historial, como Kiva (préstamos "
    "al 0% de interés mediante crowdfunding comunitario) o programas de crédito PyME de fintechs nacionales "
    "como Konfío o Credijusto, que tienen requisitos más flexibles y atienden al mercado mexicano."
))


# ═══════════════════════════════════════════════
# SECCIÓN 3: PROPUESTA Y JUSTIFICACIÓN DE 3 FUENTES DE FINANCIAMIENTO
# ═══════════════════════════════════════════════

heading(doc, "3. Propuesta y Justificación de Tres Fuentes de Financiamiento", level=1)

para(doc, (
    "Tras el análisis comparativo anterior, se seleccionan tres fuentes de financiamiento concretas que se "
    "adaptan al perfil de SIGRE como proyecto tecnológico universitario en etapa semilla, con una inversión "
    "inicial estimada de $140,000 MXN y un costo operativo anual de $28,800 MXN. Cada fuente se evalúa "
    "con los criterios que utiliza Merchant Maverick para calificar prestamistas de startups: tasas y costos, "
    "requisitos de elegibilidad, tiempo mínimo en el negocio, velocidad de fondeo y límites de crédito."
))

# ── OPCIÓN 1: Kiva ──
heading(doc, "3.1 Opción 1: Kiva — Micro-Crowdfunding al 0% de Interés", level=2)

para(doc, (
    "Kiva es una plataforma de préstamos de crowdfunding sin fines de lucro que permite a emprendedores "
    "en todo el mundo acceder a financiamiento al 0% de interés. El modelo funciona así: el emprendedor "
    "publica su proyecto en la plataforma, y una comunidad global de prestamistas individuales financia "
    "el préstamo en incrementos de $25 USD. Una vez completada la meta, el dinero se desembolsa y se "
    "devuelve en un plazo de hasta 36 meses sin generar intereses."
))

para(doc, (
    "Merchant Maverick ha evaluado a Kiva como una de las mejores opciones para startups en etapa temprana "
    "precisamente porque no exige puntaje crediticio mínimo, no requiere tiempo mínimo de operación y no "
    "cobra comisiones de apertura. El monto máximo por préstamo individual es de $15,000 USD (aproximadamente "
    "$270,000 MXN al tipo de cambio actual), lo cual cubre con holgura la inversión inicial de SIGRE."
))

para(doc, "", bold_prefix="Justificación para SIGRE: ")
para(doc, (
    "Kiva se alinea con el proyecto porque no requiere historial crediticio empresarial ni tiempo de operación "
    "previo. El proceso de fondeo toma entre 15 y 30 días una vez publicada la campaña. La tasa del 0% "
    "significa que los $140,000 MXN prestados se devuelven exactamente como $140,000 MXN, sin que el costo "
    "financiero consuma presupuesto operativo. El único requisito relevante es completar un proceso de "
    "verificación de identidad y contar con un plan de negocios coherente que convenza a la comunidad "
    "de prestamistas."
))

# ── OPCIÓN 2: FODECIJAL ──
heading(doc, "3.2 Opción 2: FODECIJAL — Fondo de Desarrollo Científico y Tecnológico de Jalisco", level=2)

para(doc, (
    "FODECIJAL es un fondo público del Gobierno del Estado de Jalisco, operado a través del Consejo Estatal "
    "de Ciencia y Tecnología de Jalisco (COECYTJAL), cuyo objetivo es financiar proyectos de investigación, "
    "desarrollo tecnológico e innovación con impacto en el estado. El fondo otorga recursos no reembolsables "
    "(a fondo perdido) a proyectos que demuestren viabilidad técnica e impacto social, económico o ambiental."
))

para(doc, (
    "Las convocatorias de FODECIJAL se publican periódicamente (generalmente una o dos veces al año) y "
    "los montos otorgados típicamente oscilan entre $100,000 y $500,000 MXN por proyecto, dependiendo de "
    "la modalidad. El proceso de evaluación incluye una revisión documental, evaluación por pares académicos "
    "y presentación ante un comité técnico. Los plazos de resolución suelen ser de 8 a 12 semanas desde el "
    "cierre de la convocatoria."
))

para(doc, "", bold_prefix="Justificación para SIGRE: ")
para(doc, (
    "SIGRE encaja directamente en el perfil de proyectos que FODECIJAL busca financiar: es un desarrollo "
    "tecnológico de base científica (arquitectura distribuida con mecanismos de concurrencia), tiene aplicación "
    "directa en una institución pública de Jalisco (CUTonalá), y resuelve un problema documentado de gestión "
    "patrimonial. El hecho de que los recursos sean no reembolsables elimina completamente el costo financiero "
    "del proyecto. La desventaja es la incertidumbre temporal: las convocatorias tienen ventanas específicas y "
    "la competencia entre proyectos puede ser alta. Sin embargo, el perfil institucional de SIGRE y su estado "
    "avanzado de desarrollo (ya cuenta con un MVP funcional) lo posicionan competitivamente."
))

# ── OPCIÓN 3: Santander X ──
heading(doc, "3.3 Opción 3: Santander X — Programas de Emprendimiento Universitario", level=2)

para(doc, (
    "Santander X es la plataforma global de emprendimiento del Grupo Financiero Santander, dirigida "
    "específicamente a estudiantes y egresados universitarios. Opera a través de convocatorias "
    "como Santander X Launch y Santander X Accelerate, que ofrecen financiamiento semilla (premios "
    "de entre $5,000 y $30,000 USD), acceso a programas de mentoría, espacios de coworking, y "
    "visibilidad ante inversionistas y corporativos. La Universidad de Guadalajara forma parte "
    "de la red de universidades asociadas a Santander Universidades, lo que da acceso directo "
    "a estas convocatorias."
))

para(doc, (
    "A diferencia de una línea de crédito convencional, Santander X no opera como un préstamo: "
    "los recursos otorgados son premios o subsidios que no generan deuda ni requieren devolución "
    "directa. Los criterios de selección priorizan innovación, impacto social, viabilidad del "
    "modelo de negocio y el perfil del equipo emprendedor."
))

para(doc, "", bold_prefix="Justificación para SIGRE: ")
para(doc, (
    "El vínculo directo entre la Universidad de Guadalajara y Santander Universidades facilita "
    "el acceso a estas convocatorias. SIGRE cumple con los criterios de selección: es un proyecto "
    "liderado por un estudiante de ingeniería, tiene un componente de impacto social en la comunidad "
    "universitaria, cuenta con un producto funcional demostrable, y su arquitectura técnica evidencia "
    "rigor de ingeniería. Además de los recursos económicos, el programa aporta mentoría especializada "
    "en modelos de escalamiento, lo cual es valioso para planificar la expansión de SIGRE hacia "
    "otros centros universitarios de la Red UdeG."
))

# ── TABLA COMPARATIVA ──
heading(doc, "3.4 Tabla Comparativa de las Tres Fuentes de Financiamiento", level=2)

para(doc, (
    "La siguiente tabla sintetiza la evaluación de las tres opciones utilizando los criterios "
    "de Merchant Maverick adaptados al contexto del proyecto."
))

comp_headers = [
    "Criterio", "Kiva\n(Crowdfunding 0%)", "FODECIJAL\n(Fondo Público Jalisco)", "Santander X\n(Emprendimiento Univ.)"
]
comp_rows = [
    ["Tasa de interés / Costo financiero", "0% APR, sin comisiones", "N/A — Recurso no reembolsable (a fondo perdido)", "N/A — Premio / Subsidio sin devolución"],
    ["Puntaje crediticio requerido", "No aplica", "No aplica (se evalúa proyecto, no historial personal)", "No aplica"],
    ["Tiempo mínimo de operación", "No se requiere", "No se requiere; se evalúa viabilidad técnica", "No se requiere; dirigido a estudiantes y egresados"],
    ["Monto máximo disponible", "Hasta $15,000 USD (~$270,000 MXN)", "$100,000 — $500,000 MXN por proyecto", "$5,000 — $30,000 USD (~$90,000 — $540,000 MXN)"],
    ["Velocidad de fondeo", "15-30 días (campaña de crowdfunding)", "8-12 semanas (convocatoria + evaluación)", "Variable según convocatoria (3-6 meses ciclo completo)"],
    ["Comisión de apertura", "Sin comisiones", "Sin comisiones", "Sin comisiones"],
    ["Tipo de financiamiento", "Préstamo con devolución a 36 meses", "Subvención no reembolsable", "Premio / Subsidio"],
    ["Valor agregado (Smart Money)", "Visibilidad en comunidad global de emprendedores", "Credibilidad institucional ante gobierno estatal", "Mentoría, red de contactos Santander, coworking"],
]
add_styled_table(doc, comp_headers, comp_rows, col_widths=[4.0, 4.2, 4.2, 4.2])


# ═══════════════════════════════════════════════
# SECCIÓN 4: DESTINO DETALLADO DE LOS RECURSOS
# ═══════════════════════════════════════════════

heading(doc, "4. Destino Detallado de los Recursos: Inversión Inicial vs. Inversión Periódica", level=1)

para(doc, (
    "Una parte fundamental de la planificación financiera de cualquier proyecto es especificar con claridad "
    "en qué se va a gastar cada peso. No basta con decir \"necesitamos $140,000 MXN\"; el inversor o fondo "
    "necesita saber exactamente qué rubros se cubren, por qué se eligió cada monto y cómo se distribuyen "
    "los recursos entre las fuentes de financiamiento propuestas."
))

para(doc, (
    "A continuación se presenta la distribución propuesta, separando los conceptos de inversión inicial "
    "(gastos únicos para poner en marcha el proyecto) de la inversión periódica (gastos recurrentes mensuales "
    "o anuales para mantener el sistema en operación)."
))

heading(doc, "4.1 Distribución de la Inversión Inicial (CAPEX)", level=2)

para(doc, (
    "La inversión inicial de SIGRE asciende a $140,000 MXN y está compuesta por seis partidas presupuestarias. "
    "La propuesta es distribuir estos costos entre las tres fuentes de la siguiente manera:"
))

para(doc, (
    "Kiva cubriría los rubros de desarrollo de software e infraestructura cloud del primer año, que son "
    "los gastos más grandes e inmediatos ($76,000 MXN). FODECIJAL financiaría el hardware de ventanilla, "
    "el marco legal y el despliegue operativo ($44,000 MXN), ya que estos rubros tienen un componente "
    "tangible y de impacto institucional que se alinea con los requisitos de rendición de cuentas de los "
    "fondos públicos. Santander X, a través de sus premios, cubriría el fondo de contingencia ($20,000 MXN) "
    "y proporcionaría el respaldo de mentoría para la fase de escalamiento."
))

heading(doc, "4.2 Distribución de la Inversión Periódica (OPEX)", level=2)

para(doc, (
    "Los costos operativos anuales de SIGRE son de $28,800 MXN ($2,400 MXN mensuales promedio). Estos costos "
    "se componen de infraestructura cloud ($16,800 MXN/año), mantenimiento de hardware ($4,000 MXN/año) y "
    "soporte técnico ($8,000 MXN/año)."
))

para(doc, (
    "La propuesta es que los costos operativos del primer año estén cubiertos dentro del financiamiento de Kiva "
    "(ya incluidos en la partida P2 de infraestructura cloud). A partir del segundo año, se contempla que la "
    "propia institución (CUTonalá) absorba los costos operativos como parte de su presupuesto regular de "
    "tecnologías de información, dado que el sistema ya estaría generando ahorros demostrados superiores a "
    "$100,000 MXN anuales en reducción de merma patrimonial. En caso de que la adopción institucional no se "
    "concrete en ese plazo, el fondo de contingencia ($20,000 MXN de Santander X) cubre parcialmente "
    "la operación mientras se gestiona la transición."
))

heading(doc, "4.3 Desglose Completo: Fuente de Financiamiento, Rubro, Tipo de Gasto y Justificación", level=2)

dest_headers = [
    "Fuente de\nFinanciamiento",
    "Rubro Específico a Cubrir",
    "Tipo de Gasto",
    "Monto\n(MXN)",
    "Justificación Financiera",
]
dest_rows = [
    [
        "Kiva",
        "Ingeniería de Software y QA (desarrollo MVP, módulos, pruebas E2E)",
        "Inversión Inicial",
        "$60,000",
        "Es el gasto más grande y urgente. Kiva permite obtenerlo rápido (15-30 días) sin costo financiero, liberando recursos para otros rubros.",
    ],
    [
        "Kiva",
        "Infraestructura Cloud — Año 1 (Cloud Run, PostgreSQL, Redis, SSL)",
        "Inversión Inicial\n(prepago anual)",
        "$16,000",
        "La infraestructura de nube es indispensable desde el día 1 del despliegue. Se incluye en Kiva porque requiere desembolso inmediato.",
    ],
    [
        "FODECIJAL",
        "Hardware de Ventanilla (3 lectores QR industriales + 1 tableta de supervisión)",
        "Inversión Inicial",
        "$20,000",
        "Equipo tangible con factura fiscal; se alinea con los requisitos de comprobación de fondos públicos de COECYTJAL.",
    ],
    [
        "FODECIJAL",
        "Marco Legal y Propiedad Intelectual (Aviso de Privacidad, Términos de Servicio, registro INDAUTOR)",
        "Inversión Inicial",
        "$12,000",
        "Rubro de protección jurídica que fortalece la propuesta ante evaluadores del fondo (demuestra seriedad y planeación).",
    ],
    [
        "FODECIJAL",
        "Despliegue Operativo y Capacitación (señalética, gafetes QR, talleres para almacenistas)",
        "Inversión Inicial",
        "$12,000",
        "Gasto de implementación con impacto social directo; evidencia de adopción real del sistema en la comunidad universitaria.",
    ],
    [
        "Santander X",
        "Fondo de Reserva de Contingencia Técnica",
        "Inversión Inicial\n(reserva)",
        "$20,000",
        "Cubre sobrecostos imprevistos o picos de tráfico en servidores. Al no generar deuda, el premio de Santander X es ideal para un fondo que puede no utilizarse en su totalidad.",
    ],
    [
        "Kiva\n(ya incluido en P2)",
        "Infraestructura Cloud mensual (GCP: cómputo, base de datos, caché)",
        "Inversión Periódica",
        "$1,400/mes",
        "Gasto operativo recurrente cubierto dentro de la partida anual de infraestructura financiada por Kiva en el primer año.",
    ],
    [
        "Institución\n(CUTonalá, Año 2+)",
        "Mantenimiento preventivo de hardware (lectores, cables USB, tableta)",
        "Inversión Periódica",
        "$4,000/año",
        "Gasto menor y predecible que la institución puede absorber como parte de su mantenimiento regular de equipo tecnológico.",
    ],
    [
        "Institución\n(CUTonalá, Año 2+)",
        "Soporte técnico y parches de seguridad de dependencias",
        "Inversión Periódica",
        "$8,000/año",
        "Horas de mantenimiento de software (actualizaciones de Node.js, Prisma, React). El ahorro institucional de +$100,000 MXN/año justifica este gasto.",
    ],
]
add_styled_table(doc, dest_headers, dest_rows, col_widths=[2.8, 4.5, 2.5, 2.0, 5.0])


# ── TABLA RESUMEN POR FUENTE ──
heading(doc, "4.4 Resumen de Inversión por Fuente de Financiamiento", level=2)

summ_headers = ["Fuente de Financiamiento", "Inversión Inicial", "Inversión Periódica (Año 1)", "Total Año 1"]
summ_rows = [
    ["Kiva (préstamo 0%)", "$76,000", "Incluida en P2", "$76,000"],
    ["FODECIJAL (fondo no reembolsable)", "$44,000", "—", "$44,000"],
    ["Santander X (premio)", "$20,000", "—", "$20,000"],
    ["TOTAL", "$140,000", "—", "$140,000"],
]
add_styled_table(doc, summ_headers, summ_rows, col_widths=[5.0, 3.5, 4.0, 3.0])


# ═══════════════════════════════════════════════
# SECCIÓN 5: REFERENCIAS BIBLIOGRÁFICAS
# ═══════════════════════════════════════════════

heading(doc, "5. Referencias Bibliográficas", level=1)

references = [
    "Consejo Estatal de Ciencia y Tecnología de Jalisco [COECYTJAL]. (2025). FODECIJAL: Fondo de Desarrollo Científico de Jalisco — Convocatorias y lineamientos. Gobierno del Estado de Jalisco. https://coecytjal.jalisco.gob.mx/fodecijal",
    "Google. (2026). Gemini [Modelo de lenguaje de gran escala]. Google DeepMind. https://gemini.google.com",
    "Kiva. (2026). How Kiva works: 0% interest crowdfunded loans for entrepreneurs. Kiva Microfunds. https://www.kiva.org/borrow",
    "Merchant Maverick. (2026). Best startup business loans 2026: Reviews & comparisons. Merchant Maverick. https://www.merchantmaverick.com/review-category/start-up-business-loan-reviews/",
    "Santander Universidades. (2026). Santander X: Programas Launch y Accelerate para emprendedores universitarios. Banco Santander. https://www.santanderx.com/",
    "Universidad de Guadalajara. (2026). SIGRE: Sistema Integrado de Gestión de Recursos y Espacios — Documento de arquitectura de software v1.0 [Documento técnico interno]. Centro Universitario de Tonalá.",
]

for ref in references:
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(1.27)
    p.paragraph_format.first_line_indent = Cm(-1.27)  # Hanging indent APA
    p.paragraph_format.space_after = Pt(8)
    p.paragraph_format.line_spacing = 2.0
    run = p.add_run(ref)
    run.font.size = Pt(11)
    run.font.name = "Calibri"


# ──────────────────────────────────────────────
# Guardar
# ──────────────────────────────────────────────

os.makedirs(OUTPUT_DIR, exist_ok=True)
doc.save(OUTPUT_FILE)
print(f"✅ Documento generado exitosamente: {OUTPUT_FILE}")
