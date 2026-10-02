# ⚖️ Módulo: Marco Legal, Privacidad y Cookies

**Etiquetas:** `#legal` `#lgpdpso` `#privacidad` `#cookies` `#custodia-patrimonial` `#sigre`  
**Referencia Detallada:** [MARCO_LEGAL_PRIVACIDAD_COOKIES.md](file:///c:/Users/erfierro/Documents/Inversion/docs/legal/MARCO_LEGAL_PRIVACIDAD_COOKIES.md)

---

## 1. Fundamento Jurídico en CUTonalá (UdeG)
- **LGPDPPSO (Federal) y Ley Estatal de Jalisco:** La UdeG es un organismo público autónomo sujeto a la supervisión del INAI e ITEI. Toda recolección de datos (firmas, fotos, códigos de estudiante) debe ajustarse a principios de licitud, consentimiento y confidencialidad.
- **Reglamento General de Alumnos de la UdeG:** Fundamento para exigir la conservación diligente de los bienes universitarios y la corresponsabilidad solidaria.

---

## 2. Política de Cookies
- **Cero rastreo publicitario:** No se utilizan píxeles ni rastreadores de marketing de terceros.
- **Cookies técnicas esenciales:**
  - `sigre_refresh_token`: Cookie `HttpOnly`, `Secure`, `SameSite=Strict` (7 días).
  - `sigre_csrf_token`: Protección contra ataques CSRF.
  - `localStorage`: Almacena la preferencia de tema (Dark/Light) y el consentimiento del banner.

---

## 3. URLs Prefirmadas en Google Cloud Storage (GCS)
- **Archivos Privados (Signed URLs con TTL de 15 min):**
  - Actas de responsiva en PDF (`actas/RESP-*.pdf`).
  - Fotografías de evidencia de daños en incidencias (`incidencias/*.jpg`).
  - Firmas digitalizadas en Base64.
- **Archivos Públicos (CDN / Bucket público):**
  - Pósters de eventos y Cineteca.
  - Fotografías de catálogo de aulas y auditorios.

---

## 4. Enlaces Relacionados
- [[Modulos/Responsivas_Digitales_y_Firmas|Responsivas Oficiales y Firmas]]
- [[Modulos/Checklists_e_Incidencias|Checklists e Incidencias]]
- [[Arquitectura/Index|Arquitectura General]]
