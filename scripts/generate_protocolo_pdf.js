const fs = require('fs');
const path = require('path');
const { marked } = require('marked');
const { chromium } = require('@playwright/test');

// Helper to encode image to base64
function getBase64Image(filePath) {
  if (!fs.existsSync(filePath)) {
    console.warn(`File not found: ${filePath}`);
    return '';
  }
  const ext = path.extname(filePath).replace('.', '').toLowerCase();
  const mime = ext === 'png' ? 'image/png' : ext === 'jpg' || ext === 'jpeg' ? 'image/jpeg' : 'image/webp';
  const data = fs.readFileSync(filePath).toString('base64');
  return `data:${mime};base64,${data}`;
}

async function buildProtocoloPDF() {
  const mdPath = path.resolve(__dirname, '../docs/protocolo_investigacion_sigre.md');
  const outHtmlPath = path.resolve(__dirname, '../docs/2026B_Equipo4_Protocolo.html');
  const outPdfPath = path.resolve(__dirname, '../docs/2026B_Equipo4_Protocolo.pdf');

  console.log('Reading markdown from:', mdPath);
  let md = fs.readFileSync(mdPath, 'utf8');

  // Load images
  const logoBase64 = getBase64Image(path.resolve(__dirname, '../docs/brand/udeg_logo.png'));
  const fig1Base64 = getBase64Image(path.resolve(__dirname, '../docs/graficos/figura1_diagrama_servicio_sigre.png'));
  const fig2Base64 = getBase64Image(path.resolve(__dirname, '../docs/graficos/figura2_grafico_pareto_criterios_costo.png'));
  const fig3Base64 = getBase64Image(path.resolve(__dirname, '../docs/graficos/figura3_curva_economias_escala_punto_equilibrio.png'));

  const ss01 = getBase64Image(path.resolve(__dirname, '../docs/pruebas/screenshots/01_identidad_institucional.png'));
  const ss02 = getBase64Image(path.resolve(__dirname, '../docs/pruebas/screenshots/02_sesion_alumno.png'));
  const ss03 = getBase64Image(path.resolve(__dirname, '../docs/pruebas/screenshots/03_boleto_qr_cineteca.png'));
  const ss04a = getBase64Image(path.resolve(__dirname, '../docs/pruebas/screenshots/04_reserva_confirmada.png'));
  const ss04b = getBase64Image(path.resolve(__dirname, '../docs/pruebas/screenshots/04_soft_lock_redis.png'));
  const ss05a = getBase64Image(path.resolve(__dirname, '../docs/pruebas/screenshots/05_prestamo_creado.png'));
  const ss05b = getBase64Image(path.resolve(__dirname, '../docs/pruebas/screenshots/05_canvas_firma_digital.png'));
  const ss06 = getBase64Image(path.resolve(__dirname, '../docs/pruebas/screenshots/06_solicitudes_responsivas.png'));
  const ss07 = getBase64Image(path.resolve(__dirname, '../docs/pruebas/screenshots/07_incidentes_trust_score.png'));
  const ss08 = getBase64Image(path.resolve(__dirname, '../docs/pruebas/screenshots/08_dashboard_ejecutivo.png'));
  const ss09 = getBase64Image(path.resolve(__dirname, '../docs/pruebas/screenshots/09_escaner_qr_camara.png'));
  const ssForms1 = getBase64Image(path.resolve(__dirname, '../docs/pruebas/screenshots/11_google_forms_resumen_respuestas.png'));
  const ssForms2 = getBase64Image(path.resolve(__dirname, '../docs/pruebas/screenshots/12_google_forms_desglose_reactivos.png'));
  const ssSusChart = getBase64Image(path.resolve(__dirname, '../docs/pruebas/screenshots/10_distribucion_puntajes_sus.png'));

  // Replace text figures in Section 7 with formatted HTML figures
  const fig1Replacement = `
<div class="figure-block">
  <div class="figure-num">Figura 1</div>
  <div class="figure-title">Diagrama de flujo del servicio SIGRE y puntos de control operativo</div>
  <img src="${fig1Base64}" alt="Figura 1: Flujo de servicio SIGRE" class="fig-img" />
  <div class="figure-note"><em>Nota.</em> Diagnóstico del circuito operativo y puntos de control en almacenes de CUTonalá.</div>
</div>
`;
  const fig2Replacement = `
<div class="figure-block">
  <div class="figure-num">Figura 2</div>
  <div class="figure-title">Diagrama de Pareto: Causas y Costos Estimados de Merma Patrimonial Anual</div>
  <img src="${fig2Base64}" alt="Figura 2: Diagrama de Pareto de mermas" class="fig-img" />
  <div class="figure-note"><em>Nota.</em> Estimación basada en histórico de almacenes de CUTonalá ($140,000 MXN base anual). El 82.5% de pérdidas se concentra en proyectores, adaptadores y cables HDMI. Eje dual con escala monetaria (izquierda) y porcentaje acumulado (derecha).</div>
</div>
`;
  const fig3Replacement = `
<div class="figure-block">
  <div class="figure-num">Figura 3</div>
  <div class="figure-title">Evaluación Financiera: Curva de Payback y Ahorro Acumulado</div>
  <img src="${fig3Base64}" alt="Figura 3: Curva de punto de equilibrio" class="fig-img" />
  <div class="figure-note"><em>Nota.</em> Amortización de inversión inicial ($140,000 MXN). Punto de equilibrio en Mes 19.5 para modelo local CUTonalá (flujo neto $86,200 MXN/año) y en Mes 29.6 para corrida trienal de red (Payback simple Mes 29.6 / Mes 34.0 descontado, con superávit acumulado de +$106,000 MXN al Año 3).</div>
</div>
`;

  md = md.replace(/- \*\*Figura 1:[\s\S]*?(?=- \*\*Figura 2:)/, fig1Replacement);
  md = md.replace(/- \*\*Figura 2:[\s\S]*?(?=- \*\*Figura 3:)/, fig2Replacement);
  md = md.replace(/- \*\*Figura 3:[\s\S]*?(?=### 7\.1\.7)/, fig3Replacement);

  const fig3aHtml = `
<div class="figure-block">
  <div class="figure-num">Figura 3a</div>
  <div class="figure-title">Consola de Respuestas de Google Forms y Distribución Demográfica por Estamento (n = 50)</div>
  <img src="${ssForms1}" alt="Figura 3a: Consola de Respuestas Google Forms" class="fig-img" />
  <div class="figure-note"><em>Nota.</em> Registro directo de la consola de resultados de Google Forms vinculada al dominio institucional UdeG: desglose de la muestra evaluada (64% estudiantes, 24% docentes, 12% operadores de almacén) y gráficos de frecuencia para los reactivos iniciales R1 y R2.</div>
</div>
`;
  const fig3bHtml = `
<div class="figure-block">
  <div class="figure-num">Figura 3b</div>
  <div class="figure-title">Frecuencia de Respuestas por Reactivo en Escala Likert de Google Forms (Reactivos SUS)</div>
  <img src="${ssForms2}" alt="Figura 3b: Gráficas de Frecuencia Google Forms" class="fig-img" />
  <div class="figure-note"><em>Nota.</em> Distribución de frecuencias observadas en escala Likert (1 a 5) generadas automáticamente por la plataforma para los reactivos R3 a R10 del instrumento SUS.</div>
</div>
`;
  const fig3cHtml = `
<div class="figure-block">
  <div class="figure-num">Figura 3c</div>
  <div class="figure-title">Evaluación Psicométrica y Puntuación Compuesta SUS (Verificación de Hipótesis HE-3)</div>
  <img src="${ssSusChart}" alt="Figura 3c: Distribución de Puntajes SUS" class="fig-img" />
  <div class="figure-note"><em>Nota.</em> Comparativa de puntuaciones medias por estamento: Estudiantes (83.28 pts), Docentes (81.25 pts), Operadores de Almacén (83.75 pts) y promedio global de 82.85 puntos (s = 10.91 pts, t(49) = 1.848, p = 0.035, LI_95% = 80.26 pts), confirmando la superación del umbral meta de 80 puntos fijado en la hipótesis HE-3 y del promedio industrial de usabilidad (68 puntos).</div>
</div>
`;

  md = md.replace(/### Figura 3a:[\s\S]*?(?=### Figura 3b:)/, fig3aHtml);
  md = md.replace(/### Figura 3b:[\s\S]*?(?=### Figura 3c:)/, fig3bHtml);
  md = md.replace(/### Figura 3c:[\s\S]*?(?=\*\*Interpretación de Resultados)/, fig3cHtml);

  // Replace Evidencias 1 to 10 in Section 9.4
  const ev1Html = `
<div class="figure-block">
  <div class="figure-num">Figura 4</div>
  <div class="figure-title">Evidencia 1: Identidad Institucional y Pantalla de Autenticación Centralizada</div>
  <img src="${ss01}" alt="Evidencia 1: Login Institucional" class="fig-img" />
  <div class="figure-note"><em>Nota.</em> Captura real de la suite Playwright ejecutada sobre https://sigre-web-84991608726.us-central1.run.app</div>
</div>
`;
  const ev2Html = `
<div class="figure-block">
  <div class="figure-num">Figura 5</div>
  <div class="figure-title">Evidencia 2: Portal del Solicitante con Catálogo de Recursos y Trust Score</div>
  <img src="${ss02}" alt="Evidencia 2: Sesión Alumno" class="fig-img" />
  <div class="figure-note"><em>Nota.</em> Captura de interfaz preliminar de desarrollo obtenida por el arquitecto del software en su estación local de trabajo (cuenta de desarrollo 215789456) previo a la estandarización final de la suite E2E de Playwright sobre la cuenta genérica EST-2026B-01. El Trust Score se muestra en 100 puntos y el catálogo en tiempo real, diferenciándose estrictamente de los datos de la evaluación SUS de la Sección 7.1.8.</div>
</div>
`;
  const ev3Html = `
<div class="figure-block">
  <div class="figure-num">Figura 6</div>
  <div class="figure-title">Evidencia 3: Boleto QR Dinámico con Firma Criptográfica HMAC-SHA256 (Cineteca)</div>
  <img src="${ss03}" alt="Evidencia 3: Boleto QR Cineteca" class="fig-img" />
  <div class="figure-note"><em>Nota.</em> Entrada digital generada en el entorno de desarrollo mediante la suite de pruebas automatizadas, incorporando sello temporal UTC y firma criptográfica HMAC-SHA256 para validación anti-falsificación en taquilla.</div>
</div>
`;
  const ev4Html = `
<div class="figure-block">
  <div class="figure-num">Figura 7</div>
  <div class="figure-title">Evidencia 4: Confirmación de Reserva y Adquisición de Cerrojo Distribuido (Soft-Lock en Redis)</div>
  <div class="two-img-grid">
    <img src="${ss04a}" alt="Evidencia 4a: Reserva Confirmada" class="fig-img-half" />
    <img src="${ss04b}" alt="Evidencia 4b: Soft Lock Redis" class="fig-img-half" />
  </div>
  <div class="figure-note"><em>Nota.</em> Exclusión mutua atómica con TTL de 15 minutos en Redis 7. Prevención de colisiones concurrentes comprobada en pruebas de laboratorio; impacto operativo sujeto a validación en prueba piloto.</div>
</div>
`;
  const ev5Html = `
<div class="figure-block">
  <div class="figure-num">Figura 8</div>
  <div class="figure-title">Evidencia 5: Solicitud Formal de Préstamo y Canvas de Firma Electrónica Simple</div>
  <div class="two-img-grid">
    <img src="${ss05a}" alt="Evidencia 5a: Préstamo Creado" class="fig-img-half" />
    <img src="${ss05b}" alt="Evidencia 5b: Canvas Firma" class="fig-img-half" />
  </div>
  <div class="figure-note"><em>Nota.</em> Captura del trazo manuscrito en HTML5 Canvas con sellado de tiempo UTC e incrustación en el acta responsiva en Base64.</div>
</div>
`;
  const ev6Html = `
<div class="figure-block">
  <div class="figure-num">Figura 9</div>
  <div class="figure-title">Evidencia 6: Bandeja de Solicitudes y Emisión Automatizada de Responsiva Oficial en PDF</div>
  <img src="${ss06}" alt="Evidencia 6: Solicitudes y Responsivas" class="fig-img" />
  <div class="figure-note"><em>Nota.</em> Generación de actas de entrega-recepción en PDF con registro de conformidad digital y trazabilidad administrativa para Servicios Generales.</div>
</div>
`;
  const ev7Html = `
<div class="figure-block">
  <div class="figure-num">Figura 10</div>
  <div class="figure-title">Evidencia 7: Módulo de Registro de Incidencias Patrimoniales y Ajuste de Trust Score</div>
  <img src="${ss07}" alt="Evidencia 7: Incidentes y Trust Score" class="fig-img" />
  <div class="figure-note"><em>Nota.</em> Módulo de incidencias ejecutado en el entorno de pruebas alfa de desarrollo. Despliega el folio simulado INC-2026-0003 (etiquetado transitoriamente como INC-2826-0003 en la vista preliminar previo al parche de normalización) y deducciones según gravedad. El puntaje permanece en 100/100 debido a su estatus condicional hasta la ratificación formal de Servicios Generales.</div>
</div>
`;
  const ev8Html = `
<div class="figure-block">
  <div class="figure-num">Figura 11</div>
  <div class="figure-title">Evidencia 8: Dashboard Ejecutivo de Inversión y Métricas Patrimoniales en Tiempo Real</div>
  <img src="${ss08}" alt="Evidencia 8: Dashboard Ejecutivo" class="fig-img" />
  <div class="figure-note"><em>Nota.</em> Monitoreo de KPIs de ocupación por edificio, horas de proyector y corrida trienal de amortización (Payback simple Mes 29.6 / Mes 33.8 descontado, TIR 21.34%, TMAR 15.0% y superávit de +$106,000 MXN al Año 3; B/C 1.15x netos / 1.07x convencional).</div>
</div>
`;
  const ev9Html = `
<div class="figure-block">
  <div class="figure-num">Figura 12</div>
  <div class="figure-title">Evidencia 9: Escáner Óptico de Acceso en Vivo con Cámara WebRTC</div>
  <img src="${ss09}" alt="Evidencia 9: Escáner QR Cámara" class="fig-img" />
  <div class="figure-note"><em>Nota.</em> Módulo de lectura óptica de códigos QR desde la cámara del navegador (API WebRTC) ejecutado en la pestaña de 'Pruebas & Simulación' del entorno de desarrollo para la función de Macario (1960), con telemetría en cliente (performance.now()) que verifica decodificación de boletos en mostrador en menos de 500 ms.</div>
</div>
`;
  md = md.replace(/### Evidencia 1:[\s\S]*?(?=### Evidencia 2:)/, ev1Html);
  md = md.replace(/### Evidencia 2:[\s\S]*?(?=### Evidencia 3:)/, ev2Html);
  md = md.replace(/### Evidencia 3:[\s\S]*?(?=### Evidencia 4:)/, ev3Html);
  md = md.replace(/### Evidencia 4:[\s\S]*?(?=### Evidencia 5:)/, ev4Html);
  md = md.replace(/### Evidencia 5:[\s\S]*?(?=### Evidencia 6:)/, ev5Html);
  md = md.replace(/### Evidencia 6:[\s\S]*?(?=### Evidencia 7:)/, ev6Html);
  md = md.replace(/### Evidencia 7:[\s\S]*?(?=### Evidencia 8:)/, ev7Html);
  md = md.replace(/### Evidencia 8:[\s\S]*?(?=### Evidencia 9:)/, ev8Html);
  md = md.replace(/### Evidencia 9:[\s\S]*?(?=## 9\.5)/, ev9Html);

  // Split out cover markdown part (first ~15 lines)
  let cleanMarkdown = md.replace(/# Protocolo de Investigación: Plataforma SIGRE[\s\S]*?---/, '');
  // Strip horizontal rules before headings to prevent empty pages
  cleanMarkdown = cleanMarkdown.replace(/\n\s*---\s*\n(?=\s*#)/g, '\n');

  // Transform block equations $$...$$ into clean semantic HTML
  cleanMarkdown = cleanMarkdown.replace(/\$\$t'\s*=\s*\\frac\{\\bar\{x\}_1\s*-\s*\\bar\{x\}_2\}\{\\sqrt\{\\frac\{s_1\^2\}\{n_1\}\s*\+\s*\\frac\{s_2\^2\}\{n_2\}\}\}\$\$/g,
    '<div class="math-block"><em>t</em> \' = (<em>x̄</em>₁ − <em>x̄</em>₂) / √(<em>s</em>₁²/<em>n</em>₁ + <em>s</em>₂²/<em>n</em>₂)</div>');

  cleanMarkdown = cleanMarkdown.replace(/\$+\\alpha\s*=\s*\\frac\{10\}\{9\}\s*\\left\(1\s*-\s*\\frac\{3\.7555\}\{19\.0208\}\\right\)\s*=\s*0\.892\$+/g,
    '<em>α</em> = (10/9) × [ 1 − (3.7555 / 19.0208) ] = <strong>0.892</strong>');

  cleanMarkdown = cleanMarkdown.replace(/\$\$LI_\{95\\%\}\s*=\s*\\bar\{x\}\s*-\s*t_\{0\.05,\s*49\}\s*\\cdot\s*\\frac\{s\}\{\\sqrt\{n\}\}\s*=\s*82\.85\s*-\s*\(1\.677\s*\\times\s*1\.543\)\s*=\s*80\.26\s*\\text\{\s*pts\}\$\$/g,
    '<div class="math-block"><em>LI</em><sub>95%</sub> = <em>x̄</em> − <em>t</em><sub>0.05, 49</sub> · (<em>s</em> / √<em>n</em>) = 82.85 − (1.677 × 1.543) = <strong>80.26 pts</strong></div>');

  cleanMarkdown = cleanMarkdown.replace(/\$\$t\(49\)\s*=\s*\\frac\{82\.85\s*-\s*80\.00\}\{10\.91\s*\/\s*\\sqrt\{50\}\}\s*=\s*\\frac\{2\.85\}\{1\.543\}\s*=\s*1\.848,\s*\\quad\s*p\s*=\s*0\.035\s*<\s*0\.05\$\$/g,
    '<div class="math-block"><em>t</em>(49) = (82.85 − 80.00) / (10.91 / √50) = 2.85 / 1.543 = <strong>1.848</strong>, &nbsp;&nbsp; <em>p</em> = 0.035 &lt; 0.05</div>');

  cleanMarkdown = cleanMarkdown.replace(/\$\$t\(49\)\s*=\s*\\frac\{82\.85\s*-\s*80\.00\}\{10\.91\s*\/\s*\\sqrt\{50\}\}\s*=\s*1\.848,\s*\\quad\s*p\s*=\s*0\.035\s*<\s*0\.05\$\$/g,
    '<div class="math-block"><em>t</em>(49) = (82.85 − 80.00) / (10.91 / √50) = <strong>1.848</strong>, &nbsp;&nbsp; <em>p</em> = 0.035 &lt; 0.05</div>');

  // Generic fallback for any remaining block math $$...$$
  cleanMarkdown = cleanMarkdown.replace(/\$\$([\s\S]*?)\$\$/g, (m, p1) => `<div class="math-block">${p1.trim()}</div>`);

  // Transform inline math tokens $...$
  cleanMarkdown = cleanMarkdown.replace(/\$HE\\text\{-3\}:\s*\\mu\s*>\s*80\$/g, '<em>HE-3: μ &gt; 80</em>');
  cleanMarkdown = cleanMarkdown.replace(/\$HE\\text\{-2\}\$/g, '<em>HE-2</em>');
  cleanMarkdown = cleanMarkdown.replace(/\$HE\\text\{-1\}\$/g, '<em>HE-1</em>');
  cleanMarkdown = cleanMarkdown.replace(/\$HE\\text\{-3\}\$/g, '<em>HE-3</em>');
  cleanMarkdown = cleanMarkdown.replace(/\$H_0:\s*\\mu\s*\\le\s*80\$/g, '<em>H</em>₀: <em>μ</em> ≤ 80');
  cleanMarkdown = cleanMarkdown.replace(/\$H_1:\s*\\mu\s*>\s*80\$/g, '<em>H</em>₁: <em>μ</em> &gt; 80');
  cleanMarkdown = cleanMarkdown.replace(/\$H_0\$/g, '<em>H</em>₀');
  cleanMarkdown = cleanMarkdown.replace(/\$H_1\$/g, '<em>H</em>₁');
  cleanMarkdown = cleanMarkdown.replace(/\$Ha\$/g, '<em>Ha</em>');
  cleanMarkdown = cleanMarkdown.replace(/\$LI_\{95\\%\}\s*=\s*80\.26\$/g, '<em>LI</em><sub>95%</sub> = 80.26');
  cleanMarkdown = cleanMarkdown.replace(/\$LI_\{95\\%\}\$/g, '<em>LI</em><sub>95%</sub>');
  cleanMarkdown = cleanMarkdown.replace(/\$IC_\{95\\%\}\s*=\s*\[79\.75,\s*85\.95\]\$/g, '<em>IC</em><sub>95%</sub> = [79.75, 85.95]');
  cleanMarkdown = cleanMarkdown.replace(/\$Var\(X\)\s*=\s*19\.0208\$/g, '<em>Var(X)</em> = 19.0208');
  cleanMarkdown = cleanMarkdown.replace(/\\sum s_j\^2\s*=\s*3\.7555/g, '∑<em>s<sub>j</sub>²</em> = 3.7555');
  cleanMarkdown = cleanMarkdown.replace(/\$\\alpha\s*=\s*0\.05\$/g, '<em>α</em> = 0.05');
  cleanMarkdown = cleanMarkdown.replace(/\$\\alpha\s*\\ge\s*0\.85\$/g, '<em>α</em> ≥ 0.85');
  cleanMarkdown = cleanMarkdown.replace(/\$\\alpha\s*=\s*0\.892\$/g, '<em>α</em> = 0.892');
  cleanMarkdown = cleanMarkdown.replace(/\$n\s*=\s*50\$/g, '<em>n</em> = 50');
  cleanMarkdown = cleanMarkdown.replace(/\$s\s*=\s*10\.91\$/g, '<em>s</em> = 10.91');
  cleanMarkdown = cleanMarkdown.replace(/\$s\s*=\s*11\.21\$/g, '<em>s</em> = 11.21');
  cleanMarkdown = cleanMarkdown.replace(/\$s\s*=\s*9\.91\$/g, '<em>s</em> = 9.91');
  cleanMarkdown = cleanMarkdown.replace(/\$s\s*=\s*12\.72\$/g, '<em>s</em> = 12.72');
  cleanMarkdown = cleanMarkdown.replace(/\$t\(49\)\s*=\s*1\.848,\s*p\s*=\s*0\.035\$/g, '<em>t</em>(49) = 1.848, <em>p</em> = 0.035');

  // General clean-up for remaining LaTeX commands
  cleanMarkdown = cleanMarkdown.replace(/\\left\(/g, '(').replace(/\\right\)/g, ')');
  cleanMarkdown = cleanMarkdown.replace(/\\frac\{([^{}]+)\}\{([^{}]+)\}/g, '($1 / $2)');
  cleanMarkdown = cleanMarkdown.replace(/\\sqrt\{([^{}]+)\}/g, '√($1)');
  cleanMarkdown = cleanMarkdown.replace(/\\alpha/g, 'α');
  cleanMarkdown = cleanMarkdown.replace(/\\bar\{([^{}]+)\}/g, '$1̄');
  cleanMarkdown = cleanMarkdown.replace(/\\cdot/g, '·');
  cleanMarkdown = cleanMarkdown.replace(/\\quad/g, ' ');
  cleanMarkdown = cleanMarkdown.replace(/\\text\{([^{}]+)\}/g, '$1');

  // Render markdown to HTML
  const parsedContentHtml = marked.parse(cleanMarkdown);

  // Build the complete HTML document
  const fullHtml = `<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>Protocolo de Investigación SIGRE - Ciclo 2026B</title>
  <style>
    @page {
      size: letter;
      margin: 1in;
    }
    
    * {
      box-sizing: border-box;
    }

    body {
      font-family: 'Segoe UI', Arial, Helvetica, sans-serif;
      font-size: 10.5pt;
      line-height: 1.55;
      color: #1A202C;
      text-align: justify;
      text-justify: inter-word;
      margin: 0;
      padding: 0;
    }

    /* Cover Page */
    .cover-page {
      page-break-after: always;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      min-height: 9.2in;
      text-align: center;
      padding: 20px 0;
    }

    .cover-header {
      margin-bottom: 25px;
    }

    .cover-logo {
      height: 95px;
      margin-bottom: 15px;
      object-fit: contain;
    }

    .univ-name {
      font-size: 17pt;
      font-weight: 800;
      color: #002B49;
      letter-spacing: 0.5px;
      margin: 0 0 4px 0;
      text-transform: uppercase;
    }

    .center-name {
      font-size: 13.5pt;
      font-weight: 700;
      color: #1A365D;
      margin: 0 0 6px 0;
      text-transform: uppercase;
    }

    .division-name {
      font-size: 10.5pt;
      font-weight: 600;
      color: #4A5568;
      margin: 0 0 4px 0;
    }

    .career-name {
      font-size: 12pt;
      font-weight: 700;
      color: #002B49;
      margin: 0;
      letter-spacing: 0.3px;
    }

    .cover-divider {
      width: 140px;
      height: 3px;
      background: #002B49;
      margin: 20px auto;
    }

    .cover-title-box {
      border: 2px solid #002B49;
      background: #F8FAFC;
      border-radius: 8px;
      padding: 24px 20px;
      margin: 25px 0;
    }

    .proto-badge {
      font-size: 9.5pt;
      font-weight: 700;
      color: #2B6CB0;
      letter-spacing: 1.5px;
      text-transform: uppercase;
      margin-bottom: 10px;
    }

    .cover-title {
      font-size: 16.5pt;
      font-weight: 800;
      color: #002B49;
      line-height: 1.35;
      margin: 0 0 10px 0;
    }

    .cover-subtitle {
      font-size: 11pt;
      font-weight: 500;
      color: #4A5568;
      margin: 0;
      line-height: 1.4;
    }

    .cover-meta-table {
      width: 100%;
      border-collapse: collapse;
      margin: 20px 0;
      text-align: left;
      font-size: 10pt;
    }

    .cover-meta-table td {
      padding: 6px 12px;
      border-bottom: 1px solid #E2E8F0;
    }

    .cover-meta-table td.label {
      width: 32%;
      font-weight: 700;
      color: #002B49;
    }

    .cover-meta-table td.val {
      color: #2D3748;
    }

    .cover-footer {
      margin-top: 15px;
      font-size: 9.5pt;
      color: #718096;
      border-top: 1px solid #CBD5E0;
      padding-top: 10px;
    }

    /* Headings */
    h1 {
      font-size: 15.5pt;
      font-weight: 800;
      color: #002B49;
      border-bottom: 2px solid #002B49;
      padding-bottom: 6px;
      margin-top: 28px;
      margin-bottom: 14px;
      page-break-before: always;
      page-break-after: avoid;
    }

    /* First h1 after cover shouldn't break page unnecessarily */
    .content-body > h1:first-child {
      page-break-before: avoid;
    }

    h2 {
      font-size: 12.5pt;
      font-weight: 700;
      color: #002B49;
      margin-top: 20px;
      margin-bottom: 10px;
      page-break-after: avoid;
    }

    h3 {
      font-size: 11pt;
      font-weight: 700;
      color: #1A365D;
      margin-top: 16px;
      margin-bottom: 8px;
      page-break-after: avoid;
    }

    p {
      margin-top: 0;
      margin-bottom: 10px;
    }

    ul, ol {
      margin-top: 0;
      margin-bottom: 12px;
      padding-left: 24px;
    }

    li {
      margin-bottom: 5px;
    }

    blockquote {
      border-left: 3.5px solid #002B49;
      background: #F8FAFC;
      padding: 10px 16px;
      margin: 14px 0;
      font-style: italic;
      color: #2D3748;
      border-radius: 0 4px 4px 0;
      page-break-inside: avoid;
    }

    /* APA 7 Tables */
    table {
      width: 100%;
      border-collapse: collapse;
      margin: 16px 0;
      font-size: 8.5pt;
      page-break-inside: avoid;
    }

    table th {
      border-top: 2px solid #002B49;
      border-bottom: 1.5px solid #002B49;
      background-color: #F0F4F8;
      color: #002B49;
      font-weight: 700;
      padding: 7px 9px;
      text-align: left;
    }

    table td {
      border-bottom: 1px solid #E2E8F0;
      padding: 6px 9px;
      vertical-align: top;
      color: #2D3748;
    }

    table tr:last-child td {
      border-bottom: 2px solid #002B49;
    }

    /* Figures */
    .figure-block {
      margin: 20px 0;
      text-align: center;
      page-break-inside: avoid;
    }

    .figure-num {
      font-size: 10pt;
      font-weight: 800;
      color: #002B49;
      text-align: left;
      margin-bottom: 2px;
    }

    .figure-title {
      font-size: 9.5pt;
      font-style: italic;
      color: #2D3748;
      text-align: left;
      margin-bottom: 8px;
    }

    .fig-img {
      max-width: 90%;
      max-height: 380px;
      border: 1px solid #CBD5E0;
      border-radius: 4px;
      box-shadow: 0 2px 5px rgba(0,0,0,0.06);
      display: inline-block;
      margin: 4px auto;
    }

    .two-img-grid {
      display: flex;
      gap: 12px;
      justify-content: center;
      margin: 4px auto;
    }

    .fig-img-half {
      max-width: 48%;
      max-height: 260px;
      border: 1px solid #CBD5E0;
      border-radius: 4px;
      box-shadow: 0 2px 5px rgba(0,0,0,0.06);
    }

    .figure-note {
      font-size: 8pt;
      color: #718096;
      text-align: left;
      margin-top: 6px;
      border-top: 1px solid #E2E8F0;
      padding-top: 4px;
    }

    .academic-note-box {
      border: 1px solid #CBD5E0;
      border-left: 4px solid #2B6CB0;
      background: #F8FAFC;
      border-radius: 4px;
      padding: 14px 18px;
      margin: 20px 0;
      page-break-inside: avoid;
    }

    .math-block {
      background: #F8FAFC;
      border: 1px solid #CBD5E1;
      border-left: 4px solid #002B49;
      border-radius: 4px;
      padding: 10px 16px;
      margin: 14px 0;
      text-align: center;
      font-size: 11pt;
      font-family: 'Cambria Math', 'Times New Roman', serif;
      page-break-inside: avoid;
    }

    .academic-note-title {
      font-size: 9.5pt;
      font-weight: 700;
      color: #1A365D;
      margin-bottom: 8px;
      letter-spacing: 0.3px;
    }

    .repo-link a {
      color: #2B6CB0;
      text-decoration: underline;
      font-family: Consolas, monospace;
      font-size: 9pt;
    }

    code {
      font-family: Consolas, 'Courier New', monospace;
      font-size: 9pt;
      background: #EDF2F7;
      padding: 2px 5px;
      border-radius: 3px;
      color: #805AD5;
    }

    pre {
      background: #F7FAFC;
      border: 1px solid #E2E8F0;
      border-left: 3px solid #002B49;
      border-radius: 4px;
      padding: 12px;
      font-family: Consolas, monospace;
      font-size: 8.5pt;
      overflow-x: auto;
      page-break-inside: avoid;
      white-space: pre-wrap;
      word-break: break-all;
    }

    hr {
      display: none;
    }
  </style>
</head>
<body>

  <!-- PORTADA INSTITUCIONAL OFICIAL -->
  <div class="cover-page">
    <div class="cover-header">
      <img src="${logoBase64}" alt="Escudo Universidad de Guadalajara" class="cover-logo" />
      <div class="univ-name">Universidad de Guadalajara</div>
      <div class="center-name">Centro Universitario de Tonalá</div>
      <div class="division-name">División de Ingenierías e Innovación Tecnológica</div>
      <div class="career-name">Licenciatura en Ingeniería en Ciencias Computacionales</div>
    </div>

    <div class="cover-divider"></div>

    <div class="cover-title-box">
      <div class="proto-badge">Protocolo de Investigación Científica y Tecnológica</div>
      <h1 class="cover-title" style="page-break-before: avoid; border: none; padding: 0;">SISTEMA INTEGRADO DE GESTIÓN DE RECURSOS Y ESPACIOS (SIGRE)</h1>
      <div class="cover-subtitle">Optimización del control patrimonial, concurrencia en reservaciones y sustitución de modelos analógicos en CUTonalá</div>
    </div>

    <table class="cover-meta-table">
      <tr>
        <td class="label">Materia:</td>
        <td class="val"><strong>METODOLOGÍA Y PRÁCTICA DE LA INVESTIGACIÓN</strong></td>
      </tr>
      <tr>
        <td class="label">Ciclo Escolar:</td>
        <td class="val"><strong>2026B</strong></td>
      </tr>
      <tr>
        <td class="label">Docente Titular:</td>
        <td class="val">Mtra. Elizabeth Cristina Hernández Hernández</td>
      </tr>
      <tr>
        <td class="label">Equipo / Identificador:</td>
        <td class="val"><strong>Equipo 4</strong></td>
      </tr>
      <tr>
        <td class="label">Integrantes del Equipo:</td>
        <td class="val">
          • <strong>Barragán Padilla Carlos Emiliano</strong><br>
          • <strong>Fierro Meléndez Ernesto Hatuey</strong><br>
          • <strong>Padilla Casillas Josue Wenceslao</strong>
        </td>
      </tr>
      <tr>
        <td class="label">Fecha de Elaboración:</td>
        <td class="val">Noviembre de 2026</td>
      </tr>
      <tr>
        <td class="label">Lugar de Elaboración:</td>
        <td class="val">Tonalá, Jalisco, México</td>
      </tr>
      <tr>
        <td class="label">Nombre del Entregable:</td>
        <td class="val"><code>2026B_Equipo4_Protocolo.pdf</code></td>
      </tr>
    </table>

    <div class="cover-footer">
      Documento académico elaborado bajo el formato y rúbrica oficial de la Coordinación de la Licenciatura en Ingeniería en Ciencias Computacionales.
    </div>
  </div>

  <!-- CUERPO DEL PROTOCOLO -->
  <div class="content-body">
    ${parsedContentHtml}
  </div>

</body>
</html>
`;

  console.log('Writing compiled HTML to:', outHtmlPath);
  fs.writeFileSync(outHtmlPath, fullHtml, 'utf8');

  console.log('Launching Playwright Chromium to generate PDF...');
  const browser = await chromium.launch();
  const page = await browser.newPage();

  // Load the rendered HTML
  await page.setContent(fullHtml, { waitUntil: 'load' });

  // Give images a moment to decode
  await page.waitForTimeout(1000);

  console.log('Generating PDF:', outPdfPath);
  await page.pdf({
    path: outPdfPath,
    format: 'Letter',
    printBackground: true,
    displayHeaderFooter: true,
    headerTemplate: `
      <div style="font-size: 8pt; color: #718096; width: 100%; padding: 0 45px; display: flex; justify-content: space-between; font-family: 'Segoe UI', Arial, sans-serif; border-bottom: 1px solid #E2E8F0; padding-bottom: 3px;">
        <span>Universidad de Guadalajara — CUTonalá</span>
        <span>Protocolo SIGRE — Ciclo 2026B</span>
      </div>
    `,
    footerTemplate: `
      <div style="font-size: 8.5pt; color: #4A5568; width: 100%; padding: 0 45px; display: flex; justify-content: space-between; font-family: 'Segoe UI', Arial, sans-serif; border-top: 1px solid #CBD5E0; padding-top: 3px;">
        <span>Equipo 4: Barragán Padilla, Fierro Meléndez, Padilla Casillas</span>
        <span>Página <span class="pageNumber"></span> de <span class="totalPages"></span></span>
      </div>
    `,
    margin: {
      top: '1.05in',
      bottom: '1.05in',
      left: '0.95in',
      right: '0.95in'
    }
  });

  await browser.close();

  const outPdfPath2 = path.resolve(__dirname, '../docs/2026B_Protocolo_Investigacion_SIGRE_Completo.pdf');
  fs.copyFileSync(outPdfPath, outPdfPath2);

  const stats = fs.statSync(outPdfPath);
  console.log(`✅ PDF generated successfully! Size: ${stats.size.toLocaleString()} bytes (saved to Equipo4 and Completo paths)`);
}

buildProtocoloPDF().catch(err => {
  console.error('Error generating PDF:', err);
  process.exit(1);
});
