import nodemailer from 'nodemailer';
import { env } from '../config/env.js';

class MailService {
  private transporter: nodemailer.Transporter | null = null;

  private async getTransporter(): Promise<nodemailer.Transporter> {
    if (this.transporter) return this.transporter;

    if (env.SMTP_USER && env.SMTP_PASS) {
      this.transporter = nodemailer.createTransport({
        host: env.SMTP_HOST || 'smtp.gmail.com',
        port: Number(env.SMTP_PORT) || 587,
        secure: Number(env.SMTP_PORT) === 465,
        auth: {
          user: env.SMTP_USER,
          pass: env.SMTP_PASS
        }
      });
    } else {
      // Usar cuenta de prueba Ethereal en desarrollo si no hay credenciales configuradas
      const testAccount = await nodemailer.createTestAccount();
      this.transporter = nodemailer.createTransport({
        host: 'smtp.ethereal.email',
        port: 587,
        secure: false,
        auth: {
          user: testAccount.user,
          pass: testAccount.pass
        }
      });
      console.log('📧 [MailService] Configurado con cuenta de prueba Ethereal:', testAccount.user);
    }
    return this.transporter;
  }

  async sendActivationEmail(to: string, fullName: string, token: string) {
    const activationLink = `${env.WEB_URL}/activar-cuenta?token=${token}`;
    const transporter = await this.getTransporter();

    const info = await transporter.sendMail({
      from: env.SMTP_FROM,
      to,
      subject: '🎓 Activa tu cuenta en SIGRE - CUTonalá',
      html: `
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #e2e8f0; border-radius: 8px;">
          <h2 style="color: #1e3a8a; text-align: center;">Bienvenido a SIGRE CUTonalá</h2>
          <p>Hola <strong>${fullName}</strong>,</p>
          <p>Has solicitado tu registro en el Sistema Integrado de Gestión de Recursos y Espacios del Centro Universitario de Tonalá.</p>
          <p>Para confirmar tu cuenta institucional y activar tu perfil, por favor haz clic en el siguiente botón:</p>
          <div style="text-align: center; margin: 30px 0;">
            <a href="${activationLink}" style="background-color: #2563eb; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; font-weight: bold;">Activar Mi Cuenta</a>
          </div>
          <p style="color: #64748b; font-size: 13px;">Si el botón no funciona, copia y pega el siguiente enlace en tu navegador:<br><a href="${activationLink}">${activationLink}</a></p>
          <hr style="border: none; border-top: 1px solid #e2e8f0; margin: 20px 0;" />
          <p style="font-size: 12px; color: #94a3b8; text-align: center;">SIGRE — CUTonalá, Universidad de Guadalajara.</p>
        </div>
      `
    });

    if (nodemailer.getTestMessageUrl(info)) {
      console.log('🔗 [Email Preview Ethereal]:', nodemailer.getTestMessageUrl(info));
    }
  }

  async sendCoResponsibleInvitation(to: string, inviterName: string, eventTitle: string, signLink: string) {
    const transporter = await this.getTransporter();
    const info = await transporter.sendMail({
      from: env.SMTP_FROM,
      to,
      subject: `📋 Invitación de Co-Responsabilidad para "${eventTitle}" - SIGRE`,
      html: `
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #e2e8f0; border-radius: 8px;">
          <h2 style="color: #1e3a8a;">Firma de Acta Responsiva Compartida</h2>
          <p><strong>${inviterName}</strong> te ha registrado como co-responsable para el evento/préstamo: <em>${eventTitle}</em>.</p>
          <p>Como co-responsable, debes revisar las normas de uso y firmar digitalmente el acta de responsiva para que la solicitud pueda ser aprobada por Almacén y Administración.</p>
          <div style="text-align: center; margin: 30px 0;">
            <a href="${signLink}" style="background-color: #059669; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; font-weight: bold;">Revisar y Firmar Responsiva</a>
          </div>
          <hr style="border: none; border-top: 1px solid #e2e8f0; margin: 20px 0;" />
          <p style="font-size: 12px; color: #94a3b8; text-align: center;">SIGRE — CUTonalá.</p>
        </div>
      `
    });

    if (nodemailer.getTestMessageUrl(info)) {
      console.log('🔗 [Email Preview Co-Responsable]:', nodemailer.getTestMessageUrl(info));
    }
  }
}

export const mailService = new MailService();
