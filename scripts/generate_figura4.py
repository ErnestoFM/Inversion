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
    padding: 12px;
    background: #ffffff;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  }
  .container {
    width: 860px;
    border: 1.5px solid #cbd5e1;
    border-radius: 8px;
    padding: 12px 18px;
    background: #ffffff;
    box-shadow: 0 3px 6px -1px rgba(0,0,0,0.04);
    box-sizing: border-box;
  }
  .title {
    text-align: center;
    font-size: 13px;
    font-weight: 800;
    color: #0f172a;
    letter-spacing: 0.5px;
    text-transform: uppercase;
    margin-bottom: 2px;
  }
  .subtitle {
    text-align: center;
    font-size: 9.5px;
    color: #64748b;
    margin-bottom: 10px;
  }
  .phases-wrapper {
    display: flex;
    align-items: stretch;
    justify-content: space-between;
    gap: 10px;
  }
  .phase-card {
    flex: 1;
    border-radius: 6px;
    padding: 8px 10px;
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    box-sizing: border-box;
  }
  .phase-1 {
    background-color: #f0fdf4;
    border: 1.5px solid #86efac;
  }
  .phase-2 {
    background-color: #eff6ff;
    border: 1.5px solid #93c5fd;
  }
  .phase-3 {
    background-color: #faf5ff;
    border: 1.5px solid #d8b4fe;
  }
  .phase-badge {
    font-size: 8px;
    font-weight: 800;
    padding: 2px 7px;
    border-radius: 4px;
    margin-bottom: 4px;
    letter-spacing: 0.4px;
    color: #ffffff;
  }
  .badge-1 { background-color: #16a34a; }
  .badge-2 { background-color: #2563eb; }
  .badge-3 { background-color: #7c3aed; }

  .phase-title {
    font-size: 10.5px;
    font-weight: 800;
    color: #1e293b;
    margin-bottom: 2px;
  }
  .phase-target {
    font-size: 12.5px;
    font-weight: 900;
    margin-bottom: 4px;
  }
  .target-1 { color: #15803d; }
  .target-2 { color: #1d4ed8; }
  .target-3 { color: #6d28d9; }

  .phase-detail {
    font-size: 8.5px;
    color: #475569;
    line-height: 1.3;
    margin-bottom: 6px;
    flex-grow: 1;
  }
  .phase-tag {
    font-size: 8px;
    font-weight: 700;
    padding: 2px 8px;
    border-radius: 3px;
    background: rgba(0,0,0,0.05);
    color: #334155;
    white-space: nowrap;
  }
  .arrow-wrapper {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: 26px;
    flex-shrink: 0;
  }
  .arrow-symbol {
    font-size: 16px;
    font-weight: 900;
    color: #94a3b8;
  }
  .arrow-label {
    font-size: 7.5px;
    font-weight: 700;
    color: #94a3b8;
    text-transform: uppercase;
    letter-spacing: 0.3px;
    margin-top: 1px;
  }
</style>
</head>
<body>
<div class="container" id="capture">
  <div class="title">Ruta de Escalamiento Institucional y Cobertura de Mercado</div>
  <div class="subtitle">Estrategia Progresiva: Desde el Núcleo UdeG hacia Universidades Públicas Estatales (UPES)</div>
  
  <div class="phases-wrapper">
    <!-- Fase 1 -->
    <div class="phase-card phase-1">
      <div class="phase-badge badge-1">FASE 1 • AÑO 1</div>
      <div class="phase-title">Piloto y Validación</div>
      <div class="phase-target target-1">3 Planteles</div>
      <div class="phase-detail">
        <strong>CUTonalá</strong> (piloto sin costo con setup)<br>
        <strong>+ 2 Prepas SEMS</strong> ($24k c/u).<br>
        Validación operativa y SLA en mostrador.
      </div>
      <div class="phase-tag">Nube GCP + Blindaje IP</div>
    </div>

    <!-- Flecha 1 -->
    <div class="arrow-wrapper">
      <div class="arrow-symbol">➔</div>
      <div class="arrow-label">Adopción</div>
    </div>

    <!-- Fase 2 -->
    <div class="phase-card phase-2">
      <div class="phase-badge badge-2">FASE 2 • AÑOS 2 - 3</div>
      <div class="phase-title">Consolidación Red UdeG</div>
      <div class="phase-target target-2">8 a 22 Planteles</div>
      <div class="phase-detail">
        <strong>Año 2:</strong> 8 sedes (3 CUs + 5 Prepas).<br>
        <strong>Año 3:</strong> 22 sedes (8 CUs + 14 Prepas).<br>
        Penetración 11.22% mercado UdeG.
      </div>
      <div class="phase-tag">Liquidación Mes 31.1 (75% FEN)</div>
    </div>

    <!-- Flecha 2 -->
    <div class="arrow-wrapper">
      <div class="arrow-symbol">➔</div>
      <div class="arrow-label">Expansión</div>
    </div>

    <!-- Fase 3 -->
    <div class="phase-card phase-3">
      <div class="phase-badge badge-3">FASE 3 • AÑOS 4 - 5</div>
      <div class="phase-title">Expansión Nacional UPES</div>
      <div class="phase-target target-3">31 a 50 Planteles</div>
      <div class="phase-detail">
        <strong>22 sedes UdeG</strong> consolidadas<br>
        <strong>+ 9 a 28 unidades UPES</strong> regionales.<br>
        Catálogo ANUIES (> 340 unidades).
      </div>
      <div class="phase-tag">TIR Inversionista: 26.51% anual</div>
    </div>
  </div>
</div>
</body>
</html>"""

os.makedirs('scratch', exist_ok=True)
os.makedirs('docs/graficos', exist_ok=True)
html_file = os.path.abspath('scratch/figura4.html')
with open(html_file, 'w', encoding='utf-8') as f:
    f.write(html_content)

chrome = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
output_img = os.path.abspath('docs/graficos/figura4_escalamiento_institucional.png')

cmd = [
    chrome,
    '--headless=new',
    '--disable-gpu',
    '--run-all-compositor-stages-before-draw',
    '--force-device-scale-factor=2',
    f'--screenshot={output_img}',
    '--window-size=920,350',
    f'file:///{html_file}'
]

print("Generando imagen de alta resolución para Figura 4 con Chrome...")
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
