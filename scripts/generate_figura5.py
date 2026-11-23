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
    padding: 10px 16px;
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
  .arch-flow {
    display: flex;
    align-items: stretch;
    justify-content: space-between;
    gap: 8px;
  }
  .arch-col {
    flex: 1.1;
    border-radius: 6px;
    padding: 8px 9px;
    display: flex;
    flex-direction: column;
    box-sizing: border-box;
    border: 1.5px solid;
  }
  .col-pwa {
    background-color: #f0fdf4;
    border-color: #86efac;
  }
  .col-gtw {
    background-color: #eff6ff;
    border-color: #93c5fd;
  }
  .col-api {
    background-color: #f8fafc;
    border-color: #cbd5e1;
  }
  .downstream-group {
    flex: 1.8;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    gap: 5px;
  }
  .layer-badge {
    font-size: 8px;
    font-weight: 800;
    padding: 2px 6px;
    border-radius: 4px;
    margin-bottom: 4px;
    align-self: flex-start;
    color: #ffffff;
    letter-spacing: 0.3px;
  }
  .badge-pwa { background-color: #16a34a; }
  .badge-gtw { background-color: #2563eb; }
  .badge-api { background-color: #0f172a; }

  .layer-title {
    font-size: 10.5px;
    font-weight: 800;
    color: #1e293b;
    margin-bottom: 2px;
  }
  .layer-tech {
    font-size: 9px;
    font-weight: 700;
    color: #475569;
    margin-bottom: 4px;
  }
  .layer-desc {
    font-size: 8px;
    color: #64748b;
    line-height: 1.25;
  }
  .arrow-sep {
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 14px;
    font-weight: 900;
    color: #94a3b8;
    width: 14px;
    flex-shrink: 0;
  }
  .sub-card {
    border-radius: 5px;
    padding: 5px 8px;
    display: flex;
    align-items: center;
    gap: 6px;
    border: 1px solid;
    box-sizing: border-box;
  }
  .card-redis {
    background-color: #fff1f2;
    border-color: #fecdd3;
  }
  .card-sql {
    background-color: #f0f9ff;
    border-color: #bae6fd;
  }
  .card-crypto {
    background-color: #faf5ff;
    border-color: #e9d5ff;
  }
  .sub-badge {
    font-size: 7.5px;
    font-weight: 800;
    padding: 1.5px 5px;
    border-radius: 3px;
    color: #ffffff;
    white-space: nowrap;
    letter-spacing: 0.3px;
  }
  .badge-c4a { background-color: #e11d48; }
  .badge-c4b { background-color: #0284c7; }
  .badge-c5 { background-color: #7c3aed; }

  .sub-tech {
    font-size: 8.5px;
    font-weight: 800;
    color: #1e293b;
    white-space: nowrap;
  }
  .sub-desc {
    font-size: 8px;
    color: #475569;
    line-height: 1.2;
  }
</style>
</head>
<body>
<div class="container" id="capture">
  <div class="title">Arquitectura Tecnológica Cloud y Seguridad de Microservicios</div>
  <div class="subtitle">Estructura Desacoplada en 5 Capas sobre Google Cloud Platform (GCP)</div>
  
  <div class="arch-flow">
    <!-- Capa 1 -->
    <div class="arch-col col-pwa">
      <div class="layer-badge badge-pwa">CAPA 1</div>
      <div class="layer-title">Frontend PWA</div>
      <div class="layer-tech">Vue.js 3 + TypeScript</div>
      <div class="layer-desc">Interfaz mostrador (< 1.2s), Canvas firma HTML5 y modo offline con IndexedDB.</div>
    </div>

    <div class="arrow-sep">➔</div>

    <!-- Capa 2 -->
    <div class="arch-col col-gtw">
      <div class="layer-badge badge-gtw">CAPA 2</div>
      <div class="layer-title">Gateway Perimetral</div>
      <div class="layer-tech">Cloud Armor + TLS 1.3</div>
      <div class="layer-desc">Terminación SSL segura, WAF, mitigación de DDoS y enrutamiento perimetral en GCP.</div>
    </div>

    <div class="arrow-sep">➔</div>

    <!-- Capa 3 -->
    <div class="arch-col col-api">
      <div class="layer-badge badge-api">CAPA 3</div>
      <div class="layer-title">Backend API Core</div>
      <div class="layer-tech">FastAPI + Python 3.11</div>
      <div class="layer-desc">Microservicios en Cloud Run (latencia p95 < 45ms), lógica REST y tokens JWT.</div>
    </div>

    <div class="arrow-sep">➔</div>

    <!-- Downstream Stack -->
    <div class="downstream-group">
      <!-- Redis -->
      <div class="sub-card card-redis">
        <span class="sub-badge badge-c4a">CAPA 4A</span>
        <span class="sub-tech">Redis Memorystore:</span>
        <span class="sub-desc">Caché transaccional y soft-lock anti-empalme (TTL 900s)</span>
      </div>
      <!-- Postgres -->
      <div class="sub-card card-sql">
        <span class="sub-badge badge-c4b">CAPA 4B</span>
        <span class="sub-tech">Cloud SQL PostgreSQL 15:</span>
        <span class="sub-desc">Persistencia relacional ACID con respaldos automáticos diarios</span>
      </div>
      <!-- Crypto -->
      <div class="sub-card card-crypto">
        <span class="sub-badge badge-c5">CAPA 5</span>
        <span class="sub-tech">Sellado HMAC-SHA256:</span>
        <span class="sub-desc">Clave simétrica en servidor para actas digitales inmutables</span>
      </div>
    </div>
  </div>
</div>
</body>
</html>"""

os.makedirs('scratch', exist_ok=True)
os.makedirs('docs/graficos', exist_ok=True)
html_file = os.path.abspath('scratch/figura5.html')
with open(html_file, 'w', encoding='utf-8') as f:
    f.write(html_content)

chrome = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
output_img = os.path.abspath('docs/graficos/figura5_arquitectura_5capas.png')

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

print("Generando imagen de alta resolución para Figura 5 con Chrome...")
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
