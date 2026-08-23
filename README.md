# 💼 Proyecto Inversión

Estructura y arquitectura modular preparada para el desarrollo ágil y escalable de plataformas de inversión, con soporte integral para agentes de IA, memoria contextual en Obsidian y gestión estructurada de requerimientos.

---

## 🏗️ Estructura del Repositorio

```text
Inversion/
├── .agents/                 # Directivas, reglas y workflows para agentes de IA
│   ├── AGENTS.md            # Directivas maestras del espacio de trabajo
│   ├── rules/               # Reglas obligatorias (estándares, obsidian, requerimientos)
│   └── workflows/           # Flujos guiados de trabajo para el agente
├── .env.example             # Plantilla de variables de entorno (JWT, DB, Redis, etc.)
├── .gitignore               # Configuración de exclusiones de Git
├── apps/                    # Aplicaciones ejecutables (API backend, Frontend web)
│   └── README.md
├── docs/                    # Documentación técnica, metodológica y funcional
│   ├── arquitectura/        # Diagramas, ERD y decisiones arquitectónicas
│   ├── metodologia/         # Roadmap y planeación
│   ├── pruebas/             # Estrategia y cobertura de pruebas
│   ├── tecnica/             # Especificaciones de APIs y seguridad
│   └── usuarios/            # Manuales y guías
├── infra/                   # Infraestructura local de desarrollo
│   ├── docker-compose.yml   # PostgreSQL + Redis
│   └── README.md
├── obsidian/                # Vault de Obsidian (Memoria contextual del agente)
│   ├── Index.md             # Índice central del vault
│   ├── Arquitectura/        # Notas arquitectónicas
│   ├── Bitacora/            # Registro cronológico diario de sesiones
│   ├── Contexto/            # Dominio de negocio y requerimientos de inversión
│   └── Modulos/             # Detalle de cada módulo del sistema
├── packages/                # Paquetes y librerías internas compartidas
│   └── README.md
├── requirements/            # Insumos y requerimientos del proyecto
│   ├── funcionales/         # Historias de usuario y reglas de negocio
│   ├── tecnicos/            # Especificaciones técnicas y contratos de API
│   └── README.md
├── package.json             # Configuración del monorepo y scripts globales
├── pnpm-workspace.yaml      # Configuración de workspaces de pnpm
└── turbo.json               # Configuración de Turborepo
```

---

## 🚀 Inicio Rápido

### 1. Variables de Entorno
Copia la plantilla de entorno e inicializa tus configuraciones locales:
```bash
cp .env.example .env
```

### 2. Infraestructura Local
Levanta PostgreSQL y Redis con un solo comando:
```bash
docker compose -f infra/docker-compose.yml up -d
```

### 3. Requerimientos para Construcción
Coloca tus documentos de especificación en `requirements/funcionales/` y `requirements/tecnicos/`. Los agentes de IA los leerán automáticamente antes de implementar cualquier funcionalidad.
