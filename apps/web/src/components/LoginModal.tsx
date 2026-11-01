import React, { useState, useEffect } from 'react';
import { Mail, Lock, Eye, EyeOff, AlertCircle, X, LogIn, ShieldCheck } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

interface LoginModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export const LoginModal: React.FC<LoginModalProps> = ({ isOpen, onClose }) => {
  const { login } = useAuth();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    if (isOpen) {
      setError(null);
      setPassword('');
    }
  }, [isOpen]);

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && isOpen) {
        onClose();
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!email.trim() || !password) {
      setError('Por favor completa todos los campos requeridos.');
      return;
    }

    try {
      setIsLoading(true);
      setError(null);
      await login(email.trim(), password);
      onClose();
    } catch (err: any) {
      setError(err.message || 'Error al iniciar sesión. Verifica tus credenciales.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="modal-backdrop" onClick={onClose} role="dialog" aria-modal="true">
      <div
        className="login-modal-container"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Encabezado del Modal */}
        <div className="login-modal-header">
          <div className="login-brand-group">
            <div className="login-brand-icon">
              <ShieldCheck size={24} />
            </div>
            <div>
              <h3 className="login-modal-title">
                Acceso Institucional SIGRE
              </h3>
              <p className="login-modal-subtitle">
                Centro Universitario de Tonalá — UdeG
              </p>
            </div>
          </div>
          <button
            type="button"
            onClick={onClose}
            className="icon-btn text-secondary hover:text-primary"
            aria-label="Cerrar ventana de acceso"
          >
            <X size={18} />
          </button>
        </div>

        {/* Formulario de Login */}
        <form onSubmit={handleSubmit} className="login-modal-form">
          {error && (
            <div className="login-alert-error">
              <AlertCircle size={18} style={{ flexShrink: 0, marginTop: 2 }} />
              <span>{error}</span>
            </div>
          )}

          <div className="login-field-group">
            <label className="login-label">
              Correo Institucional
            </label>
            <div className="login-input-box">
              <div className="login-input-icon">
                <Mail size={17} />
              </div>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="ejemplo@alumnos.udg.mx o docente@udg.mx"
                className="login-input"
                autoComplete="email"
                autoFocus
                required
                disabled={isLoading}
              />
            </div>
            <span className="login-hint">
              Utiliza tu cuenta oficial de estudiante, profesor o administrativo.
            </span>
          </div>

          <div className="login-field-group">
            <label className="login-label">
              Contraseña
            </label>
            <div className="login-input-box">
              <div className="login-input-icon">
                <Lock size={17} />
              </div>
              <input
                type={showPassword ? 'text' : 'password'}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Ingresa tu contraseña"
                className="login-input login-input-has-toggle"
                autoComplete="current-password"
                required
                disabled={isLoading}
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="login-toggle-btn"
                aria-label={showPassword ? 'Ocultar contraseña' : 'Ver contraseña'}
                tabIndex={-1}
              >
                {showPassword ? <EyeOff size={17} /> : <Eye size={17} />}
              </button>
            </div>
          </div>

          <button
            type="submit"
            disabled={isLoading}
            className="login-submit-button"
          >
            {isLoading ? (
              <>
                <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                <span>Autenticando en CUTonalá...</span>
              </>
            ) : (
              <>
                <LogIn size={17} />
                <span>Ingresar al Sistema</span>
              </>
            )}
          </button>
        </form>

        {/* Pie de Página Institucional & Aviso Legal */}
        <div className="login-modal-footer">
          Protegido bajo normativas de confidencialidad institucional y protección de datos personales de la Universidad de Guadalajara.
        </div>
      </div>
    </div>
  );
};
