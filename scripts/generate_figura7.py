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
  
  /* Estructura del organigrama */
  .tree-root {
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  .founder-card {
    background-color: #0f172a;
    color: #ffffff;
    border-radius: 6px;
    padding: 6px 18px;
    text-align: center;
    box-shadow: 0 2px 4px rgba(15, 23, 42, 0.15);
    border: 1px solid #334155;
    margin-bottom: 8px;
    position: relative;
  }
  .founder-name {
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 0.3px;
  }
  .founder-role {
    font-size: 8.5px;
    color: #94a3b8;
    font-weight: 600;
  }
  .founder-badge {
    background: #2563eb;
    color: #fff;
    font-size: 7.5px;
    font-weight: 800;
    padding: 1.5px 6px;
    border-radius: 3px;
    margin-top: 2px;
    display: inline-block;
  }

  .connector-v {
    width: 2px;
    height: 8px;
    background-color: #cbd5e1;
  }

  .connector-tree {
    display: flex;
    width: 78%;
    position: relative;
    margin-bottom: 6px;
  }
  .connector-line {
    width: 100%;
    height: 2px;
    background-color: #cbd5e1;
    position: relative;
  }

  .team-grid {
    display: flex;
    justify-content: space-between;
    gap: 12px;
    width: 100%;
  }
  .team-card {
    flex: 1;
    border-radius: 6px;
    padding: 6px 10px;
    text-align: center;
    border: 1.5px solid;
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  .card-n1 {
    background-color: #f0fdf4;
    border-color: #86efac;
  }
  .card-tc {
    background-color: #eff6ff;
    border-color: #93c5fd;
  }
  .card-cs {
    background-color: #faf5ff;
    border-color: #d8b4fe;
  }

  .card-badge {
    font-size: 7.5px;
    font-weight: 800;
    padding: 1.5px 6px;
    border-radius: 3px;
    color: #ffffff;
    margin-bottom: 3px;
  }
  .badge-n1 { background-color: #16a34a; }
  .badge-tc { background-color: #2563eb; }
  .badge-cs { background-color: #7c3aed; }

  .team-role {
    font-size: 10px;
    font-weight: 800;
    color: #1e293b;
    margin-bottom: 2px;
  }
  .team-hiring {
    font-size: 8.5px;
    font-weight: 700;
    color: #0f172a;
    margin-bottom: 2px;
  }
  .team-desc {
    font-size: 8px;
    color: #64748b;
    line-height: 1.25;
  }
</style>
</head>
<body>
<div class="container" id="capture">
  <div class="title">Organigrama Funcional y Fases de Escalamiento del Equipo</div>
  <div class="subtitle">Estructura de Capital Humano Sujeta a Metas de Facturación y Crecimiento de Planteles</div>

  <div class="tree-root">
    <!-- Nivel 1: Fundador -->
    <div class="founder-card">
      <div class="founder-name">Ernesto Hatuey Fierro Meléndez</div>
      <div class="founder-role">Fundador Único, Director General y Diseñador de Software</div>
      <div class="founder-badge">AÑO 1 • OPERACIÓN FUNDADORA ($0 NÓMINA PATRONAL)</div>
    </div>

    <!-- Conector -->
    <div class="connector-v"></div>

    <!-- Nivel 2: Equipo Escalonado -->
    <div class="team-grid">
      <!-- Soporte N1 -->
      <div class="team-card card-n1">
        <div class="card-badge badge-n1">AÑO 2 • FASE EXPANDIDA</div>
        <div class="team-role">Técnico Soporte N1</div>
        <div class="team-hiring">Contratación: Mes 15</div>
        <div class="team-desc">Gatillo: 4 planteles contratados.<br>Soporte en sitio, ventanillas y mantenimiento.</div>
      </div>

      <!-- Soporte TC -->
      <div class="team-card card-tc">
        <div class="card-badge badge-tc">AÑO 2 • MADURACIÓN OPERATIVA</div>
        <div class="team-role">Especialista Soporte TC</div>
        <div class="team-hiring">Contratación: Mes 22</div>
        <div class="team-desc">Gatillo: 8 planteles contratados.<br>Telemetría, SLA cloud y monitoreo 24/7.</div>
      </div>

      <!-- Customer Success -->
      <div class="team-card card-cs">
        <div class="card-badge badge-cs">AÑO 3 • RETENCIÓN INSTITUCIONAL</div>
        <div class="team-role">Coordinador Customer Success</div>
        <div class="team-hiring">Contratación: Mes 28</div>
        <div class="team-desc">Gatillo: 12 planteles contratados.<br>Onboarding de secretarios y retención B2G.</div>
      </div>
    </div>
  </div>
</div>
</body>
</html>"""

os.makedirs('scratch', exist_ok=True)
os.makedirs('docs/graficos', exist_ok=True)
html_file = os.path.abspath('scratch/figura7.html')
with open(html_file, 'w', encoding='utf-8') as f:
    f.write(html_content)

chrome = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
output_img = os.path.abspath('docs/graficos/figura7_organigrama_equipo.png')

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

print("Generando imagen de alta resolución para Figura 7 con Chrome...")
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
