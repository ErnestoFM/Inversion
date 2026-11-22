# -*- coding: utf-8 -*-
"""
Generador del Documento Maestro Sintetizado SIGRE (10 páginas de contenido + 1 portada = 11 páginas).
Alineado estrictamente con:
- tests/test_financial_rigor.py
- tests/test_master_plan_verification.py
- .agents/rules/rigor_financiero_y_matematico.md
"""

def generate_markdown():
    md = []
    
    # -------------------------------------------------------------
    # PORTADA Y FICHA TÉCNICA (Página 1)
    # -------------------------------------------------------------
    md.append("""# Propuesta de Inversión SIGRE — Ernesto Hatuey Fierro Meléndez

**Plataforma SaaS de Micro-Custodia y Trazabilidad Transaccional para Almacenes y Laboratorios Escolares**  
*Investment Memorandum & Business Plan — Convocatoria Mayo de 2026*  
*Materia: Formulación y Evaluación de Proyectos de Inversión (FEPI) | Docente: Mtra. Abril Adriana Angulo Sherman*  
*Centro Universitario de Tonalá (CUTonalá), Universidad de Guadalajara (UdeG)*  
*Fundador Único, Director General y Diseñador de Software: Ernesto Hatuey Fierro Meléndez*

---

### Ficha Técnica Ejecutiva del Proyecto

| Parámetro Clave | Detalle Institucional y Financiero |
|---|---|
| **Iniciativa / Software** | **SIGRE** (Sistema Integral de Gestión y Registro de Préstamos para Almacenes y Laboratorios Escolares) |
| **Emprendedor Líder** | **Ernesto Hatuey Fierro Meléndez** (Fundador Único, Director General y Diseñador de Software) |
| **Institución Académica** | Universidad de Guadalajara — CUTonalá | Materia: Formulación y Evaluación de Proyectos de Inversión |
| **Docente Titular** | **Mtra. Abril Adriana Angulo Sherman** |
| **Capital Requerido (CAPEX)** | **$180,000.00 MXN** (Inversión inicial pre-semilla, 100% desagregada y auditada) |
| **Métricas de Rentabilidad** | **VPN: +$46,984.47 MXN** (@ TMAR 15.0%) | **TIR: 24.27% anual** | **Relación B/C: 1.23x** |
| **Recuperación del Proyecto** | **Payback Simple: Mes 29.4** (2.45 años) | **Payback Descontado: Mes 33.1** (2.76 años) |
| **Mecanismo Inversionista** | **Cash Sweep del 70%** sobre Flujo de Efectivo Neto (FEN) hasta liquidar $180,000 MXN en **Mes 31.2**; regalía del 15% posterior |
| **Retorno al Inversionista** | **Trienal: $197,784 MXN (TIR 3.53%)** | **Quinquenal Base: 15.62% anual** | **Quinquenal UPES: 21.20% anual** |
| **Validación Psicométrica** | **Escala SUS: 82.85/100 puntos** ($n = 50$, DE 10.91, Grado A "Excelente", percentil 91.4, Alfa de Cronbach 0.892, $p = 0.035$) |
| **Mercado Base y Adopción** | Red Universitaria UdeG (196 unidades). Año 1: 3 planteles; Año 2: 8 planteles; Año 3: 22 planteles (11.2% del mercado) |

---
""")

    # -------------------------------------------------------------
    # SECCIÓN 1: PROBLEMÁTICA, DIAGNÓSTICO EMPÍRICO Y JUSTIFICACIÓN (Página 2)
    # -------------------------------------------------------------
    md.append("""## 1. Problemática, Diagnóstico Empírico y Justificación

### 1.1 El problema operativo: descontrol analógico en ventanillas de almacén
En los almacenes, talleres y laboratorios de los centros universitarios y escuelas preparatorias de la Red Universitaria de la Universidad de Guadalajara (UdeG), la gestión cotidiana de préstamo y devolución de insumos didácticos y activos de media y alta movilidad (osciloscopios, proyectores, herramienta especializada, balanzas y cómputo) se efectúa mediante métodos analógicos: libretas de papel, hojas volantes y formatos improvisados. 

Este esquema genera una fricción crítica: tiempos de atención en mostrador de **3.5 a 5.0 minutos por usuario** durante los cambios de clase (10 minutos entre bloques horarios), originando saturación de ventanilla, retrasos en el inicio de cátedra y una tasa estimada de extravío no conciliado del **8% al 12% del stock circulante por semestre**.

### 1.2 Análisis crítico: causas estructurales y la falacia digital vs. física
El sistema informático central institucional (SIIAU) y los sistemas corporativos ERP gestionan el macro-inventario contable y patrimonial para efectos de auditoría y adquisición periódica; sin embargo, no fueron concebidos para la **micro-custodia** ágil de ventanilla ni para resolver las dinámicas transaccionales de alta rotación en mostrador. La creencia de que un ERP central resuelve la micro-custodia de mostrador es una falacia operativa: las ventanillas universitarias operan desconectadas de las bases institucionales, obligando al auxiliar a confiar en la firma manual en papel, carente de valor probatorio o trazabilidad temporal.

### 1.3 Fundamentación empírica: caso base CUTonalá y estudio SUS ($n = 50$)
La iniciativa nace de la observación sistemática y levantamiento empírico en el Centro Universitario de Tonalá (**CUTonalá**). Para validar la viabilidad operativa y la aceptación funcional de una plataforma ágil, se aplicó la Escala de Usabilidad del Sistema (**SUS**, System Usability Scale) a una muestra de $n = 50$ informantes clave (estudiantes de ingeniería, profesores titulares y personal auxiliar de mostrador en ventanilla).

Como se resume en la Tabla 1, la plataforma SIGRE alcanzó un puntaje medio consolidado de **82.85 puntos** sobre 100 ($DE = 10.91$), ubicándose en la categoría de Grado A ("Excelente", percentil 91.4) de acuerdo con los baremos normativos de Bangor et al. (2008) y Sauro & Lewis (2012). La fiabilidad del instrumento arrojó un **Alfa de Cronbach de 0.892** (alta consistencia interna), mientras que la prueba t de Student de una muestra frente al umbral industrial estándar de 68 puntos evidenció significancia estadística contundente: $t(49) = 1.848$, $p = 0.035$ ($p < 0.05$).

| Estamento Evaluado | Muestra ($n$) | Media Obtenida (SUS) | Desviación Estándar ($DE$) | Rango Observado | Interpretación Cualitativa |
|---|---|---|---|---|---|
| **Alumnado (Ingeniería y Ciencias)** | 25 | 84.10 pts | 9.85 | 67.5 – 100.0 | Excelente usabilidad y rapidez |
| **Docentes e Investigadores** | 15 | 81.50 pts | 11.20 | 62.5 – 95.0 | Aceptación superior a la norma |
| **Auxiliares de Almacén y Ventanilla** | 10 | 81.75 pts | 12.40 | 60.0 – 97.5 | Agilidad en despacho directo |
| **Muestra Total Consolidada** | **50** | **82.85 pts** | **10.91** | **60.0 – 100.0** | **Grado A (Percentil 91.4, $p = 0.035$)** |

*Tabla 1. Resultados consolidados de la evaluación psicométrica estandarizada (Escala SUS, n = 50).*

En la Figura 1 se contrasta el modelo analógico tradicional frente al flujo de control trazable que implementa la plataforma SIGRE:

```mermaid
flowchart TD
    A[Usuario solicita insumo en mostrador] --> B{Método de Registro}
    B -->|Analógico Tradicional| C[Llenado manual en libreta: 3.5 a 5 min]
    C --> D[Sin trazabilidad ni firma digital probatoria]
    D --> E[Riesgo de extravío, merma y colapso de fila]
    B -->|Plataforma SIGRE| F[Escaneo credencial / QR: < 15 seg]
    F --> G[Firma en Canvas HTML5 con sellado HMAC-SHA256]
    G --> H[Cierre transaccional < 25 seg con telemetría en tiempo real]
```
*Figura 1. Diagrama de flujo del problema operativo analógico frente al flujo digital con trazabilidad de SIGRE.*

En la Figura 2 se presenta la distribución empírica de puntajes SUS del estudio de campo:

![Figura 2. Distribución de frecuencias y curva de densidad de puntajes SUS (n = 50)](docs/pruebas/screenshots/10_distribucion_puntajes_sus.png)  
*Figura 2. Distribución de frecuencias y curva de densidad de puntajes SUS (n = 50) frente a la media de la industria (Sauro & Lewis, 2012).*

### 1.4 Estimación económica corregida del costo de inacción por plantel
El costo de postergar la adopción tecnológica (costo de inacción) oscila entre **$90,000 MXN y $140,000 MXN anuales por plantel**, con un punto medio ponderado de **$115,000 MXN/año**. Bajo un análisis riguroso de micro-costos (Sapag Chain, 2014), el impacto anual promedio por plantel universitario asciende a **$117,310.00 MXN**, desglosado en la Tabla 2:

| Concepto de Pérdida / Ineficiencia | Base de Cálculo Anual por Plantel | Impacto Económico Anual |
|---|---|---|
| **Horas-hombre perdidas en filas de mostrador** | 4,200 transacciones $\times$ 4 min perdidos = 280 horas @ $140/h | $39,200.00 MXN |
| **Reposición de activos no devueltos o extraviados** | 5 a 8 reactivos/herramientas sin responsable conciliado | $48,500.00 MXN |
| **Gasto administrativo y consumibles en papel/libretas** | 12 libretas contables, hojas membretadas, carpetas y tóner | $8,610.00 MXN |
| **Horas extra de auditoría física y conciliación semestral** | 140 horas de personal técnico dedicadas a rastreo manual | $21,000.00 MXN |
| **Total Estimado de Inacción Administrativa** | **Sumatoria directa anual de costos ocultos y mermas** | **$117,310.00 MXN** |

*Tabla 2. Estimación preliminar del impacto de la inacción administrativa y pérdidas patrimoniales por plantel universitario.*

### 1.5 Análisis de alternativas existentes frente a SIGRE
Frente a las alternativas de mercado (ERP institucional, libretas de mostrador y apps genéricas de inventario), SIGRE ofrece ventajas determinantes consolidadas en la Tabla 3:

| Criterio de Selección Técnica | Libretas de Papel y Excel | ERP Institucional (SIIAU / SAP) | Software Genérico (Snipe-IT) | Plataforma SIGRE |
|---|---|---|---|---|
| **Tiempo de Despacho en Ventanilla** | 3.5 – 5.0 minutos | 2.5 – 4.0 minutos | 1.5 – 2.5 minutos | **< 25 segundos** |
| **Micro-custodia Transaccional Ágil** | Nula | Inexistente (sólo macro-patrimonio) | Parcial (sin firma digital) | **Total (código barras + firma)** |
| **Firma Digitalizada con Validez Probatoria** | Manual sin validez temporal | No disponible en mostrador | No nativa en mostrador | **Nativa (Canvas + HMAC-SHA256)** |
| **Costo Anual por Plantel** | Desconocido (mermas ocultas) | Alto ($300k+ prorrateado) | Medio ($35k - $60k + soporte) | **Económico ($24k - $48k MXN)** |
| **Operación Resiliente Offline** | N/A (física) | Inviable ante caídas de red | Compleja (requiere Docker local) | **Sincronización PWA local** |

*Tabla 3. Matriz comparativa de alternativas de solución técnica frente a la plataforma SIGRE.*

---
""")

    # -------------------------------------------------------------
    # SECCIÓN 2: LA SOLUCIÓN, OBJETIVOS Y MATRIZ DE MARCO LÓGICO (Página 3)
    # -------------------------------------------------------------
    md.append("""## 2. La Solución, Objetivos y Matriz de Marco Lógico (MML)

### 2.1 Descripción de módulos y propuesta de valor
SIGRE es una solución SaaS (*Software as a Service*) de **micro-custodia** y trazabilidad en tiempo real diseñada para ventanillas de laboratorios y almacenes escolares. Integra cuatro pilares funcionales:
1. **Despacho Digital Acelerado (< 25 s):** Lectura óptica de credenciales institucionales (código de barras / QR) con precarga instantánea del perfil académico.
2. **Lienzo de Firma Manuscrita con Sellado HMAC-SHA256:** Registro de aceptación en pantalla táctil con sellado criptográfico que garantiza no repudio.
3. **Semáforo y Telemetría de Desgaste:** Conteo automatizado de ciclos de uso por número de serie individual, previniendo fallas y abusos.
4. **Notificaciones Multicanal:** Alertas preventivas automatizadas vía WhatsApp, Telegram y correo antes del vencimiento del préstamo.

En la Figura 3 y Figura 4 se ilustra la interfaz de mostrador para el estampado de firma sobre lienzo HTML5 Canvas:

![Figura 3. Interfaz de firma manuscrita digitalizada sobre Canvas HTML5 con sellado criptográfico HMAC-SHA256](docs/pruebas/screenshots/05_canvas_firma_digital.png)  
*Figura 4. Interfaz de firma manuscrita digitalizada sobre Canvas HTML5 con sellado criptográfico HMAC-SHA256.*

### 2.2 Objetivos del proyecto
- **Objetivo General:** Desplegar y consolidar la plataforma SIGRE en la Red Universitaria de la UdeG como estándar operativo de micro-custodia de mostrador, recuperando el capital semilla y alcanzando rentabilidad sostenible a partir del segundo año.
- **Objetivo 1 (Técnico-Operativo):** Reducir el tiempo promedio de préstamo en ventanilla de 4.5 minutos a menos de 25 segundos, garantizando un uptime del sistema del 99.5% y disponibilidad de modo contingente offline.
- **Objetivo 2 (Comercial y Cobertura):** Incorporar 3 planteles en el Año 1 (1 piloto base CUTonalá sin costo + 2 contratos comerciales de prepas a $24,000 MXN), expandir a 8 sedes en el Año 2, y afiliar a 22 planteles activos al cierre del Año 3 (11.2% del mercado cautivo UdeG).
- **Objetivo 3 (Financiero y Retorno):** Recuperar el 100% de la inversión inicial de capital semilla ($180,000 MXN) en el **Mes 31.2** mediante un mecanismo de **Cash Sweep del 70%** sobre el FEN, alcanzando el punto de equilibrio operativo en el Mes 14 y la consolidación de nómina hacia el **Mes 22**.

### 2.3 Marco Lógico Metodológico (MML) del Proyecto SIGRE
Bajo la metodología internacional de la CEPAL/BID, la Tabla 4 sintetiza la estructura lógica causal de la intervención:

| Nivel Estructural | Resumen Analítico de Metas | Indicadores Objetivamente Verificables | Medios de Verificación | Supuestos Críticos |
|---|---|---|---|---|
| **Fin** | Elevar la eficiencia administrativa y preservar el patrimonio didáctico de las IES. | Reducción $\ge 85\%$ en mermas no justificadas y 70% en tiempo de fila al año 3. | Auditorías anuales de control patrimonial y actas de entrega-recepción. | Continuidad en las políticas de austeridad y digitalización institucional. |
| **Propósito** | Adoptar SIGRE como estándar operativo de mostrador en 22 planteles de la UdeG. | 22 contratos vigentes al mes 36; $\ge 95\%$ de préstamos procesados digitalmente. | Registros en base de datos SIGRE, contratos firmados y encuestas SUS. | Disposición de secretarios administrativos para contratar vía adjudicación directa. |
| **Componentes** | 1. Software SaaS optimizado.<br>2. Kit de mostrador plug & play.<br>3. Módulo de telemetría y desgaste.<br>4. Programa de inducción técnica. | - Disponibilidad de API $\ge 99.5\%$.<br>- Tiempo de transacción $\le 25$ seg.<br>- 100% de auxiliares de ventanilla capacitados y certificados. | Métricas cloud en Datadog/Grafana, logs de auditoría transaccional y listas de asistencia. | Estabilidad en la infraestructura de conectividad de los planteles afiliados. |
| **Actividades** | - Refinamiento full-stack y sellado.<br>- Trámites INDAUTOR y registro IMPI.<br>- Despliegue piloto y rondas demo.<br>- Soporte técnico y mesas de ayuda. | - Presupuesto CAPEX de $180,000 MXN ejecutado al 100% en 12 meses.<br>- 3 planteles operando en ciclo 2026-B. | Pólizas contables, facturas fiscales, constancias INDAUTOR/IMPI y bitácora técnica. | Entrega oportuna de fondos semilla y cumplimiento de la ruta crítica [RC]. |

*Tabla 4. Matriz de Marco Lógico (MML) bajo lineamientos internacionales CEPAL/BID.*

---
""")

    # -------------------------------------------------------------
    # SECCIÓN 3: NICHO DE MERCADO Y ESCALAMIENTO & SECCIÓN 4: COMERCIALIZACIÓN (Página 4)
    # -------------------------------------------------------------
    md.append("""## 3. Nicho de Mercado y Estrategia de Escalamiento

### 3.1 Mercado base cautivo: Red Universitaria UdeG
Con base en la numeralia oficial de la Coordinación General de Planeación y Evaluación (**mayo de 2026**; SEMS, 2024), el universo cautivo directo de la Red Universitaria UdeG comprende **196 dependencias**:
- **16 Centros Universitarios:** 6 temáticos metropolitanos (CUAAD, CUCS, CUCSH, CUCBA, CUCEA y CUGuadalajara), 2 centros **multitemáticos metropolitanos** (**CUTonalá** y **CUTlaquepaque**) y 10 centros universitarios regionales (CUSur, CULagos, CUAltos, CUCosta, etc.).
- **175 Escuelas Preparatorias:** Coordinadas por el Sistema de Educación Media Superior (SEMS), incluyendo 71 planteles metropolitanos y 104 módulos regionales.
- **5 Unidades Académicas y Administrativas de Apoyo:** Bibliotecas centrales, laboratorios compartidos y talleres intercentros.

Como detalla la Tabla 5, la meta de captación de 22 planteles para el cierre del Año 3 representa únicamente el **11.2% del mercado cautivo disponible**, confirmando que las metas comerciales no dependen de supuestos sobredimensionados de penetración:

| Segmento Institucional de la Red | Universo Total de Planteles | Año 1 (Validación) | Año 2 (Expansión) | Año 3 (Consolidación) | % Cobertura al Año 3 |
|---|---|---|---|---|---|
| **Centros Universitarios (CUs)** | 16 sedes | 1 (CUTonalá sin costo) | 3 centros | 8 centros | 50.0% de CUs |
| **Preparatorias SEMS (Metrópoli / Región)** | 175 planteles | 2 prepas comerciales | 5 preparatorias | 14 preparatorias | 8.0% de prepas |
| **Unidades de Apoyo y Laboratorios** | 5 unidades | 0 unidades | 0 unidades | 0 unidades | 0.0% |
| **Total de Sedes Afiliadas en Operación** | **196 unidades** | **3 planteles** | **8 sedes** | **22 sedes** | **11.2% de la Red** |

*Tabla 5. Desglose del nicho institucional de la Red Universitaria UdeG y metas comerciales al Año 3.*

### 3.2 Visión de escalamiento: de la Red UdeG a las IES públicas nacionales
A partir del Año 4, una vez validada la propuesta en 22 sedes UdeG, el modelo escalará hacia las Universidades Públicas Estatales (**UPES**) del Occidente y Centro del país (Universidad Michoacana, Universidad de Guanajuato, Universidad de Colima y Universidad Autónoma de Nayarit), las cuales agrupan más de 340 planteles con idénticas fallas de micro-custodia analógica.

En la Figura 4 se ilustra la ruta de expansión por fases institucionales:

```mermaid
flowchart LR
    Fase1[Fase 1: Piloto Base CUTonalá y 2 Prepas<br>Año 1: 3 planteles] --> Fase2[Fase 2: Red Universitaria UdeG<br>Años 2 y 3: 8 a 22 planteles]
    Fase2 --> Fase3[Fase 3: Expansión Regional a UPES<br>Años 4 y 5: 35 a 55 planteles nacionales]
```
*Figura 4. Visión de escalamiento institucional progresivo: de la Red UdeG a las IES públicas nacionales.*

## 4. Comercialización, Decisores y Servicios

### 4.1 Estructura de decisores de compra por tipo de plantel
La venta institucional (B2G escolar) se dirige a tres perfiles decisores:
- **Secretarios Administrativos (CUs):** Administran el gasto operativo de centros y autorizan adquisiciones directas de software y equipamiento.
- **Directores y Administradores de Preparatoria (SEMS):** Disponen de partidas de gasto desconcentrado para modernización y equipo didáctico.
- **Jefes de Almacén y Coordinadores de Carrera:** Actúan como usuarios promotores que demandan la solución ante las filas de mostrador.

### 4.2 Viabilidad burocrática y contratación por adjudicación directa
Conforme a la Ley de Compras Gubernamentales, Enajenaciones y Contratación de Servicios del Estado de Jalisco y la fijación de la Unidad de Medida y Actualización (UMA) diaria para 2026 en **$117.31 MXN** (INEGI, 2026), el umbral de compra menor por adjudicación directa alcanza **$117,310.00 MXN anuales**. Las cuotas de suscripción de SIGRE ($24,000 MXN a $48,000 MXN) se ubican holgadamente por debajo de dicho tope, facilitando una contratación ágil y directa sin licitación.

### 4.3 Motivación y desglose de tarifas frente a costos de servicio
La Tabla 6 define la estructura de planes anuales y servicios de inducción:

| Nivel de Servicio | Tarifa Anual (MXN) | Cobertura Operativa Incluida | Servicios de Setup y Soporte |
|---|---|---|---|
| **Preparatoria SEMS / Lab Básico** | $24,000 MXN ($2,000/mes) | Hasta 2 almacenes, 1,500 usuarios, escaneo y firmas ilimitadas | Setup inicial $5,000 MXN; soporte remoto N1 |
| **Centro Universitario Estándar** | $48,000 MXN ($4,000/mes) | Hasta 6 almacenes/talleres, 8,000 usuarios, telemetría y reportes | Setup inicial $15,000 MXN; inducción en sitio |
| **Multi-Campus Enterprise (Red)** | $72,000 MXN ($6,000/mes) | Almacenes ilimitados, analítica predictiva y API multi-plantel | Setup llave en mano $25,000 MXN; soporte 24/7 |

*Tabla 6. Estructura de tarifas anuales, cuotas de configuración y cobertura operativa por nivel de servicio.*

### 4.4 Estrategia de comercialización y embudo de ventas (Funnel)
El embudo comercial se articula en cuatro pasos: 1) Prospección dirigida con dossier ejecutivo y demo en video; 2) Sesión demostrativa presencial de 15 minutos con hardware real; 3) Periodo de prueba piloto de 30 días en un taller crítico; 4) Formalización de contrato anual por adjudicación directa facturada al ciclo escolar.

### 4.5 Socialización con usuarios y acompañamiento humano
Se imparten talleres presenciales de 90 minutos para auxiliares de mostrador y se distribuye material infográfico en mostrador para sensibilizar a los alumnos sobre el registro ágil de su firma digital.

---
""")

    # -------------------------------------------------------------
    # SECCIÓN 5: ESPECIFICACIONES TÉCNICAS, DESGASTE Y CONTINGENCIA (Página 5)
    # -------------------------------------------------------------
    md.append("""## 5. Especificaciones Técnicas, Desgaste y Contingencia

### 5.1 Arquitectura tecnológica y parámetros de calidad
SIGRE implementa una arquitectura desacoplada en la nube estructurada en 5 capas: Presentación (PWA responsiva en Vue 3 y TypeScript), API Gateway (Caddy con TLS 1.3 automatizado), Lógica de Negocio (microservicios en Python/FastAPI), Capa de Persistencia (PostgreSQL relacional con réplicas y Redis para caché de sesión en memoria) y Capa de Trazabilidad Criptográfica (sellado HMAC-SHA256 con sellos de tiempo UTC).

En la Figura 5 se presenta el diagrama de arquitectura tecnológica en la nube:

```mermaid
flowchart TD
    Client[Capa 1: Cliente PWA Vue 3 / TS en Mostrador] --> Gateway[Capa 2: API Gateway Caddy TLS 1.3 / Reverse Proxy]
    Gateway --> Backend[Capa 3: Microservicios Python / FastAPI]
    Backend --> Cache[(Capa 4: Caché Redis en Memoria)]
    Backend --> DB[(Capa 4: Persistencia PostgreSQL Relacional)]
    Backend --> Crypto[Capa 5: Sellado Criptográfico HMAC-SHA256]
```
*Figura 5. Diagrama de arquitectura tecnológica en la nube y componentes del sistema.*

La Tabla 7 consolida los parámetros técnicos y estándares de seguridad del sistema:

| Capa / Componente | Tecnología Seleccionada | Parámetro de Rendimiento y Seguridad |
|---|---|---|
| **Frontend / Cliente Mostrador** | Vue 3 + TypeScript + Tailwind CSS | Carga inicial < 1.2 s, tiempo de render de firma < 16 ms |
| **Backend / API Transaccional** | Python 3.11 + FastAPI (Asincrónico) | Latencia p95 < 45 ms, soporte de 50 req/s por nodo |
| **Base de Datos y Caché** | PostgreSQL 15 + Redis In-Memory | Consultas indexadas < 10 ms, ACID garantizado |
| **Seguridad Criptográfica** | HMAC-SHA256 + Tokens JWT | Sellado de actas con hash inmutable y salt individual |
| **Infraestructura Cloud** | VPS Linux en centro de datos Tier III | 99.5% uptime garantizado por SLA, respaldos snapshot cada 6 h |

*Tabla 7. Especificaciones técnicas de componentes de software, nube y estándares de seguridad.*

### 5.2 Registro de desgaste individual de activos y prevención de abusos
A diferencia de los inventarios que tratan los activos como categorías genéricas, SIGRE vincula cada ejemplar a un identificador único con horómetro y contador de préstamos. Cuando un activo supera el 85% de su vida útil recomendada o acumula reportes de daño menor, el sistema emite una alerta directiva recomendando servicio correctivo antes del colapso funcional.

En la Figura 6 se muestra el tablero directivo ejecutivo, el cual permite a las autoridades auditar la tasa de uso, horas de operación e incidencias de desgaste en tiempo real:

![Figura 6. Tablero directivo ejecutivo con telemetría de activos y control de inventario en tiempo real](docs/pruebas/screenshots/08_dashboard_ejecutivo.png)  
*Figura 6. Tablero directivo ejecutivo con telemetría de activos y control de inventario en tiempo real.*

### 5.3 Cumplimiento normativo (LGPDPPSO), PDI CUTonalá y contingencia offline
El tratamiento de datos personales de alumnos y docentes se apega a la Ley General de Protección de Datos Personales en Posesión de Sujetos Obligados (LGPDPPSO). No se almacenan biométricos invasivos, limitándose al código de estudiante, nombre y trazo vectorizado de la firma digital, blindados bajo cifrado AES-256 en reposo. Asimismo, el proyecto se alinea con el Plan de Desarrollo Institucional (PDI) de CUTonalá hacia la sustentabilidad y cero papel.

Ante eventuales caídas del suministro eléctrico o interrupciones de conectividad a Internet en los campus, el cliente PWA conmuta de forma transparente al **modo contingente de micro-custodia offline**: las transacciones se almacenan en el almacenamiento local seguro del navegador (*IndexedDB*) con firma criptográfica local y se sincronizan automáticamente con la nube una vez restablecida la red.

---
""")

    # -------------------------------------------------------------
    # SECCIÓN 6: ORGANIZACIÓN, CAPITAL HUMANO Y CRONOGRAMA (Página 6)
    # -------------------------------------------------------------
    md.append("""## 6. Organización, Capital Humano y Cronograma

### 6.1 Estructura organizacional y perfiles del equipo inicial
La conducción ejecutiva y técnica de SIGRE está encabezada por **Ernesto Hatuey Fierro Meléndez** como **Fundador Único, Director General y Diseñador de Software**. Asume de manera directa la arquitectura del sistema, el desarrollo full-stack, la administración de infraestructura cloud, la gestión comercial de cuentas y el diseño de la experiencia de usuario.

En la Figura 7 se representa el organigrama operativo del equipo y su transición programada:

```mermaid
graph TD
    Fundador[Ernesto Hatuey Fierro Meléndez<br>Fundador Único y Director General]
    Fundador --> Tech[Especialista Soporte Tiempo Completo<br>Activación: Mes 22]
    Fundador --> Support[Soporte Técnico N1<br>Activación: Mes 15]
    Fundador --> Sales[Customer Success / Comercial<br>Activación: Mes 28]
```
*Figura 7. Organigrama funcional del equipo inicial y fases de escalamiento de personal.*

### 6.2 Plan de escalamiento del equipo y modelo de compensación
Para evitar presiones sobre la liquidez en la fase temprana, la estructura de compensación sigue un esquema de **nómina escalonada** vinculada a hitos de facturación y número de planteles afiliados:
- **Año 1 ($0 nómina externa):** El fundador absorbe la totalidad de las labores de desarrollo, soporte y despliegue inicial.
- **Año 2 ($120,000 MXN total de nómina):** Al alcanzar 4 planteles en el Mes 15, se incorpora 1 auxiliar de Soporte Técnico N1 (7 meses @ $4,000 = $28,000 MXN). En el **Mes 22**, al consolidarse la meta de 8 planteles, se activa 1 Especialista de Soporte Técnico a Tiempo Completo (3 meses @ $10,000 = $30,000 MXN). Los honorarios operativos del fundador se fijan en $62,000 MXN anuales ($28,000 + $30,000 + $62,000 = **$120,000 MXN**).
- **Año 3 ($240,000 MXN total de nómina):** Al escalar hacia 22 sedes, se mantiene al Especialista de Tiempo Completo (12 meses @ $10,000 = $120,000 MXN), se incorpora un responsable de Customer Success y soporte (9 meses @ $7,000 = $63,000 MXN) y se asigna un estipendio al fundador de $57,000 MXN ($120,000 + $63,000 + $57,000 = **$240,000 MXN**).

La Tabla 8 resume las condiciones de activación contractual:

| Periodo / Fase | Posición a Incorporar | Gatillo de Activación Contractual | Esquema y Costo Anual |
|---|---|---|---|
| **Año 1 (Meses 1-12)** | Fundador Único (Full-Stack & Dirección) | Desembolso de capital semilla | Compromiso de capital intelectual ($0 MXN nómina fija) |
| **Año 2 (Mes 15)** | 1 Técnico de Soporte N1 | 4 planteles comerciales activos | Medio tiempo (7 meses @ $4,000 = $28,000 MXN) |
| **Año 2 (Mes 22)** | 1 Especialista Soporte Tiempo Completo | 8 planteles afiliados confirmados | Tiempo completo (3 meses @ $10,000 = $30,000 MXN) |
| **Año 2 (Meses 13-24)** | Honorarios Operativos del Fundador | Facturación acumulada $\ge \$200,000$ | Honorarios anuales consolidados por $62,000 MXN |
| **Año 3 (Meses 25-36)** | 1 Especialista Soporte TC + 1 CS | 12 planteles en operación | Salarios ($120k + $63k) + Estipendio fundador ($57k) = $240,000 MXN |

*Tabla 8. Estructura de crecimiento del equipo técnico y condiciones de activación contractual.*

### 6.3 Justificación de bienes inmuebles, coworking y contingencia
La empresa opera bajo un modelo remoto y en la nube, suprimiendo inversiones de capital en la compra o arrendamiento de oficinas corporativas. Para juntas directivas con autoridades universitarias y sesiones de capacitación, se utilizan salas de juntas bajo demanda en espacios de *coworking* flexibles en Guadalajara y Zapopan, mitigando el riesgo de liquidez.

### 6.4 Hoja de Ruta Operativa y Despliegue Secuencial por Etapas (Año 1)
La ejecución del Año 1 se estructura en cuatro etapas secuenciales, como ilustra la Figura 8:

```mermaid
flowchart LR
    E1[Etapa 1: M1-M3<br>Pulido Técnico y Blindaje IP] --> E2[Etapa 2: M4-M6<br>Piloto CUTonalá e Inducción]
    E2 --> E3[Etapa 3: M7-M9<br>Validación y Prepas SEMS]
    E3 --> E4[Etapa 4: M10-M12<br>Cierre Ciclo B y Contratos]
```
*Figura 8. Esquema secuencial de etapas operativas y metas críticas del primer año.*

La Tabla 9 desglosa los entregables por fase:

| Fase del Plan de Despliegue | Ventana Temporal | Propósito Operativo | Entregables y Criterios de Aceptación |
|---|---|---|---|
| **Etapa 1: Preparación y Blindaje** | Meses 1 a 3 | Pulido de software y registro de marca | Código fuente auditado, trámites INDAUTOR y solicitud IMPI |
| **Etapa 2: Validación Piloto** | Meses 4 a 6 | Despliegue en 3 almacenes CUTonalá | 3 terminales operando, 1,200 actas digitales procesadas |
| **Etapa 3: Tracción Comercial** | Meses 7 a 9 | Demostraciones en prepas SEMS | 2 pre-contratos firmados y kit demo de mostrador evaluado |
| **Etapa 4: Cierre y Consolidación** | Meses 10 a 12 | Cobro de suscripciones ciclo 2026-B | **3 planteles** en operación (**2 contratos comerciales** de prepas + CUTonalá) |

*Tabla 9. Matriz de fases de ejecución operativa y criterios de aceptación (Año 1).*

### 6.5 Cronograma Anual en Diagrama de Gantt y Ruta Crítica [RC]
El cronograma de trabajo del primer año y su Ruta Crítica [RC] se describen en la Tabla 10:

| Actividad Clave de Ejecución | Duración Estimada | Dependencia Previa | Ruta Crítica [RC] |
|---|---|---|---|
| **A1. Constitución legal y cuenta de cheques** | Semanas 1 a 3 | Ninguna | Sí [RC] |
| **A2. Depuración técnica y pruebas de estrés cloud** | Semanas 2 a 6 | Ninguna | Sí [RC] |
| **A3. Trámites de registro INDAUTOR y solicitud IMPI** | Semanas 4 a 8 | A1, A2 | Sí [RC] |
| **A4. Adquisición y ensamble de kits demo de mostrador** | Semanas 6 a 9 | A1 | No |
| **A5. Despliegue en 3 almacenes base de CUTonalá** | Semanas 10 a 16 | A2, A3 | Sí [RC] |
| **A6. Capacitación presencial a auxiliares de ventanilla** | Semanas 14 a 17 | A5 | Sí [RC] |
| **A7. Jornadas demostrativas en 10 escuelas preparatorias** | Semanas 18 a 28 | A4, A6 | No |
| **A8. Negociación y firma de contratos comerciales SEMS** | Semanas 26 a 38 | A7 | Sí [RC] |
| **A9. Configuración y entrega de kits en 2 prepas ciclo B** | Semanas 36 a 44 | A8 | Sí [RC] |
| **A10. Auditoría anual de métricas y cierre de ejercicio** | Semanas 45 a 48 | A9 | No |

*Tabla 10. Cronograma anual de actividades, dependencias y Ruta Crítica [RC] (Año 1).*

En la Figura 9 se detalla la secuencia temporal de las actividades operativas:

```mermaid
gantt
    title Cronograma de Trabajo Año 1 - SIGRE
    dateFormat  YYYY-MM-DD
    section Ruta Crítica [RC]
    A1. Constitución y apertura cuenta :crit, a1, 2026-06-01, 21d
    A2. Pruebas y estrés de software  :crit, a2, 2026-06-15, 30d
    A3. Registro INDAUTOR e IMPI      :crit, a3, 2026-07-01, 30d
    A5. Despliegue piloto CUTonalá    :crit, a5, 2026-08-15, 45d
    A6. Capacitación de personal      :crit, a6, 2026-09-15, 25d
    A8. Negociación contratos prepas  :crit, a8, 2026-11-01, 60d
    A9. Puesta en marcha 2 prepas     :crit, a9, 2027-02-01, 45d
    section Secundarias
    A4. Adquisición kits demo         :a4, 2026-07-15, 25d
    A7. Jornadas demo en prepas       :a7, 2026-10-01, 60d
    A10. Auditoría y cierre ejercicio :a10, 2027-04-15, 30d
```
*Figura 9. Cronograma de ejecución anual en diagrama de Gantt y Ruta Crítica [RC].*

---
""")

    # -------------------------------------------------------------
    # SECCIÓN 7: INVERSIONES, COSTOS Y EVALUACIÓN FINANCIERA (Páginas 7 y 8)
    # -------------------------------------------------------------
    md.append("""## 7. Inversiones, Costos, Ingresos y Evaluación Financiera

### 7.1 Presupuesto de inversión inicial (CAPEX): $180,000 MXN
El requerimiento total de capital semilla asciende a **$180,000.00 MXN**, desglosado con total rigor en cinco partidas analíticas en la Tabla 11. Cada rubro fue verificado para garantizar cero doble cómputo frente a los costos operativos (OPEX):

| Partida de Inversión Inicial | Concepto y Destino Específico del Gasto | Monto Asignado (MXN) |
|---|---|---|
| **P1. Pulido técnico y desarrollo de software** | Auditoría de código, optimización del motor criptográfico HMAC y APIs | $75,000.00 MXN |
| **P2. Infraestructura cloud y servicios web** | Reservación de instancias cloud, balanceadores y licencias por 12 meses | $20,000.00 MXN |
| **P3. Propiedad intelectual y trámites** | Derechos de registro de software ante INDAUTOR y registro de marca IMPI (Tarifa oficial de **$3,126.41 MXN** IVA incluido por clase; IMPI, 2026) | $25,000.00 MXN |
| **P4. Hardware demo y material comercial** | Terminales móviles demo (**$13,500 MXN**) y dossiers impresos con carpetas (**$6,500 MXN**) | **$20,000.00 MXN** |
| **P5. Fondo de reserva y contingencia operativa** | Colchón financiero para mitigar desfasamientos en cobros institucionales | $40,000.00 MXN |
| **Total de Inversión Inicial Requerida (CAPEX)** | **Presupuesto consolidado financiado con capital semilla** | **$180,000.00 MXN** |

*Tabla 11. Estructura analítica de asignación de capital semilla (CAPEX: $180,000 MXN).*

### 7.2 Estructura de costos operativos (OPEX)
Los egresos operativos abarcan infraestructura en la nube, soporte técnico, viáticos de inducción, servicios contables y licencias. Totalizan **$95,000 MXN en el Año 1**, **$225,000 MXN en el Año 2** y **$426,000 MXN en el Año 3**.

### 7.3 Proyecciones de ingresos trienales (Pesos MXN)
Los ingresos brutos se sustentan en las cuotas anuales de suscripción ($48k por CU y $24k por preparatoria) y las cuotas de inducción/setup ($5k a $15k). En el Año 1 operan **3 planteles** (el campus piloto **CUTonalá** sin costo de suscripción pero con $15,000 MXN de setup en 3 almacenes, más **2 contratos comerciales** de prepas SEMS a $24,000 MXN cobradas por anticipado al arranque del ciclo B = $48,000 MXN), generando **$63,000 MXN**. Los ingresos crecen a **$324,000 MXN en el Año 2** (8 sedes) y alcanzan **$850,000 MXN en el Año 3** (22 sedes), como detalla la Tabla 12:

| Concepto de Ingreso | Año 1 (Validación) | Año 2 (Crecimiento a 8 planteles) | Año 3 (Consolidación a 22 planteles) |
|---|---|---|---|
| **Planteles Activos en Operación** | **3 Planteles (1 Piloto CUTonalá sin costo + 2 Prepas comerciales)** | **8 Sedes (3 Centros Universitarios + 5 Preparatorias)** | **22 Sedes (8 Centros Universitarios + 14 Preparatorias)** |
| Suscripciones anuales CUs (@ $48,000) | $0 (Piloto Base CUTonalá) | $144,000 (3 centros) | $384,000 (8 centros) |
| Suscripciones anuales Prepas (@ $24,000) | $48,000 (2 preparatorias cobradas al ciclo B) | $120,000 (5 preparatorias) | $336,000 (14 preparatorias) |
| Talleres de inducción y setup inicial | $15,000 (Setup 3 almacenes CUTonalá) | $60,000 (6 planteles nuevos) | $130,000 (14 planteles nuevos) |
| **Ingresos Totales Brutos Anuales** | **$63,000 MXN** | **$324,000 MXN** | **$850,000 MXN** |

*Tabla 12. Proyección trienal de facturación e ingresos brutos del proyecto (Pesos MXN).*

En la Figura 10 se ilustra el comportamiento trienal de ingresos, costos y flujos netos:

```mermaid
xychart-beta
    title "Evolución Financiera Trienal SIGRE (Miles de Pesos MXN)"
    x-axis ["Año 1 (Piloto)", "Año 2 (Crecimiento)", "Año 3 (Madurez)"]
    y-axis "Monto Anual (Miles MXN)" -50 --> 900
    bar [63, 324, 850]
    bar [95, 225, 426]
    line [-32, 78.9, 296.8]
```
*Figura 10. Comportamiento proyectado de ingresos brutos, costos operativos y Flujo de Efectivo Neto (FEN).*

### 7.4 Estado de Resultados Proforma, Amortización Fiscal y Punto de Equilibrio
La Tabla 13 presenta el Estado de Resultados Proforma trienal, reflejando el cálculo estricto de la amortización de pérdidas fiscales de acuerdo con el Artículo 57 de la Ley del Impuesto sobre la Renta (LISR):

| Rubro Financiero | Año 1 (Validación Piloto) | Año 2 (Expansión Inicial) | Año 3 (Consolidación a Escala) |
|---|---|---|---|
| **Ingresos Brutos por Facturación** | **$63,000** | **$324,000** | **$850,000** |
| (−) Costos de Servidores e Infraestructura Cloud | ($18,000) | ($35,000) | ($65,000) |
| (−) Soporte Técnico y Afinación Operativa en Campo | ($40,000) | ($120,000) | ($240,000) |
| (−) Viáticos de Inducción, Desplazamiento y Material | ($12,000) | ($22,000) | ($45,000) |
| (−) Servicios Contables, Legales y Administrativos | ($15,000) | ($24,000) | ($36,000) |
| (−) Fondo de Mantenimiento de Software y Licencias | ($10,000) | ($24,000) | ($40,000) |
| **Total de Egresos Operativos (OPEX)** | **($95,000)** | **($225,000)** | **($426,000)** |
| **Utilidad de Operación Antes de Impuestos** | **−$32,000** | **+$99,000** | **+$424,000** |
| (−) Impuestos Proyectados (ISR 30% con amortización) | $0 (Pérdida deducible) | **($20,100)** | **($127,200)** |
| **Flujo de Efectivo Neto del Ejercicio (FEN)** | **−$32,000 MXN** | **+$78,900 MXN** | **+$296,800 MXN** |

*Tabla 13. Estado de Resultados Proforma proyectado a tres años (Cifras en Pesos MXN).*

> [!NOTE]
> **Consistencia Aritmética y Criterio Metodológico de Estrés Financiero:**  
> En el Año 1, los costos operativos integran la partida de soporte técnico y depuración en campo por $40,000 MXN para un total de OPEX de **($95,000)**, generando de forma matemáticamente consistente una pérdida operativa de **−$32,000** ($63,000 − $95,000). Esta pérdida fiscal deducible se amortiza formalmente en el Año 2 reduciendo la base gravable de $99,000 MXN a $67,000 MXN, causando un ISR del 30% por **($20,100)** ($67,000 × 0.30) y cuadrando con exactitud el FEN de **+$78,900** ($99,000 − $20,100). En el Año 3, con un EBIT de $424,000 MXN y un ISR del 30% por **($127,200)**, el FEN alcanza **+$296,800**.  
> **Punto de Equilibrio Operativo:** Se alcanza en el **Mes 14** con 6 planteles contratados (3 CUs a $48k y 3 prepas a $24k más ingresos prorrateados de setup), cubriendo íntegramente los egresos mensuales del Año 2 ($18,750 MXN).

### 7.5 Análisis Financiero de Rentabilidad: Proyección FEN, VPN, TIR y Payback
La evaluación se efectuó a una **Tasa Mínima Aceptable de Rendimiento (TMAR) del 15.0% anual**, calculada a partir de los Cetes a 364 días en 7.12% más una prima de riesgo de 7.88%. Los indicadores resultantes se resumen en la Tabla 14:

| Ejercicio Proyectado | Flujo Neto de Caja (FEN) | Tasa de Actualización (15%) | Valor Actual del Flujo (VA) |
|---|---|---|---|
| **Momento Cero (Desembolso de Capital Semilla)** | **($180,000.00 MXN)** | 1.0000 | ($180,000.00 MXN) |
| **Año 1 (Fase de Validación Piloto)** | **($32,000.00 MXN)** | 0.8696 | ($27,826.09 MXN) |
| **Año 2 (Crecimiento a 8 planteles)** | **+$78,900.00 MXN** | 0.7561 | +$59,659.74 MXN |
| **Año 3 (Consolidación a 22 planteles)** | **+$296,800.00 MXN** | 0.6575 | +$195,150.82 MXN |
| **VALOR PRESENTE NETO (VPN @ 15.0%)** | — | — | **+$46,984.47 MXN** |
| **TASA INTERNA DE RETORNO (TIR)** | — | — | **24.27% anual** |
| **RELACIÓN BENEFICIO / COSTO (B/C)** | — | — | **1.23 veces (Método Estándar)** |
| **PERIODO DE RECUPERACIÓN SIMPLE** | — | — | **Mes 29.4 (2.45 años)** |
| **PERIODO DE RECUPERACIÓN DESCONTADO** | — | — | **Mes 33.1 (2.76 años)** |

*Tabla 14. Indicadores consolidados de rentabilidad financiera: VPN, TIR, B/C y Periodos de Recuperación.*

### 7.6 Análisis de Sensibilidad Multiescenario y Umbral de Viabilidad
Para verificar la resiliencia del proyecto ante desviaciones comerciales, la Tabla 15 evalúa tres escenarios:

| Parámetro / Escenario Evaluado | Escenario Pesimista (Adopción Lenta) | Escenario Base (Metas Oficiales) | Escenario Optimista (Alta Tracción) |
|---|---|---|---|
| **Planteles Activos al Cierre Año 3** | **15 planteles** (5 CUs + 10 Prepas) | **22 sedes** (8 CUs + 14 Prepas) | **30 sedes** (12 CUs + 18 Prepas) |
| **Ingresos Brutos en Año 3** | $570,000.00 MXN | $850,000.00 MXN | $1,170,000.00 MXN |
| **Flujo de Efectivo Neto (FEN Año 3)** | $168,700.00 MXN | $296,800.00 MXN | $444,500.00 MXN |
| **Valor Presente Neto (VPN @ 15.0%)** | **−$37,703.62 MXN** | **+$46,984.47 MXN** | **+$143,770.85 MXN** |
| **Tasa Interna de Retorno (TIR)** | **4.79% anual** | **24.27% anual** | **42.41% anual** |
| **Periodo de Recuperación Simple** | Fuera de horizonte (> 36 m) | **Mes 29.4** | **Mes 25.1** |
| **Diagnóstico de Viabilidad** | Déficit financiero (no viable) | **Plenamente viable y solvente** | Alta rentabilidad y expansión |

*Tabla 15. Análisis de sensibilidad financiera a tres escenarios y umbral de viabilidad.*

> [!IMPORTANT]
> **Umbral de Viabilidad Financiera (Break-Even):**  
> Mediante interpolación lineal exacta, el punto donde el VPN se iguala a cero ($VPN = 0$) se sitúa en un FEN para el Año 3 de **$225,342.50 MXN**, lo que equivale a **18.12 planteles** en escala continua. En términos discretos, el proyecto requiere afiliar al menos **19 planteles** seguros al Año 3 (un umbral conservador de sólo el **9.7%** del universo total de la Red UdeG) para cubrir íntegramente la tasa de descuento exigida del 15%.

---
""")

    # -------------------------------------------------------------
    # SECCIÓN 8: ANÁLISIS FODA INSTITUCIONAL Y TÉCNICO (Página 8)
    # -------------------------------------------------------------
    md.append("""## 8. Análisis FODA Institucional y Técnico

La formulación estratégica de SIGRE se sustenta en la matriz FODA institucional, presentada en la Figura 11:

![Figura 11. Matriz oficial de análisis estratégico FODA de la plataforma SIGRE](docs/graficos/foda_oficial_sigre.jpg)  
*Figura 11. Matriz oficial de análisis estratégico FODA de la plataforma SIGRE.*

### ■ FORTALEZAS (F) — Factores Internos de Calidad y Control
- **F1. Software propietario especializado:** Código modular y ligero optimizado para tiempos de despacho inferiores a 25 segundos con sellado criptográfico HMAC-SHA256.
- **F2. Alta usabilidad psicométrica validada:** Calificación de 82.85 puntos en la escala SUS ($n = 50$, Grado A), superando con significancia estadística la media de la industria ($p = 0.035$).
- **F3. Eficiencia en costos de infraestructura:** Arquitectura cloud elástica de bajo consumo que minimiza el OPEX fijo de servidores a sólo $18,000 MXN en el primer año.
- **F4. Alineación regulatoria plena:** Cumplimiento total con la LGPDPPSO y con los ejes de digitalización del Plan de Desarrollo Institucional de la Universidad de Guadalajara.

### ■ OPORTUNIDADES (O) — Factores Externos de Crecimiento y Ahorro
- **O1. Austeridad presupuestal universitaria:** Demanda de soluciones tecnológicas económicas para frenar pérdidas de equipo en mostrador.
- **O2. Modelo B2G por Compra Directa (< 1,000 UMA = $117,310 MXN):** Facilidad de contratación expedita para Secretarios Administrativos y Directores sin licitaciones públicas.
- **O3. Mercado cautivo disponible en la Red UdeG:** Nicho de 196 dependencias donde la meta de 22 planteles al tercer año representa sólo el 11.2% del total.
- **O4. Ahorro económico y sustentabilidad:** Reducción de costos de papelería estimada en **$32,500 MXN** semestrales por plantel y eliminación de más de **32,500** actas y formatos físicos al semestre en la red.

### ■ DEBILIDADES (D) — Factores Internos a Mitigar en Fase Semilla
- **D1. Estructura unipersonal en el arranque:** Dependencia operativa inicial en el fundador, mitigada mediante la incorporación escalonada de soporte técnico a partir del Año 2.
- **D2. Inexistencia de historial comercial institucional:** Barrera de entrada inicial resuelta mediante el despliegue del piloto demostrativo sin costo en CUTonalá.
- **D3. Necesidad de inducción presencial:** Requerimiento de capacitar a auxiliares de mostrador con resistencia tecnológica, solventado con talleres prácticos de 90 minutos.

### ■ AMENAZAS (A) — Factores Externos y Riesgos de Entorno Institucional
- **A1. Rotación de directivos y secretarios de plantel:** Riesgo de discontinuidad contractual al concluir ciclos administrativos, mitigado mediante convenios plurianuales.
- **A2. Desfase en los tiempos de pago institucional:** Trámites de tesorería universitaria que pueden diferir el cobro de facturas entre 30 y 60 días, cubierto por el fondo de contingencia de $40,000 MXN.
- **A3. Interrupciones locales de energía o internet:** Caídas de conectividad en campus periféricos, neutralizadas gracias al modo de micro-custodia offline con almacenamiento local seguro.

---
""")

    # -------------------------------------------------------------
    # SECCIÓN 9: PROPUESTA FORMAL PARA EL INVERSIONISTA (Página 9)
    # -------------------------------------------------------------
    md.append("""## 9. Propuesta Formal para el Inversionista de Capital Semilla

### 9.1 Tesis de inversión y oportunidad de mercado
SIGRE representa una oportunidad de inversión en tecnología educativa (EdTech SaaS) con un mercado cautivo probado, márgenes operativos superiores al 45% a escala y un producto funcional validado empíricamente. Con un requerimiento de capital semilla de **$180,000.00 MXN**, la plataforma resuelve una ineficiencia analógica que cuesta más de $117,000 MXN anuales por plantel, ofreciendo a las autoridades un retorno tangible inmediato.

### 9.2 ¿Cuál es el siguiente paso para que el proyecto siga creciendo?
El capital semilla se aplicará de inmediato en tres frentes estratégicos:
1. **Blindaje de Propiedad Intelectual:** Registro de marca ante el IMPI y derechos de autor del software ante INDAUTOR.
2. **Consolidación del Caso Piloto Base:** Despliegue formal en los 3 almacenes de CUTonalá para certificar métricas de reducción de merma.
3. **Despliegue del Funnel de Ventas en Prepas SEMS:** Fabricación de 4 kits demo de mostrador e inicio de rondas comerciales para captar 2 contratos comerciales en el ciclo 2026-B.

### 9.3 Estructura formal de inversión, instrumento legal y retorno financiero
La inyección de capital se formalizará mediante un Acuerdo de Participación con **Mecanismo de Cash Sweep del 70%** sobre los Flujos de Efectivo Netos (FEN) del proyecto hasta la recuperación total del principal ($180,000 MXN), transicionando a partir de ese momento a una regalía / participación patrimonial del **15% sobre las utilidades netas**:
- **Año 1 (Validación Piloto):** FEN de −$32,000 MXN; el inversionista no percibe flujos ($0 MXN).
- **Año 2 (Crecimiento Inicial):** Con un FEN positivo de **+$78,900 MXN**, el Cash Sweep del 70% entrega al inversionista **$55,230.00 MXN**, reteniendo el fundador **$23,670.00 MXN** (30%). El saldo insoluto de capital pendiente disminuye a **$124,770.00 MXN** ($180,000 − $55,230).
- **Año 3 (Consolidación y Liquidación del Principal):** Con un FEN de **+$296,800 MXN** ($24,733.33/mes), el saldo insoluto restante ($124,770 MXN) se liquida íntegramente en el **Mes 31.2** de operación (a los 7.2 meses del Año 3). En el Tramo 1 (Meses 25 a 31.2), el inversionista recibe el saldo pendiente de $124,770 MXN (70%) y el fundador $53,473 MXN (30%). En el Tramo 2 (Meses 31.3 a 36), se activa la participación del 15%: el inversionista percibe $17,784 MXN y el fundador $100,773 MXN (85%). En total, en el Año 3 el inversionista recibe **$142,554.00 MXN** y el fundador **$154,246.00 MXN** ($142,554 + $154,246 = $296,800 MXN exacto).
- **Retorno Trienal Acumulado:** El inversionista recupera un total consolidado de **$197,784.00 MXN** ($55,230 en Año 2 + $142,554 en Año 3), alcanzando una TIR trienal del 3.53%.
- **Retorno a 5 Años en Escenario Base Estable:** En los Años 4 y 5, manteniendo los flujos del Año 3 ($296,800 MXN/año), la participación del 15% otorga al inversionista **$44,520.00 MXN anuales**, mientras que el fundador recibe **$252,280.00 MXN anuales**. El retorno quinquenal acumulado alcanza **$286,824.00 MXN**, elevando la **TIR del inversionista al 15.62% anual** (superior a la TMAR institucional del 15.0%).
- **Retorno a 5 Años con Escalamiento Regional a UPES (Escenario Expansión):** Al expandir hacia universidades estatales de la región, los ingresos brutos alcanzan **1.21M MXN** en el Año 4 y **1.93M MXN** en el Año 5 con márgenes operativos del **32.0%** (FEN de **387.2k MXN** y **617.6k MXN**). El 15% del inversionista asciende a **$58,080.00 MXN** en el Año 4 y **$92,640.00 MXN** en el Año 5. El flujo proyectado [−$180,000, $0, $55,230, $142,554, $58,080, $92,640] genera una **TIR para el inversionista del 21.20% anual** y un múltiplo de retorno de 1.93x sobre el capital invertido.

La Tabla 16 sintetiza la evolución de los flujos de retorno para el inversionista en ambos horizontes:

| Periodo de Flujo | Flujo Inversionista (Escenario Base Estable) | Flujo Inversionista (Expansión Regional UPES) | Saldo Insoluto de Capital | Condición Operativa y Tramo de Reparto |
|---|---|---|---|---|
| **Momento 0** | **($180,000.00 MXN)** | **($180,000.00 MXN)** | $180,000.00 MXN | Desembolso de capital semilla pre-semilla |
| **Año 1** | $0.00 MXN | $0.00 MXN | $180,000.00 MXN | FEN negativo (−$32,000); reinversión total |
| **Año 2** | **+$55,230.00 MXN** | **+$55,230.00 MXN** | **$124,770.00 MXN** | Cash Sweep del 70% sobre FEN de +$78,900 |
| **Año 3** | **+$142,554.00 MXN** | **+$142,554.00 MXN** | **$0.00 MXN (Liquidado en Mes 31.2)** | Tramo 1 (70% hasta liq) + Tramo 2 (15% regalía) |
| **Año 4** | **+$44,520.00 MXN** | **+$58,080.00 MXN** | $0.00 MXN | 15% sobre utilidades netas ($296.8k base / $387.2k UPES) |
| **Año 5** | **+$44,520.00 MXN** | **+$92,640.00 MXN** | $0.00 MXN | 15% sobre utilidades netas ($296.8k base / $617.6k UPES) |
| **Total Flujos Recibidos** | **$286,824.00 MXN** | **$348,504.00 MXN** | — | Múltiplo de 1.59x (Base) y 1.93x (Expansión) |
| **Tasa Interna de Retorno (TIR)** | **15.62% anual** | **21.20% anual** | — | **Ambos escenarios superan la TMAR del 15.0%** |

*Tabla 16. Flujos de caja proyectados y Tasa Interna de Retorno (TIR) para el inversionista privado.*

---
""")

    # -------------------------------------------------------------
    # SECCIÓN 10: REFERENCIAS Y ANEXOS (Página 10)
    # -------------------------------------------------------------
    md.append("""## 10. Referencias Bibliográficas (Norma APA 7ma Edición)

* Bangor, A., Kortum, P. T., & Miller, J. T. (2008). An empirical evaluation of the System Usability Scale. *International Journal of Human-Computer Interaction*, 24(6), 574–594. https://doi.org/10.1080/10447310802205776
* Brooke, J. (1996). SUS: A 'quick and dirty' usability scale. In P. W. Jordan, B. Thomas, B. A. Weerdmeester, & A. L. McClelland (Eds.), *Usability evaluation in industry* (pp. 189–194). Taylor & Francis.
* Coordinación General de Planeación y Evaluación. (2026). *Numeralia institucional de la Red Universitaria (corte mayo de 2026)*. Universidad de Guadalajara. http://www.cgpe.udg.mx/numeralia
* Instituto Mexicano de la Propiedad Industrial. (2026). *Tarifa por los servicios que presta el Instituto Mexicano de la Propiedad Industrial: Tarifa oficial de registro de marca ($3,126.41 MXN IVA incluido por clase)*. IMPI. https://www.gob.mx/impi
* Instituto Nacional de Estadística y Geografía. (2026). *Valor de la Unidad de Medida y Actualización (UMA) vigente a partir del 1 de febrero de 2026 ($117.31 MXN diarios)*. INEGI. https://www.inegi.org.mx
* Sapag Chain, N. (2014). *Preparación y evaluación de proyectos* (6ta ed.). McGraw-Hill Interamericana.
* Sauro, J., & Lewis, J. R. (2012). *Quantifying the user experience: Practical statistics for user research*. Morgan Kaufmann. (Referencia a la media estándar de 68 puntos).
* Sistema de Educación Media Superior. (2024). *Directorio estadístico y operativo de escuelas preparatorias de la Red Universitaria*. Universidad de Guadalajara. http://www.sems.udg.mx/directorio
* Universidad de Guadalajara. (2019). *Plan de Desarrollo Institucional 2019-2025: Visión 2030*. Coordinación General de Planeación y Evaluación.

## Anexos Técnicos y Evidencia Experimental

### Anexo A. Evidencia Psicométrica y Validación de Usabilidad SUS ($n = 50$)
El estudio experimental de campo se llevó a cabo en los laboratorios de cómputo y almacén de materiales del Centro Universitario de Tonalá (CUTonalá) durante el ciclo 2026-A. Se aplicó el instrumento estandarizado SUS de 10 ítems (Brooke, 1996) mediante un formulario digital con aleatorización de preguntas directas e inversas. La media obtenida de **82.85 puntos** ($DE = 10.91$, $n = 50$, percentil 91.4, Grado A) y el Alfa de Cronbach de **0.892** confirman la robustez psicométrica y la superioridad ergonómica de la plataforma frente a sistemas transaccionales tradicionales.

### Anexo B. Video Demostrativo E2E y Matriz de Solventación al Dictamen Técnico Docente
El repositorio de código fuente y el video demostrativo de extremo a extremo (*End-to-End*) con la simulación transaccional en tiempo real están disponibles para auditoría técnica en: `https://github.com/erfierro/sigre-platform-core`.

En la Tabla 17 se detalla la solventación punto por punto a las observaciones del dictamen técnico docente de la **Mtra. Abril Adriana Angulo Sherman**:

| Área Evaluada del Dictamen | Dictamen y Observación Docente Emitida | Solventación Técnica y Referencia en el Documento |
|---|---|---|
| **1. Justificación y Costo de Inacción** | Cuantificar el costo de inacción administrativa y mermas por plantel. | Se incorporó el modelo analítico de $117,310 MXN/año por plantel con horas-hombre y mermas. (Sección 1.4 y Tabla 2). |
| **2. Viabilidad Burocrática B2G** | Acreditar la viabilidad legal de contratación frente al marco de compras. | Se fundamentó la contratación por adjudicación directa bajo el tope de 1,000 UMA ($117,310 MXN). (Sección 4.2). |
| **3. Objetivos y Marco Lógico** | Reestructurar objetivos cuantitativos y elaborar la MML bajo CEPAL/BID. | Se fijaron metas a 22 sedes, payback a Mes 31.2 y la MML formal. (Sección 2.2, 2.3 y Tabla 4). |
| **4. Arquitectura y Privacidad** | Especificar la arquitectura tecnológica y el apego normativo de datos. | Arquitectura en 5 capas, HMAC-SHA256 y cumplimiento de la LGPDPPSO. (Sección 5 y Tabla 7). |
| **5. Organización y Salarios** | Eliminar distorsiones en salarios iniciales e incorporar nómina escalonada. | Se estableció la estructura de Fundador Único y nómina escalonada ($120k Año 2 y $240k Año 3). (Sección 6.2 y Tabla 8). |
| **6. Consistencia Financiera Proforma** | Cuadrar la amortización de pérdidas fiscales en Año 2 y retornos de inversión. | Se auditó el ISR del Año 2 ($20,100 MXN) amortizando la pérdida fiscal de −$32,000 MXN. (Sección 7.4 y Tabla 13). |
| **7. Mecanismo al Inversionista** | Detallar el mecanismo de pago y conciliación del capital semilla. | Se estructuró el Cash Sweep del 70% con liquidación en Mes 31.2 y retorno quinquenal. (Sección 9.3 y Tabla 16). |

*Tabla 17. Matriz de solventación al dictamen técnico docente de la Mtra. Abril Adriana Angulo Sherman.*
""")

    return "\n".join(md)

if __name__ == '__main__':
    content = generate_markdown()
    with open('scratch/draft_condensed.md', 'w', encoding='utf-8') as f:
        f.write(content)
    
    words = len(content.split())
    chars = len(content)
    lines = len(content.splitlines())
    print(f"Draft Generated Successfully:")
    print(f"Words: {words}")
    print(f"Characters: {chars}")
    print(f"Lines: {lines}")
