# Infraestructura del Proyecto (`infra/`)

Configuración de contenedores y servicios de infraestructura local.

## 🚀 Iniciar Servicios

Para levantar la base de datos PostgreSQL y la caché Redis localmente:

```bash
docker compose -f infra/docker-compose.yml up -d
```

Para detener los servicios:

```bash
docker compose -f infra/docker-compose.yml down
```
