"""
Suite de Pruebas de Rigor Financiero, Matemático y Consistencia Tabular
Proyecto SIGRE - Formulación y Evaluación de Proyectos de Inversión (FEPI)
Alineado con .agents/rules/rigor_financiero_y_matematico.md
"""



def test_capex_budget_breakdown():
    """Valida que el desglose de CAPEX sume exactamente $180,000 MXN al centavo."""
    capex_items = [
        ("P1. Pulido técnico y desarrollo software", 75000.0),
        ("P2. Infraestructura cloud y servicios web", 20000.0),
        ("P3. Propiedad intelectual y trámites", 25000.0),
        ("P4. Hardware demo ($13.5k) y dossiers ($6.5k)", 20000.0),
        ("P5. Fondo de reserva y contingencia", 40000.0)
    ]
    total_capex = sum(x[1] for x in capex_items)
    assert total_capex == 180000.0, f"CAPEX total incorrecto: {total_capex} != 180000.0"

def test_year1_contracts_and_revenue():
    """Valida los 3 planteles en Año 1 y los ingresos brutos de $63,000 MXN."""
    contratos_prepas = 2
    cuota_prepa = 24000.0
    ingresos_sub = contratos_prepas * cuota_prepa
    ingresos_setup_cutonala = 15000.0
    total_ingresos_y1 = ingresos_sub + ingresos_setup_cutonala
    assert total_ingresos_y1 == 63000.0, f"Ingresos Año 1 incorrectos: {total_ingresos_y1} != 63000.0"

def test_financial_indicators_and_discounted_flows():
    """Valida el cálculo formal de VPN, TIR, Relación B/C y Payback Simple/Descontado."""
    flows = [-180000.0, -32000.0, 78900.0, 296800.0]
    tmar = 0.15

    # Valor Presente Neto (VPN)
    vp_flows = [f / ((1 + tmar) ** i) for i, f in enumerate(flows)]
    vpn = sum(vp_flows)
    assert round(vpn, 2) == 46984.47, f"VPN incorrecto: {vpn:.2f} != 46984.47"

    # Tasa Interna de Retorno (TIR)
    def npv_f(r):
        return sum(f / ((1 + r) ** i) for i, f in enumerate(flows))

    low, high = 0.0, 1.0
    for _ in range(100):
        mid = (low + high) / 2
        if npv_f(mid) > 0:
            low = mid
        else:
            high = mid
    tir = mid * 100
    assert round(tir, 2) == 24.27, f"TIR incorrecta: {tir:.2f}% != 24.27%"

    # Relación Beneficio / Costo (B/C)
    vp_beneficios = vp_flows[2] + vp_flows[3]
    vp_costos = abs(vp_flows[0]) + abs(vp_flows[1])
    bc_ratio = vp_beneficios / vp_costos
    assert round(bc_ratio, 2) == 1.23, f"Relación B/C incorrecta: {bc_ratio:.4f} != 1.23"

    # Payback Simple (Mes 29.4)
    saldo_y2 = -180000.0 - 32000.0 + 78900.0
    meses_y3 = abs(saldo_y2) / (296800.0 / 12.0)
    payback_simple = 24.0 + meses_y3
    assert round(payback_simple, 1) == 29.4, f"Payback Simple incorrecto: {payback_simple:.2f} != 29.4"

    # Payback Descontado (Mes 33.1)
    saldo_vp_y2 = vp_flows[0] + vp_flows[1] + vp_flows[2]
    vp_mensual_y3 = vp_flows[3] / 12.0
    meses_vp_y3 = abs(saldo_vp_y2) / vp_mensual_y3
    payback_descontado = 24.0 + meses_vp_y3
    assert round(payback_descontado, 1) == 33.1, f"Payback Descontado incorrecto: {payback_descontado:.2f} != 33.1"

def test_investor_cash_sweep_and_profit_reconciliation():
    """Valida la reconciliación del Cash Sweep del 70% y liquidación en Mes 31.2."""
    fen_y2 = 78900.0
    inv_y2 = fen_y2 * 0.70
    found_y2 = fen_y2 * 0.30
    assert inv_y2 == 55230.0
    assert found_y2 == 23670.0
    assert (inv_y2 + found_y2) == 78900.0

    saldo_capital = 180000.0 - inv_y2
    assert saldo_capital == 124770.0

    fen_y3 = 296800.0
    cuota_mensual_inv_y3 = (fen_y3 / 12.0) * 0.70
    meses_liq = saldo_capital / cuota_mensual_inv_y3
    mes_liq_total = 24.0 + meses_liq
    assert round(mes_liq_total, 1) == 31.2, f"Mes liquidación inversionista: {mes_liq_total:.2f} != 31.2"

    fen_tramo1 = meses_liq * (fen_y3 / 12.0)
    inv_tramo1 = fen_tramo1 * 0.70
    found_tramo1 = fen_tramo1 * 0.30

    meses_tramo2 = 12.0 - meses_liq
    fen_tramo2 = meses_tramo2 * (fen_y3 / 12.0)
    inv_tramo2 = fen_tramo2 * 0.15
    found_tramo2 = fen_tramo2 * 0.85

    inv_total_y3 = inv_tramo1 + inv_tramo2
    found_total_y3 = found_tramo1 + found_tramo2

    assert round(inv_total_y3) == 142554
    assert round(found_total_y3) == 154246
    assert round(inv_total_y3) + round(found_total_y3) == 296800

    # Año 4 base
    assert 296800.0 * 0.85 == 252280.0
    assert 296800.0 * 0.15 == 44520.0

def test_stepped_payroll_budget():
    """Valida la nómina escalonada sin romper $120k en Año 2 y $240k en Año 3."""
    # Año 2
    n1_y2 = 7 * 4000.0
    esp_y2 = 3 * 10000.0
    hon_y2 = 62000.0
    total_y2 = n1_y2 + esp_y2 + hon_y2
    assert total_y2 == 120000.0, f"Nómina Año 2 incorrecta: {total_y2} != 120000.0"

    # Año 3
    esp_y3 = 12 * 10000.0
    cs_y3 = 9 * 7000.0
    estip_y3 = 57000.0
    total_y3 = esp_y3 + cs_y3 + estip_y3
    assert total_y3 == 240000.0, f"Nómina Año 3 incorrecta: {total_y3} != 240000.0"

def test_investor_irr_at_5_years():
    """Valida la TIR del 21.20% anual para el inversionista a 5 años."""
    inv_flows = [-180000.0, 0.0, 55230.0, 142554.0, 58080.0, 92640.0]
    def inv_npv(r):
        return sum(f / ((1 + r) ** i) for i, f in enumerate(inv_flows))

    low, high = 0.0, 1.0
    for _ in range(100):
        mid = (low + high) / 2
        if inv_npv(mid) > 0:
            low = mid
        else:
            high = mid
    inv_tir = mid * 100
    assert round(inv_tir, 2) == 21.20, f"TIR Inversionista incorrecta: {inv_tir:.2f}% != 21.20%"

def test_viability_threshold_interpolation():
    """Valida el cálculo del umbral de rentabilidad de 18.12 planteles (~19 planteles / 9.7% Red)."""
    slope = (46984.47 - (-37703.62)) / (22.0 - 15.0)
    umbral = 15.0 + (0 - (-37703.62)) / slope
    assert round(umbral, 2) == 18.12, f"Umbral interpolado incorrecto: {umbral:.4f} != 18.12"
    pct_red = (19.0 / 196.0) * 100.0
    assert round(pct_red, 1) == 9.7, f"Porcentaje de la red incorrecto: {pct_red:.2f}% != 9.7%"

def test_proforma_income_statement_integrity():
    """Valida la consistencia aritmética vertical y horizontal de la Tabla 12 (Proforma)."""
    # Año 1
    ingresos_y1 = 63000.0
    opex_items_y1 = [18000.0, 40000.0, 12000.0, 15000.0, 10000.0]
    total_opex_y1 = sum(opex_items_y1)
    assert total_opex_y1 == 95000.0, f"OPEX Año 1 incorrecto: {total_opex_y1} != 95000.0"
    ebit_y1 = ingresos_y1 - total_opex_y1
    assert ebit_y1 == -32000.0, f"EBIT Año 1 incorrecto: {ebit_y1} != -32000.0"
    tax_y1 = 0.0
    fen_y1 = ebit_y1 - tax_y1
    assert fen_y1 == -32000.0, f"FEN Año 1 incorrecto: {fen_y1} != -32000.0"

    # Año 2
    ingresos_y2 = 324000.0
    opex_items_y2 = [35000.0, 120000.0, 22000.0, 24000.0, 24000.0]
    total_opex_y2 = sum(opex_items_y2)
    assert total_opex_y2 == 225000.0, f"OPEX Año 2 incorrecto: {total_opex_y2} != 225000.0"
    ebit_y2 = ingresos_y2 - total_opex_y2
    assert ebit_y2 == 99000.0, f"EBIT Año 2 incorrecto: {ebit_y2} != 99000.0"
    # Amortización de pérdida fiscal del Año 1 (-$32,000)
    taxable_base_y2 = ebit_y2 - abs(fen_y1)
    assert taxable_base_y2 == 67000.0, f"Base gravable Año 2 incorrecta: {taxable_base_y2} != 67000.0"
    tax_y2 = taxable_base_y2 * 0.30
    assert tax_y2 == 20100.0, f"ISR Año 2 incorrecto: {tax_y2} != 20100.0"
    fen_y2 = ebit_y2 - tax_y2
    assert fen_y2 == 78900.0, f"FEN Año 2 incorrecto: {fen_y2} != 78900.0"

    # Año 3
    ingresos_y3 = 850000.0
    opex_items_y3 = [65000.0, 240000.0, 45000.0, 36000.0, 40000.0]
    total_opex_y3 = sum(opex_items_y3)
    assert total_opex_y3 == 426000.0, f"OPEX Año 3 incorrecto: {total_opex_y3} != 426000.0"
    ebit_y3 = ingresos_y3 - total_opex_y3
    assert ebit_y3 == 424000.0, f"EBIT Año 3 incorrecto: {ebit_y3} != 424000.0"
    tax_y3 = ebit_y3 * 0.30
    assert tax_y3 == 127200.0, f"ISR Año 3 incorrecto: {tax_y3} != 127200.0"
    fen_y3 = ebit_y3 - tax_y3
    assert fen_y3 == 296800.0, f"FEN Año 3 incorrecto: {fen_y3} != 296800.0"

if __name__ == "__main__":
    test_capex_budget_breakdown()
    test_year1_contracts_and_revenue()
    test_financial_indicators_and_discounted_flows()
    test_investor_cash_sweep_and_profit_reconciliation()
    test_stepped_payroll_budget()
    test_investor_irr_at_5_years()
    test_viability_threshold_interpolation()
    test_proforma_income_statement_integrity()
    print("Todas las pruebas financieras han pasado exitosamente.")
