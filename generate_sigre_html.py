import os
import json

def generate_html_presentation():
    html_content = """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Plataforma SIGRE — Presentación Oficial ExpoDIT 2026</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg-dark: #0D1B2A;
      --bg-surface: #1A1A2E;
      --bg-card: #162447;
      --bg-card-elev: #1E293B;
      --border: #334155;
      --navy-udeg: #002B49;
      --cyan: #38BDF8;
      --cyan-light: #7DD3FC;
      --green: #2E7D57;
      --green-bright: #4ADE80;
      --amber: #D97706;
      --amber-bright: #FBBF24;
      --red: #EF4444;
      --text-white: #F8FAFC;
      --text-muted: #94A3B8;
      --font-main: 'Outfit', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      --font-mono: 'JetBrains Mono', monospace;
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }

    body {
      background-color: #070D14;
      color: var(--text-white);
      font-family: var(--font-main);
      overflow-x: hidden;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: flex-start;
    }

    /* TOP TOOLBAR */
    .toolbar {
      width: 100%;
      max-width: 1360px;
      padding: 10px 20px;
      background: rgba(13, 27, 42, 0.85);
      backdrop-filter: blur(12px);
      border-bottom: 1px solid var(--border);
      display: flex;
      align-items: center;
      justify-content: space-between;
      position: sticky;
      top: 0;
      z-index: 100;
    }

    .toolbar-brand {
      display: flex;
      align-items: center;
      gap: 12px;
    }

    .toolbar-logo {
      height: 28px;
    }

    .toolbar-title {
      font-size: 14px;
      font-weight: 700;
      letter-spacing: 0.5px;
      color: var(--cyan);
    }

    .toolbar-controls {
      display: flex;
      align-items: center;
      gap: 12px;
    }

    .btn {
      background: var(--bg-card-elev);
      color: var(--text-white);
      border: 1px solid var(--border);
      padding: 6px 14px;
      border-radius: 8px;
      font-family: var(--font-main);
      font-size: 12px;
      font-weight: 600;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      transition: all 0.2s ease;
    }

    .btn:hover {
      background: var(--navy-udeg);
      border-color: var(--cyan);
      color: var(--cyan-light);
      transform: translateY(-1px);
    }

    .btn-primary {
      background: var(--navy-udeg);
      border-color: var(--cyan);
      color: var(--cyan);
    }

    .btn-active {
      background: var(--cyan);
      color: #0D1B2A;
      border-color: var(--cyan-light);
    }

    /* TIMER DISPLAY */
    .timer-badge {
      display: flex;
      align-items: center;
      gap: 8px;
      background: rgba(15, 23, 42, 0.9);
      border: 1px solid var(--border);
      padding: 5px 12px;
      border-radius: 8px;
      font-family: var(--font-mono);
      font-size: 13px;
      font-weight: 600;
      color: var(--green-bright);
    }

    .timer-badge.warning {
      color: var(--amber-bright);
      border-color: var(--amber);
    }

    .timer-badge.danger {
      color: var(--red);
      border-color: var(--red);
      animation: pulse 1s infinite;
    }

    @keyframes pulse {
      0%, 100% { opacity: 1; }
      50% { opacity: 0.5; }
    }

    /* SLIDE STAGE (16:9) */
    .stage-container {
      width: 100%;
      max-width: 1360px;
      padding: 20px;
      display: flex;
      flex-direction: column;
      align-items: center;
    }

    .slide-wrapper {
      width: 100%;
      aspect-ratio: 16 / 9;
      background: var(--bg-dark);
      border: 1px solid var(--border);
      border-radius: 14px;
      overflow: hidden;
      position: relative;
      box-shadow: 0 25px 60px rgba(0, 0, 0, 0.6), 0 0 40px rgba(56, 189, 248, 0.08);
      display: flex;
      flex-direction: column;
    }

    .slide {
      width: 100%;
      height: 100%;
      display: none;
      flex-direction: column;
      padding: 32px 42px;
      position: relative;
      background: radial-gradient(circle at 90% 10%, rgba(56, 189, 248, 0.07) 0%, transparent 50%),
                  radial-gradient(circle at 10% 90%, rgba(46, 125, 87, 0.08) 0%, transparent 50%),
                  var(--bg-dark);
    }

    .slide.active {
      display: flex;
    }

    /* TOP ACCENT BAR */
    .slide::before {
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      height: 4px;
      background: linear-gradient(90deg, var(--navy-udeg), var(--cyan), var(--green-bright));
    }

    /* SLIDE HEADER */
    .slide-header {
      margin-bottom: 20px;
      position: relative;
    }

    .slide-category {
      font-size: 11px;
      font-weight: 800;
      letter-spacing: 1.5px;
      text-transform: uppercase;
      color: var(--cyan);
      margin-bottom: 4px;
      display: flex;
      align-items: center;
      gap: 6px;
    }

    .slide-category::before {
      content: '';
      display: inline-block;
      width: 8px;
      height: 8px;
      background: var(--cyan);
      border-radius: 2px;
    }

    .slide-title {
      font-size: 26px;
      font-weight: 700;
      color: var(--text-white);
      line-height: 1.2;
      margin-bottom: 4px;
    }

    .slide-subtitle {
      font-size: 13.5px;
      color: var(--text-muted);
      line-height: 1.35;
    }

    .slide-corner-logo {
      position: absolute;
      top: 0;
      right: 0;
      height: 42px;
      opacity: 0.9;
    }

    /* SLIDE CONTENT AREA */
    .slide-body {
      flex: 1;
      display: flex;
      gap: 24px;
      min-height: 0;
    }

    /* SLIDE FOOTER */
    .slide-footer {
      height: 32px;
      border-top: 1px solid var(--border);
      margin-top: 16px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      font-size: 11px;
      color: var(--text-muted);
    }

    .slide-footer-left {
      font-weight: 500;
    }

    .slide-footer-center {
      color: var(--text-muted);
    }

    .slide-footer-right {
      font-weight: 700;
      color: var(--cyan-light);
    }

    /* CARDS & CONTAINERS */
    .card {
      background: rgba(26, 26, 46, 0.85);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 18px 20px;
      display: flex;
      flex-direction: column;
      position: relative;
      overflow: hidden;
    }

    .card-elevated {
      background: rgba(30, 41, 59, 0.85);
    }

    .card-border-cyan { border-color: rgba(56, 189, 248, 0.4); }
    .card-border-green { border-color: rgba(74, 222, 128, 0.4); }
    .card-border-amber { border-color: rgba(251, 191, 36, 0.4); }
    .card-border-red { border-color: rgba(239, 68, 68, 0.4); }

    .card-icon-title {
      display: flex;
      align-items: center;
      gap: 10px;
      margin-bottom: 8px;
    }

    .card-icon {
      font-size: 20px;
    }

    .card-title {
      font-size: 15px;
      font-weight: 700;
      color: var(--text-white);
    }

    .card-desc {
      font-size: 12px;
      color: var(--text-muted);
      line-height: 1.45;
      margin-bottom: 10px;
    }

    .badge {
      display: inline-flex;
      align-items: center;
      gap: 5px;
      padding: 4px 10px;
      border-radius: 6px;
      font-size: 11px;
      font-weight: 700;
      margin-bottom: 10px;
      align-self: flex-start;
    }

    .badge-red { background: rgba(239, 68, 68, 0.15); color: #F87171; border: 1px solid rgba(239, 68, 68, 0.3); }
    .badge-amber { background: rgba(217, 119, 6, 0.15); color: #FBBF24; border: 1px solid rgba(217, 119, 6, 0.3); }
    .badge-green { background: rgba(46, 125, 87, 0.2); color: #4ADE80; border: 1px solid rgba(74, 222, 128, 0.3); }
    .badge-cyan { background: rgba(56, 189, 248, 0.15); color: #38BDF8; border: 1px solid rgba(56, 189, 248, 0.3); }

    .bullet-list {
      list-style: none;
      display: flex;
      flex-direction: column;
      gap: 6px;
    }

    .bullet-list li {
      font-size: 11.5px;
      color: var(--text-muted);
      line-height: 1.4;
      display: flex;
      align-items: flex-start;
      gap: 6px;
    }

    .bullet-list li::before {
      content: '•';
      color: var(--cyan);
      font-size: 14px;
      line-height: 1;
    }

    .bullet-list li strong {
      color: var(--text-white);
    }

    /* GRID LAYOUTS */
    .grid-3 {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 18px;
      width: 100%;
    }

    .grid-4 {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 16px;
      width: 100%;
    }

    .grid-2x2 {
      display: grid;
      grid-template-columns: 1fr 1fr;
      grid-template-rows: 1fr 1fr;
      gap: 16px;
      width: 100%;
    }

    .split-col {
      flex: 1;
      display: flex;
      flex-direction: column;
      gap: 14px;
      min-width: 0;
    }

    /* IMAGE CONTAINERS */
    .media-card {
      background: rgba(26, 26, 46, 0.85);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 12px;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      position: relative;
      overflow: hidden;
    }

    .media-img {
      max-width: 100%;
      max-height: 85%;
      object-fit: contain;
      border-radius: 8px;
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
    }

    .media-caption {
      margin-top: 8px;
      font-size: 11px;
      color: var(--text-muted);
      text-align: center;
    }

    /* TABLES */
    .custom-table {
      width: 100%;
      border-collapse: collapse;
      font-size: 11.5px;
      margin-top: 6px;
    }

    .custom-table th {
      background: var(--navy-udeg);
      color: var(--cyan);
      text-align: left;
      padding: 8px 10px;
      font-size: 11px;
      font-weight: 700;
      border-bottom: 1px solid var(--border);
    }

    .custom-table td {
      padding: 7px 10px;
      border-bottom: 1px solid rgba(51, 65, 85, 0.4);
      color: var(--text-muted);
    }

    .custom-table tr:hover td {
      background: rgba(56, 189, 248, 0.05);
      color: var(--text-white);
    }

    .status-badge {
      display: inline-block;
      padding: 2px 6px;
      border-radius: 4px;
      font-size: 10px;
      font-weight: 700;
      background: rgba(74, 222, 128, 0.15);
      color: #4ADE80;
    }

    /* BIG STAT CARD */
    .stat-card {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      text-align: center;
      padding: 14px;
      border-radius: 10px;
      background: var(--bg-card-elev);
      border: 1px solid var(--border);
    }

    .stat-val {
      font-size: 28px;
      font-weight: 800;
      color: var(--cyan);
      line-height: 1.1;
      font-family: var(--font-main);
    }

    .stat-label {
      font-size: 11.5px;
      font-weight: 700;
      color: var(--text-white);
      margin-top: 4px;
    }

    .stat-sub {
      font-size: 10px;
      color: var(--text-muted);
      margin-top: 2px;
    }

    /* SPEAKER NOTES MODAL / HUD */
    .notes-modal {
      display: none;
      position: fixed;
      bottom: 20px;
      right: 20px;
      width: 480px;
      max-height: 520px;
      background: rgba(13, 27, 42, 0.96);
      backdrop-filter: blur(16px);
      border: 1px solid var(--cyan);
      border-radius: 14px;
      box-shadow: 0 20px 50px rgba(0, 0, 0, 0.8), 0 0 30px rgba(56, 189, 248, 0.2);
      z-index: 200;
      flex-direction: column;
      overflow: hidden;
      animation: slideUp 0.25s ease;
    }

    .notes-modal.show {
      display: flex;
    }

    @keyframes slideUp {
      from { transform: translateY(30px); opacity: 0; }
      to { transform: translateY(0); opacity: 1; }
    }

    .notes-header {
      padding: 12px 18px;
      background: var(--navy-udeg);
      display: flex;
      align-items: center;
      justify-content: space-between;
      border-bottom: 1px solid var(--border);
    }

    .notes-title {
      font-size: 13px;
      font-weight: 700;
      color: var(--cyan);
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .notes-close {
      background: none;
      border: none;
      color: var(--text-muted);
      font-size: 16px;
      cursor: pointer;
    }

    .notes-body {
      padding: 16px 18px;
      overflow-y: auto;
      font-size: 12.5px;
      line-height: 1.5;
      color: #E2E8F0;
      display: flex;
      flex-direction: column;
      gap: 12px;
    }

    .notes-section {
      border-left: 3px solid var(--cyan);
      padding-left: 10px;
    }

    .notes-section.goal { border-color: var(--green-bright); }
    .notes-section.script { border-color: var(--amber-bright); }
    .notes-section.cues { border-color: var(--cyan); }

    .notes-section-title {
      font-size: 11px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      margin-bottom: 4px;
    }

    .notes-section-title.goal { color: var(--green-bright); }
    .notes-section-title.script { color: var(--amber-bright); }
    .notes-section-title.cues { color: var(--cyan); }

    .notes-script-text {
      font-size: 13px;
      font-weight: 500;
      color: #F8FAFC;
      background: rgba(30, 41, 59, 0.5);
      padding: 10px 12px;
      border-radius: 8px;
      border: 1px solid rgba(51, 65, 85, 0.4);
    }

    /* FULLSCREEN HELPER */
    :fullscreen .stage-container {
      max-width: 100vw;
      height: 100vh;
      padding: 0;
      justify-content: center;
    }

    :fullscreen .slide-wrapper {
      max-width: 100vw;
      max-height: 100vh;
      border-radius: 0;
      border: none;
    }

    /* PRINT TO PDF */
    @media print {
      body {
        background: white;
        color: black;
      }
      .toolbar, .notes-modal {
        display: none !important;
      }
      .stage-container {
        padding: 0;
        max-width: 100%;
      }
      .slide-wrapper {
        border: none;
        box-shadow: none;
        border-radius: 0;
      }
      .slide {
        display: flex !important;
        page-break-after: always;
        height: 100vh;
        width: 100vw;
      }
    }
  </style>
</head>
<body>

  <!-- TOP TOOLBAR -->
  <header class="toolbar">
    <div class="toolbar-brand">
      <img src="brand/udeg_logo.png" alt="UdeG Logo" class="toolbar-logo" onerror="this.style.display='none'">
      <div class="toolbar-title">SIGRE • EXPODIT 2026</div>
    </div>

    <div class="toolbar-controls">
      <button class="btn" id="btn-prev" title="Diapositiva Anterior (←)">◀ Anterior</button>
      
      <select id="slide-select" class="btn" style="padding: 6px 10px; cursor: pointer;">
        <option value="0">1. Portada Institucional</option>
        <option value="1">2. Diagnóstico & Contexto Operativo</option>
        <option value="2">3. Alineación Estratégica ONU 2030</option>
        <option value="3">4. Alcance & Directrices Técnicas</option>
        <option value="4">5. Innovación Tecnológica</option>
        <option value="5">6. Diseño de Ingeniería de Software</option>
        <option value="6">7. Stack Tecnológico Seleccionado</option>
        <option value="7">8. Calidad & Pruebas de Humo</option>
        <option value="8">9. Operación en Ventanilla & UX</option>
        <option value="9">10. Gestión Directiva & Auditoría</option>
        <option value="10">11. Propuesta de Valor & Mercado</option>
        <option value="11">12. Evolución & Hoja de Ruta</option>
        <option value="12">13. Cierre Académico & Conclusiones</option>
      </select>

      <button class="btn" id="btn-next" title="Diapositiva Siguiente (→, Espacio)">Siguiente ▶</button>

      <!-- LIVE STOPWATCH -->
      <div class="timer-badge" id="timer-display" title="Cronómetro de Exposición (Meta: 3:00 - 5:00 min)">
        ⏱ 00:00
      </div>
      <button class="btn" id="btn-timer-toggle" title="Iniciar/Pausar Cronómetro (T)">▶ Play</button>
      <button class="btn" id="btn-timer-reset" title="Reiniciar Cronómetro">↺</button>

      <!-- MODALS & FULLSCREEN -->
      <button class="btn btn-primary" id="btn-notes" title="Ver Guion Oral de esta Lámina (N)">🎤 Guion (N)</button>
      <button class="btn" id="btn-fullscreen" title="Pantalla Completa (F)">⛶ Fullscreen (F)</button>
    </div>
  </header>

  <!-- STAGE CONTAINER -->
  <main class="stage-container" id="presentation-container">
    <div class="slide-wrapper">

      <!-- ========================================== -->
      <!-- SLIDE 1: PORTADA                           -->
      <!-- ========================================== -->
      <div class="slide active" data-slide="0">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 24px;">
          <img src="brand/udeg_logo.png" alt="UdeG" style="height: 64px;" onerror="this.style.display='none'">
          <div class="badge badge-cyan" style="font-size: 12px; padding: 6px 14px;">
            EXPODIT 2026 • PROYECTO INTEGRADOR DE DESARROLLO DE SOFTWARE
          </div>
          <img src="brand/sigre_logo_header.png" alt="SIGRE" style="height: 58px;" onerror="this.style.display='none'">
        </div>

        <div style="flex: 1; display: flex; flex-direction: column; justify-content: center; margin-bottom: 24px;">
          <h1 style="font-size: 46px; font-weight: 800; color: var(--text-white); letter-spacing: -0.5px; margin-bottom: 12px;">
            PLATAFORMA SIGRE
          </h1>
          <p style="font-size: 18px; color: var(--cyan); max-width: 90%; line-height: 1.4; font-weight: 500;">
            Sistema Integrado de Gestión de Recursos y Espacios: Control Patrimonial, Prevención de Colisiones de Agenda y Trazabilidad de Infraestructura Universitaria
          </p>
        </div>

        <div class="grid-4">
          <div class="card card-border-cyan">
            <span style="font-size: 10px; font-weight: 800; color: var(--amber-bright); text-transform: uppercase;">ESTUDIANTE / AUTOR</span>
            <strong style="font-size: 14px; margin-top: 4px; color: var(--text-white);">Ernesto Hatuey Fierro M.</strong>
            <span style="font-size: 11px; color: var(--text-muted); margin-top: 2px;">Código: 223977036 • Equipo 4</span>
          </div>

          <div class="card card-border-cyan">
            <span style="font-size: 10px; font-weight: 800; color: var(--amber-bright); text-transform: uppercase;">DOCENTE TITULAR</span>
            <strong style="font-size: 14px; margin-top: 4px; color: var(--text-white);">Dra. Abril Sherman</strong>
            <span style="font-size: 11px; color: var(--text-muted); margin-top: 2px;">Evaluación ExpoDIT 2026</span>
          </div>

          <div class="card card-border-cyan">
            <span style="font-size: 10px; font-weight: 800; color: var(--amber-bright); text-transform: uppercase;">CENTRO UNIVERSITARIO</span>
            <strong style="font-size: 14px; margin-top: 4px; color: var(--text-white);">CUTonalá (DIIT)</strong>
            <span style="font-size: 11px; color: var(--text-muted); margin-top: 2px;">Ing. en Ciencias Computacionales</span>
          </div>

          <div class="card card-border-cyan">
            <span style="font-size: 10px; font-weight: 800; color: var(--amber-bright); text-transform: uppercase;">COMPROMISO ONU 2030</span>
            <strong style="font-size: 14px; margin-top: 4px; color: var(--text-white);">ODS 4, 9, 11, 12 y 16</strong>
            <span style="font-size: 11px; color: var(--text-muted); margin-top: 2px;">Campus Inteligente y Cero Papel</span>
          </div>
        </div>

        <div class="slide-footer">
          <span class="slide-footer-left">Ernesto Hatuey Fierro M. (223977036) • Equipo 4</span>
          <span class="slide-footer-center">Docente: Dra. Abril Adriana Angulo Sherman</span>
          <span class="slide-footer-right">EXPODIT 2026 • Slide 1 / 13</span>
        </div>
      </div>

      <!-- ========================================== -->
      <!-- SLIDE 2: DIAGNÓSTICO & CONTEXTO OPERATIVO  -->
      <!-- ========================================== -->
      <div class="slide" data-slide="1">
        <div class="slide-header">
          <div class="slide-category">Diagnóstico & Contexto Operativo</div>
          <h2 class="slide-title">Problemática en la Gestión de Espacios y Activos Universitarios</h2>
          <p class="slide-subtitle">Brechas patrimoniales, logísticas y ecológicas detectadas en el modelo analógico tradicional</p>
          <img src="brand/udeg_logo.png" alt="UdeG" class="slide-corner-logo" onerror="this.style.display='none'">
        </div>

        <div class="slide-body">
          <div class="grid-3">
            <div class="card card-border-red">
              <div class="card-icon-title">
                <span class="card-icon">📉</span>
                <span class="card-title">Merma Patrimonial No Deslindada</span>
              </div>
              <p class="card-desc">El registro manual en libretas diluye la cadena de custodia cuando se devuelven cables o proyectores averiados sin checklist bilateral.</p>
              <div class="badge badge-red">Impacto: Pérdida $90k – $140k/año</div>
              <ul class="bullet-list">
                <li><strong>Firmas Ilegibles:</strong> Vales en papel sin checklist formal bilateral de entrega y recepción.</li>
                <li><strong>Extravío Continuo:</strong> 15 a 30 accesorios menores (HDMI/USB-C) perdidos al año por campus.</li>
                <li><strong>Fricción en Mostrador:</strong> Imposibilidad de deslindar responsabilidad entre alumno y laboratorista.</li>
              </ul>
            </div>

            <div class="card card-border-amber">
              <div class="card-icon-title">
                <span class="card-icon">⏰</span>
                <span class="card-title">Colisiones de Agenda y Empalmes</span>
              </div>
              <p class="card-desc">La tramitación mediante oficios y correos aislados genera traslapes concurrentes y salas cerradas sin llave disponible.</p>
              <div class="badge badge-amber">Impacto: 15 a 25 min de clase perdidos</div>
              <ul class="bullet-list">
                <li><strong>Burocracia de 5 Días:</strong> Trámites lentos que desembocan en 'acuerdos verbales de pasillo'.</li>
                <li><strong>Doble Agendamiento:</strong> Dos docentes asignados al mismo auditorio al mismo tiempo.</li>
                <li><strong>Parálisis Pedagógica:</strong> Pérdida recurrente de tiempo lectivo por falta de llave o equipo.</li>
              </ul>
            </div>

            <div class="card card-border-green">
              <div class="card-icon-title">
                <span class="card-icon">📄</span>
                <span class="card-title">Ceguera Directiva y Desperdicio</span>
              </div>
              <p class="card-desc">La administración carece de telemetría de uso real, programando compras por urgencia y acumulando miles de papeles muertos.</p>
              <div class="badge badge-green">Meta: Ahorro de >12,000 actas/año</div>
              <ul class="bullet-list">
                <li><strong>Despacho Lento:</strong> Tiempos de 4.5 a 6.0 minutos por persona en mostrador en horas pico.</li>
                <li><strong>Cero Analítica:</strong> Desconocimiento del ciclo de vida y horas de uso de activos.</li>
                <li><strong>Huella Papelera:</strong> Consumo masivo de tóner y hojas que terminan en archivo muerto.</li>
              </ul>
            </div>
          </div>
        </div>

        <div class="slide-footer">
          <span class="slide-footer-left">Ernesto Hatuey Fierro M. (223977036) • Equipo 4</span>
          <span class="slide-footer-center">Docente: Dra. Abril Adriana Angulo Sherman</span>
          <span class="slide-footer-right">EXPODIT 2026 • Slide 2 / 13</span>
        </div>
      </div>

      <!-- ========================================== -->
      <!-- SLIDE 3: ALINEACIÓN ESTRATÉGICA ONU 2030  -->
      <!-- ========================================== -->
      <div class="slide" data-slide="2">
        <div class="slide-header">
          <div class="slide-category">Alineación Estratégica ONU 2030</div>
          <h2 class="slide-title">Justificación e Impacto en los Objetivos de Desarrollo Sostenible</h2>
          <p class="slide-subtitle">SIGRE como catalizador de transformación digital, transparencia patrimonial y sostenibilidad universitaria</p>
          <img src="brand/udeg_logo.png" alt="UdeG" class="slide-corner-logo" onerror="this.style.display='none'">
        </div>

        <div class="slide-body">
          <div class="split-col">
            <div class="card card-border-cyan" style="padding: 14px 16px;">
              <div class="card-icon-title">
                <span class="card-icon">🎓</span>
                <span class="card-title" style="color: var(--cyan);">ODS 4: Educación de Calidad (Meta 4.a)</span>
              </div>
              <p class="card-desc" style="margin-bottom: 0;">Garantiza instalaciones académicas y recintos especializados equipados y disponibles al 100%, eliminando la pérdida de tiempo pedagógico por falta de proyectores o aulas cerradas.</p>
            </div>

            <div class="card card-border-amber" style="padding: 14px 16px;">
              <div class="card-icon-title">
                <span class="card-icon">☁</span>
                <span class="card-title" style="color: var(--amber-bright);">ODS 9 & 16: Innovación, Infraestructura y Paz</span>
              </div>
              <p class="card-desc" style="margin-bottom: 0;">Arquitectura cloud serverless elástica en GCP, cerrojos atómicos en Redis y auditoría criptográfica HMAC-SHA256 para total transparencia y rendición de cuentas institucional.</p>
            </div>

            <div class="card card-border-green" style="padding: 14px 16px;">
              <div class="card-icon-title">
                <span class="card-icon">🌿</span>
                <span class="card-title" style="color: var(--green-bright);">ODS 11 & 12: Comunidades Sostenibles y Cero Papel</span>
              </div>
              <p class="card-desc" style="margin-bottom: 0;">Digitalización del 100% de actas responsivas en PDF oficial con firma digital, sustituyendo más de 12,000 formatos impresos al año por plantel universitario.</p>
            </div>
          </div>

          <div class="split-col">
            <div class="media-card" style="height: 100%;">
              <img src="graficos/figura1_diagrama_servicio_sigre.png" alt="Figura 1: Matriz de Servicio y Sostenibilidad" class="media-img" style="max-height: 85%;">
              <div class="media-caption">Figura 1: Matriz Gráfica de Métricas e Indicadores de Impacto Sostenible (Agenda ONU 2030)</div>
            </div>
          </div>
        </div>

        <div class="slide-footer">
          <span class="slide-footer-left">Ernesto Hatuey Fierro M. (223977036) • Equipo 4</span>
          <span class="slide-footer-center">Docente: Dra. Abril Adriana Angulo Sherman</span>
          <span class="slide-footer-right">EXPODIT 2026 • Slide 3 / 13</span>
        </div>
      </div>

      <!-- ========================================== -->
      <!-- SLIDE 4: ALCANCE & DIRECTRICES TÉCNICAS    -->
      <!-- ========================================== -->
      <div class="slide" data-slide="3">
        <div class="slide-header">
          <div class="slide-category">Alcance & Directrices Técnicas</div>
          <h2 class="slide-title">Objetivos del Proyecto SIGRE</h2>
          <p class="slide-subtitle">Metas de desarrollo formal de software para la gestión patrimonial y logística de recintos</p>
          <img src="brand/udeg_logo.png" alt="UdeG" class="slide-corner-logo" onerror="this.style.display='none'">
        </div>

        <div class="slide-body" style="flex-direction: column; gap: 14px;">
          <!-- Objetivo General -->
          <div class="card card-border-cyan" style="padding: 14px 18px;">
            <strong style="color: var(--cyan); font-size: 13px; margin-bottom: 4px; display: block;">🎯 Objetivo General de Ingeniería</strong>
            <p style="font-size: 12px; color: var(--text-white); line-height: 1.45;">
              Diseñar, construir e implementar una plataforma web distribuida para la administración, reserva y trazabilidad de espacios y bienes móviles en CUTonalá, garantizando transacciones concurrentes libres de empalmes mediante cerrojos en Redis, autenticación federada UdeG, actas responsivas con firma digitalizada HMAC-SHA256 y un ecosistema de reputación Trust Score alineado a la Agenda 2030.
            </p>
          </div>

          <!-- 4 Métricas de Éxito -->
          <div class="grid-4">
            <div class="stat-card" style="border-color: rgba(56, 189, 248, 0.4);">
              <div class="stat-val">&lt; 30 seg</div>
              <div class="stat-label">Tiempo de Despacho</div>
              <div class="stat-sub">En ventanilla con escáner QR</div>
            </div>

            <div class="stat-card" style="border-color: rgba(74, 222, 128, 0.4);">
              <div class="stat-val" style="color: var(--green-bright);">0</div>
              <div class="stat-label">Empalmes de Agenda</div>
              <div class="stat-sub">Con Redis Distributed Lock</div>
            </div>

            <div class="stat-card" style="border-color: rgba(251, 191, 36, 0.4);">
              <div class="stat-val" style="color: var(--amber-bright);">82.85 pts</div>
              <div class="stat-label">Usabilidad SUS (n=50)</div>
              <div class="stat-sub">Grado A Nivel Excelente</div>
            </div>

            <div class="stat-card" style="border-color: rgba(56, 189, 248, 0.4);">
              <div class="stat-val">99.9%</div>
              <div class="stat-label">Disponibilidad Cloud</div>
              <div class="stat-sub">En Google Cloud Run (GCP)</div>
            </div>
          </div>

          <!-- Objetivos Específicos -->
          <div class="card" style="padding: 14px 18px;">
            <strong style="color: var(--amber-bright); font-size: 12.5px; margin-bottom: 6px; display: block;">⚙ Objetivos Específicos de Ingeniería de Software</strong>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px;">
              <div style="font-size: 11px; color: var(--text-muted);"><strong style="color: var(--text-white);">1. Concurrencia y Aislamiento:</strong> Cerrojos temporales (TTL 900s) en Redis 7.</div>
              <div style="font-size: 11px; color: var(--text-muted);"><strong style="color: var(--text-white);">2. Cadena de Custodia:</strong> Escaneo QR WebRTC y firma Canvas HMAC-SHA256.</div>
              <div style="font-size: 11px; color: var(--text-muted);"><strong style="color: var(--text-white);">3. Autenticación Exclusiva:</strong> Google OAuth 2.0 restringido a dominios @udg.mx.</div>
              <div style="font-size: 11px; color: var(--text-muted);"><strong style="color: var(--text-white);">4. Telemetría y Reputación:</strong> RBAC de 5 roles y Trust Score base 100 para auditoría.</div>
              <div style="font-size: 11px; color: var(--text-muted); grid-column: span 2;"><strong style="color: var(--text-white);">5. Despliegue Elástico y DevOps:</strong> Pipeline CI/CD en GitHub Actions y contenedores Docker serverless en Cloud Run.</div>
            </div>
          </div>
        </div>

        <div class="slide-footer">
          <span class="slide-footer-left">Ernesto Hatuey Fierro M. (223977036) • Equipo 4</span>
          <span class="slide-footer-center">Docente: Dra. Abril Adriana Angulo Sherman</span>
          <span class="slide-footer-right">EXPODIT 2026 • Slide 4 / 13</span>
        </div>
      </div>

      <!-- ========================================== -->
      <!-- SLIDE 5: INNOVACIÓN TECNOLÓGICA            -->
      <!-- ========================================== -->
      <div class="slide" data-slide="4">
        <div class="slide-header">
          <div class="slide-category">Innovación Tecnológica & Valor Diferencial</div>
          <h2 class="slide-title">Solución Propuesta: Las Genialidades del Proyecto SIGRE</h2>
          <p class="slide-subtitle">¿Por qué SIGRE redefine la administración de infraestructura y patrimonio en educación superior?</p>
          <img src="brand/udeg_logo.png" alt="UdeG" class="slide-corner-logo" onerror="this.style.display='none'">
        </div>

        <div class="slide-body">
          <div class="grid-4">
            <div class="card card-border-cyan" style="display: flex; flex-direction: column; justify-content: space-between;">
              <div>
                <div class="card-icon-title">
                  <span class="card-icon">⚡</span>
                  <span class="card-title">1. Concurrencia Redis Locks</span>
                </div>
                <p class="card-desc" style="font-size: 11px; line-height: 1.45;">Pre-reserva atómica con SET NX EX 900 (15 min): bloquea temporalmente el espacio mientras el solicitante formaliza datos y co-responsables. Si abandona, el cerrojo expira solo; si confirma, persiste en PostgreSQL sin colisión.</p>
              </div>
              <div class="badge badge-cyan" style="margin-top: 10px;">▶ Garantía: Cero Empalmes<br><span style="font-size: 10px; font-weight: normal; color: var(--text-muted);">Aislamiento transaccional estricto</span></div>
            </div>

            <div class="card card-border-green" style="display: flex; flex-direction: column; justify-content: space-between;">
              <div>
                <div class="card-icon-title">
                  <span class="card-icon">📱</span>
                  <span class="card-title">2. Despacho Óptico QR</span>
                </div>
                <p class="card-desc" style="font-size: 11px; line-height: 1.45;">Lectura de códigos QR dinámicos directamente desde la cámara del navegador web vía WebRTC, sin lectores propietarios. Firma táctil digitalizada sellada en actas PDF inmutables con HMAC-SHA256.</p>
              </div>
              <div class="badge badge-green" style="margin-top: 10px;">▶ Agilidad: &lt; 30 Segundos<br><span style="font-size: 10px; font-weight: normal; color: var(--text-muted);">Reducción de 5 min a 30 seg en entrega</span></div>
            </div>

            <div class="card card-border-amber" style="display: flex; flex-direction: column; justify-content: space-between;">
              <div>
                <div class="card-icon-title">
                  <span class="card-icon">🛡</span>
                  <span class="card-title">3. Algoritmo Trust Score</span>
                </div>
                <p class="card-desc" style="font-size: 11px; line-height: 1.45;">Calificación algorítmica de reputación de usuario (base 100): premia devoluciones a tiempo y penaliza demoras o mermas, bloqueando temporalmente a morosos. Permite adherir co-responsables solidarios.</p>
              </div>
              <div class="badge badge-amber" style="margin-top: 10px;">▶ Protección Patrimonial<br><span style="font-size: 10px; font-weight: normal; color: var(--text-muted);">Fomenta corresponsabilidad</span></div>
            </div>

            <div class="card card-border-cyan" style="display: flex; flex-direction: column; justify-content: space-between;">
              <div>
                <div class="card-icon-title">
                  <span class="card-icon">☁</span>
                  <span class="card-title">4. Serverless Cloud Run</span>
                </div>
                <p class="card-desc" style="font-size: 11px; line-height: 1.45;">Backend en contenedores Docker desplegados sobre GCP con escalado elástico de 0 a N instancias. En vacaciones el costo es cero. Además, la PWA incorpora caché local para operar ante caídas de red del campus.</p>
              </div>
              <div class="badge badge-cyan" style="margin-top: 10px;">▶ Escalabilidad Elástica<br><span style="font-size: 10px; font-weight: normal; color: var(--text-muted);">Disponibilidad 99.9% y costo optimizado</span></div>
            </div>
          </div>
        </div>

        <div class="slide-footer">
          <span class="slide-footer-left">Ernesto Hatuey Fierro M. (223977036) • Equipo 4</span>
          <span class="slide-footer-center">Docente: Dra. Abril Adriana Angulo Sherman</span>
          <span class="slide-footer-right">EXPODIT 2026 • Slide 5 / 13</span>
        </div>
      </div>

      <!-- ========================================== -->
      <!-- SLIDE 6: DISEÑO DE INGENIERÍA DE SOFTWARE  -->
      <!-- ========================================== -->
      <div class="slide" data-slide="5">
        <div class="slide-header">
          <div class="slide-category">Diseño de Ingeniería de Software</div>
          <h2 class="slide-title">Arquitectura y Diagrama del Sistema SIGRE</h2>
          <p class="slide-subtitle">Estructura desacoplada en 5 capas de software en Monorepo Turborepo con cerrojos distribuidos</p>
          <img src="brand/udeg_logo.png" alt="UdeG" class="slide-corner-logo" onerror="this.style.display='none'">
        </div>

        <div class="slide-body">
          <div class="split-col">
            <div class="media-card" style="height: 100%;">
              <img src="graficos/figura2_diagrama_arquitectura_5capas_sigre.png" alt="Figura 2: Arquitectura 5 Capas SIGRE" class="media-img" style="max-height: 88%;">
              <div class="media-caption">Figura 2: Diagrama de 5 Capas de Software SIGRE (Monorepo Turborepo)</div>
            </div>
          </div>

          <div class="split-col" style="justify-content: space-between;">
            <div class="card card-border-cyan" style="padding: 10px 14px;">
              <strong style="color: var(--cyan); font-size: 12px;">Capa 1: Interfaz Reactiva (React 18 / Vite)</strong>
              <p style="font-size: 11px; color: var(--text-muted); margin-top: 2px;">PWA responsiva para tablets de ventanilla y móviles. 18 vistas modulares organizadas por rol, diseño UdeG Outfit y firma en Canvas.</p>
            </div>

            <div class="card card-border-green" style="padding: 10px 14px;">
              <strong style="color: var(--green-bright); font-size: 12px;">Capa 2: API Gateway & Core (Express / TypeScript)</strong>
              <p style="font-size: 11px; color: var(--text-muted); margin-top: 2px;">Rutas REST (/api/v1), middleware JWT con roles RBAC (Alumno, Docente, Almacén, SuperAdmin), validación Zod y sanitización OWASP.</p>
            </div>

            <div class="card card-border-amber" style="padding: 10px 14px;">
              <strong style="color: var(--amber-bright); font-size: 12px;">Capa 3: Bus de Concurrencia (Redis 7 Locks)</strong>
              <p style="font-size: 11px; color: var(--text-muted); margin-top: 2px;">Cerrojos atómicos SET NX EX 900 (TTL 15 min) para bloqueo de slots de agenda, blacklist de tokens revocados y caché de catálogos.</p>
            </div>

            <div class="card card-border-cyan" style="padding: 10px 14px;">
              <strong style="color: var(--cyan); font-size: 12px;">Capa 4: Persistencia Relacional (PostgreSQL 16)</strong>
              <p style="font-size: 11px; color: var(--text-muted); margin-top: 2px;">Esquema relacional ACID con Prisma ORM y tipos tsrange para exclusión estricta de solapamientos temporales en reservas y activos.</p>
            </div>

            <div class="card card-border-green" style="padding: 10px 14px;">
              <strong style="color: var(--green-bright); font-size: 12px;">Capa 5: Infraestructura Cloud (Google Cloud Run)</strong>
              <p style="font-size: 11px; color: var(--text-muted); margin-top: 2px;">Contenedores Docker serverless con escalado elástico a cero en GCP, integración con Google Identity OAuth 2.0 y servidor SMTP.</p>
            </div>
          </div>
        </div>

        <div class="slide-footer">
          <span class="slide-footer-left">Ernesto Hatuey Fierro M. (223977036) • Equipo 4</span>
          <span class="slide-footer-center">Docente: Dra. Abril Adriana Angulo Sherman</span>
          <span class="slide-footer-right">EXPODIT 2026 • Slide 6 / 13</span>
        </div>
      </div>

      <!-- ========================================== -->
      <!-- SLIDE 7: ECOSISTEMA & HERRAMIENTAS         -->
      <!-- ========================================== -->
      <div class="slide" data-slide="6">
        <div class="slide-header">
          <div class="slide-category">Ecosistema & Herramientas de Desarrollo</div>
          <h2 class="slide-title">Stack Tecnológico Seleccionado</h2>
          <p class="slide-subtitle">Tecnologías modernas, probadas en producción e interoperables</p>
          <img src="brand/udeg_logo.png" alt="UdeG" class="slide-corner-logo" onerror="this.style.display='none'">
        </div>

        <div class="slide-body">
          <div class="grid-4">
            <div class="card card-border-cyan">
              <div class="card-icon-title">
                <span class="card-icon">🎨</span>
                <div>
                  <div class="card-title" style="color: var(--cyan);">Frontend & UI</div>
                  <div style="font-size: 10px; color: var(--text-white); font-weight: 600;">UX Diseñado para Mostrador</div>
                </div>
              </div>
              <ul class="bullet-list" style="margin-top: 8px;">
                <li><strong>React 18 & Vite:</strong> Carga instantánea y hot reload para terminales táctiles.</li>
                <li><strong>TypeScript:</strong> Tipado estático estricto en inventario y formularios.</li>
                <li><strong>Tailwind CSS:</strong> Design System oficial UdeG (#002B49 / Outfit).</li>
                <li><strong>Canvas & WebRTC:</strong> Firma táctil digital y lector QR por cámara.</li>
              </ul>
            </div>

            <div class="card card-border-green">
              <div class="card-icon-title">
                <span class="card-icon">⚙</span>
                <div>
                  <div class="card-title" style="color: var(--green-bright);">Backend & Datos</div>
                  <div style="font-size: 10px; color: var(--text-white); font-weight: 600;">Microservicios & Concurrencia</div>
                </div>
              </div>
              <ul class="bullet-list" style="margin-top: 8px;">
                <li><strong>Node.js & Express:</strong> API REST modular en monorepo Turborepo.</li>
                <li><strong>PostgreSQL 16:</strong> RDBMS ACID con exclusión GiST de solapes tsrange.</li>
                <li><strong>Prisma ORM:</strong> Consultas SQL tipadas y migraciones reproducibles.</li>
                <li><strong>Redis 7 In-Memory:</strong> Cerrojos atómicos distribuidos anti-empalme.</li>
              </ul>
            </div>

            <div class="card card-border-amber">
              <div class="card-icon-title">
                <span class="card-icon">🛡</span>
                <div>
                  <div class="card-title" style="color: var(--amber-bright);">Seguridad & Auth</div>
                  <div style="font-size: 10px; color: var(--text-white); font-weight: 600;">Cumplimiento Institucional</div>
                </div>
              </div>
              <ul class="bullet-list" style="margin-top: 8px;">
                <li><strong>Google OAuth 2.0:</strong> Restricción a dominios @udg.mx y @alumnos.</li>
                <li><strong>JWT RS256:</strong> Tokens de 15m con refresh tokens de 7 días.</li>
                <li><strong>HMAC-SHA256:</strong> Sellado criptográfico de actas PDF foliadas.</li>
                <li><strong>Zod & Helmet:</strong> Validación de esquema y cabeceras OWASP.</li>
              </ul>
            </div>

            <div class="card card-border-cyan">
              <div class="card-icon-title">
                <span class="card-icon">🚀</span>
                <div>
                  <div class="card-title" style="color: var(--cyan);">DevOps & Cloud</div>
                  <div style="font-size: 10px; color: var(--text-white); font-weight: 600;">Infraestructura Resiliente</div>
                </div>
              </div>
              <ul class="bullet-list" style="margin-top: 8px;">
                <li><strong>GCP Cloud Run:</strong> Contenedores serverless con autoescalado a 0.</li>
                <li><strong>Docker Multi-Stage:</strong> Imágenes de producción livianas (&lt;150MB).</li>
                <li><strong>Turborepo & pnpm:</strong> Compilación incremental y caché unificado.</li>
                <li><strong>GitHub Actions:</strong> Pipeline CI/CD con pruebas de integración E2E.</li>
              </ul>
            </div>
          </div>
        </div>

        <div class="slide-footer">
          <span class="slide-footer-left">Ernesto Hatuey Fierro M. (223977036) • Equipo 4</span>
          <span class="slide-footer-center">Docente: Dra. Abril Adriana Angulo Sherman</span>
          <span class="slide-footer-right">EXPODIT 2026 • Slide 7 / 13</span>
        </div>
      </div>

      <!-- ========================================== -->
      <!-- SLIDE 8: ASEGURAMIENTO DE CALIDAD          -->
      <!-- ========================================== -->
      <div class="slide" data-slide="7">
        <div class="slide-header">
          <div class="slide-category">Aseguramiento de Calidad de Software</div>
          <h2 class="slide-title">Módulo de Seguridad, Pruebas de Humo y Autenticación UdeG</h2>
          <p class="slide-subtitle">Validación formal de casos de prueba según formato institucional de laboratorio</p>
          <img src="brand/udeg_logo.png" alt="UdeG" class="slide-corner-logo" onerror="this.style.display='none'">
        </div>

        <div class="slide-body">
          <div class="split-col">
            <div class="media-card" style="height: 100%;">
              <img src="pruebas/screenshots/01_identidad_institucional.png" alt="Figura 3: Acceso Seguro UdeG" class="media-img" style="max-height: 85%;">
              <div class="media-caption">Figura 3: Interfaz de Acceso Institucional SIGRE con Google Workspace UdeG</div>
            </div>
          </div>

          <div class="split-col">
            <div class="card card-border-cyan" style="padding: 14px 18px;">
              <strong style="color: var(--cyan); font-size: 13px; margin-bottom: 6px; display: block;">Matriz de Casos de Prueba (Smoke Testing Automatizado)</strong>
              <table class="custom-table">
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>Escenario Evaluado</th>
                    <th>Salida Esperada</th>
                    <th>Resultado</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td><strong>CP-01</strong></td>
                    <td>Admin/Alumno con @udg.mx válido</td>
                    <td>Redirección a dashboard según rol</td>
                    <td><span class="status-badge">EXITOSO</span></td>
                  </tr>
                  <tr>
                    <td><strong>CP-02</strong></td>
                    <td>Cuenta externa personal (@gmail.com)</td>
                    <td>Bloqueo HTTP 403 ('Solo UdeG')</td>
                    <td><span class="status-badge">EXITOSO</span></td>
                  </tr>
                  <tr>
                    <td><strong>CP-03</strong></td>
                    <td>Reserva simultánea mismo bloque</td>
                    <td>Lock Redis 201 / Bloqueo 409 Conflict</td>
                    <td><span class="status-badge">EXITOSO</span></td>
                  </tr>
                  <tr>
                    <td><strong>CP-04</strong></td>
                    <td>Alumno intentando ruta /admin/config</td>
                    <td>Denegación RBAC 403 sin fuga datos</td>
                    <td><span class="status-badge">EXITOSO</span></td>
                  </tr>
                </tbody>
              </table>
            </div>

            <div class="card card-elevated" style="padding: 14px 18px;">
              <strong style="color: var(--amber-bright); font-size: 12px; margin-bottom: 4px; display: block;">🛡 Mecanismo de Autorización RBAC Institucional</strong>
              <p style="font-size: 11px; color: var(--text-muted); line-height: 1.45;">
                El token JWT contiene claims de rol inmutables. El middleware verifica autorizaciones en memoria en cada request, impidiendo escalamiento horizontal o vertical de privilegios entre estamentos universitarios.
              </p>
            </div>
          </div>
        </div>

        <div class="slide-footer">
          <span class="slide-footer-left">Ernesto Hatuey Fierro M. (223977036) • Equipo 4</span>
          <span class="slide-footer-center">Docente: Dra. Abril Adriana Angulo Sherman</span>
          <span class="slide-footer-right">EXPODIT 2026 • Slide 8 / 13</span>
        </div>
      </div>

      <!-- ========================================== -->
      <!-- SLIDE 9: OPERACIÓN EN VENTANILLA           -->
      <!-- ========================================== -->
      <div class="slide" data-slide="8">
        <div class="slide-header">
          <div class="slide-category">Operación en Ventanilla & Experiencia de Usuario</div>
          <h2 class="slide-title">Módulo de Ventanilla Ágil, Escaneo QR y Firma Digital</h2>
          <p class="slide-subtitle">Despacho de equipo en menos de 30 segundos con acta responsiva oficial y checklist bilateral</p>
          <img src="brand/udeg_logo.png" alt="UdeG" class="slide-corner-logo" onerror="this.style.display='none'">
        </div>

        <div class="slide-body">
          <div class="split-col">
            <div class="media-card" style="height: 100%;">
              <img src="pruebas/screenshots/09_escaner_qr_camara.png" alt="Figura 4: Escaneo QR Ventanilla" class="media-img" style="max-height: 85%;">
              <div class="media-caption">Figura 4: Despacho de Ventanilla con Escáner QR WebRTC y Validación Óptica</div>
            </div>
          </div>

          <div class="split-col" style="justify-content: space-between;">
            <div class="card card-border-cyan" style="padding: 14px 18px;">
              <div class="card-icon-title">
                <span class="card-icon">⚡</span>
                <span class="card-title" style="color: var(--cyan);">Despacho Óptico Express en 3 Pasos</span>
              </div>
              <ul class="bullet-list">
                <li><strong>1. Presentación QR:</strong> El usuario muestra su código dinámico desde la app web o boleto PDF.</li>
                <li><strong>2. Lectura Inmediata:</strong> La cámara web del navegador decodifica el token en menos de 2 segundos.</li>
                <li><strong>3. Validación y Asignación:</strong> El sistema muestra el número de serie físico exacto para entrega.</li>
              </ul>
            </div>

            <div class="card card-border-green" style="padding: 14px 18px;">
              <div class="card-icon-title">
                <span class="card-icon">📝</span>
                <span class="card-title" style="color: var(--green-bright);">Checklist Bilateral y Acta Digital HMAC-SHA256</span>
              </div>
              <ul class="bullet-list">
                <li><strong>Inspección Física Rápida:</strong> Marcado bilateral de puertos, cables y accesorios.</li>
                <li><strong>Firma Digitalizada en Canvas:</strong> Trazo manuscrito en pantalla táctil con sellado UTC.</li>
                <li><strong>Acta Inmutable PDF:</strong> Generación con hash HMAC-SHA256 enviado por correo al custodio.</li>
                <li><strong>Cadena de Custodia:</strong> Deslinde patrimonial automático ante auditorías universitarias.</li>
              </ul>
            </div>
          </div>
        </div>

        <div class="slide-footer">
          <span class="slide-footer-left">Ernesto Hatuey Fierro M. (223977036) • Equipo 4</span>
          <span class="slide-footer-center">Docente: Dra. Abril Adriana Angulo Sherman</span>
          <span class="slide-footer-right">EXPODIT 2026 • Slide 9 / 13</span>
        </div>
      </div>

      <!-- ========================================== -->
      <!-- SLIDE 10: GESTIÓN DIRECTIVA & AUDITORÍA   -->
      <!-- ========================================== -->
      <div class="slide" data-slide="9">
        <div class="slide-header">
          <div class="slide-category">Gestión Directiva & Auditoría Patrimonial</div>
          <h2 class="slide-title">Panel Ejecutivo, Telemetría de Espacios y Auditoría Patrimonial</h2>
          <p class="slide-subtitle">Control centralizado de inventario activo, métricas de ocupación y bitácora criptográfica para la administración</p>
          <img src="brand/udeg_logo.png" alt="UdeG" class="slide-corner-logo" onerror="this.style.display='none'">
        </div>

        <div class="slide-body">
          <div class="split-col">
            <div class="media-card" style="height: 100%;">
              <img src="pruebas/screenshots/08_dashboard_ejecutivo.png" alt="Figura 5: Dashboard Ejecutivo" class="media-img" style="max-height: 85%;">
              <div class="media-caption">Figura 5: Tablero Administrativo con Telemetría de Espacios y Métricas de Ocupación</div>
            </div>
          </div>

          <div class="split-col" style="justify-content: space-between;">
            <div class="card card-border-cyan" style="padding: 12px 16px;">
              <strong style="color: var(--cyan); font-size: 13px; display: block; margin-bottom: 2px;">📦 Control y Trazabilidad de Inventario por Serie</strong>
              <p style="font-size: 11.5px; color: var(--text-muted); line-height: 1.4;">Monitoreo en tiempo real del ciclo de vida de cada activo (en estante, en uso, mantenimiento o baja), vinculando cada préstamo a su acta digital foliada.</p>
            </div>

            <div class="card card-border-green" style="padding: 12px 16px;">
              <strong style="color: var(--green-bright); font-size: 13px; display: block; margin-bottom: 2px;">📊 Telemetría y Aprovechamiento de Aulas y Auditorios</strong>
              <p style="font-size: 11.5px; color: var(--text-muted); line-height: 1.4;">Analítica de horas de uso por edificio, tasa de ocupación pico y reportes ejecutivos exportables para planeación de compras y presupuestos.</p>
            </div>

            <div class="card card-border-amber" style="padding: 12px 16px;">
              <strong style="color: var(--amber-bright); font-size: 13px; display: block; margin-bottom: 2px;">🛡 Gestión de Incidencias y Algoritmo Trust Score</strong>
              <p style="font-size: 11.5px; color: var(--text-muted); line-height: 1.4;">Deslinde de averías con evidencia fotográfica obligatoria. El Trust Score premia el cuidado de equipo y bloquea solicitudes a usuarios con adeudos activos.</p>
            </div>
          </div>
        </div>

        <div class="slide-footer">
          <span class="slide-footer-left">Ernesto Hatuey Fierro M. (223977036) • Equipo 4</span>
          <span class="slide-footer-center">Docente: Dra. Abril Adriana Angulo Sherman</span>
          <span class="slide-footer-right">EXPODIT 2026 • Slide 10 / 13</span>
        </div>
      </div>

      <!-- ========================================== -->
      <!-- SLIDE 11: PROPUESTA DE VALOR & MERCADO     -->
      <!-- ========================================== -->
      <div class="slide" data-slide="10">
        <div class="slide-header">
          <div class="slide-category">Propuesta de Valor & Mercado</div>
          <h2 class="slide-title">Ventajas Competitivas de la Plataforma SIGRE</h2>
          <p class="slide-subtitle">Comparativa técnica frente a libretas analógicas, sistemas centrales rígidos y software comercial extranjero</p>
          <img src="brand/udeg_logo.png" alt="UdeG" class="slide-corner-logo" onerror="this.style.display='none'">
        </div>

        <div class="slide-body">
          <div class="grid-4">
            <div class="card card-border-cyan">
              <div class="card-icon-title">
                <span class="card-icon">⚡</span>
                <span class="card-title" style="color: var(--cyan);">Agilidad en Ventanilla</span>
              </div>
              <p class="card-desc">Despacho en mostrador en menos de 30 segundos mediante escaneo QR WebRTC y firma en canvas.</p>
              <div class="badge badge-cyan">Reduce 90% tiempo en fila</div>
              <ul class="bullet-list">
                <li>Operación táctil ultrarrápida.</li>
                <li>Sin pistolas lectoras propietarias.</li>
                <li>Atención ágil en cambio de turno.</li>
              </ul>
            </div>

            <div class="card card-border-green">
              <div class="card-icon-title">
                <span class="card-icon">🔒</span>
                <span class="card-title" style="color: var(--green-bright);">Cero Empalmes con Redis</span>
              </div>
              <p class="card-desc">Certeza transaccional absoluta en reservas de auditorios y laboratorios especializados.</p>
              <div class="badge badge-green">Cerrojos TTL 15 min</div>
              <ul class="bullet-list">
                <li>Aislamiento concurrente atómico.</li>
                <li>Expiración automática por abandono.</li>
                <li>Integración con PostgreSQL tsrange.</li>
              </ul>
            </div>

            <div class="card card-border-amber">
              <div class="card-icon-title">
                <span class="card-icon">💰</span>
                <span class="card-title" style="color: var(--amber-bright);">Ahorro Comprobado y ROI</span>
              </div>
              <p class="card-desc">Sustituye mermas históricas de $115k/año por un ahorro neto estimado de $80,500 MXN.</p>
              <div class="badge badge-amber">TIR 24.27% • Payback M29.4</div>
              <ul class="bullet-list">
                <li>Suscripción 60% menor a ERPs.</li>
                <li>Retorno inversión en mes 31.2.</li>
                <li>Ahorro en reposición de activos.</li>
              </ul>
            </div>

            <div class="card card-border-cyan">
              <div class="card-icon-title">
                <span class="card-icon">📜</span>
                <span class="card-title" style="color: var(--cyan);">Validez Jurídica y Cero Papel</span>
              </div>
              <p class="card-desc">Acta responsiva foliada en PDF con firma Canvas y hash HMAC-SHA256 conforme a la LGPDPPSO.</p>
              <div class="badge badge-cyan">Ahorro >12,000 actas/año</div>
              <ul class="bullet-list">
                <li>Alineación con política Cero Papel.</li>
                <li>Respaldo legal ante Contraloría.</li>
                <li>Soporte local en sitio y WhatsApp.</li>
              </ul>
            </div>
          </div>
        </div>

        <div class="slide-footer">
          <span class="slide-footer-left">Ernesto Hatuey Fierro M. (223977036) • Equipo 4</span>
          <span class="slide-footer-center">Docente: Dra. Abril Adriana Angulo Sherman</span>
          <span class="slide-footer-right">EXPODIT 2026 • Slide 11 / 13</span>
        </div>
      </div>

      <!-- ========================================== -->
      <!-- SLIDE 12: EVOLUCIÓN & ESCALABILIDAD        -->
      <!-- ========================================== -->
      <div class="slide" data-slide="11">
        <div class="slide-header">
          <div class="slide-category">Evolución & Escalabilidad</div>
          <h2 class="slide-title">Recomendaciones & Hoja de Ruta Tecnológica</h2>
          <p class="slide-subtitle">Estrategia de escalamiento comercial y evolución técnica a corto y mediano plazo (Años 1 a 5)</p>
          <img src="brand/udeg_logo.png" alt="UdeG" class="slide-corner-logo" onerror="this.style.display='none'">
        </div>

        <div class="slide-body">
          <div class="grid-2x2">
            <div class="card card-border-cyan">
              <div class="card-icon-title">
                <span class="card-icon">📱</span>
                <span class="card-title" style="color: var(--cyan);">1. Credencial Universitaria Digital NFC / Wallet</span>
              </div>
              <p class="card-desc">Integración con tarjetas de identificación institucional mediante chips NFC en teléfonos móviles, permitiendo check-in presencial en mostrador y registro de acceso sin contacto físico.</p>
              <div class="badge badge-cyan">Interoperabilidad Móvil</div>
            </div>

            <div class="card card-border-green">
              <div class="card-icon-title">
                <span class="card-icon">🚪</span>
                <span class="card-title" style="color: var(--green-bright);">2. Cerraduras Inteligentes IoT para Aulas y Recintos</span>
              </div>
              <p class="card-desc">Conexión de electroimanes y chapas inteligentes vía microcontroladores ESP32 y protocolo MQTT, habilitando la apertura automática de puertas cuando el usuario presenta su QR o reserva activa.</p>
              <div class="badge badge-green">Automatización Física</div>
            </div>

            <div class="card card-border-amber">
              <div class="card-icon-title">
                <span class="card-icon">🤖</span>
                <span class="card-title" style="color: var(--amber-bright);">3. Modelos Predictivos de Demanda y Mantenimiento (IA / ML)</span>
              </div>
              <p class="card-desc">Entrenamiento de modelos de series temporales en BigQuery ML para pronosticar picos de saturación en auditorios y calendarizar mantenimientos preventivos a proyectores según horas de lámpara.</p>
              <div class="badge badge-amber">Inteligencia Artificial</div>
            </div>

            <div class="card card-border-cyan">
              <div class="card-icon-title">
                <span class="card-icon">🌐</span>
                <span class="card-title" style="color: var(--cyan);">4. Expansión Multisede a Tecnológicos y UPES Estatales</span>
              </div>
              <p class="card-desc">Habilitación de arquitectura multi-tenant completa para desplegar SIGRE en los Institutos Tecnológicos de Jalisco (UTJ, ITSZ) y las más de 60 Universidades Públicas Estatales de México.</p>
              <div class="badge badge-cyan">Escala Nacional B2G</div>
            </div>
          </div>
        </div>

        <div class="slide-footer">
          <span class="slide-footer-left">Ernesto Hatuey Fierro M. (223977036) • Equipo 4</span>
          <span class="slide-footer-center">Docente: Dra. Abril Adriana Angulo Sherman</span>
          <span class="slide-footer-right">EXPODIT 2026 • Slide 12 / 13</span>
        </div>
      </div>

      <!-- ========================================== -->
      <!-- SLIDE 13: CIERRE ACADÉMICO & RESULTADOS    -->
      <!-- ========================================== -->
      <div class="slide" data-slide="12">
        <div class="slide-header">
          <div class="slide-category">Cierre Académico & Resultados</div>
          <h2 class="slide-title">Conclusiones del Proyecto Integrador SIGRE</h2>
          <p class="slide-subtitle">Validación integral de competencias de ingeniería, rigor financiero e impacto institucional en ExpoDIT 2026</p>
          <img src="brand/udeg_logo.png" alt="UdeG" class="slide-corner-logo" onerror="this.style.display='none'">
        </div>

        <div class="slide-body">
          <div class="split-col">
            <div class="media-card" style="height: 100%;">
              <img src="pruebas/screenshots/10_distribucion_puntajes_sus.png" alt="Figura 6: Resultados SUS" class="media-img" style="max-height: 85%;">
              <div class="media-caption">Figura 6: Resultados Empíricos de Usabilidad SUS (Media 82.85 pts, Grado A Excelente, n=50)</div>
            </div>
          </div>

          <div class="split-col" style="justify-content: space-between;">
            <div class="card card-border-cyan" style="padding: 14px 18px;">
              <strong style="color: var(--cyan); font-size: 13px; display: block; margin-bottom: 4px;">1. Solución Tecnológica Integral y Validada en Campo</strong>
              <p style="font-size: 11.5px; color: var(--text-muted); line-height: 1.45;">Se cumplió el 100% de los requerimientos técnicos: transaccionalidad atómica en Redis, firma digital Canvas HMAC, control RBAC y una usabilidad empírica sobresaliente de <strong style="color: var(--text-white);">82.85 puntos en la escala SUS (n=50)</strong>.</p>
            </div>

            <div class="card card-border-green" style="padding: 14px 18px;">
              <strong style="color: var(--green-bright); font-size: 13px; display: block; margin-bottom: 4px;">2. Viabilidad Económica y Sustentabilidad Comprobada</strong>
              <p style="font-size: 11.5px; color: var(--text-muted); line-height: 1.45;">Evaluación financiera rigurosa: CAPEX de $180,000 MXN, VPN de <strong style="color: var(--text-white);">+$46,984.47 MXN</strong> (TMAR 15%), TIR del <strong style="color: var(--text-white);">24.27% anual</strong>, Payback en el <strong style="color: var(--text-white);">Mes 29.4</strong> y ahorro de <strong style="color: var(--text-white);">+$80,500 MXN/año</strong> en mermas evitables.</p>
            </div>

            <div class="card card-border-amber" style="padding: 14px 18px;">
              <strong style="color: var(--amber-bright); font-size: 13px; display: block; margin-bottom: 4px;">3. Madurez de Ingeniería en ExpoDIT 2026</strong>
              <p style="font-size: 11.5px; color: var(--text-muted); line-height: 1.45;">La integración de patrones de software formales, despliegue cloud en GCP y cumplimiento de la Agenda ONU 2030 ('Cero Papel') demuestran la solidez formativa adquirida en el Centro Universitario de Tonalá.</p>
            </div>
          </div>
        </div>

        <div class="slide-footer">
          <span class="slide-footer-left">Ernesto Hatuey Fierro M. (223977036) • Equipo 4</span>
          <span class="slide-footer-center">Docente: Dra. Abril Adriana Angulo Sherman</span>
          <span class="slide-footer-right">EXPODIT 2026 • Slide 13 / 13</span>
        </div>
      </div>

    </div>
  </main>

  <!-- SPEAKER NOTES MODAL / HUD -->
  <aside class="notes-modal" id="notes-modal">
    <div class="notes-header">
      <div class="notes-title">
        <span>🎤 Guion Oral & Notas de Presentador</span>
        <span id="notes-slide-badge" class="badge badge-cyan" style="margin-bottom: 0;">Slide 1 / 13</span>
      </div>
      <button class="notes-close" id="btn-notes-close" title="Cerrar modal (Esc o N)">✕</button>
    </div>

    <div class="notes-body">
      <div class="notes-section">
        <div class="notes-section-title" id="notes-timing-title">⏱ TIEMPO: 00:00 - 00:18 (18 seg)</div>
      </div>

      <div class="notes-section goal">
        <div class="notes-section-title goal">🎯 OBJETIVO EN EL PITCH:</div>
        <div id="notes-goal-text">Apertura formal institucional y presentación de identidad</div>
      </div>

      <div class="notes-section script">
        <div class="notes-section-title script">📢 TEXTO LITERAL A DECIR:</div>
        <div class="notes-script-text" id="notes-script-text">
          "Buenos días, Dra. Abril Sherman y miembros del jurado evaluador..."
        </div>
      </div>

      <div class="notes-section cues">
        <div class="notes-section-title cues">💡 CUES Y LENGUAJE CORPORAL:</div>
        <div id="notes-cues-text" style="color: var(--text-muted); font-size: 12px;">
          Postura erguida, contacto visual sostenido, proyectar voz firme y pausada.
        </div>
      </div>
    </div>
  </aside>

  <!-- JAVASCRIPT LOGIC -->
  <script>
    // Speech script data for each slide
    const SLIDES_NOTES = [
      {
        timing: "00:00 - 00:18 (18 seg)",
        goal: "Apertura formal con investidura institucional, captar atención del jurado y delimitar el problema.",
        script: "Buenos días, Dra. Abril Sherman y miembros del jurado evaluador. Mi nombre es Ernesto Hatuey Fierro, estudiante de Ingeniería en Ciencias Computacionales en CUTonalá. Hoy presento la Plataforma SIGRE: Sistema Integrado de Gestión de Recursos y Espacios, una solución de software orientada a erradicar colisiones de agenda y proteger el patrimonio universitario.",
        cues: "Postura erguida, mirada directa al jurado. Enfatizar 'Plataforma SIGRE' y 'erradicar colisiones'. Clic a Slide 2 al segundo 18."
      },
      {
        timing: "00:18 - 00:38 (20 seg)",
        goal: "Demostrar dolor operativo crónico en almacenes y cuantificar el impacto negativo del modelo analógico.",
        script: "En los almacenes del campus detectamos tres puntos críticos del registro en libretas: mermas no deslindadas de hasta 140,000 pesos anuales en accesorios y proyectores; colisiones de agenda que demoran hasta 25 minutos de clase lectiva; y ceguera directiva por falta de métricas sobre el uso del inventario.",
        cues: "Gesto con mano abierta señalando las 3 columnas. Modulación grave al decir '140,000 pesos anuales' y '25 minutos'."
      },
      {
        timing: "00:38 - 00:58 (20 seg)",
        goal: "Vincular el software con política universitaria, responsabilidad social y ODS de la Agenda ONU 2030.",
        script: "SIGRE se alinea a la Agenda 2030 de la ONU: fortalece el ODS 4 garantizando aulas equipadas; cumple los ODS 9 y 16 con arquitectura en la nube y auditoría criptográfica; y avanza en los ODS 11 y 12 digitalizando más de 12,000 actas físicas al año bajo la política Cero Papel.",
        cues: "Voz inspiradora. Resaltar la política 'Cero Papel' y el dato de 'más de 12,000 actas al año'. Apuntar a la gráfica lateral."
      },
      {
        timing: "00:58 - 01:18 (20 seg)",
        goal: "Presentar el objetivo general y las 4 métricas cuantitativas clave de ingeniería.",
        script: "Nuestra meta fue construir una plataforma distribuida y transaccional. Fijamos cuatro métricas clave: reducir el despacho en ventanilla a menos de 30 segundos; eliminar al 100% los empalmes con cerrojos atómicos; alcanzar una usabilidad SUS de excelencia con 82.85 puntos; y sostener 99.9% de disponibilidad en Google Cloud.",
        cues: "Ritmo ágil y seguro. Marcar con los dedos las 4 tarjetas numéricas (<30s, 0, 82.85, 99.9%). Enfatizar el 82.85 de Usabilidad SUS."
      },
      {
        timing: "01:18 - 01:40 (22 seg)",
        goal: "Explicar las genialidades técnicas y la resolución de problemas de concurrencia y seguridad.",
        script: "SIGRE aporta cuatro ventajas de ingeniería: cerrojos distribuidos en Redis con TTL de 15 minutos que bloquean empalmes concurrentes; despacho ágil con QR dinámico y firma en canvas; un algoritmo Trust Score que incentiva devoluciones puntuales; y contenedores serverless en Cloud Run que escalan a costo cero.",
        cues: "Tono de rigor computacional. Pausa breve de 1 segundo tras 'bloquean empalmes concurrentes'. Enfatizar el soft-lock de Redis."
      },
      {
        timing: "01:40 - 01:58 (18 seg)",
        goal: "Presentar la arquitectura desacoplada en 5 capas y el monorepo Turborepo.",
        script: "El sistema opera en un Monorepo Turborepo con 5 capas desacopladas: interfaz reactiva en React 18 y Vite; API Gateway en Express y TypeScript con Zod; concurrencia en Redis 7; persistencia relacional en PostgreSQL 16 con Prisma ORM y tsrange; e infraestructura elástica en Google Cloud Platform.",
        cues: "Guiar la mirada del jurado hacia el diagrama de 5 capas en pantalla. Mencionar los tipos tsrange para validación temporal."
      },
      {
        timing: "01:58 - 02:16 (18 seg)",
        goal: "Validar la madurez del stack tecnológico y el cumplimiento de estándares de la industria.",
        script: "Seleccionamos herramientas probadas en producción: Tailwind CSS con la paleta oficial UdeG y fuente Outfit; PostgreSQL con transacciones ACID; seguridad OWASP Top 10 con OAuth federado @udg.mx y sellos HMAC-SHA256; y entrega continua mediante GitHub Actions con pruebas de integración automatizadas.",
        cues: "Gesto recorriendo con la vista los 4 cuadrantes. Voz firme que denote dominio completo de las dependencias."
      },
      {
        timing: "02:16 - 02:32 (16 seg)",
        goal: "Mostrar evidencia de pruebas formales de humo y blindaje de seguridad institucional por roles (RBAC).",
        script: "Validamos formalmente el sistema con pruebas de humo. El flujo de acceso institucional restringe el login exclusivamente a correos UdeG, denegando cuentas personales con HTTP 403, mientras que nuestro control de acceso RBAC blinda las rutas contables y directivas frente a cualquier escalamiento no autorizado.",
        cues: "Señalar la tabla de casos de prueba CP-01 a CP-04 con 100% exitoso y la captura de pantalla de acceso seguro."
      },
      {
        timing: "02:32 - 02:50 (18 seg)",
        goal: "Demostrar cómo se vive la experiencia real en mostrador y cómo se elimina la fricción operativa.",
        script: "En mostrador, el despacho toma menos de 30 segundos. El almacenista lee el QR desde la cámara del navegador web mediante WebRTC sin lectores costosos. El alumno firma en la pantalla táctil y el sistema genera de inmediato un acta foliada en PDF con firma HMAC-SHA256 enviada por correo.",
        cues: "Voz dinámica. Destacar que 'no requiere pistolas lectoras propietarias', corriendo en cualquier tablet con cámara web."
      },
      {
        timing: "02:50 - 03:08 (18 seg)",
        goal: "Ilustrar el valor directivo para la Secretaría Administrativa y la Contraloría en rendición de cuentas.",
        script: "El panel administrativo provee telemetría en tiempo real: monitorea la ocupación de auditorios y laboratorios, audita la cadena de custodia por número de serie, y clasifica incidencias fotográficas asociadas al Trust Score del usuario para transparentar la rendición de cuentas ante la administración.",
        cues: "Tono institucional. Apuntar al gráfico del dashboard ejecutivo. Enfatizar 'cadena de custodia por número de serie'."
      },
      {
        timing: "03:08 - 03:26 (18 seg)",
        goal: "Demostrar viabilidad comercial, ahorro financiero comprobado y superioridad frente a ERPs genéricos.",
        script: "Frente a libretas y software comercial genérico, SIGRE destaca por su velocidad de entrega, cero empalmes de horario y un ahorro neto proyectado de 80,500 pesos anuales por plantel en mermas evitables, a una tarifa de suscripción hasta 60% menor y con soporte local especializado.",
        cues: "Tono persuasivo. Contrastar el ahorro de $80,500 pesos frente a la suscripción anual ($24k a $48k MXN)."
      },
      {
        timing: "03:26 - 03:44 (18 seg)",
        goal: "Presentar la hoja de ruta estratégica y visión de escalamiento a nivel estatal y nacional.",
        script: "Nuestra hoja de ruta contempla cuatro etapas de crecimiento: integración de credencial digital NFC en móviles; cerraduras electrónicas IoT para aulas magnas; modelos de IA en BigQuery para mantenimiento predictivo de proyectores; y escalamiento multisede a Tecnológicos y Universidades Públicas Estatales.",
        cues: "Voz entusiasta. Mostrar que el proyecto tiene un plan de vida sólido a 5 años y tecnología emergente (IoT, IA)."
      },
      {
        timing: "03:44 - 04:04 (20 seg)",
        goal: "Cierre triunfal, confirmación del perfil de egreso, rigor financiero comprobado y agradecimiento.",
        script: "Concluimos que SIGRE valida plenamente las competencias de ingeniería de ExpoDIT 2026: un software probado con 82.85 puntos SUS, financieramente viable con VPN de 46,984 pesos y Payback en el mes 29.4, y con impacto social y ambiental para la comunidad. Muchas gracias.",
        cues: "Mirada firme al jurado, sonrisa formal, bajar levemente el tono para dar solemnidad y concluir con un 'Muchas gracias'."
      }
    ];

    // Presentation State
    let currentSlide = 0;
    const slides = document.querySelectorAll('.slide');
    const totalSlides = slides.length;
    const selectElem = document.getElementById('slide-select');
    const notesModal = document.getElementById('notes-modal');

    function showSlide(index) {
      if (index < 0) index = 0;
      if (index >= totalSlides) index = totalSlides - 1;
      currentSlide = index;

      slides.forEach((s, idx) => {
        s.classList.toggle('active', idx === currentSlide);
      });

      selectElem.value = currentSlide;
      updateNotesView();
    }

    function updateNotesView() {
      const data = SLIDES_NOTES[currentSlide];
      document.getElementById('notes-slide-badge').innerText = `Slide ${currentSlide + 1} / ${totalSlides}`;
      document.getElementById('notes-timing-title').innerText = `⏱ TIEMPO ESTIMADO: ${data.timing}`;
      document.getElementById('notes-goal-text').innerText = data.goal;
      document.getElementById('notes-script-text').innerText = `"${data.script}"`;
      document.getElementById('notes-cues-text').innerText = data.cues;
    }

    // Navigation Events
    document.getElementById('btn-prev').addEventListener('click', () => showSlide(currentSlide - 1));
    document.getElementById('btn-next').addEventListener('click', () => showSlide(currentSlide + 1));
    selectElem.addEventListener('change', (e) => showSlide(parseInt(e.target.value)));

    // Keyboard Shortcuts
    window.addEventListener('keydown', (e) => {
      if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'PageDown') {
        e.preventDefault();
        showSlide(currentSlide + 1);
      } else if (e.key === 'ArrowLeft' || e.key === 'PageUp') {
        e.preventDefault();
        showSlide(currentSlide - 1);
      } else if (e.key === 'f' || e.key === 'F') {
        toggleFullscreen();
      } else if (e.key === 'n' || e.key === 'N') {
        toggleNotes();
      } else if (e.key === 't' || e.key === 'T') {
        toggleTimer();
      } else if (e.key === 'Escape') {
        notesModal.classList.remove('show');
      }
    });

    // Notes Toggle
    function toggleNotes() {
      notesModal.classList.toggle('show');
      document.getElementById('btn-notes').classList.toggle('btn-active');
      updateNotesView();
    }
    document.getElementById('btn-notes').addEventListener('click', toggleNotes);
    document.getElementById('btn-notes-close').addEventListener('click', () => notesModal.classList.remove('show'));

    // Fullscreen Toggle
    function toggleFullscreen() {
      const container = document.getElementById('presentation-container');
      if (!document.fullscreenElement) {
        if (container.requestFullscreen) {
          container.requestFullscreen();
        } else if (container.webkitRequestFullscreen) {
          container.webkitRequestFullscreen();
        }
      } else {
        if (document.exitFullscreen) {
          document.exitFullscreen();
        }
      }
    }
    document.getElementById('btn-fullscreen').addEventListener('click', toggleFullscreen);

    // Live Presentation Timer
    let timerSeconds = 0;
    let timerInterval = null;
    let isTimerRunning = false;
    const timerElem = document.getElementById('timer-display');
    const timerToggleBtn = document.getElementById('btn-timer-toggle');

    function formatTime(sec) {
      const m = Math.floor(sec / 60).toString().padStart(2, '0');
      const s = (sec % 60).toString().padStart(2, '0');
      return `${m}:${s}`;
    }

    function updateTimerDisplay() {
      timerElem.innerText = `⏱ ${formatTime(timerSeconds)}`;
      if (timerSeconds < 210) { // < 3:30 min (ideal)
        timerElem.className = 'timer-badge';
      } else if (timerSeconds < 270) { // 3:30 - 4:30 min (target)
        timerElem.className = 'timer-badge warning';
      } else { // > 4:30 min (limit)
        timerElem.className = 'timer-badge danger';
      }
    }

    function toggleTimer() {
      if (isTimerRunning) {
        clearInterval(timerInterval);
        isTimerRunning = false;
        timerToggleBtn.innerText = '▶ Reanudar';
        timerToggleBtn.classList.remove('btn-active');
      } else {
        isTimerRunning = true;
        timerToggleBtn.innerText = '⏸ Pausa';
        timerToggleBtn.classList.add('btn-active');
        timerInterval = setInterval(() => {
          timerSeconds++;
          updateTimerDisplay();
        }, 1000);
      }
    }

    function resetTimer() {
      clearInterval(timerInterval);
      isTimerRunning = false;
      timerSeconds = 0;
      updateTimerDisplay();
      timerToggleBtn.innerText = '▶ Iniciar';
      timerToggleBtn.classList.remove('btn-active');
    }

    document.getElementById('btn-timer-toggle').addEventListener('click', toggleTimer);
    document.getElementById('btn-timer-reset').addEventListener('click', resetTimer);

    // Initial Load
    showSlide(0);
  </script>
</body>
</html>
"""

    with open('docs/Presentacion_ExpoDIT_SIGRE.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    print("Generated docs/Presentacion_ExpoDIT_SIGRE.html successfully")

if __name__ == '__main__':
    generate_html_presentation()
