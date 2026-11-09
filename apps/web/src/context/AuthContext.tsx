import React, { createContext, useContext, useEffect, useState } from 'react';
import type { User } from '../types';
import { api } from '../api/client';
import { getRecaptchaToken } from '../utils/recaptcha';

interface AuthContextType {
  user: User | null;
  token: string | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  refreshUser: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(() => {
    const stored = localStorage.getItem('sigre_token');
    return stored && stored !== 'undefined' && stored !== 'null' ? stored : null;
  });
  const [loading, setLoading] = useState<boolean>(true);

  const refreshUser = async () => {
    try {
      const currentToken = localStorage.getItem('sigre_token');
      if (!currentToken || currentToken === 'undefined' || currentToken === 'null' || !currentToken.trim()) {
        localStorage.removeItem('sigre_token');
        setUser(null);
        setToken(null);
        setLoading(false);
        return;
      }
      const res = await api.auth.me();
      setUser(res.user || (res as any).data);
    } catch (err) {
      console.warn('Sesión no encontrada o expirada:', err);
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

  const login = async (email: string, password: string) => {
    setLoading(true);
    try {
      const recaptchaToken = await getRecaptchaToken('LOGIN');
      const res: any = await api.auth.login(email.trim(), password, recaptchaToken);
      const tokenValue = res.token || res.accessToken;
      if (tokenValue) {
        localStorage.setItem('sigre_token', tokenValue);
        setToken(tokenValue);
      }
      setUser(res.user || res.data);
    } finally {
      setLoading(false);
    }
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
