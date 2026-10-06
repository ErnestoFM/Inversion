import { test, expect, Page } from '@playwright/test';
import {
  mockUserStudent,
  mockSpaces,
  mockResources,
  mockScreenings,
  mockLoans,
  mockBookings,
  mockIncidents,
  mockDashboardStats,
} from './mockData';

// Interceptor exhaustivo de API para pruebas E2E deterministas
async function setupApiMocks(page: Page) {
  await page.route(
    (url) => url.pathname.startsWith('/api/'),
    async (route) => {
      const request = route.request();
      const url = new URL(request.url());
      const path = url.pathname;
      const method = request.method();

    // 1. Autenticación
    if (path.includes('/auth/login') && method === 'POST') {
      return route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          token: 'mock-jwt-token-ey123456789',
          user: mockUserStudent,
        }),
      });
    }

    if (path.includes('/auth/me')) {
      return route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({ user: mockUserStudent }),
      });
    }

    // 2. Espacios Físicos
    if (path.includes('/spaces/my-bookings')) {
      return route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({ reservas: mockBookings }),
      });
    }

    if (path.includes('/spaces') && path.includes('/availability')) {
      return route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          espacioId: 'sp-auditorio',
          fecha: '2026-10-12',
          horarioDisponible: true,
          reservas: [],
        }),
      });
    }

    if (path.includes('/spaces') && path.includes('/lock') && method === 'POST') {
      return route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          mensaje: 'Bloqueo temporal de 15 min adquirido en Redis.',
          expiraEnSegundos: 900,
        }),
      });
    }

    if (path.includes('/spaces/book') && method === 'POST') {
      return route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          reserva: mockBookings[0],
          mensaje: 'Solicitud de espacio creada con éxito.',
        }),
      });
    }

    if (path.includes('/spaces') && method === 'GET') {
      return route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({ espacios: mockSpaces }),
      });
    }

    // 3. Recursos & Inventario
    if (path.includes('/resources') && method === 'GET') {
      return route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({ recursos: mockResources }),
      });
    }

    // 4. Cartelera Cineteca & Boletos QR
    if (path.includes('/events/screenings') && path.includes('/ticket') && method === 'POST') {
      return route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          boleto: {
            id: 'tkt-1',
            folioBoleto: 'TKT-2026-7841',
            asientoAsignado: 'B-14',
            created_at: new Date().toISOString(),
          },
          qrCodeDataUrl: 'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="120" height="120"><rect width="120" height="120" fill="black"/></svg>',
          mensaje: 'Boleto apartado exitosamente',
        }),
      });
    }

    if (path.includes('/events/screenings')) {
      return route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({ funciones: mockScreenings }),
      });
    }

    if (path.includes('/events/my-tickets')) {
      return route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          boletos: [
            {
              id: 'tkt-mine-1',
              folioBoleto: 'TKT-2026-7841',
              asientoAsignado: 'B-14',
              proyeccion: mockScreenings[0],
            },
          ],
        }),
      });
    }

    // 5. Préstamos de Material & Responsivas
    if (path.includes('/loans/request') && method === 'POST') {
      return route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          prestamo: mockLoans[1],
          mensaje: 'Préstamo solicitado con responsiva firmada.',
        }),
      });
    }

    if (path.includes('/loans/my-loans')) {
      return route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({ prestamos: mockLoans }),
      });
    }

    if (path.includes('/loans') && method === 'GET') {
      return route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({ prestamos: mockLoans }),
      });
    }

    // 6. Incidentes & Sanciones
    if (path.includes('/incidents') && method === 'POST') {
      return route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          incidente: mockIncidents[0],
          penalizacionAplicada: 5,
          nuevoScore: 95,
        }),
      });
    }

    if (path.includes('/incidents') && method === 'GET') {
      return route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({ incidentes: mockIncidents }),
      });
    }

    // 7. Notificaciones
    if (path.includes('/notifications')) {
      return route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          notificaciones: [
            {
              id: 'notif-1',
              titulo: 'Reserva Aprobada',
              mensaje: 'Tu reserva para el Auditorio Principal ha sido autorizada.',
              tipo: 'RESERVA_APROBADA',
              leido: false,
              created_at: new Date().toISOString(),
            },
          ],
          totalNoLeidas: 1,
        }),
      });
    }

    // 8. Dashboard
    if (path.includes('/dashboard/stats')) {
      return route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify(mockDashboardStats),
      });
    }

    return route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({ ok: true }),
    });
  });
}

test.describe('Suite E2E Playwright: SIGRE CUTonalá (Etapa 2)', () => {
  test.beforeEach(async ({ page }) => {
    await setupApiMocks(page);
    await page.goto('/');
  });

  test('1. Identidad Institucional, Reloj y Conmutación Dark Mode', async ({ page }) => {
    // Encabezado institucional UdeG / CUTonalá
    await expect(page.locator('.logo-sigre')).toHaveText('SIGRE');
    await expect(page.locator('.logo-udg')).toHaveText('UdeG');
    await expect(page.locator('.campus-sub')).toHaveText('Centro Universitario de Tonalá');
    await expect(page.locator('.status-text')).toContainText('Horario CUTonalá');

    // Pie de página institucional
    await expect(page.locator('.footer-desc')).toContainText('Universidad de Guadalajara');

    // Botón de alternancia de tema (Sun / Moon)
    const themeBtn = page.locator('button[aria-label="Alternar tema"]');
    await expect(themeBtn).toBeVisible();

    const html = page.locator('html');
    const initialTheme = await html.getAttribute('data-theme');

    await themeBtn.click();
    const updatedTheme = await html.getAttribute('data-theme');
    expect(updatedTheme).not.toBe(initialTheme);

    // Regresar al tema original
    await themeBtn.click();

    // Captura de pantalla oficial
    await page.screenshot({ path: 'docs/pruebas/screenshots/01_identidad_institucional.png' });
  });

  test('2. Autenticación Rápida Institucional y Badge de Alumno', async ({ page }) => {
    // Banner de acceso de prueba en modo invitado
    const demoStudentBtn = page.locator('button:has-text("Ernesto Fierro (Alumno)")');
    await expect(demoStudentBtn).toBeVisible();

    // Iniciar sesión con un clic
    await demoStudentBtn.click();

    // Verificar datos de sesión en Header (Primer nombre y badge de reputación)
    await expect(page.locator('.user-name')).toHaveText('Ernesto');
    await expect(page.locator('.user-trust-tag')).toContainText('100/100 pts');

    // Abrir menú de usuario para verificar carrera y código
    await page.locator('.user-profile-btn').click();
    await expect(page.locator('.dropdown-user-header strong')).toHaveText('Ernesto Hatuey Fierro Meléndez');
    await expect(page.locator('.dropdown-user-header .badge')).toContainText('Rol: ESTUDIANTE');

    await page.screenshot({ path: 'docs/pruebas/screenshots/02_sesion_alumno.png' });
  });

  test('3. Cartelera Cineteca & Reserva de Asiento con Código QR', async ({ page }) => {
    // Login inicial
    await page.locator('button:has-text("Ernesto Fierro (Alumno)")').click();
    await expect(page.locator('.user-name')).toHaveText('Ernesto');

    // Pestaña Cartelera Cineteca
    await page.locator('nav button:has-text("Cartelera Cineteca")').click();

    // Verificar tarjeta de función de Macario
    await expect(page.locator('.billboard-title')).toHaveText('Macario (1960) — Versión Restaurada 4K');
    await expect(page.locator('.billboard-synopsis')).toContainText('campesino');

    // Reservar Asiento QR
    const bookTicketBtn = page.locator('button:has-text("Reservar Asiento QR")').first();
    await expect(bookTicketBtn).toBeVisible();
    await bookTicketBtn.click();

    // Verificar modal con boleto digital y QR
    await expect(page.locator('.modal-title')).toHaveText('¡Boleto Digital Confirmado!');
    await expect(page.locator('.ticket-card')).toContainText('Folio: TKT-2026-7841');
    await expect(page.locator('.ticket-qr-img')).toBeVisible();

    await page.screenshot({ path: 'docs/pruebas/screenshots/03_boleto_qr_cineteca.png' });

    // Cerrar boleto digital
    await page.locator('button:has-text("Listo, guardar en Mis Solicitudes")').click();
  });

  test('4. Catálogo de Espacios, Filtros y Soft Lock de 15 Min en Redis', async ({ page }) => {
    await page.locator('button:has-text("Ernesto Fierro (Alumno)")').click();

    // Pestaña Espacios & Aulas
    await page.locator('nav button:has-text("Espacios & Aulas")').click();

    // Verificar catálogo
    await expect(page.locator('text=Auditorio Principal CUTonalá')).toBeVisible();
    await expect(page.locator('text=Laboratorio de Inteligencia Artificial')).toBeVisible();

    // Abrir modal de reserva en Auditorio Principal
    await page.locator('.space-card:has-text("Auditorio Principal") button:has-text("Solicitar Reserva")').click();

    // Verificar botón de Soft Lock Redis
    const lockBtn = page.locator('button:has-text("Apartar cupo 15 min")');
    await expect(lockBtn).toBeVisible();
    await lockBtn.click();

    // Verificar que el bloqueo en Redis entra en vigencia
    await expect(page.locator('text=Bloqueo Temporal en Redis Activo')).toBeVisible();

    await page.screenshot({ path: 'docs/pruebas/screenshots/04_soft_lock_redis.png' });

    // Completar justificación y enviar
    await page.locator('textarea.input-text').fill('Seminario Académico de Inteligencia Artificial y Finanzas');
    await page.locator('button:has-text("Confirmar Solicitud")').click();

    // Verificar mensaje de confirmación y folio
    await expect(page.locator('text=¡Solicitud Registrada con Éxito!')).toBeVisible();
    await expect(page.locator('text=SOL-ESP-2026-0012')).toBeVisible();

    await page.screenshot({ path: 'docs/pruebas/screenshots/04_reserva_confirmada.png' });
  });

  test('5. Inventario de Materiales y Firma Digital en Canvas HTML5', async ({ page }) => {
    await page.locator('button:has-text("Ernesto Fierro (Alumno)")').click();

    // Pestaña Inventario & Préstamos
    await page.locator('nav button:has-text("Inventario & Préstamos")').click();

    // Verificar equipo disponible
    await expect(page.locator('text=Laptop Lenovo ThinkPad T14')).toBeVisible();

    // Abrir modal de solicitud
    await page.locator('.resource-card:has-text("ThinkPad") button:has-text("Solicitar Préstamo")').click();

    // Activar préstamo extendido
    const extendCheckbox = page.locator('input[type="checkbox"]').first();
    await extendCheckbox.check();
    await page.locator('textarea[placeholder*="investigación"]').fill('Investigación de modelos de inversión');

    // Abrir Canvas de Firma Digital
    await page.locator('button:has-text("Firmar Ahora")').click();

    // Simular trazo en el elemento Canvas HTML5
    const canvas = page.locator('canvas.signature-canvas');
    await expect(canvas).toBeVisible();
    const box = await canvas.boundingBox();
    if (box) {
      await page.mouse.move(box.x + 30, box.y + 30);
      await page.mouse.down();
      await page.mouse.move(box.x + 80, box.y + 50);
      await page.mouse.move(box.x + 130, box.y + 20);
      await page.mouse.move(box.x + 190, box.y + 60);
      await page.mouse.up();
    }

    await page.screenshot({ path: 'docs/pruebas/screenshots/05_canvas_firma_digital.png' });

    // Estampar firma
    await page.locator('button:has-text("Estampar Firma y Aceptar")').click();

    // Verificar estado de firma lista
    await expect(page.locator('text=Firma electrónica lista para estampar en el acta PDF.')).toBeVisible();

    // Enviar solicitud con responsiva
    await page.locator('button:has-text("Confirmar y Generar Responsiva")').click();

    // Verificar resultado
    await expect(page.locator('text=¡Préstamo Solicitado con Éxito!')).toBeVisible();
    await expect(page.locator('text=PREST-2026-0089')).toBeVisible();

    await page.screenshot({ path: 'docs/pruebas/screenshots/05_prestamo_creado.png' });
  });

  test('6. Mis Solicitudes, Responsivas y Checklists de Entrega', async ({ page }) => {
    await page.locator('button:has-text("Ernesto Fierro (Alumno)")').click();

    // Pestaña Mis Solicitudes
    await page.locator('nav button:has-text("Mis Solicitudes & Responsivas")').click();

    // Verificar préstamos
    await expect(page.locator('text=PREST-2026-0041')).toBeVisible();
    await expect(page.locator('text=PREST-2026-0089')).toBeVisible();

    // Cambiar a subpestaña de Reservas
    await page.locator('button:has-text("Reservas de Espacios")').click();
    await expect(page.locator('text=SOL-ESP-2026-0012')).toBeVisible();

    // Cambiar a subpestaña de Boletos Cineteca
    await page.locator('button:has-text("Boletos Cineteca")').click();
    await expect(page.locator('text=TKT-2026-7841')).toBeVisible();

    await page.screenshot({ path: 'docs/pruebas/screenshots/06_solicitudes_responsivas.png' });
  });

  test('7. Incidentes, Sanciones y Política de Trust Score', async ({ page }) => {
    await page.locator('button:has-text("Ernesto Fierro (Alumno)")').click();

    // Pestaña Incidentes
    await page.locator('nav button:has-text("Incidentes & Reparaciones")').click();

    // Verificar banner de política
    await expect(page.locator('.trust-score-banner')).toContainText('Política de Confianza y Sanciones de CUTonalá');

    // Verificar tabla de incidentes
    await expect(page.locator('text=INC-2026-0003')).toBeVisible();
    await expect(page.locator('text=Leve (-5 pts)')).toBeVisible();

    await page.screenshot({ path: 'docs/pruebas/screenshots/07_incidentes_trust_score.png' });
  });

  test('8. Panel de Control Ejecutivo, Métrica Operativa y Matriz de Desgaste', async ({ page }) => {
    await page.locator('button:has-text("Ernesto Fierro (Alumno)")').click();

    // Pestaña Panel de Control
    await page.locator('nav button:has-text("Panel de Control")').click();

    // Verificar las 6 métricas KPI
    await expect(page.locator('text=Espacios Físicos')).toBeVisible();
    await expect(page.locator('text=Bienes de Inventario')).toBeVisible();
    await expect(page.locator('text=Reservas Aprobadas')).toBeVisible();
    await expect(page.locator('text=Préstamos en Curso')).toBeVisible();
    await expect(page.locator('text=Por Autorizar')).toBeVisible();
    await expect(page.locator('text=Incidentes Abiertos')).toBeVisible();

    // Verificar Matriz de Desgaste de Flota
    await expect(page.locator('text=Matriz de Desgaste de Flota y Riesgo Predictivo de Falla')).toBeVisible();
    await expect(page.locator('text=Laptop ThinkPad T14 Gen 3')).toBeVisible();

    await page.screenshot({ path: 'docs/pruebas/screenshots/08_dashboard_ejecutivo.png' });
  });
});
