import { Router, Request, Response } from 'express';
import { z } from 'zod';
import { prisma } from '@inversion/database';
import { authenticateJwt, requireRoles } from '../middlewares/auth.middleware.js';
import { ItemCategory, ItemStatus, UserRole } from '@inversion/shared-types';

export const resourcesRouter = Router();

const createItemSchema = z.object({
  serialNumber: z.string().min(3),
  assetTag: z.string().min(3),
  name: z.string().min(3),
  category: z.nativeEnum(ItemCategory),
  brand: z.string().optional(),
  model: z.string().optional(),
  status: z.nativeEnum(ItemStatus).default(ItemStatus.DISPONIBLE),
  estimatedLifespanHours: z.number().int().positive().default(3000),
  rulesText: z.string().optional()
});

const updateItemSchema = createItemSchema.partial();

// 1. Listar inventario de recursos con filtros
resourcesRouter.get('/', async (req: Request, res: Response) => {
  try {
    const { category, status, search } = req.query;

    const where: any = {};

    if (category && Object.values(ItemCategory).includes(category as ItemCategory)) {
      where.category = category as ItemCategory;
    }
    if (status && Object.values(ItemStatus).includes(status as ItemStatus)) {
      where.status = status as ItemStatus;
    }

    if (search && typeof search === 'string') {
      where.OR = [
        { name: { contains: search, mode: 'insensitive' } },
        { brand: { contains: search, mode: 'insensitive' } },
        { model: { contains: search, mode: 'insensitive' } },
        { assetTag: { contains: search, mode: 'insensitive' } },
        { serialNumber: { contains: search, mode: 'insensitive' } }
      ];
    }

    const items = await prisma.inventoryItem.findMany({
      where,
      orderBy: { name: 'asc' }
    });

    return res.json({ success: true, data: items });
  } catch (error: any) {
    return res.status(500).json({ success: false, error: error.message || 'Error al listar recursos' });
  }
});

// 2. Detalle de un recurso
resourcesRouter.get('/:id', async (req: Request, res: Response) => {
  try {
    const { id } = req.params;

    const item = await prisma.inventoryItem.findUnique({
      where: { id },
      include: {
        loans: {
          take: 5,
          orderBy: { loanRequest: { createdAt: 'desc' } },
          include: {
            loanRequest: {
              select: {
                folioNumber: true,
                status: true,
                startTime: true,
                endTime: true,
                user: { select: { fullName: true, studentCode: true } }
              }
            }
          }
        },
        incidents: {
          take: 3,
          orderBy: { createdAt: 'desc' }
        }
      }
    });

    if (!item) {
      return res.status(404).json({ success: false, error: 'Recurso no encontrado' });
    }

    return res.json({ success: true, data: item });
  } catch (error: any) {
    return res.status(500).json({ success: false, error: error.message || 'Error al consultar recurso' });
  }
});

// 3. Alta de recurso (Almacén o Admin)
resourcesRouter.post('/', authenticateJwt, requireRoles([UserRole.SUPERADMIN, UserRole.ALMACEN_ADMIN]), async (req: Request, res: Response) => {
  try {
    const data = createItemSchema.parse(req.body);

    const existingTag = await prisma.inventoryItem.findUnique({ where: { assetTag: data.assetTag } });
    if (existingTag) {
      return res.status(400).json({ success: false, error: `La etiqueta patrimonial ${data.assetTag} ya está registrada` });
    }

    const existingSerial = await prisma.inventoryItem.findUnique({ where: { serialNumber: data.serialNumber } });
    if (existingSerial) {
      return res.status(400).json({ success: false, error: `El número de serie ${data.serialNumber} ya está registrado` });
    }

    const item = await prisma.inventoryItem.create({ data });
    return res.status(201).json({ success: true, data: item, message: 'Recurso registrado exitosamente en inventario' });
  } catch (error: any) {
    if (error instanceof z.ZodError) {
      return res.status(400).json({ success: false, error: error.errors });
    }
    return res.status(500).json({ success: false, error: error.message || 'Error al registrar recurso' });
  }
});

// 4. Edición de recurso (Almacén o Admin)
resourcesRouter.put('/:id', authenticateJwt, requireRoles([UserRole.SUPERADMIN, UserRole.ALMACEN_ADMIN]), async (req: Request, res: Response) => {
  try {
    const { id } = req.params;
    const data = updateItemSchema.parse(req.body);

    const item = await prisma.inventoryItem.update({
      where: { id },
      data
    });

    return res.json({ success: true, data: item, message: 'Recurso actualizado exitosamente' });
  } catch (error: any) {
    if (error instanceof z.ZodError) {
      return res.status(400).json({ success: false, error: error.errors });
    }
    return res.status(500).json({ success: false, error: error.message || 'Error al actualizar recurso' });
  }
});

// 5. Cambio de estado de un recurso (Mantenimiento, Dañado, Disponible, Baja)
resourcesRouter.patch('/:id/status', authenticateJwt, requireRoles([UserRole.SUPERADMIN, UserRole.ALMACEN_ADMIN]), async (req: Request, res: Response) => {
  try {
    const { id } = req.params;
    const { status } = req.body;

    if (!status || !Object.values(ItemStatus).includes(status)) {
      return res.status(400).json({ success: false, error: 'Estado de recurso inválido' });
    }

    const item = await prisma.inventoryItem.update({
      where: { id },
      data: { status }
    });

    return res.json({ success: true, data: item, message: `Estado actualizado a ${status}` });
  } catch (error: any) {
    return res.status(500).json({ success: false, error: error.message || 'Error al actualizar estado del recurso' });
  }
});

// 6. Eliminar recurso (Solo SuperAdmin)
resourcesRouter.delete('/:id', authenticateJwt, requireRoles([UserRole.SUPERADMIN]), async (req: Request, res: Response) => {
  try {
    const { id } = req.params;

    // Verificar si tiene préstamos históricos antes de borrar
    const loanCount = await prisma.loanItem.count({ where: { itemId: id } });
    if (loanCount > 0) {
      // Si tiene préstamos históricos, se marca como BAJA en vez de eliminar para no romper auditoría
      await prisma.inventoryItem.update({
        where: { id },
        data: { status: ItemStatus.BAJA }
      });
      return res.json({
        success: true,
        message: 'El recurso tiene historial de préstamos; se cambió su estado a BAJA patrimonial para conservar trazabilidad.'
      });
    }

    await prisma.inventoryItem.delete({ where: { id } });
    return res.json({ success: true, message: 'Recurso eliminado del catálogo' });
  } catch (error: any) {
    return res.status(500).json({ success: false, error: error.message || 'Error al eliminar recurso' });
  }
});
