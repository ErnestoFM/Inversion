import React, { createContext, useContext, useEffect, useState } from 'react';
import type { User } from '../types';
import { api } from '../api/client';
import { getRecaptchaToken } from '../utils/recaptcha';

interface AuthContextType {
  user: User | null;
  token: string | null;
  loading: boolean;
  login: (email: string, password?: string) => Promise<void>;
  loginAs: (rolePreset: 'ESTUDIANTE' | 'DOCENTE' | 'ADMIN' | 'TECNICO' | 'CINETECA') => Promise<void>;
  logout: () => void;
  refreshUser: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

const PRESET_ACCOUNTS = {
  ESTUDIANTE: 'ernesto.fierro@alumnos.udg.mx',
  DOCENTE: 'elizabeth.hernandez@udg.mx',
  ADMIN: 'admin.sigre@udg.mx',
  TECNICO: 'almacen.ingenierias@cutonala.udg.mx',
  CINETECA: 'cineteca.difusion@cutonala.udg.mx',
};

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(() => localStorage.getItem('sigre_token'));
  const [loading, setLoading] = useState<boolean>(true);

  const refreshUser = async () => {
    try {
      const currentToken = localStorage.getItem('sigre_token');
      if (!currentToken) {
        setUser(null);
        setLoading(false);
        return;
      }
      const res = await api.auth.me();
      setUser(res.user);
    } catch (err) {
      console.error('Error al recuperar sesión:', err);
      localStorage.removeItem('sigre_token');
      setUser(null);
      setToken(null);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    refreshUser();
  }, []);

  const login = async (email: string, password = 'Cutonala2026!') => {
    setLoading(true);
    try {
      const recaptchaToken = await getRecaptchaToken('LOGIN');
      const res = await api.auth.login(email, password, recaptchaToken);
      localStorage.setItem('sigre_token', res.token);
      setToken(res.token);
      setUser(res.user);
    } finally {
      setLoading(false);
    }
  };

  const loginAs = async (rolePreset: keyof typeof PRESET_ACCOUNTS) => {
    const email = PRESET_ACCOUNTS[rolePreset];
    await login(email);
  };

  const logout = () => {
    localStorage.removeItem('sigre_token');
    setToken(null);
    setUser(null);
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        token,
        loading,
        login,
        loginAs,
        logout,
        refreshUser,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) throw new Error('useAuth must be used within an AuthProvider');
  return context;
};
