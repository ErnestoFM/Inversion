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
    padding: 10px 14px;
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
    margin-bottom: 8px;
  }
  .stages-wrapper {
    display: flex;
    align-items: stretch;
    justify-content: space-between;
    gap: 6px;
  }
  .stage-card {
    flex: 1;
    border-radius: 6px;
    padding: 7px 8px;
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    box-sizing: border-box;
    border: 1.5px solid;
  }
  .card-e1 {
    background-color: #eff6ff;
    border-color: #93c5fd;
  }
  .card-e2 {
    background-color: #f0fdf4;
    border-color: #86efac;
  }
  .card-e3 {
    background-color: #faf5ff;
    border-color: #d8b4fe;
  }
  .card-e4 {
    background-color: #fffbeb;
    border-color: #fde68a;
  }

  .stage-badge {
    font-size: 7.5px;
    font-weight: 800;
    padding: 1.5px 5px;
    border-radius: 3px;
    color: #ffffff;
    margin-bottom: 3px;
    letter-spacing: 0.3px;
  }
  .badge-e1 { background-color: #2563eb; }
  .badge-e2 { background-color: #16a34a; }
  .badge-e3 { background-color: #7c3aed; }
  .badge-e4 { background-color: #d97706; }

  .stage-title {
    font-size: 10px;
    font-weight: 800;
    color: #1e293b;
    margin-bottom: 2px;
  }
  .stage-dates {
    font-size: 8.5px;
    font-weight: 700;
    color: #0f172a;
    margin-bottom: 4px;
  }
  .stage-desc {
    font-size: 8px;
    color: #475569;
    line-height: 1.25;
    flex-grow: 1;
  }

  .arrow-sep {
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 13px;
    font-weight: 900;
    color: #94a3b8;
    width: 12px;
    flex-shrink: 0;
  }
</style>
</head>
<body>
<div class="container" id="capture">
  <div class="title">Esquema Secuencial de Etapas Operativas y Metas Críticas (Año 1)</div>
  <div class="subtitle">Ruta de Ejecución del Capital Semilla ($180k MXN) y Despliegue en 3 Planteles (Ciclo 2027-A / 2027-B)</div>

  <div class="stages-wrapper">
    <!-- Etapa 1 -->
    <div class="stage-card card-e1">
      <div class="stage-badge badge-e1">ETAPA 1 • M1 - M2</div>
      <div class="stage-title">CAPEX, IP y GCP</div>
      <div class="stage-dates">Ene – Feb 2027</div>
      <div class="stage-desc">
        Desembolso $180k pre-semilla.<br>
        Infraestructura en GCP.<br>
        Depósito INDAUTOR y marca IMPI.
      </div>
    </div>

    <div class="arrow-sep">➔</div>

    <!-- Etapa 2 -->
    <div class="stage-card card-e2">
      <div class="stage-badge badge-e2">ETAPA 2 • M3 - M4</div>
      <div class="stage-title">Despliegue CUTonalá</div>
      <div class="stage-dates">Mar – Abr 2027</div>
      <div class="stage-desc">
        3 terminales en producción.<br>
        Cobro setup piloto ($15k).<br>
        Auditoría 1,200 actas mostrador.
      </div>
    </div>

    <div class="arrow-sep">➔</div>

    <!-- Etapa 3 -->
    <div class="stage-card card-e3">
      <div class="stage-badge badge-e3">ETAPA 3 • M5 - M6</div>
      <div class="stage-title">Demos y Cierre SEMS</div>
      <div class="stage-dates">May – Jun 2027</div>
      <div class="stage-desc">
        Rondas comerciales B2G.<br>
        Firma 2 contratos SEMS ($48k).<br>
        Compra directa (< 37 UMA).
      </div>
    </div>

    <div class="arrow-sep">➔</div>

    <!-- Etapa 4 -->
    <div class="stage-card card-e4">
      <div class="stage-badge badge-e4">ETAPA 4 • M7 - M12</div>
      <div class="stage-title">Operación 3 Planteles</div>
      <div class="stage-dates">Jul – Dic 2027</div>
      <div class="stage-desc">
        3 planteles en operación.<br>
        Cobro facturación $63,000 MXN.<br>
        Validación cero merma patrimonial.
      </div>
    </div>
  </div>
</div>
</body>
</html>"""

os.makedirs('scratch', exist_ok=True)
os.makedirs('docs/graficos', exist_ok=True)
html_file = os.path.abspath('scratch/figura8.html')
with open(html_file, 'w', encoding='utf-8') as f:
    f.write(html_content)

chrome = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
output_img = os.path.abspath('docs/graficos/figura8_etapas_operativas_ano1.png')

cmd = [
    chrome,
    '--headless=new',
    '--disable-gpu',
    '--run-all-compositor-stages-before-draw',
    '--force-device-scale-factor=2',
    f'--screenshot={output_img}',
    '--window-size=920,320',
    f'file:///{html_file}'
]

print("Generando imagen de alta resolución para Figura 8 con Chrome...")
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
