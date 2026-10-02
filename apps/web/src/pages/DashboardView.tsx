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
} from 'lucide-react';
import { api } from '../api/client';
import type { DashboardStats } from '../types';

export const DashboardView: React.FC = () => {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [loading, setLoading] = useState(true);

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

  return (
    <div className="view-container">
      {/* Encabezado */}
      <div className="section-header">
        <div>
          <h2 className="section-title">Panel Ejecutivo & Métrica Operativa</h2>
          <p className="section-subtitle">
            Monitoreo en tiempo real de infraestructura, flota de laboratorios y ocupación en CUTonalá.
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
          <p className="text-secondary mt-3">Calculando métricas del campus...</p>
        </div>
      ) : !stats ? (
        <div className="alert-box alert-error">No se pudieron cargar las estadísticas operativas.</div>
      ) : (
        <>
          {/* Tarjetas Resumen */}
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
