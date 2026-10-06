import { Router, Request, Response } from 'express';
import argon2 from 'argon2';
import crypto from 'crypto';
import jwt from 'jsonwebtoken';
import { z } from 'zod';
import { prisma } from '@inversion/database';
import { env } from '../config/env.js';
import { mailService } from '../services/mail.service.js';
import { recaptchaService } from '../services/recaptcha.service.js';
import { authenticateJwt, AuthPayload } from '../middlewares/auth.middleware.js';
import { UserRole, UserStatus } from '@inversion/shared-types';

export const authRouter = Router();

const registerSchema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
  fullName: z.string().min(3),
  studentCode: z.string().min(6),
  career: z.string().optional(),
  semester: z.number().int().min(1).max(12).optional(),
  role: z.nativeEnum(UserRole).default(UserRole.ESTUDIANTE),
  recaptchaToken: z.string().optional()
});

const loginSchema = z.object({
  email: z.string().email(),
  password: z.string(),
  recaptchaToken: z.string().optional()
});

// 1. Registro tradicional con correo institucional
authRouter.post('/register', async (req: Request, res: Response) => {
  try {
    const data = registerSchema.parse(req.body);

    const recaptcha = await recaptchaService.verifyToken(data.recaptchaToken, 'REGISTER');
    if (!recaptcha.valid) {
      return res.status(400).json({ error: `Validación de seguridad reCAPTCHA Enterprise fallida: ${recaptcha.invalidReason || 'Score de riesgo bajo'}` });
    }

    const existing = await prisma.user.findFirst({
      where: {
        OR: [{ email: data.email }, { studentCode: data.studentCode }]
      }
    });

    if (existing) {
      return res.status(400).json({ error: 'El correo electrónico o código ya se encuentran registrados.' });
    }

    const passwordHash = await argon2.hash(data.password);
    const user = await prisma.user.create({
      data: {
        email: data.email,
        passwordHash,
        fullName: data.fullName,
        studentCode: data.studentCode,
        career: data.career,
        semester: data.semester,
        role: data.role,
        status: UserStatus.PENDIENTE_ACTIVACION
      }
    });

    // Generar token de activación seguro
    const tokenString = crypto.randomBytes(32).toString('hex');
    await prisma.activationToken.create({
      data: {
        token: tokenString,
        userId: user.id,
        expiresAt: new Date(Date.now() + 24 * 60 * 60 * 1000) // 24 horas
      }
    });

    // Enviar correo de activación
    await mailService.sendActivationEmail(user.email, user.fullName, tokenString);

    return res.status(201).json({
      message: 'Usuario registrado exitosamente. Por favor verifica tu correo para activar tu cuenta.',
      userId: user.id
    });
  } catch (error: any) {
    if (error instanceof z.ZodError) {
      return res.status(400).json({ error: error.errors });
    }
    return res.status(500).json({ error: error.message || 'Error interno en el registro.' });
  }
});

// 2. Activación de cuenta por enlace
authRouter.get('/activate', async (req: Request, res: Response) => {
  const { token } = req.query;
  if (!token || typeof token !== 'string') {
    return res.status(400).json({ error: 'Token de activación requerido.' });
  }

  const record = await prisma.activationToken.findUnique({
    where: { token },
    include: { user: true }
  });

  if (!record || record.expiresAt < new Date()) {
    return res.status(400).json({ error: 'Token de activación inválido o expirado.' });
  }

  await prisma.user.update({
    where: { id: record.userId },
    data: { status: UserStatus.ACTIVO }
  });

  await prisma.activationToken.delete({ where: { id: record.id } });

  return res.json({ message: 'Cuenta activada exitosamente. Ya puedes iniciar sesión.' });
});

// 3. Inicio de sesión tradicional
authRouter.post('/login', async (req: Request, res: Response) => {
  try {
    const { email, password, recaptchaToken } = loginSchema.parse(req.body);

    const recaptcha = await recaptchaService.verifyToken(recaptchaToken, 'LOGIN');
    if (!recaptcha.valid) {
      return res.status(400).json({ error: `Validación de seguridad reCAPTCHA Enterprise fallida: ${recaptcha.invalidReason || 'Score de riesgo bajo'}` });
    }

    const user = await prisma.user.findUnique({ where: { email } });
    if (!user || !user.passwordHash) {
      return res.status(401).json({ error: 'Credenciales inválidas.' });
    }

    if (user.status === UserStatus.PENDIENTE_ACTIVACION) {
      return res.status(403).json({ error: 'Tu cuenta aún no está activada. Revisa tu correo institucional.' });
    }

    if (user.status === UserStatus.SUSPENDIDO) {
      return res.status(403).json({ error: 'Tu cuenta ha sido suspendida. Contacta a la administración.' });
    }

    const isValid = await argon2.verify(user.passwordHash, password);
    if (!isValid) {
      return res.status(401).json({ error: 'Credenciales inválidas.' });
    }

    const payload: AuthPayload = {
      userId: user.id,
      email: user.email,
      role: user.role as UserRole,
      studentCode: user.studentCode
    };

    const accessToken = jwt.sign(payload, env.JWT_ACCESS_SECRET, { expiresIn: '15m' });
    const refreshToken = jwt.sign({ userId: user.id }, env.JWT_REFRESH_SECRET, { expiresIn: '7d' });

    res.cookie('accessToken', accessToken, { httpOnly: true, secure: env.NODE_ENV === 'production' });
    res.cookie('refreshToken', refreshToken, { httpOnly: true, secure: env.NODE_ENV === 'production' });

    return res.json({
      message: 'Inicio de sesión exitoso',
      accessToken,
      user: {
        id: user.id,
        email: user.email,
        fullName: user.fullName,
        studentCode: user.studentCode,
        role: user.role,
        reputationScore: user.reputationScore
      }
    });
  } catch (error: any) {
    if (error instanceof z.ZodError) return res.status(400).json({ error: error.errors });
    return res.status(500).json({ error: 'Error al iniciar sesión.' });
  }
});

// 4. Obtener perfil de usuario logueado
authRouter.get('/me', authenticateJwt, async (req: Request, res: Response) => {
  const user = await prisma.user.findUnique({
    where: { id: req.user!.userId },
    select: {
      id: true,
      email: true,
      fullName: true,
      studentCode: true,
      career: true,
      semester: true,
      role: true,
      status: true,
      reputationScore: true,
      signatureUrl: true,
      createdAt: true
    }
  });

  if (!user) return res.status(404).json({ error: 'Usuario no encontrado.' });
  return res.json(user);
});
