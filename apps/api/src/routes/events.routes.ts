import { Router, Request, Response } from 'express';
import { z } from 'zod';
import { prisma } from '@inversion/database';
import { redis } from '../config/redis.js';
import { authenticateJwt } from '../middlewares/auth.middleware.js';
import { CryptoQrService } from '../services/qr.service.js';
import { EventType, EventVisibility, RequestStatus, AttendeeStatus } from '@inversion/shared-types';

export const eventsRouter = Router();

// 1. Cartelera Pública de Eventos y Cineteca
eventsRouter.get('/cartelera', async (req: Request, res: Response) => {
  try {
    const { type, career } = req.query;

    const events = await prisma.event.findMany({
      where: {
        status: RequestStatus.APROBADO,
        startTime: { gte: new Date(Date.now() - 2 * 60 * 60 * 1000) }, // Eventos vigentes
        ...(type ? { type: type as EventType } : {})
      },
      include: {
        space: { select: { name: true, building: true, capacity: true } },
        creator: { select: { fullName: true } },
        _count: { select: { attendees: { where: { status: AttendeeStatus.REGISTRADO } }, reviews: true } }
      },
      orderBy: { startTime: 'asc' }
    });

    const formatted = events.map((e) => ({
      id: e.id,
      title: e.title,
      description: e.description,
      type: e.type,
      visibility: e.visibility,
      posterUrl: e.posterUrl,
      trailerUrl: e.trailerUrl,
      spaceName: e.space?.name || 'Por definir',
      building: e.space?.building || 'CUTonalá',
      startTime: e.startTime.toISOString(),
      endTime: e.endTime.toISOString(),
      maxCapacity: e.maxCapacity,
      registeredCount: e._count.attendees,
      availableCapacity: Math.max(0, e.maxCapacity - e._count.attendees),
      creatorName: e.creator.fullName,
      totalReviewsCount: e._count.reviews
    }));

    return res.json(formatted);
  } catch (error: any) {
    return res.status(500).json({ error: 'Error al consultar la cartelera de eventos.' });
  }
});

// 2. Registro a Evento y Generación de Boleto con QR
eventsRouter.post('/:id/register', authenticateJwt, async (req: Request, res: Response) => {
  try {
    const eventId = req.params.id;
    const userId = req.user!.userId;
    const { accessCode } = req.body;

    const event = await prisma.event.findUnique({
      where: { id: eventId },
      include: { _count: { select: { attendees: { where: { status: AttendeeStatus.REGISTRADO } } } } }
    });

    if (!event || event.status !== RequestStatus.APROBADO) {
      return res.status(404).json({ error: 'Evento no disponible para registro.' });
    }

    // Validación de código de acceso si es privado
    if (event.visibility === EventVisibility.PRIVADO_CODIGO && event.accessCode && event.accessCode !== accessCode) {
      return res.status(403).json({ error: 'Código de acceso al evento incorrecto.' });
    }

    const currentCount = event._count.attendees;
    const isFull = currentCount >= event.maxCapacity;

    const qrToken = CryptoQrService.generateTicketToken({
      ticketId: `${eventId}-${userId}`,
      eventId,
      userId,
      studentCode: req.user!.studentCode
    });

    const attendee = await prisma.eventAttendee.upsert({
      where: { eventId_userId: { eventId, userId } },
      update: {
        status: isFull ? AttendeeStatus.EN_LISTA_ESPERA : AttendeeStatus.REGISTRADO,
        qrToken
      },
      create: {
        eventId,
        userId,
        status: isFull ? AttendeeStatus.EN_LISTA_ESPERA : AttendeeStatus.REGISTRADO,
        qrToken
      }
    });

    const qrDataUrl = await CryptoQrService.generateQrDataUrl(qrToken);

    return res.json({
      message: isFull
        ? 'Cupo lleno. Has sido colocado en la lista de espera con prioridad.'
        : '¡Registro confirmado exitosamente!',
      status: attendee.status,
      qrToken,
      qrDataUrl
    });
  } catch (error: any) {
    return res.status(500).json({ error: 'Error al procesar el registro al evento.' });
  }
});

// 3. Escaneo y Validación de Código QR en Puerta (Staff / Encargado)
eventsRouter.post('/scan-ticket', authenticateJwt, async (req: Request, res: Response) => {
  try {
    const { qrToken } = req.body;
    if (!qrToken) return res.status(400).json({ error: 'Token de código QR requerido.' });

    const payload = CryptoQrService.verifyTicketToken(qrToken);

    const attendee = await prisma.eventAttendee.findUnique({
      where: { qrToken },
      include: {
        user: { select: { fullName: true, studentCode: true, career: true } },
        event: { select: { title: true, startTime: true } }
      }
    });

    if (!attendee) {
      return res.status(404).json({ error: 'Boleto no registrado o inválido.' });
    }

    if (attendee.status === AttendeeStatus.ASISTIO) {
      return res.status(400).json({
        error: '⚠️ Este boleto YA FUE ESCANEADO previamente.',
        scannedAt: attendee.scannedAt,
        student: attendee.user
      });
    }

    await prisma.eventAttendee.update({
      where: { id: attendee.id },
      data: {
        status: AttendeeStatus.ASISTIO,
        scannedAt: new Date()
      }
    });

    return res.json({
      success: true,
      message: '✅ Acceso Autorizado',
      student: attendee.user,
      event: attendee.event
    });
  } catch (error: any) {
    return res.status(400).json({ error: 'Código QR no válido o expirado.' });
  }
});
