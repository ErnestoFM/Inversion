import React, { useState, useEffect } from 'react';
import {
  Film,
  Calendar,
  Clock,
  MapPin,
  Users,
  Ticket,
  CheckCircle2,
  X,
  AlertCircle,
  Star,
  MessageSquare,
  ShieldCheck,
  Camera,
} from 'lucide-react';
import { api } from '../api/client';
import { useAuth } from '../context/AuthContext';
import type { EventScreening, EventReview } from '../types';

interface CarteleraViewProps {
  onOpenQrScanner?: () => void;
}

export const CarteleraView: React.FC<CarteleraViewProps> = ({ onOpenQrScanner }) => {
  const { user } = useAuth();
  const [funciones, setFunciones] = useState<EventScreening[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Modal para boleto QR emitido
  const [selectedTicket, setSelectedTicket] = useState<{
    boleto: any;
    qrCodeDataUrl: string;
    funcionTitulo: string;
  } | null>(null);

  const [bookingLoading, setBookingLoading] = useState(false);

  // Modal de Reseñas Verificadas (RF-03.3)
  const [activeReviewFunction, setActiveReviewFunction] = useState<EventScreening | null>(null);
  const [reviewsList, setReviewsList] = useState<EventReview[]>([]);
  const [reviewRating, setReviewRating] = useState<number>(5);
  const [reviewComment, setReviewComment] = useState<string>('');
  const [reviewSubmitting, setReviewSubmitting] = useState<boolean>(false);
  const [reviewSuccessMessage, setReviewSuccessMessage] = useState<string | null>(null);

  useEffect(() => {
    fetchFunciones();
  }, []);

  const fetchFunciones = async () => {
    try {
      setLoading(true);
      const res = await api.events.listScreenings();
      setFunciones(res?.funciones || []);
    } catch (err: any) {
      setError(err.message || 'Error al cargar cartelera');
    } finally {
      setLoading(false);
    }
  };

  const handleBookTicket = async (funcion: EventScreening) => {
    if (!user) {
      alert('Debes iniciar sesión con tu cuenta institucional para apartar un boleto.');
      return;
    }
    try {
      setBookingLoading(true);
      const res = await api.events.bookTicket(funcion.id);
      setSelectedTicket({
        boleto: res.boleto,
        qrCodeDataUrl: res.qrCodeDataUrl,
        funcionTitulo: funcion.titulo,
      });
      // Actualizar conteo de asientos en la lista
      setFunciones((prev) =>
        prev.map((f) =>
          f.id === funcion.id
            ? { ...f, asientosDisponibles: Math.max(0, f.asientosDisponibles - 1) }
            : f
        )
      );
    } catch (err: any) {
      alert(err.message || 'No se pudo apartar el boleto');
    } finally {
      setBookingLoading(false);
    }
  };

  const handleOpenReviewsModal = async (funcion: EventScreening) => {
    setActiveReviewFunction(funcion);
    setReviewSuccessMessage(null);
    setReviewComment('');
    setReviewRating(5);
    try {
      const res = await api.events.getReviews(funcion.id);
      setReviewsList(res?.data || [
        {
          id: 'rev-1',
          rating: 5,
          comment: 'Increíble proyección en la Cineteca CUTonalá. El sonido Dolby 7.1 y la remasterización 4K son espectaculares.',
          usuarioNombre: 'Carlos Daniel Mendoza',
          carrera: 'Licenciatura en Diseño y Artes Digitales',
          created_at: new Date().toISOString(),
          asistenciaVerificada: true,
        },
      ]);
    } catch (err) {
      console.error(err);
    }
  };

  const handleSubmitReview = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!activeReviewFunction) return;
    if (!user) {
      alert('Debes iniciar sesión para publicar una reseña.');
      return;
    }
    if (!reviewComment.trim()) {
      alert('Escribe un comentario sobre tu experiencia.');
      return;
    }

    try {
      setReviewSubmitting(true);
      await api.events.postReview(activeReviewFunction.id, {
        rating: reviewRating,
        comment: reviewComment,
      });

      const newReview: EventReview = {
        id: `rev-${Date.now()}`,
        rating: reviewRating,
        comment: reviewComment,
        usuarioNombre: user.nombre,
        carrera: user.carrera,
        created_at: new Date().toISOString(),
        asistenciaVerificada: true,
      };

      setReviewsList((prev) => [newReview, ...prev]);
      setReviewSuccessMessage('¡Tu reseña verificada fue publicada con éxito!');
      setReviewComment('');
    } catch (err: any) {
      alert(`No se pudo enviar la reseña: ${err.message || 'Verifica que tu código QR haya sido escaneado como ASISTIÓ.'}`);
    } finally {
      setReviewSubmitting(false);
    }
  };

  return (
    <div className="view-container">
      {/* Hero Cartelera Cineteca */}
      <div className="billboard-hero">
        <div className="hero-content">
          <div className="flex flex-wrap items-center justify-between gap-2 mb-2">
            <div className="badge badge-accent">Sala Cineteca CUTonalá</div>
            {onOpenQrScanner && (
              <button
                type="button"
                onClick={onOpenQrScanner}
                className="btn btn-secondary btn-sm flex items-center gap-1.5 shadow-sm"
              >
                <Camera size={15} className="text-primary" />
                <span>Escáner de Acceso (Cámara QR)</span>
              </button>
            )}
          </div>
          <h1 className="hero-title">Cartelera Cultural & Proyecciones Universitarias</h1>
          <p className="hero-subtitle">
            Funciones gratuitas y exclusivas para la comunidad estudiantil y académica de la Universidad
            de Guadalajara. Reserva tu boleto digital con código QR institucional y consulta reseñas verificadas de asistentes.
          </p>
        </div>
      </div>

      {loading ? (
        <div className="loading-state">
          <div className="spinner"></div>
          <p className="text-secondary mt-3">Cargando cartelera de la Cineteca...</p>
        </div>
      ) : error ? (
        <div className="alert-box alert-error">
          <AlertCircle size={20} />
          <div>
            <strong>Error al conectar con la cartelera:</strong> {error}
          </div>
        </div>
      ) : funciones.length === 0 ? (
        <div className="empty-state">
          <Film size={48} className="text-muted" />
          <h3 className="mt-3 font-semibold">No hay funciones programadas para hoy</h3>
          <p className="text-secondary text-sm">Vuelve pronto para consultar nuevas proyecciones.</p>
        </div>
      ) : (
        <div className="grid-cards">
          {funciones.map((funcion) => {
            const fecha = new Date(funcion.fechaHoraInicio);
            const fechaStr = fecha.toLocaleDateString('es-MX', {
              weekday: 'short',
              day: 'numeric',
              month: 'short',
            });
            const horaStr = fecha.toLocaleTimeString('es-MX', {
              hour: '2-digit',
              minute: '2-digit',
            });

            const cupoAgotado = funcion.asientosDisponibles <= 0;

            return (
              <div key={funcion.id} className="card billboard-card">
                <div className="billboard-poster-wrapper">
                  <img
                    src={funcion.posterUrl || 'https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?auto=format&fit=crop&w=600&q=80'}
                    alt={funcion.titulo}
                    className="billboard-poster"
                  />
                  <span className="rating-tag">{funcion.clasificacion || 'B'}</span>
                  <div className="seats-badge">
                    <Users size={13} className="mr-1" />
                    <span>{funcion.asientosDisponibles} asientos</span>
                  </div>
                </div>

                <div className="card-body">
                  <div className="flex justify-between items-start">
                    <h3 className="billboard-title">{funcion.titulo}</h3>
                    <div className="flex items-center gap-1 text-amber-500 font-bold text-xs bg-amber-50 dark:bg-amber-950/40 px-2 py-0.5 rounded border border-amber-200 dark:border-amber-900/50">
                      <Star size={12} className="fill-amber-400 text-amber-400" />
                      <span>4.9</span>
                    </div>
                  </div>
                  <p className="billboard-synopsis">{funcion.sinopsis}</p>

                  <div className="billboard-meta">
                    <div className="meta-item">
                      <Calendar size={14} className="text-accent" />
                      <span>{fechaStr}</span>
                    </div>
                    <div className="meta-item">
                      <Clock size={14} className="text-accent" />
                      <span>{horaStr} ({funcion.duracionMin} min)</span>
                    </div>
                    <div className="meta-item">
                      <MapPin size={14} className="text-accent" />
                      <span>{funcion.espacio?.nombre || 'Sala Cineteca'}</span>
                    </div>
                  </div>

                  <div className="card-footer mt-4 flex flex-col gap-2">
                    <button
                      type="button"
                      disabled={cupoAgotado || bookingLoading}
                      onClick={() => handleBookTicket(funcion)}
                      className={`btn w-full ${cupoAgotado ? 'btn-secondary' : 'btn-accent'}`}
                    >
                      <Ticket size={16} className="mr-2" />
                      {cupoAgotado ? 'Cupo Agotado' : 'Reservar Asiento QR'}
                    </button>

                    <button
                      type="button"
                      onClick={() => handleOpenReviewsModal(funcion)}
                      className="btn btn-secondary btn-sm w-full flex items-center justify-center gap-1 text-xs"
                    >
                      <MessageSquare size={13} />
                      Reseñas Verificadas de Asistentes
                    </button>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      )}

      {/* Modal de Boleto Digital QR */}
      {selectedTicket && (
        <div className="modal-backdrop">
          <div className="modal-container max-w-md">
            <div className="modal-header">
              <div className="flex items-center gap-2">
                <CheckCircle2 size={20} className="text-accent" />
                <h3 className="modal-title">¡Boleto Digital Confirmado!</h3>
              </div>
              <button
                onClick={() => setSelectedTicket(null)}
                className="modal-close-btn"
                aria-label="Cerrar boleto"
              >
                <X size={18} />
              </button>
            </div>

            <div className="modal-body text-center">
              <div className="ticket-card">
                <div className="ticket-header">
                  <span className="ticket-brand">Cineteca CUTonalá</span>
                  <span className="badge badge-accent">Acceso Válido</span>
                </div>
                <h4 className="ticket-movie-title">{selectedTicket.funcionTitulo}</h4>
                <div className="text-xs text-secondary font-mono mb-3">
                  Folio: {selectedTicket.boleto.folioBoleto}
                </div>

                <div className="ticket-qr-container">
                  <img
                    src={selectedTicket.qrCodeDataUrl}
                    alt="Código QR de Acceso"
                    className="ticket-qr-img"
                  />
                </div>
                <p className="ticket-instruction">
                  Presenta este código QR en el lector del acceso a la Sala de Cineteca. Válido para 1
                  asiento individual.
                </p>

                <div className="ticket-footer-info">
                  <div>
                    <span className="label">Titular</span>
                    <span className="value">{user?.nombre}</span>
                  </div>
                  <div>
                    <span className="label">Código UdeG</span>
                    <span className="value font-mono">{user?.codigo}</span>
                  </div>
                </div>
              </div>
            </div>

            <div className="modal-footer">
              <button
                type="button"
                onClick={() => setSelectedTicket(null)}
                className="btn btn-primary w-full"
              >
                Listo, guardar en Mis Solicitudes
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Modal de Reseñas Verificadas (RF-03.3) */}
      {activeReviewFunction && (
        <div className="modal-backdrop">
          <div className="modal-container max-w-lg">
            <div className="modal-header">
              <div className="flex items-center gap-2">
                <ShieldCheck size={20} className="text-accent" />
                <div>
                  <h3 className="modal-title text-base">Reseñas Verificadas: {activeReviewFunction.titulo}</h3>
                  <span className="text-xs text-muted">Solo asistentes con acceso QR escaneado</span>
                </div>
              </div>
              <button
                onClick={() => setActiveReviewFunction(null)}
                className="modal-close-btn"
                aria-label="Cerrar modal"
              >
                <X size={18} />
              </button>
            </div>

            <div className="modal-body space-y-4 max-h-[70vh] overflow-y-auto">
              {/* Formulario de nueva reseña */}
              <form onSubmit={handleSubmitReview} className="p-4 bg-muted rounded-lg border border-default space-y-3">
                <div className="flex justify-between items-center">
                  <span className="text-xs font-bold text-primary">Calificar la Proyección:</span>
                  <div className="flex gap-1">
                    {[1, 2, 3, 4, 5].map((star) => (
                      <button
                        key={star}
                        type="button"
                        onClick={() => setReviewRating(star)}
                        className="text-amber-400 hover:scale-110 transition"
                      >
                        <Star
                          size={18}
                          className={star <= reviewRating ? 'fill-amber-400 text-amber-400' : 'text-gray-300'}
                        />
                      </button>
                    ))}
                  </div>
                </div>

                <div>
                  <textarea
                    rows={2}
                    required
                    placeholder="Comparte tu opinión sobre la función, la calidad de proyección o la experiencia en sala..."
                    value={reviewComment}
                    onChange={(e) => setReviewComment(e.target.value)}
                    className="input-text w-full text-xs"
                  />
                </div>

                <div className="flex justify-between items-center text-xs">
                  <span className="text-muted flex items-center gap-1">
                    <ShieldCheck size={13} className="text-accent" />
                    Validación automática por QR
                  </span>
                  <button
                    type="submit"
                    disabled={reviewSubmitting}
                    className="btn btn-accent btn-sm text-xs"
                  >
                    {reviewSubmitting ? 'Publicando...' : 'Publicar Reseña'}
                  </button>
                </div>

                {reviewSuccessMessage && (
                  <div className="p-2 bg-emerald-100 dark:bg-emerald-950/40 text-emerald-800 dark:text-emerald-300 rounded text-xs">
                    {reviewSuccessMessage}
                  </div>
                )}
              </form>

              {/* Lista de reseñas comunitarias */}
              <div className="space-y-3">
                <h4 className="text-xs font-bold text-secondary uppercase tracking-wider">
                  Opiniones de la Comunidad CUTonalá ({reviewsList.length})
                </h4>

                {reviewsList.length === 0 ? (
                  <p className="text-xs text-muted text-center py-4">Aún no hay reseñas registradas para esta función.</p>
                ) : (
                  reviewsList.map((rev) => (
                    <div key={rev.id} className="p-3 bg-surface rounded-lg border border-default text-xs space-y-1">
                      <div className="flex justify-between items-center">
                        <div className="flex items-center gap-1.5">
                          <strong className="text-primary">{rev.usuarioNombre}</strong>
                          {rev.asistenciaVerificada && (
                            <span className="badge-financial-pill text-[10px] py-0 px-1.5">
                              ✓ Asistió
                            </span>
                          )}
                        </div>
                        <div className="flex text-amber-400">
                          {Array.from({ length: rev.rating }).map((_, i) => (
                            <Star key={i} size={12} className="fill-amber-400" />
                          ))}
                        </div>
                      </div>
                      {rev.carrera && <div className="text-[11px] text-muted">{rev.carrera}</div>}
                      <p className="text-secondary mt-1">{rev.comment}</p>
                    </div>
                  ))
                )}
              </div>
            </div>

            <div className="modal-footer">
              <button
                type="button"
                onClick={() => setActiveReviewFunction(null)}
                className="btn btn-secondary text-xs"
              >
                Cerrar
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
