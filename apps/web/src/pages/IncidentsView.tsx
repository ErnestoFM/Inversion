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
  Scale,
  FileCheck2,
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

  // Modal para resolución o conclusión de reparación supervisada
  const [selectedIncidentForResolve, setSelectedIncidentForResolve] = useState<Incident | null>(null);
  const [solucion, setSolucion] = useState<string>('');
  const [restaurarPuntos, setRestaurarPuntos] = useState<boolean>(true);
  const [resolveLoading, setResolveLoading] = useState(false);

  // Modal para formalizar compromiso de restitución supervisada (RF-01.3)
  const [selectedIncidentForCommitment, setSelectedIncidentForCommitment] = useState<Incident | null>(null);
  const [commitmentType, setCommitmentType] = useState<string>('REPARACION_TECNICA');
  const [agreedAmountMxn, setAgreedAmountMxn] = useState<number | undefined>(350);
  const [agreedHours, setAgreedHours] = useState<number | undefined>(4);
  const [deadlineDate, setDeadlineDate] = useState<string>('2026-10-20');
  const [commitmentNotes, setCommitmentNotes] = useState<string>(
    'Sustitución de refacción original y calibración técnica supervisada en taller de electrónica.'
  );
  const [commitmentLoading, setCommitmentLoading] = useState<boolean>(false);

  useEffect(() => {
    fetchIncidentes();
    fetchRecursos();
  }, []);

  const fetchIncidentes = async () => {
    try {
      setLoading(true);
      const res = await api.incidents.list();
      setIncidentes(res?.incidentes || []);
    } catch (err: any) {
      setError(err.message || 'Error al cargar incidencias');
    } finally {
      setLoading(false);
    }
  };

  const fetchRecursos = async () => {
    try {
      const res = await api.resources.list();
      setRecursos(res?.recursos || []);
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

  // Formalizar compromiso de restitución (RF-01.3)
  const handleRegisterCommitment = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedIncidentForCommitment) return;

    try {
      setCommitmentLoading(true);
      await api.incidents.registerCommitment(selectedIncidentForCommitment.id, {
        tipo: commitmentType,
        montoEstimadoMxn: commitmentType === 'REPOSICION_ECONOMICA' ? agreedAmountMxn : undefined,
        horasServicio: commitmentType !== 'REPOSICION_ECONOMICA' ? agreedHours : undefined,
        fechaLimite: deadlineDate,
        notasSupervision: commitmentNotes,
      });

      alert('¡Compromiso de restitución supervisada formalizado con éxito! El estado ha cambiado a REPARACIÓN SUPERVISADA.');
      setSelectedIncidentForCommitment(null);
      fetchIncidentes();
      refreshUser();
    } catch (err: any) {
      alert(`Error al formalizar compromiso: ${err.message}`);
    } finally {
      setCommitmentLoading(false);
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
  const isScoreLow = (user?.reputationScore || 100) < 70;

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

      {/* Alerta de cuenta con Trust Score bajo (< 70 pts) */}
      {isScoreLow && (
        <div className="mb-4 p-4 bg-amber-500/10 border border-amber-500/30 rounded-lg flex items-start gap-3">
          <AlertTriangle size={24} className="text-amber-500 flex-shrink-0 mt-0.5" />
          <div className="text-xs">
            <strong className="text-amber-500 text-sm block">
              Atención: Restricción Activa por Trust Score Bajo ({user?.reputationScore}/100 pts)
            </strong>
            <p className="text-secondary mt-0.5">
              Por reglamento de CUTonalá, las cuentas con menos de 70 puntos tienen deshabilitada la solicitud de nuevos préstamos.
              Para rehabilitar tu cuenta, formaliza un <strong>Expediente de Reparación Supervisada</strong> o restitución de material en Almacén.
            </p>
          </div>
        </div>
      )}

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
                <th>Descripción & Compromiso</th>
                <th>Equipo / Recurso</th>
                <th>Usuario</th>
                <th>Estado</th>
                {isStaff && <th>Acción Laboratorio (RF-01.3)</th>}
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
                  <td className="text-xs max-w-sm">
                    <div>{inc.descripcion}</div>
                    {inc.compromisoReparacion && (
                      <div className="mt-1.5 p-1.5 bg-amber-500/10 border border-amber-500/20 rounded text-[11px] text-amber-700 dark:text-amber-300">
                        <strong>Compromiso:</strong> {inc.compromisoReparacion.tipo}
                        {inc.compromisoReparacion.montoEstimadoMxn && ` ($${inc.compromisoReparacion.montoEstimadoMxn} MXN)`}
                        {inc.compromisoReparacion.horasServicio && ` (${inc.compromisoReparacion.horasServicio} hrs)`}
                        <div className="text-[10px] text-muted">{inc.compromisoReparacion.notasSupervision}</div>
                      </div>
                    )}
                  </td>
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
                      <div className="flex flex-col gap-1">
                        {inc.estado !== 'RESUELTA' && inc.estado !== 'REPARACION_SUPERVISADA' && (
                          <button
                            type="button"
                            onClick={() => setSelectedIncidentForCommitment(inc)}
                            className="btn btn-secondary btn-xs flex items-center gap-1 text-[11px]"
                            title="Formalizar acuerdo de restitución técnica o económica"
                          >
                            <Scale size={12} />
                            Acuerdo Restitución
                          </button>
                        )}
                        {inc.estado !== 'RESUELTA' && (
                          <button
                            type="button"
                            onClick={() => {
                              setSelectedIncidentForResolve(inc);
                              setSolucion(
                                'Equipo reparado y calibrado por el usuario bajo supervisión de laboratorio.'
                              );
                            }}
                            className="btn btn-accent btn-xs flex items-center gap-1 text-[11px]"
                            title="Concluir reparación y restaurar trust score"
                          >
                            <Wrench size={12} />
                            Concluir y Restaurar
                          </button>
                        )}
                      </div>
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

      {/* Modal para Formalizar Compromiso de Reparación Supervisada (RF-01.3) */}
      {selectedIncidentForCommitment && (
        <div className="modal-backdrop">
          <div className="modal-container max-w-md">
            <div className="modal-header">
              <div className="flex items-center gap-2">
                <Scale size={20} className="text-warning" />
                <h3 className="modal-title text-base">Expediente de Restitución Supervisada</h3>
              </div>
              <button
                onClick={() => setSelectedIncidentForCommitment(null)}
                className="modal-close-btn"
                aria-label="Cerrar modal"
              >
                <X size={18} />
              </button>
            </div>

            <form onSubmit={handleRegisterCommitment}>
              <div className="modal-body space-y-4 text-xs">
                <div className="p-3 bg-muted rounded-md space-y-1">
                  <div><strong>Folio:</strong> {selectedIncidentForCommitment.folio}</div>
                  <div><strong>Usuario Responsable:</strong> {selectedIncidentForCommitment.usuarioInfractor?.nombre}</div>
                  <div><strong>Motivo:</strong> {selectedIncidentForCommitment.descripcion}</div>
                </div>

                <div>
                  <label className="input-label">Modalidad de Restitución</label>
                  <select
                    value={commitmentType}
                    onChange={(e) => setCommitmentType(e.target.value)}
                    className="input-select w-full"
                  >
                    <option value="REPARACION_TECNICA">Reparación Técnica Supervisada</option>
                    <option value="REPOSICION_ECONOMICA">Reposición Económica de Refacción / Bien</option>
                    <option value="SERVICIO_LABORATORIO">Servicio Técnico en Laboratorios de CUTonalá</option>
                  </select>
                </div>

                {commitmentType === 'REPOSICION_ECONOMICA' ? (
                  <div>
                    <label className="input-label">Monto Pactado ($ MXN)</label>
                    <input
                      type="number"
                      min={1}
                      value={agreedAmountMxn || ''}
                      onChange={(e) => setAgreedAmountMxn(Number(e.target.value))}
                      className="input-text w-full font-mono"
                      placeholder="Ej. 450"
                      required
                    />
                  </div>
                ) : (
                  <div>
                    <label className="input-label">Horas de Servicio Técnico Supervisado</label>
                    <input
                      type="number"
                      min={1}
                      max={40}
                      value={agreedHours || ''}
                      onChange={(e) => setAgreedHours(Number(e.target.value))}
                      className="input-text w-full font-mono"
                      placeholder="Ej. 6"
                      required
                    />
                  </div>
                )}

                <div>
                  <label className="input-label">Fecha Límite de Cumplimiento</label>
                  <input
                    type="date"
                    value={deadlineDate}
                    onChange={(e) => setDeadlineDate(e.target.value)}
                    className="input-text w-full font-mono"
                    required
                  />
                </div>

                <div>
                  <label className="input-label">Términos y Dictamen del Técnico</label>
                  <textarea
                    rows={3}
                    required
                    value={commitmentNotes}
                    onChange={(e) => setCommitmentNotes(e.target.value)}
                    className="input-text w-full"
                    placeholder="Especifique el procedimiento técnico, la refacción a entregar o el horario de servicio acordado..."
                  />
                </div>
              </div>

              <div className="modal-footer">
                <button
                  type="button"
                  onClick={() => setSelectedIncidentForCommitment(null)}
                  className="btn btn-secondary text-xs"
                >
                  Cancelar
                </button>
                <button
                  type="submit"
                  disabled={commitmentLoading}
                  className="btn btn-warning text-xs flex items-center gap-1"
                >
                  <FileCheck2 size={14} />
                  {commitmentLoading ? 'Registrando...' : 'Formalizar Expediente'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Modal para Resolver / Concluir Reparación Supervisada */}
      {selectedIncidentForResolve && (
        <div className="modal-backdrop">
          <div className="modal-container max-w-md">
            <div className="modal-header">
              <div className="flex items-center gap-2">
                <Wrench size={20} className="text-accent" />
                <h3 className="modal-title">Acta de Conclusión de Reparación</h3>
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
                      al alumno por cumplimiento satisfactorio del expediente.
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
