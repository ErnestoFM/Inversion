# -*- coding: utf-8 -*-
import os
import subprocess
from PIL import Image
import numpy as np

# Dimensiones del SVG
svg_w = 820
svg_h = 220
plot_x0 = 70
plot_x1 = 790
plot_y_top = 30
plot_y_bot = 180
plot_h = plot_y_bot - plot_y_top  # 150px

min_v = -60.0
max_v = 900.0

def v_to_y(v):
    frac = (max_v - v) / (max_v - min_v)
    return plot_y_top + frac * plot_h

y_zero = v_to_y(0)

# Centros de grupos
c_x = [190, 430, 670]

# Datos
years = [
    {"label": "Año 1 (Piloto)", "sub": "3 Planteles (CUTonalá + 2 Prepas)", "ing": 63.0, "opex": 95.0, "fen": -32.0},
    {"label": "Año 2 (Crecimiento)", "sub": "8 Planteles (3 CUs + 5 Prepas)", "ing": 309.0, "opex": 225.0, "fen": 68.4},
    {"label": "Año 3 (Madurez)", "sub": "22 Planteles (8 CUs + 14 Prepas)", "ing": 840.0, "opex": 426.0, "fen": 289.8}
]

bar_w = 34

# Construir SVG
svg_elements = []

# Gridlines y etiquetas Y
y_ticks = [-50, 0, 200, 400, 600, 800]
for val in y_ticks:
    y_pos = v_to_y(val)
    is_zero = (val == 0)
    stroke = "#94a3b8" if is_zero else "#e2e8f0"
    stroke_w = "1.5" if is_zero else "1"
    dash = 'stroke-dasharray="4,3"' if not is_zero else ""
    svg_elements.append(f'<line x1="{plot_x0}" y1="{y_pos:.1f}" x2="{plot_x1}" y2="{y_pos:.1f}" stroke="{stroke}" stroke-width="{stroke_w}" {dash}/>')
    txt_weight = "bold" if is_zero else "normal"
    txt_color = "#0f172a" if is_zero else "#64748b"
    label = "$0" if val == 0 else f"${val}k" if val > 0 else f"-${abs(val)}k"
    svg_elements.append(f'<text x="{plot_x0 - 8}" y="{y_pos + 4:.1f}" font-size="9" font-family="system-ui, -apple-system, sans-serif" font-weight="{txt_weight}" fill="{txt_color}" text-anchor="end">{label}</text>')

# Barras para cada año
fen_points = []
for i, d in enumerate(years):
    cx = c_x[i]
    x_ing = cx - bar_w - 3
    x_opex = cx + 3

    # Barra Ingresos
    y_ing = v_to_y(d["ing"])
    h_ing = y_zero - y_ing
    svg_elements.append(f'<rect x="{x_ing:.1f}" y="{y_ing:.1f}" width="{bar_w}" height="{h_ing:.1f}" rx="3" fill="#2563eb" stroke="#1d4ed8" stroke-width="1"/>')
    svg_elements.append(f'<text x="{x_ing + bar_w/2:.1f}" y="{y_ing - 5:.1f}" font-size="9" font-weight="800" font-family="system-ui, -apple-system, sans-serif" fill="#1e40af" text-anchor="middle">${d["ing"]:.0f}k</text>')

    # Barra OPEX
    y_opex = v_to_y(d["opex"])
    h_opex = y_zero - y_opex
    svg_elements.append(f'<rect x="{x_opex:.1f}" y="{y_opex:.1f}" width="{bar_w}" height="{h_opex:.1f}" rx="3" fill="#f87171" stroke="#dc2626" stroke-width="1"/>')
    svg_elements.append(f'<text x="{x_opex + bar_w/2:.1f}" y="{y_opex - 5:.1f}" font-size="9" font-weight="800" font-family="system-ui, -apple-system, sans-serif" fill="#b91c1c" text-anchor="middle">${d["opex"]:.0f}k</text>')

    # FEN point
    y_fen = v_to_y(d["fen"])
    fen_points.append((cx, y_fen, d["fen"]))

    # Etiquetas eje X
    svg_elements.append(f'<text x="{cx}" y="{plot_y_bot + 16}" font-size="10.5" font-weight="800" font-family="system-ui, -apple-system, sans-serif" fill="#0f172a" text-anchor="middle">{d["label"]}</text>')
    svg_elements.append(f'<text x="{cx}" y="{plot_y_bot + 28}" font-size="8" font-weight="600" font-family="system-ui, -apple-system, sans-serif" fill="#64748b" text-anchor="middle">{d["sub"]}</text>')

# Línea FEN
pts_str = " ".join(f"{x:.1f},{y:.1f}" for x, y, _ in fen_points)
svg_elements.append(f'<polyline points="{pts_str}" fill="none" stroke="#16a34a" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>')

# Puntos FEN y badges de valor
for x, y, val in fen_points:
    svg_elements.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5" fill="#16a34a" stroke="#ffffff" stroke-width="2"/>')
    val_str = f"+${val:.1f}k" if val > 0 else f"-${abs(val):.1f}k"
    y_badge = y - 10 if val >= 0 else y + 16
    bg_badge = "#dcfce7" if val >= 0 else "#fee2e2"
    border_badge = "#86efac" if val >= 0 else "#fca5a5"
    txt_badge = "#166534" if val >= 0 else "#991b1b"
    
    # Badge flotante para FEN
    svg_elements.append(f'<rect x="{x - 24:.1f}" y="{y_badge - 10:.1f}" width="48" height="14" rx="3" fill="{bg_badge}" stroke="{border_badge}" stroke-width="1"/>')
    svg_elements.append(f'<text x="{x:.1f}" y="{y_badge + 0.5:.1f}" font-size="8.5" font-weight="900" font-family="system-ui, -apple-system, sans-serif" fill="{txt_badge}" text-anchor="middle">{val_str}</text>')

svg_body = "\n  ".join(svg_elements)

html_content = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  body {{
    margin: 0;
    padding: 10px;
    background: #ffffff;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  }}
  .container {{
    width: 860px;
    border: 1.5px solid #cbd5e1;
    border-radius: 8px;
    padding: 10px 16px;
    background: #ffffff;
    box-shadow: 0 3px 6px -1px rgba(0,0,0,0.04);
    box-sizing: border-box;
  }}
  .header-row {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 6px;
    border-bottom: 1px solid #f1f5f9;
    padding-bottom: 6px;
  }}
  .title-group {{
    flex: 1;
  }}
  .title {{
    font-size: 13px;
    font-weight: 800;
    color: #0f172a;
    letter-spacing: 0.5px;
    text-transform: uppercase;
    margin-bottom: 2px;
  }}
  .subtitle {{
    font-size: 9.5px;
    color: #64748b;
  }}
  .legend {{
    display: flex;
    gap: 12px;
    align-items: center;
  }}
  .legend-item {{
    display: flex;
    align-items: center;
    gap: 5px;
    font-size: 8.5px;
    font-weight: 700;
    color: #334155;
  }}
  .legend-box {{
    width: 11px;
    height: 11px;
    border-radius: 2.5px;
  }}
  .box-ing {{ background: #2563eb; border: 1px solid #1d4ed8; }}
  .box-opex {{ background: #f87171; border: 1px solid #dc2626; }}
  .legend-line {{
    width: 14px;
    height: 3px;
    background: #16a34a;
    position: relative;
    border-radius: 2px;
  }}
  .chart-wrapper {{
    display: flex;
    justify-content: center;
    margin-top: 4px;
  }}
</style>
</head>
<body>
<div class="container" id="capture">
  <div class="header-row">
    <div class="title-group">
      <div class="title">Evolución Financiera Trienal del Proyecto SIGRE</div>
      <div class="subtitle">Facturación Bruta, Costos Operativos (OPEX) y Flujo de Efectivo Neto (Miles MXN)</div>
    </div>
    <div class="legend">
      <div class="legend-item"><div class="legend-box box-ing"></div> Ingresos Brutos</div>
      <div class="legend-item"><div class="legend-box box-opex"></div> Costos OPEX</div>
      <div class="legend-item"><div class="legend-line"></div> FEN Neto</div>
    </div>
  </div>
  
  <div class="chart-wrapper">
    <svg width="{svg_w}" height="{svg_h}" viewBox="0 0 {svg_w} {svg_h}">
      {svg_body}
    </svg>
  </div>
</div>
</body>
</html>"""

os.makedirs('scratch', exist_ok=True)
os.makedirs('docs/graficos', exist_ok=True)
html_file = os.path.abspath('scratch/figura10.html')
with open(html_file, 'w', encoding='utf-8') as f:
    f.write(html_content)

chrome = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
output_img = os.path.abspath('docs/graficos/figura10_evolucion_financiera_trienal.png')

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

print("Generando imagen de alta resolución para Figura 10 con Chrome...")
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
