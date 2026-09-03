import jwt from 'jsonwebtoken';
import QRCode from 'qrcode';
import { env } from '../config/env.js';

export interface QRPayloadData {
  ticketId: string;
  eventId: string;
  userId: string;
  studentCode: string;
}

export class CryptoQrService {
  /**
   * Genera un token criptográfico firmado para el código QR del boleto
   */
  static generateTicketToken(data: QRPayloadData): string {
    return jwt.sign(data, env.JWT_ACCESS_SECRET, {
      expiresIn: '30d',
      algorithm: 'HS256'
    });
  }

  /**
   * Verifica el token leído del QR al escanear en la puerta del evento
   */
  static verifyTicketToken(token: string): QRPayloadData {
    return jwt.verify(token, env.JWT_ACCESS_SECRET) as QRPayloadData;
  }

  /**
   * Genera la imagen en DataURL base64 del código QR para mostrar en la interfaz web o boleto
   */
  static async generateQrDataUrl(qrToken: string): Promise<string> {
    return QRCode.toDataURL(qrToken, {
      errorCorrectionLevel: 'M',
      margin: 2,
      width: 280,
      color: {
        dark: '#1e293b',
        light: '#ffffff'
      }
    });
  }
}
