import React, { useState, useEffect } from 'react';
import {
  FileText,
  Building2,
  Ticket,
  Download,
  ClipboardCheck,
  CheckCircle2,
  X,
  Eye,
  Mail,
  PenTool,
  Star,
  Users,
  ShieldCheck,
} from 'lucide-react';
import { api } from '../api/client';
import { useAuth } from '../context/AuthContext';
import { DigitalSignatureModal } from '../components/DigitalSignatureModal';
import type { Loan, Booking } from '../types';

export const LoansAndBookingsView: React.FC = () => {
  const { user } = useAuth();
  const [activeSubTab, setActiveSubTab] = useState<'prestamos' | 'reservas' | 'boletos'>('prestamos');
  const [loans, setLoans] = useState<Loan[]>([]);
  const [bookings, setBookings] = useState<Booking[]>([]);
  const [tickets, setTickets] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  // Modal para checklist de entrega/recepción
  const [selectedLoanForChecklist, setSelectedLoanForChecklist] = useState<Loan | null>(null);
  const [checklistTipo, setChecklistTipo] = useState<'salida' | 'entrada'>('salida');
  const [condicion, setCondicion] = useState<string>('EXCELENTE');
  const [accesoriosTexto, setAccesoriosTexto] = useState<string>('Cargador, Cable de Poder, Maletín');
  const [observaciones, setObservaciones] = useState<string>('Equipo entregado en óptimas condiciones de laboratorio.');
  const [checklistLoading, setChecklistLoading] = useState<boolean>(false);

  // Modal para ver boleto QR
  const [viewingTicket, setViewingTicket] = useState<any | null>(null);

  // Modal para calificar función desde boleto (RF-03.3)
  const [reviewingTicket, setReviewingTicket] = useState<any | null>(null);
  const [ticketRating, setTicketRating] = useState<number>(5);
  const [ticketComment, setTicketComment] = useState<string>('');
  const [reviewLoading, setReviewLoading] = useState<boolean>(false);

  // Modal para firma remota de co-responsable (RF-02.3)
  const [signingLoanCoResp, setSigningLoanCoResp] = useState<Loan | null>(null);
  const [coRespInviteLoading, setCoRespInviteLoading] = useState<string | null>(null);

  useEffect(() => {
    loadData();
  }, [activeSubTab]);

  const loadData = async () => {
    setLoading(true);
    try {
      if (activeSubTab === 'prestamos') {
        const res = await api.loans.myLoans();
        setLoans(res?.prestamos || []);
      } else if (activeSubTab === 'reservas') {
        const res = await api.spaces.myBookings();
        setBookings(res?.reservas || []);
      } else {
        const res = await api.events.myTickets();
        setTickets(res?.boletos || []);
      }
    } catch (err: any) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleOpenChecklist = (loan: Loan, tipo: 'salida' | 'entrada') => {
    setSelectedLoanForChecklist(loan);
    setChecklistTipo(tipo);
    setCondicion('EXCELENTE');
  };

  const handleSubmitChecklist = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedLoanForChecklist) return;

    try {
      setChecklistLoading(true);
      await api.loans.verifyChecklist(selectedLoanForChecklist.id, checklistTipo, {
        condicion,
        accesorios: accesoriosTexto.split(',').map((s) => s.trim()),
        observaciones,
      });
      alert(`Checklist de ${checklistTipo} completado exitosamente.`);
      setSelectedLoanForChecklist(null);
      loadData();
    } catch (err: any) {
      alert(`Error al registrar checklist: ${err.message}`);
    } finally {
      setChecklistLoading(false);
    }
  };

  // Enviar invitación de correo al co-responsable (RF-02.3)
  const handleSendCoRespInvite = async (loanId: string, email?: string) => {
    try {
      setCoRespInviteLoading(loanId);
      const res = await api.loans.sendCoResponsibleInvite(loanId, email);
      alert(res.message || 'Invitación con token temporal enviada por correo al co-responsable.');
    } catch (err: any) {
      alert(`Error al enviar invitación: ${err.message}`);
    } finally {
      setCoRespInviteLoading(null);
    }
  };

  // Guardar firma remota del co-responsable (RF-02.3)
  const handleSaveCoResponsibleSignature = async (signatureBase64: string) => {
    if (!signingLoanCoResp) return;
    try {
      await api.loans.signCoResponsible(signingLoanCoResp.id, signatureBase64);
      alert('¡Firma de co-responsable asentada con éxito en el expediente oficial!');
      setSigningLoanCoResp(null);
      loadData();
    } catch (err: any) {
      alert(`Error al registrar firma: ${err.message}`);
    }
  };

  // Enviar reseña verificada desde boleto (RF-03.3)
  const handleSubmitTicketReview = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!reviewingTicket?.proyeccion?.id) return;
    try {
      setReviewLoading(true);
      await api.events.postReview(reviewingTicket.proyeccion.id, {
        rating: ticketRating,
        comment: ticketComment,
      });
      alert('¡Tu reseña verificada ha sido publicada en la cartelera de la Cineteca!');
      setReviewingTicket(null);
      setTicketComment('');
    } catch (err: any) {
      alert(`Error: ${err.message || 'Solo asistentes con QR escaneado pueden calificar.'}`);
    } finally {
      setReviewLoading(false);
    }
  };

  return (
    <div className="view-container">
      {/* Encabezado */}
      <div className="section-header">
        <div>
          <h2 className="section-title">Mis Solicitudes, Responsivas y Boletos</h2>
          <p className="section-subtitle">
            Historial de trámites activos en CUTonalá, firmas digitales compartidas y actas de entrega.
          </p>
        </div>

        {/* Sub-Tabs */}
        <div className="subtabs-wrapper">
          <button
            onClick={() => setActiveSubTab('prestamos')}
            className={`subtab-btn ${activeSubTab === 'prestamos' ? 'active' : ''}`}
          >
            <FileText size={16} />
            Préstamos de Material ({loans.length})
          </button>
          <button
            onClick={() => setActiveSubTab('reservas')}
            className={`subtab-btn ${activeSubTab === 'reservas' ? 'active' : ''}`}
          >
            <Building2 size={16} />
            Reservas de Espacios ({bookings.length})
          </button>
          <button
            onClick={() => setActiveSubTab('boletos')}
            className={`subtab-btn ${activeSubTab === 'boletos' ? 'active' : ''}`}
          >
            <Ticket size={16} />
            Boletos Cineteca ({tickets.length})
          </button>
        </div>
      </div>

      {loading ? (
        <div className="loading-state">
          <div className="spinner"></div>
          <p className="text-secondary mt-3">Cargando registros...</p>
        </div>
      ) : activeSubTab === 'prestamos' ? (
        loans.length === 0 ? (
          <div className="empty-state">
            <FileText size={48} className="text-muted" />
            <h3 className="mt-3 font-semibold">No tienes préstamos registrados</h3>
            <p className="text-secondary text-sm">
              Visita la sección de Inventario para solicitar equipo de laboratorio o cómputo.
            </p>
          </div>
        ) : (
          <div className="table-responsive card">
            <table className="table">
              <thead>
                <tr>
                  <th>Folio</th>
                  <th>Equipo / Recurso</th>
                  <th>Fecha Límite</th>
                  <th>Tipo</th>
                  <th>Estado</th>
                  <th>Co-Responsables (RF-02.3)</th>
                  <th>Responsiva PDF</th>
                  <th>Inspección / Checklist</th>
                </tr>
              </thead>
              <tbody>
                {loans.map((loan) => (
                  <tr key={loan.id}>
                    <td className="font-mono text-xs font-bold text-accent">{loan.folio}</td>
                    <td>
                      <div className="font-semibold text-primary">{loan.recurso?.nombre}</div>
                      <span className="font-mono text-xs text-muted">
                        Placa: {loan.recurso?.codigoInventario}
                      </span>
                    </td>
                    <td className="text-xs">
                      {new Date(loan.fechaLimiteDevolucion).toLocaleDateString('es-MX', {
                        day: '2-digit',
                        month: 'short',
                        year: 'numeric',
                      })}
                    </td>
                    <td>
                      {loan.esPrestamoExtendido ? (
                        <span className="badge badge-warning text-xs">Extendido</span>
                      ) : (
                        <span className="badge badge-primary text-xs">Estándar (3d)</span>
                      )}
                    </td>
                    <td>
                      <span
                        className={`badge ${
                          loan.estado === 'ACTIVO'
                            ? 'badge-accent'
                            : loan.estado === 'DEVUELTO'
                            ? 'badge-primary'
                            : 'badge-error'
                        }`}
                      >
                        {loan.estado}
                      </span>
                    </td>

                    {/* Co-Responsables (RF-02.3) */}
                    <td className="text-xs">
                      {loan.coResponsables && loan.coResponsables.length > 0 ? (
                        <div className="space-y-1">
                          {loan.coResponsables.map((cr) => (
                            <div key={cr.id} className="flex flex-col gap-0.5">
                              <div className="flex items-center gap-1 font-medium text-primary">
                                <Users size={12} className="text-accent" />
                                <span>{cr.nombre}</span>
                              </div>
                              <div className="flex items-center gap-1">
                                <span
                                  className={`badge text-[10px] py-0 px-1.5 ${
                                    cr.haFirmado ? 'badge-accent' : 'badge-warning'
                                  }`}
                                >
                                  {cr.haFirmado ? '✓ Firmado' : '⏳ Firma Pendiente'}
                                </span>
                              </div>
                            </div>
                          ))}
                          <div className="flex gap-1 mt-1">
                            <button
                              type="button"
                              onClick={() => handleSendCoRespInvite(loan.id, loan.coResponsables?.[0]?.email)}
                              disabled={coRespInviteLoading === loan.id}
                              className="btn btn-secondary btn-xs text-[10px] flex items-center gap-1 py-0.5 px-1.5"
                              title="Enviar correo con enlace de firma remota (Nodemailer)"
                            >
                              <Mail size={11} />
                              {coRespInviteLoading === loan.id ? 'Enviando...' : 'Reenviar Correo'}
                            </button>
                            <button
                              type="button"
                              onClick={() => setSigningLoanCoResp(loan)}
                              className="btn btn-accent btn-xs text-[10px] flex items-center gap-1 py-0.5 px-1.5"
                              title="Firmar digitalmente ahora como co-responsable"
                            >
                              <PenTool size={11} />
                              Firmar
                            </button>
                          </div>
                        </div>
                      ) : (
                        <span className="text-muted text-[11px]">Titular Único</span>
                      )}
                    </td>

                    <td>
                      <a
                        href={api.loans.downloadResponsivaPdf(loan.id)}
                        target="_blank"
                        rel="noreferrer"
                        className="btn btn-secondary btn-xs flex items-center gap-1"
                        title="Descargar Responsiva Oficial Firmada"
                      >
                        <Download size={13} />
                        PDF Firmado
                      </a>
                    </td>
                    <td>
                      <div className="flex gap-1">
                        <button
                          type="button"
                          onClick={() => handleOpenChecklist(loan, 'salida')}
                          className="btn btn-secondary btn-xs flex items-center gap-1"
                          title="Inspección de Entrega"
                        >
                          <ClipboardCheck size={13} />
                          Salida
                        </button>
                        <button
                          type="button"
                          onClick={() => handleOpenChecklist(loan, 'entrada')}
                          className="btn btn-accent btn-xs flex items-center gap-1"
                          title="Inspección de Devolución"
                        >
                          <CheckCircle2 size={13} />
                          Entrada
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )
      ) : activeSubTab === 'reservas' ? (
        bookings.length === 0 ? (
          <div className="empty-state">
            <Building2 size={48} className="text-muted" />
            <h3 className="mt-3 font-semibold">No tienes reservas de espacios</h3>
            <p className="text-secondary text-sm">
              Visita la sección de Espacios & Aulas para apartar auditorios o laboratorios.
            </p>
          </div>
        ) : (
          <div className="table-responsive card">
            <table className="table">
              <thead>
                <tr>
                  <th>Folio</th>
                  <th>Espacio / Recinto</th>
                  <th>Fecha y Horario</th>
                  <th>Asistentes</th>
                  <th>Motivo de Uso</th>
                  <th>Estado</th>
                </tr>
              </thead>
              <tbody>
                {bookings.map((b) => (
                  <tr key={b.id}>
                    <td className="font-mono text-xs font-bold text-accent">{b.folio}</td>
                    <td>
                      <div className="font-semibold text-primary">{b.espacio?.nombre}</div>
                      <span className="text-xs text-muted">{b.espacio?.edificio}</span>
                    </td>
                    <td className="text-xs">
                      <div>
                        {new Date(b.fechaInicio).toLocaleDateString('es-MX', {
                          day: 'numeric',
                          month: 'short',
                        })}
                      </div>
                      <span className="text-muted font-mono">
                        {new Date(b.fechaInicio).toLocaleTimeString('es-MX', {
                          hour: '2-digit',
                          minute: '2-digit',
                        })}{' '}
                        -{' '}
                        {new Date(b.fechaFin).toLocaleTimeString('es-MX', {
                          hour: '2-digit',
                          minute: '2-digit',
                        })}
                      </span>
                    </td>
                    <td>{b.asistentesEstimados} personas</td>
                    <td className="text-xs max-w-xs truncate">{b.motivoUso}</td>
                    <td>
                      <span
                        className={`badge ${
                          b.estado === 'APROBADA'
                            ? 'badge-accent'
                            : b.estado === 'PENDIENTE'
                            ? 'badge-warning'
                            : 'badge-error'
                        }`}
                      >
                        {b.estado}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )
      ) : tickets.length === 0 ? (
        <div className="empty-state">
          <Ticket size={48} className="text-muted" />
          <h3 className="mt-3 font-semibold">No tienes boletos de la Cineteca</h3>
          <p className="text-secondary text-sm">
            Explora la Cartelera de la Cineteca para apartar funciones gratuitas.
          </p>
        </div>
      ) : (
        <div className="grid-cards">
          {tickets.map((t) => (
            <div key={t.id} className="card p-4 flex flex-col justify-between">
              <div>
                <div className="flex justify-between items-start">
                  <span className="badge badge-accent text-xs">Acceso Cineteca</span>
                  <span className="font-mono text-xs font-bold text-muted">{t.folioBoleto}</span>
                </div>
                <h4 className="font-bold text-primary mt-2">{t.proyeccion?.titulo}</h4>
                <div className="text-xs text-secondary mt-1">
                  Fecha: {new Date(t.proyeccion?.fechaHoraInicio).toLocaleString('es-MX')}
                </div>
                <div className="text-xs text-secondary">
                  Espacio: {t.proyeccion?.espacio?.nombre}
                </div>
              </div>

              <div className="mt-4 pt-3 border-t border-default flex justify-between items-center gap-2">
                <button
                  type="button"
                  onClick={() => setReviewingTicket(t)}
                  className="btn btn-secondary btn-xs flex items-center gap-1 text-[11px]"
                  title="Calificar y publicar reseña verificada (RF-03.3)"
                >
                  <Star size={12} className="text-amber-500 fill-amber-500" />
                  Calificar Proyección
                </button>

                <button
                  type="button"
                  onClick={() => setViewingTicket(t)}
                  className="btn btn-primary btn-xs flex items-center gap-1 text-[11px]"
                >
                  <Eye size={13} />
                  Ver Boleto QR
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Modal de Inspección Checklist Doble */}
      {selectedLoanForChecklist && (
        <div className="modal-backdrop">
          <div className="modal-container max-w-md">
            <div className="modal-header">
              <div className="flex items-center gap-2">
                <ClipboardCheck size={20} className="text-accent" />
                <h3 className="modal-title">
                  Checklist de {checklistTipo === 'salida' ? 'Entrega (Salida)' : 'Devolución (Entrada)'}
                </h3>
              </div>
              <button
                onClick={() => setSelectedLoanForChecklist(null)}
                className="modal-close-btn"
                aria-label="Cerrar modal"
              >
                <X size={18} />
              </button>
            </div>

            <form onSubmit={handleSubmitChecklist}>
              <div className="modal-body space-y-4">
                <div className="p-3 bg-muted rounded-md text-xs">
                  <strong>Bien:</strong> {selectedLoanForChecklist.recurso?.nombre} (
                  {selectedLoanForChecklist.recurso?.codigoInventario})<br />
                  <strong>Usuario:</strong> {selectedLoanForChecklist.solicitante?.nombre}
                </div>

                <div>
                  <label className="input-label">Condición Física Comprobada</label>
                  <select
                    value={condicion}
                    onChange={(e) => setCondicion(e.target.value)}
                    className="input-select w-full"
                  >
                    <option value="EXCELENTE">Excelente (Sin detalles)</option>
                    <option value="BUENO">Bueno (Marcas leves de uso normal)</option>
                    <option value="REGULAR">Regular (Desgaste notorio pero funcional)</option>
                    <option value="DAÑADO">Dañado (Reportar incidencia)</option>
                  </select>
                </div>

                <div>
                  <label className="input-label">Accesorios Verificados (separados por coma)</label>
                  <input
                    type="text"
                    value={accesoriosTexto}
                    onChange={(e) => setAccesoriosTexto(e.target.value)}
                    className="input-text w-full"
                  />
                </div>

                <div>
                  <label className="input-label">Observaciones Técnicas de Laboratorio</label>
                  <textarea
                    rows={3}
                    value={observaciones}
                    onChange={(e) => setObservaciones(e.target.value)}
                    className="input-text w-full"
                  />
                </div>
              </div>

              <div className="modal-footer">
                <button
                  type="button"
                  onClick={() => setSelectedLoanForChecklist(null)}
                  className="btn btn-secondary"
                >
                  Cancelar
                </button>
                <button
                  type="submit"
                  disabled={checklistLoading}
                  className="btn btn-accent flex items-center gap-2"
                >
                  <CheckCircle2 size={16} />
                  Guardar Acta de Inspección
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Modal para Ver Boleto QR individual */}
      {viewingTicket && (
        <div className="modal-backdrop">
          <div className="modal-container max-w-sm text-center">
            <div className="modal-header">
              <h3 className="modal-title">Boleto Digital Cineteca</h3>
              <button
                onClick={() => setViewingTicket(null)}
                className="modal-close-btn"
                aria-label="Cerrar modal"
              >
                <X size={18} />
              </button>
            </div>
            <div className="modal-body py-4">
              <h4 className="font-bold text-primary">{viewingTicket.proyeccion?.titulo}</h4>
              <p className="text-xs text-secondary mb-3">Folio: {viewingTicket.folioBoleto}</p>

              <div className="ticket-qr-container">
                <img
                  src={
                    viewingTicket.codigoQrDataUrl ||
                    'https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=' +
                      viewingTicket.folioBoleto
                  }
                  alt="QR Boleto"
                  className="ticket-qr-img"
                />
              </div>
              <p className="text-xs text-secondary mt-3">
                Escanea este código en la entrada de la Cineteca CUTonalá.
              </p>
            </div>
            <div className="modal-footer">
              <button
                type="button"
                onClick={() => setViewingTicket(null)}
                className="btn btn-primary w-full"
              >
                Cerrar
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Modal de Calificación Verificada desde Boleto (RF-03.3) */}
      {reviewingTicket && (
        <div className="modal-backdrop">
          <div className="modal-container max-w-md">
            <div className="modal-header">
              <div className="flex items-center gap-2">
                <ShieldCheck size={20} className="text-accent" />
                <h3 className="modal-title text-base">Calificar Función de Cineteca</h3>
              </div>
              <button
                onClick={() => setReviewingTicket(null)}
                className="modal-close-btn"
                aria-label="Cerrar modal"
              >
                <X size={18} />
              </button>
            </div>

            <form onSubmit={handleSubmitTicketReview}>
              <div className="modal-body space-y-4">
                <div className="p-3 bg-muted rounded-md text-xs">
                  <strong>Función:</strong> {reviewingTicket.proyeccion?.titulo}<br />
                  <strong>Folio Boleto:</strong> {reviewingTicket.folioBoleto}
                </div>

                <div>
                  <label className="input-label mb-1">Calificación de la Experiencia:</label>
                  <div className="flex gap-2">
                    {[1, 2, 3, 4, 5].map((s) => (
                      <button
                        key={s}
                        type="button"
                        onClick={() => setTicketRating(s)}
                        className="text-amber-400 hover:scale-110 transition"
                      >
                        <Star
                          size={22}
                          className={s <= ticketRating ? 'fill-amber-400 text-amber-400' : 'text-gray-300'}
                        />
                      </button>
                    ))}
                  </div>
                </div>

                <div>
                  <label className="input-label">Tu Opinión Pos-Evento:</label>
                  <textarea
                    rows={3}
                    required
                    placeholder="Comenta sobre la proyección, acústica de la sala o la experiencia..."
                    value={ticketComment}
                    onChange={(e) => setTicketComment(e.target.value)}
                    className="input-text w-full text-xs"
                  />
                </div>
              </div>

              <div className="modal-footer">
                <button
                  type="button"
                  onClick={() => setReviewingTicket(null)}
                  className="btn btn-secondary text-xs"
                >
                  Cancelar
                </button>
                <button
                  type="submit"
                  disabled={reviewLoading}
                  className="btn btn-accent text-xs flex items-center gap-1"
                >
                  <CheckCircle2 size={14} />
                  {reviewLoading ? 'Guardando...' : 'Publicar Reseña Verificada'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Modal de Firma Digital para Co-Responsable (RF-02.3) */}
      {signingLoanCoResp && (
        <DigitalSignatureModal
          isOpen={!!signingLoanCoResp}
          onClose={() => setSigningLoanCoResp(null)}
          onSaveSignature={handleSaveCoResponsibleSignature}
          userName={user?.nombre}
          folioPrestamo={`CO-RESP-${signingLoanCoResp.folio}`}
        />
      )}
    </div>
  );
};
