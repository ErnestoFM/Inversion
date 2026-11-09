import os
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.drawing.image import Image as OpenpyxlImage

def create_cost_excel():
    wb = openpyxl.Workbook()
    # Estilos globales
    font_title = Font(name="Calibri", size=14, bold=True, color="1E3A8A")
    font_subtitle = Font(name="Calibri", size=11, italic=True, color="475569")
    font_section = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    font_bold = Font(name="Calibri", size=10, bold=True, color="0F172A")
    font_regular = Font(name="Calibri", size=10, color="0F172A")
    font_footnote = Font(name="Calibri", size=8.5, italic=True, color="64748B")
    
    fill_navy = PatternFill(start_color="1E3A8A", end_color="1E3A8A", fill_type="solid")
    fill_blue = PatternFill(start_color="2563EB", end_color="2563EB", fill_type="solid")
    fill_header = PatternFill(start_color="E2E8F0", end_color="E2E8F0", fill_type="solid")
    fill_highlight_green = PatternFill(start_color="DCFCE7", end_color="DCFCE7", fill_type="solid")
    fill_highlight_yellow = PatternFill(start_color="FEF08A", end_color="FEF08A", fill_type="solid")
    fill_highlight_soft_blue = PatternFill(start_color="DBEAFE", end_color="DBEAFE", fill_type="solid")
    fill_alert_red = PatternFill(start_color="FEE2E2", end_color="FEE2E2", fill_type="solid")

    thin_border_side = Side(border_style="thin", color="CBD5E1")
    double_bottom_side = Side(border_style="double", color="0F172A")
    thick_top_side = Side(border_style="medium", color="0F172A")
    
    border_cell = Border(left=thin_border_side, right=thin_border_side, top=thin_border_side, bottom=thin_border_side)
    border_total = Border(left=thin_border_side, right=thin_border_side, top=thick_top_side, bottom=double_bottom_side)

    align_center = Alignment(horizontal="center", vertical="center")
    align_left = Alignment(horizontal="left", vertical="center")
    align_right = Alignment(horizontal="right", vertical="center")

    num_fmt_curr = "$#,##0.00"
    num_fmt_curr_int = "$#,##0"
    num_fmt_pct = "0.0%"

    # =========================================================================
    # HOJA 1: MODELO DE COSTOS Y PRECIOS (PLANTILLA OFICIAL PROFESORA)
    # =========================================================================
    ws1 = wb.active
    ws1.title = "Modelo de Costos y Precios"
    ws1.views.sheetView[0].showGridLines = True

    # Encabezado institucional
    ws1["A1"] = "UNIVERSIDAD DE GUADALAJARA | CENTRO UNIVERSITARIO DE TONALÁ"
    ws1["A1"].font = Font(name="Calibri", size=11, bold=True, color="64748B")
    
    ws1["A2"] = "DETERMINACIÓN DEL COSTO DE UN PRODUCTO O SERVICIO — PLATAFORMA SIGRE"
    ws1["A2"].font = font_title
    
    ws1["A3"] = "Alumno: Fierro Meléndez Ernesto Hatuey | Docente: Mtra. Abril Adriana Angulo Sherman | Materia: Formulación y Evaluación de Proyectos"
    ws1["A3"].font = font_subtitle

    # --- BLOQUE 1: MATERIA PRIMA / INSUMOS TECNOLÓGICOS (LOTE 100 UNIDADES) ---
    ws1["A5"] = "Materia prima / Insumos TI"
    ws1["A5"].font = Font(name="Calibri", size=11, bold=True, color="1E3A8A")
    ws1["B5"] = "100 pzas / dependencias"
    ws1["B5"].font = Font(name="Calibri", size=10, bold=True, color="2563EB")

    mp_headers = ["Concepto", "Unidades", "CUnitario (sin iva)", "CTotal(+IVA)", "IVA"]
    for col_idx, h in enumerate(mp_headers, start=1):
        cell = ws1.cell(row=6, column=col_idx, value=h)
        cell.font = font_section
        cell.fill = fill_navy
        cell.alignment = align_center
        cell.border = border_cell

    mp_data = [
        ("A (Instancias Cloud Run Compute)", 2, 500.0, "=B7*C7*1.16", "=D7-B7*C7"),
        ("B (Base de Datos Cloud SQL PostgreSQL)", 1, 900.0, "=B8*C8*1.16", "=D8-B8*C8"),
        ("C (Almacenamiento Cloud Storage)", 2, 250.0, "=B9*C9*1.16", "=D9-B9*C9"),
        ("D (API Mensajería Transaccional)", 1, 266.666667, "=B10*C10*1.16", "=D10-B10*C10")
    ]

    for r_idx, row in enumerate(mp_data, start=7):
        ws1.cell(row=r_idx, column=1, value=row[0]).alignment = align_left
        ws1.cell(row=r_idx, column=2, value=row[1]).alignment = align_center
        ws1.cell(row=r_idx, column=3, value=row[2]).number_format = num_fmt_curr_int
        ws1.cell(row=r_idx, column=4, value=row[3]).number_format = num_fmt_curr
        ws1.cell(row=r_idx, column=5, value=row[4]).number_format = num_fmt_curr
        for c in range(1, 6):
            ws1.cell(row=r_idx, column=c).border = border_cell
            ws1.cell(row=r_idx, column=c).font = font_regular

    # Totales Materia Prima
    ws1["A11"] = "Total Insumos Directos"
    ws1["A11"].font = font_bold
    ws1["C11"] = "=SUM(B7*C7, B8*C8, B9*C9, B10*C10)"
    ws1["C11"].number_format = num_fmt_curr_int
    ws1["C11"].font = font_bold
    ws1["D11"] = "=SUM(D7:D10)"
    ws1["D11"].number_format = num_fmt_curr
    ws1["D11"].font = font_bold
    ws1["D11"].fill = fill_highlight_yellow
    ws1["E11"] = "=SUM(E7:E10)"
    ws1["E11"].number_format = num_fmt_curr
    ws1["E11"].font = font_bold
    for c in range(1, 6):
        ws1.cell(row=11, column=c).border = border_total

    # --- BLOQUE 2: MANO DE OBRA DIRECTA (MENSUAL) ---
    ws1["A13"] = "Mano de obra directa (Ingeniería y Soporte Cloud)"
    ws1["A13"].font = Font(name="Calibri", size=11, bold=True, color="1E3A8A")

    mo_headers = ["Puesto / Rol", "Personal", "Sueldo", "CTotal", ""]
    for col_idx, h in enumerate(mo_headers[:4], start=1):
        cell = ws1.cell(row=14, column=col_idx, value=h)
        cell.font = font_section
        cell.fill = fill_navy
        cell.alignment = align_center
        cell.border = border_cell

    mo_data = [
        ("Ingeniero DevOps / SysAdmin Cloud (0.5 EJC)", 0.5, 13000.0, "=B15*C15"),
        ("Técnico QA / Soporte L2 a Planteles (0.5 EJC)", 0.5, 8666.666667, "=B16*C16")
    ]

    for r_idx, row in enumerate(mo_data, start=15):
        ws1.cell(row=r_idx, column=1, value=row[0]).alignment = align_left
        ws1.cell(row=r_idx, column=2, value=row[1]).alignment = align_center
        ws1.cell(row=r_idx, column=2, value=row[1]).number_format = "0.0"
        ws1.cell(row=r_idx, column=3, value=row[2]).number_format = num_fmt_curr_int
        ws1.cell(row=r_idx, column=4, value=row[3]).number_format = num_fmt_curr
        for c in range(1, 5):
            ws1.cell(row=r_idx, column=c).border = border_cell
            ws1.cell(row=r_idx, column=c).font = font_regular

    ws1["A17"] = "Total Mano de Obra"
    ws1["A17"].font = font_bold
    ws1["D17"] = "=SUM(D15:D16)"
    ws1["D17"].number_format = num_fmt_curr
    ws1["D17"].font = font_bold
    ws1["D17"].fill = fill_highlight_yellow
    for c in range(1, 5):
        ws1.cell(row=17, column=c).border = border_total

    # --- BLOQUE 3: COSTOS INDIRECTOS DE FABRICACIÓN / SERVICIOS OPERATIVOS ---
    ws1["A19"] = "Costos Indirectos y Servicios de Operación"
    ws1["A19"].font = Font(name="Calibri", size=11, bold=True, color="1E3A8A")

    cif_headers = ["Concepto", "Unidades", "CUnitario", "CTotal", ""]
    for col_idx, h in enumerate(cif_headers[:4], start=1):
        cell = ws1.cell(row=20, column=col_idx, value=h)
        cell.font = font_section
        cell.fill = fill_navy
        cell.alignment = align_center
        cell.border = border_cell

    cif_data = [
        ("Servicios de Conectividad, Monitoreo y Oficina Técnica", 1, 2500.0, "=B21*C21"),
        ("Cumplimiento Normativo (INDAUTOR + Auditoría LGPDPPSO)", 1, 1833.333333, "=B22*C22")
    ]

    for r_idx, row in enumerate(cif_data, start=21):
        ws1.cell(row=r_idx, column=1, value=row[0]).alignment = align_left
        ws1.cell(row=r_idx, column=2, value=row[1]).alignment = align_center
        ws1.cell(row=r_idx, column=3, value=row[2]).number_format = num_fmt_curr_int
        ws1.cell(row=r_idx, column=4, value=row[3]).number_format = num_fmt_curr
        for c in range(1, 5):
            ws1.cell(row=r_idx, column=c).border = border_cell
            ws1.cell(row=r_idx, column=c).font = font_regular

    ws1["A23"] = "Total Costos Indirectos y Cumplimiento"
    ws1["A23"].font = font_bold
    ws1["D23"] = "=SUM(D21:D22)"
    ws1["D23"].number_format = num_fmt_curr
    ws1["D23"].font = font_bold
    ws1["D23"].fill = fill_highlight_yellow
    for c in range(1, 5):
        ws1.cell(row=23, column=c).border = border_total

    # --- BLOQUE 4: DETERMINACIÓN DEL COSTO TOTAL Y UNITARIO ---
    ws1["A25"] = "INTEGRACIÓN DEL COSTO TOTAL MENSUAL (LOTE 100 DEPENDENCIAS)"
    ws1["A25"].font = Font(name="Calibri", size=11, bold=True, color="1E3A8A")

    int_headers = ["Elemento de Costo", "", "", "Monto Mensual", "% Total"]
    for col_idx, h in enumerate(int_headers, start=1):
        if col_idx in (1, 4, 5):
            cell = ws1.cell(row=26, column=col_idx, value=h)
            cell.font = font_section
            cell.fill = fill_navy
            cell.alignment = align_center
            cell.border = border_cell

    cost_elements = [
        ("Materia Prima / Insumos TI Directos (+IVA)", "=D11", "=D27/D30"),
        ("Mano de Obra Directa (Ingeniería DevOps/QA)", "=D17", "=D28/D30"),
        ("Costos Indirectos y Cumplimiento Regulatorio", "=D23", "=D29/D30")
    ]

    for r_idx, elem in enumerate(cost_elements, start=27):
        ws1.cell(row=r_idx, column=1, value=elem[0]).alignment = align_left
        ws1.cell(row=r_idx, column=4, value=elem[1]).number_format = num_fmt_curr
        ws1.cell(row=r_idx, column=4).alignment = align_right
        ws1.cell(row=r_idx, column=5, value=elem[2]).number_format = num_fmt_pct
        ws1.cell(row=r_idx, column=5).alignment = align_center
        for c in (1, 2, 3, 4, 5):
            ws1.cell(row=r_idx, column=c).border = border_cell
            ws1.cell(row=r_idx, column=c).font = font_regular

    ws1["A30"] = "COSTO TOTAL MENSUAL DEL LOTE (100 DEPENDENCIAS)"
    ws1["A30"].font = font_bold
    ws1["D30"] = "=SUM(D27:D29)"
    ws1["D30"].number_format = num_fmt_curr
    ws1["D30"].font = font_bold
    ws1["D30"].fill = fill_highlight_green
    ws1["E30"] = "=SUM(E27:E29)"
    ws1["E30"].number_format = num_fmt_pct
    ws1["E30"].font = font_bold
    for c in (1, 2, 3, 4, 5):
        ws1.cell(row=30, column=c).border = border_total

    ws1["A31"] = "Unidades del Lote (Dependencias Universitarias)"
    ws1["D31"] = 100
    ws1["D31"].number_format = "#,##0"
    ws1["D31"].alignment = align_right

    ws1["A32"] = "COSTO UNITARIO POR DEPENDENCIA (MENSUAL)"
    ws1["A32"].font = font_bold
    ws1["D32"] = "=D30/D31"
    ws1["D32"].number_format = num_fmt_curr
    ws1["D32"].font = font_bold
    ws1["D32"].fill = fill_highlight_soft_blue
    for c in (1, 2, 3, 4, 5):
        ws1.cell(row=32, column=c).border = border_total

    # --- BLOQUE 5: DETERMINACIÓN DEL PRECIO DE VENTA Y MARGEN ---
    ws1["A34"] = "DETERMINACIÓN DEL PRECIO DE VENTA INSTITUCIONAL (MARKUP 2.5X)"
    ws1["A34"].font = Font(name="Calibri", size=11, bold=True, color="1E3A8A")

    pricing_data = [
        ("Costo Unitario de Producción Mensual (sin IVA)", "=D32", num_fmt_curr),
        ("Margen de Ganancia Bruto Deseado (%)", 0.60, num_fmt_pct),
        ("PRECIO DE VENTA SUGERIDO MENSUAL (sin IVA)", "=D35/(1-D36)", num_fmt_curr),
        ("IVA Trasladado (16%)", "=D37*0.16", num_fmt_curr),
        ("PRECIO DE VENTA MENSUAL FINAL CON IVA", "=D37+D38", num_fmt_curr),
        ("Licencia Anualizada por Dependencia (12 meses sin IVA)", "=D37*12", num_fmt_curr),
        ("TARIFA ANUAL DE LICENCIA CONTRATADA SIGRE (NETA)", 28950.0, num_fmt_curr)
    ]

    for r_idx, p_item in enumerate(pricing_data, start=35):
        ws1.cell(row=r_idx, column=1, value=p_item[0]).alignment = align_left
        ws1.cell(row=r_idx, column=4, value=p_item[1]).number_format = p_item[2]
        ws1.cell(row=r_idx, column=4).alignment = align_right
        for c in (1, 2, 3, 4, 5):
            ws1.cell(row=r_idx, column=c).border = border_cell
            ws1.cell(row=r_idx, column=c).font = font_regular
        if r_idx in (37, 39, 41):
            ws1.cell(row=r_idx, column=1).font = font_bold
            ws1.cell(row=r_idx, column=4).font = font_bold
            if r_idx == 41:
                ws1.cell(row=r_idx, column=4).fill = fill_highlight_green

    # Ajuste de anchos
    col_widths_ws1 = {"A": 52, "B": 14, "C": 22, "D": 22, "E": 18}
    for col, width in col_widths_ws1.items():
        ws1.column_dimensions[col].width = width

    # =========================================================================
    # HOJA 2: ECONOMÍA DE ESCALA Y PUNTO DE EQUILIBRIO
    # =========================================================================
    ws2 = wb.create_sheet(title="Economía de Escala y PE")
    ws2.views.sheetView[0].showGridLines = True

    ws2["A1"] = "ANÁLISIS DE ECONOMÍAS DE ESCALA Y PUNTO DE EQUILIBRIO OPERATIVO"
    ws2["A1"].font = font_title
    ws2["A2"] = "Comportamiento del costo unitario y punto de equilibrio en función del volumen de dependencias"
    ws2["A2"].font = font_subtitle

    # --- TABLA A: CURVA DE COSTOS UNITARIOS POR ESCALA ---
    ws2["A4"] = "A. CURVA DE COSTOS SEGÚN ESCALA DE DEPENDENCIAS ACTIVAS (MENSUAL)"
    ws2["A4"].font = Font(name="Calibri", size=11, bold=True, color="1E3A8A")

    h_escala = ["Volumen (Deps)", "Costo Fijo (CF)", "Costo Var. (CV)", "Costo Total (CT)", "Costo Unitario", "Ingreso (P=$456.50)", "Resultado Operativo"]
    cols_escala = ["A", "B", "C", "D", "E", "F", "G"]
    for c, h in zip(cols_escala, h_escala):
        cell = ws2[f"{c}5"]
        cell.value = h
        cell.font = font_section
        cell.fill = fill_navy
        cell.alignment = align_center
        cell.border = border_cell

    escalas_vol = [1, 5, 10, 20, 35, 50, 75, 100, 150, 193]
    for idx, vol in enumerate(escalas_vol, start=6):
        ws2[f"A{idx}"] = vol
        ws2[f"A{idx}"].alignment = align_center
        ws2[f"B{idx}"] = 15166.67
        ws2[f"C{idx}"] = f"=A{idx}*26.666667"
        ws2[f"D{idx}"] = f"=B{idx}+C{idx}"
        ws2[f"E{idx}"] = f"=D{idx}/A{idx}"
        ws2[f"F{idx}"] = f"=A{idx}*456.50"
        ws2[f"G{idx}"] = f"=F{idx}-D{idx}"

        for c in ["B", "C", "D", "E", "F", "G"]:
            ws2[f"{c}{idx}"].number_format = num_fmt_curr
            ws2[f"{c}{idx}"].alignment = align_right

        for c in cols_escala:
            ws2[f"{c}{idx}"].border = border_cell
            ws2[f"{c}{idx}"].font = font_regular

        if vol == 35:
            for c in cols_escala:
                ws2[f"{c}{idx}"].fill = fill_highlight_yellow
                ws2[f"{c}{idx}"].font = font_bold
        elif vol == 100:
            for c in cols_escala:
                ws2[f"{c}{idx}"].fill = fill_highlight_soft_blue
                ws2[f"{c}{idx}"].font = font_bold

    # --- TABLA B: FÓRMULA DEL PUNTO DE EQUILIBRIO ---
    ws2["A18"] = "B. DETERMINACIÓN MATEMÁTICA DEL PUNTO DE EQUILIBRIO OPERATIVO"
    ws2["A18"].font = Font(name="Calibri", size=11, bold=True, color="1E3A8A")

    pe_params = [
        ("Costos Fijos Mensuales Totales (CF)", 15166.67, num_fmt_curr, "Nómina ($10,833.33) + Servicios ($2,500) + Legal ($1,833.33)"),
        ("Precio de Venta Unitario Mensual (P)", 456.50, num_fmt_curr, "Tarifa mensual neta por dependencia contratada"),
        ("Costo Variable Unitario Mensual (CVU)", 26.67, num_fmt_curr, "Consumo Cloud Run y Storage por dependencia"),
        ("Margen de Contribución Unitario (MCU = P - CVU)", "=B20-B21", num_fmt_curr, "Contribución marginal por cada dependencia nueva"),
        ("Razón de Margen de Contribución (MCU / P)", "=B22/B20", num_fmt_pct, "Porcentaje de cada peso de ingreso disponible para cubrir CF"),
        ("PUNTO DE EQUILIBRIO EN UNIDADES (Q_PE = CF / MCU)", "=B19/B22", "0.0", "Dependencias requeridas para cubrir exactamente costos"),
        ("PUNTO DE EQUILIBRIO EN DEPENDENCIAS (REDONDEADO)", "=ROUNDUP(B24, 0)", "#,##0", "Meta mínima comercial para zona de beneficio"),
        ("PUNTO DE EQUILIBRIO EN VENTAS MENSUALES ($)", "=B25*B20", num_fmt_curr, "Facturación mensual neta requerida"),
        ("PUNTO DE EQUILIBRIO EN VENTAS ANUALES ($)", "=B26*12", num_fmt_curr, "Facturación anual neta en punto de equilibrio")
    ]

    for idx, param in enumerate(pe_params, start=19):
        ws2[f"A{idx}"] = param[0]
        ws2[f"B{idx}"] = param[1]
        ws2[f"B{idx}"].number_format = param[2]
        ws2[f"C{idx}"] = param[3]
        ws2[f"A{idx}"].alignment = align_left
        ws2[f"B{idx}"].alignment = align_right
        ws2[f"C{idx}"].alignment = align_left
        ws2[f"A{idx}"].border = border_cell
        ws2[f"B{idx}"].border = border_cell
        ws2[f"C{idx}"].border = border_cell
        ws2[f"A{idx}"].font = font_regular
        ws2[f"B{idx}"].font = font_regular
        ws2[f"C{idx}"].font = font_footnote

        if idx in (24, 25, 26):
            ws2[f"A{idx}"].font = font_bold
            ws2[f"B{idx}"].font = font_bold
            ws2[f"B{idx}"].fill = fill_highlight_green

    col_widths_ws2 = {"A": 44, "B": 20, "C": 20, "D": 20, "E": 20, "F": 22, "G": 22}
    for col, width in col_widths_ws2.items():
        ws2.column_dimensions[col].width = width

    # =========================================================================
    # HOJA 3: CRITERIOS Y ANÁLISIS DE PARETO (80/20)
    # =========================================================================
    ws3 = wb.create_sheet(title="Criterios y Pareto")
    ws3.views.sheetView[0].showGridLines = True

    ws3["A1"] = "ANÁLISIS DE CRITERIOS DE COSTO Y CLASIFICACIÓN ABC (PARETO 80/20)"
    ws3["A1"].font = font_title
    ws3["A2"] = "Ponderación multicriterio de las partidas de gasto mensual para el lote de 100 dependencias"
    ws3["A2"].font = font_subtitle

    h_pareto = ["Partida de Costo", "Monto Mensual", "% del Total", "% Acumulado", "Zona ABC", "Criticidad Operativa", "Sensibilidad al Volumen"]
    cols_pareto = ["A", "B", "C", "D", "E", "F", "G"]
    for c, h in zip(cols_pareto, h_pareto):
        cell = ws3[f"{c}4"]
        cell.value = h
        cell.font = font_section
        cell.fill = fill_navy
        cell.alignment = align_center
        cell.border = border_cell

    pareto_data = [
        ("Capital Humano Directo (Ingeniería DevOps y Soporte QA)", 10833.33, "=B5/$B$9", "=C5", "Zona A (Vital)", "Máxima (SLA 99.5%)", "Baja (Costo Fijo)"),
        ("Insumos de Tecnología TI (Servidores Cloud GCP + IVA)", 3093.33, "=B6/$B$9", "=D5+C6", "Zona A (Vital)", "Alta (24/7 Nube)", "Alta (Escala con tráfico)"),
        ("Servicios de Conectividad, Enlaces y Oficina Técnica", 2500.0, "=B7/$B$9", "=D6+C7", "Zona B (Técnica)", "Media (Soporte local)", "Baja (Gasto base)"),
        ("Cumplimiento Normativo (LGPDPPSO y Registro INDAUTOR)", 1833.33, "=B8/$B$9", "=D7+C8", "Zona C (Legal)", "Alta (Blindaje legal)", "Nula (Amortizado)")
    ]

    for idx, row in enumerate(pareto_data, start=5):
        ws3[f"A{idx}"] = row[0]
        ws3[f"B{idx}"] = row[1]
        ws3[f"C{idx}"] = row[2]
        ws3[f"D{idx}"] = row[3]
        ws3[f"E{idx}"] = row[4]
        ws3[f"F{idx}"] = row[5]
        ws3[f"G{idx}"] = row[6]

        ws3[f"A{idx}"].alignment = align_left
        ws3[f"B{idx}"].number_format = num_fmt_curr
        ws3[f"B{idx}"].alignment = align_right
        ws3[f"C{idx}"].number_format = num_fmt_pct
        ws3[f"C{idx}"].alignment = align_center
        ws3[f"D{idx}"].number_format = num_fmt_pct
        ws3[f"D{idx}"].alignment = align_center
        ws3[f"E{idx}"].alignment = align_center
        ws3[f"F{idx}"].alignment = align_left
        ws3[f"G{idx}"].alignment = align_left

        for c in cols_pareto:
            ws3[f"{c}{idx}"].border = border_cell
            ws3[f"{c}{idx}"].font = font_regular

        if idx in (5, 6):
            ws3[f"E{idx}"].fill = fill_highlight_yellow
            ws3[f"E{idx}"].font = font_bold
        elif idx == 7:
            ws3[f"E{idx}"].fill = fill_highlight_soft_blue
        elif idx == 8:
            ws3[f"E{idx}"].fill = fill_header

    ws3["A9"] = "TOTAL COSTO MENSUAL DEL LOTE"
    ws3["A9"].font = font_bold
    ws3["B9"] = "=SUM(B5:B8)"
    ws3["B9"].number_format = num_fmt_curr
    ws3["B9"].font = font_bold
    ws3["C9"] = "=SUM(C5:C8)"
    ws3["C9"].number_format = num_fmt_pct
    ws3["C9"].font = font_bold
    ws3["D9"] = "100.0%"
    ws3["D9"].font = font_bold
    ws3["D9"].alignment = align_center
    for c in cols_pareto:
        ws3[f"{c}9"].border = border_total

    col_widths_ws3 = {"A": 48, "B": 18, "C": 14, "D": 16, "E": 18, "F": 24, "G": 24}
    for col, width in col_widths_ws3.items():
        ws3.column_dimensions[col].width = width

    # =========================================================================
    # HOJA 4: CUANTIFICACIÓN DEL PROBLEMA Y BENCHMARKING COMPETITIVO
    # =========================================================================
    ws4 = wb.create_sheet(title="Cuantificación y Benchmarking")
    ws4.views.sheetView[0].showGridLines = True

    ws4["A1"] = "EVALUACIÓN CUANTITATIVA DEL DOLOR OPERATIVO Y BENCHMARKING COMPETITIVO"
    ws4["A1"].font = font_title
    ws4["A2"] = "Cuantificación de mermas/horas-hombre vs. ahorro con SIGRE y análisis comparativo de mercado"
    ws4["A2"].font = font_subtitle

    # --- TABLA A: CUANTIFICACIÓN DEL IMPACTO EN UN CENTRO UNIVERSITARIO PROMEDIO (CUTonalá / CUCEI) ---
    ws4["A4"] = "A. CUANTIFICACIÓN ANUAL DEL PROBLEMA (PROCESO MANUAL CON VALES DE PAPEL VS. SIGRE)"
    ws4["A4"].font = Font(name="Calibri", size=11, bold=True, color="1E3A8A")

    h_quant = ["Parámetro Operativo / Financiero Analizado", "Gestión Manual (Vales de Papel)", "Gestión Digital con SIGRE", "Impacto / Ahorro Generado", "Rango de Certeza / Fuente"]
    cols_quant = ["A", "B", "C", "D", "E"]
    for c, h in zip(cols_quant, h_quant):
        cell = ws4[f"{c}5"]
        cell.value = h
        cell.font = font_section
        cell.fill = fill_navy
        cell.alignment = align_center
        cell.border = border_cell

    quant_data = [
        ("Transacciones diarias de préstamo promedio (ventanillas de laboratorio)", 300, 300, "Mismo volumen atendido", "Muestreo en CUTonalá / CUCEI"),
        ("Días hábiles promedio por ciclo académico anual", 200, 200, "Calendario escolar oficial", "Calendario General UdeG"),
        ("Total anual de solicitudes de préstamo tramitadas", "=B6*B7", "=C6*C7", "60,000 transacciones anuales", "Proyección operacional base"),
        ("Tiempo promedio invertido por transacción de ventanilla (minutos)", 4.5, 0.45, "-4.05 min (-90.0% de reducción)", "Cronometraje en almacén"),
        ("Horas-hombre totales consumidas al año en ventanilla", "=(B8*B9)/60", "=(C8*C9)/60", "4,050 horas-hombre liberadas", "Cálculo derivado"),
        ("Costo laboral promedio por hora (personal operativo/técnico UdeG)", 110.0, 110.0, "Costo estándar tabular con prestaciones", "Tabulador salarial UdeG 2024"),
        ("Costo anual de nómina absorbido en burocracia de vales", "=B10*B11", "=C10*C11", "$445,500.00 MXN en tiempo recuperado", "Horas x Costo por hora"),
        ("Mermas y extravíos anuales de instrumental/equipo no devuelto", 240000.0, 12000.0, "$228,000.00 MXN mitigados (95% control)", "Histórico almacén (5% inventario)"),
        ("Gasto anual en papelería física (vales impresos, carpetas, tóner)", 16500.0, 0.0, "$16,500.00 MXN ahorro en insumos", "Presupuesto de compras de insumos"),
        ("COSTO TOTAL ANUAL DE INEFICIENCIA Y PÉRDIDA POR PLANTEL", "=SUM(B12:B14)", "=SUM(C12:C14)", "=$B$15-$C$15", "Fuga operativa total anual"),
        ("Tasa de Prácticas de Laboratorio Afectadas (TPSR)", "14.5% de sesiones", "< 1.5% de sesiones", "Reducción 89.7% afectación formativa", "Muestreo en CUTonalá (CACEI)"),
        ("Costo de Adopción Anual de Licencia SIGRE (1 Almacén Central)", 0.0, 28950.0, "-$28,950.00 MXN inversión anual", "Tarifa SaaS anual SIGRE"),
        ("BENEFICIO NETO ANUAL GENERADO AL CENTRO UNIVERSITARIO", "=-B15", "=D15-C17", "$661,050.00 MXN beneficio neto", "ROI Operativo: 2,283% | Payback: 15 días")
    ]

    for idx, row in enumerate(quant_data, start=6):
        ws4[f"A{idx}"] = row[0]
        ws4[f"A{idx}"].alignment = align_left
        ws4[f"A{idx}"].font = font_regular
        ws4[f"B{idx}"] = row[1]
        ws4[f"C{idx}"] = row[2]
        ws4[f"D{idx}"] = row[3]
        ws4[f"E{idx}"] = row[4]

        for c in ["B", "C"]:
            if idx in (6, 7, 8):
                ws4[f"{c}{idx}"].number_format = "#,##0" if idx == 8 else "0"
                ws4[f"{c}{idx}"].alignment = align_center
            elif idx in (9,):
                ws4[f"{c}{idx}"].number_format = "0.0"
                ws4[f"{c}{idx}"].alignment = align_center
            elif idx in (10,):
                ws4[f"{c}{idx}"].number_format = "#,##0"
                ws4[f"{c}{idx}"].alignment = align_center
            elif idx in (11, 12, 13, 14, 15, 17, 18):
                ws4[f"{c}{idx}"].number_format = num_fmt_curr
                ws4[f"{c}{idx}"].alignment = align_right
            elif idx == 16:
                ws4[f"{c}{idx}"].alignment = align_center

        ws4[f"D{idx}"].alignment = align_right if idx in (12, 13, 14, 15, 17, 18) else align_center
        ws4[f"E{idx}"].alignment = align_left

        for c in cols_quant:
            ws4[f"{c}{idx}"].border = border_cell
            ws4[f"{c}{idx}"].font = font_regular

        if idx in (15, 18):
            ws4[f"A{idx}"].font = font_bold
            ws4[f"B{idx}"].font = font_bold
            ws4[f"C{idx}"].font = font_bold
            ws4[f"D{idx}"].font = font_bold
            if idx == 15:
                ws4[f"B{idx}"].fill = fill_alert_red
                ws4[f"D{idx}"].fill = fill_highlight_yellow
            elif idx == 18:
                ws4[f"C{idx}"].fill = fill_highlight_green
                ws4[f"D{idx}"].fill = fill_highlight_green
                for c in cols_quant:
                    ws4[f"{c}{idx}"].border = border_total

    # --- TABLA B: BENCHMARKING COMPETITIVO DE MERCADO ---
    ws4["A21"] = "B. ESTUDIO DE MERCADO Y BENCHMARKING COMPETITIVO (SIGRE VS. ALTERNATIVAS)"
    ws4["A21"].font = Font(name="Calibri", size=11, bold=True, color="1E3A8A")

    h_bench = ["Criterio / Factor Clave", "SIGRE (Propuesta)", "ERP Corporativo (SAP Ariba / Oracle)", "Software Comercial (Odoo / Zoho)", "Gestión Artesanal (Excel / Papel)"]
    cols_bench = ["A", "B", "C", "D", "E"]
    for c, h in zip(cols_bench, h_bench):
        cell = ws4[f"{c}22"]
        cell.value = h
        cell.font = font_section
        cell.fill = fill_blue
        cell.alignment = align_center
        cell.border = border_cell

    bench_data = [
        ("Costo Anual de Licenciamiento por Dependencia", "$28,950 MXN netos", "$220,000 - $480,000 MXN", "$65,000 - $110,000 MXN", "$0 MXN (Aparente)"),
        ("Costo y Tiempo de Implementación / Setup", "Inmediato (<1 semana, SaaS)", "6 a 12 meses ($350,000+ consultoría)", "2 a 3 meses ($45,000 setup)", "Inmediato (sin gobierno ni soporte)"),
        ("Mecanismo de Contratación Pública en UdeG", "Adjudicación Directa (<$200k Art. 55)", "Licitación Pública Nacional Obligatoria", "Licitación / Invitación Restringida", "No aplica"),
        ("Cumplimiento Normativo LGPDPPSO (Jalisco)", "100% Nativo (Auditoría ITEI / Sujetos Obligados)", "Requiere desarrollos y add-ons costosos", "Parcial (Enfoque comercial privado)", "Nulo (Infracción flagrante por datos expuestos)"),
        ("Algoritmo Predictivo de Scoring de Fiabilidad", "Sí (Calificación dinámica de riesgo del alumno)", "No nativo (Requiere módulo BI a la medida)", "No disponible en versión estándar", "No existe"),
        ("Modo Operativo Offline en Ventanilla (Contingencia)", "Sí (PWA con Service Worker + IndexedDB)", "No (Dependencia estricta de red corporativa)", "Parcial (App móvil no optimizada a ventanilla)", "Papel (Inmune a red, pero sin trazabilidad)"),
        ("Tiempo Promedio de Despacho en Horas Pico", "< 30 segundos (Escaneo QR credencial)", "2 a 3 minutos (Navegación en módulos ERP)", "1 a 2 minutos", "4 a 5 minutos (Llenado y firma de vale)"),
        ("Enfoque y Adaptabilidad al Entorno Universitario", "Específico para almacenes y talleres UdeG", "Cadenas de suministro transnacionales", "PyME comercial y venta al menudeo", "Artesanal e inseguro"),
        ("Propuesta de Valor Única / Barrera de Entrada", "Scoring + LGPDPPSO + Compras Menores UdeG", "Ecosistema corporativo integrado", "Ecosistema modular de bajo costo", "Costo financiero directo cero")
    ]

    for idx, row in enumerate(bench_data, start=23):
        for c_idx, col in enumerate(cols_bench):
            cell = ws4[f"{col}{idx}"]
            cell.value = row[c_idx]
            cell.border = border_cell
            cell.font = font_regular
            if col == "A":
                cell.alignment = align_left
                cell.font = font_bold
            elif col == "B":
                cell.alignment = align_center
                cell.fill = fill_highlight_soft_blue
                cell.font = Font(name="Calibri", size=9.5, bold=True, color="1E3A8A")
            else:
                cell.alignment = align_center

    # --- TABLA C: MÉTRICAS COMERCIALES Y SOCIALES (CAC Y TASA TPSR) ---
    ws4["A34"] = "C. MÉTRICAS COMERCIALES Y SOCIALES (CAC INSTITUCIONAL Y TASA TPSR DE PRÁCTICAS)"
    ws4["A34"].font = Font(name="Calibri", size=11, bold=True, color="1E3A8A")

    h_cac = ["Dimensión / Indicador Clave", "Métrica Cuantitativa", "Horizonte / Escala", "Impacto Operativo / Retorno"]
    cols_cac = ["A", "B", "C", "D"]
    for c, h in zip(cols_cac, h_cac):
        cell = ws4[f"{c}35"]
        cell.value = h
        cell.font = font_section
        cell.fill = fill_navy
        cell.alignment = align_center
        cell.border = border_cell

    cac_rows = [
        ("Costo de Adquisición de Clientes (CAC) Institucional", "$5,000.00 MXN", "Por campus / dependencia", "25 hrs ingeniería ($3,750) + viáticos/traslados ($1,250)"),
        ("Valor de Vida del Cliente (Customer Lifetime Value - LTV)", "$86,850.00 MXN", "3 años x $28,950/año", "Facturación neta recurrente por módulo"),
        ("Ratio LTV / CAC Institucional", "17.37x", "Amortización en 2.1 meses", "Supera holgadamente el estándar de capital de riesgo (>3.0x)"),
        ("Línea Base Tasa de Prácticas Afectadas (TPSR)", "14.5% semestral", "Diagnóstico empírico CUTonalá", "Sesiones suspendidas o hacinamiento de 4-5 alumnos por equipo"),
        ("Meta TPSR con Plataforma SIGRE", "< 1.5% semestral", "Reducción del 89.7%", "Eliminación de colisiones, reserva predictiva y blindaje CACEI")
    ]

    for idx, row in enumerate(cac_rows, start=36):
        ws4[f"A{idx}"] = row[0]
        ws4[f"B{idx}"] = row[1]
        ws4[f"C{idx}"] = row[2]
        ws4[f"D{idx}"] = row[3]
        ws4[f"A{idx}"].alignment = align_left
        ws4[f"B{idx}"].alignment = align_center
        ws4[f"C{idx}"].alignment = align_center
        ws4[f"D{idx}"].alignment = align_left
        for col_l in cols_cac:
            ws4[f"{col_l}{idx}"].border = border_cell
            ws4[f"{col_l}{idx}"].font = font_regular
        if idx in (38, 40):
            ws4[f"A{idx}"].font = font_bold
            ws4[f"B{idx}"].font = font_bold
            ws4[f"B{idx}"].fill = fill_highlight_green

    col_widths_ws4 = {"A": 48, "B": 24, "C": 26, "D": 34, "E": 36}
    for col, width in col_widths_ws4.items():
        ws4.column_dimensions[col].width = width

    # =========================================================================
    # HOJA 5: MATRIZ DE MARCO LÓGICO (MML)
    # =========================================================================
    ws5 = wb.create_sheet(title="Marco Lógico (MML)")
    ws5.views.sheetView[0].showGridLines = True

    ws5["A1"] = "MATRIZ DE MARCO LÓGICO (MML) DEL PROYECTO SIGRE — METODOLOGÍA CEPAL / ILPES"
    ws5["A1"].font = font_title
    ws5["A2"] = "Estructura formal de formulación, objetivos, indicadores verificables y supuestos de sostenibilidad"
    ws5["A2"].font = font_subtitle

    h_mml = ["Nivel de Jerarquía de Objetivos", "Resumen Narrativo de Objetivos", "Indicadores Objetivamente Verificables (IOV)", "Medios de Verificación (MoV)", "Supuestos Críticos de Sostenibilidad"]
    cols_mml = ["A", "B", "C", "D", "E"]
    for c, h in zip(cols_mml, h_mml):
        cell = ws5[f"{c}4"]
        cell.value = h
        cell.font = font_section
        cell.fill = fill_navy
        cell.alignment = align_center
        cell.border = border_cell

    mml_data = [
        ("FIN",
         "Contribuir a la modernización tecnológica, transparencia en la rendición de cuentas públicas y optimización del gasto operativo en la gestión de materiales, reactivos y equipos en la Red Universitaria de la Universidad de Guadalajara.",
         "1. Tasa de pérdida o extravío de activos reducida a menos del 0.5% en planteles participantes al término del Año 3.\n2. Reducción del 85% en tiempos de espera de alumnos en ventanillas de laboratorios a nivel Red.\n3. Reducción de la TPSR a <1.5% semestral.",
         "Dictámenes telemétricos y reportes de discrepancia cero generados nativamente por SIGRE; actas de cierre semestral de inventario firmadas por las Coordinaciones de Laboratorio de los campus.",
         "La política de la UdeG mantiene prioridad en cero papel y digitalización. (Mitigación ante recortes: El ROI acelerado de $661k de ahorro neto frente a $28k de costo con payback de 15 días posiciona a SIGRE como medida de austeridad operativa que blinda el proyecto)."),
        ("PROPÓSITO",
         "Optimizar los procesos de solicitud, validación de riesgo, despacho y devolución de inventario en almacenes y ventanillas de centros universitarios (Piloto CUTonalá, expansión a CUCEI y red).",
         "1. Tiempo promedio de despacho por vale menor a 30 segundos en el 98% de transacciones.\n2. 100% de los préstamos cuentan con trazabilidad criptográfica y score de riesgo asignado al solicitante al cierre del Año 1.",
         "Métricas telemétricas de Cloud SQL / BigQuery; reportes mensuales de operación generados automáticamente por SIGRE; bitácoras de auditoría de despacho.",
         "Coordinadores y laboratoristas aplican la plataforma con disciplina. (Mitigación: Talleres de 30 min, red de laboratoristas campeones y deslinde legal de responsabilidades patrimoniales con firma digital neutralizan la resistencia de base)."),
        ("COMPONENTES (PRODUCTOS)",
         "C1. Plataforma Web SaaS multi-tenant en Google Cloud Platform (Cloud Run + PostgreSQL Cloud SQL + Secret Manager).\nC2. Algoritmo predictivo de Scoring de Fiabilidad del Solicitante.\nC3. Interfaz de Ventanilla PWA con capacidad de operación en modo offline y sincronización asíncrona.\nC4. Programa integral de Capacitación, Gobernanza de Datos (LGPDPPSO) y Manuales de Operación.",
         "1. Disponibilidad de la plataforma de 99.5% mensual (SLA Cloud Run).\n2. Capacidad de operación offline local de hasta 4 horas continuas sin conexión a internet.\n3. 100% de encargados de ventanilla y jefes de almacén de centros piloto acreditados en el uso del sistema.",
         "Dashboard de monitoreo de Google Cloud Monitoring; reportes de pruebas de carga y estrés k6; actas de acreditación de talleres de capacitación y entrega de manuales.",
         "La infraestructura de Google Cloud Platform mantiene su estándar de estabilidad y el personal operativo muestra adaptabilidad a herramientas digitales."),
        ("ACTIVIDADES",
         "A1. Arquitectura de microservicios y despliegue CI/CD en GCP (M1-M2).\nA2. Desarrollo del motor de scoring y Progressive Web App con Service Workers (M3-M4).\nA3. Pruebas QA, pentesting OWASP y auditoría LGPDPPSO (M5-M6).\nA4. Registro software INDAUTOR y Visto Bueno SUTUdeG (M6).\nA5. Despliegue piloto en almacenes y talleres de CUTonalá (M7).\nA6. Capacitación presencial y marcha blanca con supervisión en sitio (M8-M9).\nA7. Auditoría técnica, medición de KPIs y release v1.5 para expansión a CUCEI (M10-M12).",
         "1. Inversión ejecutada conforme al cronograma de $120,000 MXN en Año 1.\n2. 100% de los hitos técnicos concluidos en los plazos acordados.\n3. Certificado de INDAUTOR y Dictamen de Pentesting obtenidos en Mes 6.",
         "Repositorio de código GitHub con tags de release firmados; comprobante oficial de registro ante INDAUTOR; listas de asistencia a talleres y minuta sindical firmada.",
         "Los recursos de capital semilla se desembolsan oportunamente y los centros universitarios autorizan el acceso físico y operativo a almacenes para la implementación.")
    ]

    for idx, row in enumerate(mml_data, start=5):
        ws5[f"A{idx}"] = row[0]
        ws5[f"A{idx}"].alignment = align_center
        ws5[f"A{idx}"].font = font_bold
        ws5[f"A{idx}"].fill = fill_highlight_soft_blue

        for col_idx, col in enumerate(["B", "C", "D", "E"], start=1):
            cell = ws5[f"{col}{idx}"]
            cell.value = row[col_idx]
            cell.alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)
            cell.font = font_regular
            cell.border = border_cell
        ws5[f"A{idx}"].border = border_cell
        ws5.row_dimensions[idx].height = 110

    # Bloque de Gobernanza y Revisión Trimestral
    ws5["A10"] = "PROTOCOLO DE GOBERNANZA Y REVISIÓN PERIÓDICA TRIMESTRAL DE LA MML (AÑO 1):"
    ws5["A10"].font = font_bold
    ws5["A11"] = "Se establece un Comité Técnico de Seguimiento Operativo que sesionará trimestralmente (Q1, Q2, Q3 y Q4 del Año 1). Los Indicadores Objetivamente Verificables (IOV) se auditan automáticamente mediante consultas telemétricas en Google Cloud SQL y reportes nativos de SIGRE. Si se detecta una desviación superior al 5.0% en tiempos de despacho (>30 s) o mermas (>0.5%), se activan ajustes prioritarios en el siguiente sprint de mantenimiento y refuerzo de capacitación en ventanilla."
    ws5["A11"].font = font_footnote
    ws5["A11"].alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
    ws5.row_dimensions[11].height = 40

    col_widths_ws5 = {"A": 18, "B": 42, "C": 38, "D": 38, "E": 38}
    for col, width in col_widths_ws5.items():
        ws5.column_dimensions[col].width = width

    # =========================================================================
    # HOJA 6: CRONOGRAMA DE EJECUCIÓN (GANTT) Y ABSORCIÓN DE INVERSIÓN AÑO 1
    # =========================================================================
    ws6 = wb.create_sheet(title="Cronograma e Inversión Año 1")
    ws6.views.sheetView[0].showGridLines = True

    ws6["A1"] = "CRONOGRAMA DETALLADO DE EJECUCIÓN (DIAGRAMA DE GANTT) Y ABSORCIÓN DE CAPITAL — AÑO 1"
    ws6["A1"].font = font_title
    ws6["A2"] = "Programación mensual de hitos críticos: Desarrollo, QA, Trámite INDAUTOR, Piloto CUTonalá y Capacitación (Meses 1 a 12)"
    ws6["A2"].font = font_subtitle

    h_gantt = ["Fase / Actividad Crítica", "Responsable Operativo", "M1", "M2", "M3", "M4", "M5", "M6", "M7", "M8", "M9", "M10", "M11", "M12", "Presupuesto Partida"]
    cols_gantt = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O"]
    for c, h in zip(cols_gantt, h_gantt):
        cell = ws6[f"{c}4"]
        cell.value = h
        cell.font = font_section
        cell.fill = fill_navy
        cell.alignment = align_center
        cell.border = border_cell

    gantt_data = [
        ("1. Arquitectura Cloud GCP y Microservicios Base (Cloud Run, PostgreSQL)", "Lead DevOps", [1,1,0,0,0,0,0,0,0,0,0,0], 24000.0),
        ("2. Motor Algorítmico de Scoring de Riesgo y PWA Offline con Service Workers", "Dev Full-Stack", [0,0,1,1,0,0,0,0,0,0,0,0], 25000.0),
        ("3. QA, Estrés k6, Pentesting OWASP Top 10 y Auditoría LGPDPPSO", "QA Engineer", [0,0,0,0,1,1,0,0,0,0,0,0], 12000.0),
        ("4. Hito Legal: Registro INDAUTOR (Buffer 3s) y V.B. Sindical SUTUdeG", "Asesor Jurídico / PM", [0,0,0,0,0,1,0,0,0,0,0,0], 5500.0),
        ("5. Despliegue Piloto en CUTonalá (Almacén Central y Laboratorios)", "DevOps + Soporte", [0,0,0,0,0,0,1,0,0,0,0,0], 11500.0),
        ("6. Programa de Capacitación Presencial a Almacenistas y Talleres", "Customer Success / Soporte", [0,0,0,0,0,0,0,1,1,0,0,0], 10000.0),
        ("7. Marcha Blanca, KPIs y Firma Acta Entrega-Recepción M9 (Buffer 2s)", "Soporte L2", [0,0,0,0,0,0,0,0,1,1,1,0], 16500.0),
        ("8. Evaluación de Impacto, Release v1.5 y Preparación Expansión a CUCEI", "Equipo Completo", [0,0,0,0,0,0,0,0,0,0,0,1], 15500.0)
    ]

    for idx, row in enumerate(gantt_data, start=5):
        ws6[f"A{idx}"] = row[0]
        ws6[f"A{idx}"].alignment = align_left
        ws6[f"A{idx}"].font = font_regular
        ws6[f"B{idx}"] = row[1]
        ws6[f"B{idx}"].alignment = align_center
        ws6[f"B{idx}"].font = font_regular

        months = row[2]
        for m_idx, active in enumerate(months):
            col_letter = get_column_letter(3 + m_idx)
            cell = ws6[f"{col_letter}{idx}"]
            if active == 1:
                cell.value = "●"
                cell.fill = fill_highlight_soft_blue
                cell.font = Font(name="Calibri", size=11, bold=True, color="1E3A8A")
            else:
                cell.value = ""
            cell.alignment = align_center
            cell.border = border_cell

        ws6[f"O{idx}"] = row[3]
        ws6[f"O{idx}"].number_format = num_fmt_curr
        ws6[f"O{idx}"].alignment = align_right
        ws6[f"O{idx}"].font = font_regular
        ws6[f"O{idx}"].border = border_cell
        ws6[f"A{idx}"].border = border_cell
        ws6[f"B{idx}"].border = border_cell

    # Fila total inversión
    ws6["A13"] = "ABSORCIÓN PRESUPUESTAL MENSUAL ESTIMADA (MXN)"
    ws6["A13"].font = font_bold
    ws6["B13"] = "Total por Mes"
    ws6["B13"].font = font_bold
    ws6["B13"].alignment = align_center

    monthly_spending = [12000.0, 12000.0, 12500.0, 12500.0, 12000.0, 5500.0, 11500.0, 5000.0, 10500.0, 5500.0, 5500.0, 15500.0]
    for m_idx, spend in enumerate(monthly_spending):
        col_letter = get_column_letter(3 + m_idx)
        cell = ws6[f"{col_letter}{13}"]
        cell.value = spend
        cell.number_format = num_fmt_curr_int
        cell.alignment = align_center
        cell.font = font_bold
        cell.fill = fill_header
        cell.border = border_total

    ws6["O13"] = "=SUM(O5:O12)"
    ws6["O13"].number_format = num_fmt_curr
    ws6["O13"].font = font_bold
    ws6["O13"].fill = fill_highlight_green
    ws6["O13"].border = border_total
    ws6["A13"].border = border_total
    ws6["B13"].border = border_total

    # Notas operativas del Gantt
    ws6["A15"] = "NOTAS SOBRE MITIGACIÓN Y HITOS FORMALES EN GANTT:"
    ws6["A15"].font = font_bold
    ws6["A16"] = "• Mes 6: Se completa el registro INDAUTOR (Buffer 3 sem), la auditoría de ciberseguridad con Pentesting OWASP Top 10 y la Minuta de Visto Bueno Sindical con el SUTUdeG."
    ws6["A16"].font = font_footnote
    ws6["A17"] = "• Mes 9: Firma del Acta Oficial de Entrega-Recepción y Dictamen de Marcha Blanca por Coordinadores del CUTonalá, autorizando formalmente la expansión a CUCEI."
    ws6["A17"].font = font_footnote

    col_widths_ws6 = {"A": 44, "B": 24, "C": 8, "D": 8, "E": 8, "F": 8, "G": 8, "H": 8, "I": 8, "J": 8, "K": 8, "L": 8, "M": 8, "N": 8, "O": 22}
    for col, width in col_widths_ws6.items():
        ws6.column_dimensions[col].width = width

    # =========================================================================
    # HOJA 7: ESTADO DE RESULTADOS PROYECTADO PRO FORMA (3 AÑOS)
    # =========================================================================
    ws7 = wb.create_sheet(title="Estado de Resultados Pro Forma")
    ws7.views.sheetView[0].showGridLines = True

    ws7["A1"] = "ESTADO DE RESULTADOS PROYECTADO PRO FORMA — HORIZONTE A 3 AÑOS (MXN)"
    ws7["A1"].font = font_title
    ws7["A2"] = "Proyección contable bajo supuestos de adopción escalonada: Piloto CUTonalá (Año 1), Expansión CUCEI (Año 2) y Consolidación Red (Año 3)"
    ws7["A2"].font = font_subtitle
    ws7["A3"] = "Cláusula contractual: Tarifa de $28,950 MXN y nómina técnica indexadas anualmente conforme al INPC (4.5% - 5.0%), blindando márgenes netos >50%"
    ws7["A3"].font = Font(name="Calibri", size=9, italic=True, color="2563EB")

    h_er = ["Concepto Contable / Financiero", "Año 1 (Piloto CUTonalá - 5 deps)", "Año 2 (Expansión CUCEI - 25 deps)", "Año 3 (Consolidación Red - 100 deps)", "Notas Técnicas y Criterios Contables"]
    cols_er = ["A", "B", "C", "D", "E"]
    for c, h in zip(cols_er, h_er):
        cell = ws7[f"{c}4"]
        cell.value = h
        cell.font = font_section
        cell.fill = fill_navy
        cell.alignment = align_center
        cell.border = border_cell

    er_rows = [
        ("Dependencias Universitarias Contratadas", 5, 25, 100, "Almacenes y laboratorios de centros universitarios"),
        ("Precio de Venta Anual por Dependencia (sin IVA)", 28950.0, 28950.0, 28950.0, "Tarifa fija anualizada ($2,412.50 MXN / mes neto)"),
        ("INGRESOS BRUTOS OPERACIONALES", "=B5*B6", "=C5*C6", "=D5*D6", "Facturación por servicios SaaS institucional"),
        ("Descuentos y Devoluciones Comerciales (0%)", 0.0, 0.0, 0.0, "Contratación directa anual fija"),
        ("INGRESOS NETOS OPERACIONALES", "=B7-B8", "=C7-C8", "=D7-D8", "Base gravable neta operacional"),
        ("Costo del Servicio / Servidores Cloud GCP (Costo Variable)", 6120.0, 30600.0, 122400.0, "Consumo de Cloud Run, Cloud SQL, Storage ($102 MXN/dep/mes x12)"),
        ("UTILIDAD BRUTA", "=B9-B10", "=C9-C10", "=D9-D10", "Margen de contribución total"),
        ("Margen Bruto (%)", "=B11/B9", "=C11/C9", "=D11/D9", "Margen bruto SaaS típicamente >90%"),
        ("GASTOS DE OPERACIÓN Y ADMINISTRACIÓN:", "", "", "", "Costos fijos operacionales y talento humano"),
        ("  • Nómina y Honorarios Técnicos (DevOps, QA, Soporte N1/N2)", 126000.0, 252000.0, 540000.0, "Evolución de organigrama: 2 perfiles A1 -> 3 A2 -> 5 A3"),
        ("  • Conectividad, Licencias de Desarrollo y Oficina Técnica", 18000.0, 36000.0, 72000.0, "Herramientas de monitoreo, repositorios y oficina"),
        ("  • Viáticos, Talleres y Capacitación Presencial en Campus", 8500.0, 22000.0, 45000.0, "Onboarding y sesiones prácticas en almacenes"),
        ("  • Trámites Legales, Contabilidad y Registro INDAUTOR", 5500.0, 12000.0, 25000.0, "Registro de software en A1, compliance legal continuo"),
        ("TOTAL GASTOS DE OPERACIÓN", "=SUM(B14:B17)", "=SUM(C14:C17)", "=SUM(D14:D17)", "Total OPEX anual"),
        ("UTILIDAD DE OPERACIÓN / EBITDA", "=B11-B18", "=C11-C18", "=D11-D18", "Flujo operacional antes de impuestos"),
        ("Margen Operativo (%)", "=B19/B9", "=C19/C9", "=D19/D9", "Rentabilidad sobre ventas brutas"),
        ("Impuesto Sobre la Renta (ISR Estimado 30%)", "=IF(B19>0, B19*0.30, 0)", "=IF(C19>0, C19*0.30, 0)", "=IF(D19>0, D19*0.30, 0)", "Tasa corporativa estándar (sin base gravable en déficit)"),
        ("UTILIDAD (PÉRDIDA) NETA PROYECTADA", "=B19-B21", "=C19-C21", "=D19-D21", "Resultado neto contable del ejercicio"),
        ("Margen Neto (%)", "=B22/B9", "=C22/C9", "=D22/D9", "Rentabilidad neta contable"),
        ("(-) Fondo de Reserva para Reinversión Tecnológica (5% U.B.)", 0.0, "=C11*0.05", "=D11*0.05", "Provisión estatutaria para refactorización de código y modernización cloud"),
        ("UTILIDAD NETA RETENIDA / DISTRIBUIBLE", "=B22-B24", "=C22-C24", "=D22-D24", "Excedente financiero neto libre después de reservas tecnológicas"),
        ("Margen Neto Final Retenido (%)", "=B25/B9", "=C25/C9", "=D25/D9", "Rentabilidad neta final retenida en tesorería")
    ]

    for idx, row in enumerate(er_rows, start=5):
        ws7[f"A{idx}"] = row[0]
        ws7[f"A{idx}"].alignment = align_left
        ws7[f"B{idx}"] = row[1]
        ws7[f"C{idx}"] = row[2]
        ws7[f"D{idx}"] = row[3]
        ws7[f"E{idx}"] = row[4]
        ws7[f"E{idx}"].alignment = align_left
        ws7[f"E{idx}"].font = font_footnote

        for col in ["B", "C", "D"]:
            cell = ws7[f"{col}{idx}"]
            if idx == 5:
                cell.number_format = "#,##0"
                cell.alignment = align_center
            elif idx in (6, 7, 8, 9, 10, 11, 14, 15, 16, 17, 18, 19, 21, 22, 24, 25):
                cell.number_format = num_fmt_curr
                cell.alignment = align_right
            elif idx in (12, 20, 23, 26):
                cell.number_format = num_fmt_pct
                cell.alignment = align_center

        for c in cols_er:
            ws7[f"{c}{idx}"].border = border_cell
            ws7[f"{c}{idx}"].font = font_regular

        if idx in (7, 9, 11, 18, 19, 22, 25):
            ws7[f"A{idx}"].font = font_bold
            ws7[f"B{idx}"].font = font_bold
            ws7[f"C{idx}"].font = font_bold
            ws7[f"D{idx}"].font = font_bold
            if idx == 11:
                ws7[f"B{idx}"].fill = fill_highlight_soft_blue
                ws7[f"C{idx}"].fill = fill_highlight_soft_blue
                ws7[f"D{idx}"].fill = fill_highlight_soft_blue
            elif idx == 19:
                ws7[f"B{idx}"].fill = fill_alert_red
                ws7[f"C{idx}"].fill = fill_highlight_yellow
                ws7[f"D{idx}"].fill = fill_highlight_green
            elif idx == 22:
                ws7[f"B{idx}"].fill = fill_alert_red
                ws7[f"C{idx}"].fill = fill_highlight_yellow
                ws7[f"D{idx}"].fill = fill_highlight_green
            elif idx == 25:
                ws7[f"B{idx}"].fill = fill_alert_red
                ws7[f"C{idx}"].fill = fill_highlight_yellow
                ws7[f"D{idx}"].fill = fill_highlight_green
                for c in cols_er:
                    ws7[f"{c}{idx}"].border = border_total

    col_widths_ws7 = {"A": 48, "B": 24, "C": 24, "D": 26, "E": 46}
    for col, width in col_widths_ws7.items():
        ws7.column_dimensions[col].width = width

    # =========================================================================
    # HOJA 8: FLUJO DE EFECTIVO MENSUAL PRO FORMA (CASH FLOW AÑO 1)
    # =========================================================================
    ws8 = wb.create_sheet(title="Flujo de Efectivo Mensual")
    ws8.views.sheetView[0].showGridLines = True

    ws8["A1"] = "PRESUPUESTO DE FLUJO DE EFECTIVO MENSUAL (CASH FLOW) — AÑO 1 PILOTO CUTONALÁ (MXN)"
    ws8["A1"].font = font_title
    ws8["A2"] = "Monitoreo mensual de liquidez, tasa de quema (burn rate), capital de trabajo ($120k) y superávit"
    ws8["A2"].font = font_subtitle

    h_cf = ["Concepto de Tesorería", "M1", "M2", "M3", "M4", "M5", "M6", "M7", "M8", "M9", "M10", "M11", "M12", "Total Año 1"]
    cols_cf = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N"]
    for c, h in zip(cols_cf, h_cf):
        cell = ws8[f"{c}4"]
        cell.value = h
        cell.font = font_section
        cell.fill = fill_navy
        cell.alignment = align_center
        cell.border = border_cell

    # Entradas de efectivo
    ws8["A5"] = "Saldo Inicial de Caja"
    ws8["A5"].font = font_bold
    ws8["B5"] = 0.0

    ws8["A6"] = "ENTRADAS DE EFECTIVO:"
    ws8["A6"].font = Font(name="Calibri", size=10, bold=True, color="1E3A8A")
    ws8["A7"] = "  • Aportación Capital Semilla Inicial"
    ws8["B7"] = 120000.0
    for col_l in ["C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M"]:
        ws8[f"{col_l}7"] = 0.0
    ws8["N7"] = "=SUM(B7:M7)"

    ws8["A8"] = "  • Cobranza Facturación Piloto (5 deps x $28,950 + 16% IVA)"
    for col_l in ["B", "C", "D", "E", "F", "G"]:
        ws8[f"{col_l}8"] = 0.0
    ws8["H8"] = 167910.0
    for col_l in ["I", "J", "K", "L", "M"]:
        ws8[f"{col_l}8"] = 0.0
    ws8["N8"] = "=SUM(B8:M8)"

    ws8["A9"] = "TOTAL ENTRADAS DE EFECTIVO"
    ws8["A9"].font = font_bold
    for col_l in cols_cf[1:]:
        ws8[f"{col_l}9"] = f"=SUM({col_l}7:{col_l}8)"
        ws8[f"{col_l}9"].font = font_bold
        ws8[f"{col_l}9"].fill = fill_highlight_soft_blue

    # Salidas de efectivo
    ws8["A10"] = "SALIDAS DE EFECTIVO (OPEX):"
    ws8["A10"].font = Font(name="Calibri", size=10, bold=True, color="1E3A8A")

    salidas_det = [
        ("  • Servidores Nube GCP (Cloud Run, SQL, Storage con IVA)", [102.0]*6 + [510.0]*6),
        ("  • Nómina y Honorarios Técnicos (DevOps y Soporte QA)", [10500.0]*12),
        ("  • Conectividad, Licencias de Desarrollo y Oficina Técnica", [1500.0]*12),
        ("  • Viáticos, Traslados y Talleres Presenciales en Planteles", [0.0, 0.0, 500.0, 500.0, 0.0, 0.0, 1500.0, 1000.0, 2000.0, 1000.0, 1000.0, 1000.0]),
        ("  • Gastos Regulatorios, INDAUTOR y Dictamen LGPDPPSO", [0.0, 0.0, 0.0, 0.0, 0.0, 2500.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3000.0])
    ]

    for s_idx, (s_name, s_vals) in enumerate(salidas_det, start=11):
        ws8[f"A{s_idx}"] = s_name
        for m_i, val in enumerate(s_vals):
            c_letter = get_column_letter(2 + m_i)
            ws8[f"{c_letter}{s_idx}"] = val
        ws8[f"N{s_idx}"] = f"=SUM(B{s_idx}:M{s_idx})"

    ws8["A16"] = "TOTAL SALIDAS DE EFECTIVO"
    ws8["A16"].font = font_bold
    for col_l in cols_cf[1:]:
        ws8[f"{col_l}16"] = f"=SUM({col_l}11:{col_l}15)"
        ws8[f"{col_l}16"].font = font_bold
        ws8[f"{col_l}16"].fill = fill_alert_red

    # Flujo neto y saldo final
    ws8["A17"] = "FLUJO NETO DEL MES (Entradas - Salidas)"
    ws8["A17"].font = font_bold
    for col_l in cols_cf[1:]:
        ws8[f"{col_l}17"] = f"={col_l}9-{col_l}16"
        ws8[f"{col_l}17"].font = font_bold

    ws8["A18"] = "SALDO FINAL EN CAJA"
    ws8["A18"].font = font_bold
    ws8["B18"] = "=B5+B17"
    for col_idx in range(3, 14):
        curr_col = get_column_letter(col_idx)
        prev_col = get_column_letter(col_idx - 1)
        ws8[f"{curr_col}5"] = f"={prev_col}18"
        ws8[f"{curr_col}18"] = f"={curr_col}5+{curr_col}17"
    ws8["N18"] = "=M18"

    # Formatos de tabla Cash Flow
    for r in range(5, 19):
        for col_l in cols_cf:
            cell = ws8[f"{col_l}{r}"]
            cell.border = border_cell
            if col_l != "A":
                cell.number_format = num_fmt_curr_int
                cell.alignment = align_right
            else:
                cell.alignment = align_left

        if r in (9, 16, 17, 18):
            for col_l in cols_cf:
                ws8[f"{col_l}{r}"].border = border_total
            if r == 18:
                for col_l in cols_cf[1:]:
                    ws8[f"{col_l}18"].fill = fill_highlight_green
                    ws8[f"{col_l}18"].font = font_bold

    col_widths_ws8 = {"A": 44, "B": 13, "C": 13, "D": 13, "E": 13, "F": 13, "G": 13, "H": 13, "I": 13, "J": 13, "K": 13, "L": 13, "M": 13, "N": 15}
    for col, width in col_widths_ws8.items():
        ws8.column_dimensions[col].width = width

    # =========================================================================
    # HOJA 9: ANÁLISIS DE SENSIBILIDAD Y RESILIENCIA DE TESORERÍA
    # =========================================================================
    ws9 = wb.create_sheet(title="Análisis de Sensibilidad")
    ws9.views.sheetView[0].showGridLines = True

    ws9["A1"] = "ANÁLISIS DE SENSIBILIDAD FINANCIERA Y ESTRÉS DE TESORERÍA — PROYECTO SIGRE"
    ws9["A1"].font = font_title
    ws9["A2"] = "Simulación de resiliencia: Escenario Base, Pesimista Cambiario (+15% GCP) y Pesimista Comercial (Retraso 4 meses de cobranza)"
    ws9["A2"].font = font_subtitle

    # --- TABLA A: MATRIZ DE COMPARACIÓN DE ESCENARIOS AÑO 1 ---
    ws9["A4"] = "A. COMPARACIÓN DE ESCENARIOS DE ESTRÉS OPERATIVO Y FINANCIERO (AÑO 1)"
    ws9["A4"].font = Font(name="Calibri", size=11, bold=True, color="1E3A8A")

    h_sens = ["Parámetro Financiero / Métrica Clave", "Escenario Base (Esperado)", "Escenario Pesimista Cambiario (+15% GCP)", "Escenario Pesimista Comercial (Retraso 4 Meses)", "Evaluación de Resiliencia / Diagnóstico"]
    cols_sens = ["A", "B", "C", "D", "E"]
    for c_i, h in zip(cols_sens, h_sens):
        cell = ws9[f"{c_i}5"]
        cell.value = h
        cell.font = font_section
        cell.fill = fill_navy
        cell.alignment = align_center
        cell.border = border_cell

    sens_rows = [
        ("Dependencias Contratadas en Año 1", "5 dependencias", "5 dependencias", "5 dependencias", "Mismo alcance piloto CUTonalá"),
        ("Mes de Cobranza Efectiva de Contratos", "Mes 7 (Arranque Piloto)", "Mes 7 (Arranque Piloto)", "Mes 11 (Retraso de 4 meses de firmas)", "Estrés de morosidad administrativa universitaria"),
        ("Ingresos Totales con IVA Año 1", "$167,910.00", "$167,910.00", "$167,910.00", "Facturación íntegra de 5 dependencias contratadas"),
        ("Costo Anual Infraestructura Cloud GCP", "$6,120.00", "$7,038.00", "$6,120.00", "+15% por paridad peso/dólar en Google Cloud"),
        ("Margen Bruto de Servicio (%)", "95.8%", "95.1%", "95.8%", "Impacto marginal que no compromete rentabilidad"),
        ("Gastos Operativos Fijos y Trámites", "$145,440.00", "$145,440.00", "$145,440.00", "Nóminas técnicas y registro de obra INDAUTOR"),
        ("Total Egresos Operativos Año 1", "$151,560.00", "$152,478.00", "$151,560.00", "Incremento máximo de $918 MXN en todo el año"),
        ("Tasa de Quema de Efectivo (Burn Rate Pre-op)", "$12,583.33 / mes", "$12,660.00 / mes", "$12,583.33 / mes", "Gasto mensual neto estrictamente controlado"),
        ("PUNTO MÍNIMO DE TESORERÍA EN CAJA", "$44,500.00 (Mes 6)", "$43,962.00 (Mes 6)", "$7,470.00 (Mes 10)", "Caja SIEMPRE positiva: resiste 4 meses de mora"),
        ("Colchón Mínimo de Seguridad (% Capital)", "37.1%", "36.6%", "6.2%", "Resiste demoras de firmas sin caer en insolvencia"),
        ("SUPERÁVIT FINAL EN CAJA AL CIERRE DE AÑO 1", "$136,380.00", "$135,462.00", "$136,380.00", "Solvencia asegurada para expansión en CUCEI")
    ]

    for idx, row in enumerate(sens_rows, start=6):
        ws9[f"A{idx}"] = row[0]
        ws9[f"A{idx}"].alignment = align_left
        ws9[f"B{idx}"] = row[1]
        ws9[f"B{idx}"].alignment = align_center
        ws9[f"C{idx}"] = row[2]
        ws9[f"C{idx}"].alignment = align_center
        ws9[f"D{idx}"] = row[3]
        ws9[f"D{idx}"].alignment = align_center
        ws9[f"E{idx}"] = row[4]
        ws9[f"E{idx}"].alignment = align_left

        for col_l in cols_sens:
            ws9[f"{col_l}{idx}"].border = border_cell
            ws9[f"{col_l}{idx}"].font = font_regular

        if idx in (14, 16):
            ws9[f"A{idx}"].font = font_bold
            ws9[f"B{idx}"].font = font_bold
            ws9[f"C{idx}"].font = font_bold
            ws9[f"D{idx}"].font = font_bold
            if idx == 14:
                ws9[f"B{idx}"].fill = fill_highlight_green
                ws9[f"C{idx}"].fill = fill_highlight_green
                ws9[f"D{idx}"].fill = fill_highlight_yellow
            elif idx == 16:
                ws9[f"B{idx}"].fill = fill_highlight_green
                ws9[f"C{idx}"].fill = fill_highlight_green
                ws9[f"D{idx}"].fill = fill_highlight_green
                for col_l in cols_sens:
                    ws9[f"{col_l}{idx}"].border = border_total

    # --- TABLA B: REQUERIMIENTOS MÍNIMOS DE VENTANILLA Y MÉTRICAS DE SATURACIÓN ---
    ws9["A19"] = "B. REQUERIMIENTOS TÉCNICOS DE VENTANILLA, SATURACIÓN Y PLAN DE TALENTO"
    ws9["A19"].font = Font(name="Calibri", size=11, bold=True, color="1E3A8A")

    h_req = ["Componente / Dimensión", "Requerimiento Técnico Mínimo en Ventanilla", "Métrica / Umbral de Saturación", "Impacto en SLA y Mitigación de Riesgo"]
    cols_req = ["A", "B", "C", "D"]
    for c_i, h in zip(cols_req, h_req):
        cell = ws9[f"{c_i}20"]
        cell.value = h
        cell.font = font_section
        cell.fill = fill_blue
        cell.alignment = align_center
        cell.border = border_cell

    req_data = [
        ("Hardware de Cómputo en Ventanilla", "CPU 2 núcleos 2.0 GHz (Core i3 4ª gen / AMD Ryzen 3), 4 GB RAM, 500 MB libres", "Compatibilidad con el 98% del parque instalado en UdeG", "Asegura ejecución ágil de PWA con IndexedDB y AES-256 sin retardo"),
        ("Navegador y Conectividad", "Google Chrome v90+, Firefox v88+ o Edge v90+ (con Service Workers)", "Soporte obligatorio de Background Sync API y almacenamiento local", "Garantiza el modo contingencia offline ininterrumpido en horas pico"),
        ("Periféricos de Captura", "Lector óptico USB de código de barras/QR (Plug & Play) o webcam 720p", "Lectura en <1 segundo por credencial", "Reduce el tiempo de atención de 4.5 min a <27 segundos"),
        ("Umbral de Contratación Soporte N1 (Escala)", "Alcanzar 15 dependencias universitarias activas concurrentes", "Métrica de saturación comercial (Trigger Fase 2)", "Evita sobrecargar al Lead DevOps y asegura SLA de respuesta <15 min"),
        ("Umbral de Contratación Soporte N1 (Carga)", "> 20 tickets semanales durante dos semanas consecutivas o respuesta L2 > 25 min", "Métrica de saturación operativa de Mesa de Ayuda", "Garantiza resolución de fallas críticas en <1 hora en ventanillas"),
        ("Plan de Retención de Talento Clave", "Bono anual SLA $12k/año + Equity Vesting 10% a 24 meses + Bolsa GCP $4k", "Mitigación de fuga del 59.3% de costo en capital humano", "Asegura continuidad del Lead DevOps y cumplimiento ininterrumpido del SLA 99.5%")
    ]

    for idx, row in enumerate(req_data, start=21):
        for c_idx, col in enumerate(cols_req):
            cell = ws9[f"{col}{idx}"]
            cell.value = row[c_idx]
            cell.border = border_cell
            cell.font = font_regular
            if col == "A":
                cell.alignment = align_left
                cell.font = font_bold
            else:
                cell.alignment = align_left
        if idx == 26:
            ws9[f"A{idx}"].fill = fill_highlight_soft_blue

    col_widths_ws9 = {"A": 36, "B": 48, "C": 38, "D": 44}
    for col, width in col_widths_ws9.items():
        ws9.column_dimensions[col].width = width

    # Guardar archivo Excel
    out_excel = os.path.join("docs", "Determinacion_Costos_Producto_Servicio_SIGRE.xlsx")
    wb.save(out_excel)
    print(f"Archivo Excel creado con éxito: {out_excel}")

if __name__ == "__main__":
    create_cost_excel()
