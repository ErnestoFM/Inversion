import { Router, Request, Response } from 'express';
import { prisma } from '@inversion/database';
import { authenticateJwt } from '../middlewares/auth.middleware.js';

export const notificationsRouter = Router();

// 1. Listar notificaciones del usuario en sesión
notificationsRouter.get('/', authenticateJwt, async (req: Request, res: Response) => {
  try {
    const userId = req.user!.userId;
    const limit = Number(req.query.limit) || 20;

    const notifications = await prisma.notification.findMany({
      where: { userId },
      orderBy: { createdAt: 'desc' },
      take: limit
    });

    const unreadCount = await prisma.notification.count({
      where: { userId, isRead: false }
    });

    return res.json({
      success: true,
      data: {
        notifications,
        unreadCount
      }
    });
  } catch (error: any) {
    return res.status(500).json({ success: false, error: error.message || 'Error al obtener notificaciones' });
  }
});

// 2. Contador rápido de no leídas (Polling / Campana)
notificationsRouter.get('/unread-count', authenticateJwt, async (req: Request, res: Response) => {
  try {
    const userId = req.user!.userId;
    const unreadCount = await prisma.notification.count({
      where: { userId, isRead: false }
    });

    return res.json({ success: true, data: { unreadCount } });
  } catch (error: any) {
    return res.status(500).json({ success: false, error: error.message });
  }
});

// 3. Marcar notificación individual como leída
notificationsRouter.patch('/:id/read', authenticateJwt, async (req: Request, res: Response) => {
  try {
    const { id } = req.params;
    const userId = req.user!.userId;

    const notification = await prisma.notification.findUnique({ where: { id } });
    if (!notification || notification.userId !== userId) {
      return res.status(404).json({ success: false, error: 'Notificación no encontrada' });
    }

    const updated = await prisma.notification.update({
      where: { id },
      data: { isRead: true }
    });

    return res.json({ success: true, data: updated });
  } catch (error: any) {
    return res.status(500).json({ success: false, error: error.message });
  }
});

// 4. Marcar todas las notificaciones como leídas
notificationsRouter.patch('/read-all', authenticateJwt, async (req: Request, res: Response) => {
  try {
    const userId = req.user!.userId;

    await prisma.notification.updateMany({
      where: { userId, isRead: false },
      data: { isRead: true }
    });

    return res.json({ success: true, message: 'Todas las notificaciones han sido marcadas como leídas' });
  } catch (error: any) {
    return res.status(500).json({ success: false, error: error.message });
  }
});
