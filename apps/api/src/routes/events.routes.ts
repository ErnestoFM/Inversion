import { Router, Request, Response } from 'express';
import { z } from 'zod';
import { prisma } from '@inversion/database';
import { authenticateJwt, requireRoles } from '../middlewares/auth.middleware.js';
import { CryptoQrService } from '../services/qr.service.js';
import { RedisLockService } from '../services/redis-lock.service.js';
import { CutonalaBusinessRules } from '../utils/cutonala-rules.js';
import { EventType, EventVisibility, RequestStatus, AttendeeStatus, UserRole } from '@inversion/shared-types';

export const eventsRouter = Router();

const preReserveSchema = z.object({
  spaceId: z.string().uuid(),
  startTime: z.string().datetime(),
  endTime: z.string().datetime()
});

const createEventSchema = z.object({
  title: z.string().min(5),
  description: z.string().min(10),
  type: z.nativeEnum(EventType),
  visibility: z.nativeEnum(EventVisibility).default(EventVisibility.PUBLICO),
  targetCareer: z.string().optional(),
  targetSemesters: z.array(z.number().int()).optional(),
  accessCode: z.string().optional(),
  posterUrl: z.string().url().optional(),
  trailerUrl: z.string().url().optional(),
  spaceId: z.string().uuid(),
  startTime: z.string().datetime(),
  endTime: z.string().datetime(),
  maxCapacity: z.number().int().positive(),
  coResponsibleStudentCodes: z.array(z.string()).optional()
});

const reviewSchema = z.object({
  rating: z.number().int().min(1).max(5),
  comment: z.string().min(5)
});

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

    return res.json({ success: true, data: formatted });
  } catch (error: any) {
    return res.status(500).json({ success: false, error: 'Error al consultar la cartelera de eventos.' });
  }
});

// 2. Pre-reserva temporal con bloqueo Anti-Empalme en Redis (TTL 15 min)
eventsRouter.post('/pre-reserve', authenticateJwt, async (req: Request, res: Response) => {
  try {
    const data = preReserveSchema.parse(req.body);
    const start = new Date(data.startTime);
    const end = new Date(data.endTime);
    const userId = req.user!.userId;

    // Validación de horario CUTonalá (08:00 a 19:00 hrs)
    const hoursValidation = CutonalaBusinessRules.validateOperatingHours(start, end);
    if (!hoursValidation.valid) {
      return res.status(400).json({ success: false, error: hoursValidation.error });
    }

    // Validación de antelación (3 a 15 días)
    const antValidation = CutonalaBusinessRules.validateSpaceAnticipation(start);
    if (!antValidation.valid) {
      return res.status(400).json({ success: false, error: antValidation.error });
    }

    // Verificar si ya existe un evento aprobado o en curso en PostgreSQL
    const existingConflict = await prisma.event.findFirst({
      where: {
        spaceId: data.spaceId,
        status: { in: [RequestStatus.APROBADO, RequestStatus.EN_CURSO, RequestStatus.PENDIENTE_APROBACION] },
        OR: [
          { startTime: { lt: end, gte: start } },
          { endTime: { gt: start, lte: end } },
          { startTime: { lte: start }, endTime: { gte: end } }
        ]
      }
    });

    if (existingConflict) {
      return res.status(409).json({
        success: false,
        error: 'El espacio seleccionado ya tiene una reserva confirmada o en revisión para ese horario.'
      });
    }

    // Intentar adquirir el bloqueo en Redis por 15 minutos (900 seg)
    const lockResult = await RedisLockService.acquireLock('space', data.spaceId, start, end, userId, 900);

    if (!lockResult.acquired) {
      return res.status(409).json({
        success: false,
        error: 'El espacio se encuentra en proceso de solicitud por otro usuario. Intenta de nuevo en unos minutos.',
        remainingTtl: lockResult.remainingTtl
      });
    }

    return res.json({
      success: true,
      message: 'Espacio pre-reservado con éxito. Tienes 15 minutos para completar los datos de la solicitud.',
      spaceId: data.spaceId,
      expiresAt: new Date(Date.now() + 900 * 1000).toISOString()
    });
  } catch (error: any) {
    if (error instanceof z.ZodError) {
      return res.status(400).json({ success: false, error: error.errors });
    }
    return res.status(500).json({ success: false, error: error.message || 'Error al procesar pre-reserva' });
  }
});

// 3. Crear solicitud formal de Evento / Reserva de Espacio
eventsRouter.post('/', authenticateJwt, async (req: Request, res: Response) => {
  try {
    const data = createEventSchema.parse(req.body);
    const start = new Date(data.startTime);
    const end = new Date(data.endTime);
    const userId = req.user!.userId;

    // Validación de horario CUTonalá
    const hoursVal = CutonalaBusinessRules.validateOperatingHours(start, end);
    if (!hoursVal.valid) return res.status(400).json({ success: false, error: hoursVal.error });

    const antVal = CutonalaBusinessRules.validateSpaceAnticipation(start);
    if (!antVal.valid) return res.status(400).json({ success: false, error: antVal.error });

    // Verificar en base de datos solapamiento
    const conflict = await prisma.event.findFirst({
      where: {
        spaceId: data.spaceId,
        status: { in: [RequestStatus.APROBADO, RequestStatus.EN_CURSO] },
        OR: [
          { startTime: { lt: end, gte: start } },
          { endTime: { gt: start, lte: end } },
          { startTime: { lte: start }, endTime: { gte: end } }
        ]
      }
    });

    if (conflict) {
      return res.status(409).json({ success: false, error: 'Conflicto: Ya existe un evento aprobado en ese horario.' });
    }

    // Resolver co-responsables si se enviaron códigos de estudiante
    let coResponsibleUserIds: string[] = [];
    if (data.coResponsibleStudentCodes && data.coResponsibleStudentCodes.length > 0) {
      const coUsers = await prisma.user.findMany({
        where: { studentCode: { in: data.coResponsibleStudentCodes } },
        select: { id: true }
      });
      coResponsibleUserIds = coUsers.map((u) => u.id);
    }

    // Crear evento e insertar co-responsables en transacción
    const event = await prisma.event.create({
      data: {
        title: data.title,
        description: data.description,
        type: data.type,
        visibility: data.visibility,
        targetCareer: data.targetCareer,
        targetSemesters: data.targetSemesters || [],
        accessCode: data.accessCode,
        posterUrl: data.posterUrl,
        trailerUrl: data.trailerUrl,
        spaceId: data.spaceId,
        startTime: start,
        endTime: end,
        maxCapacity: data.maxCapacity,
        status: RequestStatus.PENDIENTE_APROBACION,
        creatorId: userId,
        coResponsibles: {
          create: coResponsibleUserIds.map((cId) => ({
            userId: cId,
            hasSigned: false
          }))
        }
      },
      include: {
        space: true,
        coResponsibles: { include: { user: { select: { fullName: true, studentCode: true } } } }
      }
    });

    // Liberar el lock de Redis ya que quedó registrado en BD
    await RedisLockService.releaseLock('space', data.spaceId, start, end, userId);

    return res.status(201).json({
      success: true,
      data: event,
      message: 'Solicitud de evento registrada exitosamente. Queda pendiente de aprobación por Coordinación.'
    });
  } catch (error: any) {
    if (error instanceof z.ZodError) {
      return res.status(400).json({ success: false, error: error.errors });
    }
    return res.status(500).json({ success: false, error: error.message || 'Error al crear evento' });
  }
});

// 4. Registro a Evento y Generación de Boleto con QR
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
      return res.status(404).json({ success: false, error: 'Evento no disponible para registro.' });
    }

    if (event.visibility === EventVisibility.PRIVADO_CODIGO && event.accessCode && event.accessCode !== accessCode) {
      return res.status(403).json({ success: false, error: 'Código de acceso al evento incorrecto.' });
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
      success: true,
      message: isFull
        ? 'Cupo lleno. Has sido colocado en la lista de espera con prioridad.'
        : '¡Registro confirmado exitosamente!',
      status: attendee.status,
      qrToken,
      qrDataUrl
    });
  } catch (error: any) {
    return res.status(500).json({ success: false, error: 'Error al procesar el registro al evento.' });
  }
});

// 5. Escaneo de Boleto QR en Puerta (Staff / Encargado)
eventsRouter.post('/scan-ticket', authenticateJwt, async (req: Request, res: Response) => {
  try {
    const { qrToken } = req.body;
    if (!qrToken) return res.status(400).json({ success: false, error: 'Token de código QR requerido.' });

    const payload = CryptoQrService.verifyTicketToken(qrToken);

    const attendee = await prisma.eventAttendee.findUnique({
      where: { qrToken },
      include: {
        user: { select: { fullName: true, studentCode: true, career: true } },
        event: { select: { title: true, startTime: true } }
      }
    });

    if (!attendee) {
      return res.status(404).json({ success: false, error: 'Boleto no registrado o inválido.' });
    }

    if (attendee.status === AttendeeStatus.ASISTIO) {
      return res.status(400).json({
        success: false,
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
    return res.status(400).json({ success: false, error: 'Código QR no válido o expirado.' });
  }
});

// 6. Dictamen de Aprobación o Rebote con Motivo (Admin / Coordinador)
eventsRouter.patch(
  '/:id/status',
  authenticateJwt,
  requireRoles([UserRole.SUPERADMIN, UserRole.DIFUSION_EVENTOS]),
  async (req: Request, res: Response) => {
    try {
      const { id } = req.params;
      const { status, rejectionReason } = req.body;

      if (!status || ![RequestStatus.APROBADO, RequestStatus.REBOTADO_CON_MOTIVO, RequestStatus.CANCELADO].includes(status)) {
        return res.status(400).json({ success: false, error: 'Estado de dictamen no válido.' });
      }

      if (status === RequestStatus.REBOTADO_CON_MOTIVO && (!rejectionReason || rejectionReason.trim().length < 5)) {
        return res.status(400).json({ success: false, error: 'El motivo de rechazo es obligatorio (mínimo 5 caracteres).' });
      }

      const event = await prisma.event.update({
        where: { id },
        data: {
          status,
          rejectionReason: status === RequestStatus.REBOTADO_CON_MOTIVO ? rejectionReason : null
        },
        include: { creator: true }
      });

      // Notificar al creador del evento
      await prisma.notification.create({
        data: {
          userId: event.creatorId,
          title: status === RequestStatus.APROBADO ? '🎉 Evento Aprobado' : '⚠️ Solicitud de Evento Rechazada',
          message:
            status === RequestStatus.APROBADO
              ? `Tu solicitud para el evento "${event.title}" ha sido autorizada.`
              : `Tu evento "${event.title}" fue rechazado: ${rejectionReason}`
        }
      });

      return res.json({ success: true, data: event, message: `Evento marcado como ${status}` });
    } catch (error: any) {
      return res.status(500).json({ success: false, error: error.message || 'Error al dictaminar evento' });
    }
  }
);

// 7. Reseñas Verificadas (Solo asistentes con QR escaneado)
eventsRouter.post('/:id/reviews', authenticateJwt, async (req: Request, res: Response) => {
  try {
    const eventId = req.params.id;
    const userId = req.user!.userId;
    const { rating, comment } = reviewSchema.parse(req.body);

    // Validar que el usuario haya ASISTIDO al evento
    const attendance = await prisma.eventAttendee.findUnique({
      where: { eventId_userId: { eventId, userId } }
    });

    if (!attendance || attendance.status !== AttendeeStatus.ASISTIO) {
      return res.status(403).json({
        success: false,
        error: '⚠️ Solo los usuarios con asistencia verificada mediante código QR pueden publicar una reseña.'
      });
    }

    const review = await prisma.review.upsert({
      where: { eventId_userId: { eventId, userId } },
      update: { rating, comment },
      create: { eventId, userId, rating, comment }
    });

    return res.status(201).json({ success: true, data: review, message: '¡Gracias por tu reseña verificada!' });
  } catch (error: any) {
    if (error instanceof z.ZodError) {
      return res.status(400).json({ success: false, error: error.errors });
    }
    return res.status(500).json({ success: false, error: error.message || 'Error al registrar reseña' });
  }
});

// 8. Listar reseñas de un evento
eventsRouter.get('/:id/reviews', async (req: Request, res: Response) => {
  try {
    const { id } = req.params;
    const reviews = await prisma.review.findMany({
      where: { eventId: id },
      include: { user: { select: { fullName: true, career: true } } },
      orderBy: { createdAt: 'desc' }
    });

    return res.json({ success: true, data: reviews });
  } catch (error: any) {
    return res.status(500).json({ success: false, error: error.message });
  }
});
