import type {
  User,
  Space,
  Resource,
  EventScreening,
  Booking,
  Loan,
  Incident,
  NotificationItem,
  DashboardStats,
} from '../types';

const API_BASE = import.meta.env.VITE_API_BASE || '/api';

function getAuthHeaders(): HeadersInit {
  const token = localStorage.getItem('sigre_token');
  return {
    'Content-Type': 'application/json',
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
  };
}

async function request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
  const res = await fetch(`${API_BASE}${endpoint}`, {
    ...options,
    headers: {
      ...getAuthHeaders(),
      ...options.headers,
    },
  });

  const data = await res.json();
  if (!res.ok) {
    throw new Error(data.error || data.mensaje || `Error en la solicitud: ${res.status}`);
  }
  return data;
}

export const api = {
  // Auth
  auth: {
    login: (email: string, password?: string, recaptchaToken?: string) =>
      request<{ token: string; user: User }>('/auth/login', {
        method: 'POST',
        body: JSON.stringify({ email, password: password || 'Cutonala2026!', recaptchaToken }),
      }),
    me: () => request<{ user: User }>('/auth/me'),
  },

  // Espacios & Bloqueo Concurrente en Redis
  spaces: {
    list: (params?: { tipo?: string; capacidadMinima?: number }) => {
      const q = new URLSearchParams();
      if (params?.tipo) q.set('tipo', params.tipo);
      if (params?.capacidadMinima) q.set('capacidadMinima', params.capacidadMinima.toString());
      return request<{ espacios: Space[] }>(`/spaces?${q.toString()}`);
    },
    getAvailability: (id: string, fecha: string) =>
      request<{ espacioId: string; fecha: string; horarioDisponible: boolean; reservas: any[] }>(
        `/spaces/${id}/availability?fecha=${fecha}`
      ),
    acquireLock: (espacioId: string, fechaInicio: string, fechaFin: string) =>
      request<{ lockAdquirido: boolean; lockKey: string; expiraEnSegundos: number; mensaje: string }>(
        `/spaces/${espacioId}/lock`,
        {
          method: 'POST',
          body: JSON.stringify({ fechaInicio, fechaFin }),
        }
      ),
    releaseLock: (espacioId: string, fechaInicio: string, fechaFin: string) =>
      request<{ liberado: boolean }>(`/spaces/${espacioId}/lock`, {
        method: 'DELETE',
        body: JSON.stringify({ fechaInicio, fechaFin }),
      }),
    book: (data: {
      espacioId: string;
      fechaInicio: string;
      fechaFin: string;
      motivoUso: string;
      asistentesEstimados: number;
    }) =>
      request<{ reserva: Booking; mensaje: string }>('/spaces/book', {
        method: 'POST',
        body: JSON.stringify(data),
      }),
    myBookings: () => request<{ reservas: Booking[] }>('/spaces/my-bookings'),
  },

  // Recursos e Inventario
  resources: {
    list: (params?: { categoria?: string; estado?: string; search?: string }) => {
      const q = new URLSearchParams();
      if (params?.categoria) q.set('categoria', params.categoria);
      if (params?.estado) q.set('estado', params.estado);
      if (params?.search) q.set('search', params.search);
      return request<{ recursos: Resource[] }>(`/resources?${q.toString()}`);
    },
    requestLoan: (data: {
      recursoId: string;
      fechaInicio: string;
      fechaLimiteDevolucion: string;
      esPrestamoExtendido?: boolean;
      justificacionExtendida?: string;
      coResponsableCodigo?: string;
      firmaDigitalBase64?: string;
    }) =>
      request<{ prestamo: Loan; mensaje: string }>('/loans/request', {
        method: 'POST',
        body: JSON.stringify(data),
      }),
  },

  // Cartelera Cineteca & Boletos QR
  events: {
    listScreenings: () => request<{ funciones: EventScreening[] }>('/events/screenings'),
    getScreening: (id: string) => request<{ funcion: EventScreening }>(`/events/screenings/${id}`),
    bookTicket: (funcionId: string) =>
      request<{ boleto: any; qrCodeDataUrl: string; mensaje: string }>(`/events/screenings/${funcionId}/ticket`, {
        method: 'POST',
      }),
    myTickets: () => request<{ boletos: any[] }>('/events/my-tickets'),
    postReview: (eventId: string, data: { rating: number; comment: string }) =>
      request<{ success: boolean; data: any; message: string }>(`/events/${eventId}/reviews`, {
        method: 'POST',
        body: JSON.stringify(data),
      }),
    getReviews: (eventId: string) =>
      request<{ success: boolean; data: any[] }>(`/events/${eventId}/reviews`),
    scanTicket: (qrToken: string) =>
      request<{
        success: boolean;
        message: string;
        student?: { fullName: string; studentCode: string; career?: string };
        event?: { title: string; startTime: string };
        scannedAt?: string;
      }>('/events/scan-ticket', {
        method: 'POST',
        body: JSON.stringify({ qrToken }),
      }),
  },

  // Préstamos, Responsivas & Checklist
  loans: {
    list: () => request<{ prestamos: Loan[] }>('/loans'),
    myLoans: () => request<{ prestamos: Loan[] }>('/loans/my-loans'),
    verifyChecklist: (
      loanId: string,
      tipo: 'salida' | 'entrada',
      checklist: { condicion: string; accesorios: string[]; observaciones: string }
    ) =>
      request<{ prestamo: Loan; mensaje: string }>(`/loans/${loanId}/checklist`, {
        method: 'POST',
        body: JSON.stringify({ tipo, checklist }),
      }),
    downloadResponsivaPdf: (loanId: string) => `${API_BASE}/loans/${loanId}/responsiva-pdf`,
    sendCoResponsibleInvite: (loanId: string, email?: string) =>
      request<{ success: boolean; message: string }>(`/loans/${loanId}/send-co-responsible-invite`, {
        method: 'POST',
        body: JSON.stringify({ email }),
      }),
    signCoResponsible: (loanId: string, signatureBase64: string, token?: string) =>
      request<{ success: boolean; message: string }>(`/loans/${loanId}/sign-co-responsible`, {
        method: 'POST',
        body: JSON.stringify({ signatureBase64, token }),
      }),
  },

  // Incidentes & Sanciones
  incidents: {
    list: () => request<{ incidentes: Incident[] }>('/incidents'),
    report: (data: {
      recursoId?: string;
      espacioId?: string;
      tipo: string;
      gravedad: string;
      descripcion: string;
      fotosEvidencia?: string[];
    }) =>
      request<{ incidente: Incident; penalizacionAplicada: number; nuevoScore: number }>(
        '/incidents',
        {
          method: 'POST',
          body: JSON.stringify(data),
        }
      ),
    registerCommitment: (
      id: string,
      data: {
        tipo: string;
        montoEstimadoMxn?: number;
        horasServicio?: number;
        fechaLimite?: string;
        notasSupervision: string;
      }
    ) =>
      request<{ success: boolean; data: Incident; message: string }>(`/incidents/${id}/commitment`, {
        method: 'PATCH',
        body: JSON.stringify(data),
      }),
    resolve: (id: string, solucion: string, restaurarPuntos?: boolean) =>
      request<{ incidente: Incident; scoreRestaurado?: boolean }>(`/incidents/${id}/resolve`, {
        method: 'POST',
        body: JSON.stringify({ solucion, restaurarPuntos }),
      }),
  },

  // Notificaciones
  notifications: {
    list: () => request<{ notificaciones: NotificationItem[]; totalNoLeidas: number }>('/notifications'),
    markAsRead: (id: string) => request<{ ok: boolean }>(`/notifications/${id}/read`, { method: 'PATCH' }),
  },

  // Dashboard Ejecutivo
  dashboard: {
    getStats: () => request<DashboardStats>('/dashboard/stats'),
  },
};
