import React, { useState, useEffect } from 'react';
import {
  Building2,
  Package,
  CalendarCheck,
  AlertTriangle,
  Clock,
  TrendingUp,
  Activity,
  Cpu,
  RefreshCw,
  DollarSign,
  Scale,
  ShieldCheck,
  PieChart,
  ArrowUpRight,
  CheckCircle2,
} from 'lucide-react';
import { api } from '../api/client';
import type { DashboardStats, EvaluacionInversion } from '../types';

export const DashboardView: React.FC = () => {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [activeFinancialTab, setActiveFinancialTab] = useState<'flujo' | 'capex' | 'patrimonio'>('flujo');

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      setLoading(true);
      const data = await api.dashboard.getStats();
      setStats(data);
    } catch (err: any) {
      console.error('Error al cargar dashboard:', err);
    } finally {
      setLoading(false);
    }
  };

  const getRiesgoBadge = (riesgo: 'BAJO' | 'MEDIO' | 'ALTO') => {
    switch (riesgo) {
      case 'ALTO':
        return <span className="badge badge-error">Riesgo Alto</span>;
      case 'MEDIO':
        return <span className="badge badge-warning">Riesgo Medio</span>;
      default:
        return <span className="badge badge-accent">Óptimo (Bajo)</span>;
    }
  };

  const formatMxn = (val: number) => {
    return new Intl.NumberFormat('es-MX', {
      style: 'currency',
      currency: 'MXN',
      maximumFractionDigits: 2,
    }).format(val);
  };

  // Fallback seguro con los datos oficiales de la investigación financiera
  const evaluacion: EvaluacionInversion = stats?.evaluacionInversion || {
    capexTotal: 140000,
    capexDesglose: [
      { concepto: 'Desarrollo MVP & Pruebas', monto: 60000, descripcion: 'Ingeniería de software, módulos de firma digital y checklist de control' },
      { concepto: 'Infraestructura Cloud GCP (Año 1)', monto: 16000, descripcion: 'Cloud SQL PostgreSQL, Redis Memorystore, GCS y Cloud Run' },
      { concepto: 'Lectores Ópticos Industriales (3 Almacenes)', monto: 20000, descripcion: 'Hardware QR / código de barras Dell de uso rudo para ventanillas' },
      { concepto: 'Marco Legal, Privacidad & INDAUTOR', monto: 12000, descripcion: 'Aviso de Privacidad Ley General y depósito de derechos de autor' },
      { concepto: 'Señalética & Viáticos CUTonalá', monto: 12000, descripcion: 'Rotulación institucional, señalética QR y logística de campus' },
      { concepto: 'Fondo de Contingencia Operativa', monto: 20000, descripcion: 'Reserva para imprevistos técnicos o reabastecimiento de repuestos' }
    ],
    tmarPorcentaje: 15.0,
    vpnMxn: 23790.58,
    tirPorcentaje: 21.34,
    paybackMesesSimple: 29.6,
    paybackMesesDescontado: 34.0,
    puntoEquilibrioMeses: 15,
    relacionBeneficioCosto: 1.15,
    flujoTrienal: [
      { periodo: 'Año 0', fase: 'Inversión Inicial Semilla', planteles: 'Planeación & Setup', ingresos: 0, egresos: 140000, flujoNeto: -140000, flujoAcumulado: -140000 },
      { periodo: 'Año 1', fase: 'Piloto Controlado', planteles: 'CUTonalá (3 almacenes)', ingresos: 48000, egresos: 70000, flujoNeto: -22000, flujoAcumulado: -162000 },
      { periodo: 'Año 2', fase: 'Expansión Temática', planteles: 'CUTonalá + CUCEI', ingresos: 160000, egresos: 92000, flujoNeto: 68000, flujoAcumulado: -94000 },
      { periodo: 'Año 3', fase: 'Consolidación Red', planteles: '3 Centros + 1 Preparatoria', ingresos: 340000, egresos: 140000, flujoNeto: 200000, flujoAcumulado: 106000 }
    ],
    impactoPatrimonial: {
      reduccionMermasPorcentaje: 80,
      eliminacionEmpalmesPorcentaje: 100,
      tiempoDespachoSegundos: 28,
      tiempoDespachoAnteriorMinutos: 15,
      ahorroEstimadoMermasMxn: 148500
    }
  };

  return (
    <div className="view-container">
      {/* Encabezado General */}
      <div className="section-header">
        <div>
          <h2 className="section-title">Panel Ejecutivo & Métrica Operativa</h2>
          <p className="section-subtitle">
            Monitoreo en tiempo real de infraestructura, flota de laboratorios y viabilidad financiera del proyecto en CUTonalá.
          </p>
        </div>

        <button
          type="button"
          onClick={fetchStats}
          className="btn btn-secondary flex items-center gap-2"
        >
          <RefreshCw size={15} />
          Actualizar Indicadores
        </button>
      </div>

      {loading ? (
        <div className="loading-state">
          <div className="spinner"></div>
          <p className="text-secondary mt-3">Calculando métricas del campus y flujos financieros...</p>
        </div>
      ) : !stats ? (
        <div className="alert-box alert-error">No se pudieron cargar las estadísticas operativas.</div>
      ) : (
        <>
          {/* ══════════════ MÓDULO DE EVALUACIÓN FINANCIERA & ROI ══════════════ */}
          <div className="financial-banner">
            <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-3">
              <div>
                <div className="flex items-center gap-2">
                  <span className="badge-financial-pill">
                    <CheckCircle2 size={13} />
                    Proyecto Viable
                  </span>
                  <span className="text-xs text-white opacity-80">
                    TMAR Evaluada: {evaluacion.tmarPorcentaje}% Anual (Cetes 10.5% + 4.5% Riesgo)
                  </span>
                </div>
                <h3 className="text-xl font-bold mt-1 text-white">
                  Evaluación Financiera & Retorno de Inversión (SIGRE)
                </h3>
                <p className="text-xs text-white opacity-80 max-w-3xl mt-1">
                  Modelo matemático de rentabilidad y proyecciones proforma trienales formulado para la Red Universitaria UdeG.
                </p>
              </div>

              <div className="flex items-center gap-2 bg-white bg-opacity-10 px-3 py-1.5 rounded-lg border border-white border-opacity-20">
                <Scale size={16} className="text-emerald-300" />
                <span className="text-xs font-semibold text-white">Punto de Equilibrio: Mes 15</span>
              </div>
            </div>

            {/* Grid de KPIs Financieros */}
            <div className="financial-grid">
              {/* VPN */}
              <div className="financial-kpi-card">
                <div className="financial-kpi-header">
                  <span className="financial-kpi-title">Valor Presente Neto (VPN)</span>
                  <ArrowUpRight size={16} className="text-emerald-400" />
                </div>
                <div className="financial-kpi-value text-emerald-300">
                  +{formatMxn(evaluacion.vpnMxn)}
                </div>
                <div className="financial-kpi-sub flex justify-between items-center">
                  <span>Flujo descontado positivo</span>
                  <span className="badge-financial-pill text-[10px]">Aceptado</span>
                </div>
              </div>

              {/* TIR */}
              <div className="financial-kpi-card">
                <div className="financial-kpi-header">
                  <span className="financial-kpi-title">Tasa Interna Retorno (TIR)</span>
                  <TrendingUp size={16} className="text-teal-300" />
                </div>
                <div className="financial-kpi-value text-teal-200">
                  {evaluacion.tirPorcentaje}%
                </div>
                <div className="financial-kpi-sub flex justify-between items-center">
                  <span>TIR &gt; TMAR ({evaluacion.tmarPorcentaje}%)</span>
                  <span className="badge-financial-pill text-[10px]">+6.34% spread</span>
                </div>
              </div>

              {/* CAPEX */}
              <div className="financial-kpi-card">
                <div className="financial-kpi-header">
                  <span className="financial-kpi-title">Inversión Inicial (CAPEX)</span>
                  <DollarSign size={16} className="text-amber-300" />
                </div>
                <div className="financial-kpi-value text-amber-100">
                  {formatMxn(evaluacion.capexTotal)}
                </div>
                <div className="financial-kpi-sub flex justify-between items-center">
                  <span>Capital semilla total</span>
                  <span className="text-white opacity-70 text-[11px]">6 rubros clave</span>
                </div>
              </div>

              {/* Payback */}
              <div className="financial-kpi-card">
                <div className="financial-kpi-header">
                  <span className="financial-kpi-title">Periodo de Recuperación</span>
                  <Clock size={16} className="text-cyan-300" />
                </div>
                <div className="financial-kpi-value text-cyan-200">
                  Mes {evaluacion.paybackMesesSimple}
                </div>
                <div className="financial-kpi-sub flex justify-between items-center">
                  <span>Payback descontado: Mes {evaluacion.paybackMesesDescontado}</span>
                  <span className="text-white opacity-70 text-[11px]">2.47 años</span>
                </div>
              </div>

              {/* Relación B/C */}
              <div className="financial-kpi-card">
                <div className="financial-kpi-header">
                  <span className="financial-kpi-title">Relación Beneficio / Costo</span>
                  <Scale size={16} className="text-indigo-300" />
                </div>
                <div className="financial-kpi-value text-indigo-200">
                  {evaluacion.relacionBeneficioCosto}x
                </div>
                <div className="financial-kpi-sub flex justify-between items-center">
                  <span>Retorno por cada peso invertido</span>
                  <span className="badge-financial-pill text-[10px]">+15% margen</span>
                </div>
              </div>
            </div>
          </div>

          {/* Sub-tarjetas de detalle financiero interactivo */}
          <div className="card mb-6">
            <div className="card-header flex justify-between items-center">
              <div className="flex items-center gap-2">
                <PieChart size={18} className="text-accent" />
                <h3 className="card-title text-base">
                  Desglose Detallado de Viabilidad Financiera & Retorno Social
                </h3>
              </div>

              {/* Sub-tabs switcher */}
              <div className="flex gap-1 bg-muted p-1 rounded-lg">
                <button
                  type="button"
                  onClick={() => setActiveFinancialTab('flujo')}
                  className={`px-3 py-1 rounded text-xs font-semibold transition ${
                    activeFinancialTab === 'flujo'
                      ? 'bg-surface text-primary shadow-sm'
                      : 'text-secondary hover:text-primary'
                  }`}
                >
                  Flujo Trienal Proforma
                </button>
                <button
                  type="button"
                  onClick={() => setActiveFinancialTab('capex')}
                  className={`px-3 py-1 rounded text-xs font-semibold transition ${
                    activeFinancialTab === 'capex'
                      ? 'bg-surface text-primary shadow-sm'
                      : 'text-secondary hover:text-primary'
                  }`}
                >
                  Presupuesto CAPEX ($140k)
                </button>
                <button
                  type="button"
                  onClick={() => setActiveFinancialTab('patrimonio')}
                  className={`px-3 py-1 rounded text-xs font-semibold transition ${
                    activeFinancialTab === 'patrimonio'
                      ? 'bg-surface text-primary shadow-sm'
                      : 'text-secondary hover:text-primary'
                  }`}
                >
                  Ahorro Patrimonial UdeG
                </button>
              </div>
            </div>

            <div className="card-body">
              {activeFinancialTab === 'flujo' && (
                <div className="table-responsive">
                  <table className="table">
                    <thead>
                      <tr>
                        <th>Periodo</th>
                        <th>Fase Estratégica</th>
                        <th>Cobertura de Centros</th>
                        <th className="text-right">Ingresos Proyectados</th>
                        <th className="text-right">Egresos Operativos</th>
                        <th className="text-right">Flujo Neto</th>
                        <th className="text-right">Flujo Acumulado</th>
                        <th>Estado de Rentabilidad</th>
                      </tr>
                    </thead>
                    <tbody>
                      {evaluacion.flujoTrienal.map((row) => (
                        <tr key={row.periodo}>
                          <td className="font-bold text-primary">{row.periodo}</td>
                          <td className="text-xs font-medium">{row.fase}</td>
                          <td className="text-xs text-secondary">{row.planteles}</td>
                          <td className="text-right font-mono text-xs text-success font-semibold">
                            {formatMxn(row.ingresos)}
                          </td>
                          <td className="text-right font-mono text-xs text-secondary">
                            {formatMxn(row.egresos)}
                          </td>
                          <td
                            className={`text-right font-mono text-xs font-bold ${
                              row.flujoNeto >= 0 ? 'text-success' : 'text-error'
                            }`}
                          >
                            {row.flujoNeto >= 0 ? '+' : ''}
                            {formatMxn(row.flujoNeto)}
                          </td>
                          <td
                            className={`text-right font-mono text-xs font-bold ${
                              row.flujoAcumulado >= 0 ? 'text-accent' : 'text-secondary'
                            }`}
                          >
                            {row.flujoAcumulado >= 0 ? '+' : ''}
                            {formatMxn(row.flujoAcumulado)}
                          </td>
                          <td>
                            {row.flujoAcumulado >= 0 ? (
                              <span className="badge badge-accent">Superávit Consolidado</span>
                            ) : row.flujoNeto > 0 ? (
                              <span className="badge badge-warning">En Recuperación Activa</span>
                            ) : (
                              <span className="badge badge-secondary">Inversión & Piloto</span>
                            )}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                  <div className="mt-3 p-3 bg-muted rounded-md text-xs text-secondary flex items-center justify-between">
                    <span>
                      * <strong>Punto de Equilibrio:</strong> Se logra en el mes 15 de operación (Año 2). La pérdida inicial de $22,000 en el Año 1 es amortizada íntegramente por el capital semilla de contingencia.
                    </span>
                    <span className="font-bold text-accent">Payback Simple: Mes 29.6</span>
                  </div>
                </div>
              )}

              {activeFinancialTab === 'capex' && (
                <div>
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    {evaluacion.capexDesglose.map((item, idx) => {
                      const porcentaje = ((item.monto / evaluacion.capexTotal) * 100).toFixed(1);
                      return (
                        <div key={idx} className="p-4 bg-muted rounded-lg border border-default flex flex-col justify-between">
                          <div>
                            <div className="flex justify-between items-start">
                              <span className="text-xs font-bold text-accent">Rubro {idx + 1}</span>
                              <span className="badge badge-secondary text-xs">{porcentaje}% del CAPEX</span>
                            </div>
                            <h4 className="text-sm font-bold text-primary mt-1">{item.concepto}</h4>
                            <p className="text-xs text-secondary mt-1">{item.descripcion}</p>
                          </div>
                          <div className="mt-3 pt-2 border-t border-default flex justify-between items-center">
                            <span className="text-xs text-muted">Monto Presupuestado</span>
                            <span className="font-mono text-sm font-bold text-primary">{formatMxn(item.monto)}</span>
                          </div>
                        </div>
                      );
                    })}
                  </div>
                  <div className="mt-4 p-3 bg-accent-soft rounded-lg text-xs text-primary flex justify-between items-center">
                    <span>Presupuesto austero formulado con investigación comparativa de 3 proveedores por cada rubro (Google Cloud, Dell Technologies, Asesoría Especializada INDAUTOR).</span>
                    <strong className="font-mono text-sm font-bold text-accent">Total: {formatMxn(evaluacion.capexTotal)}</strong>
                  </div>
                </div>
              )}

              {activeFinancialTab === 'patrimonio' && (
                <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                  <div className="p-4 bg-muted rounded-lg border border-default text-center">
                    <ShieldCheck size={28} className="text-success mx-auto mb-2" />
                    <div className="text-2xl font-bold font-mono text-success">
                      -{evaluacion.impactoPatrimonial.reduccionMermasPorcentaje}%
                    </div>
                    <div className="text-xs font-semibold text-primary mt-1">Reducción de Mermas</div>
                    <p className="text-xs text-secondary mt-1">
                      Eliminación de pérdidas de accesorios y equipo gracias a actas PDF con firma digital y validación obligatoria.
                    </p>
                  </div>

                  <div className="p-4 bg-muted rounded-lg border border-default text-center">
                    <CheckCircle2 size={28} className="text-accent mx-auto mb-2" />
                    <div className="text-2xl font-bold font-mono text-accent">
                      {evaluacion.impactoPatrimonial.eliminacionEmpalmesPorcentaje}%
                    </div>
                    <div className="text-xs font-semibold text-primary mt-1">Eliminación de Empalmes</div>
                    <p className="text-xs text-secondary mt-1">
                      Sincronización de disponibilidad en tiempo real para auditorios, cineteca y laboratorios sin conflictos de agenda.
                    </p>
                  </div>

                  <div className="p-4 bg-muted rounded-lg border border-default text-center">
                    <Clock size={28} className="text-info mx-auto mb-2" />
                    <div className="text-2xl font-bold font-mono text-info">
                      &lt; {evaluacion.impactoPatrimonial.tiempoDespachoSegundos}s
                    </div>
                    <div className="text-xs font-semibold text-primary mt-1">Despacho en Ventanilla</div>
                    <p className="text-xs text-secondary mt-1">
                      Reducción drástica del tiempo de atención en almacén frente a los {evaluacion.impactoPatrimonial.tiempoDespachoAnteriorMinutos} minutos promedio del sistema tradicional en papel.
                    </p>
                  </div>

                  <div className="p-4 bg-muted rounded-lg border border-default text-center">
                    <DollarSign size={28} className="text-warning mx-auto mb-2" />
                    <div className="text-2xl font-bold font-mono text-warning">
                      +{formatMxn(evaluacion.impactoPatrimonial.ahorroEstimadoMermasMxn)}
                    </div>
                    <div className="text-xs font-semibold text-primary mt-1">Ahorro Institucional Acumulado</div>
                    <p className="text-xs text-secondary mt-1">
                      Estimación de costos directos evitados en reposición de equipo de cómputo y horas-hombre administrativas.
                    </p>
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* ══════════════ PANEL OPERATIVO TRADICIONAL & FLOTA ══════════════ */}
          <div className="flex justify-between items-center mb-3">
            <h3 className="text-sm font-bold text-secondary uppercase tracking-wider flex items-center gap-2">
              <Building2 size={16} />
              Monitoreo Operativo de Instalaciones & Flota CUTonalá
            </h3>
            <span className="text-xs text-muted">Datos sincronizados con Cloud SQL</span>
          </div>

          {/* Tarjetas Resumen (Métricas requeridas por Playwright test 8) */}
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4 mb-6">
            <div className="kpi-card">
              <div className="kpi-icon-wrapper bg-primary-soft text-primary">
                <Building2 size={20} />
              </div>
              <div className="kpi-value">{stats.resumen.totalEspacios}</div>
              <div className="kpi-label">Espacios Físicos</div>
            </div>

            <div className="kpi-card">
              <div className="kpi-icon-wrapper bg-accent-soft text-accent">
                <Package size={20} />
              </div>
              <div className="kpi-value">{stats.resumen.totalRecursos}</div>
              <div className="kpi-label">Bienes de Inventario</div>
            </div>

            <div className="kpi-card">
              <div className="kpi-icon-wrapper bg-info-soft text-info">
                <CalendarCheck size={20} />
              </div>
              <div className="kpi-value">{stats.resumen.reservasActivas}</div>
              <div className="kpi-label">Reservas Aprobadas</div>
            </div>

            <div className="kpi-card">
              <div className="kpi-icon-wrapper bg-success-soft text-success">
                <Activity size={20} />
              </div>
              <div className="kpi-value">{stats.resumen.prestamosActivos}</div>
              <div className="kpi-label">Préstamos en Curso</div>
            </div>

            <div className="kpi-card">
              <div className="kpi-icon-wrapper bg-warning-soft text-warning">
                <Clock size={20} />
              </div>
              <div className="kpi-value">{stats.resumen.reservasPendientesAprobacion}</div>
              <div className="kpi-label">Por Autorizar</div>
            </div>

            <div className="kpi-card">
              <div className="kpi-icon-wrapper bg-error-soft text-error">
                <AlertTriangle size={20} />
              </div>
              <div className="kpi-value">{stats.resumen.incidentesPendientes}</div>
              <div className="kpi-label">Incidentes Abiertos</div>
            </div>
          </div>

          {/* Matriz de Desgaste y Vida Útil */}
          <div className="card mb-6">
            <div className="card-header flex justify-between items-center">
              <div className="flex items-center gap-2">
                <Cpu size={18} className="text-accent" />
                <h3 className="card-title text-base">
                  Matriz de Desgaste de Flota y Riesgo Predictivo de Falla
                </h3>
              </div>
              <span className="badge badge-primary text-xs">Mantenimiento Preventivo</span>
            </div>

            <div className="table-responsive">
              <table className="table">
                <thead>
                  <tr>
                    <th>Placa / Folio</th>
                    <th>Bien Tecnológico</th>
                    <th>Categoría</th>
                    <th>Condición Física</th>
                    <th>Horas Uso</th>
                    <th>Préstamos</th>
                    <th>Diagnóstico Predictivo</th>
                  </tr>
                </thead>
                <tbody>
                  {stats.matrizDesgaste.map((item) => (
                    <tr key={item.id}>
                      <td className="font-mono text-xs font-bold text-accent">{item.codigo}</td>
                      <td className="font-medium text-primary">{item.nombre}</td>
                      <td className="text-xs">{item.categoria}</td>
                      <td>
                        <span className="badge badge-secondary text-xs">{item.condicion}</span>
                      </td>
                      <td className="font-mono text-xs">{item.horasUso} hrs</td>
                      <td className="font-mono text-xs">{item.vecesPrestado} veces</td>
                      <td>{getRiesgoBadge(item.riesgoFalla)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* Ocupación de Espacios en Vivo */}
          <div className="card">
            <div className="card-header flex justify-between items-center">
              <div className="flex items-center gap-2">
                <TrendingUp size={18} className="text-accent" />
                <h3 className="card-title text-base">Ocupación Diaria de Recintos en CUTonalá</h3>
              </div>
              <span className="text-xs text-muted">Jornada 08:00 - 19:00 hrs</span>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 p-4">
              {stats.ocupacionEspaciosHoy.map((esp) => (
                <div key={esp.id} className="p-3 bg-muted rounded-md border border-default">
                  <div className="flex justify-between items-start">
                    <strong className="text-sm text-primary">{esp.nombre}</strong>
                    <span
                      className={`status-dot ${
                        esp.ocupadoActualmente ? 'dot-occupied' : 'dot-available'
                      }`}
                      title={esp.ocupadoActualmente ? 'Ocupado actualmente' : 'Libre en este momento'}
                    />
                  </div>
                  <div className="text-xs text-secondary mt-1">{esp.edificio}</div>
                  <div className="flex justify-between items-center mt-3 text-xs">
                    <span className="text-muted">Capacidad: {esp.capacidad}</span>
                    <span className="font-bold text-accent">
                      {esp.reservasHoy} {esp.reservasHoy === 1 ? 'evento' : 'eventos'} hoy
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </>
      )}
    </div>
  );
};
