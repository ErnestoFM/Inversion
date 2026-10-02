import React from 'react';
import { Film, Building2, Package, FileText, AlertTriangle, LayoutDashboard } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

export type TabKey = 'cartelera' | 'espacios' | 'inventario' | 'solicitudes' | 'incidentes' | 'dashboard';

interface NavigationProps {
  activeTab: TabKey;
  onSelectTab: (tab: TabKey) => void;
}

export const Navigation: React.FC<NavigationProps> = ({ activeTab, onSelectTab }) => {
  const { user } = useAuth();
  const isAdminOrCoord = user?.rol === 'ADMIN' || user?.rol === 'COORDINADOR' || user?.rol === 'TECNICO_LAB';

  const tabs: Array<{ key: TabKey; label: string; icon: React.ReactNode; badge?: string; staffOnly?: boolean }> = [
    {
      key: 'cartelera',
      label: 'Cartelera Cineteca',
      icon: <Film size={18} />,
      badge: 'Cultura',
    },
    {
      key: 'espacios',
      label: 'Espacios & Aulas',
      icon: <Building2 size={18} />,
    },
    {
      key: 'inventario',
      label: 'Inventario & Préstamos',
      icon: <Package size={18} />,
    },
    {
      key: 'solicitudes',
      label: 'Mis Solicitudes & Responsivas',
      icon: <FileText size={18} />,
    },
    {
      key: 'incidentes',
      label: 'Incidentes & Reparaciones',
      icon: <AlertTriangle size={18} />,
    },
    {
      key: 'dashboard',
      label: 'Panel de Control',
      icon: <LayoutDashboard size={18} />,
      badge: isAdminOrCoord ? 'Gestión' : undefined,
    },
  ];

  return (
    <nav className="nav-bar-container">
      <div className="nav-tabs-wrapper">
        {tabs.map((tab) => {
          const isActive = activeTab === tab.key;
          return (
            <button
              key={tab.key}
              onClick={() => onSelectTab(tab.key)}
              className={`nav-tab-btn ${isActive ? 'active' : ''}`}
            >
              <span className="tab-icon">{tab.icon}</span>
              <span className="tab-label">{tab.label}</span>
              {tab.badge && (
                <span className={`tab-badge ${isActive ? 'tab-badge-active' : ''}`}>
                  {tab.badge}
                </span>
              )}
            </button>
          );
        })}
      </div>
    </nav>
  );
};
