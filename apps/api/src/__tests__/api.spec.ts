import { describe, it, expect, vi, beforeAll } from 'vitest';
import request from 'supertest';
import app from '../server.js';
import { CryptoQrService } from '../services/qr.service.js';
import { CutonalaBusinessRules } from '../utils/cutonala-rules.js';

describe('SIGRE API - Suite de Pruebas Unitarias y de Integración', () => {
  it('GET /health debe responder con status 200 y servicio identificado', async () => {
    const res = await request(app).get('/health');
    expect(res.status).toBe(200);
    expect(res.body.status).toBe('ok');
    expect(res.body.service).toContain('SIGRE');
    expect(res.body.timestamp).toBeDefined();
  });

  it('GET /api y GET /api/v1 deben responder con la información del catálogo de rutas', async () => {
    const resV1 = await request(app).get('/api/v1');
    expect(resV1.status).toBe(200);
    expect(resV1.body.name).toBe('SIGRE API');
    expect(resV1.body.institution).toContain('Tonalá');
    expect(resV1.body.endpoints).toBeDefined();

    const resBase = await request(app).get('/api');
    expect(resBase.status).toBe(200);
    expect(resBase.body.name).toBe('SIGRE API');
  });

  it('CryptoQrService debe firmar y validar tokens de boletos QR criptográficamente', () => {
    const payload = {
      ticketId: 'test-ticket-001',
      eventId: '11111111-2222-3333-4444-555555555555',
      userId: '66666666-7777-8888-9999-000000000000',
      studentCode: '219482910'
    };

    const token = CryptoQrService.generateTicketToken(payload);
    expect(typeof token).toBe('string');
    expect(token.length).toBeGreaterThan(30);

    const decoded = CryptoQrService.verifyTicketToken(token);
    expect(decoded.ticketId).toBe(payload.ticketId);
    expect(decoded.eventId).toBe(payload.eventId);
    expect(decoded.userId).toBe(payload.userId);
    expect(decoded.studentCode).toBe(payload.studentCode);
  });

  it('CryptoQrService: debe generar dataUrl en formato base64 para renderizado offline', async () => {
    const dataUrl = await CryptoQrService.generateQrDataUrl('SIGRE-TICKET-OFFLINE-TEST-12345');
    expect(typeof dataUrl).toBe('string');
    expect(dataUrl.startsWith('data:image/png;base64,')).toBe(true);
  });

  it('CutonalaBusinessRules: debe validar horario de operación (08:00 a 19:00 hrs)', () => {
    // Horario válido: Jueves 10:00 a 12:00 local
    const validStart = new Date(2026, 10, 5, 10, 0, 0);
    const validEnd = new Date(2026, 10, 5, 12, 0, 0);
    const validCheck = CutonalaBusinessRules.validateOperatingHours(validStart, validEnd);
    expect(validCheck.valid).toBe(true);

    // Horario inválido: 22:00 a 23:00 (fuera de horario de campus)
    const invalidStart = new Date(2026, 10, 5, 22, 0, 0);
    const invalidEnd = new Date(2026, 10, 5, 23, 0, 0);
    const invalidCheck = CutonalaBusinessRules.validateOperatingHours(invalidStart, invalidEnd);
    expect(invalidCheck.valid).toBe(false);
  });

  it('CutonalaBusinessRules: debe validar límite de duración (ordinario máx 3 días)', () => {
    const start = new Date('2026-11-05T10:00:00Z');
    
    // 2 días -> Válido
    const end2Days = new Date('2026-11-07T10:00:00Z');
    const check2Days = CutonalaBusinessRules.validateLoanDuration(start, end2Days, false);
    expect(check2Days.valid).toBe(true);

    // 5 días sin justificación extendida -> Inválido
    const end5Days = new Date('2026-11-10T10:00:00Z');
    const check5Days = CutonalaBusinessRules.validateLoanDuration(start, end5Days, false);
    expect(check5Days.valid).toBe(false);

    // 15 días con justificación extendida -> Válido (hasta 30 días)
    const end15Days = new Date('2026-11-20T10:00:00Z');
    const check15Days = CutonalaBusinessRules.validateLoanDuration(start, end15Days, true);
    expect(check15Days.valid).toBe(true);
  });

  it('Seguridad HTTP: Helmet debe configurar cabeceras de protección', async () => {
    const res = await request(app).get('/health');
    expect(res.headers['x-dns-prefetch-control']).toBe('off');
    expect(res.headers['x-frame-options']).toBe('SAMEORIGIN');
    expect(res.headers['strict-transport-security']).toBeDefined();
    expect(res.headers['x-download-options']).toBe('noopen');
    expect(res.headers['x-content-type-options']).toBe('nosniff');
  });
});
