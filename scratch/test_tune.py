import os
import re
import sys

def tune():
    with open('docs/Propuesta_Inversion_SIGRE_Corregida.md', 'r', encoding='utf-8') as f:
        text = f.read()

    t = text

    # 1. Lead-ins & alt text
    t = t.replace('En la Figura 1 se contrasta el flujo analógico frente al control digital con trazabilidad de SIGRE:\n\n', '')
    t = t.replace('En la Figura 2 se presenta la distribución empírica de puntajes SUS:\n\n', '')
    t = t.replace('![Figura 2. Distribución de frecuencias y curva de densidad de puntajes SUS (n = 50)](docs/pruebas/screenshots/10_distribucion_puntajes_sus.png)', '![Figura 2](docs/pruebas/screenshots/10_distribucion_puntajes_sus.png)')
    t = t.replace('![Figura 3. Interfaz de firma manuscrita digitalizada sobre Canvas HTML5 con sellado criptográfico HMAC-SHA256](docs/pruebas/screenshots/05_canvas_firma_digital.png)', '![Figura 3](docs/pruebas/screenshots/05_canvas_firma_digital.png)')
    t = t.replace('![Figura 6. Tablero directivo ejecutivo con telemetría de activos y control de inventario en tiempo real](docs/pruebas/screenshots/08_dashboard_ejecutivo.png)', '![Figura 6](docs/pruebas/screenshots/08_dashboard_ejecutivo.png)')
    t = t.replace('![Figura 11. Matriz oficial de análisis estratégico FODA de la plataforma SIGRE](docs/graficos/foda_oficial_sigre.jpg)', '![Figura 11](docs/graficos/foda_oficial_sigre.jpg)')
    t = t.replace('La formulación estratégica de SIGRE se sustenta en la matriz FODA institucional (Figura 11):\n\n', '')

    # 2. Ficha Técnica
    old_ft = """| **CAPEX** | **$180,000.00 MXN** (Inversión pre-semilla auditada, cojín de liquidez, sin doble cómputo) |
| **Métricas** | **VPN: +$46,984.47 MXN** (@ 15.0% TMAR) \\| **TIR: 24.27% anual** \\| **Relación B/C: 1.23x** |
| **Payback** | **Payback Simple: Mes 29.4** (2.45 años) \\| **Payback Descontado: Mes 33.1** (2.76 años) |
| **Mecanismo** | **Cash Sweep del 70%** hasta liquidar $180,000 MXN en **Mes 31.2**; regalía del 15% posterior |
| **Retorno** | **Trienal: $197,784 MXN (TIR 3.53%)** \\| **5 años Base: 15.62%** \\| **5 años UPES: 21.20% anual** |
| **Psicometría** | **Escala SUS: 82.85/100 pts** ($n = 50$, DE 10.91, Grado A "Excelente", percentil 91.4, Alfa 0.892, $p = 0.035$) |
| **Mercado** | Red UdeG (196 unidades). Año 1: 3 planteles; Año 2: 8 planteles; Año 3: 22 planteles (11.2%) |"""

    new_ft = """| **CAPEX** | **$180,000.00 MXN** (Inversión pre-semilla auditada con cojín de liquidez) |
| **Métricas** | **VPN: +$46,984.47 MXN** (@ 15.0% TMAR) \\| **TIR: 24.27% anual** \\| **Relación B/C: 1.23x** |
| **Payback** | **Payback Simple: Mes 29.4** (2.45 a) \\| **Payback Descontado: Mes 33.1** (2.76 a) |
| **Mecanismo** | **Cash Sweep del 70%** (liquidación en **Mes 31.2**; regalía del 15% posterior) |
| **Retorno** | **Trienal: $197,784 MXN (TIR 3.53%)** \\| **5 a Base: 15.62%** \\| **5 a UPES: 21.20% anual** |
| **Psicometría** | **Escala SUS: 82.85/100 pts** ($n = 50$, DE 10.91, Grado A, percentil 91.4, Alfa 0.892, $p = 0.035$) |
| **Mercado** | Red UdeG (196 sedes). Año 1: 3 planteles; Año 2: 8 planteles; Año 3: 22 planteles (11.2%) |"""
    t = t.replace(old_ft, new_ft)

    # 3. Sec 1 text
    t = t.replace(
        'En almacenes y laboratorios de la Red UdeG, los préstamos se registran en libretas manuales. Este método genera demoras de **3.5 a 5.0 minutos por usuario** en cambios de clase (bloques de 10 min), aglomeraciones y una merma del **8% al 12% del stock circulante semestral**.',
        'En almacenes y laboratorios de la Red UdeG, el registro manual en libretas genera demoras de **3.5 a 5.0 minutos por usuario** en cambios de clase (bloques de 10 min), aglomeraciones y una merma del **8% al 12% del stock circulante semestral**.'
    )
    t = t.replace(
        'El macro-ERP institucional (SIIAU) gestiona inventario contable patrimonial diferido; no atiende la **micro-custodia** ágil de ventanilla en transacciones menores a 25 segundos. Creer que un ERP resuelve el mostrador es una falacia operativa que perpetúa bitácoras en papel sin validez jurídica probatoria ni trazabilidad individual.',
        'El macro-ERP institucional (SIIAU) gestiona inventario contable diferido, no la **micro-custodia** ágil de ventanilla (< 25 s). Asumir que un ERP resuelve el mostrador es una falacia operativa que perpetúa bitácoras en papel sin validez jurídica probatoria ni trazabilidad individual.'
    )
    t = t.replace(
        'La prueba t frente al estándar de 68 puntos probó significancia: $t(49) = 1.848$, $p = 0.035$ ($p < 0.05$). La Tabla 1 consolida la muestra:',
        'La prueba t frente al estándar de 68 puntos probó significancia: $t(49) = 1.848$, $p = 0.035$. La Tabla 1 consolida la muestra:'
    )
    t = t.replace(
        'El costo de inacción oscila entre **$90,000 MXN y $140,000 MXN anuales por plantel** (punto medio **$115,000 MXN/año**). Siguiendo a Sapag Chain (2014), la Tabla 2 desglosa esta ineficiencia en **$117,310.00 MXN anuales**:',
        'El costo de inacción oscila entre **$90,000 MXN y $140,000 MXN anuales por plantel** (punto medio **$115,000 MXN/año**). Siguiendo a Sapag Chain (2014), la Tabla 2 desglosa la ineficiencia en **$117,310.00 MXN anuales**:'
    )

    # 4. Sec 2 text & objetivos
    t = t.replace(
        'SIGRE es un SaaS de **micro-custodia** transaccional para ventanillas escolares: 1) Despacho veloz (< 25 s) vía código de barras o QR; 2) Firma digitalizada sobre Canvas HTML5 con sellado HMAC-SHA256 para no repudio probatorio; 3) Telemetría preventiva de desgaste por activo; 4) Notificaciones multicanal (WhatsApp/Telegram/correo; Figura 3):',
        'SIGRE es un SaaS de **micro-custodia** transaccional para ventanillas escolares: 1) Despacho veloz (< 25 s) vía código de barras o QR; 2) Firma digitalizada en Canvas HTML5 con sellado HMAC-SHA256 (Figura 3); 3) Telemetría preventiva de desgaste por activo; 4) Notificaciones multicanal:'
    )

    old_obj = """- **Objetivo General:** Estandarizar SIGRE en la Red UdeG como plataforma líder de micro-custodia en mostrador, alcanzando autosuficiencia operativa.
- **Objetivo 1 (Técnico):** Despachar préstamos en menos de 25 segundos con 99.5% de disponibilidad cloud y modo contingente offline.
- **Objetivo 2 (Comercial):** Afiliar 3 planteles en Año 1 (1 piloto CUTonalá sin costo + 2 contratos comerciales de prepas a $24,000 MXN), 8 en Año 2 y 22 en Año 3 (11.2% de la Red UdeG).
- **Objetivo 3 (Financiero):** Reintegrar los $180,000 MXN de capital semilla en el **Mes 31.2** mediante un **Cash Sweep del 70%** sobre el FEN, logrando equilibrio operativo en el Mes 14 y consolidación de nómina hacia el **Mes 22**."""

    new_obj = """- **Objetivo General:** Estandarizar SIGRE en la Red UdeG como plataforma líder de micro-custodia en mostrador.
- **Objetivo 1 (Técnico):** Despachar préstamos en < 25 s con 99.5% de disponibilidad cloud y modo offline.
- **Objetivo 2 (Comercial):** Afiliar 3 planteles en Año 1 (1 piloto CUTonalá sin costo + 2 contratos comerciales de prepas a $24,000 MXN), 8 en Año 2 y 22 en Año 3 (11.2% de la Red UdeG).
- **Objetivo 3 (Financiero):** Reintegrar los $180,000 MXN en el **Mes 31.2** mediante un **Cash Sweep del 70%** sobre el FEN, logrando equilibrio en Mes 14 y consolidación de nómina hacia el **Mes 22**."""
    t = t.replace(old_obj, new_obj)

    # 5. Sec 3 & 4
    t = t.replace(
        'Conforme a la numeralia de Planeación y Evaluación (**mayo de 2026**; SEMS, 2024), la Red UdeG suma **196 dependencias**:',
        'Según la numeralia de Planeación y Evaluación (**mayo de 2026**; SEMS, 2024), la Red UdeG suma **196 dependencias**:'
    )
    t = t.replace(
        'A partir del Año 4, SIGRE escalará a Universidades Públicas Estatales (**UPES**) del Centro-Occidente (340+ planteles):',
        'Hacia el Año 4, SIGRE escalará a Universidades Públicas Estatales (**UPES**) del Centro-Occidente (340+ planteles):'
    )
    t = t.replace(
        'Las suscripciones de SIGRE ($24k a $48k MXN) quedan amparadas mediante adjudicación directa sin licitación pública (Tabla 6):',
        'Las suscripciones de SIGRE ($24k a $48k MXN) califican para adjudicación directa sin licitación pública (Tabla 6):'
    )

    # 6. Sec 5
    t = t.replace(
        'SIGRE opera sobre una arquitectura de 5 capas: PWA en Vue 3 y TypeScript (Capa 1), Gateway Caddy TLS 1.3 (Capa 2), FastAPI Python 3.11 (Capa 3), PostgreSQL 15 y Redis (Capa 4), y Sellado HMAC-SHA256 (Capa 5; Figura 5 y Tabla 7):',
        'SIGRE opera en 5 capas: PWA Vue 3 y TypeScript (Capa 1), Gateway Caddy TLS 1.3 (Capa 2), FastAPI Python 3.11 (Capa 3), PostgreSQL 15 y Redis (Capa 4), y Sellado HMAC-SHA256 (Capa 5; Figura 5 y Tabla 7):'
    )
    t = t.replace(
        'El sistema prescinde de datos biométricos y cifra información con AES-256 en reposo conforme a la LGPDPPSO, apoyando la directiva de cero papel del PDI CUTonalá. Ante fallas de red, la PWA activa el **modo contingente de micro-custodia offline**: registra firmas en *IndexedDB* con sellado local y sincroniza automáticamente al restablecer conectividad.',
        'El sistema prescinde de datos biométricos y cifra con AES-256 conforme a LGPDPPSO y directiva cero papel del PDI CUTonalá. Ante fallas de red, la PWA activa el **modo contingente de micro-custodia offline**: registra firmas en *IndexedDB* con sellado local y sincroniza al reconectar.'
    )

    # 7. Sec 6
    t = t.replace(
        'La conducción ejecutiva corresponde a **Ernesto Hatuey Fierro Meléndez** como **Fundador Único, Director General y Diseñador de Software**, quien lidera desarrollo, operaciones cloud, comercialización B2G y arquitectura (Figura 7):',
        'La dirección corresponde a **Ernesto Hatuey Fierro Meléndez** como **Fundador Único, Director General y Diseñador de Software**, liderando desarrollo, operaciones cloud y comercialización B2G (Figura 7):'
    )

    old_pay = 'La compensación aplica **nómina escalonada** por hitos: Año 1 ($0 nómina externa); Año 2 ($120,000 MXN) con Técnico N1 en Mes 15 (7 meses @ $4k = $28,000 MXN), Especialista TC en **Mes 22** (3 meses @ $10k = $30,000 MXN) y honorarios fundador por $62,000 MXN ($28k + $30k + $62k = **$120,000 MXN**); Año 3 ($240,000 MXN) con Especialista TC (12 meses @ $10k = $120,000 MXN), CS (9 meses @ $7k = $63,000 MXN) y estipendio fundador por $57,000 MXN ($120k + $63k + $57k = **$240,000 MXN**). La Tabla 8 resume las condiciones:'
    new_pay = 'La compensación aplica **nómina escalonada** por hitos: Año 1 ($0 nómina externa); Año 2 (**$120,000** MXN: Técnico N1 $28,000 MXN, Especialista TC activado en **Mes 22** por $30,000 MXN y honorarios fundador por $62,000 MXN); Año 3 (**$240,000** MXN: Especialista TC $120,000 MXN, CS $63,000 MXN y estipendio fundador por $57,000 MXN). La Tabla 8 resume las condiciones:'
    t = t.replace(old_pay, new_pay)

    t = t.replace(
        'La ejecución comprende 4 fases operativas hacia la tracción comercial (Figura 8 y Tabla 9):',
        'La ejecución comprende 4 fases hacia la tracción comercial (Figura 8 y Tabla 9):'
    )
    t = t.replace(
        'La Tabla 10 y la Figura 9 detallan la programación de actividades en Ruta Crítica:',
        'La programación de actividades en Ruta Crítica se detalla en la Tabla 10 y la Figura 9:'
    )

    # 8. Sec 7
    t = t.replace(
        'El requerimiento inicial asciende a **$180,000.00 MXN**, desglosado con rigor en la Tabla 11 sin duplicidad frente al OPEX:',
        'El requerimiento inicial suma **$180,000.00 MXN**, desglosado en la Tabla 11 sin duplicidad frente al OPEX:'
    )
    old_rev = 'Los costos operativos totalizan **$95,000 MXN en Año 1**, **$225,000 MXN en Año 2** y **$426,000 MXN en Año 3**. En ingresos, el Año 1 suma **$63,000 MXN** con **3 planteles** (piloto **CUTonalá** sin costo con setup de $15,000 MXN en 3 almacenes + **2 contratos comerciales** prepas SEMS a $24,000 MXN = $48,000 MXN). Los ingresos escalan a **$324,000 MXN en Año 2** (8 sedes) y alcanzan **$850,000 MXN en Año 3** (22 sedes; Tabla 12 y Figura 10):'
    new_rev = 'Los costos operativos suman **$95,000 MXN en Año 1**, **$225,000 MXN en Año 2** y **$426,000 MXN en Año 3**. Los ingresos de Año 1 totalizan **$63,000 MXN** con **3 planteles** (piloto **CUTonalá** sin costo con setup de $15,000 MXN + **2 contratos comerciales** prepas SEMS a $24,000 MXN = $48,000 MXN), escalando a **$324,000 MXN en Año 2** (8 sedes) y **$850,000 MXN en Año 3** (22 sedes; Tabla 12 y Figura 10):'
    t = t.replace(old_rev, new_rev)

    old_proforma_callout = """> [!NOTE]
> **Consistencia Aritmética y Estrés Financiero:**  
> Año 1: OPEX de **($95,000)** genera pérdida de **−$32,000** ($63k − $95k), amortizada en Año 2 (base gravable $67,000 MXN, ISR 30% por **($20,100)** y FEN de **+$78,900**). Año 3: EBIT $424,000 MXN e ISR **($127,200)** arrojan FEN de **+$296,800**. Punto de equilibrio en **Mes 14**."""
    new_proforma_callout = """> [!NOTE]
> **Consistencia Aritmética y Estrés Financiero:**  
> Año 1: OPEX de **($95,000)** genera pérdida de **−$32,000**, amortizada en Año 2 (base gravable $67,000 MXN, ISR 30% por **($20,100)** y FEN de **+$78,900**). Año 3: EBIT $424,000 MXN e ISR **($127,200)** arrojan FEN de **+$296,800**. Punto de equilibrio en **Mes 14**."""
    t = t.replace(old_proforma_callout, new_proforma_callout)

    t = t.replace(
        'A una **TMAR del 15.0% anual** (Cetes 7.12% + Prima 7.88%), la Tabla 14 resume la rentabilidad del proyecto:',
        'A una **TMAR del 15.0% anual** (Cetes 7.12% + Prima 7.88%), la Tabla 14 resume la rentabilidad:'
    )

    old_sens_callout = """> [!IMPORTANT]
> **Umbral de Viabilidad Financiera (Break-Even):**  
> El punto donde $VPN = 0$ exige un FEN en Año 3 de **$225,342.50 MXN**, equivalente a **18.12 planteles** continuos. En términos discretos, se requiere afiliar al menos **19 planteles** seguros al Año 3 (sólo el **9.7%** de la Red UdeG) para cubrir íntegramente la tasa de descuento del 15%."""
    new_sens_callout = """> [!IMPORTANT]
> **Umbral de Viabilidad Financiera (Break-Even):**  
> El punto con $VPN = 0$ exige un FEN en Año 3 de **$225,342.50 MXN** (**18.12 planteles** continuos). En términos discretos, se requiere afiliar **19 planteles** seguros al Año 3 (sólo el **9.7%** de la Red UdeG) para cubrir íntegramente la tasa de descuento del 15%."""
    t = t.replace(old_sens_callout, new_sens_callout)

    # 9. Sec 8 (FODA)
    old_foda = """### Fortalezas (F) y Oportunidades (O)
- **F1. Software propio:** Despacho ágil en < 25 s con firma digitalizada y sellado criptográfico HMAC-SHA256.
- **F2. Usabilidad validada:** 82.85 puntos en escala SUS ($n = 50$, Grado A "Excelente", percentil 91.4, $p = 0.035$).
- **F3. Infraestructura cloud eficiente:** OPEX de servidores de $18,000 MXN en Año 1.
- **F4. Cumplimiento normativo:** Alineación con LGPDPPSO y sustentabilidad universitaria.
- **O1. Austeridad universitaria:** Demanda institucional para abatir mermas en mostrador.
- **O2. Modelo B2G por Compra Directa (< 1,000 UMA = $117,310 MXN):** Contratación ágil sin licitación pública.
- **O3. Mercado cautivo Red UdeG:** 196 dependencias (22 sedes al Año 3 representa sólo el 11.2%).
- **O4. Ahorro y sustentabilidad:** Reducción de costos de papelería de **$32,500 MXN** semestrales por plantel y eliminación de más de **32,500** actas físicas al semestre.

### Debilidades (D) y Amenazas (A)
- **D1. Estructura inicial:** Mitigada con nómina escalonada técnica a partir del Año 2.
- **D2. Falta de historial:** Superada mediante el caso piloto demostrativo sin costo en CUTonalá.
- **D3. Inducción en sitio:** Resistencia al cambio resuelta con talleres prácticos de 90 minutos.
- **A1. Rotación directiva:** Mitigada formalizando convenios institucionales plurianuales.
- **A2. Desfase en pagos:** Trámites a 30-60 días, cubiertos con fondo de reserva de $40,000 MXN.
- **A3. Cortes locales de red:** Resueltos con modo de micro-custodia offline y sincronización diferida."""

    new_foda = """### Fortalezas (F) y Oportunidades (O)
- **F1. Software propio:** Despacho ágil en < 25 s con firma digitalizada y sellado criptográfico HMAC-SHA256.
- **F2. Usabilidad validada:** 82.85 puntos en escala SUS ($n = 50$, Grado A "Excelente", percentil 91.4, $p = 0.035$).
- **F3. Cloud eficiente:** Servidores $18,000 MXN Año 1.
- **F4. Cumplimiento:** LGPDPPSO y directrices PDI CUTonalá.
- **O1. Austeridad:** Demanda institucional para abatir mermas de mostrador.
- **O2. Modelo B2G por Compra Directa (< 1,000 UMA = $117,310 MXN):** Adjudicación directa sin licitación pública.
- **O3. Mercado cautivo Red UdeG:** 196 dependencias (22 sedes al Año 3 representa sólo el 11.2%).
- **O4. Ahorro y sustentabilidad:** Reducción de costos de papelería de **$32,500 MXN** semestrales por plantel y eliminación de más de **32,500** actas físicas al semestre.

### Debilidades (D) y Amenazas (A)
- **D1. Estructura inicial:** Mitigada con nómina escalonada técnica a partir del Año 2.
- **D2. Falta de historial:** Superada con caso piloto sin costo en CUTonalá.
- **D3. Inducción:** Talleres prácticos de 90 minutos para auxiliares.
- **A1. Rotación directiva:** Convenios institucionales plurianuales.
- **A2. Desfase en pagos:** Cobro a 30-60 días cubierto con reserva de $40,000 MXN.
- **A3. Cortes locales de red:** Modo de micro-custodia offline y sync diferida."""
    t = t.replace(old_foda, new_foda)

    # 10. Sec 9
    old_t = 'SIGRE ofrece una oportunidad SaaS con mercado cautivo validado, márgenes operativos superiores al 45% y validación empírica. Con un ticket pre-semilla de **$180,000.00 MXN**, resuelve una merma analógica de más de $117,000 MXN anuales por plantel con un modelo B2G ágil.'
    new_t = 'SIGRE representa una oportunidad SaaS con mercado cautivo validado y márgenes operativos > 45%. Con ticket pre-semilla de **$180,000.00 MXN**, resuelve una merma de más de $117,000 MXN anuales por plantel mediante un modelo B2G ágil.'
    t = t.replace(old_t, new_t)

    old_paso = 'El capital semilla se destinará de inmediato a: 1) Registro de marca ante el IMPI y derechos ante INDAUTOR; 2) Consolidación operativa en los 3 almacenes de CUTonalá; 3) Fabricación de 4 kits demo e inicio de visitas para concretar 2 contratos comerciales en prepas SEMS en el ciclo 2026-B.'
    new_paso = 'El capital semilla se destinará de inmediato a: 1) Registro de marca ante el IMPI y derechos ante INDAUTOR; 2) Consolidación operativa en 3 almacenes de CUTonalá; 3) Fabricación de 4 kits demo e inicio de visitas para cerrar 2 contratos comerciales en prepas SEMS en ciclo 2026-B.'
    t = t.replace(old_paso, new_paso)

    old_cs = 'El capital se instrumenta mediante un Acuerdo de Participación con **Cash Sweep del 70%** sobre el FEN hasta liquidar $180,000 MXN en **Mes 31.2**, con regalía del **15% sobre utilidades netas** posterior. En Año 1 (FEN **−$32,000 MXN**), el flujo se reinvierte íntegramente. En Año 2 (FEN **+$78,900 MXN**), el Cash Sweep 70% distribuye **$55,230.00 MXN** al inversionista y **$23,670.00 MXN** al fundador (30%), restando un saldo insoluto de **$124,770.00 MXN**. En Año 3 (FEN **+$296,800 MXN**), se amortiza el saldo insoluto en el Mes 31.2 (Tramo 1: inversionista $124,770 MXN, fundador $53,473 MXN) y se activa la regalía del 15% (Tramo 2: inversionista $17,784 MXN, fundador $100,773 MXN), totalizando en el año **$142,554.00 MXN** para el inversionista y **$154,246.00 MXN** para el fundador ($142,554 + $154,246 = $296,800 MXN).'
    new_cs = 'El capital se instrumenta con un Acuerdo de Participación con **Cash Sweep del 70%** sobre el FEN hasta liquidar $180,000 MXN en **Mes 31.2**, con regalía del **15% sobre utilidades netas** posterior. En Año 1 (FEN **−$32,000 MXN**), el flujo se reinvierte. En Año 2 (FEN **+$78,900 MXN**), el Cash Sweep 70% paga **$55,230.00 MXN** al inversionista y **$23,670.00 MXN** al fundador (30%), restando un saldo insoluto de **$124,770.00 MXN**. En Año 3 (FEN **+$296,800 MXN**), se amortiza el saldo en Mes 31.2 (Tramo 1: inversionista $124,770 MXN, fundador $53,473 MXN) y se activa la regalía del 15% (Tramo 2: inversionista $17,784 MXN, fundador $100,773 MXN), sumando en el año **$142,554.00 MXN** para el inversionista y **$154,246.00 MXN** para el fundador ($142,554 + $154,246 = $296,800 MXN).'
    t = t.replace(old_cs, new_cs)

    old_ret = 'El retorno trienal acumulado suma **$197,784.00 MXN** (TIR 3.53%). A 5 años en Escenario Base, la regalía del 15% genera **$44,520.00 MXN anuales** al inversionista y **$252,280.00 MXN** al fundador, alcanzando una **TIR del 15.62% anual** (acumulado $286,824 MXN). En el modelo de expansión UPES, con ingresos de **1.21M MXN** (Año 4) y **1.93M MXN** (Año 5) a un margen del **32.0%** (FEN **387.2k MXN** y **617.6k MXN**), la regalía del 15% otorga **$58,080.00 MXN** en Año 4 y **$92,640.00 MXN** en Año 5, alcanzando una **TIR del 21.20% anual** (múltiplo 1.93x; Tabla 16):'
    new_ret = 'El retorno trienal acumulado suma **$197,784.00 MXN** (TIR 3.53%). A 5 años en Escenario Base, la regalía del 15% genera **$44,520.00 MXN anuales** al inversionista y **$252,280.00 MXN** al fundador, alcanzando una **TIR del 15.62% anual** (acumulado $286,824 MXN). En expansión UPES, con ingresos de **1.21M MXN** (Año 4) y **1.93M MXN** (Año 5) a un margen del **32.0%** (FEN **387.2k MXN** y **617.6k MXN**), la regalía del 15% otorga **$58,080.00 MXN** en Año 4 y **$92,640.00 MXN** en Año 5, alcanzando una **TIR del 21.20% anual** (múltiplo 1.93x; Tabla 16):'
    t = t.replace(old_ret, new_ret)

    # 11. Anexos
    old_anexo_a = 'El estudio de campo se realizó en CUTonalá durante el ciclo 2026-A con el instrumento SUS de 10 ítems (Brooke, 1996). La media de **82.85 puntos** ($DE = 10.91$, $n = 50$, percentil 91.4, Grado A) y el Alfa de Cronbach de **0.892** confirman la robustez psicométrica y la superioridad de SIGRE frente a métodos analógicos.'
    new_anexo_a = 'El estudio de campo en CUTonalá (ciclo 2026-A, SUS de 10 ítems; Brooke, 1996) arrojó media de **82.85 puntos** ($DE = 10.91$, $n = 50$, percentil 91.4, Grado A) y Alfa de Cronbach de **0.892**, probando la superioridad de SIGRE frente a métodos analógicos.'
    t = t.replace(old_anexo_a, new_anexo_a)

    old_anexo_b = 'Código fuente y video demostrativo (*End-to-End*) disponibles en: `https://github.com/erfierro/sigre-platform-core`.\n\nEn la Tabla 17 se detalla la solventación a las observaciones del dictamen técnico docente de la **Mtra. Abril Adriana Angulo Sherman**:'
    new_anexo_b = 'Código fuente y video (*End-to-End*) en: `https://github.com/erfierro/sigre-platform-core`.\n\nEn la Tabla 17 se detalla la solventación al dictamen técnico docente de la **Mtra. Abril Adriana Angulo Sherman**:'
    t = t.replace(old_anexo_b, new_anexo_b)

    return t

if __name__ == '__main__':
    t = tune()
    w_regex = re.findall(r'\b[^\W_]+\b', t)
    w_split = t.split()
    w_no_pipes = [x for x in w_split if x != '|']

    print('--- RESULTS ---')
    print('Chars with spaces:', len(t))
    print('Split words:', len(w_split))
    print('No pipes words:', len(w_no_pipes))
    print('Regex words:', len(w_regex))
