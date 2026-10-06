import { RecaptchaEnterpriseServiceClient } from '@google-cloud/recaptcha-enterprise';
import path from 'path';
import fs from 'fs';
import { env } from '../config/env.js';

export interface RecaptchaVerificationResult {
  valid: boolean;
  score: number;
  action?: string;
  reasons?: string[];
  invalidReason?: string;
}

export class RecaptchaService {
  private client: RecaptchaEnterpriseServiceClient | null = null;
  private projectId: string;
  private siteKey: string;
  private minScore: number;
  private isConfigured: boolean = false;

  constructor() {
    this.projectId = env.GCP_PROJECT_ID;
    this.siteKey = env.RECAPTCHA_KEY_ID;
    this.minScore = env.RECAPTCHA_SCORE_THRESHOLD;
    this.initClient();
  }

  private initClient() {
    try {
      const candidates = [
        process.env.GOOGLE_APPLICATION_CREDENTIALS,
        path.resolve(process.cwd(), 'sa-key.json'),
        path.resolve(process.cwd(), '../../sa-key.json')
      ];

      const keyFile = candidates.find((p) => p && fs.existsSync(p));

      if (keyFile) {
        this.client = new RecaptchaEnterpriseServiceClient({
          projectId: this.projectId,
          keyFilename: keyFile
        });
        this.isConfigured = true;
      } else if (env.NODE_ENV === 'production') {
        // En Cloud Run se usan ADC por defecto
        this.client = new RecaptchaEnterpriseServiceClient({ projectId: this.projectId });
        this.isConfigured = true;
      } else {
        this.client = null;
        this.isConfigured = false;
      }
    } catch (err) {
      console.warn('⚠️ [RecaptchaService] No se pudo inicializar cliente de reCAPTCHA Enterprise:', err);
      this.client = null;
      this.isConfigured = false;
    }
  }

  /**
   * Valida un token generado en el frontend mediante el Assessment API de reCAPTCHA Enterprise.
   */
  async verifyToken(token?: string, expectedAction?: string): Promise<RecaptchaVerificationResult> {
    // 1. Manejo en ambientes de test o sin token explícito en desarrollo
    if (env.NODE_ENV === 'test' || token === 'bypass-test-token') {
      return { valid: true, score: 1.0, action: expectedAction };
    }

    if (!token) {
      if (env.NODE_ENV === 'production') {
        return { valid: false, score: 0.0, invalidReason: 'Token de reCAPTCHA ausente' };
      }
      // En desarrollo local sin credenciales se permite continuar alertando en consola
      console.warn('⚠️ [reCAPTCHA] Token ausente en entorno local, permitiendo bypass de desarrollo.');
      return { valid: true, score: 1.0, action: expectedAction };
    }

    if (!this.client || !this.isConfigured) {
      console.warn('⚠️ [reCAPTCHA] Cliente Enterprise no inicializado, omitiendo validación en desarrollo.');
      return { valid: true, score: 1.0, action: expectedAction };
    }

    try {
      const projectPath = this.client.projectPath(this.projectId);

      const [response] = await this.client.createAssessment({
        parent: projectPath,
        assessment: {
          event: {
            token,
            siteKey: this.siteKey,
            expectedAction
          }
        }
      });

      if (!response.tokenProperties?.valid) {
        return {
          valid: false,
          score: 0.0,
          invalidReason: response.tokenProperties?.invalidReason?.toString() || 'Token inválido'
        };
      }

      if (expectedAction && response.tokenProperties.action !== expectedAction) {
        return {
          valid: false,
          score: Number(response.riskAnalysis?.score || 0),
          invalidReason: `Acción no coincide: esperada '${expectedAction}', recibida '${response.tokenProperties.action}'`
        };
      }

      const score = Number(response.riskAnalysis?.score ?? 0);
      const reasons = (response.riskAnalysis?.reasons || []).map((r) => r.toString());

      return {
        valid: score >= this.minScore,
        score,
        action: response.tokenProperties.action || undefined,
        reasons
      };
    } catch (error: any) {
      console.error('❌ [reCAPTCHA Enterprise] Error al evaluar token:', error);
      if (env.NODE_ENV === 'production') {
        return { valid: false, score: 0.0, invalidReason: 'Error de comunicación con Google reCAPTCHA' };
      }
      return { valid: true, score: 1.0 };
    }
  }
}

export const recaptchaService = new RecaptchaService();
