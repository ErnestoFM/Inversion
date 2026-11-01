import { Component, type ErrorInfo, type ReactNode } from 'react';
import { AlertTriangle, RefreshCw } from 'lucide-react';

interface Props {
  children: ReactNode;
}

interface State {
  hasError: boolean;
  error: Error | null;
}

export class ErrorBoundary extends Component<Props, State> {
  public state: State = {
    hasError: false,
    error: null,
  };

  public static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('Uncaught error in React tree:', error, errorInfo);
  }

  private handleReset = () => {
    localStorage.removeItem('sigre_token');
    window.location.reload();
  };

  public render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-screen w-full flex items-center justify-center p-6 bg-base">
          <div className="max-w-md w-full bg-surface border border-default rounded-2xl p-6 text-center shadow-lg">
            <div className="w-12 h-12 rounded-full bg-red-500/10 text-red-500 flex items-center justify-center mx-auto mb-4">
              <AlertTriangle size={24} />
            </div>
            <h3 className="text-lg font-bold text-primary mb-2">
              Se produjo un error en la aplicación
            </h3>
            <p className="text-xs text-secondary mb-4 leading-relaxed">
              Ocurrió un problema al procesar la vista. Hemos aislado el error para evitar cierres inesperados.
            </p>
            {this.state.error?.message && (
              <div className="p-3 bg-muted rounded-lg text-left text-xs font-mono text-secondary mb-4 overflow-x-auto">
                {this.state.error.message}
              </div>
            )}
            <button
              type="button"
              onClick={this.handleReset}
              className="btn btn-primary w-full flex items-center justify-center gap-2"
            >
              <RefreshCw size={15} />
              <span>Reiniciar y Recargar SIGRE</span>
            </button>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}
