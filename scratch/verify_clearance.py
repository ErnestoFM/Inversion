import pypdf

reader = pypdf.PdfReader('docs/Propuesta_Proyecto_Inversion_SIGRE.pdf')

print("=" * 80)
print("VERIFICACIÓN GEOMÉTRICA DE NO-COLISIÓN EN TODAS LAS PÁGINAS (2 A 11)")
print("Línea divisoria del encabezado ReportLab en y = 765.0 pt")
print("Texto del encabezado ReportLab en y = 769.0 pt")
print("=" * 80)

all_good = True

for page_idx in range(1, len(reader.pages)):
    page = reader.pages[page_idx]
    text_items = []
    
    def visitor(text, cm, tm, font_dict, font_size):
        t = text.strip()
        if t:
            # Calculate true y position in points from bottom of page
            # Standard PDF affine transform: y_pts = tm[5]*cm[3] + cm[5]
            y_pts = tm[5] * cm[3] + cm[5]
            text_items.append((y_pts, t))
            
    page.extract_text(visitor_text=visitor)
    
    # Filter out header string itself which is stamped on top
    body_items = [it for it in text_items if 'Propuesta de Inversión SIGRE' not in it[1] and 'Página' not in it[1]]
    if body_items:
        body_items.sort(key=lambda x: x[0], reverse=True)
        top_y, top_text = body_items[0]
        gap = 765.0 - top_y
        status = "PASÓ (ESPACIO LIMPIO)" if gap >= 12.0 else "FALLÓ (COLISIÓN)"
        if gap < 12.0:
            all_good = False
        print(f"Página {page_idx+1:2d} | Elemento superior: y = {top_y:5.1f} pt | Holgura bajo línea: {gap:4.1f} pt | {status} | '{top_text[:45]}'")

print("=" * 80)
if all_good:
    print("ÉXITO TOTAL: Ningún contenido toca, roza ni es cortado por el encabezado o la línea divisoria.")
else:
    print("ALERTA: Se detectaron colisiones o espacios insuficientes.")
print("=" * 80)
