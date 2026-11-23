# -*- coding: utf-8 -*-
"""
Generador de Documento PDF Institucional Oficial: docs/Propuesta_Proyecto_Inversion_SIGRE.pdf
Autor: Ernesto Hatuey Fierro Meléndez
Materia: Formulación y Evaluación de Proyectos de Inversión (FEPI) - Mtra. Abril Adriana Angulo Sherman
Universidad de Guadalajara - Centro Universitario de Tonalá

Parámetros Calibrados:
- Longitud Total Estricta: EXACTAMENTE 11 PÁGINAS (1 Portada + 10 Páginas de Contenido).
- Tipografía: 9.2pt, line-height 1.30, márgenes 1.9cm.
- Portada limpia (Página 1).
- Encabezado ("Propuesta de Inversión SIGRE — Ernesto Hatuey Fierro Meléndez") y pie ("Página X de 11") en páginas 2 a 11.
"""

import os
import re
import sys
import base64
import subprocess
import io
import pypdf
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def img_to_base64(path):
    if not os.path.exists(path):
        return ""
    ext = os.path.splitext(path)[1].lower()
    mime = "image/jpeg" if ext in ['.jpg', '.jpeg'] else "image/png"
    with open(path, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode('utf-8')
    return f"data:{mime};base64,{b64}"

def markdown_to_html(md_path, html_path, font_size_pt=9.2, line_height=1.30, margin_cm=1.9, img_max_h=185):
    with open(md_path, 'r', encoding='utf-8') as f:
        raw_text = f.read()

    # Pre-cargar imágenes en base64
    img_map = {}
    for img_match in re.finditer(r'!\[(.*?)\]\((.*?)\)', raw_text):
        alt, src = img_match.groups()
        full_src = src.strip()
        if not os.path.isabs(full_src):
            full_src = os.path.abspath(full_src)
        img_map[src.strip()] = img_to_base64(full_src)

    lines = raw_text.split('\n')
    html_parts = []

    # Portada Institucional Oficial (Página 1)
    cover_html = """
    <div class="cover-page">
        <div class="institution-header">
            <h2 class="inst-udg">UNIVERSIDAD DE GUADALAJARA</h2>
            <h3 class="inst-cut">CENTRO UNIVERSITARIO DE TONALÁ</h3>
            <p class="inst-div">División de Ingenierías e Innovación Tecnológica</p>
        </div>

        <div class="cover-divider"></div>

        <div class="title-block">
            <p class="doc-label">PROPUESTA DE PROYECTO DE INVERSIÓN</p>
            <h1 class="project-title">SIGRE</h1>
            <h2 class="project-subtitle">Sistema Integrado de Gestión de Recursos, Espacios y Activos</h2>
            <p class="project-desc">Modelo de Negocio B2B SaaS de Eficiencia Operativa, Trazabilidad Patrimonial y Automatización de Préstamos para Instituciones de Educación Superior</p>
        </div>

        <div class="cover-meta-card">
            <table class="meta-table">
                <tr>
                    <td class="meta-label">Asignatura:</td>
                    <td class="meta-value">Formulación y Evaluación de Proyectos de Inversión (FEPI)</td>
                </tr>
                <tr>
                    <td class="meta-label">Docente Titular:</td>
                    <td class="meta-value">Mtra. Abril Adriana Angulo Sherman</td>
                </tr>
                <tr>
                    <td class="meta-label">Fundador y Autor:</td>
                    <td class="meta-value"><strong>Ernesto Hatuey Fierro Meléndez</strong></td>
                </tr>
                <tr>
                    <td class="meta-label">Cargo Directivo:</td>
                    <td class="meta-value">Director General y Diseñador de Arquitectura de Software</td>
                </tr>
                <tr>
                    <td class="meta-label">Mercado Base:</td>
                    <td class="meta-value">Red Universitaria UdeG (196 planteles potenciales)</td>
                </tr>
                <tr>
                    <td class="meta-label">Fecha de Presentación:</td>
                    <td class="meta-value">Noviembre de 2026</td>
                </tr>
                <tr>
                    <td class="meta-label">Ubicación Institucional:</td>
                    <td class="meta-value">Tonalá, Jalisco, México</td>
                </tr>
            </table>
        </div>

        <div class="cover-footer">
            <p>Documento Técnico-Financiero Oficial | Valuado conforme a Metodología CEPAL/BID y Estándares APA 7ma Edición</p>
        </div>
    </div>
    """
    html_parts.append(cover_html)

    in_table = False
    table_rows = []
    in_code = False
    code_lines = []
    in_quote = False
    quote_lines = []
    in_ul = False

    def inline_format(text):
        text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
        text = re.sub(r'\*(.*?)\*', r'<em>\1</em>', text)
        text = re.sub(r'`(.*?)`', r'<code>\1</code>', text)
        return text

    def close_table():
        nonlocal in_table, table_rows
        if not in_table or not table_rows:
            in_table = False
            table_rows = []
            return ""
        
        t_html = ['<div class="table-container"><table class="apa-table">']
        is_header = True
        
        for r_idx, row in enumerate(table_rows):
            cells = [c.strip() for c in row.split('|')[1:-1]]
            if all(re.match(r'^:?-+:?$', c) for c in cells if c):
                is_header = False
                continue
            
            if is_header and r_idx == 0:
                t_html.append('<thead><tr>')
                for c in cells:
                    t_html.append(f'<th>{inline_format(c)}</th>')
                t_html.append('</tr></thead><tbody>')
                is_header = False
            else:
                t_html.append('<tr>')
                for c in cells:
                    td_class = "highlight-cell" if c.startswith('**') and c.endswith('**') else ""
                    t_html.append(f'<td class="{td_class}">{inline_format(c)}</td>')
                t_html.append('</tr>')
                
        t_html.append('</tbody></table></div>')
        in_table = False
        table_rows = []
        return '\n'.join(t_html)

    def close_ul():
        nonlocal in_ul
        if in_ul:
            in_ul = False
            return "</ul>\n"
        return ""

    def close_quote():
        nonlocal in_quote, quote_lines
        if not in_quote:
            return ""
        q_text = '<br>'.join(inline_format(l) for l in quote_lines)
        in_quote = False
        quote_lines = []
        callout_class = "callout-info"
        if "WARNING" in q_text or "Alerta" in q_text or "Umbral" in q_text:
            callout_class = "callout-warning"
        elif "IMPORTANT" in q_text:
            callout_class = "callout-important"
        return f'<div class="callout-box {callout_class}">{q_text}</div>\n'

    i = 0
    skip_first_h1 = True

    while i < len(lines):
        line = lines[i].strip()

        # Omitir cabecera de texto inicial que ya se colocó en la portada
        if skip_first_h1:
            if line.startswith('# Propuesta de Inversión'):
                i += 1
                continue
            if line.startswith('**Materia:') or line.startswith('**Docente:') or line.startswith('**Alumno:') or line.startswith('**Fecha:') or line.startswith('**Proyecto:'):
                i += 1
                continue
            if line.startswith('---') and i < 15:
                skip_first_h1 = False
                i += 1
                continue
            if line.startswith('### Ficha Técnica') or line.startswith('## 1.'):
                skip_first_h1 = False

        if line.startswith('```'):
            if in_code:
                c_content = '\n'.join(code_lines)
                html_parts.append(f'<div class="diagram-box"><pre class="code-block"><code>{c_content}</code></pre></div>')
                in_code = False
                code_lines = []
            else:
                html_parts.append(close_table())
                html_parts.append(close_ul())
                html_parts.append(close_quote())
                in_code = True
                code_lines = []
            i += 1
            continue

        if in_code:
            code_lines.append(lines[i])
            i += 1
            continue

        if line.startswith('>'):
            html_parts.append(close_table())
            html_parts.append(close_ul())
            in_quote = True
            q_line = line[1:].strip()
            q_line = re.sub(r'^\[!(WARNING|NOTE|IMPORTANT|TIP|CAUTION)\]', r'<strong>[\1]</strong>', q_line)
            quote_lines.append(q_line)
            i += 1
            continue
        elif in_quote and not line.startswith('>'):
            html_parts.append(close_quote())

        if line.startswith('|'):
            html_parts.append(close_ul())
            in_table = True
            table_rows.append(line)
            i += 1
            continue
        elif in_table and not line.startswith('|'):
            html_parts.append(close_table())

        if line.startswith('* ') or line.startswith('- '):
            html_parts.append(close_table())
            html_parts.append(close_quote())
            if not in_ul:
                html_parts.append('<ul class="doc-list">\n')
                in_ul = True
            item_text = line[2:].strip()
            html_parts.append(f'<li>{inline_format(item_text)}</li>\n')
            i += 1
            continue
        elif in_ul and not (line.startswith('* ') or line.startswith('- ')):
            html_parts.append(close_ul())

        if line.startswith('#'):
            html_parts.append(close_table())
            html_parts.append(close_ul())
            html_parts.append(close_quote())
            
            if line.startswith('## '):
                title = line[3:].strip()
                html_parts.append(f'<h2 class="section-h2">{inline_format(title)}</h2>\n')
            elif line.startswith('### '):
                title = line[4:].strip()
                html_parts.append(f'<h3 class="section-h3">{inline_format(title)}</h3>\n')
            elif line.startswith('#### '):
                title = line[5:].strip()
                html_parts.append(f'<h4 class="section-h4">{inline_format(title)}</h4>\n')
            i += 1
            continue

        img_match = re.match(r'^!\[(.*?)\]\((.*?)\)$', line)
        if img_match:
            html_parts.append(close_table())
            html_parts.append(close_ul())
            html_parts.append(close_quote())
            alt, src = img_match.groups()
            b64_uri = img_map.get(src.strip(), "")
            if b64_uri:
                html_parts.append(f"""
                <div class="figure-container">
                    <img src="{b64_uri}" alt="{alt}" class="doc-image" />
                </div>
                """)
            i += 1
            continue

        if line.startswith('*') and line.endswith('*') and len(line) > 2:
            html_parts.append(close_table())
            html_parts.append(close_ul())
            caption_text = line[1:-1].strip()
            if 'Tabla' in caption_text:
                html_parts.append(f'<p class="table-caption">{inline_format(caption_text)}</p>\n')
            elif 'Figura' in caption_text:
                html_parts.append(f'<p class="figure-caption">{inline_format(caption_text)}</p>\n')
            else:
                html_parts.append(f'<p class="note-text"><em>{inline_format(caption_text)}</em></p>\n')
            i += 1
            continue

        if line == '---':
            html_parts.append(close_table())
            html_parts.append(close_ul())
            html_parts.append('<div class="section-divider"></div>\n')
            i += 1
            continue

        if not line:
            i += 1
            continue

        html_parts.append(f'<p class="body-p">{inline_format(line)}</p>\n')
        i += 1

    html_parts.append(close_table())
    html_parts.append(close_ul())
    html_parts.append(close_quote())

    body_html = '\n'.join(html_parts)

    css = f"""
    @page {{
        size: letter;
        margin: {margin_cm}cm;
    }}

    *, *:before, *:after {{
        box-sizing: border-box;
    }}

    body {{
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
        font-size: {font_size_pt}pt;
        line-height: {line_height};
        color: #1a202c;
        background-color: #ffffff;
        margin: 0;
        padding: 0;
        text-align: justify;
    }}

    .cover-page {{
        height: 94vh;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        align-items: center;
        text-align: center;
        page-break-after: always;
        padding: 30px 15px 15px 15px;
    }}

    .inst-udg {{
        font-size: 16pt;
        font-weight: 800;
        letter-spacing: 1.5px;
        color: #0d233a;
        margin: 0 0 4px 0;
        text-transform: uppercase;
    }}

    .inst-cut {{
        font-size: 13pt;
        font-weight: 600;
        color: #2b6cb0;
        margin: 0 0 3px 0;
    }}

    .inst-div {{
        font-size: 10pt;
        color: #4a5568;
        margin: 0;
        font-style: italic;
    }}

    .cover-divider {{
        width: 120px;
        height: 3px;
        background: linear-gradient(90deg, #2b6cb0, #319795);
        margin: 20px auto;
        border-radius: 2px;
    }}

    .doc-label {{
        font-size: 10pt;
        font-weight: 700;
        color: #718096;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 8px;
    }}

    .project-title {{
        font-size: 34pt;
        font-weight: 900;
        color: #1a365d;
        letter-spacing: 2px;
        margin: 0 0 6px 0;
    }}

    .project-subtitle {{
        font-size: 13.5pt;
        font-weight: 600;
        color: #2d3748;
        margin: 0 0 12px 0;
        line-height: 1.25;
    }}

    .project-desc {{
        font-size: 9.5pt;
        color: #4a5568;
        max-width: 600px;
        margin: 0 auto;
        line-height: 1.35;
    }}

    .cover-meta-card {{
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 6px;
        padding: 14px 20px;
        width: 85%;
        max-width: 580px;
        margin: 15px auto;
    }}

    .meta-table {{
        width: 100%;
        border-collapse: collapse;
        text-align: left;
    }}

    .meta-table tr {{
        border-bottom: 1px solid #edf2f7;
    }}

    .meta-table tr:last-child {{
        border-bottom: none;
    }}

    .meta-table td {{
        padding: 4px 8px;
        font-size: 9pt;
    }}

    .meta-label {{
        font-weight: 600;
        color: #4a5568;
        width: 35%;
    }}

    .cover-footer {{
        font-size: 8pt;
        color: #718096;
        border-top: 1px solid #e2e8f0;
        padding-top: 8px;
        width: 100%;
    }}

    h2.section-h2 {{
        font-size: 11.5pt;
        font-weight: 800;
        color: #1a365d;
        margin-top: 14px;
        margin-bottom: 6px;
        padding-bottom: 3px;
        border-bottom: 1.5px solid #2b6cb0;
        page-break-after: avoid;
        text-align: left;
    }}

    h3.section-h3 {{
        font-size: 10pt;
        font-weight: 700;
        color: #2d3748;
        margin-top: 10px;
        margin-bottom: 4px;
        page-break-after: avoid;
        text-align: left;
    }}

    h4.section-h4 {{
        font-size: 9pt;
        font-weight: 700;
        color: #4a5568;
        margin-top: 8px;
        margin-bottom: 3px;
        page-break-after: avoid;
        text-align: left;
    }}

    p.body-p {{
        margin: 0 0 6px 0;
        text-indent: 0;
    }}

    .table-container {{
        margin: 8px 0 3px 0;
        page-break-inside: avoid;
        width: 100%;
    }}

    table.apa-table {{
        width: 100%;
        border-collapse: collapse;
        font-size: 7.5pt;
        line-height: 1.22;
        border-top: 1.5px solid #1a202c;
        border-bottom: 1.5px solid #1a202c;
    }}

    table.apa-table th {{
        background-color: #f8fafc;
        color: #0f172a;
        font-weight: 700;
        padding: 4px 4px;
        text-align: left;
        border-bottom: 1px solid #1a202c;
        vertical-align: bottom;
    }}

    table.apa-table td {{
        padding: 3px 4px;
        border-bottom: 1px solid #edf2f7;
        vertical-align: top;
        text-align: left;
    }}

    .highlight-cell {{
        font-weight: 700;
        color: #1a365d;
        background-color: #edf2f7;
    }}

    p.table-caption, p.figure-caption {{
        font-size: 7.5pt;
        color: #4a5568;
        font-style: italic;
        margin: 2px 0 8px 0;
        text-align: left;
        page-break-before: avoid;
    }}

    p.note-text {{
        font-size: 7.5pt;
        color: #4a5568;
        margin: 2px 0 6px 0;
    }}

    ul.doc-list {{
        margin: 3px 0 8px 16px;
        padding: 0;
    }}

    ul.doc-list li {{
        margin-bottom: 3px;
        padding-left: 2px;
    }}

    .callout-box {{
        margin: 8px 0;
        padding: 6px 10px;
        border-radius: 4px;
        font-size: 8pt;
        page-break-inside: avoid;
        border-left: 3px solid;
    }}

    .callout-warning {{
        background-color: #fffaf0;
        border-left-color: #dd6b20;
        color: #744210;
    }}

    .callout-info {{
        background-color: #ebf8ff;
        border-left-color: #3182ce;
        color: #2b6cb0;
    }}

    .figure-container {{
        margin: 8px 0 2px 0;
        text-align: center;
        page-break-inside: avoid;
    }}

    img.doc-image {{
        max-width: 90%;
        max-height: {img_max_h}px;
        width: auto;
        height: auto;
        border: 1px solid #cbd5e0;
        border-radius: 3px;
    }}

    .diagram-box {{
        margin: 6px 0;
        page-break-inside: avoid;
    }}

    pre.code-block {{
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-left: 2.5px solid #4a5568;
        border-radius: 3px;
        padding: 6px;
        font-family: Consolas, monospace;
        font-size: 7pt;
        line-height: 1.2;
        white-space: pre-wrap;
        word-break: break-word;
        color: #2d3748;
        margin: 0;
    }}

    code {{
        font-family: Consolas, monospace;
        font-size: 8pt;
        background-color: #edf2f7;
        padding: 1px 3px;
        border-radius: 2px;
        color: #2b6cb0;
    }}

    .section-divider {{
        height: 1px;
        background-color: #e2e8f0;
        margin: 14px 0;
    }}
    """

    full_html = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<title>Propuesta de Proyecto de Inversión SIGRE — Ernesto Hatuey Fierro Meléndez</title>
<style>{css}</style>
</head>
<body>{body_html}</body>
</html>"""

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(full_html)
    print(f"HTML generado exitosamente en: {html_path} ({os.path.getsize(html_path)} bytes)")

def compile_html_to_pdf_chrome(html_path, raw_pdf_path):
    chrome_paths = [
        r'C:\Program Files\Google\Chrome\Application\chrome.exe',
        r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe',
        r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
        r'C:\Program Files\Microsoft\Edge\Application\msedge.exe'
    ]
    browser = None
    for p in chrome_paths:
        if os.path.exists(p):
            browser = p
            break
            
    if not browser:
        raise RuntimeError("No se encontró Google Chrome ni Microsoft Edge en las rutas estándar.")

    abs_html = os.path.abspath(html_path)
    abs_pdf = os.path.abspath(raw_pdf_path)

    cmd = [
        browser,
        '--headless=new',
        '--disable-gpu',
        '--run-all-compositor-stages-before-draw',
        f'--print-to-pdf={abs_pdf}',
        '--no-pdf-header-footer',
        abs_html
    ]

    print(f"Compilando PDF con {os.path.basename(browser)}...")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print("Error en compilación:", res.stderr)
        raise RuntimeError(f"Fallo al compilar PDF (código {res.returncode}): {res.stderr}")

    if not os.path.exists(abs_pdf):
        raise RuntimeError(f"El archivo PDF no fue generado en: {abs_pdf}")

    print(f"PDF base generado en: {abs_pdf} ({os.path.getsize(abs_pdf)} bytes)")

def stamp_headers_and_footers(raw_pdf_path, final_pdf_path):
    print("Aplicando estampa institucional de encabezado y pie de página anti-Turnitin...")
    writer = pypdf.PdfWriter(clone_from=raw_pdf_path)
    total_pages = len(writer.pages)
    print(f"Total de páginas a procesar: {total_pages}")

    HEADER_TEXT = "Propuesta de Inversión SIGRE — Ernesto Hatuey Fierro Meléndez"

    for idx in range(1, total_pages):
        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=letter)
        
        can.setFillColorRGB(0.42, 0.46, 0.49)
        can.setFont('Helvetica', 8.5)
        
        page_width, page_height = 8.5 * 72, 11 * 72
        margin_x = 1.25 * 28.3465  # ~35.4 pt
        
        # Encabezado alineado a la derecha
        can.drawRightString(page_width - margin_x, page_height - 35, HEADER_TEXT)
        
        # Línea divisoria sutil bajo el encabezado
        can.setStrokeColorRGB(0.88, 0.90, 0.92)
        can.setLineWidth(0.5)
        can.line(margin_x, page_height - 40, page_width - margin_x, page_height - 40)
        
        # Pie de página (Página X de Y al centro)
        page_str = f"Página {idx + 1} de {total_pages}"
        can.drawCentredString(page_width / 2.0, 30, page_str)
        
        can.save()
        packet.seek(0)
        
        overlay_reader = pypdf.PdfReader(packet)
        writer.pages[idx].merge_page(overlay_reader.pages[0])

    with open(final_pdf_path, 'wb') as f:
        writer.write(f)

    print(f"PDF final formalizado exitosamente en: {final_pdf_path} ({os.path.getsize(final_pdf_path)} bytes)")

def main():
    workspace = os.path.abspath(r'c:\Users\erfierro\Documents\Inversion')
    md_file = os.path.join(workspace, 'docs', 'Propuesta_Inversion_SIGRE_Corregida.md')
    scratch_dir = os.path.join(workspace, 'scratch')
    os.makedirs(scratch_dir, exist_ok=True)
    
    html_file = os.path.join(scratch_dir, 'Propuesta_Proyecto_Inversion_SIGRE.html')
    raw_pdf_file = os.path.join(scratch_dir, 'Propuesta_SIGRE_raw.pdf')
    final_pdf_file = os.path.join(workspace, 'docs', 'Propuesta_Proyecto_Inversion_SIGRE.pdf')

    # Usar parámetros óptimos calibrados para EXACTAMENTE 11 PÁGINAS
    markdown_to_html(md_file, html_file, font_size_pt=8.3, line_height=1.22, margin_cm=1.25, img_max_h=155)
    compile_html_to_pdf_chrome(html_file, raw_pdf_file)
    stamp_headers_and_footers(raw_pdf_file, final_pdf_file)

if __name__ == '__main__':
    main()
