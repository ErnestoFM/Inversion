import React, { useState, useEffect } from 'react';
import {
  Package,
  Laptop,
  Tv,
  Microscope,
  Wrench,
  Search,
  CheckCircle2,
  AlertCircle,
  FileSignature,
  X,
  Clock,
  UserCheck,
} from 'lucide-react';
import { api } from '../api/client';
import { useAuth } from '../context/AuthContext';
import { DigitalSignatureModal } from '../components/DigitalSignatureModal';
import type { Resource } from '../types';

export const InventoryView: React.FC = () => {
  const { user } = useAuth();
  const [recursos, setRecursos] = useState<Resource[]>([]);
  const [selectedCategoria, setSelectedCategoria] = useState<string>('');
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Modal para solicitar préstamo
  const [selectedResource, setSelectedResource] = useState<Resource | null>(null);
  const [fechaInicio, setFechaInicio] = useState<string>('');
  const [fechaDevolucion, setFechaDevolucion] = useState<string>('');
  const [esExtendido, setEsExtendido] = useState<boolean>(false);
  const [justificacionExtendida, setJustificacionExtendida] = useState<string>('');
  const [coResponsableCodigo, setCoResponsableCodigo] = useState<string>('');
  const [digitalSignature, setDigitalSignature] = useState<string | null>(null);

  // Modal de Firma Canvas
  const [showSignatureModal, setShowSignatureModal] = useState<boolean>(false);
  const [loanResult, setLoanResult] = useState<{ folio: string; id: string } | null>(null);
  const [loanLoading, setLoanLoading] = useState(false);

  useEffect(() => {
    fetchRecursos();
  }, [selectedCategoria, searchQuery]);

  const fetchRecursos = async () => {
    try {
      setLoading(true);
      const res = await api.resources.list({
        categoria: selectedCategoria || undefined,
        search: searchQuery || undefined,
      });
      setRecursos(res?.recursos || []);
    } catch (err: any) {
      setError(err.message || 'Error al obtener inventario');
    } finally {
      setLoading(false);
    }
  };

  const handleOpenLoanModal = (recurso: Resource) => {
    setSelectedResource(recurso);
    setLoanResult(null);
    setDigitalSignature(null);
    setEsExtendido(false);
    setJustificacionExtendida('');
    setCoResponsableCodigo('');

    const hoy = new Date();
    setFechaInicio(hoy.toISOString().split('T')[0]);

    // Préstamo normal de 3 días máximo por reglamento
    const maxNormal = new Date();
    maxNormal.setDate(maxNormal.getDate() + 3);
    setFechaDevolucion(maxNormal.toISOString().split('T')[0]);
  };

  const handleConfirmLoan = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedResource) return;
    if (!user) {
      alert('Debes iniciar sesión con tu cuenta institucional UdeG.');
      return;
    }
    if (!digitalSignature) {
      alert('Debes firmar electrónicamente la responsiva antes de enviar la solicitud.');
      return;
    }

    try {
      setLoanLoading(true);
      const res = await api.resources.requestLoan({
        recursoId: selectedResource.id,
        fechaInicio: `${fechaInicio}T09:00:00.000Z`,
        fechaLimiteDevolucion: `${fechaDevolucion}T18:00:00.000Z`,
        esPrestamoExtendido: esExtendido,
        justificacionExtendida: esExtendido ? justificacionExtendida : undefined,
        coResponsableCodigo: coResponsableCodigo || undefined,
        firmaDigitalBase64: digitalSignature,
      });

      setLoanResult({ folio: res.prestamo.folio, id: res.prestamo.id });
      // Refrescar inventario
      fetchRecursos();
    } catch (err: any) {
      alert(`Error al solicitar préstamo: ${err.message}`);
    } finally {
      setLoanLoading(false);
    }
  };

  const getCategoryIcon = (cat: string) => {
    switch (cat) {
      case 'COMPUTO':
        return <Laptop size={18} className="text-accent" />;
      case 'AUDIOVISUAL':
        return <Tv size={18} className="text-accent" />;
      case 'LABORATORIO':
        return <Microscope size={18} className="text-accent" />;
      default:
        return <Wrench size={18} className="text-accent" />;
    }
  };

  return (
    <div className="view-container">
      {/* Encabezado */}
      <div className="section-header">
        <div>
          <h2 className="section-title">Inventario y Préstamo de Recursos</h2>
          <p className="section-subtitle">
            Equipamiento de cómputo, laboratorio y audiovisual del almacén de CUTonalá.
          </p>
        </div>

        {/* Búsqueda y Filtros */}
        <div className="flex gap-2 flex-wrap">
          <div className="relative search-input-wrapper">
            <Search size={16} className="search-icon" />
            <input
              type="text"
              placeholder="Buscar por nombre o placa..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="input-text pl-8"
            />
          </div>

          <select
            value={selectedCategoria}
            onChange={(e) => setSelectedCategoria(e.target.value)}
            className="input-select"
          >
            <option value="">Todas las Categorías</option>
            <option value="COMPUTO">Cómputo</option>
            <option value="AUDIOVISUAL">Audiovisual</option>
            <option value="LABORATORIO">Laboratorio</option>
            <option value="HERRAMIENTAS">Herramientas</option>
          </select>
        </div>
      </div>

      {/* Regla CUTonalá de Préstamos */}
      <div className="notice-banner">
        <Clock size={18} className="text-accent flex-shrink-0" />
        <div className="text-xs leading-relaxed">
          <strong>Regla de Préstamos CUTonalá:</strong> El periodo estándar es de máximo <strong>3 días</strong>.
          Los préstamos extendidos (hasta 30 días para cómputo o proyectos de tesis) requieren
          justificación y visto bueno. La firma de la responsiva digital es obligatoria.
        </div>
      </div>

      {loading ? (
        <div className="loading-state">
          <div className="spinner"></div>
          <p className="text-secondary mt-3">Consultando inventario de almacén...</p>
        </div>
      ) : error ? (
        <div className="alert-box alert-error">
          <AlertCircle size={20} />
          <div>{error}</div>
        </div>
      ) : (
        <div className="grid-cards">
          {recursos.map((rec) => {
            const disponible = rec.estado === 'DISPONIBLE';

            return (
              <div key={rec.id} className="card resource-card">
                <div className="card-header flex justify-between items-start">
                  <div className="flex items-center gap-2">
                    {getCategoryIcon(rec.categoria)}
                    <div>
                      <h3 className="card-title text-base">{rec.nombre}</h3>
                      <span className="font-mono text-xs text-muted">
                        Placa: {rec.codigoInventario}
                      </span>
                    </div>
                  </div>
                  <span
                    className={`badge ${
                      disponible ? 'badge-accent' : 'badge-secondary'
                    }`}
                  >
                    {rec.estado}
                  </span>
                </div>

                <div className="card-body">
                  <div className="resource-specs space-y-1 text-xs text-secondary mt-2">
                    <div>
                      <strong>Marca/Modelo:</strong> {rec.marca || 'N/A'} {rec.modelo || ''}
                    </div>
                    <div>
                      <strong>Ubicación:</strong> {rec.ubicacion}
                    </div>
                    <div>
                      <strong>Estado Físico:</strong>{' '}
                      <span className="font-semibold text-primary">
                        {rec.condicionFisica}
                      </span>
                    </div>
                    <div>
                      <strong>Horas de Uso Acumuladas:</strong>{' '}
                      <span className="font-mono">{rec.horasUsoTotales || 0} hrs</span>
                    </div>
                  </div>

                  <div className="card-footer mt-4">
                    <button
                      type="button"
                      disabled={!disponible}
                      onClick={() => handleOpenLoanModal(rec)}
                      className={`btn w-full ${disponible ? 'btn-accent' : 'btn-secondary'}`}
                    >
                      <Package size={16} className="mr-2" />
                      {disponible ? 'Solicitar Préstamo' : 'No Disponible'}
                    </button>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      )}

      {/* Modal de Solicitud de Préstamo */}
      {selectedResource && (
        <div className="modal-backdrop">
          <div className="modal-container max-w-lg">
            <div className="modal-header">
              <div className="flex items-center gap-2">
                <Package size={20} className="text-accent" />
                <h3 className="modal-title">Préstamo: {selectedResource.nombre}</h3>
              </div>
              <button
                onClick={() => setSelectedResource(null)}
                className="modal-close-btn"
                aria-label="Cerrar modal"
              >
                <X size={18} />
              </button>
            </div>

            {loanResult ? (
              <div className="modal-body text-center py-6">
                <div className="w-16 h-16 bg-accent-soft text-accent rounded-full flex items-center justify-center mx-auto mb-3">
                  <CheckCircle2 size={36} />
                </div>
                <h3 className="text-lg font-bold">¡Préstamo Solicitado con Éxito!</h3>
                <p className="text-secondary text-sm mt-1">
                  Tu responsiva digital ha sido firmada y archivada. Puedes descargar el comprobante en
                  formato PDF.
                </p>
                <div className="mt-4 p-3 bg-muted rounded-md inline-block">
                  <span className="text-xs text-secondary">Folio de Préstamo:</span>
                  <div className="font-mono font-bold text-accent text-lg">
                    {loanResult.folio}
                  </div>
                </div>

                <div className="mt-6 flex flex-col gap-2">
                  <a
                    href={api.loans.downloadResponsivaPdf(loanResult.id)}
                    target="_blank"
                    rel="noreferrer"
                    className="btn btn-primary"
                  >
                    Descargar Responsiva PDF Oficial
                  </a>
                  <button
                    type="button"
                    onClick={() => setSelectedResource(null)}
                    className="btn btn-secondary"
                  >
                    Cerrar
                  </button>
                </div>
              </div>
            ) : (
              <form onSubmit={handleConfirmLoan}>
                <div className="modal-body space-y-4">
                  <div className="grid grid-cols-2 gap-3">
                    <div>
                      <label className="input-label">Fecha de Entrega</label>
                      <input
                        type="date"
                        required
                        value={fechaInicio}
                        onChange={(e) => setFechaInicio(e.target.value)}
                        className="input-text w-full"
                      />
                    </div>
                    <div>
                      <label className="input-label">Fecha de Devolución</label>
                      <input
                        type="date"
                        required
                        value={fechaDevolucion}
                        onChange={(e) => setFechaDevolucion(e.target.value)}
                        className="input-text w-full"
                      />
                    </div>
                  </div>

                  {/* Toggle Préstamo Extendido */}
                  <div className="p-3 bg-muted rounded-md space-y-2">
                    <label className="flex items-center gap-2 cursor-pointer">
                      <input
                        type="checkbox"
                        checked={esExtendido}
                        onChange={(e) => setEsExtendido(e.target.checked)}
                        className="checkbox-custom"
                      />
                      <span className="text-sm font-semibold text-primary">
                        Solicitar Préstamo Extendido (Mayor a 3 días)
                      </span>
                    </label>

                    {esExtendido && (
                      <div className="mt-2">
                        <label className="input-label">Justificación Especial</label>
                        <textarea
                          rows={2}
                          required={esExtendido}
                          value={justificacionExtendida}
                          onChange={(e) => setJustificacionExtendida(e.target.value)}
                          placeholder="Explica el proyecto de investigación, materia o justificación por la que requieres el equipo por más de 3 días..."
                          className="input-text w-full"
                        />
                      </div>
                    )}
                  </div>

                  {/* Co-Responsable Solidario */}
                  <div>
                    <label className="input-label flex items-center gap-1">
                      <UserCheck size={14} className="text-accent" />
                      Código UdeG de Co-Responsable (Opcional)
                    </label>
                    <input
                      type="text"
                      placeholder="Ej. 219876543"
                      value={coResponsableCodigo}
                      onChange={(e) => setCoResponsableCodigo(e.target.value)}
                      className="input-text w-full font-mono"
                    />
                    <span className="input-hint">
                      Permite que un compañero de brigada o equipo asuma custodia compartida.
                    </span>
                  </div>

                  {/* Firma Electrónica Obligatoria */}
                  <div className="p-3 border rounded-md border-default">
                    <div className="flex justify-between items-center">
                      <div>
                        <div className="text-sm font-semibold flex items-center gap-1">
                          <FileSignature size={16} className="text-accent" />
                          Firma de Responsiva Digital
                        </div>
                        <p className="text-xs text-secondary mt-0.5">
                          {digitalSignature
                            ? 'Firma digital registrada y vinculada a la responsiva.'
                            : 'Es obligatorio plasmar tu firma para comprometerte al cuidado del bien.'}
                        </p>
                      </div>

                      <button
                        type="button"
                        onClick={() => setShowSignatureModal(true)}
                        className={`btn btn-sm ${
                          digitalSignature ? 'btn-accent' : 'btn-primary'
                        }`}
                      >
                        {digitalSignature ? 'Modificar Firma' : 'Firmar Ahora'}
                      </button>
                    </div>

                    {digitalSignature && (
                      <div className="mt-2 p-2 bg-surface rounded flex items-center gap-2 border border-accent">
                        <CheckCircle2 size={16} className="text-accent" />
                        <span className="text-xs text-accent font-medium">
                          Firma electrónica lista para estampar en el acta PDF.
                        </span>
                      </div>
                    )}
                  </div>
                </div>

                <div className="modal-footer">
                  <button
                    type="button"
                    onClick={() => setSelectedResource(null)}
                    className="btn btn-secondary"
                  >
                    Cancelar
                  </button>
                  <button
                    type="submit"
                    disabled={loanLoading || !digitalSignature}
                    className="btn btn-accent flex items-center gap-2"
                  >
                    {loanLoading ? (
                      <span className="spinner-sm" />
                    ) : (
                      <CheckCircle2 size={16} />
                    )}
                    Confirmar y Generar Responsiva
                  </button>
                </div>
              </form>
            )}
          </div>
        </div>
      )}

      {/* Modal de Firma Canvas */}
      <DigitalSignatureModal
        isOpen={showSignatureModal}
        onClose={() => setShowSignatureModal(false)}
        onSaveSignature={(sig) => setDigitalSignature(sig)}
        userName={user?.nombre}
        folioPrestamo={`SOL-${selectedResource?.codigoInventario || 'REC'}`}
      />
    </div>
  );
};
