import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# Configurar estilo visual profesional
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#CBD5E1'
plt.rcParams['axes.linewidth'] = 0.8

COLOR_NAVY = '#1E3A8A'
COLOR_BLUE = '#2563EB'
COLOR_GREEN = '#10B981'
COLOR_DARK = '#0F172A'
COLOR_LIGHT_BG = '#F8FAFC'
COLOR_AMBER = '#F59E0B'
COLOR_RED = '#EF4444'

out_dir = os.path.join("docs", "graficos")
os.makedirs(out_dir, exist_ok=True)

# ==============================================================================
# FIGURA 1: DIAGRAMA DE FLUJO Y ARQUITECTURA DEL SERVICIO SIGRE
# ==============================================================================
def generate_figure_1():
    fig, ax = plt.subplots(figsize=(12, 6.5), dpi=300)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor(COLOR_LIGHT_BG)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 7)
    ax.axis('off')

    # Título principal del diagrama
    ax.text(6, 6.5, "Diagrama Operativo y de Arquitectura del Servicio SaaS SIGRE", 
            ha='center', va='center', fontsize=14, fontweight='bold', color=COLOR_DARK)
    ax.text(6, 6.15, "Flujo Integral de 5 Pasos: Desde la Pre-reserva Web hasta la Devolución y Trazabilidad Digital", 
            ha='center', va='center', fontsize=10, color='#64748B')

    steps = [
        ("Paso 1: Solicitud Web", "Pre-reserva y Módulo\nAnti-empalmes", "• Autenticación UdeG\n• Catálogo dinámico\n• Verificación cruces", COLOR_NAVY),
        ("Paso 2: Token QR", "Emisión de Código\nCifrado Dinámico", "• Token temporal 15m\n• Blindaje capturas\n• Notificación push/mail", COLOR_BLUE),
        ("Paso 3: Ventanilla", "Despacho Rápido\ny Doble Checklist", "• Escaneo QR <30 seg\n• Inspección física\n• Validación de estatus", COLOR_GREEN),
        ("Paso 4: Acta Digital", "Generación de PDF\ncon Validez Jurídica", "• Hash criptográfico\n• Firma digitalizada\n• Archivo en GCP Bucket", COLOR_AMBER),
        ("Paso 5: Devolución", "Cierre de Folio y\nScoring de Alumno", "• Cotejo de entrega\n• Actualiza reputación\n• Cierre sin libretas", COLOR_NAVY)
    ]

    box_width = 2.05
    box_height = 4.2
    y_pos = 1.3

    for i, (title, subtitle, details, color) in enumerate(steps):
        x_pos = 0.5 + i * 2.3
        
        # Sombra de la caja
        shadow = patches.FancyBboxPatch((x_pos + 0.04, y_pos - 0.04), box_width, box_height,
                                        boxstyle="round,pad=0.08,rounding_size=0.15",
                                        facecolor='#E2E8F0', edgecolor='none')
        ax.add_patch(shadow)
        
        # Caja principal
        box = patches.FancyBboxPatch((x_pos, y_pos), box_width, box_height,
                                     boxstyle="round,pad=0.08,rounding_size=0.15",
                                     facecolor='#FFFFFF', edgecolor=color, linewidth=1.8)
        ax.add_patch(box)
        
        # Encabezado coloreado
        header_box = patches.FancyBboxPatch((x_pos, y_pos + box_height - 0.9), box_width, 0.9,
                                           boxstyle="round,pad=0.08,rounding_size=0.15",
                                           facecolor=color, edgecolor='none')
        ax.add_patch(header_box)
        
        ax.text(x_pos + box_width/2, y_pos + box_height - 0.45, title,
                ha='center', va='center', fontsize=9.5, fontweight='bold', color='#FFFFFF')
        
        # Subtítulo funcional
        ax.text(x_pos + box_width/2, y_pos + box_height - 1.4, subtitle,
                ha='center', va='center', fontsize=9, fontweight='bold', color=COLOR_DARK)
        
        # Línea divisoria
        ax.plot([x_pos + 0.2, x_pos + box_width - 0.2], [y_pos + box_height - 1.9, y_pos + box_height - 1.9],
                color='#CBD5E1', linewidth=0.8)
        
        # Detalles
        ax.text(x_pos + 0.2, y_pos + box_height - 2.8, details,
                ha='left', va='top', fontsize=8, color='#334155', linespacing=1.6)

        # Flecha conectora entre pasos
        if i < len(steps) - 1:
            ax.annotate('', xy=(x_pos + box_width + 0.22, y_pos + box_height / 2),
                        xytext=(x_pos + box_width + 0.02, y_pos + box_height / 2),
                        arrowprops=dict(facecolor=COLOR_BLUE, edgecolor=COLOR_BLUE, width=2, headwidth=6))

    # Pie de infraestructura tecnológica
    ax.text(6, 0.6, "Infraestructura Base de Soporte: Google Cloud Platform (Cloud Run, PostgreSQL Cloud SQL, Cloud Storage)",
            ha='center', va='center', fontsize=8.5, fontstyle='italic', color='#64748B')
    ax.text(6, 0.3, "Cumplimiento normativo: Ley General de Protección de Datos Personales en Posesión de Sujetos Obligados (LGPDPPSO)",
            ha='center', va='center', fontsize=8, color='#94A3B8')

    plt.tight_layout()
    fig_path = os.path.join(out_dir, "figura1_diagrama_servicio_sigre.png")
    plt.savefig(fig_path, bbox_inches='tight')
    plt.close()
    print(f"Figura 1 creada: {fig_path}")

# ==============================================================================
# FIGURA 2: GRÁFICO DE PARETO (80/20) DE CRITERIOS Y ESTRUCTURA DE COSTOS
# ==============================================================================
def generate_figure_2():
    categories = [
        "Capital Humano\n(Desarrollo y Soporte)",
        "Insumos Cloud / TI\n(GCP Run, SQL, Storage)",
        "Servicios Operativos\n(Red, Luz, Traslados)",
        "Cumplimiento Legal\n(LGPDPPSO / INDAUTOR)"
    ]
    costs = [10833.33, 3093.33, 2500.00, 1833.33]
    total_cost = sum(costs)
    percentages = [c / total_cost * 100 for c in costs]
    cumulative = np.cumsum(percentages)

    fig, ax1 = plt.subplots(figsize=(10, 6), dpi=300)
    fig.patch.set_facecolor('#FFFFFF')
    ax1.set_facecolor('#FFFFFF')

    # Barras de costos
    colors = [COLOR_NAVY, COLOR_BLUE, COLOR_GREEN, COLOR_AMBER]
    bars = ax1.bar(categories, costs, color=colors, width=0.55, edgecolor='#0F172A', linewidth=0.8, zorder=3)
    ax1.set_ylabel("Costo Mensual por Partida (MXN)", fontsize=11, fontweight='bold', color=COLOR_DARK)
    ax1.set_ylim(0, 13500)
    ax1.grid(axis='y', linestyle='--', alpha=0.5, zorder=0)

    # Etiquetas de valor en barras
    for bar, cost, pct in zip(bars, costs, percentages):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width() / 2, height + 250,
                 f"${cost:,.2f}\n({pct:.1f}%)", ha='center', va='bottom',
                 fontsize=9, fontweight='bold', color=COLOR_DARK)

    # Eje secundario para la curva acumulada de Pareto
    ax2 = ax1.twinx()
    ax2.plot(categories, cumulative, color=COLOR_RED, marker='o', linewidth=2.2, markersize=7, zorder=4)
    ax2.set_ylabel("Porcentaje Acumulado (%)", fontsize=11, fontweight='bold', color=COLOR_RED)
    ax2.set_ylim(0, 110)

    # Línea de referencia del 80% (Ley de Pareto)
    ax2.axhline(80, color=COLOR_RED, linestyle=':', linewidth=1.5, alpha=0.8)
    ax2.text(2.55, 82, "Umbral Pareto 80%", color=COLOR_RED, fontsize=9, fontweight='bold')

    for i, cum in enumerate(cumulative):
        ax2.annotate(f"{cum:.1f}%", (i, cum), textcoords="offset points", xytext=(0, 10),
                     ha='center', fontsize=9, fontweight='bold', color=COLOR_RED)

    plt.title("Diagrama de Pareto de Estructura de Costos del Servicio SIGRE (Lote 100 Unidades)\n"
              "Identificación de Criterios Críticos: El 76.3% del costo radica en Talento y Nube (90.0% con Servicios)",
              fontsize=12, fontweight='bold', color=COLOR_DARK, pad=15)

    plt.tight_layout()
    fig_path = os.path.join(out_dir, "figura2_grafico_pareto_criterios_costo.png")
    plt.savefig(fig_path, bbox_inches='tight')
    plt.close()
    print(f"Figura 2 creada: {fig_path}")

# ==============================================================================
# FIGURA 3: ECONOMÍAS DE ESCALA Y PUNTO DE EQUILIBRIO
# ==============================================================================
def generate_figure_3():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6), dpi=300)
    fig.patch.set_facecolor('#FFFFFF')

    # Datos para economías de escala
    volumes = np.array([1, 5, 10, 20, 30, 35, 50, 75, 100])
    fixed_cost = 15166.67  # Sueldos (10.83k) + Servicios (2.5k) + Permisos/Normatividad (1.83k)
    variable_cost_per_unit = 26.6667  # Materia prima cloud por unidad sin IVA (30.93 con IVA)
    
    total_costs = fixed_cost + variable_cost_per_unit * volumes
    unit_costs = total_costs / volumes

    price_without_iva = 456.50
    price_with_iva = 529.54

    # Panel 1: Curva de Economía de Escala (Costo Unitario vs Volumen)
    ax1.plot(volumes, unit_costs, color=COLOR_NAVY, marker='s', linewidth=2.2, label='Costo Medio Unitario')
    ax1.axhline(price_without_iva, color=COLOR_GREEN, linestyle='--', linewidth=1.8, label=f'Precio Venta s/IVA (${price_without_iva:,.2f})')
    ax1.axvline(35, color=COLOR_RED, linestyle=':', linewidth=1.5, label='Punto de Equilibrio (Q = 35)')

    ax1.set_title("Economías de Escala:\nCosto Unitario Decreciente por Volumen", fontsize=11, fontweight='bold', color=COLOR_DARK)
    ax1.set_xlabel("Volumen de Dependencias / Licencias Atendidas", fontsize=10, fontweight='bold')
    ax1.set_ylabel("Costo Unitario Promedio (MXN)", fontsize=10, fontweight='bold')
    ax1.set_ylim(0, 3500)
    ax1.set_xlim(0, 105)
    ax1.grid(True, linestyle='--', alpha=0.5)
    ax1.legend(loc='upper right', fontsize=8.5)

    ax1.annotate(f"Q=1: ${unit_costs[0]:,.0f}\n(Pérdida)", xy=(1, 3200), xytext=(8, 3000),
                 arrowprops=dict(arrowstyle="->", color=COLOR_RED), fontsize=8.5, color=COLOR_RED, fontweight='bold')
    ax1.annotate(f"Q=100: ${unit_costs[-1]:,.2f}\n(Margen 60%)", xy=(100, unit_costs[-1]), xytext=(65, 800),
                 arrowprops=dict(arrowstyle="->", color=COLOR_GREEN), fontsize=8.5, color=COLOR_GREEN, fontweight='bold')

    # Panel 2: Gráfico de Punto de Equilibrio (Ingresos vs Costos Totales)
    vol_grid = np.linspace(0, 100, 101)
    tot_costs_grid = fixed_cost + variable_cost_per_unit * vol_grid
    revenues_grid = price_without_iva * vol_grid

    ax2.plot(vol_grid, revenues_grid, color=COLOR_GREEN, linewidth=2.2, label='Ingresos Totales (sin IVA)')
    ax2.plot(vol_grid, tot_costs_grid, color=COLOR_RED, linewidth=2.2, label='Costos Totales (Fijos + Variables)')
    ax2.axhline(fixed_cost, color='#64748B', linestyle='--', linewidth=1.2, label=f'Costos Fijos (${fixed_cost:,.0f})')

    # Punto de corte
    be_units = fixed_cost / (price_without_iva - variable_cost_per_unit)
    be_revenue = be_units * price_without_iva
    ax2.plot(be_units, be_revenue, marker='o', markersize=9, color=COLOR_DARK, zorder=5)
    ax2.annotate(f"P.E. Exacto:\nQ = {be_units:.1f} dependencias\nVentas: ${be_revenue:,.2f}",
                 xy=(be_units, be_revenue), xytext=(be_units - 15, be_revenue + 12000),
                 arrowprops=dict(arrowstyle="->", color=COLOR_DARK, lw=1.5),
                 fontsize=9, fontweight='bold', bbox=dict(boxstyle="round,pad=0.4", fc="#FEF3C7", ec="#F59E0B"))

    # Zonas de pérdida y utilidad
    ax2.fill_between(vol_grid, tot_costs_grid, revenues_grid, where=(revenues_grid < tot_costs_grid),
                     color='#FEE2E2', alpha=0.5, label='Zona de Déficit Operativo')
    ax2.fill_between(vol_grid, tot_costs_grid, revenues_grid, where=(revenues_grid >= tot_costs_grid),
                     color='#D1FAE5', alpha=0.5, label='Zona de Utilidad Neta')

    ax2.set_title("Análisis Gráfico del Punto de Equilibrio\n(Determinación de Producción Mínima Competitiva)", fontsize=11, fontweight='bold', color=COLOR_DARK)
    ax2.set_xlabel("Volumen de Dependencias / Licencias Atendidas", fontsize=10, fontweight='bold')
    ax2.set_ylabel("Monto Financiero Mensual (MXN)", fontsize=10, fontweight='bold')
    ax2.set_ylim(0, 55000)
    ax2.set_xlim(0, 105)
    ax2.grid(True, linestyle='--', alpha=0.5)
    ax2.legend(loc='lower right', fontsize=8.5)

    plt.tight_layout()
    fig_path = os.path.join(out_dir, "figura3_curva_economias_escala_punto_equilibrio.png")
    plt.savefig(fig_path, bbox_inches='tight')
    plt.close()
    print(f"Figura 3 creada: {fig_path}")

if __name__ == "__main__":
    generate_figure_1()
    generate_figure_2()
    generate_figure_3()
