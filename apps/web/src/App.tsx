import React, { useState } from 'react';
import { ThemeProvider } from './context/ThemeContext';
import { AuthProvider, useAuth } from './context/AuthContext';
import { Header } from './components/Header';
import { Navigation, type TabKey } from './components/Navigation';
import { Footer } from './components/Footer';
import { QrCameraScannerModal } from './components/QrCameraScannerModal';
import { LoginModal } from './components/LoginModal';
import { ErrorBoundary } from './components/ErrorBoundary';
import { CarteleraView } from './pages/CarteleraView';
import { SpacesView } from './pages/SpacesView';
import { InventoryView } from './pages/InventoryView';
import { LoansAndBookingsView } from './pages/LoansAndBookingsView';
import { IncidentsView } from './pages/IncidentsView';
import { DashboardView } from './pages/DashboardView';
import { canAccessDashboard } from './utils/roles';
import { ShieldAlert, Film } from 'lucide-react';

const MainApp: React.FC = () => {
  const [activeTab, setActiveTab] = useState<TabKey>('cartelera');
  const [isQrScannerOpen, setIsQrScannerOpen] = useState<boolean>(false);
  const [isLoginModalOpen, setIsLoginModalOpen] = useState<boolean>(false);
  const { user } = useAuth();

  const hasDashboardAccess = canAccessDashboard(user);

  return (
    <div className="app-layout">
      {/* Header Institucional con UdeG, CUTonalá, Reloj y Perfil */}
      <Header
        onOpenQrScanner={() => setIsQrScannerOpen(true)}
        onOpenLogin={() => setIsLoginModalOpen(true)}
      />

      {/* Barra de Navegación Principal Dinámica según Rol */}
      <Navigation activeTab={activeTab} onSelectTab={setActiveTab} />

      {/* Vistas Principales */}
      <main className="main-content">
        {activeTab === 'cartelera' && (
          <CarteleraView onOpenQrScanner={() => setIsQrScannerOpen(true)} />
        )}
        {activeTab === 'espacios' && <SpacesView />}
        {activeTab === 'inventario' && <InventoryView />}
        {activeTab === 'solicitudes' && <LoansAndBookingsView />}
        {activeTab === 'incidentes' && <IncidentsView />}
        {activeTab === 'dashboard' && (
          hasDashboardAccess ? (
            <DashboardView />
          ) : (
            <div className="view-container">
              <div className="card text-center p-8 max-w-xl mx-auto my-12 shadow-md">
                <div className="w-12 h-12 rounded-full bg-amber-500/10 text-amber-500 flex items-center justify-center mx-auto mb-4">
                  <ShieldAlert size={28} />
                </div>
                <h3 className="text-lg font-bold text-primary mb-2">
                  Acceso Restringido al Panel Ejecutivo
                </h3>
                <p className="text-secondary text-sm mb-6 leading-relaxed">
                  Las métricas financieras (VPN, TIR, Flujo Trienal Proforma, CAPEX) y la auditoría predictiva de desgaste de flota de laboratorios están reservadas para las autoridades de Coordinación de Tecnologías, Secretaría Administrativa y Administración de Almacén de CUTonalá.
                </p>
                <div className="flex justify-center gap-3">
                  <button
                    type="button"
                    onClick={() => setActiveTab('cartelera')}
                    className="btn btn-primary btn-sm flex items-center gap-2"
                  >
                    <Film size={14} />
                    <span>Volver a Cartelera Cineteca</span>
                  </button>
                  {!user && (
                    <button
                      type="button"
                      onClick={() => setIsLoginModalOpen(true)}
                      className="btn btn-accent btn-sm"
                    >
                      Identificarse como Coordinador
                    </button>
                  )}
                </div>
              </div>
            </div>
          )
        )}
      </main>

      {/* Modal de Acceso Institucional Formal */}
      <LoginModal
        isOpen={isLoginModalOpen}
        onClose={() => setIsLoginModalOpen(false)}
      />

      {/* Modal de Escaneo con Cámara Física QR */}
      <QrCameraScannerModal
        isOpen={isQrScannerOpen}
        onClose={() => setIsQrScannerOpen(false)}
      />

      {/* Pie de Página Institucional & Marco Legal LGPDPPSO */}
      <Footer />
    </div>
  );
};

export default function App() {
  return (
    <ErrorBoundary>
      <ThemeProvider>
        <AuthProvider>
          <MainApp />
        </AuthProvider>
      </ThemeProvider>
    </ErrorBoundary>
  );
}
