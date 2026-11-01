import { Router, Request, Response } from 'express';
import { z } from 'zod';
import { prisma } from '@inversion/database';
import { authenticateJwt, requireRoles } from '../middlewares/auth.middleware.js';
import { RedisLockService } from '../services/redis-lock.service.js';
import { SpaceType, UserRole, RequestStatus, EventType, EventVisibility } from '@inversion/shared-types';

export const spacesRouter = Router();

const createSpaceSchema = z.object({
  name: z.string().min(3),
  code: z.string().min(3),
  type: z.nativeEnum(SpaceType),
  building: z.string().min(2),
  capacity: z.number().int().positive(),
  hasProjector: z.boolean().default(false),
  hasAudio: z.boolean().default(false),
  rulesText: z.string().optional()
});

const updateSpaceSchema = createSpaceSchema.partial();

const bookSpaceSchema = z.object({
  espacioId: z.string().uuid().optional(),
  spaceId: z.string().uuid().optional(),
  fechaInicio: z.string().datetime().optional(),
  startTime: z.string().datetime().optional(),
  fechaFin: z.string().datetime().optional(),
  endTime: z.string().datetime().optional(),
  motivoUso: z.string().min(5).optional(),
  purpose: z.string().min(5).optional(),
  asistentesEstimados: z.number().int().positive().optional(),
  estimatedAttendees: z.number().int().positive().optional()
});

// 1. Listar espacios con filtros opcionales (Soporta contrato data y espacios)
spacesRouter.get('/', async (req: Request, res: Response) => {
  try {
    const { type, tipo, building, capacityMin, capacidadMinima, hasProjector, hasAudio, isActive } = req.query;

    const where: any = {};
    const targetType = (type || tipo) as string;

    if (targetType && Object.values(SpaceType).includes(targetType as SpaceType)) {
      where.type = targetType as SpaceType;
    }
    if (building) {
      where.building = { contains: String(building), mode: 'insensitive' };
    }
    const minCap = Number(capacityMin || capacidadMinima);
    if (!isNaN(minCap) && minCap > 0) {
      where.capacity = { gte: minCap };
    }
    if (hasProjector !== undefined) {
      where.hasProjector = hasProjector === 'true';
    }
    if (hasAudio !== undefined) {
      where.hasAudio = hasAudio === 'true';
    }
    if (isActive !== undefined) {
      where.isActive = isActive === 'true';
    } else {
      where.isActive = true; // Por defecto solo activos
    }

    const spaces = await prisma.space.findMany({
      where,
      orderBy: { name: 'asc' }
    });

    const defaultImages: Record<string, string> = {
      AUDITORIO: 'https://images.unsplash.com/photo-1541829070764-84a7d30dd3f3?auto=format&fit=crop&w=800&q=80',
      AULA: 'https://images.unsplash.com/photo-1509062522246-3755977927d7?auto=format&fit=crop&w=800&q=80',
      CINETECA: 'https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?auto=format&fit=crop&w=800&q=80',
      LABORATORIO: 'https://images.unsplash.com/photo-1581092160607-ee22621dd758?auto=format&fit=crop&w=800&q=80',
      SALA_JUNTAS: 'https://images.unsplash.com/photo-1497366216548-37526070297c?auto=format&fit=crop&w=800&q=80',
      CANCHA: 'https://images.unsplash.com/photo-1534438327276-14e5300c3a48?auto=format&fit=crop&w=800&q=80'
    };

    const formattedSpaces = spaces.map((s) => {
      const equip: string[] = [];
      if (s.hasProjector) equip.push('Proyector Láser 4K');
      if (s.hasAudio) equip.push('Sistema de Audio Shure');
      if (s.type === SpaceType.CINETECA) equip.push('Sonido Envolvente Dolby');
      if (s.type === SpaceType.LABORATORIO) equip.push('40 Workstations i7');

      const fallbackImg = defaultImages[s.type] || defaultImages.AULA;

      return {
        ...s,
        // Campos en español y anidados para compatibilidad total con la UI
        nombre: s.name,
        codigoEspacio: s.code,
        edificio: s.building,
        piso: s.building.includes('Planta Alta') || s.building.includes('Primer Nivel') ? '1' : (s.building.includes('Nivel 2') ? '2' : 'PB'),
        capacidad: s.capacity,
        tipo: s.type,
        activo: s.isActive,
        equipamiento: equip,
        fotos: [fallbackImg],
        reglamento: s.rulesText || 'Normativa institucional de CUTonalá UdeG.'
      };
    });

    return res.json({
      success: true,
      data: formattedSpaces,
      espacios: formattedSpaces
    });
  } catch (error: any) {
    return res.status(500).json({ success: false, error: error.message || 'Error al listar espacios' });
  }
});

// 2. Mis Reservas de Espacios (RF-02)
spacesRouter.get('/my-bookings', authenticateJwt, async (req: Request, res: Response) => {
  try {
    const userId = req.user!.userId;

    const bookings = await prisma.event.findMany({
      where: {
        creatorId: userId,
        spaceId: { not: null }
      },
      include: {
        space: { select: { id: true, name: true, building: true, capacity: true } }
      },
      orderBy: { startTime: 'desc' }
    });

    const formatted = bookings.map((b) => ({
      id: b.id,
      folio: `RES-${b.id.substring(0, 8).toUpperCase()}`,
      spaceId: b.spaceId,
      espacio: b.space ? {
        id: b.space.id,
        nombre: b.space.name,
        edificio: b.space.building,
        capacidad: b.space.capacity
      } : undefined,
      startTime: b.startTime.toISOString(),
      endTime: b.endTime.toISOString(),
      status: b.status,
      estado: b.status,
      purpose: b.description,
      motivoUso: b.description,
      estimatedAttendees: b.maxCapacity,
      asistentesEstimados: b.maxCapacity,
      created_at: b.createdAt.toISOString()
    }));

    return res.json({
      success: true,
      data: formatted,
      reservas: formatted
    });
  } catch (error: any) {
    return res.status(500).json({ success: false, error: error.message || 'Error al obtener mis reservas' });
  }
});

// 3. Crear reserva directa de espacio (RF-02.1)
spacesRouter.post('/book', authenticateJwt, async (req: Request, res: Response) => {
  try {
    const parsed = bookSpaceSchema.parse(req.body);
    const spaceId = parsed.espacioId || parsed.spaceId;
    const startTimeStr = parsed.fechaInicio || parsed.startTime;
    const endTimeStr = parsed.fechaFin || parsed.endTime;
    const purpose = parsed.motivoUso || parsed.purpose || 'Uso académico de espacio';
    const attendees = parsed.asistentesEstimados || parsed.estimatedAttendees || 20;

    if (!spaceId || !startTimeStr || !endTimeStr) {
      return res.status(400).json({
        success: false,
        error: 'espacioId, fechaInicio y fechaFin son obligatorios'
      });
    }

    const start = new Date(startTimeStr);
    const end = new Date(endTimeStr);

    if (start >= end) {
      return res.status(400).json({ success: false, error: 'La fecha de fin debe ser posterior a la fecha de inicio' });
    }

    // Verificar si el espacio existe y está activo
    const space = await prisma.space.findUnique({ where: { id: spaceId } });
    if (!space || !space.isActive) {
      return res.status(404).json({ success: false, error: 'El espacio solicitado no existe o no se encuentra activo' });
    }

    // Verificar empalme de horarios en base de datos
    const overlap = await prisma.event.findFirst({
      where: {
        spaceId,
        status: { in: [RequestStatus.APROBADO, RequestStatus.PRE_RESERVADO, RequestStatus.EN_CURSO] },
        OR: [
          { startTime: { lt: end }, endTime: { gt: start } }
        ]
      }
    });

    if (overlap) {
      return res.status(409).json({
        success: false,
        error: 'El espacio ya cuenta con una reserva confirmada o en curso en el horario seleccionado'
      });
    }

    // Crear el evento de reserva
    const booking = await prisma.event.create({
      data: {
        title: `Reserva: ${space.name} - ${purpose.substring(0, 30)}`,
        description: purpose,
        type: EventType.ACADEMICO,
        visibility: EventVisibility.PUBLICO,
        spaceId,
        creatorId: req.user!.userId,
        startTime: start,
        endTime: end,
        maxCapacity: Math.min(attendees, space.capacity),
        status: RequestStatus.APROBADO
      },
      include: {
        space: true
      }
    });

    // Liberar el bloqueo temporal en Redis si existía
    await RedisLockService.releaseLock('space', spaceId, start, end, req.user!.userId);

    const formattedReserva = {
      id: booking.id,
      folio: `RES-${booking.id.substring(0, 8).toUpperCase()}`,
      spaceId: booking.spaceId,
      espacio: {
        id: space.id,
        nombre: space.name,
        edificio: space.building,
        capacidad: space.capacity
      },
      startTime: booking.startTime.toISOString(),
      endTime: booking.endTime.toISOString(),
      status: booking.status,
      estado: booking.status,
      purpose: booking.description,
      motivoUso: booking.description,
      asistentesEstimados: booking.maxCapacity
    };

    return res.status(201).json({
      success: true,
      data: formattedReserva,
      reserva: formattedReserva,
      folio: formattedReserva.folio,
      mensaje: 'Reserva confirmada exitosamente'
    });
  } catch (error: any) {
    if (error instanceof z.ZodError) {
      return res.status(400).json({ success: false, error: error.errors });
    }
    return res.status(500).json({ success: false, error: error.message || 'Error al crear reserva de espacio' });
  }
});

// 4. Adquirir Soft Lock concurrente en Redis (RT-02.1)
spacesRouter.post('/:id/lock', authenticateJwt, async (req: Request, res: Response) => {
  try {
    const { id } = req.params;
    const { fechaInicio, startTime, fechaFin, endTime } = req.body;
    const startStr = fechaInicio || startTime;
    const endStr = fechaFin || endTime;

    if (!startStr || !endStr) {
      return res.status(400).json({ success: false, error: 'fechaInicio y fechaFin requeridos para adquirir el bloqueo' });
    }

    const lockResult = await RedisLockService.acquireLock(
      'space',
      id,
      new Date(startStr),
      new Date(endStr),
      req.user!.userId,
      900 // 15 minutos de TTL
    );

    return res.json({
      success: lockResult.acquired,
      lockAdquirido: lockResult.acquired,
      lockKey: `sigre:lock:space:${id}`,
      expiraEnSegundos: lockResult.remainingTtl || 900,
      mensaje: lockResult.acquired
        ? 'Bloqueo temporal en Redis adquirido con éxito (15 min)'
        : 'El espacio se encuentra en proceso de reserva por otro usuario. Intenta con otro horario o espacio.'
    });
  } catch (error: any) {
    return res.status(500).json({ success: false, error: error.message || 'Error al adquirir bloqueo en Redis' });
  }
});

// 5. Liberar Soft Lock en Redis (RT-02.1)
spacesRouter.delete('/:id/lock', authenticateJwt, async (req: Request, res: Response) => {
  try {
    const { id } = req.params;
    const { fechaInicio, startTime, fechaFin, endTime } = req.body;
    const startStr = fechaInicio || startTime;
    const endStr = fechaFin || endTime;

    if (startStr && endStr) {
      await RedisLockService.releaseLock('space', id, new Date(startStr), new Date(endStr), req.user!.userId);
    }

    return res.json({
      success: true,
      liberado: true,
      mensaje: 'Bloqueo temporal liberado'
    });
  } catch (error: any) {
    return res.status(500).json({ success: false, error: error.message || 'Error al liberar bloqueo' });
  }
});

// 6. Consultar Disponibilidad de un espacio por fecha
spacesRouter.get('/:id/availability', async (req: Request, res: Response) => {
  try {
    const { id } = req.params;
    const { date, fecha } = req.query;
    const targetDate = String(fecha || date || new Date().toISOString().split('T')[0]);

    const startOfDay = new Date(`${targetDate}T00:00:00.000Z`);
    const endOfDay = new Date(`${targetDate}T23:59:59.999Z`);

    const events = await prisma.event.findMany({
      where: {
        spaceId: id,
        status: { in: [RequestStatus.APROBADO, RequestStatus.PRE_RESERVADO, RequestStatus.EN_CURSO] },
        startTime: { lte: endOfDay },
        endTime: { gte: startOfDay }
      },
      select: {
        id: true,
        title: true,
        startTime: true,
        endTime: true,
        status: true
      },
      orderBy: { startTime: 'asc' }
    });

    const isAvailable = events.length === 0;

    return res.json({
      success: true,
      data: {
        spaceId: id,
        date: targetDate,
        occupiedSlots: events
      },
      espacioId: id,
      fecha: targetDate,
      horarioDisponible: isAvailable,
      reservas: events
    });
  } catch (error: any) {
    return res.status(500).json({ success: false, error: error.message || 'Error al consultar disponibilidad' });
  }
});

// 7. Detalle de un espacio
spacesRouter.get('/:id', async (req: Request, res: Response) => {
  try {
    const { id } = req.params;

    const space = await prisma.space.findUnique({
      where: { id },
      include: {
        events: {
          where: {
            endTime: { gte: new Date() },
            status: { in: ['APROBADO', 'EN_CURSO'] }
          },
          select: {
            id: true,
            title: true,
            startTime: true,
            endTime: true,
            type: true
          },
          take: 5
        }
      }
    });

    if (!space) {
      return res.status(404).json({ success: false, error: 'Espacio no encontrado' });
    }

    return res.json({ success: true, data: space, espacio: space });
  } catch (error: any) {
    return res.status(500).json({ success: false, error: error.message || 'Error al obtener detalle del espacio' });
  }
});

// 8. Crear nuevo espacio (Admin)
spacesRouter.post('/', authenticateJwt, requireRoles([UserRole.SUPERADMIN, UserRole.ALMACEN_ADMIN]), async (req: Request, res: Response) => {
  try {
    const data = createSpaceSchema.parse(req.body);

    const existing = await prisma.space.findUnique({ where: { code: data.code } });
    if (existing) {
      return res.status(400).json({ success: false, error: `Ya existe un espacio con el código ${data.code}` });
    }

    const space = await prisma.space.create({ data });
    return res.status(201).json({ success: true, data: space, espacio: space, message: 'Espacio registrado exitosamente' });
  } catch (error: any) {
    if (error instanceof z.ZodError) {
      return res.status(400).json({ success: false, error: error.errors });
    }
    return res.status(500).json({ success: false, error: error.message || 'Error al crear espacio' });
  }
});

// 9. Modificar espacio existente (Admin)
spacesRouter.put('/:id', authenticateJwt, requireRoles([UserRole.SUPERADMIN, UserRole.ALMACEN_ADMIN]), async (req: Request, res: Response) => {
  try {
    const { id } = req.params;
    const data = updateSpaceSchema.parse(req.body);

    const space = await prisma.space.update({
      where: { id },
      data
    });

    return res.json({ success: true, data: space, espacio: space, message: 'Espacio actualizado exitosamente' });
  } catch (error: any) {
    if (error instanceof z.ZodError) {
      return res.status(400).json({ success: false, error: error.errors });
    }
    return res.status(500).json({ success: false, error: error.message || 'Error al actualizar espacio' });
  }
});

// 10. Activar/Desactivar espacio (Admin)
spacesRouter.patch('/:id/status', authenticateJwt, requireRoles([UserRole.SUPERADMIN, UserRole.ALMACEN_ADMIN]), async (req: Request, res: Response) => {
  try {
    const { id } = req.params;
    const { isActive } = req.body;

    if (typeof isActive !== 'boolean') {
      return res.status(400).json({ success: false, error: 'El campo isActive debe ser booleano' });
    }

    const space = await prisma.space.update({
      where: { id },
      data: { isActive }
    });

    return res.json({
      success: true,
      data: space,
      espacio: space,
      message: `Espacio ${isActive ? 'habilitado' : 'inhabilitado'} exitosamente`
    });
  } catch (error: any) {
    return res.status(500).json({ success: false, error: error.message || 'Error al cambiar estado del espacio' });
  }
});
