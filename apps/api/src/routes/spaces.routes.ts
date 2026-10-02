import { Router, Request, Response } from 'express';
import { z } from 'zod';
import { prisma } from '@inversion/database';
import { authenticateJwt, requireRoles } from '../middlewares/auth.middleware.js';
import { SpaceType, UserRole } from '@inversion/shared-types';

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

// 1. Listar espacios con filtros opcionales
spacesRouter.get('/', async (req: Request, res: Response) => {
  try {
    const { type, building, capacityMin, hasProjector, hasAudio, isActive } = req.query;

    const where: any = {};

    if (type && Object.values(SpaceType).includes(type as SpaceType)) {
      where.type = type as SpaceType;
    }
    if (building) {
      where.building = { contains: String(building), mode: 'insensitive' };
    }
    if (capacityMin) {
      where.capacity = { gte: Number(capacityMin) };
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

    return res.json({ success: true, data: spaces });
  } catch (error: any) {
    return res.status(500).json({ success: false, error: error.message || 'Error al listar espacios' });
  }
});

// 2. Detalle de un espacio
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
          orderBy: { startTime: 'asc' },
          take: 5
        }
      }
    });

    if (!space) {
      return res.status(404).json({ success: false, error: 'Espacio no encontrado' });
    }

    return res.json({ success: true, data: space });
  } catch (error: any) {
    return res.status(500).json({ success: false, error: error.message || 'Error al consultar espacio' });
  }
});

// 3. Consulta de disponibilidad y franjas ocupadas para una fecha dada
spacesRouter.get('/:id/availability', async (req: Request, res: Response) => {
  try {
    const { id } = req.params;
    const { date } = req.query; // Formato YYYY-MM-DD

    if (!date || typeof date !== 'string') {
      return res.status(400).json({ success: false, error: 'Parámetro date (YYYY-MM-DD) requerido' });
    }

    const targetDate = new Date(date);
    if (isNaN(targetDate.getTime())) {
      return res.status(400).json({ success: false, error: 'Fecha inválida. Usa formato YYYY-MM-DD' });
    }

    const startOfDay = new Date(targetDate);
    startOfDay.setHours(0, 0, 0, 0);

    const endOfDay = new Date(targetDate);
    endOfDay.setHours(23, 59, 59, 999);

    // Buscar eventos y préstamos aprobados o en curso que ocupen el espacio en esa fecha
    const events = await prisma.event.findMany({
      where: {
        spaceId: id,
        status: { in: ['APROBADO', 'EN_CURSO', 'PRE_RESERVADO', 'PENDIENTE_APROBACION'] },
        OR: [
          { startTime: { gte: startOfDay, lte: endOfDay } },
          { endTime: { gte: startOfDay, lte: endOfDay } },
          { startTime: { lte: startOfDay }, endTime: { gte: endOfDay } }
        ]
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

    return res.json({
      success: true,
      data: {
        spaceId: id,
        date,
        occupiedSlots: events.map((e) => ({
          eventId: e.id,
          title: e.title,
          start: e.startTime,
          end: e.endTime,
          status: e.status
        }))
      }
    });
  } catch (error: any) {
    return res.status(500).json({ success: false, error: error.message || 'Error al consultar disponibilidad' });
  }
});

// 4. Crear nuevo espacio (Admin)
spacesRouter.post('/', authenticateJwt, requireRoles([UserRole.SUPERADMIN, UserRole.ALMACEN_ADMIN]), async (req: Request, res: Response) => {
  try {
    const data = createSpaceSchema.parse(req.body);

    const existing = await prisma.space.findUnique({ where: { code: data.code } });
    if (existing) {
      return res.status(400).json({ success: false, error: `Ya existe un espacio con el código ${data.code}` });
    }

    const space = await prisma.space.create({ data });
    return res.status(201).json({ success: true, data: space, message: 'Espacio registrado exitosamente' });
  } catch (error: any) {
    if (error instanceof z.ZodError) {
      return res.status(400).json({ success: false, error: error.errors });
    }
    return res.status(500).json({ success: false, error: error.message || 'Error al crear espacio' });
  }
});

// 5. Modificar espacio existente (Admin)
spacesRouter.put('/:id', authenticateJwt, requireRoles([UserRole.SUPERADMIN, UserRole.ALMACEN_ADMIN]), async (req: Request, res: Response) => {
  try {
    const { id } = req.params;
    const data = updateSpaceSchema.parse(req.body);

    const space = await prisma.space.update({
      where: { id },
      data
    });

    return res.json({ success: true, data: space, message: 'Espacio actualizado exitosamente' });
  } catch (error: any) {
    if (error instanceof z.ZodError) {
      return res.status(400).json({ success: false, error: error.errors });
    }
    return res.status(500).json({ success: false, error: error.message || 'Error al actualizar espacio' });
  }
});

// 6. Activar/Desactivar espacio (Admin)
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
      message: `Espacio ${isActive ? 'habilitado' : 'inhabilitado'} exitosamente`
    });
  } catch (error: any) {
    return res.status(500).json({ success: false, error: error.message || 'Error al cambiar estado del espacio' });
  }
});
