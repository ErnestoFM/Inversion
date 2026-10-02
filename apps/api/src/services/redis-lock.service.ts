import { Redis } from 'ioredis';
import { env } from '../config/env.js';

export class RedisLockService {
  private static instance: Redis | null = null;

  public static getClient(): Redis {
    if (!this.instance) {
      this.instance = new Redis(env.REDIS_URL, {
        maxRetriesPerRequest: 3,
        retryStrategy(times) {
          const delay = Math.min(times * 100, 3000);
          return delay;
        }
      });

      this.instance.on('connect', () => {
        console.log('⚡ [Redis] Conectado exitosamente para control de concurrencia y caché');
      });

      this.instance.on('error', (err) => {
        console.error('❌ [Redis Error]:', err.message);
      });
    }
    return this.instance;
  }

  /**
   * Genera una clave canónica normalizada para el recurso y rango de tiempo
   */
  private static formatKey(resourceType: 'space' | 'item', resourceId: string, startTime: string | Date, endTime: string | Date): string {
    const startIso = new Date(startTime).toISOString();
    const endIso = new Date(endTime).toISOString();
    return `sigre:lock:${resourceType}:${resourceId}:${startIso}_${endIso}`;
  }

  /**
   * Intenta adquirir un bloqueo distribuido temporal (Soft Lock) por defecto de 15 minutos (900 seg)
   * Retorna true si adquirió el lock con éxito, false si ya está bloqueado por otro usuario
   */
  public static async acquireLock(
    resourceType: 'space' | 'item',
    resourceId: string,
    startTime: string | Date,
    endTime: string | Date,
    userId: string,
    ttlSeconds: number = 900
  ): Promise<{ acquired: boolean; ownerId?: string; remainingTtl?: number }> {
    const redis = this.getClient();
    const key = this.formatKey(resourceType, resourceId, startTime, endTime);

    // Intentar SET con NX (solo si no existe) y EX (tiempo de expiración)
    const result = await redis.set(key, userId, 'EX', ttlSeconds, 'NX');

    if (result === 'OK') {
      return { acquired: true, ownerId: userId, remainingTtl: ttlSeconds };
    }

    // Si ya existe, averiguar quién es el dueño actual y el tiempo restante
    const currentOwner = await redis.get(key);
    const remainingTtl = await redis.ttl(key);

    if (currentOwner === userId) {
      // Si el mismo usuario ya tenía el lock, renovamos el TTL
      await redis.expire(key, ttlSeconds);
      return { acquired: true, ownerId: userId, remainingTtl: ttlSeconds };
    }

    return { acquired: false, ownerId: currentOwner || undefined, remainingTtl: remainingTtl > 0 ? remainingTtl : 0 };
  }

  /**
   * Libera el bloqueo si el usuario que lo solicita es el dueño legítimo
   */
  public static async releaseLock(
    resourceType: 'space' | 'item',
    resourceId: string,
    startTime: string | Date,
    endTime: string | Date,
    userId: string
  ): Promise<boolean> {
    const redis = this.getClient();
    const key = this.formatKey(resourceType, resourceId, startTime, endTime);

    // Script Lua atómico para verificar propiedad antes de eliminar
    const luaScript = `
      if redis.call("get", KEYS[1]) == ARGV[1] then
        return redis.call("del", KEYS[1])
      else
        return 0
      end
    `;

    const deleted = await redis.eval(luaScript, 1, key, userId);
    return deleted === 1;
  }

  /**
   * Verifica si un recurso está bloqueado actualmente en ese horario
   */
  public static async isLocked(
    resourceType: 'space' | 'item',
    resourceId: string,
    startTime: string | Date,
    endTime: string | Date
  ): Promise<{ isLocked: boolean; ownerId?: string; remainingTtl?: number }> {
    const redis = this.getClient();
    const key = this.formatKey(resourceType, resourceId, startTime, endTime);

    const owner = await redis.get(key);
    if (!owner) {
      return { isLocked: false };
    }

    const ttl = await redis.ttl(key);
    return { isLocked: true, ownerId: owner, remainingTtl: ttl > 0 ? ttl : 0 };
  }

  /**
   * Agrega un JTI de token JWT a la lista negra al hacer logout
   */
  public static async blacklistToken(jti: string, ttlSeconds: number): Promise<void> {
    const redis = this.getClient();
    await redis.set(`sigre:token_blacklist:${jti}`, 'revoked', 'EX', ttlSeconds);
  }

  /**
   * Comprueba si un token ha sido revocado
   */
  public static async isTokenBlacklisted(jti: string): Promise<boolean> {
    const redis = this.getClient();
    const result = await redis.get(`sigre:token_blacklist:${jti}`);
    return result !== null;
  }
}
