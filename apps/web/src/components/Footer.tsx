import React, { useState } from 'react';
import { ShieldCheck, Info, X } from 'lucide-react';

export const Footer: React.FC = () => {
  const [showLegalModal, setShowLegalModal] = useState(false);

  return (
    <>
      <footer className="footer-institutional">
        <div className="footer-container">
          <div className="footer-column">
            <div className="footer-logo">
              <span className="font-bold text-accent">SIGRE</span>
              <span className="text-secondary ml-1">CUTonalá</span>
            </div>
            <p className="footer-desc">
              Sistema Integrado de Gestión de Recursos y Espacios del Centro Universitario de Tonalá.
              Universidad de Guadalajara.
            </p>
          </div>

          <div className="footer-column">
            <h4>Políticas y Normativa</h4>
            <ul className="footer-links">
              <li>
                <button
                  type="button"
                  onClick={() => setShowLegalModal(true)}
                  className="footer-link-btn"
                >
                  <ShieldCheck size={14} className="text-accent" />
                  Aviso de Privacidad (LGPDPPSO)
                </button>
              </li>
              <li>
                <button
                  type="button"
                  onClick={() => setShowLegalModal(true)}
                  className="footer-link-btn"
                >
                  <Info size={14} className="text-accent" />
                  Uso de Cookies y Almacenamiento
                </button>
              </li>
              <li>
                <a
                  href="http://www.cutonala.udg.mx"
                  target="_blank"
                  rel="noreferrer"
                  className="footer-link-btn"
                >
                  Portal Oficial CUTonalá
                </a>
              </li>
            </ul>
          </div>

          <div className="footer-column">
            <h4>Soporte Técnico y Laboratorios</h4>
            <p className="text-xs text-secondary leading-relaxed">
              Edificio de Ingenierías y Aulas Amplias.<br />
              Horario de atención: Lunes a Sábado de 08:00 a 19:00 hrs.<br />
              Contacto: <code>soporte.sigre@cutonala.udg.mx</code>
            </p>
          </div>
        </div>

        <div className="footer-bottom">
          <p>© {new Date().getFullYear()} Universidad de Guadalajara. Todos los derechos reservados.</p>
          <span className="text-muted text-xs">Versión 1.0.0 — CUTonalá Cloud Run Edition</span>
        </div>
      </footer>

      {showLegalModal && (
        <div className="modal-backdrop">
          <div className="modal-container max-w-2xl">
            <div className="modal-header">
              <div className="flex items-center gap-2">
                <ShieldCheck size={20} className="text-accent" />
                <h3 className="modal-title">Aviso de Privacidad y Marco Legal</h3>
              </div>
              <button
                onClick={() => setShowLegalModal(false)}
                className="modal-close-btn"
                aria-label="Cerrar modal"
              >
                <X size={18} />
              </button>
            </div>
            <div className="modal-body space-y-4 text-sm leading-relaxed max-h-96 overflow-y-auto pr-2">
              <div className="p-3 bg-muted rounded-md text-xs border-l-4 border-accent">
                <strong>Cumplimiento Normativo:</strong> Conforme a la Ley General de Protección de Datos
                Personales en Posesión de Sujetos Obligados (LGPDPPSO) y la Ley de Transparencia del
                Estado de Jalisco.
              </div>
              <h4 className="font-semibold text-primary">1. Identidad del Responsable</h4>
              <p className="text-secondary">
                La Universidad de Guadalajara, a través del Centro Universitario de Tonalá (CUTonalá), con
                domicilio en Av. Nuevo Periférico No. 555, es responsable del tratamiento de los datos
                personales recabados a través del portal SIGRE.
              </p>
              <h4 className="font-semibold text-primary">2. Finalidad del Tratamiento</h4>
              <p className="text-secondary">
                Sus datos (nombre, código institucional, correo UdeG, carreras, firmas electrónicas y
                fotografías de incidencias) se recaban con el único propósito de validar la identidad para la
                reserva de espacios físicos (Auditorios, Cineteca, Laboratorios) y el control de inventario de
                equipamiento institucional.
              </p>
              <h4 className="font-semibold text-primary">3. Política de Cookies y Almacenamiento</h4>
              <p className="text-secondary">
                SIGRE utiliza <strong>únicamente cookies técnicas y almacenamiento local estrictamente necesario</strong> para:
              </p>
              <ul className="list-disc pl-5 text-secondary space-y-1">
                <li>Mantener la sesión autenticada con JWT.</li>
                <li>Prevenir colisiones y duplicidad de reservas mediante bloqueos en Redis (15 minutos).</li>
                <li>Recordar la preferencia de tema (claro u oscuro).</li>
                <li><strong>No se utilizan cookies de terceros ni con fines de rastreo publicitario.</strong></li>
              </ul>
              <h4 className="font-semibold text-primary">4. Almacenamiento Seguro de Evidencias</h4>
              <p className="text-secondary">
                Las firmas digitales de responsivas y las fotografías de evidencias de daños se resguardan de
                manera cifrada en Google Cloud Storage (GCS) y se accede a ellas exclusivamente mediante URLs
                prefirmadas de caducidad corta (15 minutos), asegurando la estricta privacidad de la comunidad.
              </p>
            </div>
            <div className="modal-footer">
              <button
                type="button"
                onClick={() => setShowLegalModal(false)}
                className="btn btn-accent"
              >
                Entendido
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
};
