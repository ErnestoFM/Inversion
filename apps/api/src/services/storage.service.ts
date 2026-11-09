import { Storage } from '@google-cloud/storage';
import path from 'path';
import fs from 'fs';
import { env } from '../config/env.js';

export interface StorageUploadResult {
  gcsUri: string;
  storagePath: string;
  signedUrl: string;
}

export class StorageService {
  private storage: Storage | null = null;
  private bucketName: string;
  private isGcpConfigured: boolean = false;

  constructor() {
    this.bucketName = env.GCS_BUCKET;
    this.initStorage();
  }

  private initStorage() {
    try {
      const candidates = [
        process.env.GOOGLE_APPLICATION_CREDENTIALS,
        path.resolve(process.cwd(), 'sa-key.json'),
        path.resolve(process.cwd(), '../../sa-key.json')
      ];

      const keyFile = candidates.find((p) => p && fs.existsSync(p));

      if (keyFile) {
        this.storage = new Storage({
          projectId: env.GCP_PROJECT_ID,
          keyFilename: keyFile
        });
        this.isGcpConfigured = true;
      } else if (env.NODE_ENV === 'production') {
        // En Cloud Run se usan Application Default Credentials (ADC) automáticamente
        this.storage = new Storage({ projectId: env.GCP_PROJECT_ID });
        this.isGcpConfigured = true;
      } else {
        // En entorno local de desarrollo sin SA key
        this.storage = null;
        this.isGcpConfigured = false;
      }
    } catch (err) {
      console.warn('⚠️ [StorageService] No se pudo inicializar Google Cloud Storage, usando almacenamiento local:', err);
      this.storage = null;
      this.isGcpConfigured = false;
    }
  }

  public isAvailable(): boolean {
    return this.isGcpConfigured && this.storage !== null;
  }

  /**
   * Sube un archivo desde disco local a Cloud Storage o guarda copia local si GCS no está conectado.
   */
  async uploadFile(localFilePath: string, destinationName: string, contentType = 'application/pdf'): Promise<StorageUploadResult> {
    const cleanDest = destinationName.replace(/\\/g, '/').replace(/^\//, '');

    if (this.isAvailable() && this.storage) {
      try {
        const bucket = this.storage.bucket(this.bucketName);
        await bucket.upload(localFilePath, {
          destination: cleanDest,
          metadata: {
            contentType
          }
        });

        const signedUrl = await this.getSignedUrl(cleanDest, 60);

        return {
          gcsUri: `gs://${this.bucketName}/${cleanDest}`,
          storagePath: cleanDest,
          signedUrl
        };
      } catch (error) {
        console.warn('⚠️ [StorageService] Error al subir a GCS, conservando copia local:', error);
      }
    }

    // Fallback local: Conserva el archivo local y retorna ruta relativa
    return {
      gcsUri: `local://${cleanDest}`,
      storagePath: localFilePath,
      signedUrl: `/uploads/${cleanDest}`
    };
  }

  /**
   * Sube un Buffer binario directamente al bucket de GCS.
   */
  async uploadBuffer(buffer: Buffer, destinationName: string, contentType = 'application/pdf'): Promise<StorageUploadResult> {
    const cleanDest = destinationName.replace(/\\/g, '/').replace(/^\//, '');

    if (this.isAvailable() && this.storage) {
      try {
        const bucket = this.storage.bucket(this.bucketName);
        const file = bucket.file(cleanDest);

        await file.save(buffer, {
          metadata: { contentType },
          resumable: false
        });

        const signedUrl = await this.getSignedUrl(cleanDest, 60);

        return {
          gcsUri: `gs://${this.bucketName}/${cleanDest}`,
          storagePath: cleanDest,
          signedUrl
        };
      } catch (error) {
        console.warn('⚠️ [StorageService] Error al subir Buffer a GCS:', error);
      }
    }

    // Fallback local
    const localDir = path.resolve(process.cwd(), 'uploads', path.dirname(cleanDest));
    if (!fs.existsSync(localDir)) {
      fs.mkdirSync(localDir, { recursive: true });
    }
    const localPath = path.resolve(process.cwd(), 'uploads', cleanDest);
    fs.writeFileSync(localPath, buffer);

    return {
      gcsUri: `local://${cleanDest}`,
      storagePath: localPath,
      signedUrl: `/uploads/${cleanDest}`
    };
  }

  /**
   * Genera una URL firmada v4 con vencimiento temporal para acceso seguro y privado.
   */
  async getSignedUrl(storagePath: string, expiresInMinutes = 60): Promise<string> {
    if (!this.isAvailable() || !this.storage) {
      return `/uploads/${storagePath}`;
    }

    try {
      const cleanPath = storagePath.startsWith('gs://') 
        ? storagePath.replace(`gs://${this.bucketName}/`, '')
        : storagePath;

      const [url] = await this.storage
        .bucket(this.bucketName)
        .file(cleanPath)
        .getSignedUrl({
          version: 'v4',
          action: 'read',
          expires: Date.now() + expiresInMinutes * 60 * 1000
        });

      return url;
    } catch (error) {
      console.warn('⚠️ [StorageService] Error generando Signed URL:', error);
      return `/uploads/${storagePath}`;
    }
  }

  /**
   * Obtiene stream de lectura para reenviar archivo al cliente
   */
  async getFileStream(storagePath: string) {
    if (!this.isAvailable() || !this.storage) {
      const cleanPath = storagePath.startsWith('local://') ? storagePath.replace('local://', '') : storagePath;
      const localFile = path.isAbsolute(cleanPath) ? cleanPath : path.resolve(process.cwd(), 'uploads', cleanPath);
      return fs.createReadStream(localFile);
    }

    const cleanPath = storagePath.startsWith('gs://') 
      ? storagePath.replace(`gs://${this.bucketName}/`, '')
      : storagePath;

    return this.storage.bucket(this.bucketName).file(cleanPath).createReadStream();
  }
}

export const storageService = new StorageService();
