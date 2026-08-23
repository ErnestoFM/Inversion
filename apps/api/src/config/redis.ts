import Redis from 'ioredis';
import { env } from './env.js';

export const redis = new Redis(env.REDIS_URL, {
  maxRetriesPerRequest: 3,
  retryStrategy(times) {
    if (times > 3) {
      console.warn('[Redis] Conexión en reintento fallido, usando fallback en memoria si aplica.');
      return null;
    }
    return Math.min(times * 200, 1000);
  }
});

redis.on('connect', () => {
  console.log('✅ [Redis] Conectado exitosamente');
});

redis.on('error', (err) => {
  console.warn('⚠️ [Redis] Error de conexión:', err.message);
});
