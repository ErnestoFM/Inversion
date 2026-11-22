import pypdf
from optimize_pdf_pages import build_html, test_compile

for font in [9.1, 9.2, 9.3, 9.4, 9.5]:
    for lh in [1.30, 1.32, 1.35]:
        h = build_html(font_size_pt=font, line_height=lh, margin_cm=1.45, img_max_h=195)
        pages = test_compile(h, 'scratch/test_opt.html', 'scratch/test_opt.pdf')
        print(f"font={font}, lh={lh} -> pages={pages}")
        if pages == 11:
            print(f"*** FOUND 11 PAGES: font={font}, lh={lh} ***")
            break
    if pages == 11:
        break
