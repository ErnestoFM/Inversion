import { Router, Request, Response } from 'express';
import { z } from 'zod';
import path from 'path';
import { prisma } from '@inversion/database';
import { authenticateJwt, requireRoles } from '../middlewares/auth.middleware.js';
import { PdfService } from '../services/pdf.service.js';
import { mailService } from '../services/mail.service.js';
import { UserRole, RequestStatus, ItemStatus } from '@inversion/shared-types';

export const loansRouter = Router();

const createLoanSchema = z.object({
  spaceId: z.string().optional(),
  itemIds: z.array(z.string()).default([]),
  purpose: z.string().min(5),
  startTime: z.string().datetime(),
  endTime: z.string().datetime(),
  coResponsibleStudentCodes: z.array(z.string()).default([]),
  signatureBase64: z.string().min(20) // Firma digital
});

// 1. Crear Solicitud de Préstamo con Firma y Pre-reserva
loansRouter.post('/', authenticateJwt, async (req: Request, res: Response) => {
  try {
    const data = createLoanSchema.parse(req.body);
    const userId = req.user!.userId;
    const ipAddress = req.ip || req.socket.remoteAddress || '127.0.0.1';

    // Generar Folio Único
    const year = new Date().getFullYear();
    const count = await prisma.loanRequest.count();
    const folioNumber = `RESP-${year}-${String(count + 1).padStart(4, '0')}`;

    // Validar co-responsables si existen
    const coResponsibleUsers = await prisma.user.findMany({
      where: { studentCode: { in: data.coResponsibleStudentCodes } }
    });

    const loan = await prisma.loanRequest.create({
      data: {
        folioNumber,
        userId,
        spaceId: data.spaceId,
        purpose: data.purpose,
        startTime: new Date(data.startTime),
        endTime: new Date(data.endTime),
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

    // Registrar co-responsables y enviarles invitación por correo
    for (const cr of coResponsibleUsers) {
      if (cr.id !== userId) {
        await prisma.eventCoResponsible.create({
          data: { userId: cr.id, hasSigned: false }
        });
        await mailService.sendCoResponsibleInvitation(
          cr.email,
          req.user!.studentCode,
          data.purpose,
          `http://localhost:3000/responsivas/${loan.id}/firmar`
        );
      }
    }

    return res.status(201).json({
      message: 'Solicitud de préstamo y acta preliminar registradas con éxito.',
      folioNumber,
      loanId: loan.id
    });
  } catch (error: any) {
    if (error instanceof z.ZodError) return res.status(400).json({ error: error.errors });
    return res.status(500).json({ error: error.message || 'Error al procesar la solicitud.' });
  }
});

// 2. Aprobación Administrativa con Generación de PDF Oficial
loansRouter.post('/:id/approve', authenticateJwt, requireRoles([UserRole.ALMACEN_ADMIN, UserRole.SUPERADMIN]), async (req: Request, res: Response) => {
  try {
    const loanId = req.params.id;
    const { approverSignatureBase64 } = req.body;

    const loan = await prisma.loanRequest.findUnique({
      where: { id: loanId },
      include: {
        user: true,
        space: true,
        items: { include: { item: true } }
      }
    });

    if (!loan) return res.status(404).json({ error: 'Solicitud no encontrada.' });

    // Actualizar estado de materiales a PRESTADO
    for (const item of loan.items) {
      await prisma.inventoryItem.update({
        where: { id: item.itemId },
        data: { status: ItemStatus.PRESTADO }
      });
    }

    // Generar archivo PDF oficial
    const outputDir = path.resolve(process.cwd(), 'uploads/actas');
    const pdfPath = await PdfService.generateResponsivaPdf(
      {
        folioNumber: loan.folioNumber,
        createdAt: loan.createdAt.toISOString(),
        userName: loan.user.fullName,
        studentCode: loan.user.studentCode,
        career: loan.user.career || 'Estudiante UdeG',
        purpose: loan.purpose,
        spaceName: loan.space?.name,
        items: loan.items.map((i) => ({
          name: i.item.name,
          assetTag: i.item.assetTag,
          serialNumber: i.item.serialNumber
        })),
        coResponsibles: [],
        approverName: req.user!.studentCode,
        ipAddress: loan.ipAddress || '127.0.0.1'
      },
      outputDir
    );

    const updated = await prisma.loanRequest.update({
      where: { id: loanId },
      data: {
        status: RequestStatus.APROBADO,
        approverSignatureUrl: approverSignatureBase64,
        responsivaPdfPath: pdfPath
      }
    });

    return res.json({
      message: '✅ Solicitud Aprobada y Acta Oficial en PDF generada exitosamente.',
      folioNumber: updated.folioNumber,
      pdfUrl: `/api/v1/loans/${loanId}/pdf`
    });
  } catch (error: any) {
    return res.status(500).json({ error: error.message || 'Error al autorizar el préstamo.' });
  }
});

// 3. Descarga del Acta PDF Oficial
loansRouter.get('/:id/pdf', authenticateJwt, async (req: Request, res: Response) => {
  const loan = await prisma.loanRequest.findUnique({ where: { id: req.params.id } });
  if (!loan || !loan.responsivaPdfPath) {
    return res.status(404).json({ error: 'Acta responsiva en PDF no disponible o aún no generada.' });
  }
  return res.download(loan.responsivaPdfPath);
});
