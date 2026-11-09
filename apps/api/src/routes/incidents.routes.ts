import { Router, Request, Response } from 'express';
import { z } from 'zod';
import { prisma } from '@inversion/database';
import { authenticateJwt, requireRoles } from '../middlewares/auth.middleware.js';
import { IncidentSeverity, IncidentStatus, ItemStatus, UserRole, UserStatus } from '@inversion/shared-types';

export const incidentsRouter = Router();

const createIncidentSchema = z.object({
  userId: z.string().uuid(),
  itemId: z.string().uuid().optional(),
  loanRequestId: z.string().uuid().optional(),
  severity: z.nativeEnum(IncidentSeverity),
  description: z.string().min(10),
  reparationCostMxn: z.number().positive().optional()
});

const resolveIncidentSchema = z.object({
  supervisionNotes: z.string().min(5),
  reparationCostMxn: z.number().positive().optional(),
  restoreReputationPoints: z.number().int().min(0).max(30).default(10)
});

// 1. Listar incidencias con filtros
incidentsRouter.get('/', authenticateJwt, async (req: Request, res: Response) => {
  try {
    const { status, severity, userId } = req.query;

    const where: any = {};

    // Si es estudiante o docente solo puede ver sus propias incidencias
    if (req.user?.role === UserRole.ESTUDIANTE || req.user?.role === UserRole.DOCENTE) {
      where.userId = req.user.userId;
    } else if (userId && typeof userId === 'string') {
      where.userId = userId;
    }

    if (status && Object.values(IncidentStatus).includes(status as IncidentStatus)) {
      where.status = status as IncidentStatus;
    }
    if (severity && Object.values(IncidentSeverity).includes(severity as IncidentSeverity)) {
      where.severity = severity as IncidentSeverity;
    }

    const incidents = await prisma.incident.findMany({
      where,
      include: {
        user: {
          select: { id: true, fullName: true, studentCode: true, email: true, reputationScore: true }
        },
        item: {
          select: { id: true, name: true, assetTag: true, serialNumber: true }
        }
      },
      orderBy: { createdAt: 'desc' }
    });

    return res.json({
      success: true,
      data: incidents,
      incidentes: incidents
    });
  } catch (error: any) {
    return res.status(500).json({ success: false, error: error.message || 'Error al listar incidencias' });
  }
});

// 2. Detalle de una incidencia
incidentsRouter.get('/:id', authenticateJwt, async (req: Request, res: Response) => {
  try {
    const { id } = req.params;

    const incident = await prisma.incident.findUnique({
      where: { id },
      include: {
        user: { select: { id: true, fullName: true, studentCode: true, email: true, reputationScore: true, status: true } },
        item: true,
        loanRequest: { select: { id: true, folioNumber: true, startTime: true, endTime: true } }
      }
    });

    if (!incident) {
      return res.status(404).json({ success: false, error: 'Incidencia no encontrada' });
    }

    // Validación de pertenencia si no es admin
    if (
      (req.user?.role === UserRole.ESTUDIANTE || req.user?.role === UserRole.DOCENTE) &&
      incident.userId !== req.user.userId
    ) {
      return res.status(403).json({ success: false, error: 'No tienes permiso para ver esta incidencia' });
    }

    return res.json({ success: true, data: incident });
  } catch (error: any) {
    return res.status(500).json({ success: false, error: error.message || 'Error al consultar incidencia' });
  }
});

// 3. Crear incidencia y penalizar Trust Score (Técnico / Almacén / Admin)
incidentsRouter.post('/', authenticateJwt, requireRoles([UserRole.SUPERADMIN, UserRole.ALMACEN_ADMIN]), async (req: Request, res: Response) => {
  try {
    const data = createIncidentSchema.parse(req.body);

    // Calcular deducción de reputación según la severidad
    let deduction = 5;
    if (data.severity === IncidentSeverity.MODERADA) deduction = 15;
    if (data.severity === IncidentSeverity.GRAVE) deduction = 30;

    const targetUser = await prisma.user.findUnique({ where: { id: data.userId } });
    if (!targetUser) {
      return res.status(404).json({ success: false, error: 'Usuario no encontrado' });
    }

    const newScore = Math.max(0, targetUser.reputationScore - deduction);
    const newStatus = newScore < 50 ? UserStatus.SANCIONADO : targetUser.status;

    // Ejecutar en transacción atómica
    const [incident, updatedUser] = await prisma.$transaction([
      prisma.incident.create({
        data: {
          userId: data.userId,
          itemId: data.itemId,
          loanRequestId: data.loanRequestId,
          severity: data.severity,
          description: data.description,
          reparationCostMxn: data.reparationCostMxn,
          status: IncidentStatus.ABIERTO
        }
      }),
      prisma.user.update({
        where: { id: data.userId },
        data: {
          reputationScore: newScore,
          status: newStatus
        }
      }),
      // Crear notificación para el usuario
      prisma.notification.create({
        data: {
          userId: data.userId,
          title: `⚠️ Incidencia Registrada: Penalización de ${deduction} pts en Trust Score`,
          message: `Se ha abierto un reporte de incidencia por: ${data.description}. Tu puntuación actual es ${newScore}/100.${newScore < 50 ? ' Tu cuenta ha sido suspendida temporalmente para nuevas reservas.' : ''}`
        }
      })
    ]);

    // Si se reportó un equipo específico, marcarlo como DAÑADO
    if (data.itemId) {
      await prisma.inventoryItem.update({
        where: { id: data.itemId },
        data: { status: ItemStatus.DANADO }
      });
    }

    return res.status(201).json({
      success: true,
      data: incident,
      userUpdatedScore: updatedUser.reputationScore,
      userStatus: updatedUser.status,
      message: `Incidencia registrada. Se dedujeron ${deduction} puntos de confiabilidad al usuario.`
    });
  } catch (error: any) {
    if (error instanceof z.ZodError) {
      return res.status(400).json({ success: false, error: error.errors });
    }
    return res.status(500).json({ success: false, error: error.message || 'Error al registrar incidencia' });
  }
});

// 3.1. Formalizar Compromiso de Reparación / Restitución Supervisada (RF-01.3)
incidentsRouter.patch('/:id/commitment', authenticateJwt, requireRoles([UserRole.SUPERADMIN, UserRole.ALMACEN_ADMIN]), async (req: Request, res: Response) => {
  try {
    const { id } = req.params;
    const raw = req.body || {};
    const commitmentType = raw.commitmentType || raw.tipo;
    const agreedAmountMxn = raw.agreedAmountMxn !== undefined ? Number(raw.agreedAmountMxn) : (raw.montoEstimadoMxn !== undefined ? Number(raw.montoEstimadoMxn) : undefined);
    const agreedHours = raw.agreedHours !== undefined ? Number(raw.agreedHours) : (raw.horasServicio !== undefined ? Number(raw.horasServicio) : undefined);
    const deadlineDate = raw.deadlineDate || raw.fechaLimite;
    const supervisionNotes = raw.supervisionNotes || raw.notasSupervision;

    const validated = z.object({
      commitmentType: z.enum(['REPOSICION_ECONOMICA', 'REPARACION_TECNICA', 'SERVICIO_LABORATORIO']),
      agreedAmountMxn: z.number().positive().optional(),
      agreedHours: z.number().positive().optional(),
      deadlineDate: z.string().optional(),
      supervisionNotes: z.string().min(3)
    }).parse({ commitmentType, agreedAmountMxn, agreedHours, deadlineDate, supervisionNotes });

    const incident = await prisma.incident.findUnique({
      where: { id },
      include: { user: true, item: true }
    });

    if (!incident) {
      return res.status(404).json({ success: false, error: 'Incidencia no encontrada' });
    }

    const commitmentDetail = `[COMPROMISO ACORDADO - ${validated.commitmentType}] ${validated.supervisionNotes}. ` +
      (validated.agreedAmountMxn ? `Monto pactado: $${validated.agreedAmountMxn} MXN. ` : '') +
      (validated.agreedHours ? `Horas de servicio: ${validated.agreedHours} hrs. ` : '') +
      (validated.deadlineDate ? `Fecha límite: ${validated.deadlineDate}.` : '');

    const updatedIncident = await prisma.incident.update({
      where: { id },
      data: {
        status: IncidentStatus.EN_REPARACION_SUPERVISADA,
        supervisionNotes: commitmentDetail,
        reparationCostMxn: validated.agreedAmountMxn || incident.reparationCostMxn
      }
    });

    // Notificar al estudiante para su seguimiento
    await prisma.notification.create({
      data: {
        userId: incident.userId,
        title: '🛠️ Expediente de Reparación Supervisada Abierto',
        message: `Se ha registrado tu compromiso de restitución para el folio ${incident.id.slice(0, 8)}. Al cumplirlo satisfactoriamente, tus puntos de reputación serán restaurados.`
      }
    });

    return res.json({
      success: true,
      data: updatedIncident,
      incidente: updatedIncident,
      message: 'Compromiso de reparación formalizado exitosamente. Estado cambiado a En Reparación Supervisada.'
    });
  } catch (error: any) {
    if (error instanceof z.ZodError) {
      return res.status(400).json({ success: false, error: error.errors });
    }
    return res.status(500).json({ success: false, error: error.message || 'Error al formalizar compromiso' });
  }
});

// 4. Resolver Incidencia / Reparación Supervisada (Soporta PATCH y POST)
const resolveIncidentHandler = async (req: Request, res: Response) => {
  try {
    const { id } = req.params;
    const body = req.body || {};
    const normalizedBody = {
      supervisionNotes: body.supervisionNotes || body.solucion || 'Incidencia resuelta satisfactoriamente',
      reparationCostMxn: body.reparationCostMxn,
      restoreReputationPoints: body.restoreReputationPoints ?? (body.restaurarPuntos ? 15 : 10)
    };

    const { supervisionNotes, reparationCostMxn, restoreReputationPoints } = resolveIncidentSchema.parse(normalizedBody);

    const incident = await prisma.incident.findUnique({ where: { id } });
    if (!incident) {
      return res.status(404).json({ success: false, error: 'Incidencia no encontrada' });
    }

    // Actualizar usuario bonificando reputación si cumplió con la reparación
    const user = await prisma.user.findUnique({ where: { id: incident.userId } });
    const restoredScore = Math.min(100, (user?.reputationScore || 0) + (restoreReputationPoints || 0));
    const restoredStatus = restoredScore >= 50 && user?.status === UserStatus.SANCIONADO ? UserStatus.ACTIVO : user?.status;

    await prisma.$transaction([
      prisma.incident.update({
        where: { id },
        data: {
          status: IncidentStatus.RESUELTO,
          supervisionNotes,
          reparationCostMxn: reparationCostMxn || incident.reparationCostMxn,
          resolvedAt: new Date()
        }
      }),
      prisma.user.update({
        where: { id: incident.userId },
        data: {
          reputationScore: restoredScore,
          status: restoredStatus
        }
      }),
      prisma.notification.create({
        data: {
          userId: incident.userId,
          title: '✅ Expediente de Incidencia Resuelto',
          message: `La reparación o reposición ha sido aprobada por almacén. Se abonaron +${restoreReputationPoints} puntos a tu Trust Score (${restoredScore}/100).`
        }
      })
    ]);

    // Si el ítem ya fue reparado, volver a DISPONIBLE
    if (incident.itemId) {
      await prisma.inventoryItem.update({
        where: { id: incident.itemId },
        data: { status: ItemStatus.DISPONIBLE }
      });
    }

    return res.json({
      success: true,
      message: 'Incidencia resuelta y expediente archivado exitosamente.',
      incidente: { ...incident, status: IncidentStatus.RESUELTO },
      scoreRestaurado: true
    });
  } catch (error: any) {
    if (error instanceof z.ZodError) {
      return res.status(400).json({ success: false, error: error.errors });
    }
    return res.status(500).json({ success: false, error: error.message || 'Error al resolver incidencia' });
  }
};

incidentsRouter.patch('/:id/resolve', authenticateJwt, requireRoles([UserRole.SUPERADMIN, UserRole.ALMACEN_ADMIN]), resolveIncidentHandler);
incidentsRouter.post('/:id/resolve', authenticateJwt, requireRoles([UserRole.SUPERADMIN, UserRole.ALMACEN_ADMIN]), resolveIncidentHandler);
