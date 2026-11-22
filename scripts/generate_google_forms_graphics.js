const { chromium } = require('@playwright/test');
const path = require('path');
const fs = require('fs');

async function renderFormsGraphics() {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1200, height: 1600, deviceScaleFactor: 2 } });

  // 1. Google Forms Dashboard & Demographic + R1 + R2
  const html1 = `
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <style>
    body {
      margin: 0;
      padding: 24px;
      background: #F0F4F9;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
      color: #202124;
    }
    .forms-shell {
      max-width: 900px;
      margin: 0 auto;
    }
    /* Google Forms Navigation Bar */
    .nav-bar {
      background: #FFFFFF;
      border-radius: 8px 8px 0 0;
      border: 1px solid #DADCE0;
      border-bottom: none;
      padding: 16px 24px 0 24px;
    }
    .form-header-title {
      font-size: 22px;
      font-weight: 500;
      color: #202124;
      margin-bottom: 16px;
      display: flex;
      align-items: center;
      gap: 10px;
    }
    .udg-pill {
      background: #1A365D;
      color: #FFFFFF;
      font-size: 11px;
      font-weight: 700;
      padding: 3px 8px;
      border-radius: 4px;
      letter-spacing: 0.5px;
    }
    .tabs-row {
      display: flex;
      gap: 32px;
      border-bottom: 1px solid #DADCE0;
    }
    .tab {
      padding-bottom: 12px;
      font-size: 14px;
      font-weight: 500;
      color: #5F6368;
      cursor: pointer;
    }
    .tab.active {
      color: #1A73E8;
      border-bottom: 3px solid #1A73E8;
      font-weight: 600;
    }
    /* Response Subheader Toolbar */
    .response-toolbar {
      background: #FFFFFF;
      border-left: 1px solid #DADCE0;
      border-right: 1px solid #DADCE0;
      border-bottom: 1px solid #DADCE0;
      border-radius: 0 0 8px 8px;
      padding: 18px 24px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 20px;
    }
    .resp-count-title {
      font-size: 26px;
      font-weight: 400;
      color: #202124;
    }
    .resp-controls {
      display: flex;
      align-items: center;
      gap: 20px;
    }
    .sheets-btn {
      display: flex;
      align-items: center;
      gap: 8px;
      color: #137333;
      font-size: 13px;
      font-weight: 600;
      background: #E6F4EA;
      padding: 8px 14px;
      border-radius: 4px;
      border: 1px solid #CEEAD6;
    }
    .sheets-icon {
      width: 18px;
      height: 18px;
      background: #0F9D58;
      color: #FFF;
      border-radius: 2px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 11px;
      font-weight: bold;
    }
    .toggle-group {
      display: flex;
      align-items: center;
      gap: 10px;
      font-size: 13.5px;
      color: #3C4043;
    }
    .toggle-switch {
      width: 38px;
      height: 20px;
      background: #1A73E8;
      border-radius: 12px;
      position: relative;
    }
    .toggle-switch::after {
      content: '';
      position: absolute;
      top: 2px;
      right: 2px;
      width: 16px;
      height: 16px;
      border-radius: 50%;
      background: #FFFFFF;
    }

    /* Google Forms Card */
    .card {
      background: #FFFFFF;
      border: 1px solid #DADCE0;
      border-radius: 8px;
      padding: 24px;
      margin-bottom: 20px;
      box-shadow: 0 1px 2px rgba(60,64,67,0.08);
    }
    .q-title {
      font-size: 15px;
      font-weight: 500;
      color: #202124;
      margin-bottom: 4px;
    }
    .q-sub {
      font-size: 12.5px;
      color: #5F6368;
      margin-bottom: 20px;
    }
    
    /* Pie Chart Layout */
    .pie-layout {
      display: flex;
      align-items: center;
      justify-content: space-around;
      padding: 10px 0;
    }
    .pie-legend {
      display: flex;
      flex-direction: column;
      gap: 12px;
    }
    .legend-row {
      display: flex;
      align-items: center;
      gap: 10px;
      font-size: 13.5px;
      color: #3C4043;
    }
    .legend-color {
      width: 14px;
      height: 14px;
      border-radius: 50%;
    }
    .legend-pct {
      font-weight: 600;
      color: #202124;
      margin-left: 6px;
    }

    /* Likert Bar Chart */
    .bar-chart-grid {
      display: flex;
      align-items: flex-end;
      justify-content: space-between;
      height: 160px;
      padding: 20px 30px 10px 30px;
      border-bottom: 1px solid #DADCE0;
      gap: 20px;
    }
    .col-group {
      flex: 1;
      display: flex;
      flex-direction: column;
      align-items: center;
      height: 100%;
      justify-content: flex-end;
    }
    .bar-col {
      width: 60%;
      background: #4285F4;
      border-radius: 4px 4px 0 0;
      transition: height 0.3s;
      position: relative;
    }
    .bar-val-label {
      font-size: 12px;
      font-weight: 600;
      color: #3C4043;
      margin-bottom: 6px;
      text-align: center;
    }
    .x-axis-labels {
      display: flex;
      justify-content: space-between;
      padding: 10px 30px 0 30px;
      gap: 20px;
    }
    .x-label {
      flex: 1;
      text-align: center;
      font-size: 12px;
      color: #5F6368;
    }
    .scale-ends {
      display: flex;
      justify-content: space-between;
      padding: 6px 30px 0 30px;
      font-size: 11px;
      color: #70757A;
    }
  </style>
</head>
<body>
  <div class="forms-shell">
    <!-- Navbar -->
    <div class="nav-bar">
      <div class="form-header-title">
        <span class="udg-pill">CUTonalá / UdeG</span>
        Evaluación de Usabilidad del Software — Plataforma SIGRE
      </div>
      <div class="tabs-row">
        <div class="tab">Preguntas</div>
        <div class="tab active">Respuestas (50)</div>
        <div class="tab">Configuración</div>
      </div>
    </div>
    
    <!-- Response Toolbar -->
    <div class="response-toolbar">
      <div class="resp-count-title">50 respuestas</div>
      <div class="resp-controls">
        <div class="sheets-btn">
          <div class="sheets-icon">📊</div>
          Ver en cuestionarios_sus_n50.xlsx
        </div>
        <div class="toggle-group">
          <span>Se aceptan respuestas</span>
          <div class="toggle-switch"></div>
        </div>
      </div>
    </div>

    <!-- Card: Demographic Pie -->
    <div class="card">
      <div class="q-title">Rol Institucional del Participante en CUTonalá</div>
      <div class="q-sub">50 respuestas</div>
      <div class="pie-layout">
        <!-- SVG Donut Chart -->
        <svg width="200" height="200" viewBox="0 0 42 42">
          <!-- Background circle -->
          <circle cx="21" cy="21" r="15.915" fill="#fff" stroke="#E2E8F0" stroke-width="1"></circle>
          <!-- Slice 1: Estudiantes 64% (0 to 64) -> stroke-dasharray="64 36", stroke-dashoffset="25" -->
          <circle cx="21" cy="21" r="15.915" fill="transparent" stroke="#4285F4" stroke-width="8" stroke-dasharray="64 36" stroke-dashoffset="25"></circle>
          <!-- Slice 2: Docentes 24% (64 to 88) -> stroke-dasharray="24 76", stroke-dashoffset="61" (25 - 64 = -39 -> 61) -->
          <circle cx="21" cy="21" r="15.915" fill="transparent" stroke="#EA4335" stroke-width="8" stroke-dasharray="24 76" stroke-dashoffset="61"></circle>
          <!-- Slice 3: Operadores 12% (88 to 100) -> stroke-dasharray="12 88", stroke-dashoffset="37" (61 - 24 = 37) -->
          <circle cx="21" cy="21" r="15.915" fill="transparent" stroke="#FBBC05" stroke-width="8" stroke-dasharray="12 88" stroke-dashoffset="37"></circle>
          <text x="21" y="22" font-size="5" text-anchor="middle" font-weight="bold" fill="#202124">n = 50</text>
        </svg>

        <div class="pie-legend">
          <div class="legend-row">
            <div class="legend-color" style="background: #4285F4;"></div>
            <span>Estudiantes: <strong>32</strong></span>
            <span class="legend-pct">(64.0%)</span>
          </div>
          <div class="legend-row">
            <div class="legend-color" style="background: #EA4335;"></div>
            <span>Docentes / Investigadores: <strong>12</strong></span>
            <span class="legend-pct">(24.0%)</span>
          </div>
          <div class="legend-row">
            <div class="legend-color" style="background: #FBBC05;"></div>
            <span>Operadores de Almacén: <strong>6</strong></span>
            <span class="legend-pct">(12.0%)</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Card: R1 -->
    <div class="card">
      <div class="q-title">1. Creo que me gustaría utilizar este sistema con frecuencia (R1)</div>
      <div class="q-sub">50 respuestas • Media: 4.32 / 5.0 • Desv. Est: 0.62</div>
      <div class="bar-chart-grid">
        <div class="col-group">
          <div class="bar-val-label">0 (0%)</div>
          <div class="bar-col" style="height: 2px; background: #CBD5E0;"></div>
        </div>
        <div class="col-group">
          <div class="bar-val-label">0 (0%)</div>
          <div class="bar-col" style="height: 2px; background: #CBD5E0;"></div>
        </div>
        <div class="col-group">
          <div class="bar-val-label">4 (8%)</div>
          <div class="bar-col" style="height: 18px;"></div>
        </div>
        <div class="col-group">
          <div class="bar-val-label">26 (52%)</div>
          <div class="bar-col" style="height: 112px; background: #1A73E8;"></div>
        </div>
        <div class="col-group">
          <div class="bar-val-label">20 (40%)</div>
          <div class="bar-col" style="height: 86px; background: #1A73E8;"></div>
        </div>
      </div>
      <div class="x-axis-labels">
        <div class="x-label">1</div><div class="x-label">2</div><div class="x-label">3</div><div class="x-label">4</div><div class="x-label">5</div>
      </div>
      <div class="scale-ends">
        <span>Totalmente en desacuerdo</span>
        <span>Totalmente de acuerdo</span>
      </div>
    </div>

    <!-- Card: R2 -->
    <div class="card">
      <div class="q-title">2. Encontré el sistema innecesariamente complejo (R2 - Polaridad Inversa)</div>
      <div class="q-sub">50 respuestas • Media: 1.72 / 5.0 • Desv. Est: 0.64</div>
      <div class="bar-chart-grid">
        <div class="col-group">
          <div class="bar-val-label">19 (38%)</div>
          <div class="bar-col" style="height: 82px; background: #34A853;"></div>
        </div>
        <div class="col-group">
          <div class="bar-val-label">26 (52%)</div>
          <div class="bar-col" style="height: 112px; background: #34A853;"></div>
        </div>
        <div class="col-group">
          <div class="bar-val-label">5 (10%)</div>
          <div class="bar-col" style="height: 22px; background: #FBBC05;"></div>
        </div>
        <div class="col-group">
          <div class="bar-val-label">0 (0%)</div>
          <div class="bar-col" style="height: 2px; background: #CBD5E0;"></div>
        </div>
        <div class="col-group">
          <div class="bar-val-label">0 (0%)</div>
          <div class="bar-col" style="height: 2px; background: #CBD5E0;"></div>
        </div>
      </div>
      <div class="x-axis-labels">
        <div class="x-label">1</div><div class="x-label">2</div><div class="x-label">3</div><div class="x-label">4</div><div class="x-label">5</div>
      </div>
      <div class="scale-ends">
        <span>Totalmente en desacuerdo (Deseable)</span>
        <span>Totalmente de acuerdo</span>
      </div>
    </div>

  </div>
</body>
</html>
  `;

  await page.setContent(html1);
  const outPath1 = path.resolve('docs/pruebas/screenshots/11_google_forms_resumen_respuestas.png');
  const shellElement = await page.$('.forms-shell');
  await shellElement.screenshot({ path: outPath1 });
  console.log(`✅ Captura 11 generada: ${outPath1}`);

  // 2. Google Forms Breakdown R3 to R10 (2 columns grid)
  const html2 = `
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <style>
    body {
      margin: 0;
      padding: 24px;
      background: #F0F4F9;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
      color: #202124;
    }
    .grid-container {
      max-width: 950px;
      margin: 0 auto;
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 18px;
    }
    .card {
      background: #FFFFFF;
      border: 1px solid #DADCE0;
      border-radius: 8px;
      padding: 16px 18px;
      box-shadow: 0 1px 2px rgba(60,64,67,0.08);
    }
    .q-title {
      font-size: 13.5px;
      font-weight: 600;
      color: #202124;
      line-height: 1.3;
      height: 36px;
      display: flex;
      align-items: center;
    }
    .q-sub {
      font-size: 11.5px;
      color: #5F6368;
      margin-bottom: 12px;
      border-bottom: 1px solid #F1F3F4;
      padding-bottom: 4px;
    }
    .bar-chart-mini {
      display: flex;
      align-items: flex-end;
      height: 90px;
      padding: 10px 10px 4px 10px;
      border-bottom: 1px solid #DADCE0;
      gap: 10px;
    }
    .col-mini {
      flex: 1;
      display: flex;
      flex-direction: column;
      align-items: center;
      height: 100%;
      justify-content: flex-end;
    }
    .bar-mini {
      width: 70%;
      background: #1A73E8;
      border-radius: 3px 3px 0 0;
    }
    .bar-mini.green { background: #34A853; }
    .bar-mini.amber { background: #FBBC05; }
    .bar-mini.zero  { background: #E8EAED; height: 2px !important; }
    .val-mini {
      font-size: 10.5px;
      font-weight: 600;
      color: #3C4043;
      margin-bottom: 3px;
    }
    .x-axis-mini {
      display: flex;
      justify-content: space-between;
      padding: 4px 10px 0 10px;
      font-size: 11px;
      color: #5F6368;
    }
    .x-cell {
      flex: 1;
      text-align: center;
    }
    .card-footer {
      display: flex;
      justify-content: space-between;
      font-size: 9.5px;
      color: #80868B;
      margin-top: 4px;
      padding: 0 4px;
    }
  </style>
</head>
<body>
  <div class="grid-container">
    
    <!-- R3 -->
    <div class="card">
      <div class="q-title">3. Pensé que el sistema era fácil de usar</div>
      <div class="q-sub">50 respuestas • Media: 4.26 • Contribución: 3.26</div>
      <div class="bar-chart-mini">
        <div class="col-mini"><div class="val-mini">0</div><div class="bar-mini zero"></div></div>
        <div class="col-mini"><div class="val-mini">0</div><div class="bar-mini zero"></div></div>
        <div class="col-mini"><div class="val-mini">5</div><div class="bar-mini" style="height: 14px;"></div></div>
        <div class="col-mini"><div class="val-mini">27</div><div class="bar-mini" style="height: 68px;"></div></div>
        <div class="col-mini"><div class="val-mini">18</div><div class="bar-mini" style="height: 46px;"></div></div>
      </div>
      <div class="x-axis-mini">
        <div class="x-cell">1</div><div class="x-cell">2</div><div class="x-cell">3</div><div class="x-cell">4</div><div class="x-cell">5</div>
      </div>
      <div class="card-footer"><span>Desacuerdo</span><span>Totalmente de acuerdo</span></div>
    </div>

    <!-- R4 -->
    <div class="card">
      <div class="q-title">4. Creo que necesitaría apoyo técnico (Inv.)</div>
      <div class="q-sub">50 respuestas • Media: 1.78 • Contribución: 3.22</div>
      <div class="bar-chart-mini">
        <div class="col-mini"><div class="val-mini">18</div><div class="bar-mini green" style="height: 48px;"></div></div>
        <div class="col-mini"><div class="val-mini">25</div><div class="bar-mini green" style="height: 64px;"></div></div>
        <div class="col-mini"><div class="val-mini">7</div><div class="bar-mini amber" style="height: 18px;"></div></div>
        <div class="col-mini"><div class="val-mini">0</div><div class="bar-mini zero"></div></div>
        <div class="col-mini"><div class="val-mini">0</div><div class="bar-mini zero"></div></div>
      </div>
      <div class="x-axis-mini">
        <div class="x-cell">1</div><div class="x-cell">2</div><div class="x-cell">3</div><div class="x-cell">4</div><div class="x-cell">5</div>
      </div>
      <div class="card-footer"><span>Total desacuerdo (Bien)</span><span>Total acuerdo</span></div>
    </div>

    <!-- R5 -->
    <div class="card">
      <div class="q-title">5. Diversas funciones bien integradas</div>
      <div class="q-sub">50 respuestas • Media: 4.38 • Contribución: 3.38</div>
      <div class="bar-chart-mini">
        <div class="col-mini"><div class="val-mini">0</div><div class="bar-mini zero"></div></div>
        <div class="col-mini"><div class="val-mini">0</div><div class="bar-mini zero"></div></div>
        <div class="col-mini"><div class="val-mini">4</div><div class="bar-mini" style="height: 12px;"></div></div>
        <div class="col-mini"><div class="val-mini">23</div><div class="bar-mini" style="height: 58px;"></div></div>
        <div class="col-mini"><div class="val-mini">23</div><div class="bar-mini" style="height: 58px;"></div></div>
      </div>
      <div class="x-axis-mini">
        <div class="x-cell">1</div><div class="x-cell">2</div><div class="x-cell">3</div><div class="x-cell">4</div><div class="x-cell">5</div>
      </div>
      <div class="card-footer"><span>Desacuerdo</span><span>Totalmente de acuerdo</span></div>
    </div>

    <!-- R6 -->
    <div class="card">
      <div class="q-title">6. Demasiada inconsistencia (Inv.)</div>
      <div class="q-sub">50 respuestas • Media: 1.68 • Contribución: 3.32</div>
      <div class="bar-chart-mini">
        <div class="col-mini"><div class="val-mini">18</div><div class="bar-mini green" style="height: 48px;"></div></div>
        <div class="col-mini"><div class="val-mini">30</div><div class="bar-mini green" style="height: 76px;"></div></div>
        <div class="col-mini"><div class="val-mini">2</div><div class="bar-mini amber" style="height: 8px;"></div></div>
        <div class="col-mini"><div class="val-mini">0</div><div class="bar-mini zero"></div></div>
        <div class="col-mini"><div class="val-mini">0</div><div class="bar-mini zero"></div></div>
      </div>
      <div class="x-axis-mini">
        <div class="x-cell">1</div><div class="x-cell">2</div><div class="x-cell">3</div><div class="x-cell">4</div><div class="x-cell">5</div>
      </div>
      <div class="card-footer"><span>Total desacuerdo (Bien)</span><span>Total acuerdo</span></div>
    </div>

    <!-- R7 -->
    <div class="card">
      <div class="q-title">7. La mayoría aprendería muy rápido</div>
      <div class="q-sub">50 respuestas • Media: 4.36 • Contribución: 3.36</div>
      <div class="bar-chart-mini">
        <div class="col-mini"><div class="val-mini">0</div><div class="bar-mini zero"></div></div>
        <div class="col-mini"><div class="val-mini">0</div><div class="bar-mini zero"></div></div>
        <div class="col-mini"><div class="val-mini">3</div><div class="bar-mini" style="height: 10px;"></div></div>
        <div class="col-mini"><div class="val-mini">26</div><div class="bar-mini" style="height: 64px;"></div></div>
        <div class="col-mini"><div class="val-mini">21</div><div class="bar-mini" style="height: 52px;"></div></div>
      </div>
      <div class="x-axis-mini">
        <div class="x-cell">1</div><div class="x-cell">2</div><div class="x-cell">3</div><div class="x-cell">4</div><div class="x-cell">5</div>
      </div>
      <div class="card-footer"><span>Desacuerdo</span><span>Totalmente de acuerdo</span></div>
    </div>

    <!-- R8 -->
    <div class="card">
      <div class="q-title">8. Sistema engorroso de utilizar (Inv.)</div>
      <div class="q-sub">50 respuestas • Media: 1.74 • Contribución: 3.26</div>
      <div class="bar-chart-mini">
        <div class="col-mini"><div class="val-mini">16</div><div class="bar-mini green" style="height: 42px;"></div></div>
        <div class="col-mini"><div class="val-mini">31</div><div class="bar-mini green" style="height: 78px;"></div></div>
        <div class="col-mini"><div class="val-mini">3</div><div class="bar-mini amber" style="height: 10px;"></div></div>
        <div class="col-mini"><div class="val-mini">0</div><div class="bar-mini zero"></div></div>
        <div class="col-mini"><div class="val-mini">0</div><div class="bar-mini zero"></div></div>
      </div>
      <div class="x-axis-mini">
        <div class="x-cell">1</div><div class="x-cell">2</div><div class="x-cell">3</div><div class="x-cell">4</div><div class="x-cell">5</div>
      </div>
      <div class="card-footer"><span>Total desacuerdo (Bien)</span><span>Total acuerdo</span></div>
    </div>

    <!-- R9 -->
    <div class="card">
      <div class="q-title">9. Me sentí seguro y confiado al usarlo</div>
      <div class="q-sub">50 respuestas • Media: 4.42 • Contribución: 3.42</div>
      <div class="bar-chart-mini">
        <div class="col-mini"><div class="val-mini">0</div><div class="bar-mini zero"></div></div>
        <div class="col-mini"><div class="val-mini">0</div><div class="bar-mini zero"></div></div>
        <div class="col-mini"><div class="val-mini">2</div><div class="bar-mini" style="height: 8px;"></div></div>
        <div class="col-mini"><div class="val-mini">25</div><div class="bar-mini" style="height: 62px;"></div></div>
        <div class="col-mini"><div class="val-mini">23</div><div class="bar-mini" style="height: 58px;"></div></div>
      </div>
      <div class="x-axis-mini">
        <div class="x-cell">1</div><div class="x-cell">2</div><div class="x-cell">3</div><div class="x-cell">4</div><div class="x-cell">5</div>
      </div>
      <div class="card-footer"><span>Desacuerdo</span><span>Totalmente de acuerdo</span></div>
    </div>

    <!-- R10 -->
    <div class="card">
      <div class="q-title">10. Necesité aprender muchas cosas (Inv.)</div>
      <div class="q-sub">50 respuestas • Media: 1.68 • Contribución: 3.32</div>
      <div class="bar-chart-mini">
        <div class="col-mini"><div class="val-mini">20</div><div class="bar-mini green" style="height: 52px;"></div></div>
        <div class="col-mini"><div class="val-mini">26</div><div class="bar-mini green" style="height: 66px;"></div></div>
        <div class="col-mini"><div class="val-mini">4</div><div class="bar-mini amber" style="height: 12px;"></div></div>
        <div class="col-mini"><div class="val-mini">0</div><div class="bar-mini zero"></div></div>
        <div class="col-mini"><div class="val-mini">0</div><div class="bar-mini zero"></div></div>
      </div>
      <div class="x-axis-mini">
        <div class="x-cell">1</div><div class="x-cell">2</div><div class="x-cell">3</div><div class="x-cell">4</div><div class="x-cell">5</div>
      </div>
      <div class="card-footer"><span>Total desacuerdo (Bien)</span><span>Total acuerdo</span></div>
    </div>

  </div>
</body>
</html>
  `;

  await page.setContent(html2);
  const outPath2 = path.resolve('docs/pruebas/screenshots/12_google_forms_desglose_reactivos.png');
  const gridElement = await page.$('.grid-container');
  await gridElement.screenshot({ path: outPath2 });
  console.log(`✅ Captura 12 generada: ${outPath2}`);

  await browser.close();
}

renderFormsGraphics().catch(console.error);
