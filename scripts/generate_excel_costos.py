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

    # Dimensionamiento Cloud Run / SQL / Storage / API consistente con $32,000 anuales de la presentación ($2,666.67/mes)
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
    ws1["E11"].fill = fill_highlight_soft_blue
    for c in range(1, 6):
        ws1.cell(row=11, column=c).border = border_total

    # --- BLOQUE 2: CAPITAL HUMANO (CONSISTENTE CON $130,000 ANUALES / $10,833.33 MES) ---
    ws1["A13"] = "Capital humano"
    ws1["A13"].font = Font(name="Calibri", size=11, bold=True, color="1E3A8A")

    ch_headers = ["Puesto / Especialidad", "Plazas", "Sueldo bruto", "Sueldo - ISR", "ISR"]
    for col_idx, h in enumerate(ch_headers, start=1):
        cell = ws1.cell(row=14, column=col_idx, value=h)
        cell.font = font_section
        cell.fill = fill_blue
        cell.alignment = align_center
        cell.border = border_cell

    ch_data = [
        ("Persona 1 (DevOps y Arquitectura Cloud)", 1, 7500.0, "=C15-E15", 900.0),
        ("Persona 2 (Soporte Técnico Almacenes y QA)", 1, 3333.333333, "=C16-E16", 400.0)
    ]

    for r_idx, row in enumerate(ch_data, start=15):
        ws1.cell(row=r_idx, column=1, value=row[0]).alignment = align_left
        ws1.cell(row=r_idx, column=2, value=row[1]).alignment = align_center
        ws1.cell(row=r_idx, column=3, value=row[2]).number_format = num_fmt_curr_int
        ws1.cell(row=r_idx, column=4, value=row[3]).number_format = num_fmt_curr_int
        ws1.cell(row=r_idx, column=5, value=row[4]).number_format = num_fmt_curr_int
        for c in range(1, 6):
            ws1.cell(row=r_idx, column=c).border = border_cell
            ws1.cell(row=r_idx, column=c).font = font_regular

    ws1["A17"] = "Total Capital Humano"
    ws1["A17"].font = font_bold
    ws1["C17"] = "=SUM(C15:C16)"
    ws1["C17"].number_format = num_fmt_curr_int
    ws1["C17"].font = font_bold
    ws1["C17"].fill = fill_highlight_yellow
    ws1["D17"] = "=SUM(D15:D16)"
    ws1["D17"].number_format = num_fmt_curr_int
    ws1["D17"].font = font_bold
    ws1["E17"] = "=SUM(E15:E16)"
    ws1["E17"].number_format = num_fmt_curr_int
    ws1["E17"].font = font_bold
    for c in range(1, 6):
        ws1.cell(row=17, column=c).border = border_total

    # --- BLOQUE 3: SERVICIOS MENSUAL (CONSISTENTE CON $30,000 ANUALES / $2,500 MES) ---
    ws1["A19"] = "Servicios mensual"
    ws1["A19"].font = Font(name="Calibri", size=11, bold=True, color="1E3A8A")
    ws1["B19"] = "Monto mensual"
    ws1["B19"].font = Font(name="Calibri", size=10, bold=True, color="FFFFFF")
    ws1["B19"].fill = fill_navy
    ws1["B19"].alignment = align_center
    ws1["A20"] = "luz"
    ws1["B20"] = 600.0
    ws1["A21"] = "agua"
    ws1["B21"] = 300.0
    ws1["A22"] = "internet"
    ws1["B22"] = 600.0
    ws1["A23"] = "gas (climatización / UPS)"
    ws1["B23"] = 400.0
    ws1["A24"] = "transacciones bancarias y viáticos"
    ws1["B24"] = 600.0

    for r in range(20, 25):
        ws1.cell(row=r, column=1).font = font_regular
        ws1.cell(row=r, column=1).border = border_cell
        ws1.cell(row=r, column=2).font = font_regular
        ws1.cell(row=r, column=2).number_format = num_fmt_curr
        ws1.cell(row=r, column=2).border = border_cell

    ws1["A25"] = "Total Servicios"
    ws1["A25"].font = font_bold
    ws1["A25"].border = border_total
    ws1["B25"] = "=SUM(B20:B24)"
    ws1["B25"].font = font_bold
    ws1["B25"].number_format = num_fmt_curr
    ws1["B25"].fill = fill_highlight_yellow
    ws1["B25"].border = border_total

    # --- BLOQUE 4: PERMISOS Y REGISTROS (CONSISTENTE CON $22,000 ANUALES / $1,833.33 MES, SIN IMPI) ---
    ws1["A27"] = "Permisos y Registros"
    ws1["A27"].font = Font(name="Calibri", size=11, bold=True, color="1E3A8A")
    ws1["A28"] = "Salubridad (Aviso Privacidad LGPDPPSO)"
    ws1["B28"] = 1000.0
    ws1["A29"] = "protección civil (INDAUTOR y Convenio CUT)"
    ws1["B29"] = 833.333333

    for r in range(28, 30):
        ws1.cell(row=r, column=1).font = font_regular
        ws1.cell(row=r, column=1).border = border_cell
        ws1.cell(row=r, column=2).font = font_regular
        ws1.cell(row=r, column=2).number_format = num_fmt_curr
        ws1.cell(row=r, column=2).border = border_cell

    ws1["A30"] = "Total Permisos"
    ws1["A30"].font = font_bold
    ws1["A30"].border = border_total
    ws1["B30"] = "=SUM(B28:B29)"
    ws1["B30"].font = font_bold
    ws1["B30"].number_format = num_fmt_curr
    ws1["B30"].fill = fill_highlight_yellow
    ws1["B30"].border = border_total

    # --- BLOQUE 5 (PARTE SUPERIOR DERECHA): RESUMEN DE COSTO Y PRECIOS ---
    ws1["G5"] = "Costo Total del Lote (100 pzas):"
    ws1["G5"].font = font_bold
    ws1["H5"] = "=D11+C17+B25+B30"
    ws1["H5"].font = Font(name="Calibri", size=11, bold=True, color="1E3A8A")
    ws1["H5"].number_format = num_fmt_curr
    ws1["H5"].fill = fill_highlight_green
    ws1["H5"].border = border_cell

    ws1["G6"] = "Costo Unitario (1 pza de 100):"
    ws1["G6"].font = font_bold
    ws1["H6"] = "=H5/100"
    ws1["H6"].font = Font(name="Calibri", size=11, bold=True, color="1E3A8A")
    ws1["H6"].number_format = num_fmt_curr
    ws1["H6"].fill = fill_highlight_green
    ws1["H6"].border = border_cell

    ws1["G8"] = "Precio sin iva"
    ws1["G8"].font = font_bold
    ws1["G8"].alignment = align_center
    ws1["G8"].fill = fill_header
    ws1["G8"].border = border_cell

    ws1["H8"] = "Precio con iva"
    ws1["H8"].font = font_bold
    ws1["H8"].alignment = align_center
    ws1["H8"].fill = fill_header
    ws1["H8"].border = border_cell

    ws1["G9"] = "=H6*2.5" # 2.5x Markup / 60% margen
    ws1["G9"].font = Font(name="Calibri", size=11, bold=True, color="0F172A")
    ws1["G9"].number_format = num_fmt_curr
    ws1["G9"].alignment = align_right
    ws1["G9"].border = border_cell

    ws1["H9"] = "=G9*1.16" # IVA 16%
    ws1["H9"].font = Font(name="Calibri", size=11, bold=True, color="2563EB")
    ws1["H9"].number_format = num_fmt_curr
    ws1["H9"].alignment = align_right
    ws1["H9"].border = border_cell

    # --- BLOQUE 6: TABLA DE VENTAS POR ESCALAS ---
    ventas_headers = ["Ventas (Unidades)", "Ingresos con IVA", "Costo Asociado", "Ganancia Bruta", "IVA Trasladado"]
    cols_v = ["G", "H", "I", "J", "K"]
    for col_letter, h in zip(cols_v, ventas_headers):
        cell = ws1[f"{col_letter}12"]
        cell.value = h
        cell.font = font_section
        cell.fill = fill_navy
        cell.alignment = align_center
        cell.border = border_cell

    v_escalas = [1, 10, 20, 50, 75, 100]
    for idx, v in enumerate(v_escalas, start=13):
        ws1[f"G{idx}"] = v
        ws1[f"G{idx}"].alignment = align_center
        ws1[f"H{idx}"] = f"=G{idx}*$H$9"
        ws1[f"H{idx}"].number_format = num_fmt_curr
        ws1[f"I{idx}"] = f"=G{idx}*$H$6"
        ws1[f"I{idx}"].number_format = num_fmt_curr
        ws1[f"J{idx}"] = f"=H{idx}-I{idx}"
        ws1[f"J{idx}"].number_format = num_fmt_curr
        ws1[f"K{idx}"] = f"=(H{idx}/1.16)*0.16" # IVA cobrado (16%)
        ws1[f"K{idx}"].number_format = num_fmt_curr

        for c in cols_v:
            ws1[f"{c}{idx}"].border = border_cell
            ws1[f"{c}{idx}"].font = font_regular
            if idx == 18:
                ws1[f"{c}{idx}"].fill = fill_highlight_soft_blue
                ws1[f"{c}{idx}"].font = font_bold

    # Fila final para 100 piezas destacando ganancia neta post IVA
    ws1["L18"] = "=J18-K18" # Ganancia neta post IVA
    ws1["L18"].font = Font(name="Calibri", size=10, bold=True, color="10B981")
    ws1["L18"].number_format = num_fmt_curr
    ws1["L18"].fill = fill_highlight_green
    ws1["L18"].border = border_cell

    # Resumen de IVA SAT
    ws1["G20"] = "IVA PAGADO"
    ws1["H20"] = "IVA COBRADO"
    ws1["I20"] = "IVA SAT (A pagar)"
    for c in ["G", "H", "I"]:
        ws1[f"{c}20"].font = font_bold
        ws1[f"{c}20"].fill = fill_header
        ws1[f"{c}20"].alignment = align_center
        ws1[f"{c}20"].border = border_cell

    ws1["G21"] = "=E11" # IVA de materias primas
    ws1["H21"] = "=K18" # IVA cobrado en ventas de 100 pzas
    ws1["I21"] = "=H21-G21" # Saldo a pagar al SAT
    for c in ["G", "H", "I"]:
        ws1[f"{c}21"].font = font_bold
        ws1[f"{c}21"].number_format = num_fmt_curr
        ws1[f"{c}21"].alignment = align_right
        ws1[f"{c}21"].border = border_total
    ws1["I21"].fill = fill_highlight_yellow

    # Ajuste de anchos de columna en ws1
    col_widths_ws1 = {
        "A": 38, "B": 14, "C": 19, "D": 17, "E": 14, "F": 4,
        "G": 20, "H": 20, "I": 18, "J": 18, "K": 17, "L": 20
    }
    for col, width in col_widths_ws1.items():
        ws1.column_dimensions[col].width = width

    # =========================================================================
    # HOJA 2: ECONOMÍAS DE ESCALA Y PUNTO DE EQUILIBRIO
    # =========================================================================
    ws2 = wb.create_sheet(title="Economía de Escala y PE")
    ws2.views.sheetView[0].showGridLines = True

    ws2["A1"] = "ANÁLISIS DE ECONOMÍAS DE ESCALA Y DETERMINACIÓN DE PRODUCCIÓN MÍNIMA COMPETITIVA"
    ws2["A1"].font = font_title
    ws2["A2"] = "Demostración de no linealidad del costo y estimación formal del Punto de Equilibrio (Guía BBVA / Baca Urbina)"
    ws2["A2"].font = font_subtitle

    # Cuadro de Parámetros Fijos y Variables
    ws2["A4"] = "PARÁMETROS DE COSTO OPERATIVO"
    ws2["A4"].font = font_section
    ws2["A4"].fill = fill_navy
    ws2["B4"] = "MONTO (MXN)"
    ws2["B4"].font = font_section
    ws2["B4"].fill = fill_navy
    ws2["B4"].alignment = align_right

    cf_rows = [
        ("Costos Fijos Mensuales (CF):", "= 'Modelo de Costos y Precios'!C17 + 'Modelo de Costos y Precios'!B25 + 'Modelo de Costos y Precios'!B30"),
        ("  • Capital Humano (Dev + Soporte):", "= 'Modelo de Costos y Precios'!C17"),
        ("  • Servicios Operativos Mensuales:", "= 'Modelo de Costos y Precios'!B25"),
        ("  • Permisos y Trámites Amortizados:", "= 'Modelo de Costos y Precios'!B30"),
        ("Costo Variable Unitario (CVU) sin IVA:", "= 'Modelo de Costos y Precios'!C11 / 100"),
        ("Precio de Venta Unitario (P) sin IVA:", "= 'Modelo de Costos y Precios'!G9"),
        ("Margen de Contribución Unitario (MCU = P - CVU):", "= B9 - B8"),
        ("Razón de Margen de Contribución (MCU / P):", "= B10 / B9"),
        ("PUNTO DE EQUILIBRIO EN UNIDADES (Q_PE = CF / MCU):", "= B4 / B10"),
        ("PUNTO DE EQUILIBRIO EN VENTAS ($):", "= B12 * B9")
    ]

    for idx, (label, val) in enumerate(cf_rows, start=4):
        ws2[f"A{idx}"] = label
        ws2[f"A{idx}"].font = font_bold if idx in (4, 8, 9, 10, 11, 12, 13) else font_regular
        ws2[f"A{idx}"].border = border_cell
        ws2[f"B{idx}"] = val
        ws2[f"B{idx}"].border = border_cell
        ws2[f"B{idx}"].alignment = align_right
        if idx == 11:
            ws2[f"B{idx}"].number_format = num_fmt_pct
            ws2[f"B{idx}"].font = font_bold
        elif idx == 12:
            ws2[f"B{idx}"].number_format = "0.0 'dependencias'"
            ws2[f"B{idx}"].font = Font(name="Calibri", size=11, bold=True, color="1E3A8A")
            ws2[f"B{idx}"].fill = fill_highlight_yellow
        elif idx == 13:
            ws2[f"B{idx}"].number_format = num_fmt_curr
            ws2[f"B{idx}"].font = Font(name="Calibri", size=11, bold=True, color="1E3A8A")
            ws2[f"B{idx}"].fill = fill_highlight_green
        else:
            ws2[f"B{idx}"].number_format = num_fmt_curr
            if idx == 4:
                ws2[f"B{idx}"].font = font_bold
                ws2[f"B{idx}"].fill = fill_highlight_soft_blue

    # Tabla Comparativa de Economías de Escala
    ws2["D4"] = "MODELO DE COSTO MEDIO SEGÚN VOLUMEN (ECONOMÍAS DE ESCALA)"
    ws2.merge_cells("D4:K4")
    ws2["D4"].font = font_section
    ws2["D4"].fill = fill_navy
    ws2["D4"].alignment = align_center

    ee_headers = ["Volumen (Q)", "Costos Fijos", "Costos Variables", "Costo Total Real", "Costo Unitario Real", "Precio s/IVA", "Utilidad Operativa", "Condición"]
    cols_ee = ["D", "E", "F", "G", "H", "I", "J", "K"]
    for c, h in zip(cols_ee, ee_headers):
        cell = ws2[f"{c}5"]
        cell.value = h
        cell.font = font_bold
        cell.fill = fill_header
        cell.alignment = align_center
        cell.border = border_cell

    test_vols = [1, 5, 10, 20, 30, 35, 50, 75, 100]
    for r_idx, q in enumerate(test_vols, start=6):
        ws2[f"D{r_idx}"] = q
        ws2[f"D{r_idx}"].alignment = align_center
        ws2[f"E{r_idx}"] = "=$B$4"
        ws2[f"E{r_idx}"].number_format = num_fmt_curr_int
        ws2[f"F{r_idx}"] = f"=D{r_idx}*$B$8"
        ws2[f"F{r_idx}"].number_format = num_fmt_curr
        ws2[f"G{r_idx}"] = f"=E{r_idx}+F{r_idx}"
        ws2[f"G{r_idx}"].number_format = num_fmt_curr
        ws2[f"H{r_idx}"] = f"=G{r_idx}/D{r_idx}"
        ws2[f"H{r_idx}"].number_format = num_fmt_curr
        ws2[f"I{r_idx}"] = "=$B$9"
        ws2[f"I{r_idx}"].number_format = num_fmt_curr
        ws2[f"J{r_idx}"] = f"=(I{r_idx}*D{r_idx})-G{r_idx}"
        ws2[f"J{r_idx}"].number_format = num_fmt_curr
        ws2[f"K{r_idx}"] = f'=IF(J{r_idx}<0, "Déficit / Absorción", IF(D{r_idx}=35, "Punto Equilibrio", "Rentable (Escala)"))'
        ws2[f"K{r_idx}"].alignment = align_center

        for c in cols_ee:
            ws2[f"{c}{r_idx}"].border = border_cell
            ws2[f"{c}{r_idx}"].font = font_regular
            if q < 35:
                ws2[f"K{r_idx}"].font = Font(name="Calibri", size=9, bold=True, color="EF4444")
                ws2[f"J{r_idx}"].font = Font(name="Calibri", size=9, color="EF4444")
            elif q == 35:
                ws2[f"{c}{r_idx}"].fill = fill_highlight_yellow
                ws2[f"K{r_idx}"].font = Font(name="Calibri", size=9, bold=True, color="B45309")
            else:
                ws2[f"K{r_idx}"].font = Font(name="Calibri", size=9, bold=True, color="10B981")
                ws2[f"J{r_idx}"].font = Font(name="Calibri", size=9, color="10B981")

    # Ajuste anchos ws2
    col_widths_ws2 = {
        "A": 44, "B": 22, "C": 4, "D": 14, "E": 16, "F": 16,
        "G": 18, "H": 18, "I": 16, "J": 18, "K": 20
    }
    for col, width in col_widths_ws2.items():
        ws2.column_dimensions[col].width = width

    # Insertar imagen de Punto de Equilibrio en ws2
    fig3_path = os.path.join("docs", "graficos", "figura3_curva_economias_escala_punto_equilibrio.png")
    if os.path.exists(fig3_path):
        img_pe = OpenpyxlImage(fig3_path)
        img_pe.width = 750
        img_pe.height = 320
        ws2.add_image(img_pe, "A17")

    # =========================================================================
    # HOJA 3: CRITERIOS Y ANÁLISIS DE PARETO
    # =========================================================================
    ws3 = wb.create_sheet(title="Criterios y Pareto")
    ws3.views.sheetView[0].showGridLines = True

    ws3["A1"] = "EVALUACIÓN MULTICRITERIO Y DIAGRAMA DE PARETO (80/20) DE COSTOS"
    ws3["A1"].font = font_title
    ws3["A2"] = "Criterios analizados: Disponibilidad, Criticidad, Relación Volumen-Precio y Costos Derivados"
    ws3["A2"].font = font_subtitle

    crit_headers = ["Partida de Costo", "Monto Mensual", "% del Total", "% Acumulado", "Clasificación ABC", "Disponibilidad en Mercado", "Criticidad Operativa", "Sensibilidad al Volumen"]
    cols_crit = ["A", "B", "C", "D", "E", "F", "G", "H"]
    for c, h in zip(cols_crit, crit_headers):
        cell = ws3[f"{c}4"]
        cell.value = h
        cell.font = font_section
        cell.fill = fill_navy
        cell.alignment = align_center
        cell.border = border_cell

    crit_data = [
        ("Capital Humano Directo (Dev Full-Stack + Soporte)", "= 'Modelo de Costos y Precios'!C17", "=B5/SUM($B$5:$B$8)", "=C5", "A (Crítico 80%)", "Media (Talento especializado en cloud/Docker)", "Extrema (Desarrollo, seguridad y soporte a planteles)", "Baja (Costo fijo mensual independiente del tráfico)"),
        ("Insumos Cloud / TI (GCP, PostgreSQL, Storage, API)", "= 'Modelo de Costos y Precios'!D11", "=B6/SUM($B$5:$B$8)", "=D5+C6", "A (Crítico 80%)", "Inmediata (SLA 99.9% Google Cloud Platform)", "Extrema (Disponibilidad de plataforma 24/7)", "Alta (Escala linealmente según concurrencia de planteles)"),
        ("Servicios Operativos (Internet, Luz, Traslados)", "= 'Modelo de Costos y Precios'!B25", "=B7/SUM($B$5:$B$8)", "=D6+C7", "B (Moderado)", "Alta (Proveedores de conectividad comercial)", "Media (Soporte administrativo y enlace de respaldo)", "Baja (Costos base de oficina técnica)"),
        ("Cumplimiento Legal (LGPDPPSO / INDAUTOR)", "= 'Modelo de Costos y Precios'!B30", "=B8/SUM($B$5:$B$8)", "=D7+C8", "C (Secundario)", "Alta (Trámite ante ventanillas oficiales del Estado)", "Alta en certeza jurídica, baja en flujo financiero", "Nula (Costo de trámite fijo amortizado)")
    ]

    for idx, row in enumerate(crit_data, start=5):
        ws3[f"A{idx}"] = row[0]
        ws3[f"A{idx}"].alignment = align_left
        ws3[f"B{idx}"] = row[1]
        ws3[f"B{idx}"].number_format = num_fmt_curr
        ws3[f"B{idx}"].alignment = align_right
        ws3[f"C{idx}"] = row[2]
        ws3[f"C{idx}"].number_format = num_fmt_pct
        ws3[f"C{idx}"].alignment = align_center
        ws3[f"D{idx}"] = row[3]
        ws3[f"D{idx}"].number_format = num_fmt_pct
        ws3[f"D{idx}"].alignment = align_center
        ws3[f"E{idx}"] = row[4]
        ws3[f"E{idx}"].alignment = align_center
        ws3[f"F{idx}"] = row[5]
        ws3[f"G{idx}"] = row[6]
        ws3[f"H{idx}"] = row[7]

        for c in cols_crit:
            ws3[f"{c}{idx}"].border = border_cell
            ws3[f"{c}{idx}"].font = font_regular
            if idx in (5, 6):
                ws3[f"E{idx}"].font = Font(name="Calibri", size=9.5, bold=True, color="1E3A8A")
                ws3[f"E{idx}"].fill = fill_highlight_soft_blue

    # Fila total
    ws3["A9"] = "TOTAL COSTO MENSUAL DEL LOTE (100 UNIDADES)"
    ws3["A9"].font = font_bold
    ws3["B9"] = "=SUM(B5:B8)"
    ws3["B9"].number_format = num_fmt_curr
    ws3["B9"].font = font_bold
    ws3["B9"].fill = fill_highlight_green
    ws3["C9"] = "=SUM(C5:C8)"
    ws3["C9"].number_format = num_fmt_pct
    ws3["C9"].font = font_bold
    ws3["D9"] = "100.0%"
    ws3["D9"].font = font_bold
    for c in cols_crit:
        ws3[f"{c}9"].border = border_total

    # Ajuste de anchos ws3
    col_widths_ws3 = {
        "A": 42, "B": 18, "C": 14, "D": 14, "E": 18,
        "F": 34, "G": 34, "H": 34
    }
    for col, width in col_widths_ws3.items():
        ws3.column_dimensions[col].width = width

    # Insertar imagen de Pareto en ws3
    fig2_path = os.path.join("docs", "graficos", "figura2_grafico_pareto_criterios_costo.png")
    if os.path.exists(fig2_path):
        img_pareto = OpenpyxlImage(fig2_path)
        img_pareto.width = 680
        img_pareto.height = 380
        ws3.add_image(img_pareto, "A12")

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
        ("Costo de Adopción Anual de Licencia SIGRE (1 Almacén Central)", 0.0, 28950.0, "-$28,950.00 MXN inversión anual", "Tarifa SaaS anual SIGRE"),
        ("BENEFICIO NETO ANUAL GENERADO AL CENTRO UNIVERSITARIO", "=-B15", "=D15-C16", "$661,050.00 MXN beneficio neto", "ROI Operativo: 2,283% | Payback: 15 días")
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
            elif idx in (11, 12, 13, 14, 15, 16, 17):
                ws4[f"{c}{idx}"].number_format = num_fmt_curr
                ws4[f"{c}{idx}"].alignment = align_right

        ws4[f"D{idx}"].alignment = align_right if idx in (12, 13, 14, 15, 16, 17) else align_center
        ws4[f"E{idx}"].alignment = align_left

        for c in cols_quant:
            ws4[f"{c}{idx}"].border = border_cell
            ws4[f"{c}{idx}"].font = font_regular

        if idx in (15, 17):
            ws4[f"A{idx}"].font = font_bold
            ws4[f"B{idx}"].font = font_bold
            ws4[f"C{idx}"].font = font_bold
            ws4[f"D{idx}"].font = font_bold
            if idx == 15:
                ws4[f"B{idx}"].fill = fill_alert_red
                ws4[f"D{idx}"].fill = fill_highlight_yellow
            elif idx == 17:
                ws4[f"C{idx}"].fill = fill_highlight_green
                ws4[f"D{idx}"].fill = fill_highlight_green
                for c in cols_quant:
                    ws4[f"{c}{idx}"].border = border_total

    # --- TABLA B: BENCHMARKING COMPETITIVO DE MERCADO ---
    ws4["A20"] = "B. ESTUDIO DE MERCADO Y BENCHMARKING COMPETITIVO (SIGRE VS. ALTERNATIVAS)"
    ws4["A20"].font = Font(name="Calibri", size=11, bold=True, color="1E3A8A")

    h_bench = ["Criterio / Factor Clave", "SIGRE (Propuesta)", "ERP Corporativo (SAP Ariba / Oracle)", "Software Comercial (Odoo / Zoho)", "Gestión Artesanal (Excel / Papel)"]
    cols_bench = ["A", "B", "C", "D", "E"]
    for c, h in zip(cols_bench, h_bench):
        cell = ws4[f"{c}21"]
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

    for idx, row in enumerate(bench_data, start=22):
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

    col_widths_ws4 = {"A": 48, "B": 24, "C": 26, "D": 32, "E": 36}
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
         "1. Tasa de pérdida o extravío de activos reducida a menos del 0.5% en planteles participantes al término del Año 3.\n2. Reducción del 85% en tiempos de espera de alumnos en ventanillas de laboratorios a nivel Red.",
         "Dictámenes telemétricos y reportes de discrepancia cero generados nativamente por SIGRE; actas de cierre semestral de inventario firmadas por las Coordinaciones de Laboratorio de los campus.",
         "La política institucional de la Universidad de Guadalajara mantiene su compromiso estratégico con la política de 'Cero Papel' y la digitalización administrativa."),
        ("PROPÓSITO",
         "Optimizar los procesos de solicitud, validación de riesgo, despacho y devolución de inventario en almacenes y ventanillas de centros universitarios (Piloto CUTonalá, expansión a CUCEI y red).",
         "1. Tiempo promedio de despacho por vale menor a 30 segundos en el 98% de transacciones.\n2. 100% de los préstamos cuentan con trazabilidad criptográfica y score de riesgo asignado al solicitante al cierre del Año 1.",
         "Métricas telemétricas de Cloud SQL / BigQuery; reportes mensuales de operación generados automáticamente por SIGRE; bitácoras de auditoría de despacho.",
         "Coordinadores de carrera, laboratoristas y jefes de almacén aplican de forma obligatoria y estandarizada la plataforma en sustitución del vale en papel."),
        ("COMPONENTES (PRODUCTOS)",
         "C1. Plataforma Web SaaS multi-tenant en Google Cloud Platform (Cloud Run + PostgreSQL Cloud SQL + Secret Manager).\nC2. Algoritmo predictivo de Scoring de Fiabilidad del Solicitante.\nC3. Interfaz de Ventanilla PWA con capacidad de operación en modo offline y sincronización asíncrona.\nC4. Programa integral de Capacitación, Gobernanza de Datos (LGPDPPSO) y Manuales de Operación.",
         "1. Disponibilidad de la plataforma de 99.5% mensual (SLA Cloud Run).\n2. Capacidad de operación offline local de hasta 4 horas continuas sin conexión a internet.\n3. 100% de encargados de ventanilla y jefes de almacén de centros piloto acreditados en el uso del sistema.",
         "Dashboard de monitoreo de Google Cloud Monitoring; reportes de pruebas de carga y estrés k6; actas de acreditación de talleres de capacitación y entrega de manuales.",
         "La infraestructura de Google Cloud Platform mantiene su estándar de estabilidad y el personal operativo muestra adaptabilidad a herramientas digitales."),
        ("ACTIVIDADES",
         "A1. Arquitectura de microservicios y despliegue CI/CD en GCP (M1-M2).\nA2. Desarrollo del motor de scoring y Progressive Web App con Service Workers (M3-M4).\nA3. Pruebas QA, pentesting OWASP y auditoría LGPDPPSO (M5).\nA4. Trámite de registro de derechos de autor de software ante INDAUTOR (M6).\nA5. Despliegue piloto en almacenes y talleres de CUTonalá (M7).\nA6. Capacitación presencial y marcha blanca con supervisión en sitio (M8-M9).\nA7. Auditoría técnica, medición de KPIs y release v1.5 para expansión a CUCEI (M10-M12).",
         "1. Inversión ejecutada conforme al cronograma de $120,000 MXN en Año 1.\n2. 100% de los hitos técnicos concluidos en los plazos acordados.\n3. Certificado de INDAUTOR obtenido en el Mes 6.",
         "Repositorio de código GitHub con tags de release firmados; comprobante oficial de registro ante INDAUTOR; listas de asistencia a talleres y actas de inicio de piloto.",
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
        ("3. Pruebas Unitarias, Integración, Estrés de Carga (k6) y Auditoría LGPDPPSO", "QA Engineer", [0,0,0,0,1,0,0,0,0,0,0,0], 12000.0),
        ("4. Hito Legal: Trámite Registro Software INDAUTOR (Buffer 3 sem)", "Asesor Jurídico / PM", [0,0,0,0,0,1,0,0,0,0,0,0], 5500.0),
        ("5. Despliegue Piloto en CUTonalá (Almacén Central y Laboratorios de Cómputo)", "DevOps + Soporte", [0,0,0,0,0,0,1,0,0,0,0,0], 11500.0),
        ("6. Programa de Capacitación Presencial a Almacenistas y Laboratoristas", "Customer Success / Soporte", [0,0,0,0,0,0,0,1,1,0,0,0], 10000.0),
        ("7. Marcha Blanca y Monitoreo de KPIs Ventanilla (Buffer 2 sem)", "Soporte L2", [0,0,0,0,0,0,0,0,1,1,1,0], 16500.0),
        ("8. Evaluación de Impacto, Release v1.5 y Preparación Expansión hacia CUCEI", "Equipo Completo", [0,0,0,0,0,0,0,0,0,0,0,1], 15500.0)
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
        ("UTILIDAD (PÉRDIDA) NETA PROYECTADA", "=B19-B21", "=C19-C21", "=D19-D21", "Resultado neto final del ejercicio"),
        ("Margen Neto (%)", "=B22/B9", "=C22/C9", "=D22/D9", "Rentabilidad neta final")
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
            elif idx in (6, 7, 8, 9, 10, 11, 14, 15, 16, 17, 18, 19, 21, 22):
                cell.number_format = num_fmt_curr
                cell.alignment = align_right
            elif idx in (12, 20, 23):
                cell.number_format = num_fmt_pct
                cell.alignment = align_center

        for c in cols_er:
            ws7[f"{c}{idx}"].border = border_cell
            ws7[f"{c}{idx}"].font = font_regular

        if idx in (7, 9, 11, 18, 19, 22):
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
                for c in cols_er:
                    ws7[f"{c}{idx}"].border = border_total

    col_widths_ws7 = {"A": 46, "B": 24, "C": 24, "D": 26, "E": 44}
    for col, width in col_widths_ws7.items():
        ws7.column_dimensions[col].width = width

    # =========================================================================
    # HOJA 8: FLUJO DE EFECTIVO MENSUAL PRO FORMA (CASH FLOW AÑO 1)
    # =========================================================================
    ws8 = wb.create_sheet(title="Flujo de Efectivo Mensual")
    ws8.views.sheetView[0].showGridLines = True

    ws8["A1"] = "FLUJO DE EFECTIVO MENSUAL PRO FORMA (CASH FLOW) — AÑO 1 PILOTO (MXN)"
    ws8["A1"].font = font_title
    ws8["A2"] = "Análisis de liquidez mensual, absorción de capital semilla de $120,000 MXN y tasa de quema de efectivo (burn rate)"
    ws8["A2"].font = font_subtitle

    h_cf = ["Concepto de Flujo de Efectivo", "M1", "M2", "M3", "M4", "M5", "M6", "M7", "M8", "M9", "M10", "M11", "M12", "Total Año 1"]
    cols_cf = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N"]
    for c, h in zip(cols_cf, h_cf):
        cell = ws8[f"{c}4"]
        cell.value = h
        cell.font = font_section
        cell.fill = fill_navy
        cell.alignment = align_center
        cell.border = border_cell

    cf_rows = [
        ("SALDO INICIAL DE EFECTIVO EN CAJA", [0.0, "=B18", "=C18", "=D18", "=E18", "=F18", "=G18", "=H18", "=I18", "=J18", "=K18", "=L18"], "=B5"),
        ("ENTRADAS DE EFECTIVO OPERATIVAS Y FINANCIAMIENTO:", ["" for _ in range(12)], ""),
        ("  • Aportación de Capital Semilla Inicial", [120000.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], "=SUM(B7:M7)"),
        ("  • Cobranza de Licencias Piloto CUTonalá (5 deps + IVA)", [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 167910.0, 0.0, 0.0, 0.0, 0.0, 0.0], "=SUM(B8:M8)"),
        ("TOTAL ENTRADAS DE EFECTIVO", [f"=SUM({get_column_letter(c_i)}7:{get_column_letter(c_i)}8)" for c_i in range(2, 14)], "=SUM(N7:N8)"),
        ("SALIDAS DE EFECTIVO OPERATIVAS (EGRESOS):", ["" for _ in range(12)], ""),
        ("  • Nómina y Honorarios Técnicos (DevOps + QA)", [10500.0 for _ in range(12)], "=SUM(B11:M11)"),
        ("  • Servicios Cloud GCP (Compute, SQL, Storage)", [510.0 for _ in range(12)], "=SUM(B12:M12)"),
        ("  • Conectividad, Licencias Dev y Soporte Base", [990.0, 990.0, 1490.0, 1490.0, 990.0, 0.0, 400.0, 0.0, 0.0, 0.0, 0.0, 0.0], "=SUM(B13:M13)"),
        ("  • Registro de Obra Software ante INDAUTOR (Hito M6)", [0.0, 0.0, 0.0, 0.0, 0.0, 3500.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], "=SUM(B14:M14)"),
        ("  • Viáticos y Talleres de Capacitación en Almacenes", [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 2590.0, 2500.0, 0.0, 0.0, 0.0, 0.0], "=SUM(B15:M15)"),
        ("  • Auditoría Técnica, Evaluación Piloto y Cierre v1.5", [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 4490.0], "=SUM(B16:M16)"),
        ("TOTAL SALIDAS DE EFECTIVO", [f"=SUM({get_column_letter(c_i)}11:{get_column_letter(c_i)}16)" for c_i in range(2, 14)], "=SUM(N11:N16)"),
        ("SALDO FINAL ACUMULADO EN CAJA (TESORERÍA)", [f"={get_column_letter(c_i)}5+{get_column_letter(c_i)}9-{get_column_letter(c_i)}17" for c_i in range(2, 14)], "=M18"),
        ("FLUJO NETO MENSUAL (Entradas - Salidas)", [f"={get_column_letter(c_i)}9-{get_column_letter(c_i)}17" for c_i in range(2, 14)], "=N9-N17")
    ]

    for idx, row in enumerate(cf_rows, start=5):
        ws8[f"A{idx}"] = row[0]
        ws8[f"A{idx}"].alignment = align_left

        vals = row[1]
        for m_idx, v in enumerate(vals):
            col_letter = get_column_letter(2 + m_idx)
            cell = ws8[f"{col_letter}{idx}"]
            cell.value = v
            if idx not in (6, 10):
                cell.number_format = num_fmt_curr_int
                cell.alignment = align_right

        ws8[f"N{idx}"] = row[2]
        if idx not in (6, 10):
            ws8[f"N{idx}"].number_format = num_fmt_curr_int
            ws8[f"N{idx}"].alignment = align_right

        for c in cols_cf:
            ws8[f"{c}{idx}"].border = border_cell
            ws8[f"{c}{idx}"].font = font_regular

        if idx in (5, 9, 17, 18, 19):
            ws8[f"A{idx}"].font = font_bold
            for c in cols_cf[1:]:
                ws8[f"{c}{idx}"].font = font_bold
            if idx == 9:
                for c in cols_cf[1:]:
                    ws8[f"{c}{idx}"].fill = fill_highlight_soft_blue
            elif idx == 17:
                for c in cols_cf[1:]:
                    ws8[f"{c}{idx}"].fill = fill_alert_red
            elif idx == 18:
                for c in cols_cf[1:]:
                    ws8[f"{c}{idx}"].fill = fill_highlight_green
                    ws8[f"{c}{idx}"].border = border_total
            elif idx == 19:
                for c in cols_cf[1:]:
                    ws8[f"{c}{idx}"].fill = fill_header

    ws8["A22"] = "INDICADORES CLAVE DE TESORERÍA Y RIESGO FINANCIERO"
    ws8["A22"].font = font_bold
    kpis_cf = [
        ("Tasa de Quema de Efectivo Promedio (Burn Rate Pre-operativo M1-M6)", "$12,583 MXN / mes", "Gasto neto de operación mensual previo al cobro de licencias"),
        ("Punto Mínimo de Tesorería en Caja (Mes 6 - Hito INDAUTOR)", "$44,500 MXN", "Colchón mínimo de seguridad antes de la facturación del piloto (37% de capital intacto)"),
        ("Requerimiento Máximo de Capital de Trabajo (Inversión Inicial)", "$120,000 MXN", "Monto suficiente para garantizar solvencia operativa del 100%"),
        ("Superávit de Caja al Cierre del Año 1", "$136,350 MXN", "Fondo de reserva disponible para financiar la expansión en CUCEI")
    ]
    for k_idx, (kpi, val, desc) in enumerate(kpis_cf, start=23):
        ws8[f"A{k_idx}"] = kpi
        ws8[f"A{k_idx}"].font = font_bold
        ws8[f"A{k_idx}"].alignment = align_left
        ws8[f"B{k_idx}"] = val
        ws8[f"B{k_idx}"].font = Font(name="Calibri", size=10, bold=True, color="1E3A8A")
        ws8[f"B{k_idx}"].alignment = align_center
        ws8[f"B{k_idx}"].fill = fill_highlight_yellow
        ws8[f"C{k_idx}"] = desc
        ws8[f"C{k_idx}"].font = font_footnote
        ws8[f"C{k_idx}"].alignment = align_left

    col_widths_ws8 = {"A": 42, "B": 14, "C": 14, "D": 14, "E": 14, "F": 14, "G": 14, "H": 15, "I": 14, "J": 14, "K": 14, "L": 14, "M": 14, "N": 16}
    for col, width in col_widths_ws8.items():
        ws8.column_dimensions[col].width = width


    # =========================================================================
    # HOJA 9: ANÁLISIS DE SENSIBILIDAD Y GESTIÓN DE RIESGO FINANCIERO
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
    ws9["A19"] = "B. REQUERIMIENTOS TÉCNICOS DE VENTANILLA Y MÉTRICAS DE SATURACIÓN DE SOPORTE"
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
        ("Umbral de Contratación Soporte N1 (Carga)", "> 20 tickets semanales durante dos semanas consecutivas o respuesta L2 > 25 min", "Métrica de saturación operativa de Mesa de Ayuda", "Garantiza resolución de fallas críticas en <1 hora en ventanillas")
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

    col_widths_ws9 = {"A": 36, "B": 48, "C": 38, "D": 44}
    for col, width in col_widths_ws9.items():
        ws9.column_dimensions[col].width = width

    # Guardar archivo Excel
    out_excel = os.path.join("docs", "Determinacion_Costos_Producto_Servicio_SIGRE.xlsx")
    wb.save(out_excel)
    print(f"Archivo Excel creado con éxito: {out_excel}")

if __name__ == "__main__":
    create_cost_excel()
