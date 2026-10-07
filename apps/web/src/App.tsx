import React, { useState } from 'react';
import { ThemeProvider } from './context/ThemeContext';
import { AuthProvider, useAuth } from './context/AuthContext';
import { Header } from './components/Header';
import { Navigation, type TabKey } from './components/Navigation';
import { Footer } from './components/Footer';
import { QrCameraScannerModal } from './components/QrCameraScannerModal';
import { CarteleraView } from './pages/CarteleraView';
import { SpacesView } from './pages/SpacesView';
import { InventoryView } from './pages/InventoryView';
import { LoansAndBookingsView } from './pages/LoansAndBookingsView';
import { IncidentsView } from './pages/IncidentsView';
import { DashboardView } from './pages/DashboardView';

const MainApp: React.FC = () => {
  const [activeTab, setActiveTab] = useState<TabKey>('cartelera');
  const [isQrScannerOpen, setIsQrScannerOpen] = useState<boolean>(false);
  const { user, loginAs } = useAuth();

  return (
    <div className="app-layout">
      {/* Header Institucional con UdeG, CUTonalá y Reloj */}
      <Header onOpenQrScanner={() => setIsQrScannerOpen(true)} />

      {/* Barra de Navegación Principal */}
      <Navigation activeTab={activeTab} onSelectTab={setActiveTab} />

      {/* Banner de bienvenida si es usuario de prueba */}
      {!user && (
        <div className="guest-banner">
          <div className="guest-banner-content">
            <span className="font-semibold">Acceso de Demostración CUTonalá:</span>
            <span className="text-secondary text-sm ml-2">
              Inicia sesión rápida para interactuar con el sistema de reservas y préstamos:
            </span>
            <div className="flex gap-2 mt-2 sm:mt-0 flex-wrap">
              <button
                type="button"
                onClick={() => loginAs('ESTUDIANTE')}
                className="btn btn-accent btn-xs"
              >
                🎓 Ernesto Fierro (Alumno)
              </button>
              <button
                type="button"
                onClick={() => loginAs('DOCENTE')}
                className="btn btn-secondary btn-xs"
              >
                👩‍🏫 Dra. Elizabeth (Docente)
              </button>
              <button
                type="button"
                onClick={() => loginAs('ADMIN')}
                className="btn btn-primary btn-xs"
              >
                🏛️ Coordinador SIGRE
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Vistas Principales */}
      <main className="main-content">
        {activeTab === 'cartelera' && (
          <CarteleraView onOpenQrScanner={() => setIsQrScannerOpen(true)} />
        )}
        {activeTab === 'espacios' && <SpacesView />}
        {activeTab === 'inventario' && <InventoryView />}
        {activeTab === 'solicitudes' && <LoansAndBookingsView />}
        {activeTab === 'incidentes' && <IncidentsView />}
        {activeTab === 'dashboard' && <DashboardView />}
      </main>

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
    <ThemeProvider>
      <AuthProvider>
        <MainApp />
      </AuthProvider>
    </ThemeProvider>
  );
}
