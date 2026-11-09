# 🎨 SIGRE — Guía de Identidad de Marca

**Proyecto:** SIGRE (Sistema Integrado de Gestión de Recursos y Espacios)  
**Institución:** Centro Universitario de Tonalá — Universidad de Guadalajara  
**Fecha:** Septiembre 2026

---

## 1. Concepto de Marca

> **SIGRE es confianza institucional con eficiencia moderna.**

La identidad visual de SIGRE equilibra dos mundos: el **peso institucional** de la Universidad de Guadalajara (azul profundo, seriedad patrimonial) con la **frescura natural** de un campus vivo (verde, crecimiento, transparencia). El resultado es un sistema que transmite:

| Atributo | Cómo se expresa |
|---|---|
| **Confiabilidad** | Azul institucional UdeG como ancla cromática |
| **Transparencia** | Verde naturaleza como co-protagonista (custodía limpia) |
| **Simplicidad** | Tipografía geométrica limpia, sin adornos innecesarios |
| **Formalidad** | Estructura visual seria, sin infantilismos |
| **Modernidad** | UI con soporte dark mode, micro-interacciones suaves |

---

## 2. Paleta de Colores

![Paleta de colores SIGRE](/C:/Users/erfierro/.gemini/antigravity-ide/brain/332a6d27-43b3-4504-9e62-a4b1e0c5d751/sigre_color_palette_1788965210620.jpg)

### 2.1 Colores Primarios (Co-protagonistas)

| Nombre | Hex | RGB | Uso |
|---|---|---|---|
| **Azul Institucional** | `#002B49` | 0, 43, 73 | Navbar, encabezados, fondos de portada, botones primarios |
| **Verde Natural** | `#2E7D57` | 46, 125, 87 | Elementos activos, badges de éxito, acentos, íconos seleccionados |

### 2.2 Colores Secundarios / De Soporte

| Nombre | Hex | RGB | Uso |
|---|---|---|---|
| **Verde-Azul Profundo** | `#1A6B5A` | 26, 107, 90 | Gradientes, hover en botones, transiciones entre primarios |
| **Verde Suave** | `#D4E8DC` | 212, 232, 220 | Backgrounds sutiles, tarjetas de estado positivo, hover en modo claro |
| **Gris Azulado** | `#E8EFF5` | 232, 239, 245 | Fondo general modo claro, separadores, bordes suaves |

### 2.3 Colores de Texto

| Nombre | Hex | Modo | Uso |
|---|---|---|---|
| **Texto Principal** | `#1A1A2E` | Claro | Encabezados y cuerpo de texto |
| **Texto Secundario** | `#6B7280` | Claro | Subtítulos, labels, metadata |
| **Texto Principal** | `#F1F5F9` | Oscuro | Encabezados y cuerpo de texto |
| **Texto Secundario** | `#94A3B8` | Oscuro | Subtítulos, labels, metadata |

### 2.4 Colores Semánticos / De Estado

| Estado | Hex Claro | Hex Oscuro | Uso |
|---|---|---|---|
| **Éxito / Aprobado** | `#16A34A` | `#4ADE80` | Solicitudes aprobadas, checklist completado |
| **Advertencia / Pendiente** | `#D97706` | `#FBBF24` | Solicitudes pendientes, alertas de score |
| **Error / Rechazado** | `#DC2626` | `#F87171` | Rechazos, incidencias, suspensiones |
| **Informativo** | `#2563EB` | `#60A5FA` | Notificaciones, enlaces, información |

### 2.5 Colores de Fondo (Dark Mode)

| Nombre | Hex | Uso |
|---|---|---|
| **Base** | `#0D1B2A` | Fondo principal de la aplicación |
| **Superficie** | `#1A1A2E` | Sidebar, cards, modales |
| **Superficie Elevada** | `#1E293B` | Cards con hover, dropdowns |
| **Borde Sutil** | `#334155` | Líneas divisoras, bordes de cards |

---

## 3. Tipografía

### 3.1 Fuente Principal: **Outfit**
- **Fuente:** [Outfit](https://fonts.google.com/specimen/Outfit) (Google Fonts, gratuita)
- **Tipo:** Sans-serif geométrica
- **Carácter:** Moderna con personalidad, legible a todos los tamaños, equilibrio entre formal y accesible

### 3.2 Escala Tipográfica

| Nivel | Tamaño | Peso | Uso |
|---|---|---|---|
| **Display** | 36px / 2.25rem | 700 (Bold) | Pantallas de login, hero sections |
| **H1** | 30px / 1.875rem | 700 (Bold) | Título principal de página |
| **H2** | 24px / 1.5rem | 600 (SemiBold) | Secciones dentro de la página |
| **H3** | 20px / 1.25rem | 600 (SemiBold) | Títulos de cards, modales |
| **Body** | 16px / 1rem | 400 (Regular) | Texto general, párrafos |
| **Body Small** | 14px / 0.875rem | 400 (Regular) | Subtítulos, labels de formulario |
| **Caption** | 12px / 0.75rem | 500 (Medium) | Badges, timestamps, metadata |

### 3.3 Importación CSS

```css
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');

body {
  font-family: 'Outfit', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  -webkit-font-smoothing: antialiased;
}
```

### 3.4 Fuente Monoespaciada (Datos Técnicos)
- **Fuente:** JetBrains Mono (solo para códigos QR, folios, IDs de responsiva)
- **Tamaño:** 13px / 0.8125rem
- **Peso:** 400

---

## 4. Logotipo

### 4.1 Concepto del Logotipo

El logotipo de SIGRE es **puramente tipográfico**. La letra **"S"** lleva un degradado del azul institucional al verde natural, actuando como puente visual entre la identidad de la UdeG y la personalidad propia de SIGRE. Una pequeña **barra verde** debajo de la "S" refuerza el acento.

### 4.2 Versiones del Logo

````carousel
#### Versión Principal (Fondos Claros)
La versión estándar usa el azul institucional con la "S" en degradado.

**Archivo:** [`sigre-logo.svg`](file:///C:/Users/erfierro/Documents/Inversion/docs/brand/sigre-logo.svg)

**Colores:** "S" en gradiente `#002B49` → `#2E7D57`, "IGRE" en `#002B49`
<!-- slide -->
#### Versión Invertida (Fondos Oscuros / Dark Mode)
Para uso sobre fondos oscuros o en el modo oscuro de la aplicación.

**Archivo:** [`sigre-logo-white.svg`](file:///C:/Users/erfierro/Documents/Inversion/docs/brand/sigre-logo-white.svg)

**Colores:** "S" en gradiente `#FFFFFF` → `#4ADE80`, "IGRE" en `#FFFFFF`
<!-- slide -->
#### Favicon / Ícono de App
Versión compacta para pestañas del navegador y accesos directos móviles.

**Archivo:** [`sigre-favicon.svg`](file:///C:/Users/erfierro/Documents/Inversion/docs/brand/sigre-favicon.svg)

**Diseño:** Cuadrado redondeado con gradiente azul-teal y "S" blanca centrada
````

### 4.3 Referencia Visual del Concepto

![Concepto de logotipo SIGRE](/C:/Users/erfierro/.gemini/antigravity-ide/brain/332a6d27-43b3-4504-9e62-a4b1e0c5d751/sigre_logotype_concept_1788965185357.jpg)

### 4.4 Reglas de Uso

> [!IMPORTANT]
> - **Zona de exclusión:** Mantener al menos el equivalente a la altura de la letra "S" como espacio libre alrededor del logo.
> - **Tamaño mínimo:** 120px de ancho para web, 30mm para impresión.
> - **Nunca** distorsionar, rotar, cambiar los colores del gradiente o agregar efectos (sombras, biseles, brillos).
> - **Nunca** colocar el logo sobre fondos con fotos o patrones sin una caja de contención sólida.

---

## 5. Principios de Interfaz (UI)

### 5.1 Modo Claro

![Mockup dashboard en modo claro](/C:/Users/erfierro/.gemini/antigravity-ide/brain/332a6d27-43b3-4504-9e62-a4b1e0c5d751/sigre_ui_light_mockup_1788965234770.jpg)

### 5.2 Modo Oscuro

![Mockup dashboard en modo oscuro](/C:/Users/erfierro/.gemini/antigravity-ide/brain/332a6d27-43b3-4504-9e62-a4b1e0c5d751/sigre_ui_dark_mockup_1788965244797.jpg)

### 5.3 Principios de Diseño

| Principio | Descripción |
|---|---|
| **Simplicidad** | Cada pantalla tiene un propósito claro. Sin ruido visual. |
| **Jerarquía** | Los números grandes destacan KPIs. Los detalles secundarios usan grises. |
| **Consistencia** | Mismo estilo de cards, badges y botones en toda la aplicación. |
| **Responsividad** | La interfaz funciona por igual en celular, tablet y escritorio. |
| **Accesibilidad** | Contraste mínimo AA (4.5:1) entre texto y fondo. |

### 5.4 Componentes Clave

| Componente | Estilo |
|---|---|
| **Cards** | `border-radius: 12px`, sombra sutil `0 1px 3px rgba(0,0,0,0.08)`, padding `24px` |
| **Botones primarios** | Fondo `#002B49`, texto blanco, hover → `#1A6B5A`, `border-radius: 8px` |
| **Botones secundarios** | Borde `#002B49`, texto `#002B49`, hover → fondo `#E8EFF5` |
| **Botones de éxito** | Fondo `#2E7D57`, texto blanco, para acciones de aprobación |
| **Badges de estado** | `border-radius: 9999px`, tipografía Caption (12px Medium) |
| **Inputs** | Borde `#D1D5DB`, focus → borde `#2E7D57` + sombra verde sutil |
| **Navbar** | Fondo `#002B49` (claro) / `#0D1B2A` (oscuro), fija en top |
| **Sidebar** | Fondo `#F8FAFC` (claro) / `#1A1A2E` (oscuro), ítem activo con acento verde |

---

## 6. Design Tokens (CSS Custom Properties)

```css
:root {
  /* ══════════════ Paleta Primaria ══════════════ */
  --color-primary:          #002B49;
  --color-primary-hover:    #003D66;
  --color-accent:           #2E7D57;
  --color-accent-hover:     #1A6B5A;
  --color-bridge:           #1A6B5A;  /* transición azul↔verde */

  /* ══════════════ Fondos ══════════════ */
  --bg-base:                #FFFFFF;
  --bg-surface:             #F8FAFC;
  --bg-muted:               #E8EFF5;
  --bg-accent-soft:         #D4E8DC;

  /* ══════════════ Texto ══════════════ */
  --text-primary:           #1A1A2E;
  --text-secondary:         #6B7280;
  --text-on-primary:        #FFFFFF;

  /* ══════════════ Bordes ══════════════ */
  --border-default:         #D1D5DB;
  --border-focus:           #2E7D57;

  /* ══════════════ Semánticos ══════════════ */
  --color-success:          #16A34A;
  --color-warning:          #D97706;
  --color-error:            #DC2626;
  --color-info:             #2563EB;

  /* ══════════════ Sombras ══════════════ */
  --shadow-sm:              0 1px 2px rgba(0, 0, 0, 0.05);
  --shadow-md:              0 4px 6px rgba(0, 0, 0, 0.07);
  --shadow-lg:              0 10px 15px rgba(0, 0, 0, 0.1);

  /* ══════════════ Bordes Redondeados ══════════════ */
  --radius-sm:              6px;
  --radius-md:              8px;
  --radius-lg:              12px;
  --radius-xl:              16px;
  --radius-full:            9999px;

  /* ══════════════ Tipografía ══════════════ */
  --font-family:            'Outfit', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  --font-mono:              'JetBrains Mono', 'Fira Code', monospace;
  --font-size-xs:           0.75rem;     /* 12px */
  --font-size-sm:           0.875rem;    /* 14px */
  --font-size-base:         1rem;        /* 16px */
  --font-size-lg:           1.25rem;     /* 20px */
  --font-size-xl:           1.5rem;      /* 24px */
  --font-size-2xl:          1.875rem;    /* 30px */
  --font-size-3xl:          2.25rem;     /* 36px */

  /* ══════════════ Transiciones ══════════════ */
  --transition-fast:        150ms ease;
  --transition-normal:      250ms ease;
  --transition-slow:        350ms ease;
}

/* ══════════════ DARK MODE ══════════════ */
[data-theme="dark"] {
  --color-primary:          #1A6B5A;
  --color-primary-hover:    #2E7D57;
  --color-accent:           #4ADE80;
  --color-accent-hover:     #86EFAC;

  --bg-base:                #0D1B2A;
  --bg-surface:             #1A1A2E;
  --bg-muted:               #1E293B;
  --bg-accent-soft:         rgba(46, 125, 87, 0.15);

  --text-primary:           #F1F5F9;
  --text-secondary:         #94A3B8;
  --text-on-primary:        #FFFFFF;

  --border-default:         #334155;
  --border-focus:           #4ADE80;

  --color-success:          #4ADE80;
  --color-warning:          #FBBF24;
  --color-error:            #F87171;
  --color-info:             #60A5FA;

  --shadow-sm:              0 1px 2px rgba(0, 0, 0, 0.3);
  --shadow-md:              0 4px 6px rgba(0, 0, 0, 0.4);
  --shadow-lg:              0 10px 15px rgba(0, 0, 0, 0.5);
}
```

---

## 7. Iconografía

> [!TIP]
> Se recomienda usar **Lucide Icons** (derivado open-source de Feather Icons) por su estilo geométrico limpio que armoniza con Outfit.

| Módulo | Ícono sugerido | Código Lucide |
|---|---|---|
| Dashboard | Cuadrícula | `LayoutDashboard` |
| Préstamos | Paquete / Caja | `Package` |
| Espacios | Edificio | `Building2` |
| Eventos | Calendario | `CalendarDays` |
| Mi Perfil | Usuario | `UserCircle` |
| Notificaciones | Campana | `Bell` |
| QR | Escáner | `QrCode` |
| Checklist | Lista verificada | `ListChecks` |
| Score | Estrella / Escudo | `ShieldCheck` |

---

## 8. Resumen de Archivos de Marca

| Archivo | Ubicación | Descripción |
|---|---|---|
| [`sigre-logo.svg`](file:///C:/Users/erfierro/Documents/Inversion/docs/brand/sigre-logo.svg) | `docs/brand/` | Logo principal (fondos claros) |
| [`sigre-logo-white.svg`](file:///C:/Users/erfierro/Documents/Inversion/docs/brand/sigre-logo-white.svg) | `docs/brand/` | Logo invertido (fondos oscuros) |
| [`sigre-favicon.svg`](file:///C:/Users/erfierro/Documents/Inversion/docs/brand/sigre-favicon.svg) | `docs/brand/` | Favicon / ícono de app |
