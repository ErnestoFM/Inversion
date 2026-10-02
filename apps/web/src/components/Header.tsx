import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { useTheme } from '../context/ThemeContext';
import {
  Sun,
  Moon,
  Bell,
  LogOut,
  ShieldCheck,
  Clock,
  Sparkles,
  ChevronDown
} from 'lucide-react';
import { api } from '../api/client';
import type { NotificationItem } from '../types';

export const Header: React.FC = () => {
  const { user, logout, loginAs } = useAuth();
  const { theme, toggleTheme } = useTheme();
  const [currentTime, setCurrentTime] = useState<string>('');
  const [notifications, setNotifications] = useState<NotificationItem[]>([]);
  const [unreadCount, setUnreadCount] = useState<number>(0);
  const [showNotifications, setShowNotifications] = useState<boolean>(false);
  const [showUserMenu, setShowUserMenu] = useState<boolean>(false);

  // Reloj institucional CUTonalá en vivo
  useEffect(() => {
    const updateClock = () => {
      const now = new Date();
      setCurrentTime(
        now.toLocaleTimeString('es-MX', {
          hour: '2-digit',
          minute: '2-digit',
          second: '2-digit',
          hour12: false,
        })
      );
    };
    updateClock();
    const interval = setInterval(updateClock, 1000);
    return () => clearInterval(interval);
  }, []);

  // Carga periódica de notificaciones
  useEffect(() => {
    if (!user) return;
    const fetchNotifications = async () => {
      try {
        const res = await api.notifications.list();
        setNotifications(res.notificaciones);
        setUnreadCount(res.totalNoLeidas);
      } catch (e) {
        // Silenciar si no hay auth
      }
    };
    fetchNotifications();
    const interval = setInterval(fetchNotifications, 30000);
    return () => clearInterval(interval);
  }, [user]);

  const handleMarkAsRead = async (id: string) => {
    try {
      await api.notifications.markAsRead(id);
      setNotifications((prev) =>
        prev.map((n) => (n.id === id ? { ...n, leido: true } : n))
      );
      setUnreadCount((c) => Math.max(0, c - 1));
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <header className="header-institutional">
      <div className="header-container">
        {/* Logos institucionales */}
        <div className="brand-group">
          <div className="logo-badge">
            <span className="logo-udg">UdeG</span>
            <span className="logo-divider">|</span>
            <span className="logo-sigre">SIGRE</span>
          </div>
          <div className="campus-info">
            <span className="campus-title">CUTonalá</span>
            <span className="campus-sub">Centro Universitario de Tonalá</span>
          </div>
        </div>

        {/* Reloj y Estado Campus */}
        <div className="campus-status-pill">
          <Clock size={15} className="pulse-icon text-accent" />
          <span className="status-text">Horario CUTonalá: Lun–Sáb 08:00–19:00</span>
          <span className="clock-badge">{currentTime || '08:00:00'}</span>
        </div>

        {/* Acciones de Usuario y Tema */}
        <div className="header-actions">
          {/* Botón de Tema (Claro / Oscuro) */}
          <button
            onClick={toggleTheme}
            className="icon-btn"
            title={theme === 'dark' ? 'Cambiar a modo claro' : 'Cambiar a modo oscuro'}
            aria-label="Alternar tema"
          >
            {theme === 'dark' ? <Sun size={19} className="text-warning" /> : <Moon size={19} />}
          </button>

          {/* Notificaciones */}
          {user && (
            <div className="relative">
              <button
                onClick={() => setShowNotifications(!showNotifications)}
                className="icon-btn relative"
                title="Notificaciones"
                aria-label="Ver notificaciones"
              >
                <Bell size={19} />
                {unreadCount > 0 && (
                  <span className="notification-counter">{unreadCount}</span>
                )}
              </button>

              {showNotifications && (
                <div className="notifications-dropdown">
                  <div className="dropdown-header">
                    <h4>Notificaciones del Sistema</h4>
                    <span className="badge badge-primary">{unreadCount} pendientes</span>
                  </div>
                  <div className="dropdown-list">
                    {notifications.length === 0 ? (
                      <p className="p-sm text-secondary text-center py-4">No tienes notificaciones pendientes.</p>
                    ) : (
                      notifications.slice(0, 5).map((n) => (
                        <div
                          key={n.id}
                          className={`notification-item ${!n.leido ? 'unread' : ''}`}
                          onClick={() => handleMarkAsRead(n.id)}
                        >
                          <div className="notif-title">{n.titulo}</div>
                          <div className="notif-msg">{n.mensaje}</div>
                          <div className="notif-time">
                            {new Date(n.created_at).toLocaleDateString('es-MX', {
                              hour: '2-digit',
                              minute: '2-digit',
                            })}
                          </div>
                        </div>
                      ))
                    )}
                  </div>
                </div>
              )}
            </div>
          )}

          {/* Perfil de Usuario o Botón Iniciar Sesión */}
          {user ? (
            <div className="relative">
              <button
                onClick={() => setShowUserMenu(!showUserMenu)}
                className="user-profile-btn"
              >
                <div className="avatar-circle">
                  {user.nombre.charAt(0).toUpperCase()}
                </div>
                <div className="user-details">
                  <span className="user-name">{user.nombre.split(' ')[0]}</span>
                  <div className="user-trust-tag">
                    <ShieldCheck size={13} className="text-accent" />
                    <span>{user.reputationScore}/100 pts</span>
                  </div>
                </div>
                <ChevronDown size={14} className="text-secondary ml-1" />
              </button>

              {showUserMenu && (
                <div className="user-dropdown-menu">
                  <div className="dropdown-user-header">
                    <strong>{user.nombre}</strong>
                    <div className="text-sm text-secondary font-mono">{user.email}</div>
                    <span className="badge badge-accent mt-2">Rol: {user.rol}</span>
                  </div>

                  <div className="dropdown-divider" />

                  <div className="dropdown-section-title">Cambiar a cuenta de prueba:</div>
                  <button
                    className="menu-item-btn"
                    onClick={() => {
                      loginAs('ESTUDIANTE');
                      setShowUserMenu(false);
                    }}
                  >
                    🎓 Estudiante (Ernesto Fierro)
                  </button>
                  <button
                    className="menu-item-btn"
                    onClick={() => {
                      loginAs('DOCENTE');
                      setShowUserMenu(false);
                    }}
                  >
                    👩‍🏫 Docente (Dra. Elizabeth)
                  </button>
                  <button
                    className="menu-item-btn"
                    onClick={() => {
                      loginAs('ADMIN');
                      setShowUserMenu(false);
                    }}
                  >
                    🏛️ Coordinador / Admin SIGRE
                  </button>
                  <button
                    className="menu-item-btn"
                    onClick={() => {
                      loginAs('TECNICO');
                      setShowUserMenu(false);
                    }}
                  >
                    🔧 Técnico de Laboratorio
                  </button>

                  <div className="dropdown-divider" />

                  <button
                    className="menu-item-btn text-error"
                    onClick={() => {
                      logout();
                      setShowUserMenu(false);
                    }}
                  >
                    <LogOut size={15} className="mr-2" />
                    Cerrar Sesión
                  </button>
                </div>
              )}
            </div>
          ) : (
            <button
              onClick={() => loginAs('ESTUDIANTE')}
              className="btn btn-accent btn-sm"
            >
              <Sparkles size={14} className="mr-1" />
              Acceso Institucional
            </button>
          )}
        </div>
      </div>
    </header>
  );
};
