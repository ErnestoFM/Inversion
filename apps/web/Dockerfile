# ==============================================================================
# Dockerfile Multi-Stage de Producción: SIGRE Frontend (React 18 + Vite + Nginx)
# ==============================================================================

# ------------------------------------------------------------------------------
# Etapa 1: Compilación de Assets con Vite
# ------------------------------------------------------------------------------
FROM node:20-slim AS builder

# Habilitar pnpm
ENV PNPM_HOME="/pnpm"
ENV PATH="$PNPM_HOME:$PATH"
RUN corepack enable && corepack prepare pnpm@9.1.0 --activate

WORKDIR /app

# Copiar manifiestos y código fuente
COPY package.json pnpm-lock.yaml pnpm-workspace.yaml turbo.json ./
COPY packages/shared-types ./packages/shared-types
COPY packages/database/package.json ./packages/database/package.json
COPY apps/api/package.json ./apps/api/package.json
COPY apps/web ./apps/web

# Argumento opcional de build para la URL del backend en producción
ARG VITE_API_BASE="/api"
ENV VITE_API_BASE=$VITE_API_BASE

# Instalar dependencias exactas
RUN pnpm install --frozen-lockfile

# Compilar tipos compartidos y bundle optimizado de Vite
RUN pnpm --filter @inversion/shared-types run build
RUN pnpm --filter @inversion/web run build

# ------------------------------------------------------------------------------
# Etapa 2: Servidor Nginx Alpine Ultraligero para Producción
# ------------------------------------------------------------------------------
FROM nginx:1.27-alpine AS runner

# Eliminar configuración por defecto de Nginx
RUN rm -rf /etc/nginx/conf.d/default.conf /usr/share/nginx/html/*

# Copiar configuración personalizada optimizada para SPA y Cloud Run
COPY apps/web/nginx.conf /etc/nginx/conf.d/default.conf

# Copiar los archivos estáticos compilados desde la etapa builder
COPY --from=builder /app/apps/web/dist /usr/share/nginx/html

# Exponer el puerto estándar de GCP Cloud Run
EXPOSE 8080

# Healthcheck nativo para contenedores web
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD wget --quiet --tries=1 --spider http://localhost:8080/ || exit 1

# Ejecutar Nginx en primer plano
CMD ["nginx", "-g", "daemon off;"]
