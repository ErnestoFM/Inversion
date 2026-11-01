import React from 'react';
import { Film, Building2, Package, FileText, AlertTriangle, LayoutDashboard } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { canAccessDashboard, isStaffUser } from '../utils/roles';

export type TabKey = 'cartelera' | 'espacios' | 'inventario' | 'solicitudes' | 'incidentes' | 'dashboard';

interface NavigationProps {
  activeTab: TabKey;
  onSelectTab: (tab: TabKey) => void;
}

export const Navigation: React.FC<NavigationProps> = ({ activeTab, onSelectTab }) => {
  const { user } = useAuth();
  const hasDashboardAccess = canAccessDashboard(user);
  const isStaff = isStaffUser(user);

  const tabs: Array<{ key: TabKey; label: string; icon: React.ReactNode; badge?: string; visible: boolean }> = [
    {
      key: 'cartelera',
      label: 'Cartelera Cineteca',
      icon: <Film size={18} />,
      badge: 'Cultura',
      visible: true,
    },
    {
      key: 'espacios',
      label: 'Espacios & Aulas',
      icon: <Building2 size={18} />,
      visible: true,
    },
    {
      key: 'inventario',
      label: 'Inventario & Préstamos',
      icon: <Package size={18} />,
      visible: true,
    },
    {
      key: 'solicitudes',
      label: isStaff ? 'Gestión de Préstamos' : 'Mis Solicitudes & Responsivas',
      icon: <FileText size={18} />,
      badge: isStaff ? 'Control' : undefined,
      visible: true,
    },
    {
      key: 'incidentes',
      label: isStaff ? 'Gestión de Incidentes' : 'Reportar Incidencias',
      icon: <AlertTriangle size={18} />,
      visible: true,
    },
    {
      key: 'dashboard',
      label: 'Panel Ejecutivo & Inversión',
      icon: <LayoutDashboard size={18} />,
      badge: 'Ejecutivo',
      visible: hasDashboardAccess,
    },
  ];

  return (
    <nav className="nav-bar-container">
      <div className="nav-tabs-wrapper">
        {tabs
          .filter((tab) => tab.visible)
          .map((tab) => {
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
