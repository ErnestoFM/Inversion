# ==============================================================================
# Dockerfile Multi-Stage de Producción: SIGRE Backend API (Express + TypeScript)
# ==============================================================================

# ------------------------------------------------------------------------------
# Etapa 1: Builder y Compilación
# ------------------------------------------------------------------------------
FROM node:20-slim AS builder

# Instalar dependencias del sistema requeridas para Prisma y compilación de módulos nativos (Argon2)
RUN apt-get update && apt-get install -y --no-install-recommends \
    openssl \
    python3 \
    make \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Habilitar pnpm
ENV PNPM_HOME="/pnpm"
ENV PATH="$PNPM_HOME:$PATH"
RUN corepack enable && corepack prepare pnpm@9.1.0 --activate

WORKDIR /app

# Copiar manifiestos de todo el monorepo y código fuente para evitar sobreescritura de symlinks
COPY package.json pnpm-lock.yaml pnpm-workspace.yaml turbo.json ./
COPY packages/shared-types ./packages/shared-types
COPY packages/database ./packages/database
COPY apps/api ./apps/api
COPY apps/web/package.json ./apps/web/package.json

# Instalar dependencias completas del monorepo
RUN pnpm install --frozen-lockfile

# Generar Prisma y compilar librerías y API a JavaScript
RUN pnpm --filter @inversion/database run generate
RUN pnpm --filter @inversion/shared-types run build
RUN pnpm --filter @inversion/api run build

# ------------------------------------------------------------------------------
# Etapa 2: Entorno de Ejecución (Runner) - Imagen mínima para Producción
# ------------------------------------------------------------------------------
FROM node:20-slim AS runner

# Dependencias mínimas de ejecución (openssl para Prisma, curl para Healthcheck)
RUN apt-get update && apt-get install -y --no-install-recommends \
    openssl \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Variables de entorno por defecto en Cloud Run
ENV NODE_ENV=production
ENV PORT=8080

# Usuario no privilegiado para seguridad
USER node

# Copiar archivos compilados y árbol de dependencias
COPY --chown=node:node --from=builder /app/package.json /app/pnpm-lock.yaml /app/pnpm-workspace.yaml ./
COPY --chown=node:node --from=builder /app/node_modules ./node_modules
COPY --chown=node:node --from=builder /app/packages/shared-types ./packages/shared-types
COPY --chown=node:node --from=builder /app/packages/database ./packages/database
COPY --chown=node:node --from=builder /app/apps/api ./apps/api

EXPOSE 8080

# Healthcheck nativo para GCP Cloud Run y Docker
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD curl -f http://localhost:8080/health || exit 1

WORKDIR /app/apps/api

# Iniciar servidor compilado
CMD ["node", "dist/server.js"]
