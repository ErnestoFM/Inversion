const { chromium } = require('@playwright/test');
const fs = require('fs');
const path = require('path');

async function renderCharts() {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.setViewportSize({ width: 980, height: 530 });

  // -------------------------------------------------------------------------
  // FIGURA 2: Diagrama de Pareto de Causas y Costos de Merma Patrimonial
  // -------------------------------------------------------------------------
  const fig2Html = `
  <!DOCTYPE html>
  <html>
  <head>
    <meta charset="utf-8">
    <style>
      body {
        margin: 0;
        padding: 20px 30px;
        background: #ffffff;
        font-family: 'Segoe UI', Arial, sans-serif;
        color: #1A202C;
        box-sizing: border-box;
      }
      .title-container {
        text-align: center;
        margin-bottom: 16px;
      }
      .title {
        font-size: 15px;
        font-weight: 800;
        color: #002B49;
        margin: 0 0 4px 0;
      }
      .subtitle {
        font-size: 11.5px;
        color: #4A5568;
        margin: 0;
      }
      .chart-wrapper {
        position: relative;
        width: 820px;
        margin: 0 auto;
      }
      .chart-container {
        position: relative;
        width: 820px;
        height: 370px;
        border-left: 2px solid #002B49;
        border-right: 2px solid #D97706;
        border-bottom: 2px solid #002B49;
      }
      .grid-line {
        position: absolute;
        left: 0;
        width: 100%;
        border-top: 1px dashed #E2E8F0;
      }
      .y-label-left {
        position: absolute;
        left: -68px;
        font-size: 10px;
        font-weight: 700;
        color: #002B49;
        text-align: right;
        width: 60px;
      }
      .y-label-right {
        position: absolute;
        right: -60px;
        font-size: 10px;
        font-weight: 700;
        color: #D97706;
        text-align: left;
        width: 52px;
      }
      .bars-wrapper {
        position: absolute;
        bottom: 0;
        left: 0;
        width: 100%;
        height: 100%;
        display: flex;
        justify-content: space-around;
        align-items: flex-end;
      }
      .bar-col {
        width: 120px;
        display: flex;
        flex-direction: column;
        align-items: center;
        position: relative;
      }
      .bar {
        width: 72px;
        background: linear-gradient(180deg, #1A365D 0%, #002B49 100%);
        border-radius: 4px 4px 0 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
      }
      .bar-val {
        font-size: 10px;
        font-weight: 700;
        color: #002B49;
        margin-bottom: 5px;
        text-align: center;
        line-height: 1.2;
      }
      .bar-pct {
        font-size: 9px;
        color: #4A5568;
      }
      .bar-title {
        position: absolute;
        bottom: -44px;
        font-size: 9.5px;
        font-weight: 600;
        text-align: center;
        color: #2D3748;
        line-height: 1.25;
        width: 135px;
      }
      svg.pareto-line {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
      }
      .legend {
        display: flex;
        justify-content: center;
        gap: 24px;
        margin-top: 52px;
        font-size: 10.5px;
        font-weight: 600;
      }
      .legend-item {
        display: flex;
        align-items: center;
        gap: 6px;
      }
      .box-bar {
        width: 14px;
        height: 14px;
        background: #002B49;
        border-radius: 2px;
      }
      .line-pareto {
        width: 18px;
        height: 3px;
        background: #D97706;
      }
      .line-cutoff {
        width: 18px;
        height: 2px;
        border-top: 2px dashed #DC2626;
      }
    </style>
  </head>
  <body>
    <div class="title-container">
      <div class="title">Diagrama de Pareto: Causas y Costos Estimados de Merma Patrimonial Anual</div>
      <div class="subtitle">Estimación basada en Almacén Central y Servicios Generales CUTonalá (Línea Base Anual: $140,000 MXN)</div>
    </div>

    <div class="chart-wrapper">
      <div class="chart-container">
        <!-- Grid Lines & Dual Y-axis labels -->
        <!-- Max = $60,000 / 100% (Height = 370px) -->
        <div class="grid-line" style="bottom: 370px;"><span class="y-label-left">$60,000</span><span class="y-label-right">100%</span></div>
        <div class="grid-line" style="bottom: 296px;"><span class="y-label-left">$48,000</span><span class="y-label-right">80%</span></div>
        <div class="grid-line" style="bottom: 222px;"><span class="y-label-left">$36,000</span><span class="y-label-right">60%</span></div>
        <div class="grid-line" style="bottom: 148px;"><span class="y-label-left">$24,000</span><span class="y-label-right">40%</span></div>
        <div class="grid-line" style="bottom: 74px;"><span class="y-label-left">$12,000</span><span class="y-label-right">20%</span></div>

        <!-- 82.5% Cutoff Line -->
        <div style="position: absolute; bottom: 305px; left: 0; width: 100%; border-top: 2px dashed #DC2626; z-index: 2;">
          <span style="position: absolute; right: 20px; top: -16px; font-size: 9.5px; font-weight: bold; color: #DC2626; background: #FFF5F5; padding: 2px 8px; border-radius: 4px; border: 1px solid #FEB2B2; white-space: nowrap;">
            Umbral Pareto 82.5% (Causas Críticas)
          </span>
        </div>

        <!-- Bars -->
        <div class="bars-wrapper">
          <!-- 1. Proyectores ($55,000 -> 339px) -->
          <div class="bar-col">
            <div class="bar-val">$55,000<br><span class="bar-pct">(39.3%)</span></div>
            <div class="bar" style="height: 339px;"></div>
            <div class="bar-title">Proyectores<br>(Lámparas/Óptica)</div>
          </div>
          <!-- 2. Adaptadores ($35,000 -> 216px) -->
          <div class="bar-col">
            <div class="bar-val" style="margin-bottom: 22px;">$35,000<br><span class="bar-pct">(25.0%)</span></div>
            <div class="bar" style="height: 216px;"></div>
            <div class="bar-title">Adaptadores<br>(USB-C/VGA/Display)</div>
          </div>
          <!-- 3. Cables HDMI ($25,500 -> 157px) -->
          <div class="bar-col">
            <div class="bar-val">$25,500<br><span class="bar-pct">(18.2%)</span></div>
            <div class="bar" style="height: 157px;"></div>
            <div class="bar-title">Cables HDMI<br>(Terminales/Pérdida)</div>
          </div>
          <!-- 4. Periféricos ($14,500 -> 89px) -->
          <div class="bar-col">
            <div class="bar-val">$14,500<br><span class="bar-pct">(10.4%)</span></div>
            <div class="bar" style="height: 89px;"></div>
            <div class="bar-title">Periféricos<br>(Mouses/Apuntador)</div>
          </div>
          <!-- 5. Llaves ($10,000 -> 62px) -->
          <div class="bar-col">
            <div class="bar-val">$10,000<br><span class="bar-pct">(7.1%)</span></div>
            <div class="bar" style="height: 62px;"></div>
            <div class="bar-title">Llaves / Candados<br>(Reposición física)</div>
          </div>
        </div>

        <!-- SVG Pareto Cumulative Line -->
        <!-- Centers: 82px, 246px, 410px, 574px, 738px -->
        <!-- Heights from top: 225px (39.3%), 132px (64.3%), 65px (82.5%), 26px (92.9%), 0px (100%) -->
        <svg class="pareto-line">
          <polyline
            fill="none"
            stroke="#D97706"
            stroke-width="3"
            points="82,225 246,132 410,65 574,26 738,0"
          />
          <!-- Dots and labels -->
          <circle cx="82" cy="225" r="5" fill="#D97706" stroke="#fff" stroke-width="2"/>
          <text x="82" y="216" font-size="10" font-weight="bold" fill="#D97706" text-anchor="middle">39.3%</text>

          <circle cx="246" cy="132" r="5" fill="#D97706" stroke="#fff" stroke-width="2"/>
          <text x="272" y="125" font-size="10" font-weight="bold" fill="#D97706" text-anchor="start">64.3%</text>

          <circle cx="410" cy="65" r="6" fill="#DC2626" stroke="#fff" stroke-width="2"/>
          <text x="410" y="54" font-size="10.5" font-weight="800" fill="#DC2626" text-anchor="middle">82.5%</text>

          <circle cx="574" cy="26" r="5" fill="#D97706" stroke="#fff" stroke-width="2"/>
          <text x="574" y="18" font-size="10" font-weight="bold" fill="#D97706" text-anchor="middle">92.9%</text>

          <circle cx="738" cy="0" r="5" fill="#D97706" stroke="#fff" stroke-width="2"/>
          <text x="738" y="14" font-size="10" font-weight="bold" fill="#D97706" text-anchor="end">100%</text>
        </svg>
      </div>
    </div>

    <div class="legend">
      <div class="legend-item"><div class="box-bar"></div><span>Costo Estimado Anual ($ MXN)</span></div>
      <div class="legend-item"><div class="line-pareto"></div><span>% Acumulado de Merma</span></div>
      <div class="legend-item"><div class="line-cutoff"></div><span>Regla 80/20 (82.5% acumulado en Top 3)</span></div>
    </div>
  </body>
  </html>
  `;

  await page.setContent(fig2Html);
  const fig2Path = path.resolve(__dirname, '../docs/graficos/figura2_grafico_pareto_criterios_costo.png');
  await page.screenshot({ path: fig2Path, type: 'png' });
  console.log('✅ Figura 2 generada exitosamente:', fig2Path);

  // -------------------------------------------------------------------------
  // FIGURA 3: Curva de Payback y Ahorro Acumulado
  // -------------------------------------------------------------------------
  const fig3Html = `
  <!DOCTYPE html>
  <html>
  <head>
    <meta charset="utf-8">
    <style>
      body {
        margin: 0;
        padding: 24px;
        background: #ffffff;
        font-family: 'Segoe UI', Arial, sans-serif;
        color: #1A202C;
        box-sizing: border-box;
      }
      .title-container {
        text-align: center;
        margin-bottom: 20px;
      }
      .title {
        font-size: 15px;
        font-weight: 800;
        color: #002B49;
        margin: 0 0 4px 0;
      }
      .subtitle {
        font-size: 11.5px;
        color: #4A5568;
        margin: 0;
      }
      .chart-container {
        position: relative;
        width: 820px;
        height: 380px;
        border-left: 2px solid #002B49;
        border-bottom: 2px solid #002B49;
        margin-left: 65px;
      }
      .grid-line {
        position: absolute;
        left: 0;
        width: 100%;
        border-top: 1px dashed #E2E8F0;
      }
      .grid-line-vert {
        position: absolute;
        bottom: 0;
        height: 100%;
        border-left: 1px dashed #E2E8F0;
      }
      .y-label {
        position: absolute;
        left: -65px;
        font-size: 10px;
        font-weight: 600;
        color: #002B49;
        text-align: right;
        width: 55px;
      }
      .x-label {
        position: absolute;
        bottom: -22px;
        font-size: 9.5px;
        font-weight: 600;
        color: #4A5568;
        text-align: center;
        width: 40px;
        margin-left: -20px;
      }
      svg.chart-svg {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
      }
      .legend {
        display: flex;
        justify-content: center;
        gap: 20px;
        margin-top: 35px;
        font-size: 10px;
        font-weight: 600;
      }
      .legend-item {
        display: flex;
        align-items: center;
        gap: 6px;
      }
      .line-local {
        width: 20px;
        height: 3px;
        background: #002B49;
      }
      .line-scale {
        width: 20px;
        height: 3px;
        border-top: 3px dashed #2563EB;
      }
      .line-zero {
        width: 20px;
        height: 2px;
        background: #10B981;
      }
    </style>
  </head>
  <body>
    <div class="title-container">
      <div class="title">Evaluación Financiera: Amortización de Inversión Inicial (CAPEX $140,000 MXN)</div>
      <div class="subtitle">Curva de Payback en Modelo Local CUTonalá (Mes 19.5) y Modelo de Escalamiento Red UdeG (Mes 29.6)</div>
    </div>

    <div class="chart-container">
      <!-- Total Y range: -$180,000 to +$120,000 (Total = $300,000 -> 380px -> 1k = 1.266px) -->
      <!-- Zero Line: -$180k is at bottom 0, $0 is at 180 * 1.266 = 228px from bottom (152px from top) -->
      
      <!-- Horizontal Grids -->
      <div class="grid-line" style="top: 0px;"><span class="y-label">+$120k</span></div>
      <div class="grid-line" style="top: 76px;"><span class="y-label">+$60k</span></div>
      <div class="grid-line" style="top: 152px; border-top: 2px solid #10B981;"><span class="y-label" style="color: #10B981; font-weight: bold;">$0 (Equil.)</span></div>
      <div class="grid-line" style="top: 228px;"><span class="y-label">-$60k</span></div>
      <div class="grid-line" style="top: 304px;"><span class="y-label">-$120k</span></div>
      <div class="grid-line" style="top: 380px;"><span class="y-label">-$180k</span></div>

      <!-- Vertical Grids (Months 0, 6, 12, 18, 24, 30, 36) -> Width = 820px -> 1 month = 22.77px -->
      <div class="grid-line-vert" style="left: 0px;"><span class="x-label">M0</span></div>
      <div class="grid-line-vert" style="left: 136px;"><span class="x-label">M6</span></div>
      <div class="grid-line-vert" style="left: 273px;"><span class="x-label">M12</span></div>
      <div class="grid-line-vert" style="left: 410px;"><span class="x-label">M18</span></div>
      <div class="grid-line-vert" style="left: 546px;"><span class="x-label">M24</span></div>
      <div class="grid-line-vert" style="left: 683px;"><span class="x-label">M30</span></div>
      <div class="grid-line-vert" style="left: 820px;"><span class="x-label">M36</span></div>

      <svg class="chart-svg">
        <!-- Zero Line Highlight -->
        <line x1="0" y1="152" x2="820" y2="152" stroke="#10B981" stroke-width="2" />

        <!-- 1. Modelo Local CUTonalá:
             Month 0: -$140,000 -> Y = 152 + 140*1.266 = 329px
             Month 19.5: $0 -> X = 19.49 * 22.77 = 444px, Y = 152px
             Month 36: -$140k + 36 * (86.2k / 12) = -$140k + $258.6k = +$118.6k -> Y = 152 - 118.6*1.266 = 2px, X = 820px
        -->
        <!-- Filled polygon for local recovery zone -->
        <polygon points="0,329 444,152 0,152" fill="#EF4444" fill-opacity="0.08" />
        <polygon points="444,152 820,2 820,152" fill="#10B981" fill-opacity="0.12" />

        <line x1="0" y1="329" x2="820" y2="2" stroke="#002B49" stroke-width="3" />

        <!-- 2. Modelo Escalamiento Red UdeG (Dashboard):
             Month 0: -$140,000 -> (0, 329)
             Month 12: -$162,000 -> Y = 152 + 162*1.266 = 357px, X = 273px
             Month 24: -$94,000 -> Y = 152 + 94*1.266 = 271px, X = 546px
             Month 29.6: $0 -> X = 29.64 * 22.77 = 675px, Y = 152px
             Month 36: +$106,000 -> Y = 152 - 106*1.266 = 18px, X = 820px
        -->
        <polyline
          fill="none"
          stroke="#2563EB"
          stroke-width="2.5"
          stroke-dasharray="6,4"
          points="0,329 273,357 546,271 675,152 820,18"
        />

        <!-- Marker Payback Local (Mes 19.5) -->
        <circle cx="444" cy="152" r="6" fill="#002B49" stroke="#fff" stroke-width="2"/>
        <rect x="360" y="85" width="170" height="45" rx="5" fill="#F0F4F8" stroke="#002B49" stroke-width="1.5"/>
        <text x="445" y="103" font-size="10" font-weight="bold" fill="#002B49" text-anchor="middle">Payback Local CUTonalá</text>
        <text x="445" y="120" font-size="9" fill="#2D3748" text-anchor="middle">Mes 19.5 ($140k amortizados)</text>
        <line x1="444" y1="130" x2="444" y2="145" stroke="#002B49" stroke-width="1.5"/>

        <!-- Marker Payback Escalamiento (Mes 29.6) -->
        <circle cx="675" cy="152" r="6" fill="#2563EB" stroke="#fff" stroke-width="2"/>
        <rect x="585" y="180" width="180" height="45" rx="5" fill="#EFF6FF" stroke="#2563EB" stroke-width="1.5"/>
        <text x="675" y="198" font-size="10" font-weight="bold" fill="#2563EB" text-anchor="middle">Payback Escalamiento Red</text>
        <text x="675" y="215" font-size="9" fill="#2D3748" text-anchor="middle">Mes 29.6 (Superávit +$106k)</text>
        <line x1="675" y1="180" x2="675" y2="160" stroke="#2563EB" stroke-width="1.5"/>
      </svg>
    </div>

    <div class="legend">
      <div class="legend-item"><div class="line-local"></div><span>Modelo Local CUTonalá (Ahorro Neto $86.2k/año — Payback Mes 19.5)</span></div>
      <div class="legend-item"><div class="line-scale"></div><span>Modelo Escalamiento Red UdeG (Dashboard — Payback Mes 29.6)</span></div>
      <div class="legend-item"><div class="line-zero"></div><span>Punto de Equilibrio (Flujo = $0)</span></div>
    </div>
  </body>
  </html>
  `;

  await page.setContent(fig3Html);
  const fig3Path = path.resolve(__dirname, '../docs/graficos/figura3_curva_economias_escala_punto_equilibrio.png');
  await page.screenshot({ path: fig3Path, type: 'png' });
  console.log('✅ Figura 3 generada exitosamente:', fig3Path);

  await browser.close();
}

renderCharts().catch(console.error);
