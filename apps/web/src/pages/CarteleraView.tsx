import React, { useState, useEffect } from 'react';
import { Film, Calendar, Clock, MapPin, Users, Ticket, CheckCircle2, X, AlertCircle } from 'lucide-react';
import { api } from '../api/client';
import { useAuth } from '../context/AuthContext';
import type { EventScreening } from '../types';

export const CarteleraView: React.FC = () => {
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

  return (
    <div className="view-container">
      {/* Hero Cartelera Cineteca */}
      <div className="billboard-hero">
        <div className="hero-content">
          <div className="badge badge-accent mb-2">Sala Cineteca CUTonalá</div>
          <h1 className="hero-title">Cartelera Cultural & Proyecciones Universitarias</h1>
          <p className="hero-subtitle">
            Funciones gratuitas y exclusivas para la comunidad estudiantil y académica de la Universidad
            de Guadalajara. Reserva tu boleto digital con código QR institucional.
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
                  <h3 className="billboard-title">{funcion.titulo}</h3>
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

                  <div className="card-footer mt-4">
                    <button
                      type="button"
                      disabled={cupoAgotado || bookingLoading}
                      onClick={() => handleBookTicket(funcion)}
                      className={`btn w-full ${cupoAgotado ? 'btn-secondary' : 'btn-accent'}`}
                    >
                      <Ticket size={16} className="mr-2" />
                      {cupoAgotado ? 'Cupo Agotado' : 'Reservar Asiento QR'}
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
    </div>
  );
};
