import type { User, UserRole } from '../types';

export const isStaffUser = (user: User | null | undefined): boolean => {
  if (!user) return false;
  const role = (user.rol || user.role || '') as UserRole;
  return [
    'SUPERADMIN',
    'ADMIN',
    'ALMACEN_ADMIN',
    'COORDINADOR',
    'TECNICO_LAB',
    'DIFUSION_EVENTOS',
  ].includes(role);
};

export const isAdminUser = (user: User | null | undefined): boolean => {
  if (!user) return false;
  const role = (user.rol || user.role || '') as UserRole;
  return role === 'SUPERADMIN' || role === 'ADMIN';
};

export const isAlmacenAdmin = (user: User | null | undefined): boolean => {
  if (!user) return false;
  const role = (user.rol || user.role || '') as UserRole;
  return role === 'ALMACEN_ADMIN' || role === 'TECNICO_LAB';
};

export const isDocente = (user: User | null | undefined): boolean => {
  if (!user) return false;
  const role = (user.rol || user.role || '') as UserRole;
  return role === 'DOCENTE';
};

export const isEstudiante = (user: User | null | undefined): boolean => {
  if (!user) return false;
  const role = (user.rol || user.role || '') as UserRole;
  return role === 'ESTUDIANTE';
};

export const canAccessDashboard = (user: User | null | undefined): boolean => {
  if (!user) return false;
  const role = (user.rol || user.role || '') as UserRole;
  return ['SUPERADMIN', 'ADMIN', 'ALMACEN_ADMIN', 'COORDINADOR'].includes(role);
};

export const getRoleLabel = (role: UserRole | string | undefined): string => {
  switch (role) {
    case 'SUPERADMIN':
      return 'Superadministrador / Coordinador General';
    case 'ADMIN':
      return 'Administrador SIGRE';
    case 'ALMACEN_ADMIN':
      return 'Administrador de Almacén & Préstamos';
    case 'DIFUSION_EVENTOS':
      return 'Coordinación de Cineteca & Difusión';
    case 'DOCENTE':
      return 'Docente / Académico';
    case 'ESTUDIANTE':
      return 'Estudiante UdeG';
    case 'TECNICO_LAB':
      return 'Técnico de Laboratorio';
    case 'COORDINADOR':
      return 'Coordinador de Carrera';
    default:
      return role || 'Usuario';
  }
};

export const getRoleBadgeClass = (role: UserRole | string | undefined): string => {
  switch (role) {
    case 'SUPERADMIN':
    case 'ADMIN':
      return 'badge-primary';
    case 'ALMACEN_ADMIN':
    case 'TECNICO_LAB':
      return 'badge-warning';
    case 'DIFUSION_EVENTOS':
      return 'badge-secondary';
    case 'DOCENTE':
      return 'badge-info';
    case 'ESTUDIANTE':
    default:
      return 'badge-accent';
  }
};

