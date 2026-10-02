import React, { useRef, useState, useEffect } from 'react';
import { PenTool, RotateCcw, CheckCircle2, X } from 'lucide-react';

interface DigitalSignatureModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSaveSignature: (signatureBase64: string) => void;
  folioPrestamo?: string;
  userName?: string;
}

export const DigitalSignatureModal: React.FC<DigitalSignatureModalProps> = ({
  isOpen,
  onClose,
  onSaveSignature,
  folioPrestamo = 'SOL-TEMP',
  userName = 'Usuario Institucional',
}) => {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const [isDrawing, setIsDrawing] = useState(false);
  const [hasSignature, setHasSignature] = useState(false);

  useEffect(() => {
    if (!isOpen) return;
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    // Ajustar resolución interna del canvas
    canvas.width = canvas.offsetWidth;
    canvas.height = canvas.offsetHeight;
    ctx.strokeStyle = '#002B49';
    ctx.lineWidth = 2.5;
    ctx.lineCap = 'round';
    ctx.lineJoin = 'round';

    setHasSignature(false);
  }, [isOpen]);

  if (!isOpen) return null;

  const startDrawing = (e: React.MouseEvent<HTMLCanvasElement> | React.TouchEvent<HTMLCanvasElement>) => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const rect = canvas.getBoundingClientRect();
    const clientX = 'touches' in e ? e.touches[0].clientX : e.clientX;
    const clientY = 'touches' in e ? e.touches[0].clientY : e.clientY;

    ctx.beginPath();
    ctx.moveTo(clientX - rect.left, clientY - rect.top);
    setIsDrawing(true);
  };

  const draw = (e: React.MouseEvent<HTMLCanvasElement> | React.TouchEvent<HTMLCanvasElement>) => {
    if (!isDrawing) return;
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const rect = canvas.getBoundingClientRect();
    const clientX = 'touches' in e ? e.touches[0].clientX : e.clientX;
    const clientY = 'touches' in e ? e.touches[0].clientY : e.clientY;

    ctx.lineTo(clientX - rect.left, clientY - rect.top);
    ctx.stroke();
    setHasSignature(true);
  };

  const stopDrawing = () => {
    setIsDrawing(false);
  };

  const clearCanvas = () => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    setHasSignature(false);
  };

  const handleConfirm = () => {
    const canvas = canvasRef.current;
    if (!canvas || !hasSignature) return;
    const dataUrl = canvas.toDataURL('image/png');
    onSaveSignature(dataUrl);
    onClose();
  };

  return (
    <div className="modal-backdrop">
      <div className="modal-container max-w-lg">
        <div className="modal-header">
          <div className="flex items-center gap-2">
            <PenTool size={20} className="text-accent" />
            <h3 className="modal-title">Firma Electrónica de Responsiva</h3>
          </div>
          <button onClick={onClose} className="modal-close-btn" aria-label="Cerrar modal">
            <X size={18} />
          </button>
        </div>

        <div className="modal-body">
          <div className="p-3 bg-muted rounded-md mb-4 text-sm border-l-4 border-accent">
            <strong>Declaración de Conformidad:</strong>
            <p className="mt-1 text-secondary">
              Yo, <strong>{userName}</strong>, acepto la custodia del equipo bajo el folio{' '}
              <code>{folioPrestamo}</code>, comprometiéndome a su cuidado y devolución en los plazos
              establecidos por el Centro Universitario de Tonalá (CUTonalá).
            </p>
          </div>

          <p className="text-xs text-secondary mb-2 font-medium">
            Traza tu firma en el recuadro inferior utilizando tu mouse o pantalla táctil:
          </p>

          <div className="canvas-wrapper">
            <canvas
              ref={canvasRef}
              className="signature-canvas"
              onMouseDown={startDrawing}
              onMouseMove={draw}
              onMouseUp={stopDrawing}
              onMouseLeave={stopDrawing}
              onTouchStart={startDrawing}
              onTouchMove={draw}
              onTouchEnd={stopDrawing}
            />
            <div className="canvas-signature-line" />
            <span className="canvas-signature-hint">Línea de firma autorizada</span>
          </div>

          <div className="flex justify-between items-center mt-3 text-xs text-muted">
            <span>Hash SHA-256 generado al firmar</span>
            <button
              type="button"
              onClick={clearCanvas}
              className="btn btn-secondary btn-sm flex items-center gap-1"
            >
              <RotateCcw size={13} />
              Limpiar trazo
            </button>
          </div>
        </div>

        <div className="modal-footer">
          <button type="button" onClick={onClose} className="btn btn-secondary">
            Cancelar
          </button>
          <button
            type="button"
            disabled={!hasSignature}
            onClick={handleConfirm}
            className="btn btn-accent flex items-center gap-2"
          >
            <CheckCircle2 size={16} />
            Estampar Firma y Aceptar
          </button>
        </div>
      </div>
    </div>
  );
};
