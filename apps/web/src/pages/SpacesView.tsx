import React, { useState, useEffect } from 'react';
import {
  Building2,
  Users,
  MapPin,
  Calendar,
  Lock,
  Unlock,
  CheckCircle2,
  AlertCircle,
  X,
  Info,
} from 'lucide-react';
import { api } from '../api/client';
import { useAuth } from '../context/AuthContext';
import type { Space } from '../types';

export const SpacesView: React.FC = () => {
  const { user } = useAuth();
  const [espacios, setEspacios] = useState<Space[]>([]);
  const [selectedTipo, setSelectedTipo] = useState<string>('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Modal de reserva y Soft Lock en Redis
  const [selectedSpace, setSelectedSpace] = useState<Space | null>(null);
  const [fechaReserva, setFechaReserva] = useState<string>('');
  const [horaInicio, setHoraInicio] = useState<string>('09:00');
  const [horaFin, setHoraFin] = useState<string>('11:00');
  const [motivoUso, setMotivoUso] = useState<string>('');
  const [asistentes, setAsistentes] = useState<number>(20);

  // Estado del bloqueo temporal en Redis
  const [lockStatus, setLockStatus] = useState<{
    activo: boolean;
    timeLeftSeconds: number;
    mensaje?: string;
  }>({ activo: false, timeLeftSeconds: 0 });

  const [bookingResult, setBookingResult] = useState<{ folio: string } | null>(null);
  const [bookingLoading, setBookingLoading] = useState(false);

  useEffect(() => {
    fetchEspacios();
  }, [selectedTipo]);

  // Temporizador para el Soft Lock de Redis
  useEffect(() => {
    if (!lockStatus.activo || lockStatus.timeLeftSeconds <= 0) return;
    const timer = setInterval(() => {
      setLockStatus((prev) => {
        if (prev.timeLeftSeconds <= 1) {
          clearInterval(timer);
          return { activo: false, timeLeftSeconds: 0, mensaje: 'El bloqueo en Redis ha expirado.' };
        }
        return { ...prev, timeLeftSeconds: prev.timeLeftSeconds - 1 };
      });
    }, 1000);
    return () => clearInterval(timer);
  }, [lockStatus.activo, lockStatus.timeLeftSeconds]);

  const fetchEspacios = async () => {
    try {
      setLoading(true);
      const res = await api.spaces.list({ tipo: selectedTipo || undefined });
      setEspacios(res.espacios);
    } catch (err: any) {
      setError(err.message || 'Error al obtener espacios');
    } finally {
      setLoading(false);
    }
  };

  const handleOpenBookingModal = (space: Space) => {
    setSelectedSpace(space);
    setBookingResult(null);
    setLockStatus({ activo: false, timeLeftSeconds: 0 });
    // Fecha sugerida por defecto: 4 días después de hoy para cumplir la regla de CUTonalá (mínimo 3 días)
    const d = new Date();
    d.setDate(d.getDate() + 4);
    // Si cae en domingo, mover al lunes
    if (d.getDay() === 0) d.setDate(d.getDate() + 1);
    setFechaReserva(d.toISOString().split('T')[0]);
  };

  const handleAcquireLock = async () => {
    if (!selectedSpace || !fechaReserva) return;
    const inicioIso = `${fechaReserva}T${horaInicio}:00.000Z`;
    const finIso = `${fechaReserva}T${horaFin}:00.000Z`;

    try {
      const res = await api.spaces.acquireLock(selectedSpace.id, inicioIso, finIso);
      setLockStatus({
        activo: true,
        timeLeftSeconds: res.expiraEnSegundos || 900,
        mensaje: res.mensaje,
      });
    } catch (err: any) {
      alert(`No se pudo apartar temporalmente: ${err.message}`);
    }
  };

  const handleConfirmBooking = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedSpace) return;
    if (!user) {
      alert('Debes iniciar sesión con tu cuenta institucional UdeG.');
      return;
    }

    const inicioIso = `${fechaReserva}T${horaInicio}:00.000Z`;
    const finIso = `${fechaReserva}T${horaFin}:00.000Z`;

    try {
      setBookingLoading(true);
      const res = await api.spaces.book({
        espacioId: selectedSpace.id,
        fechaInicio: inicioIso,
        fechaFin: finIso,
        motivoUso,
        asistentesEstimados: Number(asistentes),
      });

      setBookingResult({ folio: res.reserva.folio });
      setLockStatus({ activo: false, timeLeftSeconds: 0 });
    } catch (err: any) {
      alert(`Error al registrar reserva: ${err.message}`);
    } finally {
      setBookingLoading(false);
    }
  };

  const formatTimer = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs < 10 ? '0' : ''}${secs}`;
  };

  return (
    <div className="view-container">
      {/* Encabezado */}
      <div className="section-header">
        <div>
          <h2 className="section-title">Espacios Físicos, Auditorios y Laboratorios</h2>
          <p className="section-subtitle">
            Reserva de instalaciones de uso común en CUTonalá con control de colisiones en tiempo real.
          </p>
        </div>

        {/* Filtros */}
        <div className="flex gap-2">
          <select
            value={selectedTipo}
            onChange={(e) => setSelectedTipo(e.target.value)}
            className="input-select"
          >
            <option value="">Todos los Tipos</option>
            <option value="AUDITORIO">Auditorios</option>
            <option value="CINETECA">Cineteca</option>
            <option value="LABORATORIO">Laboratorios</option>
            <option value="AULA">Aulas</option>
            <option value="SALA_JUNTAS">Salas de Juntas</option>
          </select>
        </div>
      </div>

      {/* Regla CUTonalá Notice */}
      <div className="notice-banner">
        <Info size={18} className="text-accent flex-shrink-0" />
        <div className="text-xs leading-relaxed">
          <strong>Reglamento CUTonalá:</strong> Las solicitudes de espacios deben registrarse con un
          mínimo de <strong>3 días</strong> y un máximo de <strong>15 días hábiles</strong> de
          anticipación. Horario disponible de lunes a sábado de 08:00 a 19:00 hrs. Los domingos no se
          habilitan reservas.
        </div>
      </div>

      {loading ? (
        <div className="loading-state">
          <div className="spinner"></div>
          <p className="text-secondary mt-3">Cargando catálogo de espacios...</p>
        </div>
      ) : error ? (
        <div className="alert-box alert-error">
          <AlertCircle size={20} />
          <div>{error}</div>
        </div>
      ) : (
        <div className="grid-cards">
          {espacios.map((espacio) => (
            <div key={espacio.id} className="card space-card">
              <div className="space-img-wrapper">
                <img
                  src={
                    espacio.fotos[0] ||
                    'https://images.unsplash.com/photo-1541829070764-84a7d30dd3f3?auto=format&fit=crop&w=600&q=80'
                  }
                  alt={espacio.nombre}
                  className="space-img"
                />
                <span className="badge badge-primary space-type-badge">{espacio.tipo}</span>
              </div>

              <div className="card-body">
                <div className="flex justify-between items-start">
                  <h3 className="card-title">{espacio.nombre}</h3>
                  <span className="font-mono text-xs text-muted">{espacio.codigoEspacio}</span>
                </div>

                <div className="space-meta mt-2">
                  <div className="meta-item">
                    <MapPin size={14} className="text-accent" />
                    <span>{espacio.edificio}, Piso {espacio.piso}</span>
                  </div>
                  <div className="meta-item">
                    <Users size={14} className="text-accent" />
                    <span>Capacidad: {espacio.capacidad} personas</span>
                  </div>
                </div>

                {espacio.equipamiento.length > 0 && (
                  <div className="equipment-chips mt-3">
                    {espacio.equipamiento.map((eq, i) => (
                      <span key={i} className="chip">
                        {eq}
                      </span>
                    ))}
                  </div>
                )}

                <div className="card-footer mt-4">
                  <button
                    type="button"
                    onClick={() => handleOpenBookingModal(espacio)}
                    className="btn btn-accent w-full"
                  >
                    <Calendar size={16} className="mr-2" />
                    Solicitar Reserva
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Modal de Reserva con Soft Lock Redis */}
      {selectedSpace && (
        <div className="modal-backdrop">
          <div className="modal-container max-w-lg">
            <div className="modal-header">
              <div className="flex items-center gap-2">
                <Building2 size={20} className="text-accent" />
                <h3 className="modal-title">Reservar {selectedSpace.nombre}</h3>
              </div>
              <button
                onClick={() => setSelectedSpace(null)}
                className="modal-close-btn"
                aria-label="Cerrar modal"
              >
                <X size={18} />
              </button>
            </div>

            {bookingResult ? (
              <div className="modal-body text-center py-6">
                <div className="w-16 h-16 bg-accent-soft text-accent rounded-full flex items-center justify-center mx-auto mb-3">
                  <CheckCircle2 size={36} />
                </div>
                <h3 className="text-lg font-bold">¡Solicitud Registrada con Éxito!</h3>
                <p className="text-secondary text-sm mt-1">
                  Tu solicitud ha sido enviada para revisión por la Coordinación de CUTonalá.
                </p>
                <div className="mt-4 p-3 bg-muted rounded-md inline-block">
                  <span className="text-xs text-secondary">Folio Oficial:</span>
                  <div className="font-mono font-bold text-accent text-lg">
                    {bookingResult.folio}
                  </div>
                </div>
                <div className="mt-6">
                  <button
                    type="button"
                    onClick={() => setSelectedSpace(null)}
                    className="btn btn-primary"
                  >
                    Cerrar y Ver Mis Solicitudes
                  </button>
                </div>
              </div>
            ) : (
              <form onSubmit={handleConfirmBooking}>
                <div className="modal-body space-y-4">
                  {/* Banner de Soft Lock en Redis */}
                  <div
                    className={`lock-banner ${
                      lockStatus.activo ? 'lock-active' : 'lock-inactive'
                    }`}
                  >
                    <div className="flex items-center gap-2">
                      {lockStatus.activo ? (
                        <Lock size={16} className="text-accent pulse-icon" />
                      ) : (
                        <Unlock size={16} className="text-secondary" />
                      )}
                      <span className="font-semibold text-xs">
                        {lockStatus.activo
                          ? `Bloqueo Temporal en Redis Activo (${formatTimer(
                              lockStatus.timeLeftSeconds
                            )} restantes)`
                          : 'Bloqueo Concurrente en Redis'}
                      </span>
                    </div>
                    {!lockStatus.activo && (
                      <button
                        type="button"
                        onClick={handleAcquireLock}
                        className="btn btn-secondary btn-xs mt-1"
                      >
                        Apartar cupo 15 min
                      </button>
                    )}
                  </div>

                  <div>
                    <label className="input-label">Fecha de la Reserva</label>
                    <input
                      type="date"
                      required
                      value={fechaReserva}
                      onChange={(e) => setFechaReserva(e.target.value)}
                      className="input-text w-full"
                    />
                    <span className="input-hint">
                      Mínimo 3 días y máximo 15 días posteriores a hoy (Lunes a Sábado).
                    </span>
                  </div>

                  <div className="grid grid-cols-2 gap-3">
                    <div>
                      <label className="input-label">Hora Inicio</label>
                      <input
                        type="time"
                        required
                        value={horaInicio}
                        onChange={(e) => setHoraInicio(e.target.value)}
                        className="input-text w-full"
                      />
                    </div>
                    <div>
                      <label className="input-label">Hora Fin</label>
                      <input
                        type="time"
                        required
                        value={horaFin}
                        onChange={(e) => setHoraFin(e.target.value)}
                        className="input-text w-full"
                      />
                    </div>
                  </div>

                  <div>
                    <label className="input-label">Asistentes Estimados</label>
                    <input
                      type="number"
                      min="1"
                      max={selectedSpace.capacidad}
                      value={asistentes}
                      onChange={(e) => setAsistentes(Number(e.target.value))}
                      className="input-text w-full"
                      required
                    />
                    <span className="input-hint">
                      Capacidad máxima del recinto: {selectedSpace.capacidad} personas.
                    </span>
                  </div>

                  <div>
                    <label className="input-label">Motivo o Justificación Académica</label>
                    <textarea
                      rows={3}
                      required
                      value={motivoUso}
                      onChange={(e) => setMotivoUso(e.target.value)}
                      placeholder="Describa el objetivo académico, proyecto o evento para el uso del espacio..."
                      className="input-text w-full"
                    />
                  </div>
                </div>

                <div className="modal-footer">
                  <button
                    type="button"
                    onClick={() => setSelectedSpace(null)}
                    className="btn btn-secondary"
                  >
                    Cancelar
                  </button>
                  <button
                    type="submit"
                    disabled={bookingLoading}
                    className="btn btn-accent flex items-center gap-2"
                  >
                    {bookingLoading ? (
                      <span className="spinner-sm" />
                    ) : (
                      <CheckCircle2 size={16} />
                    )}
                    Confirmar Solicitud
                  </button>
                </div>
              </form>
            )}
          </div>
        </div>
      )}
    </div>
  );
};
