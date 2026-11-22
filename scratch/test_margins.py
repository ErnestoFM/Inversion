# -*- coding: utf-8 -*-
import os, sys, subprocess, pypdf
from optimize_pdf_pages import build_html

def test_one(font_size=9.2, line_h=1.30, margin_cm=1.8, img_max_h=180):
    h = build_html(font_size_pt=font_size, line_height=line_h, margin_cm=margin_cm, img_max_h=img_max_h)
    abs_html = os.path.abspath('scratch/test_single.html')
    abs_pdf = os.path.abspath('scratch/test_single.pdf')
    with open(abs_html, 'w', encoding='utf-8') as f:
        f.write(h)
    chrome = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
    cmd = [chrome, '--headless=new', '--disable-gpu', '--run-all-compositor-stages-before-draw', f'--print-to-pdf={abs_pdf}', '--no-pdf-header-footer', abs_html]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if os.path.exists(abs_pdf) and os.path.getsize(abs_pdf) > 0:
        reader = pypdf.PdfReader(abs_pdf)
        print(f"Margin {margin_cm}cm, Font {font_size}pt, LH {line_h} -> PAGES: {len(reader.pages)}")
        return len(reader.pages)
    else:
        print("Failed to generate PDF")
        return -1

if __name__ == '__main__':
    for m in [1.6, 1.7, 1.8, 1.9, 2.0]:
        test_one(font_size=9.2, line_h=1.30, margin_cm=m, img_max_h=185)
