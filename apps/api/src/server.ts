import express from 'express';
import cors from 'cors';
import helmet from 'helmet';
import cookieParser from 'cookie-parser';
import { env } from './config/env.js';
import { authRouter } from './routes/auth.routes.js';
import { eventsRouter } from './routes/events.routes.js';
import { loansRouter } from './routes/loans.routes.js';

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
      inventory: '/api/v1/inventory',
      dashboard: '/api/v1/dashboard'
    }
  });
});

app.listen(Number(env.PORT), () => {
  console.log(`🚀 [SIGRE API] Servidor activo en http://localhost:${env.PORT}`);
});

export default app;
