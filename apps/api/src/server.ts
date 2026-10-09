import express from 'express';
import cors from 'cors';
import helmet from 'helmet';
import cookieParser from 'cookie-parser';
import { env } from './config/env.js';
import { authRouter } from './routes/auth.routes.js';
import { eventsRouter } from './routes/events.routes.js';
import { loansRouter } from './routes/loans.routes.js';
import { spacesRouter } from './routes/spaces.routes.js';
import { resourcesRouter } from './routes/resources.routes.js';
import { incidentsRouter } from './routes/incidents.routes.js';
import { notificationsRouter } from './routes/notifications.routes.js';
import { dashboardRouter } from './routes/dashboard.routes.js';

const app = express();

app.use(helmet());
app.use(
  cors({
    origin: [env.WEB_URL, 'http://localhost:3000', 'http://localhost:5173'],
    credentials: true
  })
);
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true }));
app.use(cookieParser());

// Endpoint de Salud
app.get('/health', (req, res) => {
  res.json({
    status: 'ok',
    service: 'SIGRE API - CUTonalá',
    timestamp: new Date().toISOString()
  });
});

// Rutas API v1
app.use('/api/v1/auth', authRouter);
app.use('/api/v1/events', eventsRouter);
app.use('/api/v1/loans', loansRouter);
app.use('/api/v1/spaces', spacesRouter);
app.use('/api/v1/resources', resourcesRouter);
app.use('/api/v1/incidents', incidentsRouter);
app.use('/api/v1/notifications', notificationsRouter);
app.use('/api/v1/dashboard', dashboardRouter);

app.get('/api/v1', (req, res) => {
  res.json({
    name: 'SIGRE API',
    version: '1.0.0',
    institution: 'Centro Universitario de Tonalá (UdeG)',
    endpoints: {
      auth: '/api/v1/auth',
      events: '/api/v1/events',
      loans: '/api/v1/loans',
      spaces: '/api/v1/spaces',
      resources: '/api/v1/resources',
      incidents: '/api/v1/incidents',
      notifications: '/api/v1/notifications',
      dashboard: '/api/v1/dashboard'
    }
  });
});

app.listen(Number(env.PORT), '0.0.0.0', () => {
  console.log(`🚀 [SIGRE API] Servidor activo en http://0.0.0.0:${env.PORT}`);
});

export default app;
