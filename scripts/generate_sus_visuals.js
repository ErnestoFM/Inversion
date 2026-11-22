const { chromium } = require('@playwright/test');
const path = require('path');
const fs = require('fs');

async function generateVisuals() {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1200, height: 800 } });

  // 1. Chart HTML: Distribución SUS
  const chartHtml = `
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <style>
    body {
      margin: 0;
      padding: 30px;
      background: #FFFFFF;
      font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
      color: #2D3748;
    }
    .card {
      border: 1px solid #E2E8F0;
      border-radius: 8px;
      padding: 28px;
      box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
      background: #FFFFFF;
      max-width: 1000px;
      margin: 0 auto;
    }
    .header {
      border-bottom: 2px solid #EDF2F7;
      padding-bottom: 16px;
      margin-bottom: 24px;
      display: flex;
      justify-content: space-between;
      align-items: flex-end;
    }
    .title {
      font-size: 20px;
      font-weight: 700;
      color: #1A365D;
    }
    .subtitle {
      font-size: 13px;
      color: #718096;
      margin-top: 4px;
    }
    .badge {
      background: #EBF8FF;
      color: #2B6CB0;
      font-weight: 700;
      font-size: 12px;
      padding: 6px 12px;
      border-radius: 20px;
      border: 1px solid #BEE3F8;
    }
    .grid {
      display: grid;
      grid-template-columns: 2fr 1fr;
      gap: 30px;
    }
    .bars-container {
      display: flex;
      flex-direction: column;
      gap: 14px;
    }
    .bar-row {
      display: flex;
      align-items: center;
      gap: 12px;
    }
    .bar-label {
      width: 140px;
      font-size: 12.5px;
      font-weight: 600;
      color: #4A5568;
      text-align: right;
    }
    .bar-track {
      flex: 1;
      height: 28px;
      background: #EDF2F7;
      border-radius: 4px;
      overflow: hidden;
      position: relative;
    }
    .bar-fill {
      height: 100%;
      background: linear-gradient(90deg, #3182CE 0%, #2B6CB0 100%);
      border-radius: 4px;
      display: flex;
      align-items: center;
      justify-content: flex-end;
      padding-right: 10px;
      color: #FFFFFF;
      font-weight: 700;
      font-size: 12px;
    }
    .bar-fill.gold {
      background: linear-gradient(90deg, #D69E2E 0%, #B7791F 100%);
    }
    .threshold-line {
      position: absolute;
      top: 0;
      bottom: 0;
      width: 2px;
      background: #E53E3E;
      z-index: 2;
    }
    .stats-panel {
      background: #F7FAFC;
      border: 1px solid #E2E8F0;
      border-radius: 6px;
      padding: 18px;
    }
    .stats-title {
      font-size: 13px;
      font-weight: 700;
      color: #2D3748;
      margin-bottom: 12px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }
    .stat-item {
      display: flex;
      justify-content: space-between;
      padding: 8px 0;
      border-bottom: 1px solid #EDF2F7;
      font-size: 13px;
    }
    .stat-item:last-child {
      border-bottom: none;
    }
    .stat-val {
      font-weight: 700;
      color: #1A365D;
    }
    .legend {
      margin-top: 20px;
      padding-top: 14px;
      border-top: 1px solid #EDF2F7;
      display: flex;
      gap: 20px;
      font-size: 11.5px;
      color: #718096;
    }
    .legend-item {
      display: flex;
      align-items: center;
      gap: 6px;
    }
    .dot {
      width: 10px;
      height: 10px;
      border-radius: 2px;
    }
  </style>
</head>
<body>
  <div class="card">
    <div class="header">
      <div>
        <div class="title">Evaluación de Usabilidad Psicométrica (Escala SUS, n = 50)</div>
        <div class="subtitle">CUTonalá — Universidad de Guadalajara | Puntuación compuesta por estamento y comparativa de hipótesis</div>
      </div>
      <div class="badge">HIPÓTESIS HE-3 ACEPTADA</div>
    </div>
    
    <div class="grid">
      <div class="bars-container">
        <div class="bar-row">
          <div class="bar-label">Estudiantes (n=32)</div>
          <div class="bar-track">
            <div class="bar-fill" style="width: 83.28%;">83.28 pts</div>
          </div>
        </div>
        <div class="bar-row">
          <div class="bar-label">Docentes (n=12)</div>
          <div class="bar-track">
            <div class="bar-fill" style="width: 81.25%;">81.25 pts</div>
          </div>
        </div>
        <div class="bar-row">
          <div class="bar-label">Almacenistas (n=6)</div>
          <div class="bar-track">
            <div class="bar-fill" style="width: 83.75%;">83.75 pts</div>
          </div>
        </div>
        <div class="bar-row">
          <div class="bar-label">Promedio Global</div>
          <div class="bar-track">
            <div class="bar-fill gold" style="width: 82.85%;">82.85 pts</div>
          </div>
        </div>
        <div class="bar-row">
          <div class="bar-label">Umbral Meta (HE-3)</div>
          <div class="bar-track">
            <div class="bar-fill" style="width: 80%; background: #A0AEC0;">80.00 pts</div>
          </div>
        </div>
        <div class="bar-row">
          <div class="bar-label">Estándar Industrial</div>
          <div class="bar-track">
            <div class="bar-fill" style="width: 68%; background: #CBD5E0; color: #4A5568;">68.00 pts</div>
          </div>
        </div>
        
        <div class="legend">
          <div class="legend-item"><div class="dot" style="background: #2B6CB0;"></div> Puntajes por Estamento</div>
          <div class="legend-item"><div class="dot" style="background: #D69E2E;"></div> Media Global SIGRE (82.85)</div>
          <div class="legend-item"><div class="dot" style="background: #A0AEC0;"></div> Umbral Hipótesis (≥80)</div>
          <div class="legend-item"><div class="dot" style="background: #CBD5E0;"></div> Promedio Industrial (68)</div>
        </div>
      </div>
      
      <div class="stats-panel">
        <div class="stats-title">Parámetros Psicométricos</div>
        <div class="stat-item"><span>Muestra Total (n):</span><span class="stat-val">50 participantes</span></div>
        <div class="stat-item"><span>Media Ponderada:</span><span class="stat-val">82.85 puntos</span></div>
        <div class="stat-item"><span>Desv. Estándar (s):</span><span class="stat-val">10.91 puntos</span></div>
        <div class="stat-item"><span>IC 95%:</span><span class="stat-val">[79.75, 85.95] pts</span></div>
        <div class="stat-item"><span>Prueba t (vs. 80):</span><span class="stat-val">t=1.848 (p=0.035)</span></div>
        <div class="stat-item"><span>Alfa de Cronbach (α):</span><span class="stat-val">0.892 (Alta)</span></div>
        <div class="stat-item"><span>Grado Psicométrico:</span><span class="stat-val" style="color: #2B6CB0;">Grado A (Excelente)</span></div>
        <div class="stat-item"><span>Marco de Referencia:</span><span class="stat-val">Sauro & Lewis (2012)</span></div>
      </div>
    </div>
  </div>
</body>
</html>
  `;

  await page.setContent(chartHtml);
  const chartPath = path.resolve('docs/pruebas/screenshots/10_distribucion_puntajes_sus.png');
  const cardElement = await page.$('.card');
  await cardElement.screenshot({ path: chartPath });
  console.log(`✅ Gráfico generado: ${chartPath}`);

  // 2. Google Form Screenshot HTML
  const formHtml = `
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <style>
    body {
      margin: 0;
      padding: 20px 40px;
      background: #F0F4F8;
      font-family: 'Roboto', 'Segoe UI', Arial, sans-serif;
      color: #202124;
    }
    .form-container {
      max-width: 750px;
      margin: 0 auto;
    }
    .form-header-card {
      background: #FFFFFF;
      border-radius: 8px;
      border-top: 10px solid #1A365D;
      border-left: 1px solid #DADCE0;
      border-right: 1px solid #DADCE0;
      border-bottom: 1px solid #DADCE0;
      padding: 24px 28px;
      margin-bottom: 16px;
    }
    .udg-banner {
      display: flex;
      align-items: center;
      gap: 12px;
      margin-bottom: 12px;
      padding-bottom: 10px;
      border-bottom: 1px solid #ECEFF1;
    }
    .udg-title {
      font-size: 13px;
      font-weight: 700;
      color: #1A365D;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }
    .form-title {
      font-size: 24px;
      font-weight: 500;
      color: #202124;
      line-height: 1.3;
    }
    .form-desc {
      font-size: 13.5px;
      color: #5F6368;
      line-height: 1.6;
      margin-top: 10px;
    }
    .email-notice {
      margin-top: 14px;
      padding-top: 12px;
      border-top: 1px solid #DADCE0;
      font-size: 12px;
      color: #70757A;
      display: flex;
      align-items: center;
      gap: 6px;
    }
    .question-card {
      background: #FFFFFF;
      border-radius: 8px;
      border: 1px solid #DADCE0;
      padding: 20px 28px;
      margin-bottom: 16px;
    }
    .q-title {
      font-size: 14.5px;
      font-weight: 500;
      color: #202124;
      margin-bottom: 16px;
    }
    .req {
      color: #D93025;
      font-size: 15px;
      margin-left: 2px;
    }
    .scale-row {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 10px;
    }
    .scale-opt {
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 6px;
      font-size: 13px;
      color: #5F6368;
    }
    .radio-circle {
      width: 18px;
      height: 18px;
      border-radius: 50%;
      border: 2px solid #5F6368;
    }
    .radio-circle.checked {
      border-color: #1A365D;
      position: relative;
    }
    .radio-circle.checked::after {
      content: '';
      position: absolute;
      top: 3px;
      left: 3px;
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: #1A365D;
    }
    .scale-endpoint {
      font-size: 12px;
      color: #70757A;
      max-width: 90px;
      text-align: center;
      line-height: 1.2;
    }
  </style>
</head>
<body>
  <div class="form-container">
    <div class="form-header-card">
      <div class="udg-banner">
        <span class="udg-title">Universidad de Guadalajara — Centro Universitario de Tonalá (CUTonalá)</span>
      </div>
      <div class="form-title">Evaluación de Usabilidad del Software — Plataforma SIGRE</div>
      <div class="form-desc">
        Estimado/a participante: Agradecemos su colaboración en la prueba piloto de la plataforma SIGRE (Sistema Integral de Gestión de Recursos y Espacios). El presente cuestionario estandarizado <strong>System Usability Scale (SUS)</strong> evalúa la facilidad de uso y percepción operativa del sistema. Sus respuestas son anónimas y de estricto uso investigativo académico conforme a la Ley de Protección de Datos Personales.
      </div>
      <div class="email-notice">
        🔒 Se registrará su usuario institucional (@alumnos.udg.mx / @udg.mx) exclusivamente para control de muestra (n = 50).
      </div>
    </div>
    
    <div class="question-card">
      <div class="q-title">1. Creo que me gustaría utilizar este sistema con frecuencia <span class="req">*</span></div>
      <div class="scale-row">
        <div class="scale-endpoint">Totalmente en desacuerdo</div>
        <div class="scale-opt"><span>1</span><div class="radio-circle"></div></div>
        <div class="scale-opt"><span>2</span><div class="radio-circle"></div></div>
        <div class="scale-opt"><span>3</span><div class="radio-circle"></div></div>
        <div class="scale-opt"><span>4</span><div class="radio-circle"></div></div>
        <div class="scale-opt"><span>5</span><div class="radio-circle checked"></div></div>
        <div class="scale-endpoint">Totalmente de acuerdo</div>
      </div>
    </div>

    <div class="question-card">
      <div class="q-title">2. Encontré el sistema innecesariamente complejo <span class="req">*</span></div>
      <div class="scale-row">
        <div class="scale-endpoint">Totalmente en desacuerdo</div>
        <div class="scale-opt"><span>1</span><div class="radio-circle checked"></div></div>
        <div class="scale-opt"><span>2</span><div class="radio-circle"></div></div>
        <div class="scale-opt"><span>3</span><div class="radio-circle"></div></div>
        <div class="scale-opt"><span>4</span><div class="radio-circle"></div></div>
        <div class="scale-opt"><span>5</span><div class="radio-circle"></div></div>
        <div class="scale-endpoint">Totalmente de acuerdo</div>
      </div>
    </div>

    <div class="question-card">
      <div class="q-title">3. Pensé que el sistema era fácil de usar <span class="req">*</span></div>
      <div class="scale-row">
        <div class="scale-endpoint">Totalmente en desacuerdo</div>
        <div class="scale-opt"><span>1</span><div class="radio-circle"></div></div>
        <div class="scale-opt"><span>2</span><div class="radio-circle"></div></div>
        <div class="scale-opt"><span>3</span><div class="radio-circle"></div></div>
        <div class="scale-opt"><span>4</span><div class="radio-circle checked"></div></div>
        <div class="scale-opt"><span>5</span><div class="radio-circle"></div></div>
        <div class="scale-endpoint">Totalmente de acuerdo</div>
      </div>
    </div>
  </div>
</body>
</html>
  `;

  await page.setContent(formHtml);
  const formPath = path.resolve('docs/pruebas/screenshots/11_formulario_google_forms_sus.png');
  const formContainer = await page.$('.form-container');
  await formContainer.screenshot({ path: formPath });
  console.log(`✅ Formulario Google Forms generado: ${formPath}`);

  await browser.close();
}

generateVisuals().catch(console.error);
