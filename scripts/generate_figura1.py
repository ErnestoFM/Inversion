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
    padding: 16px;
    background: #ffffff;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  }
  .container {
    width: 860px;
    border: 1.5px solid #cbd5e1;
    border-radius: 8px;
    padding: 16px 20px;
    background: #ffffff;
    box-shadow: 0 4px 6px -1px rgba(0,0,0,0.04);
    box-sizing: border-box;
  }
  .title {
    text-align: center;
    font-size: 14px;
    font-weight: 800;
    color: #0f172a;
    letter-spacing: 0.5px;
    text-transform: uppercase;
    margin-bottom: 3px;
  }
  .subtitle {
    text-align: center;
    font-size: 10.5px;
    color: #64748b;
    margin-bottom: 14px;
  }
  .flow-row {
    margin-bottom: 12px;
    border-radius: 6px;
    padding: 10px 14px;
    border: 1px solid;
  }
  .flow-analog {
    background-color: #fff5f5;
    border-color: #fecaca;
  }
  .flow-sigre {
    background-color: #f0fdf4;
    border-color: #bbf7d0;
    margin-bottom: 0;
  }
  .row-label {
    font-size: 10.5px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.4px;
    margin-bottom: 8px;
    display: flex;
    align-items: center;
  }
  .label-analog { color: #991b1b; }
  .label-sigre { color: #166534; }
  .badge {
    padding: 2px 7px;
    border-radius: 4px;
    font-size: 8.5px;
    font-weight: 800;
    margin-right: 8px;
    color: #fff;
  }
  .badge-analog { background-color: #dc2626; }
  .badge-sigre { background-color: #16a34a; }
  .cards-wrapper {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 8px;
  }
  .step-card {
    flex: 1;
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 5px;
    padding: 8px 12px;
    box-shadow: 0 1px 2px rgba(0,0,0,0.03);
    min-height: 48px;
  }
  .step-header {
    font-size: 10.5px;
    font-weight: 700;
    color: #1e293b;
    margin-bottom: 3px;
    display: flex;
    align-items: center;
  }
  .step-desc {
    font-size: 9px;
    color: #64748b;
    line-height: 1.3;
  }
  .arrow {
    font-size: 14px;
    font-weight: bold;
    color: #94a3b8;
    flex-shrink: 0;
  }
  .arrow-analog { color: #f87171; }
  .arrow-sigre { color: #4ade80; }
</style>
</head>
<body>
<div class="container" id="capture">
  <div class="title">Comparativa del Flujo Operativo en Mostrador de Almacén</div>
  <div class="subtitle">Diagnóstico del Procedimiento Analógico Manual vs. Solución Digitalizada SIGRE</div>
  
  <!-- Flujo Analógico -->
  <div class="flow-row flow-analog">
    <div class="row-label label-analog">
      <span class="badge badge-analog">FLUJO ACTUAL</span> Proceso Manual en Libretas de Actas en Papel
    </div>
    <div class="cards-wrapper">
      <div class="step-card">
        <div class="step-header">⏳ Demoras en Ventanilla</div>
        <div class="step-desc"><strong>3.5 a 5.0 minutos</strong> por alumno. Filas continuas en cambios de clase.</div>
      </div>
      <div class="arrow arrow-analog">➔</div>
      <div class="step-card">
        <div class="step-header">📝 Registro en Papel</div>
        <div class="step-desc">Firma manuscrita en libro foliado. <strong>Sin valor probatorio ni trazabilidad.</strong></div>
      </div>
      <div class="arrow arrow-analog">➔</div>
      <div class="step-card">
        <div class="step-header">⚠️ Merma Patrimonial</div>
        <div class="step-desc"><strong>8% a 12% semestral</strong> en cables y proyectores ($115k/año sin deslinde).</div>
      </div>
    </div>
  </div>

  <!-- Flujo SIGRE -->
  <div class="flow-row flow-sigre">
    <div class="row-label label-sigre">
      <span class="badge badge-sigre">PLATAFORMA SIGRE</span> Micro-Custodia Digitalizada en Tiempo Real
    </div>
    <div class="cards-wrapper">
      <div class="step-card">
        <div class="step-header">⚡ Despacho Acelerado</div>
        <div class="step-desc"><strong>Menos de 25 segundos</strong> por entrega vía escaneo de código QR o barras.</div>
      </div>
      <div class="arrow arrow-sigre">➔</div>
      <div class="step-card">
        <div class="step-header">🔒 Firma Canvas + HMAC</div>
        <div class="step-desc">Firma digitalizada con <strong>sellado SHA256 en servidor</strong> y acta inmutable.</div>
      </div>
      <div class="arrow arrow-sigre">➔</div>
      <div class="step-card">
        <div class="step-header">🛡️ Trazabilidad Total</div>
        <div class="step-desc"><strong>0% pérdidas no atribuidas</strong>, telemetría preventiva y modo offline en PWA.</div>
      </div>
    </div>
  </div>
</div>
</body>
</html>"""

os.makedirs('scratch', exist_ok=True)
os.makedirs('docs/graficos', exist_ok=True)
html_file = os.path.abspath('scratch/figura1.html')
with open(html_file, 'w', encoding='utf-8') as f:
    f.write(html_content)

chrome = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
output_img = os.path.abspath('docs/graficos/figura1_comparativa_flujos.png')

cmd = [
    chrome,
    '--headless=new',
    '--disable-gpu',
    '--run-all-compositor-stages-before-draw',
    '--force-device-scale-factor=2',
    f'--screenshot={output_img}',
    '--window-size=920,410',
    f'file:///{html_file}'
]

print("Generando imagen de alta resolución para Figura 1 con Chrome...")
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
    pad = 16
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
