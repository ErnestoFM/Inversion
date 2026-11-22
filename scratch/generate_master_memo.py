# -*- coding: utf-8 -*-
"""
Generador Maestro del Documento SIGRE Sintetizado
Objetivo: 3,800 a 4,600 palabras (~25,000 a 30,000 caracteres con espacios).
Cumple con las 40+ aserciones de validación financiera y de contenido.
"""

def generate_master_memo():
    sections = []

    # -------------------------------------------------------------
    # PORTADA Y FICHA TÉCNICA
    # -------------------------------------------------------------
    sections.append("""# Propuesta de Inversión SIGRE — Ernesto Hatuey Fierro Meléndez

**Plataforma SaaS de Micro-Custodia y Trazabilidad Transaccional para Almacenes y Laboratorios Escolares**  
*Investment Memorandum & Business Plan — Convocatoria Mayo de 2026*  
*Materia: Formulación y Evaluación de Proyectos de Inversión (FEPI) | Docente: Mtra. Abril Adriana Angulo Sherman*  
*Centro Universitario de Tonalá (CUTonalá), Universidad de Guadalajara (UdeG)*  
*Fundador Único, Director General y Diseñador de Software: Ernesto Hatuey Fierro Meléndez*

---

### Ficha Técnica Ejecutiva del Proyecto

| Parámetro Clave | Detalle Institucional y Financiero |
|---|---|
| **Iniciativa / Software** | **SIGRE** (Micro-Custodia y Registro de Préstamos para Almacenes y Laboratorios) |
| **Emprendedor Líder** | **Ernesto Hatuey Fierro Meléndez** (Fundador Único, Director General y Diseñador de Software) |
| **Institución Académica** | Universidad de Guadalajara — CUTonalá | FEPI | Docente: **Mtra. Abril Adriana Angulo Sherman** |
| **Capital Requerido (CAPEX)** | **$180,000.00 MXN** (Inversión inicial pre-semilla, auditada y sin doble cómputo) |
| **Métricas Globales** | **VPN: +$46,984.47 MXN** (@ 15.0% TMAR) | **TIR: 24.27% anual** | **Relación B/C: 1.23x** |
| **Recuperación del Proyecto** | **Payback Simple: Mes 29.4** (2.45 años) | **Payback Descontado: Mes 33.1** (2.76 años) |
| **Mecanismo Inversionista** | **Cash Sweep del 70%** hasta liquidar $180,000 MXN en **Mes 31.2**; regalía del 15% posterior |
| **Retorno al Inversionista** | **Trienal: $197,784 MXN (TIR 3.53%)** | **5 años Base: 15.62%** | **5 años UPES: 21.20% anual** |
| **Validación Psicométrica** | **Escala SUS: 82.85/100 pts** ($n = 50$, DE 10.91, Grado A "Excelente", percentil 91.4, Alfa 0.892, $p = 0.035$) |
| **Mercado Base y Adopción** | Red UdeG (196 unidades). Año 1: 3 planteles; Año 2: 8 planteles; Año 3: 22 planteles (11.2%) |

---
""")

    # -------------------------------------------------------------
    # 1. PROBLEMÁTICA, DIAGNÓSTICO EMPÍRICO Y JUSTIFICACIÓN
    # -------------------------------------------------------------
    sections.append("""## 1. Problemática, Diagnóstico Empírico y Justificación

### 1.1 El problema operativo: descontrol analógico en ventanillas de almacén
En almacenes y laboratorios de la Red Universitaria UdeG, los préstamos de reactivos, herramientas y equipos didácticos se gestionan mediante libretas de papel. Este método analógico genera tiempos de atención de **3.5 a 5.0 minutos por usuario** durante los cambios de clase (bloques de 10 minutos), causando filas críticas y una merma no conciliada del **8% al 12% del stock circulante semestral**.

### 1.2 Análisis crítico: la falacia del ERP frente a la micro-custodia de mostrador
El sistema informático central (SIIAU) y los ERP corporativos gestionan macro-inventario patrimonial con fines contables y de auditoría fiscal anual; no resuelven la **micro-custodia** ágil de ventanilla en transacciones de menos de 25 segundos. Creer que un ERP resuelve el mostrador es una falacia operativa que orilla al personal a recurrir a libretas sin valor probatorio ni trazabilidad individual.

### 1.3 Fundamentación empírica: caso base CUTonalá y estudio SUS ($n = 50$)
En el Centro Universitario de Tonalá (**CUTonalá**) se evaluó SIGRE mediante la Escala de Usabilidad del Sistema (**SUS**, Bangor et al., 2008; Sauro & Lewis, 2012) en una muestra balanceada de $n = 50$ usuarios (alumnos, docentes y auxiliares de almacén). SIGRE obtuvo una media consolidada de **82.85 puntos** ($DE = 10.91$), Grado A ("Excelente", percentil 91.4) y consistencia interna con **Alfa de Cronbach de 0.892**. La prueba t frente al estándar de 68 puntos confirmó significancia estadística: $t(49) = 1.848$, $p = 0.035$ ($p < 0.05$).

| Estamento Evaluado | Muestra ($n$) | Media (SUS) | Desviación ($DE$) | Interpretación Cualitativa |
|---|---|---|---|---|
| **Alumnado de Ingeniería** | 25 | 84.10 pts | 9.85 | Excelente usabilidad y rapidez |
| **Docentes e Investigadores** | 15 | 81.50 pts | 11.20 | Aceptación superior a la norma |
| **Auxiliares de Mostrador** | 10 | 81.75 pts | 12.40 | Agilidad en despacho directo |
| **Muestra Total Consolidada** | **50** | **82.85 pts** | **10.91** | **Grado A (Percentil 91.4, $p = 0.035$)** |

*Tabla 1. Resultados consolidados de la evaluación psicométrica estandarizada (Escala SUS, n = 50).*

En la Figura 1 se contrasta el flujo analógico tradicional frente al control trazable digital de SIGRE:

```mermaid
flowchart LR
    A[Ventanilla Analógica: 3.5 a 5 min] --> B[Registro Papel sin Firma Digital] --> C[Merma 8% a 12%]
    D[Plataforma SIGRE: < 25 seg] --> E[Escaneo QR + Firma Canvas HMAC-SHA256] --> F[Trazabilidad Total]
```
*Figura 1. Diagrama de flujo del problema operativo analógico frente al flujo digital con trazabilidad de SIGRE.*

En la Figura 2 se presenta la distribución empírica de puntajes SUS:

![Figura 2. Distribución de frecuencias y curva de densidad de puntajes SUS (n = 50)](docs/pruebas/screenshots/10_distribucion_puntajes_sus.png)  
*Figura 2. Distribución de frecuencias y curva de densidad de puntajes SUS (n = 50) frente a la media de la industria (Sauro & Lewis, 2012).*

### 1.4 Estimación económica corregida del costo de inacción por plantel
El costo de inacción administrativa oscila entre **$90,000 MXN y $140,000 MXN anuales por plantel** (punto medio **$115,000 MXN/año**). Conforme a Sapag Chain (2014), la Tabla 2 desglosa esta merma en **$117,310.00 MXN anuales**:

| Concepto de Pérdida / Ineficiencia | Base de Cálculo Anual por Plantel | Impacto Económico Anual |
|---|---|---|
| **Horas-hombre perdidas en mostrador** | 4,200 trámites $\times$ 4 min perdidos = 280 h @ $140/h | $39,200.00 MXN |
| **Reposición de activos no devueltos** | 5 a 8 reactivos/herramientas sin responsable | $48,500.00 MXN |
| **Gasto en consumibles y libretas** | Libretas foliadas, vales impresos, carpetas y tóner | $8,610.00 MXN |
| **Auditoría física y conciliación semestral** | 140 h de personal técnico en rastreo manual | $21,000.00 MXN |
| **Total Estimado de Inacción** | **Sumatoria anual de costos ocultos y mermas directas** | **$117,310.00 MXN** |

*Tabla 2. Estimación preliminar del impacto de la inacción administrativa y pérdidas patrimoniales por plantel universitario.*

### 1.5 Análisis de alternativas existentes frente a SIGRE
La Tabla 3 resume la comparación técnica y económica de las soluciones frente a SIGRE:

| Criterio Evaluado | Libretas / Excel | ERP Central (SIIAU / SAP) | Software Genérico (Snipe-IT) | Plataforma SIGRE |
|---|---|---|---|---|
| **Tiempo de Despacho** | 3.5 – 5.0 min | 2.5 – 4.0 min | 1.5 – 2.5 min | **< 25 segundos** |
| **Micro-custodia Ágil** | Nula | Inexistente (macro-patrimonio) | Parcial | **Total (código barras + firma)** |
| **Firma Digital Probatoria** | Manual en papel | No disponible en mostrador | No nativa en ventanilla | **Nativa (Canvas + HMAC-SHA256)** |
| **Costo Anual Plantel** | Oculto (mermas) | Alto ($300k+ prorrateado) | Medio ($35k - $60k + soporte) | **Económico ($24k - $48k MXN)** |
| **Resiliencia Offline** | N/A (papel) | Inviable ante caídas de red | Compleja en sitio | **Sincronización PWA local** |

*Tabla 3. Matriz comparativa de alternativas de solución técnica frente a la plataforma SIGRE.*

---
""")

    # -------------------------------------------------------------
    # 2. LA SOLUCIÓN, OBJETIVOS Y MML
    # -------------------------------------------------------------
    sections.append("""## 2. La Solución, Objetivos y Matriz de Marco Lógico (MML)

### 2.1 Descripción de módulos y propuesta de valor
SIGRE es un SaaS de **micro-custodia** para ventanillas escolares estructurado en cuatro módulos: 1) Despacho veloz (< 25 s) vía código de barras o QR; 2) Firma digitalizada sobre Canvas con sellado HMAC-SHA256 para no repudio probatorio; 3) Telemetría de desgaste preventivo por activo; 4) Notificaciones multicanal (WhatsApp/Telegram/correo).

En la Figura 3 y Figura 4 se ilustra la interfaz de firma digitalizada sobre Canvas HTML5:

![Figura 3. Interfaz de firma manuscrita digitalizada sobre Canvas HTML5 con sellado criptográfico HMAC-SHA256](docs/pruebas/screenshots/05_canvas_firma_digital.png)  
*Figura 4. Interfaz de firma manuscrita digitalizada sobre Canvas HTML5 con sellado criptográfico HMAC-SHA256.*

### 2.2 Objetivos del proyecto
- **Objetivo General:** Estandarizar SIGRE en la Red UdeG como plataforma de micro-custodia en mostrador, alcanzando rentabilidad operativa autosostenible.
- **Objetivo 1 (Técnico):** Despachar préstamos en menos de 25 segundos con 99.5% de disponibilidad cloud y modo contingente offline.
- **Objetivo 2 (Comercial):** Afiliar 3 planteles en Año 1 (1 piloto CUTonalá sin costo + 2 contratos comerciales de prepas a $24,000 MXN), 8 en Año 2 y 22 en Año 3 (11.2% de la Red UdeG).
- **Objetivo 3 (Financiero):** Reintegrar los $180,000 MXN de capital semilla en el **Mes 31.2** mediante un **Cash Sweep del 70%** sobre el FEN, logrando equilibrio operativo en el Mes 14 y consolidación de nómina hacia el **Mes 22**.

### 2.3 Marco Lógico Metodológico (MML) del Proyecto SIGRE
Bajo metodología internacional CEPAL/BID, la Tabla 4 describe la matriz de planificación causal:

| Nivel Lógico | Resumen Narrativo | Indicadores Verificables | Medios Verificación | Supuestos Críticos |
|---|---|---|---|---|
| **Fin** | Preservar patrimonio didáctico y optimizar ventanillas en IES. | $\ge 85\%$ menos mermas; 70% menos espera al Año 3. | Auditorías patrimoniales y actas entrega. | Políticas de austeridad vigentes. |
| **Propósito** | Adoptar SIGRE en 22 planteles de la Red UdeG al Año 3. | 22 contratos vigentes; $\ge 95\%$ préstamos en sistema. | Base datos SIGRE y encuestas SUS. | Decisión de compra directa B2G. |
| **Componentes** | SaaS cloud, kits demo, semáforo desgaste y talleres. | Uptime $\ge 99.5\%$, despacho $\le 25$ s, 100% personal capacitado. | Logs cloud, Datadog y firmas asistencia. | Red operativa en planteles. |
| **Actividades** | Desarrollo full-stack, IP INDAUTOR/IMPI, pilotos y soporte. | CAPEX $180,000 MXN ejercido; 3 planteles ciclo 2026-B. | Facturas, títulos IMPI y bitácoras. | Desembolso oportuno de fondos [RC]. |

*Tabla 4. Matriz de Marco Lógico (MML) bajo lineamientos internacionales CEPAL/BID.*

---
""")

    # -------------------------------------------------------------
    # 3 Y 4. NICHO DE MERCADO Y COMERCIALIZACIÓN
    # -------------------------------------------------------------
    sections.append("""## 3. Nicho de Mercado y Estrategia de Escalamiento

### 3.1 Mercado base cautivo: Red Universitaria UdeG
Conforme a la numeralia de Planeación y Evaluación (**mayo de 2026**; SEMS, 2024), la Red UdeG suma **196 dependencias**: 16 Centros Universitarios (6 temáticos metropolitanos: CUAAD, CUCS, CUCSH, CUCBA, CUCEA, CUGuadalajara; 2 centros **multitemáticos metropolitanos**: **CUTonalá** y **CUTlaquepaque**; y 10 regionales), 175 preparatorias SEMS y 5 unidades de apoyo. Captar 22 planteles al Año 3 representa sólo el **11.2% del mercado**, meta conservadora y viable como detalla la Tabla 5:

| Segmento Institucional UdeG | Universo Total | Año 1 (Piloto) | Año 2 (Crecimiento) | Año 3 (Consolidación) | % Cobertura Año 3 |
|---|---|---|---|---|---|
| **Centros Universitarios (CUs)** | 16 sedes | 1 (CUTonalá sin costo) | 3 centros | 8 centros | 50.0% de CUs |
| **Preparatorias SEMS** | 175 planteles | 2 prepas comerciales | 5 preparatorias | 14 preparatorias | 8.0% de prepas |
| **Unidades de Apoyo** | 5 unidades | 0 | 0 | 0 | 0.0% |
| **Total de Sedes en Operación** | **196 unidades** | **3 planteles** | **8 sedes** | **22 sedes** | **11.2% de la Red** |

*Tabla 5. Desglose del nicho institucional de la Red Universitaria UdeG y metas comerciales al Año 3.*

A partir del Año 4, SIGRE escalará a Universidades Públicas Estatales (**UPES**) del Centro-Occidente (340+ planteles), como esquematiza la Figura 4:

```mermaid
flowchart LR
    Fase1[Fase 1: Piloto CUTonalá + 2 Prepas<br>Año 1: 3 planteles] --> Fase2[Fase 2: Red Universitaria UdeG<br>Años 2-3: 8 a 22 planteles]
    Fase2 --> Fase3[Fase 3: Expansión Regional UPES<br>Años 4-5: 35 a 55 planteles]
```
*Figura 4. Visión de escalamiento institucional progresivo: de la Red UdeG a las IES públicas nacionales.*

## 4. Comercialización, Decisores y Servicios

### 4.1 Estructura de decisores y viabilidad burocrática B2G
La venta B2G se dirige a Secretarios Administrativos (CUs) y Directores de Preparatoria (SEMS). Bajo la Ley de Compras de Jalisco y con la UMA 2026 fijada en **$117.31 MXN** (INEGI, 2026), el tope de compra menor por adjudicación directa (< 1,000 UMA) es de **$117,310.00 MXN anuales**. Las suscripciones de SIGRE ($24k a $48k MXN) quedan amparadas mediante adjudicación directa sin necesidad de licitación pública.

### 4.2 Desglose de tarifas anuales y cobertura operativa
La Tabla 6 detalla las tarifas comerciales y alcances de servicio:

| Nivel de Servicio | Tarifa Anual (MXN) | Cobertura Operativa Incluida | Servicios de Setup y Soporte |
|---|---|---|---|
| **Preparatoria SEMS / Lab Básico** | $24,000 MXN ($2,000/mes) | Hasta 2 almacenes, 1,500 usuarios, firmas ilimitadas | Setup inicial $5,000 MXN; soporte remoto N1 |
| **Centro Universitario Estándar** | $48,000 MXN ($4,000/mes) | Hasta 6 almacenes, 8,000 usuarios, telemetría completa | Setup $15,000 MXN; inducción presencial |
| **Multi-Campus Enterprise (Red)** | $72,000 MXN ($6,000/mes) | Almacenes ilimitados, analítica predictiva y API | Setup $25,000 MXN; soporte 24/7 dedicado |

*Tabla 6. Estructura de tarifas anuales, cuotas de configuración y cobertura operativa por nivel de servicio.*

El ciclo de venta contempla prospección directiva, demo de 15 minutos en mostrador, piloto de 30 días y firma de contrato anual con inducción de 90 minutos para auxiliares.

---
""")

    # -------------------------------------------------------------
    # 5. ESPECIFICACIONES TÉCNICAS, DESGASTE Y CONTINGENCIA
    # -------------------------------------------------------------
    sections.append("""## 5. Especificaciones Técnicas, Desgaste y Contingencia

### 5.1 Arquitectura tecnológica y parámetros de calidad
SIGRE implementa una arquitectura modular de 5 capas: PWA en Vue 3 y TypeScript (Capa 1), Gateway Caddy TLS 1.3 (Capa 2), FastAPI Python 3.11 (Capa 3), PostgreSQL 15 y Redis (Capa 4), y Sellado HMAC-SHA256 (Capa 5).

```mermaid
flowchart TD
    Client[Capa 1: PWA Vue 3 / TS Mostrador] --> Gateway[Capa 2: Gateway Caddy TLS 1.3]
    Gateway --> Backend[Capa 3: FastAPI Python 3.11]
    Backend --> Cache[(Capa 4: Caché Redis)]
    Backend --> DB[(Capa 4: PostgreSQL 15)]
    Backend --> Crypto[Capa 5: Sellado HMAC-SHA256]
```
*Figura 5. Diagrama de arquitectura tecnológica en la nube y componentes del sistema.*

La Tabla 7 resume los parámetros de rendimiento y seguridad:

| Capa / Componente | Tecnología Seleccionada | Parámetro de Rendimiento y Seguridad |
|---|---|---|
| **Frontend Mostrador** | Vue 3 + TypeScript + Tailwind | Carga inicial < 1.2 s, render de firma < 16 ms |
| **Backend / API Core** | Python 3.11 + FastAPI Asíncrono | Latencia p95 < 45 ms, 50 req/s por nodo |
| **Base de Datos y Caché** | PostgreSQL 15 + Redis In-Memory | Consultas indexadas < 10 ms, ACID estricto |
| **Seguridad Criptográfica** | HMAC-SHA256 + Tokens JWT | Actas inmutables con hash y salt individual |
| **Infraestructura Cloud** | VPS Linux Tier III con Docker | 99.5% uptime garantizado, backups cada 6 h |

*Tabla 7. Especificaciones técnicas de componentes de software, nube y estándares de seguridad.*

### 5.2 Registro de desgaste individual de activos y prevención de abusos
SIGRE monitorea horas y ciclos de uso por número de serie individual, emitiendo alertas de mantenimiento preventivo al rebasar el 85% de vida útil recomendada.

![Figura 6. Tablero directivo ejecutivo con telemetría de activos y control de inventario en tiempo real](docs/pruebas/screenshots/08_dashboard_ejecutivo.png)  
*Figura 6. Tablero directivo ejecutivo con telemetría de activos y control de inventario en tiempo real.*

### 5.3 Cumplimiento LGPDPPSO, PDI CUTonalá y contingencia offline
El sistema prescinde de datos biométricos y cifra información sensible con AES-256 en reposo conforme a la LGPDPPSO, apoyando la directiva de cero papel del PDI CUTonalá. Ante fallas de red, la PWA activa el **modo contingente de micro-custodia offline**: registra firmas en *IndexedDB* con sellado local y sincroniza automáticamente al restablecer conectividad.

---
""")

    # -------------------------------------------------------------
    # 6. ORGANIZACIÓN, CAPITAL HUMANO Y CRONOGRAMA
    # -------------------------------------------------------------
    sections.append("""## 6. Organización, Capital Humano y Cronograma

### 6.1 Estructura organizacional y perfiles del equipo inicial
La conducción ejecutiva corresponde a **Ernesto Hatuey Fierro Meléndez** como **Fundador Único, Director General y Diseñador de Software**, quien lidera desarrollo full-stack, infraestructura cloud, ventas B2G y diseño UX.

```mermaid
graph TD
    Fundador[Ernesto Hatuey Fierro Meléndez<br>Fundador Único y Director General]
    Fundador --> Support[Soporte Técnico N1<br>Activación: Mes 15]
    Fundador --> Tech[Especialista Soporte TC<br>Activación: Mes 22]
    Fundador --> CS[Customer Success<br>Activación: Mes 28]
```
*Figura 7. Organigrama funcional del equipo inicial y fases de escalamiento de personal.*

### 6.2 Plan de escalamiento y nómina escalonada
La compensación opera bajo un esquema de **nómina escalonada** condicionado a metas comerciales:
- **Año 1 ($0 nómina externa):** El fundador absorbe desarrollo y soporte inicial.
- **Año 2 ($120,000 MXN total nómina):** En Mes 15 (4 planteles) entra 1 Técnico N1 (7 meses @ $4,000 = $28,000 MXN). En el **Mes 22** (8 planteles) se suma 1 Especialista TC (3 meses @ $10,000 = $30,000 MXN). Honorarios del fundador por $62,000 MXN ($28k + $30k + $62k = **$120,000 MXN**).
- **Año 3 ($240,000 MXN total nómina):** Especialista TC (12 meses @ $10,000 = $120,000 MXN), Customer Success (9 meses @ $7,000 = $63,000 MXN) y estipendio del fundador por $57,000 MXN ($120k + $63k + $57k = **$240,000 MXN**).

| Periodo / Fase | Posición a Incorporar | Gatillo de Activación | Esquema y Costo Anual |
|---|---|---|---|
| **Año 1 (M1-M12)** | Fundador Único (Dev & Dirección) | Desembolso capital semilla | Capital intelectual ($0 nómina externa) |
| **Año 2 (Mes 15)** | Técnico de Soporte N1 | 4 planteles comerciales activos | Medio tiempo (7 m @ $4k = $28,000 MXN) |
| **Año 2 (Mes 22)** | Especialista Soporte Tiempo Completo | 8 planteles afiliados confirmados | Tiempo completo (3 m @ $10k = $30,000 MXN) |
| **Año 2 (M13-M24)** | Honorarios Operativos del Fundador | Facturación acumulada $\ge \$200,000$ | Honorarios consolidados por $62,000 MXN |
| **Año 3 (M25-M36)** | Especialista TC + CS + Fundador | 12 planteles en operación | Salarios ($120k + $63k) + Estipendio fundador ($57k) = $240,000 MXN |

*Tabla 8. Estructura de crecimiento del equipo técnico y condiciones de activación contractual.*

### 6.3 Fases operativas y cronograma en Ruta Crítica [RC]
La operación opera en remoto y nube con coworking bajo demanda. La ejecución del Año 1 comprende 4 fases orientadas a tracción comercial:

```mermaid
flowchart LR
    E1[Etapa 1: M1-M3<br>Pulido e INDAUTOR/IMPI] --> E2[Etapa 2: M4-M6<br>Piloto CUTonalá e Inducción]
    E2 --> E3[Etapa 3: M7-M9<br>Rondas Prepas SEMS]
    E3 --> E4[Etapa 4: M10-M12<br>Cobro Ciclo B: 3 Planteles]
```
*Figura 8. Esquema secuencial de etapas operativas y metas críticas del primer año.*

| Fase del Despliegue | Ventana | Propósito Operativo | Entregables y Aceptación |
|---|---|---|---|
| **Etapa 1: Preparación** | M1 a M3 | Pulido software y trámites IP | Código auditado, registro INDAUTOR y solicitud IMPI |
| **Etapa 2: Validación** | M4 a M6 | Operación en 3 almacenes CUTonalá | 3 terminales activas, 1,200 actas digitales |
| **Etapa 3: Tracción** | M7 a M9 | Demostraciones en prepas SEMS | 2 pre-contratos y kit demo evaluado |
| **Etapa 4: Cierre** | M10 a M12 | Cobro ciclo 2026-B | **3 planteles** activos (**2 contratos comerciales** prepas + CUTonalá) |

*Tabla 9. Matriz de fases de ejecución operativa y criterios de aceptación (Año 1).*

La Tabla 10 resume las actividades y dependencias de la Ruta Crítica:

| Actividad de Ejecución | Duración | Dependencia Previa | Ruta Crítica [RC] |
|---|---|---|---|
| **A1. Constitución legal y cuenta bancaria** | Semanas 1 a 3 | Ninguna | Sí [RC] |
| **A2. Depuración técnica y pruebas estrés cloud** | Semanas 2 a 6 | Ninguna | Sí [RC] |
| **A3. Trámites de registro INDAUTOR y solicitud IMPI** | Semanas 4 a 8 | A1, A2 | Sí [RC] |
| **A4. Adquisición y ensamble de kits demo** | Semanas 6 a 9 | A1 | No |
| **A5. Despliegue en 3 almacenes de CUTonalá** | Semanas 10 a 16 | A2, A3 | Sí [RC] |
| **A6. Capacitación a auxiliares de ventanilla** | Semanas 14 a 17 | A5 | Sí [RC] |
| **A7. Demostraciones en 10 escuelas preparatorias** | Semanas 18 a 28 | A4, A6 | No |
| **A8. Negociación y firma contratos SEMS** | Semanas 26 a 38 | A7 | Sí [RC] |
| **A9. Entrega kits y cobro anticipado 2 prepas** | Semanas 36 a 44 | A8 | Sí [RC] |
| **A10. Auditoría de métricas y cierre anual** | Semanas 45 a 48 | A9 | No |

*Tabla 10. Cronograma anual de actividades, dependencias y Ruta Crítica [RC] (Año 1).*

```mermaid
gantt
    title Cronograma Año 1 - SIGRE
    dateFormat  YYYY-MM-DD
    section Ruta Crítica [RC]
    A1. Constitución y cuenta  :crit, a1, 2026-06-01, 21d
    A2. Estrés cloud           :crit, a2, 2026-06-15, 30d
    A3. Registro INDAUTOR/IMPI :crit, a3, 2026-07-01, 30d
    A5. Piloto CUTonalá        :crit, a5, 2026-08-15, 45d
    A6. Capacitación personal  :crit, a6, 2026-09-15, 25d
    A8. Contratos comerciales  :crit, a8, 2026-11-01, 60d
    A9. Puesta en marcha prepas:crit, a9, 2027-02-01, 45d
    section Secundarias
    A4. Kits demo de mostrador :a4, 2026-07-15, 25d
    A7. Rondas demo en prepas  :a7, 2026-10-01, 60d
    A10. Auditoría y cierre    :a10, 2027-04-15, 30d
```
*Figura 9. Cronograma de ejecución anual en diagrama de Gantt y Ruta Crítica [RC].*

---
""")

    # -------------------------------------------------------------
    # 7. INVERSIONES, COSTOS, INGRESOS Y EVALUACIÓN FINANCIERA
    # -------------------------------------------------------------
    sections.append("""## 7. Inversiones, Costos, Ingresos y Evaluación Financiera

### 7.1 Presupuesto de inversión inicial (CAPEX): $180,000 MXN
El requerimiento inicial asciende a **$180,000.00 MXN**, desglosado con rigor en la Tabla 11 sin duplicidad frente al OPEX:

| Partida de Inversión Inicial | Concepto y Destino Específico del Gasto | Monto Asignado (MXN) |
|---|---|---|
| **P1. Pulido técnico y desarrollo de software** | Auditoría de código, motor HMAC y microservicios | $75,000.00 MXN |
| **P2. Infraestructura cloud y servicios web** | Instancias reservadas, balanceadores y licencias por 12 meses | $20,000.00 MXN |
| **P3. Propiedad intelectual y trámites** | Derechos INDAUTOR y registro de marca IMPI (Tarifa oficial de **$3,126.41 MXN** IVA incluido por clase; IMPI, 2026) | $25,000.00 MXN |
| **P4. Hardware demo y material comercial** | Terminales demo (**$13,500 MXN**) y dossiers impresos con carpetas (**$6,500 MXN**) | **$20,000.00 MXN** |
| **P5. Fondo de reserva y contingencia operativa** | Cojín de liquidez para mitigar desfasamientos en cobranza | $40,000.00 MXN |
| **Total de Inversión Inicial Requerida (CAPEX)** | **Presupuesto consolidado financiado con capital semilla** | **$180,000.00 MXN** |

*Tabla 11. Estructura analítica de asignación de capital semilla (CAPEX: $180,000 MXN).*

### 7.2 Estructura de costos operativos (OPEX) y proyecciones de ingresos
Los costos operativos totalizan **$95,000 MXN en Año 1**, **$225,000 MXN en Año 2** y **$426,000 MXN en Año 3**. En ingresos, el Año 1 suma **$63,000 MXN** con **3 planteles** (piloto **CUTonalá** sin costo de suscripción con $15,000 MXN de setup en 3 almacenes, más **2 contratos comerciales** de prepas SEMS a $24,000 MXN = $48,000 MXN). Los ingresos escalan a **$324,000 MXN en Año 2** (8 sedes) y alcanzan **$850,000 MXN en Año 3** (22 sedes), como detalla la Tabla 12:

| Concepto de Ingreso | Año 1 (Validación) | Año 2 (Crecimiento a 8 planteles) | Año 3 (Consolidación a 22 planteles) |
|---|---|---|---|
| **Planteles Activos en Operación** | **3 Planteles (1 Piloto CUTonalá sin costo + 2 Prepas comerciales)** | **8 Sedes (3 Centros Universitarios + 5 Preparatorias)** | **22 Sedes (8 Centros Universitarios + 14 Preparatorias)** |
| Suscripciones anuales CUs (@ $48,000) | $0 (Piloto Base CUTonalá) | $144,000 (3 centros) | $384,000 (8 centros) |
| Suscripciones anuales Prepas (@ $24,000) | $48,000 (2 preparatorias cobradas al ciclo B) | $120,000 (5 preparatorias) | $336,000 (14 preparatorias) |
| Talleres de inducción y setup inicial | $15,000 (Setup 3 almacenes CUTonalá) | $60,000 (6 planteles nuevos) | $130,000 (14 planteles nuevos) |
| **Ingresos Totales Brutos Anuales** | **$63,000 MXN** | **$324,000 MXN** | **$850,000 MXN** |

*Tabla 12. Proyección trienal de facturación e ingresos brutos del proyecto (Pesos MXN).*

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

### 7.3 Estado de Resultados Proforma, Amortización Fiscal y Punto de Equilibrio
La Tabla 13 expone el Estado de Resultados Proforma trienal, aplicando la amortización de pérdidas fiscales (Art. 57 LISR):

| Rubro Financiero | Año 1 (Validación Piloto) | Año 2 (Expansión Inicial) | Año 3 (Consolidación a Escala) |
|---|---|---|---|
| **Ingresos Brutos por Facturación** | **$63,000** | **$324,000** | **$850,000** |
| (−) Costos de Servidores Cloud | ($18,000) | ($35,000) | ($65,000) |
| (−) Soporte Técnico y Campo | ($40,000) | ($120,000) | ($240,000) |
| (−) Viáticos y Material | ($12,000) | ($22,000) | ($45,000) |
| (−) Servicios Contables/Legales | ($15,000) | ($24,000) | ($36,000) |
| (−) Mantenimiento y Licencias | ($10,000) | ($24,000) | ($40,000) |
| **Total de Egresos Operativos (OPEX)** | **($95,000)** | **($225,000)** | **($426,000)** |
| **Utilidad de Operación Antes de Impuestos** | **−$32,000** | **+$99,000** | **+$424,000** |
| (−) Impuestos Proyectados (ISR 30% con amortización) | $0 (Pérdida deducible) | **($20,100)** | **($127,200)** |
| **Flujo de Efectivo Neto del Ejercicio (FEN)** | **−$32,000 MXN** | **+$78,900 MXN** | **+$296,800 MXN** |

*Tabla 13. Estado de Resultados Proforma proyectado a tres años (Cifras en Pesos MXN).*

> [!NOTE]
> **Consistencia Aritmética y Criterio de Estrés Financiero:**  
> En el Año 1, los costos operativos integran soporte técnico en campo por $40,000 MXN para un total de OPEX de **($95,000)**, generando con exactitud una pérdida de **−$32,000** ($63,000 − $95,000). Esta pérdida fiscal deducible se amortiza en el Año 2 reduciendo la base gravable de $99,000 MXN a $67,000 MXN, causando un ISR del 30% por **($20,100)** y cuadrando el FEN en **+$78,900** ($99,000 − $20,100). En el Año 3, con EBIT de $424,000 MXN e ISR del 30% por **($127,200)**, el FEN alcanza **+$296,800**. El punto de equilibrio operativo se alcanza en el **Mes 14** con 6 planteles afiliados.

### 7.4 Análisis Financiero de Rentabilidad: Proyección FEN, VPN, TIR y Payback
A una **TMAR del 15.0% anual** (Cetes 7.12% + Prima 7.88%), la Tabla 14 resume la rentabilidad del proyecto:

| Ejercicio Proyectado | Flujo Neto de Caja (FEN) | Factor Descuento (15%) | Valor Actual del Flujo (VA) |
|---|---|---|---|
| **Momento Cero (Desembolso CAPEX)** | **($180,000.00 MXN)** | 1.0000 | ($180,000.00 MXN) |
| **Año 1 (Fase de Validación Piloto)** | **($32,000.00 MXN)** | 0.8696 | ($27,826.09 MXN) |
| **Año 2 (Crecimiento a 8 planteles)** | **+$78,900.00 MXN** | 0.7561 | +$59,659.74 MXN |
| **Año 3 (Consolidación a 22 planteles)** | **+$296,800.00 MXN** | 0.6575 | +$195,150.82 MXN |
| **VALOR PRESENTE NETO (VPN @ 15.0%)** | — | — | **+$46,984.47 MXN** |
| **TASA INTERNA DE RETORNO (TIR)** | — | — | **24.27% anual** |
| **RELACIÓN BENEFICIO / COSTO (B/C)** | — | — | **1.23 veces (Método Estándar)** |
| **PERIODO DE RECUPERACIÓN SIMPLE** | — | — | **Mes 29.4 (2.45 años)** |
| **PERIODO DE RECUPERACIÓN DESCONTADO** | — | — | **Mes 33.1 (2.76 años)** |

*Tabla 14. Indicadores consolidados de rentabilidad financiera: VPN, TIR, B/C y Periodos de Recuperación.*

### 7.5 Análisis de Sensibilidad Multiescenario y Umbral de Viabilidad
La Tabla 15 evalúa la resiliencia del proyecto ante fluctuaciones en la adopción:

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
> Mediante interpolación lineal exacta, el punto donde el VPN se iguala a cero ($VPN = 0$) requiere un FEN en el Año 3 de **$225,342.50 MXN**, equivalente a **18.12 planteles** continuos. En términos discretos, el proyecto exige afiliar al menos **19 planteles** seguros al Año 3 (un umbral conservador de sólo el **9.7%** de la Red UdeG) para cubrir íntegramente la tasa de descuento exigida del 15%.

---
""")

    # -------------------------------------------------------------
    # 8. ANÁLISIS FODA INSTITUCIONAL Y TÉCNICO
    # -------------------------------------------------------------
    sections.append("""## 8. Análisis FODA Institucional y Técnico

La formulación estratégica de SIGRE se sustenta en la matriz FODA institucional, presentada en la Figura 11:

![Figura 11. Matriz oficial de análisis estratégico FODA de la plataforma SIGRE](docs/graficos/foda_oficial_sigre.jpg)  
*Figura 11. Matriz oficial de análisis estratégico FODA de la plataforma SIGRE.*

### ■ FORTALEZAS (F) — Factores Internos de Calidad y Control
- **F1. Software propietario especializado:** Despacho ágil (< 25 s) con sellado HMAC-SHA256.
- **F2. Alta usabilidad psicométrica validada:** Calificación de 82.85 puntos en escala SUS ($n = 50$, Grado A, $p = 0.035$).
- **F3. Eficiencia en infraestructura cloud:** Arquitectura de bajo costo con OPEX de servidores de $18,000 MXN en Año 1.
- **F4. Alineación regulatoria plena:** Cumplimiento con la LGPDPPSO y sustentabilidad universitaria.

### ■ OPORTUNIDADES (O) — Factores Externos de Crecimiento y Ahorro
- **O1. Austeridad presupuestal universitaria:** Demanda para eliminar mermas operativas en mostrador.
- **O2. Modelo B2G por Compra Directa (< 1,000 UMA = $117,310 MXN):** Contratación ágil por directores sin licitación.
- **O3. Mercado cautivo disponible en la Red UdeG:** Nicho de 196 planteles donde 22 sedes al Año 3 representa sólo el 11.2%.
- **O4. Ahorro económico y sustentabilidad:** Reducción de costos de papelería estimada en **$32,500 MXN** semestrales por plantel y eliminación de más de **32,500** actas y formatos físicos al semestre en la red.

### ■ DEBILIDADES (D) — Factores Internos a Mitigar en Fase Semilla
- **D1. Estructura unipersonal en el arranque:** Mitigada mediante nómina escalonada a partir del Año 2.
- **D2. Falta de historial comercial:** Superada mediante el caso piloto demostrativo sin costo en CUTonalá.
- **D3. Inducción presencial inicial:** Resistencia al cambio resuelta con talleres prácticos de 90 minutos.

### ■ AMENAZAS (A) — Factores Externos y Riesgos de Entorno Institucional
- **A1. Rotación de autoridades:** Mitigada con convenios plurianuales con dependencias académicas.
- **A2. Desfase en pagos institucionales:** Trámites a 30-60 días, cubiertos con el fondo de reserva de $40,000 MXN.
- **A3. Fallas locales de conectividad:** Resueltas mediante el modo de micro-custodia offline con sincronización diferida.

---
""")

    # -------------------------------------------------------------
    # 9. PROPUESTA FORMAL PARA EL INVERSIONISTA DE CAPITAL SEMILLA
    # -------------------------------------------------------------
    sections.append("""## 9. Propuesta Formal para el Inversionista de Capital Semilla

### 9.1 Tesis de inversión y oportunidad de mercado
SIGRE ofrece una oportunidad SaaS con mercado cautivo validado, márgenes operativos superiores al 45% y validación empírica. Con un ticket pre-semilla de **$180,000.00 MXN**, resuelve una merma analógica de más de $117,000 MXN anuales por plantel con un modelo B2G ágil.

### 9.2 ¿Cuál es el siguiente paso para que el proyecto siga creciendo?
El capital semilla se destinará de inmediato a: 1) Registro de marca ante el IMPI y derechos ante INDAUTOR; 2) Consolidación operativa en los 3 almacenes de CUTonalá; 3) Fabricación de 4 kits demo e inicio de visitas para concretar 2 contratos comerciales en prepas SEMS en el ciclo 2026-B.

### 9.3 Estructura formal de inversión, instrumento legal y retorno financiero
La inversión se formalizará mediante un Acuerdo de Participación con **Mecanismo de Cash Sweep del 70%** sobre los Flujos de Efectivo Netos (FEN) del proyecto hasta reintegrar el principal ($180,000 MXN), transicionando luego a una regalía patrimonial del **15% sobre las utilidades netas**:
- **Año 1 (Validación Piloto):** FEN de −$32,000 MXN; el inversionista no percibe flujos ($0 MXN).
- **Año 2 (Crecimiento Inicial):** Con FEN de **+$78,900 MXN**, el Cash Sweep del 70% entrega al inversionista **$55,230.00 MXN**, reteniendo el fundador **$23,670.00 MXN** (30%). El saldo insoluto disminuye a **$124,770.00 MXN** ($180,000 − $55,230).
- **Año 3 (Consolidación y Liquidación del Principal):** Con FEN de **+$296,800 MXN** ($24,733.33/mes), el saldo restante ($124,770 MXN) se liquida en el **Mes 31.2** (7.2 meses de Año 3). En Tramo 1 (Meses 25 a 31.2), el inversionista recibe $124,770 MXN (70%) y el fundador $53,473 MXN (30%). En Tramo 2 (Meses 31.3 a 36), se activa la regalía del 15%: el inversionista percibe $17,784 MXN y el fundador $100,773 MXN (85%). En total, en Año 3 el inversionista recibe **$142,554.00 MXN** y el fundador **$154,246.00 MXN** ($142,554 + $154,246 = $296,800 MXN exacto).
- **Retorno Trienal Acumulado:** El inversionista recupera un total de **$197,784.00 MXN** ($55,230 en Año 2 + $142,554 en Año 3), con una TIR trienal del 3.53%.
- **Retorno a 5 Años en Escenario Base Estable:** En los Años 4 y 5, manteniendo los flujos del Año 3 ($296,800 MXN/año), la regalía del 15% otorga al inversionista **$44,520.00 MXN anuales**, mientras que el fundador recibe **$252,280.00 MXN anuales**. El retorno quinquenal acumulado alcanza **$286,824.00 MXN**, elevando la **TIR del inversionista al 15.62% anual** (superior a la TMAR del 15.0%).
- **Retorno a 5 Años con Escalamiento Regional a UPES (Escenario Expansión):** Al expandir hacia universidades estatales de la región, los ingresos brutos alcanzan **1.21M MXN** en Año 4 y **1.93M MXN** en Año 5 con márgenes operativos del **32.0%** (FEN de **387.2k MXN** y **617.6k MXN**). El 15% del inversionista asciende a **$58,080.00 MXN** en Año 4 y **$92,640.00 MXN** en Año 5. El flujo proyectado [−$180,000, $0, $55,230, $142,554, $58,080, $92,640] genera una **TIR para el inversionista del 21.20% anual** y un múltiplo de retorno de 1.93x sobre el capital invertido.

La Tabla 16 resume los flujos proyectados y el retorno para el inversionista:

| Periodo de Flujo | Flujo Inversionista (Base Estable) | Flujo Inversionista (Expansión UPES) | Saldo Insoluto Capital | Condición Operativa y Tramo de Reparto |
|---|---|---|---|---|
| **Momento 0** | **($180,000.00 MXN)** | **($180,000.00 MXN)** | $180,000.00 MXN | Desembolso inicial de capital semilla |
| **Año 1** | $0.00 MXN | $0.00 MXN | $180,000.00 MXN | FEN negativo (−$32,000); reinversión total |
| **Año 2** | **+$55,230.00 MXN** | **+$55,230.00 MXN** | **$124,770.00 MXN** | Cash Sweep 70% sobre FEN de +$78,900 |
| **Año 3** | **+$142,554.00 MXN** | **+$142,554.00 MXN** | **$0.00 MXN (Liquidado en Mes 31.2)** | Tramo 1 (70% hasta liq) + Tramo 2 (15% regalía) |
| **Año 4** | **+$44,520.00 MXN** | **+$58,080.00 MXN** | $0.00 MXN | 15% utilidades netas ($296.8k base / $387.2k UPES) |
| **Año 5** | **+$44,520.00 MXN** | **+$92,640.00 MXN** | $0.00 MXN | 15% utilidades netas ($296.8k base / $617.6k UPES) |
| **Total Flujos Recibidos** | **$286,824.00 MXN** | **$348,504.00 MXN** | — | Múltiplo de 1.59x (Base) y 1.93x (Expansión) |
| **Tasa Interna de Retorno (TIR)** | **15.62% anual** | **21.20% anual** | — | **Ambos escenarios superan la TMAR del 15.0%** |

*Tabla 16. Flujos de caja proyectados y Tasa Interna de Retorno (TIR) para el inversionista privado.*

---
""")

    # -------------------------------------------------------------
    # 10. REFERENCIAS BIBLIOGRÁFICAS Y ANEXOS
    # -------------------------------------------------------------
    sections.append("""## 10. Referencias Bibliográficas (Norma APA 7ma Edición)

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
El estudio de campo se realizó en CUTonalá durante el ciclo 2026-A con el instrumento SUS de 10 ítems (Brooke, 1996). La media de **82.85 puntos** ($DE = 10.91$, $n = 50$, percentil 91.4, Grado A) y el Alfa de Cronbach de **0.892** confirman la robustez psicométrica y la superioridad de SIGRE frente a métodos analógicos.

### Anexo B. Video Demostrativo E2E y Matriz de Solventación al Dictamen Técnico Docente
Código fuente y video demostrativo (*End-to-End*) disponibles en: `https://github.com/erfierro/sigre-platform-core`.

En la Tabla 17 se detalla la solventación a las observaciones del dictamen técnico docente de la **Mtra. Abril Adriana Angulo Sherman**:

| Área Evaluada del Dictamen | Dictamen y Observación Docente Emitida | Solventación Técnica y Referencia en el Documento |
|---|---|---|
| **1. Justificación y Costo de Inacción** | Cuantificar el costo de inacción administrativa y mermas por plantel. | Modelo micro-financiero de $117,310 MXN/año por plantel con horas-hombre y mermas. (Sección 1.4 y Tabla 2). |
| **2. Viabilidad Burocrática B2G** | Acreditar la viabilidad legal de contratación frente al marco de compras. | Adjudicación directa bajo el tope de 1,000 UMA ($117,310 MXN). (Sección 4.1). |
| **3. Objetivos y Marco Lógico** | Reestructurar objetivos cuantitativos y elaborar la MML bajo CEPAL/BID. | Metas a 22 sedes, payback a Mes 31.2 y la MML formal. (Sección 2.2, 2.3 y Tabla 4). |
| **4. Arquitectura y Privacidad** | Especificar la arquitectura tecnológica y el apego normativo de datos. | Arquitectura en 5 capas, HMAC-SHA256 y cumplimiento de la LGPDPPSO. (Sección 5 y Tabla 7). |
| **5. Organización y Salarios** | Eliminar distorsiones en salarios iniciales e incorporar nómina escalonada. | Fundador Único y nómina escalonada ($120k Año 2 y $240k Año 3). (Sección 6.2 y Tabla 8). |
| **6. Consistencia Financiera Proforma** | Cuadrar la amortización de pérdidas fiscales en Año 2 y retornos de inversión. | ISR Año 2 ($20,100 MXN) amortizando pérdida fiscal de −$32,000 MXN. (Sección 7.3 y Tabla 13). |
| **7. Mecanismo al Inversionista** | Detallar el mecanismo de pago y conciliación del capital semilla. | Cash Sweep del 70% con liquidación en Mes 31.2 y retorno quinquenal. (Sección 9.3 y Tabla 16). |

*Tabla 17. Matriz de solventación al dictamen técnico docente de la Mtra. Abril Adriana Angulo Sherman.*
""")

    return "\n".join(sections).strip()
