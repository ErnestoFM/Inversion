// ==============================================================================
// TIPOS GLOBALES Y CONTRATOS DEL SISTEMA SIGRE
// ==============================================================================

export enum UserRole {
  ESTUDIANTE = 'ESTUDIANTE',
  DOCENTE = 'DOCENTE',
  ALMACEN_ADMIN = 'ALMACEN_ADMIN',
  DIFUSION_EVENTOS = 'DIFUSION_EVENTOS',
  SUPERADMIN = 'SUPERADMIN'
}

export enum UserStatus {
  PENDIENTE_ACTIVACION = 'PENDIENTE_ACTIVACION',
  ACTIVO = 'ACTIVO',
  SANCIONADO = 'SANCIONADO',
  SUSPENDIDO = 'SUSPENDIDO'
}

export enum SpaceType {
  AULA = 'AULA',
  LABORATORIO = 'LABORATORIO',
  CINETECA = 'CINETECA',
  AUDITORIO = 'AUDITORIO',
  SALA_JUNTAS = 'SALA_JUNTAS',
  CANCHA = 'CANCHA'
}

export enum ItemCategory {
  COMPUTO = 'COMPUTO',
  PROYECCION = 'PROYECCION',
  AUDIO = 'AUDIO',
  CABLEADO_ADAPTADORES = 'CABLEADO_ADAPTADORES',
  MOBILIARIO = 'MOBILIARIO',
  HERRAMIENTAS = 'HERRAMIENTAS'
}

export enum ItemStatus {
  DISPONIBLE = 'DISPONIBLE',
  PRESTADO = 'PRESTADO',
  EN_MANTENIMIENTO = 'EN_MANTENIMIENTO',
  DANADO = 'DANADO',
  BAJA = 'BAJA'
}

export enum EventType {
  CINETECA = 'CINETECA',
  ACADEMICO = 'ACADEMICO',
  CULTURAL = 'CULTURAL',
  DEPORTIVO = 'DEPORTIVO',
  TALLER = 'TALLER',
  CONFERENCIA = 'CONFERENCIA'
}

export enum EventVisibility {
  PUBLICO = 'PUBLICO',
  PRIVADO_PERFIL = 'PRIVADO_PERFIL',
  PRIVADO_CODIGO = 'PRIVADO_CODIGO'
}

export enum RequestStatus {
  PRE_RESERVADO = 'PRE_RESERVADO',
  PENDIENTE_APROBACION = 'PENDIENTE_APROBACION',
  APROBADO = 'APROBADO',
  REBOTADO_CON_MOTIVO = 'REBOTADO_CON_MOTIVO',
  EN_CURSO = 'EN_CURSO',
  FINALIZADO = 'FINALIZADO',
  CANCELADO = 'CANCELADO'
}

export enum AttendeeStatus {
  REGISTRADO = 'REGISTRADO',
  EN_LISTA_ESPERA = 'EN_LISTA_ESPERA',
  ASISTIO = 'ASISTIO',
  NO_SHOW = 'NO_SHOW',
  CANCELADO = 'CANCELADO'
}

export enum IncidentSeverity {
  LEVE = 'LEVE',           // Retraso de minutos, desgaste normal
  MODERADA = 'MODERADA',   // Faltante de accesorio menor, cable dañado
  GRAVE = 'GRAVE'          // Daño físico a equipo/aula, pérdida o robo
}

export enum IncidentStatus {
  ABIERTO = 'ABIERTO',
  EN_REPARACION_SUPERVISADA = 'EN_REPARACION_SUPERVISADA',
  RESUELTO = 'RESUELTO',
  SANCION_DEFINITIVA = 'SANCION_DEFINITIVA'
}

// --- Entidades e Interfaces de Datos ---

export interface UserProfileDTO {
  id: string;
  email: string;
  fullName: string;
  studentCode: string;
  career?: string;
  semester?: number;
  role: UserRole;
  status: UserStatus;
  reputationScore: number;
  activeLoansCount: number;
  totalIncidentsCount: number;
  createdAt: string;
}

export interface SpaceDTO {
  id: string;
  name: string;
  code: string;
  type: SpaceType;
  building: string;
  capacity: number;
  hasProjector: boolean;
  hasAudio: boolean;
  rulesText?: string;
  isActive: boolean;
}

export interface InventoryItemDTO {
  id: string;
  serialNumber: string;
  assetTag: string;
  name: string;
  category: ItemCategory;
  brand?: string;
  model?: string;
  status: ItemStatus;
  currentHoursUsed: number;
  estimatedLifespanHours: number;
  rulesText?: string;
}

export interface EventDTO {
  id: string;
  title: string;
  description: string;
  type: EventType;
  visibility: EventVisibility;
  targetCareer?: string;
  targetSemesters?: number[];
  accessCode?: string;
  posterUrl?: string;
  trailerUrl?: string;
  spaceId?: string;
  spaceName?: string;
  startTime: string;
  endTime: string;
  maxCapacity: number;
  registeredCount: number;
  availableCapacity: number;
  status: RequestStatus;
  creatorId: string;
  creatorName: string;
  averageRating?: number;
  totalReviewsCount: number;
}

export interface EventAttendeeTicketDTO {
  ticketId: string;
  eventId: string;
  eventTitle: string;
  spaceName?: string;
  startTime: string;
  endTime: string;
  userId: string;
  userName: string;
  studentCode: string;
  status: AttendeeStatus;
  qrPayload: string; // Token firmado
  scannedAt?: string;
}

export interface LoanRequestDTO {
  id: string;
  folioNumber: string;
  userId: string;
  userName: string;
  userStudentCode: string;
  userReputation: number;
  spaceId?: string;
  spaceName?: string;
  items: {
    itemId: string;
    itemName: string;
    serialNumber: string;
    category: ItemCategory;
  }[];
  coResponsibles: {
    userId: string;
    userName: string;
    studentCode: string;
    hasSigned: boolean;
    signedAt?: string;
  }[];
  purpose: string;
  startTime: string;
  endTime: string;
  status: RequestStatus;
  rejectionReason?: string;
  responsivaPdfUrl?: string;
  isChecklistDeliveryCompleted: boolean;
  isChecklistReturnCompleted: boolean;
  createdAt: string;
}

export interface ReviewDTO {
  id: string;
  eventId: string;
  userId: string;
  userName: string;
  rating: number; // 1 a 5
  comment: string;
  createdAt: string;
}

// --- Métricas del Dashboard de Inversión ---

export interface InvestmentDashboardDTO {
  spaceUtilizationRate: number;        // Porcentaje global de ocupación
  inventoryReturnRate: number;         // Tasa de retornos sin daños (ej. 99.2%)
  eventAttendanceRate: number;         // Asistencia real vs proyectada
  communitySatisfactionScore: number;  // Calificación media (1-5)
  totalActiveSpaces: number;
  totalInventoryItems: number;
  totalEventsOrganized: number;
  estimatedReplacementSavingsMxn: number; // Ahorro estimado por responsivas
  subutilizedSpaces: {
    spaceName: string;
    utilizationPercentage: number;
  }[];
  inventoryWearMatrix: {
    category: ItemCategory;
    averageWearPercentage: number;
    itemsNeedingMaintenance: number;
  }[];
}
