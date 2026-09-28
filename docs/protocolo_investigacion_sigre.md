# Protocolo de Investigación: Plataforma SIGRE

**Materia:** METODOLOGÍA Y PRÁCTICA DE LA INVESTIGACIÓN  
**Ciclo Escolar:** 2026B  
**Licenciatura:** Ingeniería en Ciencias Computacionales  
**Institución:** Universidad de Guadalajara | Centro Universitario de Tonalá (CUTonalá)  
**Docente Titular:** Mtra. Elizabeth Cristina Hernández Hernández  
**Equipo:** Equipo 4  
**Integrantes:**
- Barragán Padilla Carlos Emiliano
- Fierro Meléndez Ernesto Hatuey
- Padilla Casillas Josue Wenceslao  
**Fecha y Lugar de Elaboración:** Septiembre de 2026, Tonalá, Jalisco, México  
**Entregable Oficial:** `2026B_Equipo4_Protocolo.pdf`

---

## Título del Protocolo
**SIGRE: Sistema Integrado de Gestión de Recursos y Espacios para la optimización del control patrimonial y reserva de infraestructura en CUTonalá**

---

## Índice General

1. **Portada**
2. **Índice (Tabla de Contenido)**
3. **Breve Introducción**
4. **Planteamiento del Problema**
   - 4.1 Contexto institucional y operacional
   - 4.2 El colapso del modelo analógico de gestión
   - 4.3 Causas fundamentales de la problemática
   - 4.4 Consecuencias e impacto cuantificado en el campus
   - 4.5 Formulación de la pregunta de investigación
5. **Justificación**
   - 5.1 Relevancia institucional, operativa y académica
   - 5.2 Pertinencia en la Ingeniería en Ciencias Computacionales
   - 5.3 Alineación con los Objetivos de Desarrollo Sostenible (ODS 2030)
     - 5.3.1 ODS 4: Educación de Calidad (Meta 4.a)
     - 5.3.2 ODS 9: Industria, Innovación e Infraestructura (Metas 9.4 y 9.c)
     - 5.3.3 ODS 12: Producción y Consumo Responsables (Meta 12.5)
6. **Objetivos de la Investigación**
   - 6.1 Criterio metodológico y epistemológico de formulación
   - 6.2 Objetivo General
   - 6.3 Objetivos Específicos
     - 6.3.1 Objetivo Específico 1: Diagnóstico situacional y mapeo de flujos operativos
     - 6.3.2 Objetivo Específico 2: Diseño arquitectónico y desarrollo de módulos funcionales
     - 6.3.3 Objetivo Específico 3: Implementación piloto y evaluación cuantitativa de impacto
   - 6.4 Matriz de Coherencia Metodológica de Objetivos
7. **Referencias Bibliográficas (APA 7ma Edición)**

---

## 1. Breve Introducción

El presente protocolo de investigación aborda el diseño, desarrollo e implementación de una solución tecnológica orientada a resolver una de las problemáticas operativas más recurrentes y costosas en las instituciones públicas de educación superior: la ineficiencia, descontrol y vulnerabilidad en la administración de espacios físicos y el préstamo de equipamiento audiovisual y técnico. Centrado en el contexto del Centro Universitario de Tonalá (CUTonalá) de la Universidad de Guadalajara, el proyecto **SIGRE (Sistema Integrado de Gestión de Recursos y Espacios)** plantea la sustitución integral de los modelos analógicos tradicionales —basados en registros manuales en libretas de papel y acuerdos verbales desarticulados— por un ecosistema digital distribuido, seguro y accesible vía web y dispositivos móviles. 

A través del rigor metodológico propio de la Ingeniería en Ciencias Computacionales, este protocolo articula un diagnóstico fundado en la observación directa en almacenes y Servicios Generales, formula los requerimientos funcionales y técnicos necesarios, y alinea sus metas con la agenda global de sostenibilidad de la Organización de las Naciones Unidas (ODS 2030). El documento expone a continuación el planteamiento detallado del problema, su justificación institucional y social, y la estructura jerárquica de objetivos generales y específicos que guiarán la construcción y evaluación del software.

---

## 2. Planteamiento del Problema

### 2.1 Contexto institucional y operacional
La Universidad de Guadalajara (UdeG) constituye la segunda red universitaria pública más grande de México, atendiendo a una matrícula que supera los 330,000 estudiantes y a más de 17,000 académicos y directivos distribuidos en centros universitarios temáticos y regionales (Coordinación General de Planeación y Evaluación [CGPE], 2024). En particular, el Centro Universitario de Tonalá (CUTonalá) se distingue como un campus multidisciplinario de rápido crecimiento, con una infraestructura diseñada para albergar licenciaturas e ingenierías de vanguardia, laboratorios de alta especialidad, clínicas de salud y edificios multiaula orientados a esquemas educativos flexibles (Centro Universitario de Tonalá [CUTonalá], 2023).

No obstante, esta modernización física convive cotidianamente con una severa contradicción operativa: mientras las aulas y auditorios se equipan con tecnología de última generación, los procesos para solicitar, asignar, prestar y custodiar dichos bienes e instalaciones continúan anclados en procedimientos analógicos que datan de hace varias décadas.

### 2.2 El colapso del modelo analógico de gestión
En la actualidad, la solicitud diaria de proyectores, cables HDMI, adaptadores multipuerto, micrófonos, apuntadores láser y llaves de acceso a aulas magnas y auditorios depende de registros manuales efectuados en libretas físicas de ventanilla o bitácoras en papel. Este modelo adolece de tres fallas críticas estructurales:

1. **Vulnerabilidad documental e ilegibilidad:** Las libretas de mostrador presentan hojas desprendidas, datos apresurados e ilegibles tomados durante las horas pico de entrada a clase (7:00 a 8:00 hrs y 15:00 a 16:00 hrs), manchas por uso constante y riesgo permanente de extravío o daño físico.
2. **Empalmes de agenda y desarticulación:** La reserva de aulas de usos múltiples, salas de seminarios y auditorios se realiza mediante oficios en papel, correos electrónicos aislados o acuerdos verbales entre coordinaciones académicas y prefectura. Esta dispersión genera duplicidad de eventos, empalmes de horarios y cancelaciones abruptas de conferencias magistrales y clases programadas.
3. **Ruptura de la cadena de custodia patrimonial:** Al prestarse un bien técnico, el solicitante únicamente anota su código o firma un vale informal sin un checklist funcional estandarizado. Al momento de la devolución, es imposible determinar si un accesorio faltante o un desperfecto físico (como puertos quemados o cables trozados) ocurrió durante el uso del último profesor o venía arrastrándose de turnos anteriores, imposibilitando legalmente el deslinde de responsabilidades.

### 2.3 Causas fundamentales de la problemática
El análisis de fondo permite identificar tres causas primarias que perpetúan la crisis operativa:
- **Causa Operativa-Tecnológica:** Inexistencia de un sistema informático centralizado con sincronización en tiempo real entre el inventario del almacén de Servicios Generales y el estatus operativo del recurso (disponible, en préstamo activo, en mantenimiento correctivo o reservado con anticipación).
- **Causa Jurídico-Administrativa:** Fragilidad de los mecanismos de entrega-recepción. Una firma en una libreta convencional carece de validez pericial y no satisface los lineamientos legales de la Ley General de Protección de Datos Personales en Posesión de Sujetos Obligados (Cámara de Diputados del H. Congreso de la Unión, 2017) ni el Reglamento de Bienes Muebles y Patrimonio Universitario (Universidad de Guadalajara, 2019).
- **Causa Cultural y de Control Interno:** Ausencia de un historial o puntaje de confiabilidad del usuario solicitante. Al no registrarse formalmente las entregas con demora sistemática, las devoluciones incompletas o los daños patrimoniales, no existe incentivo individual para el uso diligente de los bienes públicos institucionales.

### 2.4 Consecuencias e impacto cuantificado en el campus
Las secuelas del sostenimiento de este sistema manual impactan severamente las finanzas y el desempeño académico de CUTonalá:
- **Merma patrimonial silenciosa:** De acuerdo con los datos recabados en la experiencia de campo en Servicios Generales y almacenes universitarios, se estima una merma anual de entre **$130,000 y $150,000 MXN por plantel**, derivada del extravío crónico de adaptadores, cables de alta resolución y mouses inalámbricos, así como de proyectores que sufren daño prematuro por descargas o sobrecalentamiento no reportado.
- **Pérdida de horas-clase efectivas:** Cada incidencia por falta de equipo disponible o empalme de aula consume entre **15 y 25 minutos de clase**, afectando el avance programático docente y desmotivando a los alumnos.
- **Ceguera directiva para presupuestación:** Los secretarios administrativos y jefes de almacén carecen de reportes analíticos sobre tasa de uso, horas de operación acumulada por proyector o índices de depreciación real, forzando la compra ciega de materiales de repuesto.

### 2.5 Formulación de la pregunta de investigación
A partir de la problemática expuesta, se define la **Pregunta General de Investigación**:
> *¿De qué manera el diseño e implementación de un sistema web centralizado con responsivas digitales, checklist de verificación y código QR dinámico (SIGRE) permite reducir las mermas patrimoniales por extravío no atribuible de equipo técnico y erradicar los empalmes en la asignación de espacios académicos en el Centro Universitario de Tonalá durante el ciclo escolar 2026B?*

Asimismo, se desprenden las siguientes **Preguntas Específicas**:
1. ¿Cuáles son los cuellos de botella, tiempos muertos y riesgos de descontrol que caracterizan actualmente el circuito de préstamo en ventanilla de Servicios Generales en CUTonalá?
2. ¿Qué modelo arquitectónico de software y qué tecnologías de interoperabilidad garantizan una plataforma ligera, segura y accesible para docentes, alumnos y almacenistas?
3. ¿Cuál es el grado de efectividad técnica y viabilidad operativa alcanzado por la plataforma en un ambiente de pilotaje real medido a través de indicadores de disponibilidad y reducción de mermas?

---

## 3. Justificación

### 3.1 Relevancia institucional, operativa y académica
La presente investigación se fundamenta en la necesidad imperativa de transformar digitalmente la gestión de recursos en la educación pública superior. Administrar infraestructura física y técnica en una institución como la Universidad de Guadalajara no es una tarea meramente burocrática; es la base material indispensable que hace posible la docencia de excelencia, la experimentación científica y la difusión de la cultura.

Desde la perspectiva operativa, la implementación de la plataforma SIGRE dignifica y optimiza la labor del personal de ventanilla y almacén. Los encargados de turno enfrentan diariamente largas filas de profesores que requieren material simultáneamente antes del inicio de su clase. Al sustituir la anotación manual por el escaneo de un código QR personal generado en segundos desde el teléfono móvil, el tiempo de despacho en mostrador se reduce en más de un 70%, erradicando disputas y malas interpretaciones sobre el estado en que se entrega o recibe el equipo.

Desde la óptica de la gestión patrimonial, el proyecto proporciona a la Secretaría Administrativa y a la Coordinación de Servicios Generales una herramienta de control probatorio de primer orden. Al generar actas de entrega-recepción digitales (responsivas) que consignan la matrícula, fecha, hora exacta, número de serie del activo y checklist fotográfico/funcional firmado electrónicamente, se establece una cadena de custodia inquebrantable que desalienta el descuido y ampara legalmente el deslinde de responsabilidades ante auditorías internas y externas de la Contraloría Universitaria.

### 3.2 Pertinencia en la Ingeniería en Ciencias Computacionales
El desarrollo del proyecto SIGRE representa una aplicación directa y rigurosa de las competencias centrales de la Ingeniería en Ciencias Computacionales. No se trata de un formulario superficial de reservaciones, sino de una arquitectura de software distribuida orientada a servicios, capaz de resolver retos complejos:
- **Seguridad e integridad de datos:** Implementación de protocolos robustos de autenticación (JWT/OAuth2), encriptación en tránsito y reposo, y cumplimiento de la Ley de Protección de Datos Personales.
- **Escalabilidad y concurrencia:** Diseño de esquemas de bases de datos relacionales optimizados que soportan cientos de solicitudes simultáneas en las horas de mayor demanda sin bloqueos transaccionales ni fallas de integridad referencial.
- **Interoperabilidad y accesibilidad móvil:** Empleo de interfaces web progresivas y estándares modernos (APIs RESTful, frameworks reactivos) que garantizan compatibilidad universal en dispositivos móviles sin requerir instalaciones pesadas.

### 3.3 Alineación con los Objetivos de Desarrollo Sostenible (ODS 2030)
De acuerdo con las directrices metodológicas del protocolo, el proyecto SIGRE se encuentra estrechamente vinculado con tres objetivos de la **Agenda 2030 para el Desarrollo Sostenible** adoptada por la Organización de las Naciones Unidas (ONU, 2015):

```
+----------------------------------------------------------------------------------------------------+
|                                VINCULACIÓN CON LA AGENDA ODS 2030                                 |
+------------------------------+------------------------------------+--------------------------------+
| ODS 4: EDUCACIÓN DE CALIDAD  | ODS 9: INNOVACIÓN E INFRAESTRUCTURA| ODS 12: PRODUCCIÓN Y CONSUMO   |
| Meta 4.a: Entornos de        | Meta 9.4 y 9.c: Modernización e    | Meta 12.5: Reducción de mermas |
| aprendizaje eficaces y libres| infraestructura tecnológica digital| y uso responsable de recursos  |
| de pérdidas de tiempo lectivo| y de alta conectividad institucional| públicos universitarios        |
+------------------------------+------------------------------------+--------------------------------+
```

#### 5.3.1 ODS 4: Educación de Calidad (Meta 4.a)
La Meta 4.a de los ODS insta a los Estados miembros a *"construir y adecuar instalaciones educativas que ofrezcan entornos de aprendizaje seguros, inclusivos y eficaces para todos"*. El descontrol en la asignación de espacios y el retraso en la entrega de proyectores o adaptadores mutilan directamente el tiempo lectivo efectivo de los estudiantes universitarios. SIGRE garantiza que las aulas tecnológicas y auditorios se reserven con precisión matemática, eliminando cancelaciones por empalme y asegurando que las clases inicien con el material didáctico audiovisual disponible en tiempo y forma, salvaguardando la calidad del proceso educativo de miles de universitarios.

#### 5.3.2 ODS 9: Industria, Innovación e Infraestructura (Metas 9.4 y 9.c)
La Meta 9.4 demanda modernizar la infraestructura para que sea sostenible, aplicando tecnologías de vanguardia, mientras que la Meta 9.c promueve un acceso ampliado a las tecnologías de información y comunicación. CUTonalá se ostenta como un campus de innovación y sustentabilidad; perpetuar libretas de papel en sus áreas administrativas contradice su visión institucional. SIGRE digitaliza por completo el flujo logístico del campus, integrando códigos QR, responsivas en la nube y trazabilidad instantánea, convirtiendo a la infraestructura física de la universidad en un sistema interconectado, eficiente y transparente.

#### 5.3.3 ODS 12: Producción y Consumo Responsables (Meta 12.5)
La Meta 12.5 exige *"reducir considerablemente la generación de desechos mediante actividades de prevención, reducción, reciclado y reutilización"*. En la actualidad, cientos de cables, adaptadores y componentes electrónicos terminan catalogados como basura prematura debido a malos tratos o negligencia al no existir inspecciones de entrada y salida. El doble checklist de SIGRE prolonga la vida útil de los equipos institucionales al detectar fallas incipientes antes de que el daño sea irreparable, reduciendo la chatarrización innecesaria de bienes electrónicos y evitando gastos repetitivos que drenan el erario público universitario.

---

## 4. Objetivos de la Investigación

### 4.1 Criterio metodológico y epistemológico de formulación
La formulación de los objetivos de este protocolo responde a las mejores prácticas metodológicas documentadas por autores clave en el ámbito de la investigación aplicada y la formulación de proyectos tecnológicos (Hernández-Sampieri & Mendoza, 2018; Bernal, 2016). Se adopta la Taxonomía de Bloom revisada para garantizar que los enunciados comiencen con verbos en infinitivo de alto orden analítico, evitando términos ambiguos o meramente asociativos.

Asimismo, los objetivos satisfacen íntegramente el estándar **SMART**:
- **Specific (Específicos):** Determinan exactamente qué se va a investigar, diseñar y construir, sin dispersión.
- **Measurable (Medibles):** Vinculados a indicadores concretos de desempeño operativo, satisfacción de usuarios y trazabilidad patrimonial.
- **Achievable (Alcanzables):** Viables técnica y operativamente dentro de las capacidades computacionales y recursos institucionales disponibles en CUTonalá.
- **Relevant (Relevantes):** Resuelven directamente las causas de descontrol y merma diagnosticadas en la problemática.
- **Time-bound (Temporales):** Enmarcados cronológicamente para su ejecución y validación durante el ciclo escolar universitario 2026B.

### 4.2 Objetivo General
> **"Desarrollar e implementar un sistema web centralizado (SIGRE) para la gestión integral y reserva transparente de recursos técnicos, equipamiento audiovisual y espacios físicos, con el fin de optimizar el aprovechamiento patrimonial, erradicar los empalmes de agenda y reducir los tiempos de despacho en mostrador en la comunidad universitaria del Centro Universitario de Tonalá durante el ciclo escolar 2026B."**

### 4.3 Objetivos Específicos
Para materializar el cumplimiento cabal del objetivo general, la investigación se desagrega en **tres objetivos específicos secuenciales y complementarios**, que abarcan desde el diagnóstico de campo hasta la validación y evaluación de impacto:

#### 6.3.1 Objetivo Específico 1: Diagnóstico situacional y mapeo de flujos operativos
> **"Diagnosticar el flujo operativo actual, los cuellos de botella y las vulnerabilidades de registro en el préstamo de equipo técnico y asignación de espacios físicos en los almacenes y áreas de Servicios Generales de CUTonalá, mediante el levantamiento de encuestas estructuradas, entrevistas a personal de mostrador y análisis documental de bitácoras físicas."**

- **Justificación y Alcance Metodológico:** Este objetivo responde a la pregunta de investigación diagnóstica. Antes de formular líneas de código, es imperativo cuantificar la demanda real, identificar los horarios pico de mayor saturación de ventanilla, inventariar los tipos de activos con mayor índice de extravío y documentar las fricciones reportadas por los profesores y almacenistas.
- **Variables Asociadas:** Tiempo promedio de atención por usuario en mostrador (minutos), índice de discrepancia documental en bitácoras de papel y tasa mensual estimada de activos no devueltos o dañados.
- **Entregable Verificable:** Informe de diagnóstico situacional y Matriz de Requerimientos del Sistema (documento de especificación formal de casos de uso y reglas de negocio del campus).

#### 6.3.2 Objetivo Específico 2: Diseño arquitectónico y desarrollo de módulos funcionales
> **"Diseñar y construir una arquitectura modular de software basada en tecnologías web (frontend responsivo y backend escalable con base de datos relacional), que integre autenticación institucional segura, emisión de códigos QR dinámicos para control en puerta, generación automática de responsivas oficiales con firma digital y módulo de doble checklist de inspección funcional."**

- **Justificación y Alcance Metodológico:** Constituye el núcleo de la aportación en ingeniería computacional del proyecto. Descompone la solución en componentes desacoplados: un motor de reservaciones que previene matemáticamente solapamientos de horario mediante validaciones transaccionales ACID; un generador de tickets móviles con códigos QR temporales para autenticación rápida; y un generador de responsivas PDF oficiales con sellos criptográficos.
- **Variables Asociadas:** Latencia en la generación y validación del código QR (milisegundos), cobertura de pruebas unitarias/integración de la lógica de negocio y tiempo de generación del acta responsiva digital.
- **Entregable Verificable:** Código fuente de la plataforma SIGRE documentado bajo repositorio de control de versiones Git, esquema relacional de base de datos normalizado (3FN) y manual técnico de despliegue en entorno local/cloud.

#### 6.3.3 Objetivo Específico 3: Implementación piloto y evaluación cuantitativa de impacto
> **"Evaluar la viabilidad técnica, la eficiencia operativa y el nivel de satisfacción de la plataforma SIGRE a través de una prueba piloto controlada en almacenes seleccionados de CUTonalá, contrastando los tiempos de despacho, la precisión del inventario activo y la experiencia de usuario frente al modelo tradicional de registro en libretas."**

- **Justificación y Alcance Metodológico:** Cumple con la fase de contrastación empírica requerida en todo protocolo de investigación aplicada. La plataforma será sometida al uso cotidiano de una muestra representativa de docentes, coordinadores y personal administrativo para verificar su robustez bajo carga real, evaluar la usabilidad (mediante escalas estandarizadas como SUS - System Usability Scale) y determinar la efectividad en la disminución de pérdidas de tiempo y equipo.
- **Variables Asociadas:** Porcentaje de reducción en tiempos de espera en ventanilla, índice de satisfacción de usuarios finales (escala 1 a 5) y porcentaje de activos prestados con trazabilidad y responsiva legal completada.
- **Entregable Verificable:** Reporte de resultados del pilotaje experimental, análisis estadístico comparativo de tiempos/mermas (antes vs. después) y plan de recomendaciones de mejora continua para la escalabilidad a otros centros de la Red UdeG.

### 4.4 Matriz de Coherencia Metodológica de Objetivos

| Nivel de Objetivo | Verbo / Acción | Pregunta a la que Responde | Etapa Metodológica | Indicador Clave de Cumplimiento | Entregable Concreto |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **General** | **Desarrollar e implementar** | ¿Cómo solucionar de fondo la vulnerabilidad, empalmes y mermas en CUTonalá? | Fin / Propósito Integral del Proyecto | Erradicación del 100% de empalmes y reducción $\ge 70\%$ en tiempos de mostrador | Plataforma SIGRE operando en entorno institucional |
| **Específico 1** | **Diagnosticar** | ¿Cuáles son las fallas exactas y demandas del flujo analógico actual? | Fase 1: Diagnóstico de Campo y Requerimientos | Mapeo del 100% de tipos de activos prestados y cuantificación de tiempos muertos | Documento de Especificación de Requerimientos y Diagnóstico |
| **Específico 2** | **Diseñar y construir** | ¿Qué arquitectura computacional resuelve de forma segura y ágil el problema? | Fase 2: Desarrollo e Ingeniería de Software | Módulos construidos: QR, checklist, responsivas y base de datos con ACID | Repositorio de código fuente funcional y manual de arquitectura |
| **Específico 3** | **Evaluar** | ¿Qué tan viable y efectiva resulta la plataforma en condiciones reales de uso? | Fase 3: Validación Empírica y Pruebas de Impacto | Satisfacción $\ge 85\%$ en SUS y 100% de trazabilidad de los bienes prestados | Informe de Resultados del Piloto y Evaluación Estadística |

---

## 5. Referencias Bibliográficas (Estilo APA 7ma Edición)

- Asociación Nacional de Universidades e Instituciones de Educación Superior. (2023). *Anuario estadístico de la educación superior 2022-2023*. ANUIES. http://www.anuies.mx/informacion-y-servicios/informacion-estadistica-de-educacion-superior
- Bernal, C. A. (2016). *Metodología de la investigación: administración, economía, humanidades y ciencias sociales* (4.ª ed.). Pearson Educación.
- Cámara de Diputados del H. Congreso de la Unión. (2017). *Ley general de protección de datos personales en posesión de sujetos obligados*. Diario Oficial de la Federación. https://www.diputados.gob.mx/LeyesBiblio/pdf/LGPDPPSO.pdf
- Centro Universitario de Tonalá. (2023). *Plan de desarrollo de CUTonalá 2019-2025: Visión 2030*. Universidad de Guadalajara. http://www.cutonala.udg.mx/transparencia/pdi
- Coordinación General de Planeación y Evaluación. (2024). *Numeralia institucional de la Red Universitaria*. Universidad de Guadalajara. http://www.cgpe.udg.mx/numeralia
- Hernández-Sampieri, R., & Mendoza Torres, C. P. (2018). *Metodología de la investigación: las rutas cuantitativa, cualitativa y mixta*. McGraw-Hill Education.
- Miranda Miranda, J. J. (2012). *Gestión de proyectos: Identificación, formulación, evaluación financiera, económica, social, ambiental* (7.ª ed.). MMEditores.
- Organización de las Naciones Unidas. (2015). *Transformar nuestro mundo: la Agenda 2030 para el Desarrollo Sostenible*. ONU. https://sdgs.un.org/es/2030agenda
- Sapag Chain, N., Sapag Chain, R., & Sapag Puelma, J. M. (2014). *Preparación y evaluación de proyectos* (6.ª ed.). McGraw-Hill Interamericana.
- Universidad de Guadalajara. (2019). *Reglamento de adquisiciones, arrendamientos y contratación de servicios de la Universidad de Guadalajara*. Gaceta de la Universidad de Guadalajara. http://www.secgen.udg.mx/normatividad/reglamentos
