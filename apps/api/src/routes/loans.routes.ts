import { Router, Request, Response } from 'express';
import { z } from 'zod';
import path from 'path';
import { prisma } from '@inversion/database';
import { authenticateJwt, requireRoles } from '../middlewares/auth.middleware.js';
import { PdfService } from '../services/pdf.service.js';
import { storageService } from '../services/storage.service.js';
import { mailService } from '../services/mail.service.js';
import { CutonalaBusinessRules } from '../utils/cutonala-rules.js';
import { UserRole, RequestStatus, ItemStatus } from '@inversion/shared-types';

export const loansRouter = Router();

const createLoanSchema = z.object({
  spaceId: z.string().uuid().optional(),
  itemIds: z.array(z.string().uuid()).min(1, 'Debes seleccionar al menos un recurso para el préstamo'),
  purpose: z.string().min(10, 'La justificación o propósito debe tener al menos 10 caracteres'),
  startTime: z.string().datetime(),
  endTime: z.string().datetime(),
  isExtendedLoan: z.boolean().default(false),
  coResponsibleStudentCodes: z.array(z.string()).default([]),
  signatureBase64: z.string().min(20, 'Firma digital obligatoria')
});

const signCoResponsibleSchema = z.object({
  signatureBase64: z.string().min(20, 'Firma digital obligatoria')
});

const checklistSalidaSchema = z.object({
  deliveryNotes: z.string().min(5, 'Notas de inspección de salida requeridas'),
  approverSignatureBase64: z.string().min(20, 'Firma del técnico requerida')
});

const checklistEntradaSchema = z.object({
  returnNotes: z.string().min(5, 'Notas de inspección de entrada requeridas'),
  hasIncidents: z.boolean().default(false),
  incidentDescription: z.string().optional()
});

// 1. Listar solicitudes de préstamo con filtros y control de rol
loansRouter.get('/', authenticateJwt, async (req: Request, res: Response) => {
  try {
    const { status, search } = req.query;
    const where: any = {};

    // Si es estudiante o docente, solo ve sus propios préstamos
    if (req.user?.role === UserRole.ESTUDIANTE || req.user?.role === UserRole.DOCENTE) {
      where.userId = req.user.userId;
    }

    if (status && Object.values(RequestStatus).includes(status as RequestStatus)) {
      where.status = status as RequestStatus;
    }

    if (search && typeof search === 'string') {
      where.OR = [
        { folioNumber: { contains: search, mode: 'insensitive' } },
        { purpose: { contains: search, mode: 'insensitive' } },
        { user: { fullName: { contains: search, mode: 'insensitive' } } }
      ];
    }

    const loans = await prisma.loanRequest.findMany({
      where,
      include: {
        user: { select: { id: true, fullName: true, studentCode: true, email: true, reputationScore: true } },
        space: { select: { id: true, name: true, building: true } },
        items: { include: { item: { select: { id: true, name: true, assetTag: true, category: true, status: true } } } }
      },
      orderBy: { createdAt: 'desc' }
    });

    return res.json({ success: true, data: loans });
  } catch (error: any) {
    return res.status(500).json({ success: false, error: error.message || 'Error al listar préstamos' });
  }
});

// 2. Detalle de una solicitud de préstamo
loansRouter.get('/:id', authenticateJwt, async (req: Request, res: Response) => {
  try {
    const { id } = req.params;

    const loan = await prisma.loanRequest.findUnique({
      where: { id },
      include: {
        user: { select: { id: true, fullName: true, studentCode: true, email: true, reputationScore: true, career: true } },
        space: true,
        items: { include: { item: true } },
        incidents: true
      }
    });

    if (!loan) {
      return res.status(404).json({ success: false, error: 'Solicitud de préstamo no encontrada' });
    }

    // Validación de pertenencia
    if (
      (req.user?.role === UserRole.ESTUDIANTE || req.user?.role === UserRole.DOCENTE) &&
      loan.userId !== req.user.userId
    ) {
      return res.status(403).json({ success: false, error: 'No tienes autorización para ver esta solicitud' });
    }

    return res.json({ success: true, data: loan });
  } catch (error: any) {
    return res.status(500).json({ success: false, error: error.message || 'Error al consultar préstamo' });
  }
});

// 3. Crear Solicitud de Préstamo con Firma y Validaciones CUTonalá
loansRouter.post('/', authenticateJwt, async (req: Request, res: Response) => {
  try {
    const data = createLoanSchema.parse(req.body);
    const userId = req.user!.userId;
    const ipAddress = req.ip || req.socket.remoteAddress || '127.0.0.1';

    const start = new Date(data.startTime);
    const end = new Date(data.endTime);

    // Validación de horario CUTonalá (08:00 a 19:00 hrs)
    const hoursVal = CutonalaBusinessRules.validateOperatingHours(start, end);
    if (!hoursVal.valid) return res.status(400).json({ success: false, error: hoursVal.error });

    // Validación de duración de préstamo (3 días ordinario, 30 extendido)
    const loanVal = CutonalaBusinessRules.validateLoanDuration(start, end, data.isExtendedLoan);
    if (!loanVal.valid) return res.status(400).json({ success: false, error: loanVal.error });

    // Verificar que los ítems solicitados estén DISPONIBLES
    const items = await prisma.inventoryItem.findMany({
      where: { id: { in: data.itemIds } }
    });

    const unavailableItems = items.filter((i) => i.status !== ItemStatus.DISPONIBLE);
    if (unavailableItems.length > 0) {
      return res.status(409).json({
        success: false,
        error: `Los siguientes recursos no se encuentran disponibles: ${unavailableItems.map((i) => i.name).join(', ')}`
      });
    }

    // Generar Folio Oficial Criptográfico
    const year = new Date().getFullYear();
    const count = await prisma.loanRequest.count();
    const folioNumber = `RESP-${year}-${String(count + 1).padStart(4, '0')}`;

    // Validar existencia de co-responsables
    const coResponsibleUsers = await prisma.user.findMany({
      where: { studentCode: { in: data.coResponsibleStudentCodes } }
    });

    const loan = await prisma.loanRequest.create({
      data: {
        folioNumber,
        userId,
        spaceId: data.spaceId,
        purpose: data.purpose,
        startTime: start,
        endTime: end,
        status: RequestStatus.PENDIENTE_APROBACION,
        requesterSignatureUrl: data.signatureBase64,
        ipAddress,
        items: {
          create: data.itemIds.map((itemId) => ({ itemId }))
        }
      },
      include: {
        user: true,
        space: true,
        items: { include: { item: true } }
      }
    });

    // Enviar correos de notificación e invitación a co-responsables
    for (const cr of coResponsibleUsers) {
      if (cr.id !== userId) {
        await mailService.sendCoResponsibleInvitation(
          cr.email,
          req.user!.studentCode,
          data.purpose,
          `http://localhost:3000/responsivas/${loan.id}/firmar`
        );
      }
    }

    return res.status(201).json({
      success: true,
      message: 'Solicitud de préstamo registrada con éxito. Pasa a revisión administrativa.',
      folioNumber,
      loanId: loan.id
    });
  } catch (error: any) {
    if (error instanceof z.ZodError) return res.status(400).json({ success: false, error: error.errors });
    return res.status(500).json({ success: false, error: error.message || 'Error al procesar la solicitud.' });
  }
});

// 3.1. Enviar / Reenviar Invitación a Co-Responsables vía Correo (Nodemailer)
loansRouter.post('/:id/send-co-responsible-invite', authenticateJwt, async (req: Request, res: Response) => {
  try {
    const loanId = req.params.id;
    const { email } = req.body;

    const loan = await prisma.loanRequest.findUnique({
      where: { id: loanId },
      include: {
        user: true,
        event: { include: { coResponsibles: { include: { user: true } } } }
      }
    });

    if (!loan) return res.status(404).json({ success: false, error: 'Solicitud de préstamo no encontrada.' });

    const targetEmail = email || loan.event?.coResponsibles?.[0]?.user?.email;

    if (!targetEmail) {
      return res.status(400).json({ success: false, error: 'No se especificó un correo destinatario para el co-responsable.' });
    }

    const signLink = `${process.env.WEB_URL || 'http://localhost:3000'}/responsivas/${loan.id}/firmar?token=${loanId}`;

    await mailService.sendCoResponsibleInvitation(
      targetEmail,
      loan.user.fullName,
      loan.purpose,
      signLink
    );

    return res.json({
      success: true,
      message: `Enlace de firma remota enviado exitosamente a ${targetEmail}.`
    });
  } catch (error: any) {
    return res.status(500).json({ success: false, error: error.message || 'Error al enviar invitación.' });
  }
});

// 3.2. Firma Remota de Co-Responsable (Móvil / Web)
loansRouter.post('/:id/sign-co-responsible', authenticateJwt, async (req: Request, res: Response) => {
  try {
    const loanId = req.params.id;
    const { signatureBase64 } = signCoResponsibleSchema.parse(req.body);
    const userId = req.user!.userId;

    const loan = await prisma.loanRequest.findUnique({
      where: { id: loanId },
      include: {
        user: true,
        event: { include: { coResponsibles: true } }
      }
    });

    if (!loan) return res.status(404).json({ success: false, error: 'Solicitud no encontrada.' });

    // Si tiene evento y co-responsables asociados, actualizar
    if (loan.event?.id) {
      const coResp = await prisma.eventCoResponsible.findFirst({
        where: { eventId: loan.event.id, userId }
      });
      if (coResp) {
        await prisma.eventCoResponsible.update({
          where: { id: coResp.id },
          data: { hasSigned: true, signedAt: new Date() }
        });
      }
    }

    // Notificar al solicitante principal
    await prisma.notification.create({
      data: {
        userId: loan.userId,
        title: '✍️ Firma de Co-Responsable Registrada',
        message: `Un co-responsable ha firmado digitalmente el acta responsiva del folio ${loan.folioNumber}.`
      }
    });

    return res.json({
      success: true,
      message: 'Firma remota del co-responsable asentada y notificada exitosamente.'
    });
  } catch (error: any) {
    if (error instanceof z.ZodError) return res.status(400).json({ success: false, error: error.errors });
    return res.status(500).json({ success: false, error: error.message || 'Error al procesar la firma.' });
  }
});

// 4. Checklist de Salida (Entrega Física) y Generación de PDF Oficial
loansRouter.patch('/:id/checklist-salida', authenticateJwt, requireRoles([UserRole.ALMACEN_ADMIN, UserRole.SUPERADMIN]), async (req: Request, res: Response) => {
  try {
    const loanId = req.params.id;
    const { deliveryNotes, approverSignatureBase64 } = checklistSalidaSchema.parse(req.body);

    const loan = await prisma.loanRequest.findUnique({
      where: { id: loanId },
      include: {
        user: true,
        space: true,
        items: { include: { item: true } }
      }
    });

    if (!loan) return res.status(404).json({ success: false, error: 'Solicitud no encontrada.' });

    // Actualizar estado de materiales a PRESTADO
    for (const item of loan.items) {
      await prisma.inventoryItem.update({
        where: { id: item.itemId },
        data: { status: ItemStatus.PRESTADO }
      });
    }

    // Generar archivo PDF oficial con firmas digitales
    const outputDir = path.resolve(process.cwd(), 'uploads/actas');
    const localPdfPath = await PdfService.generateResponsivaPdf(
      {
        folioNumber: loan.folioNumber,
        createdAt: loan.createdAt.toISOString(),
        userName: loan.user.fullName,
        studentCode: loan.user.studentCode,
        career: loan.user.career || 'Estudiante CUTonalá',
        purpose: loan.purpose,
        spaceName: loan.space?.name,
        items: loan.items.map((i) => ({
          name: i.item.name,
          assetTag: i.item.assetTag,
          serialNumber: i.item.serialNumber
        })),
        coResponsibles: [],
        approverName: req.user!.studentCode,
        approverSignatureBase64,
        requesterSignatureBase64: loan.requesterSignatureUrl || undefined,
        ipAddress: loan.ipAddress || '127.0.0.1'
      },
      outputDir
    );

    // Persistir acta PDF en Google Cloud Storage (GCS)
    const fileName = path.basename(localPdfPath);
    const storageResult = await storageService.uploadFile(localPdfPath, `actas/${fileName}`, 'application/pdf');

    const updated = await prisma.loanRequest.update({
      where: { id: loanId },
      data: {
        status: RequestStatus.EN_CURSO,
        approverSignatureUrl: approverSignatureBase64,
        responsivaPdfPath: storageResult.gcsUri,
        isChecklistDeliveryCompleted: true,
        deliveryNotes
      }
    });

    // Notificar al solicitante
    await prisma.notification.create({
      data: {
        userId: loan.userId,
        title: '📦 Entrega de Recursos Concretada',
        message: `Se ha completado el checklist de salida y emitido tu Acta Responsiva con Folio: ${loan.folioNumber}.`
      }
    });

    return res.json({
      success: true,
      message: '✅ Checklist de salida completado. Equipo entregado y acta PDF generada exitosamente.',
      folioNumber: updated.folioNumber,
      pdfUrl: `/api/v1/loans/${loanId}/pdf`
    });
  } catch (error: any) {
    if (error instanceof z.ZodError) return res.status(400).json({ success: false, error: error.errors });
    return res.status(500).json({ success: false, error: error.message || 'Error al procesar checklist de salida.' });
  }
});

// 5. Checklist de Entrada (Devolución Física) y Cierre
loansRouter.patch('/:id/checklist-entrada', authenticateJwt, requireRoles([UserRole.ALMACEN_ADMIN, UserRole.SUPERADMIN]), async (req: Request, res: Response) => {
  try {
    const loanId = req.params.id;
    const { returnNotes, hasIncidents, incidentDescription } = checklistEntradaSchema.parse(req.body);

    const loan = await prisma.loanRequest.findUnique({
      where: { id: loanId },
      include: { items: true, user: true }
    });

    if (!loan) return res.status(404).json({ success: false, error: 'Solicitud no encontrada.' });

    // Si NO hubo incidencias: devolver ítems a DISPONIBLE, cerrar préstamo y abonar +2 puntos de reputación
    if (!hasIncidents) {
      for (const item of loan.items) {
        await prisma.inventoryItem.update({
          where: { id: item.itemId },
          data: { status: ItemStatus.DISPONIBLE }
        });
      }

      const updatedScore = Math.min(100, loan.user.reputationScore + 2);

      await prisma.$transaction([
        prisma.loanRequest.update({
          where: { id: loanId },
          data: {
            status: RequestStatus.FINALIZADO,
            isChecklistReturnCompleted: true,
            returnNotes
          }
        }),
        prisma.user.update({
          where: { id: loan.userId },
          data: { reputationScore: updatedScore }
        }),
        prisma.notification.create({
          data: {
            userId: loan.userId,
            title: '✅ Devolución Exitosa',
            message: `El material del folio ${loan.folioNumber} fue devuelto en tiempo y forma. Se han abonado +2 puntos a tu Trust Score (${updatedScore}/100).`
          }
        })
      ]);

      return res.json({
        success: true,
        message: 'Devolución conforme. Préstamo cerrado exitosamente y puntos de reputación abonados.'
      });
    }

    // Si HUBO incidencia: registrarla y marcar el préstamo
    await prisma.loanRequest.update({
      where: { id: loanId },
      data: {
        status: RequestStatus.FINALIZADO,
        isChecklistReturnCompleted: true,
        returnNotes: `[INCIDENCIA REPORTADA] ${returnNotes}: ${incidentDescription}`
      }
    });

    return res.json({
      success: true,
      message: 'Recepción registrada con observaciones de incidencia. Se requiere abrir el reporte correspondiente.'
    });
  } catch (error: any) {
    if (error instanceof z.ZodError) return res.status(400).json({ success: false, error: error.errors });
    return res.status(500).json({ success: false, error: error.message || 'Error al procesar devolución.' });
  }
});

// 6. Rechazar Solicitud de Préstamo con Motivo Obligatorio
loansRouter.patch('/:id/reject', authenticateJwt, requireRoles([UserRole.ALMACEN_ADMIN, UserRole.SUPERADMIN]), async (req: Request, res: Response) => {
  try {
    const loanId = req.params.id;
    const { rejectionReason } = req.body;

    if (!rejectionReason || typeof rejectionReason !== 'string' || rejectionReason.trim().length < 5) {
      return res.status(400).json({ success: false, error: 'El motivo de rechazo es obligatorio (mínimo 5 caracteres).' });
    }

    const loan = await prisma.loanRequest.update({
      where: { id: loanId },
      data: {
        status: RequestStatus.REBOTADO_CON_MOTIVO,
        rejectionReason
      },
      include: { user: true }
    });

    await prisma.notification.create({
      data: {
        userId: loan.userId,
        title: '⚠️ Solicitud de Préstamo Rechazada',
        message: `Tu solicitud ${loan.folioNumber} fue rechazada: ${rejectionReason}`
      }
    });

    return res.json({ success: true, message: 'Solicitud rechazada con motivo registrado.' });
  } catch (error: any) {
    return res.status(500).json({ success: false, error: error.message });
  }
});

// 7. Descarga del Acta PDF Oficial
loansRouter.get('/:id/pdf', authenticateJwt, async (req: Request, res: Response) => {
  try {
    const loan = await prisma.loanRequest.findUnique({ where: { id: req.params.id } });
    if (!loan || !loan.responsivaPdfPath) {
      return res.status(404).json({ success: false, error: 'Acta responsiva en PDF no disponible o aún no generada.' });
    }

    // Si está almacenada en Google Cloud Storage, generar Signed URL o redirigir
    if (loan.responsivaPdfPath.startsWith('gs://')) {
      const signedUrl = await storageService.getSignedUrl(loan.responsivaPdfPath, 30);
      return res.redirect(signedUrl);
    }

    // Soporte para archivos locales o rutas relativas
    const localPath = loan.responsivaPdfPath.startsWith('local://')
      ? path.resolve(process.cwd(), 'uploads', loan.responsivaPdfPath.replace('local://', ''))
      : loan.responsivaPdfPath;

    return res.download(localPath);
  } catch (error: any) {
    return res.status(500).json({ success: false, error: error.message });
  }
});
