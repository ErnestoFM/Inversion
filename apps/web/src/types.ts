export interface User {
  id: string;
  email: string;
  nombre: string;
  codigo: string;
  rol: 'ESTUDIANTE' | 'DOCENTE' | 'ADMIN' | 'COORDINADOR' | 'TECNICO_LAB';
  carrera?: string | null;
  telefono?: string | null;
  reputationScore: number;
}

export interface Space {
  id: string;
  nombre: string;
  codigoEspacio: string;
  edificio: string;
  piso: string;
  capacidad: number;
  tipo: 'AULA' | 'AUDITORIO' | 'LABORATORIO' | 'CINETECA' | 'SALA_JUNTAS' | 'AREA_COMUN';
  activo: boolean;
  equipamiento: string[];
  fotos: string[];
  reglamento?: string;
  created_at: string;
}

export interface Resource {
  id: string;
  nombre: string;
  codigoInventario: string;
  categoria: 'COMPUTO' | 'AUDIOVISUAL' | 'LABORATORIO' | 'HERRAMIENTAS' | 'MOBILIARIO';
  marca?: string | null;
  modelo?: string | null;
  numeroSerie?: string | null;
  estado: 'DISPONIBLE' | 'PRESTADO' | 'EN_REPARACION' | 'BAJA' | 'RESERVADO';
  condicionFisica: 'EXCELENTE' | 'BUENO' | 'REGULAR' | 'DAÑADO';
  ubicacion: string;
  diasMaxPrestamo: number;
  requiereCapacitacion: boolean;
  horasUsoTotales: number;
}

export interface EventScreening {
  id: string;
  titulo: string;
  sinopsis: string;
  posterUrl?: string | null;
  trailerUrl?: string | null;
  clasificacion: string;
  duracionMin: number;
  director?: string | null;
  fechaHoraInicio: string;
  fechaHoraFin: string;
  cupoMaximo: number;
  asientosDisponibles: number;
  espacio: {
    id: string;
    nombre: string;
    edificio: string;
  };
}

export interface Booking {
  id: string;
  folio: string;
  fechaInicio: string;
  fechaFin: string;
  estado: 'PENDIENTE' | 'APROBADA' | 'RECHAZADA' | 'CANCELADA' | 'COMPLETADA';
  motivoUso: string;
  asistentesEstimados: number;
  espacio: Space;
  solicitante: User;
  created_at: string;
}

export interface Loan {
  id: string;
  folio: string;
  fechaInicio: string;
  fechaLimiteDevolucion: string;
  fechaDevolucionReal?: string | null;
  estado: 'ACTIVO' | 'DEVUELTO' | 'CON_INCIDENCIA' | 'VENCIDO';
  esPrestamoExtendido: boolean;
  recurso: Resource;
  solicitante: User;
  responsivaHash?: string;
  firmaDigitalBase64?: string;
  checklistSalida?: {
    condicion: string;
    accesoriosEntregados: string[];
    observaciones: string;
  };
  checklistEntrada?: {
    condicion: string;
    accesoriosDevueltos: string[];
    observaciones: string;
  };
}

export interface Incident {
  id: string;
  folio: string;
  tipo: 'DAÑO_EQUIPO' | 'EXTRAVIO' | 'RETRASO_GRAVE' | 'USO_INDEBIDO' | 'DESPERFECTO_ESPACIO';
  gravedad: 'LEVE' | 'MODERADO' | 'GRAVE';
  puntosSancion: number;
  descripcion: string;
  estado: 'REPORTADA' | 'EN_REVISION' | 'REPARACION_SUPERVISADA' | 'RESUELTA';
  recurso?: {
    id: string;
    nombre: string;
    codigoInventario: string;
  } | null;
  usuarioInfractor: User;
  created_at: string;
}

export interface NotificationItem {
  id: string;
  titulo: string;
  mensaje: string;
  tipo: 'RESERVA_APROBADA' | 'RESERVA_RECHAZADA' | 'RECORDATORIO_PRESTAMO' | 'INCIDENCIA' | 'GENERAL';
  leido: boolean;
  created_at: string;
}

export interface EvaluacionInversion {
  capexTotal: number;
  capexDesglose: Array<{
    concepto: string;
    monto: number;
    descripcion: string;
  }>;
  tmarPorcentaje: number;
  vpnMxn: number;
  tirPorcentaje: number;
  paybackMesesSimple: number;
  paybackMesesDescontado: number;
  puntoEquilibrioMeses: number;
  relacionBeneficioCosto: number;
  flujoTrienal: Array<{
    periodo: string;
    fase: string;
    planteles: string;
    ingresos: number;
    egresos: number;
    flujoNeto: number;
    flujoAcumulado: number;
  }>;
  impactoPatrimonial: {
    reduccionMermasPorcentaje: number;
    eliminacionEmpalmesPorcentaje: number;
    tiempoDespachoSegundos: number;
    tiempoDespachoAnteriorMinutos: number;
    ahorroEstimadoMermasMxn: number;
  };
}

export interface DashboardStats {
  resumen: {
    totalEspacios: number;
    totalRecursos: number;
    reservasActivas: number;
    prestamosActivos: number;
    incidentesPendientes: number;
    reservasPendientesAprobacion: number;
  };
  matrizDesgaste: Array<{
    id: string;
    nombre: string;
    codigo: string;
    categoria: string;
    condicion: string;
    horasUso: number;
    vecesPrestado: number;
    riesgoFalla: 'BAJO' | 'MEDIO' | 'ALTO';
  }>;
  ocupacionEspaciosHoy: Array<{
    id: string;
    nombre: string;
    edificio: string;
    capacidad: number;
    reservasHoy: number;
    ocupadoActualmente: boolean;
  }>;
  evaluacionInversion?: EvaluacionInversion;
}
