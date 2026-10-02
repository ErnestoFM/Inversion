import React, { useState, useEffect } from 'react';
import {
  AlertTriangle,
  ShieldAlert,
  Wrench,
  CheckCircle2,
  AlertCircle,
  PlusCircle,
  X,
  RotateCcw,
} from 'lucide-react';
import { api } from '../api/client';
import { useAuth } from '../context/AuthContext';
import type { Incident, Resource } from '../types';

export const IncidentsView: React.FC = () => {
  const { user, refreshUser } = useAuth();
  const [incidentes, setIncidentes] = useState<Incident[]>([]);
  const [recursos, setRecursos] = useState<Resource[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Modal para reportar nueva incidencia
  const [showReportModal, setShowReportModal] = useState(false);
  const [selectedRecursoId, setSelectedRecursoId] = useState<string>('');
  const [tipo, setTipo] = useState<string>('DAÑO_EQUIPO');
  const [gravedad, setGravedad] = useState<string>('LEVE');
  const [descripcion, setDescripcion] = useState<string>('');
  const [reportLoading, setReportLoading] = useState(false);

  // Modal para resolución o reparación supervisada
  const [selectedIncidentForResolve, setSelectedIncidentForResolve] = useState<Incident | null>(null);
  const [solucion, setSolucion] = useState<string>('');
  const [restaurarPuntos, setRestaurarPuntos] = useState<boolean>(true);
  const [resolveLoading, setResolveLoading] = useState(false);

  useEffect(() => {
    fetchIncidentes();
    fetchRecursos();
  }, []);

  const fetchIncidentes = async () => {
    try {
      setLoading(true);
      const res = await api.incidents.list();
      setIncidentes(res.incidentes);
    } catch (err: any) {
      setError(err.message || 'Error al cargar incidencias');
    } finally {
      setLoading(false);
    }
  };

  const fetchRecursos = async () => {
    try {
      const res = await api.resources.list();
      setRecursos(res.recursos);
    } catch (err: any) {
      console.error(err);
    }
  };

  const handleCreateIncident = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!descripcion.trim()) return;

    try {
      setReportLoading(true);
      const res = await api.incidents.report({
        recursoId: selectedRecursoId || undefined,
        tipo,
        gravedad,
        descripcion,
      });

      alert(
        `Incidencia registrada (Folio: ${res.incidente.folio}). Penalización de confianza: -${res.penalizacionAplicada} pts.`
      );
      setShowReportModal(false);
      setDescripcion('');
      fetchIncidentes();
      refreshUser();
    } catch (err: any) {
      alert(`Error al registrar incidencia: ${err.message}`);
    } finally {
      setReportLoading(false);
    }
  };

  const handleResolveIncident = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedIncidentForResolve) return;

    try {
      setResolveLoading(true);
      await api.incidents.resolve(
        selectedIncidentForResolve.id,
        solucion,
        restaurarPuntos
      );
      alert(
        `Incidencia resuelta.${
          restaurarPuntos
            ? ' Los puntos de reputación fueron restaurados al usuario tras su servicio supervisado.'
            : ''
        }`
      );
      setSelectedIncidentForResolve(null);
      setSolucion('');
      fetchIncidentes();
      refreshUser();
    } catch (err: any) {
      alert(`Error al resolver incidencia: ${err.message}`);
    } finally {
      setResolveLoading(false);
    }
  };

  const getGravedadBadge = (grav: string) => {
    switch (grav) {
      case 'GRAVE':
        return <span className="badge badge-error">Grave (-30 pts)</span>;
      case 'MODERADO':
        return <span className="badge badge-warning">Moderado (-15 pts)</span>;
      default:
        return <span className="badge badge-secondary">Leve (-5 pts)</span>;
    }
  };

  const isStaff = user?.rol === 'ADMIN' || user?.rol === 'COORDINADOR' || user?.rol === 'TECNICO_LAB';

  return (
    <div className="view-container">
      {/* Encabezado */}
      <div className="section-header">
        <div>
          <h2 className="section-title">Incidentes, Sanciones y Reparación Supervisada</h2>
          <p className="section-subtitle">
            Sistema de Confianza Institucional (Trust Score 0-100 pts) y restitución de bienes en CUTonalá.
          </p>
        </div>

        <button
          type="button"
          onClick={() => setShowReportModal(true)}
          className="btn btn-error flex items-center gap-2"
        >
          <PlusCircle size={16} />
          Reportar Daño o Incidencia
        </button>
      </div>

      {/* Explicación de Trust Score */}
      <div className="trust-score-banner">
        <div className="banner-icon-col">
          <ShieldAlert size={28} className="text-warning" />
        </div>
        <div className="text-xs leading-relaxed">
          <strong>Política de Confianza y Sanciones de CUTonalá:</strong> Cada integrante inicia con 100
          puntos de reputación. Los retrasos leves descuentan <strong>5 pts</strong>, daños moderados{' '}
          <strong>15 pts</strong> y daños graves o extravío <strong>30 pts</strong>. Si la puntuación
          baja de 70 pts, el sistema inhabilita nuevos préstamos hasta realizar una{' '}
          <strong>Reparación Supervisada</strong> o servicio comunitario en laboratorios.
        </div>
      </div>

      {loading ? (
        <div className="loading-state">
          <div className="spinner"></div>
          <p className="text-secondary mt-3">Cargando incidencias registradas...</p>
        </div>
      ) : error ? (
        <div className="alert-box alert-error">
          <AlertCircle size={20} />
          <div>{error}</div>
        </div>
      ) : incidentes.length === 0 ? (
        <div className="empty-state">
          <CheckCircle2 size={48} className="text-accent" />
          <h3 className="mt-3 font-semibold">Todo en Orden en el Campus</h3>
          <p className="text-secondary text-sm">
            No hay incidencias ni reportes de daños pendientes en CUTonalá.
          </p>
        </div>
      ) : (
        <div className="table-responsive card">
          <table className="table">
            <thead>
              <tr>
                <th>Folio</th>
                <th>Tipo & Gravedad</th>
                <th>Descripción</th>
                <th>Equipo / Recurso</th>
                <th>Usuario</th>
                <th>Estado</th>
                {isStaff && <th>Acción Laboratorio</th>}
              </tr>
            </thead>
            <tbody>
              {incidentes.map((inc) => (
                <tr key={inc.id}>
                  <td className="font-mono text-xs font-bold text-accent">{inc.folio}</td>
                  <td>
                    <div className="font-semibold text-xs mb-1">{inc.tipo}</div>
                    {getGravedadBadge(inc.gravedad)}
                  </td>
                  <td className="text-xs max-w-sm">{inc.descripcion}</td>
                  <td className="text-xs">
                    {inc.recurso ? (
                      <div>
                        <strong>{inc.recurso.nombre}</strong>
                        <div className="font-mono text-muted">{inc.recurso.codigoInventario}</div>
                      </div>
                    ) : (
                      <span className="text-muted">Espacio General</span>
                    )}
                  </td>
                  <td className="text-xs">
                    <span className="font-medium text-primary">
                      {inc.usuarioInfractor?.nombre}
                    </span>
                    <div className="text-muted font-mono">{inc.usuarioInfractor?.codigo}</div>
                  </td>
                  <td>
                    <span
                      className={`badge ${
                        inc.estado === 'RESUELTA'
                          ? 'badge-accent'
                          : inc.estado === 'REPARACION_SUPERVISADA'
                          ? 'badge-warning'
                          : 'badge-error'
                      }`}
                    >
                      {inc.estado}
                    </span>
                  </td>
                  {isStaff && (
                    <td>
                      {inc.estado !== 'RESUELTA' && (
                        <button
                          type="button"
                          onClick={() => {
                            setSelectedIncidentForResolve(inc);
                            setSolucion(
                              'Equipo reparado y calibrado por el usuario bajo supervisión de laboratorio.'
                            );
                          }}
                          className="btn btn-secondary btn-xs flex items-center gap-1"
                        >
                          <Wrench size={13} />
                          Reparación
                        </button>
                      )}
                    </td>
                  )}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* Modal para Reportar Incidencia */}
      {showReportModal && (
        <div className="modal-backdrop">
          <div className="modal-container max-w-lg">
            <div className="modal-header">
              <div className="flex items-center gap-2">
                <AlertTriangle size={20} className="text-error" />
                <h3 className="modal-title">Reportar Incidencia o Desperfecto</h3>
              </div>
              <button
                onClick={() => setShowReportModal(false)}
                className="modal-close-btn"
                aria-label="Cerrar modal"
              >
                <X size={18} />
              </button>
            </div>

            <form onSubmit={handleCreateIncident}>
              <div className="modal-body space-y-4">
                <div>
                  <label className="input-label">Equipo Relacionado</label>
                  <select
                    value={selectedRecursoId}
                    onChange={(e) => setSelectedRecursoId(e.target.value)}
                    className="input-select w-full"
                  >
                    <option value="">(Ninguno / Daño en Instalación)</option>
                    {recursos.map((r) => (
                      <option key={r.id} value={r.id}>
                        {r.codigoInventario} - {r.nombre}
                      </option>
                    ))}
                  </select>
                </div>

                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <label className="input-label">Tipo de Incidencia</label>
                    <select
                      value={tipo}
                      onChange={(e) => setTipo(e.target.value)}
                      className="input-select w-full"
                    >
                      <option value="DAÑO_EQUIPO">Daño en Equipo</option>
                      <option value="EXTRAVIO">Extravío de Accesorio</option>
                      <option value="RETRASO_GRAVE">Retraso Injustificado</option>
                      <option value="USO_INDEBIDO">Uso Indebido</option>
                      <option value="DESPERFECTO_ESPACIO">Desperfecto de Espacio</option>
                    </select>
                  </div>

                  <div>
                    <label className="input-label">Gravedad de la Falta</label>
                    <select
                      value={gravedad}
                      onChange={(e) => setGravedad(e.target.value)}
                      className="input-select w-full"
                    >
                      <option value="LEVE">Leve (-5 Puntos)</option>
                      <option value="MODERADO">Moderado (-15 Puntos)</option>
                      <option value="GRAVE">Grave (-30 Puntos)</option>
                    </select>
                  </div>
                </div>

                <div>
                  <label className="input-label">Descripción Detallada del Suceso</label>
                  <textarea
                    rows={4}
                    required
                    value={descripcion}
                    onChange={(e) => setDescripcion(e.target.value)}
                    placeholder="Describa cómo ocurrió el daño, fallas observadas, componentes afectados..."
                    className="input-text w-full"
                  />
                </div>
              </div>

              <div className="modal-footer">
                <button
                  type="button"
                  onClick={() => setShowReportModal(false)}
                  className="btn btn-secondary"
                >
                  Cancelar
                </button>
                <button
                  type="submit"
                  disabled={reportLoading}
                  className="btn btn-error flex items-center gap-2"
                >
                  <AlertTriangle size={16} />
                  Aplicar Reporte y Sanción
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Modal para Resolver / Reparación Supervisada */}
      {selectedIncidentForResolve && (
        <div className="modal-backdrop">
          <div className="modal-container max-w-md">
            <div className="modal-header">
              <div className="flex items-center gap-2">
                <Wrench size={20} className="text-accent" />
                <h3 className="modal-title">Acta de Reparación Supervisada</h3>
              </div>
              <button
                onClick={() => setSelectedIncidentForResolve(null)}
                className="modal-close-btn"
                aria-label="Cerrar modal"
              >
                <X size={18} />
              </button>
            </div>

            <form onSubmit={handleResolveIncident}>
              <div className="modal-body space-y-4">
                <div className="p-3 bg-muted rounded-md text-xs">
                  <strong>Folio Incidencia:</strong> {selectedIncidentForResolve.folio}<br />
                  <strong>Usuario:</strong> {selectedIncidentForResolve.usuarioInfractor?.nombre}
                </div>

                <div>
                  <label className="input-label">Dictamen y Solución Aplicada</label>
                  <textarea
                    rows={3}
                    required
                    value={solucion}
                    onChange={(e) => setSolucion(e.target.value)}
                    className="input-text w-full"
                  />
                </div>

                <div className="p-3 bg-accent-soft rounded-md">
                  <label className="flex items-center gap-2 cursor-pointer">
                    <input
                      type="checkbox"
                      checked={restaurarPuntos}
                      onChange={(e) => setRestaurarPuntos(e.target.checked)}
                      className="checkbox-custom"
                    />
                    <span className="text-xs font-semibold text-primary">
                      Restaurar puntos de confianza ({selectedIncidentForResolve.puntosSancion} pts)
                      al alumno por cumplimiento satisfactorio.
                    </span>
                  </label>
                </div>
              </div>

              <div className="modal-footer">
                <button
                  type="button"
                  onClick={() => setSelectedIncidentForResolve(null)}
                  className="btn btn-secondary"
                >
                  Cancelar
                </button>
                <button
                  type="submit"
                  disabled={resolveLoading}
                  className="btn btn-accent flex items-center gap-2"
                >
                  <RotateCcw size={16} />
                  Concluir y Restaurar
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
