# -*- coding: utf-8 -*-
import os
import subprocess
from PIL import Image
import numpy as np

html_content = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  body {
    margin: 0;
    padding: 10px;
    background: #ffffff;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  }
  .container {
    width: 860px;
    border: 1.5px solid #cbd5e1;
    border-radius: 8px;
    padding: 10px 16px;
    background: #ffffff;
    box-shadow: 0 3px 6px -1px rgba(0,0,0,0.04);
    box-sizing: border-box;
  }
  .header-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 6px;
    border-bottom: 1px solid #f1f5f9;
    padding-bottom: 6px;
  }
  .title-group {
    flex: 1;
  }
  .title {
    font-size: 13px;
    font-weight: 800;
    color: #0f172a;
    letter-spacing: 0.5px;
    text-transform: uppercase;
    margin-bottom: 2px;
  }
  .subtitle {
    font-size: 9.5px;
    color: #64748b;
  }
  .legend {
    display: flex;
    gap: 12px;
    align-items: center;
  }
  .legend-item {
    display: flex;
    align-items: center;
    gap: 5px;
    font-size: 8.5px;
    font-weight: 700;
    color: #334155;
  }
  .legend-box {
    width: 12px;
    height: 10px;
    border-radius: 2px;
  }
  .box-done { background: #16a34a; border: 1px solid #15803d; }
  .box-crit { background: #dc2626; border: 1px solid #b91c1c; }

  .chart-wrapper {
    display: flex;
    justify-content: center;
    margin-top: 4px;
  }
</style>
</head>
<body>
<div class="container" id="capture">
  <div class="header-row">
    <div class="title-group">
      <div class="title">Cronograma de Ejecución y Ruta Crítica [RC] (Ciclos 2026-B y 2027-A)</div>
      <div class="subtitle">Programación Temporal, Dependencias Secuenciales y Ventanas de Despliegue en 23 Semanas</div>
    </div>
    <div class="legend">
      <div class="legend-item"><div class="legend-box box-done"></div> Antecedente Concluido (2026-B)</div>
      <div class="legend-item"><div class="legend-box box-crit"></div> Ruta Crítica [RC] (Holgura = 0 sem, 2027-A)</div>
    </div>
  </div>

  <div class="chart-wrapper">
    <svg width="830" height="200" viewBox="0 0 830 200" font-family="system-ui, -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif">
      <!-- Fondo y Cuadrícula -->
      <!-- Cabecera de Meses -->
      <!-- Ciclo 2026-B -->
      <rect x="290" y="5" width="100" height="18" fill="#f0fdf4" rx="2" stroke="#bbf7d0" stroke-width="1"/>
      <text x="340" y="17" font-size="8.5" font-weight="800" fill="#166534" text-anchor="middle">2026-B (Ago-Nov)</text>

      <!-- Ciclo 2027-A -->
      <rect x="400" y="5" width="415" height="18" fill="#f8fafc" rx="2" stroke="#cbd5e1" stroke-width="1"/>
      <!-- Meses 2027 -->
      <text x="432" y="17" font-size="8.5" font-weight="700" fill="#475569" text-anchor="middle">Ene</text>
      <text x="497" y="17" font-size="8.5" font-weight="700" fill="#475569" text-anchor="middle">Feb</text>
      <text x="565" y="17" font-size="8.5" font-weight="700" fill="#475569" text-anchor="middle">Mar</text>
      <text x="635" y="17" font-size="8.5" font-weight="700" fill="#475569" text-anchor="middle">Abr</text>
      <text x="705" y="17" font-size="8.5" font-weight="700" fill="#475569" text-anchor="middle">May</text>
      <text x="775" y="17" font-size="8.5" font-weight="700" fill="#475569" text-anchor="middle">Jun</text>

      <!-- Líneas verticales de meses -->
      <line x1="290" y1="23" x2="290" y2="195" stroke="#e2e8f0" stroke-width="1"/>
      <line x1="390" y1="23" x2="390" y2="195" stroke="#cbd5e1" stroke-width="1.5" stroke-dasharray="3,2"/>
      <line x1="400" y1="23" x2="400" y2="195" stroke="#cbd5e1" stroke-width="1"/>
      <line x1="465" y1="23" x2="465" y2="195" stroke="#e2e8f0" stroke-width="1"/>
      <line x1="530" y1="23" x2="530" y2="195" stroke="#e2e8f0" stroke-width="1"/>
      <line x1="600" y1="23" x2="600" y2="195" stroke="#e2e8f0" stroke-width="1"/>
      <line x1="670" y1="23" x2="670" y2="195" stroke="#e2e8f0" stroke-width="1"/>
      <line x1="740" y1="23" x2="740" y2="195" stroke="#e2e8f0" stroke-width="1"/>
      <line x1="815" y1="23" x2="815" y2="195" stroke="#cbd5e1" stroke-width="1"/>

      <!-- Tareas -->
      <!-- A0 -->
      <g transform="translate(0, 32)">
        <text x="5" y="11" font-size="9" font-weight="700" fill="#1e293b">A0. Diagnóstico y Validación SUS (n = 50)</text>
        <text x="245" y="11" font-size="8" font-weight="600" fill="#64748b" text-anchor="end">15 sem • Antecedente</text>
        <rect x="295" y="1" width="90" height="13" rx="3" fill="#16a34a" stroke="#15803d" stroke-width="1"/>
        <text x="340" y="10.5" font-size="7.5" font-weight="800" fill="#ffffff" text-anchor="middle">10 Ago – 20 Nov</text>
      </g>

      <!-- A1 -->
      <g transform="translate(0, 56)">
        <text x="5" y="11" font-size="9" font-weight="800" fill="#0f172a">A1. Desembolso CAPEX y Nube GCP ($180k)</text>
        <text x="245" y="11" font-size="8" font-weight="700" fill="#b91c1c" text-anchor="end">4 sem • [RC]</text>
        <rect x="410" y="1" width="52" height="13" rx="3" fill="#dc2626" stroke="#b91c1c" stroke-width="1"/>
        <text x="436" y="10.5" font-size="7.5" font-weight="800" fill="#ffffff" text-anchor="middle">11 Ene – 06 Feb</text>
      </g>

      <!-- A2 -->
      <g transform="translate(0, 80)">
        <text x="5" y="11" font-size="9" font-weight="800" fill="#0f172a">A2. Registro INDAUTOR y Solicitud IMPI</text>
        <text x="245" y="11" font-size="8" font-weight="700" fill="#b91c1c" text-anchor="end">3 sem • [RC]</text>
        <rect x="466" y="1" width="46" height="13" rx="3" fill="#dc2626" stroke="#b91c1c" stroke-width="1"/>
        <text x="489" y="10.5" font-size="7" font-weight="800" fill="#ffffff" text-anchor="middle">08 Feb – 27 Feb</text>
      </g>

      <!-- A3 -->
      <g transform="translate(0, 104)">
        <text x="5" y="11" font-size="9" font-weight="800" fill="#0f172a">A3. Hardware y Despliegue CUTonalá</text>
        <text x="245" y="11" font-size="8" font-weight="700" fill="#b91c1c" text-anchor="end">4 sem • [RC]</text>
        <rect x="530" y="1" width="56" height="13" rx="3" fill="#dc2626" stroke="#b91c1c" stroke-width="1"/>
        <text x="558" y="10.5" font-size="7.5" font-weight="800" fill="#ffffff" text-anchor="middle">01 Mar – 27 Mar</text>
      </g>

      <!-- A4 -->
      <g transform="translate(0, 128)">
        <text x="5" y="11" font-size="9" font-weight="800" fill="#0f172a">A4. Operación y Auditoría 1,200 Actas</text>
        <text x="245" y="11" font-size="8" font-weight="700" fill="#b91c1c" text-anchor="end">5 sem • [RC]</text>
        <rect x="595" y="1" width="68" height="13" rx="3" fill="#dc2626" stroke="#b91c1c" stroke-width="1"/>
        <text x="629" y="10.5" font-size="7.5" font-weight="800" fill="#ffffff" text-anchor="middle">29 Mar – 30 Abr</text>
      </g>

      <!-- A5 -->
      <g transform="translate(0, 152)">
        <text x="5" y="11" font-size="9" font-weight="800" fill="#0f172a">A5. Rondas Comerciales en SEMS</text>
        <text x="245" y="11" font-size="8" font-weight="700" fill="#b91c1c" text-anchor="end">4 sem • [RC]</text>
        <rect x="670" y="1" width="56" height="13" rx="3" fill="#dc2626" stroke="#b91c1c" stroke-width="1"/>
        <text x="698" y="10.5" font-size="7.5" font-weight="800" fill="#ffffff" text-anchor="middle">03 May – 28 May</text>
      </g>

      <!-- A6 -->
      <g transform="translate(0, 176)">
        <text x="5" y="11" font-size="9" font-weight="800" fill="#0f172a">A6. Cierre 2 Contratos Comerciales SEMS</text>
        <text x="245" y="11" font-size="8" font-weight="700" fill="#b91c1c" text-anchor="end">3 sem • [RC]</text>
        <rect x="735" y="1" width="52" height="13" rx="3" fill="#dc2626" stroke="#b91c1c" stroke-width="1"/>
        <text x="761" y="10.5" font-size="7.5" font-weight="800" fill="#ffffff" text-anchor="middle">31 May – 20 Jun</text>
      </g>

      <!-- Flechas conectoras de dependencia secuencial RC -->
      <path d="M 462 62 L 466 84" fill="none" stroke="#991b1b" stroke-width="1.2" stroke-dasharray="2,2"/>
      <path d="M 512 86 L 530 110" fill="none" stroke="#991b1b" stroke-width="1.2" stroke-dasharray="2,2"/>
      <path d="M 586 110 L 595 134" fill="none" stroke="#991b1b" stroke-width="1.2" stroke-dasharray="2,2"/>
      <path d="M 663 134 L 670 158" fill="none" stroke="#991b1b" stroke-width="1.2" stroke-dasharray="2,2"/>
      <path d="M 726 158 L 735 182" fill="none" stroke="#991b1b" stroke-width="1.2" stroke-dasharray="2,2"/>
    </svg>
  </div>
</div>
</body>
</html>"""

os.makedirs('scratch', exist_ok=True)
os.makedirs('docs/graficos', exist_ok=True)
html_file = os.path.abspath('scratch/figura9.html')
with open(html_file, 'w', encoding='utf-8') as f:
    f.write(html_content)

chrome = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
output_img = os.path.abspath('docs/graficos/figura9_cronograma_gantt_rc.png')

cmd = [
    chrome,
    '--headless=new',
    '--disable-gpu',
    '--run-all-compositor-stages-before-draw',
    '--force-device-scale-factor=2',
    f'--screenshot={output_img}',
    '--window-size=920,380',
    f'file:///{html_file}'
]

print("Generando imagen de alta resolución para Figura 9 con Chrome...")
res = subprocess.run(cmd, capture_output=True, text=True)
if res.returncode != 0:
    print("Error:", res.stderr)
    raise RuntimeError(f"Fallo al ejecutar Chrome: {res.stderr}")

if not os.path.exists(output_img):
    raise FileNotFoundError(f"No se generó {output_img}")

# Recorte preciso del contenido
im = Image.open(output_img)
arr = np.array(im)
non_white = np.where(arr[:, :, :3] < 250)
if len(non_white[0]) > 0:
    min_y, max_y = np.min(non_white[0]), np.max(non_white[0])
    min_x, max_x = np.min(non_white[1]), np.max(non_white[1])
    pad = 14
    crop_box = (
        max(0, min_x - pad),
        max(0, min_y - pad),
        min(im.width, max_x + pad),
        min(im.height, max_y + pad)
    )
    cropped = im.crop(crop_box)
    cropped.save(output_img, optimize=True)
    print(f"Imagen recortada y optimizada: {cropped.size} ({os.path.getsize(output_img)} bytes)")
else:
    print(f"Imagen guardada: {im.size} ({os.path.getsize(output_img)} bytes)")
