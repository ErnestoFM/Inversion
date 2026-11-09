# Estrategia de Pruebas E2E — SIGRE CUTonalá

Este directorio contiene la documentación, configuración y evidencias visuales de las pruebas automatizadas del proyecto **SIGRE (Sistema Integrado de Gestión de Recursos y Espacios — CUTonalá)**.

---

## 🎭 Suite End-to-End con Playwright

Las pruebas automatizadas de extremo a extremo (E2E) están implementadas con **Playwright Test** y cubren los flujos de usuario completos correspondientes a la **Etapa 2 (Frontend React 18 + Vite)**.

### Archivos de la Suite:
- `playwright.config.ts`: Configuración global de Playwright para el monorepo (Chromium, reporter HTML y list, webServer automático).
- `tests/e2e/sigre.spec.ts`: Especificación de las 8 pruebas integrales.
- `tests/e2e/mockData.ts`: Modelado institucional de datos de prueba para CUTonalá (estudiantes, docentes, espacios, recursos, cineteca y métricas).
- `docs/pruebas/screenshots/`: Capturas de pantalla generadas automáticamente durante la ejecución de las pruebas.

---

## 🧪 Cobertura de los 8 Escenarios de Prueba

| # | Escenario de Prueba | Componente / Flujo Validado | Evidencia | Resultado |
| :-: | :--- | :--- | :--- | :-: |
| **1** | **Identidad Institucional y Dark Mode** | Logos UdeG/SIGRE, reloj en vivo CUTonalá, pie de página LGPDPPSO y conmutación de tema (Light/Dark). | `screenshots/01_identidad_institucional.png` | ✅ **PASS** (1.9s) |
| **2** | **Autenticación Rápida Institucional** | Acceso de prueba de alumno (Ernesto Fierro), verificación de reputación (100/100 pts) y menú de perfil. | `screenshots/02_sesion_alumno.png` | ✅ **PASS** (1.4s) |
| **3** | **Cartelera Cineteca & Boleto QR** | Función *Macario (1960)*, reserva de butaca y emisión de boleto digital con código QR dinámico. | `screenshots/03_boleto_qr_cineteca.png` | ✅ **PASS** (1.4s) |
| **4** | **Espacios & Soft Lock en Redis** | Catálogo de auditorios/aulas, adquisición de bloqueo temporal de 15 minutos en Redis y confirmación de reserva. | `screenshots/04_soft_lock_redis.png`<br>`screenshots/04_reserva_confirmada.png` | ✅ **PASS** (3.3s) |
| **5** | **Inventario y Firma Digital Canvas** | Solicitud de préstamo extendido, trazo de firma electrónica en Canvas HTML5 y emisión de responsiva. | `screenshots/05_canvas_firma_digital.png`<br>`screenshots/05_prestamo_creado.png` | ✅ **PASS** (3.6s) |
| **6** | **Mis Solicitudes y Responsivas** | Historial de préstamos de material, reservas de espacio y visualización de boletos de Cineteca. | `screenshots/06_solicitudes_responsivas.png` | ✅ **PASS** (1.5s) |
| **7** | **Incidentes y Trust Score** | Banner de sanciones y deducción de puntos (-5, -15, -30 pts), historial de incidencias y estado. | `screenshots/07_incidentes_trust_score.png` | ✅ **PASS** (1.6s) |
| **8** | **Dashboard Ejecutivo y Flota** | Las 6 tarjetas KPI (espacios, inventario, reservas, préstamos, pendientes), Matriz de Desgaste de Flota y ocupación. | `screenshots/08_dashboard_ejecutivo.png` | ✅ **PASS** (2.0s) |

---

## 🚀 Ejecución de las Pruebas

Para correr la suite de pruebas Playwright en cualquier momento:

```bash
# Ejecutar todas las pruebas E2E en modo headless
pnpm exec playwright test

# Ejecutar con interfaz gráfica interactiva (UI Mode)
pnpm exec playwright test --ui

# Ver el reporte HTML detallado
pnpm exec playwright show-report docs/pruebas/playwright-report
```
