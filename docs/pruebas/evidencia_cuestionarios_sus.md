# Evidencia de Evaluación de Usabilidad: Cuestionarios SUS (n = 50)

**Proyecto:** Plataforma SIGRE (Sistema Integral de Gestión de Recursos y Espacios)  
**Institución:** Universidad de Guadalajara — Centro Universitario de Tonalá (CUTonalá)  
**Asignatura:** Metodología y Práctica de la Investigación (Ciclo 2026B)  
**Instrumento:** *System Usability Scale* (SUS) de John Brooke (1996)  
**Fecha de Aplicación de Pruebas:** 26 de octubre al 06 de noviembre de 2026 (Semana 14)  
**Diseño Muestral:** Muestra no probabilística por conveniencia de $n = 50$ usuarios activos de CUTonalá (32 estudiantes, 12 docentes, 6 operadores de almacén).  
**Consentimiento y Privacidad:** Instrumento digital autoadministrado en Google Forms bajo dominio UdeG, precedido de pantalla obligatoria de consentimiento informado y Aviso de Privacidad simplificado. Las direcciones de correo electrónico fueron disociadas del dataset analítico para garantizar el estricto anonimato del participante.

---

## 1. Estructura del Instrumento Administrado

El instrumento fue implementado en formato digital estandarizado y aplicado inmediatamente después de que cada participante interactuara de forma guiada con el circuito de software de SIGRE (solicitud de préstamo de equipo de laboratorio, firma digital en Canvas, emisión de responsiva y escaneo óptico QR en mostrador).

### Escala de Respuesta (Likert de 5 Puntos):
- **1:** Totalmente en desacuerdo
- **2:** En desacuerdo
- **3:** Neutral / Indiferente
- **4:** De acuerdo
- **5:** Totalmente de acuerdo

### Reactivos Estandarizados:
1. **R1 (+):** Creo que me gustaría utilizar este sistema con frecuencia.
2. **R2 (−):** Encontré el sistema innecesariamente complejo.
3. **R3 (+):** Pensé que el sistema era fácil de usar.
4. **R4 (−):** Creo que necesitaría el apoyo de un técnico para poder utilizar este sistema.
5. **R5 (+):** Encontré que las diversas funciones del sistema estaban bien integradas.
6. **R6 (−):** Pensé que había demasiada inconsistencia en este sistema.
7. **R7 (+):** Imagino que la mayoría de las personas aprenderían a utilizar este sistema muy rápidamente.
8. **R8 (−):** Encontré el sistema muy engorroso o pesado de utilizar.
9. **R9 (+):** Me sentí muy seguro y confiado al utilizar el sistema.
10. **R10 (−):** Necesité aprender muchas cosas antes de poder utilizar este sistema.

---

## 2. Resumen Estadístico y Fiabilidad Psicométrica

- **Puntaje Promedio Global:** **82.85 puntos** ($s = 10.91$ pts, mediana = 82.5 pts).
- **Consistencia Interna (Alfa de Cronbach):** $\alpha = 0.892 \approx 0.892$ (alta fiabilidad psicométrica; George & Mallery, 2003).
  - Varianza del total bruto ($Var(X)$): **19.0208**
  - Sumatoria de varianzas de los ítems ($\sum s_j^2$): **3.7555**
  - Fórmula: $\alpha = \frac{10}{9} \left(1 - \frac{3.7555}{19.0208}\right) = 0.892$
- **Inferencia Estadística:**
  - **Intervalo de Confianza al 95%:** $IC_{95\%} = [79.75, 85.95]$ puntos.
  - **Prueba t de Una Muestra ($H_0: \mu \le 80$ vs $H_1: \mu > 80$):**
    $$t(49) = \frac{82.85 - 80.00}{10.91 / \sqrt{50}} = 1.848, \quad p = 0.035 < 0.05$$
    Se rechaza $H_0$ con un 95% de nivel de confianza, demostrando que la usabilidad percibida supera de forma estadísticamente significativa el benchmark de excelencia.
- **Calificación Cualitativa:** Grado **"Excelente" (Grado A, Percentil ~92)** conforme a las escalas normalizadas de Sauro y Lewis (2012) y Bangor, Kortum y Miller (2008, 2009), superando holgadamente el promedio estándar de la industria fijado en 68.0 puntos.
- **Veredicto Hipótesis $HE\text{-}3$:** **Aceptada.** El sistema superó de manera concluyente el umbral mínimo fijado de 80 puntos de aceptabilidad.

### Desglose por Estamento Institucional:
| Estamento / Rol | Muestra ($n$) | Media SUS | Desv. Est. ($s$) | Calificación Sauro & Lewis (2012) | Estatus $HE\text{-}3$ |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Estudiantes** | 32 | **83.28 pts** | 11.21 pts | Excelente (Grado A) | Cumple (≥ 80) |
| **Docentes / Investigadores** | 12 | **81.25 pts** | 9.91 pts | Excelente (Grado A) | Cumple (≥ 80) |
| **Operadores de Almacén** | 6 | **83.75 pts** | 12.72 pts | Excelente (Grado A) | Cumple (≥ 80) |
| **TOTAL MUESTRAL** | **50** | **82.85 pts** | **10.91 pts** | **Excelente (Grado A)** | **HIPÓTESIS VERIFICADA** |

---

## 3. Matriz Completa de Respuestas Brutas (n = 50)

Archivos fuente originales disponibles en el repositorio:
- **CSV:** [`docs/pruebas/cuestionarios_sus_n50.csv`](cuestionarios_sus_n50.csv)
- **Excel:** [`docs/pruebas/cuestionarios_sus_n50.xlsx`](cuestionarios_sus_n50.xlsx)

| ID Sujeto | Rol | Programa / Adscripción | Fecha | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 | R10 | Puntaje SUS |
| :---: | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `EST-2026B-01` | Estudiante | Lic. en Ciencias Computacionales | 2026-10-26 | 5 | 2 | 5 | 1 | 5 | 2 | 5 | 1 | 5 | 1 | **95.0** |
| `EST-2026B-02` | Estudiante | Ing. en Computación | 2026-10-26 | 4 | 1 | 4 | 2 | 5 | 1 | 5 | 2 | 4 | 1 | **87.5** |
| `EST-2026B-03` | Estudiante | Lic. en Ciencias Computacionales | 2026-10-27 | 4 | 1 | 5 | 1 | 5 | 1 | 4 | 1 | 4 | 1 | **92.5** |
| `EST-2026B-04` | Estudiante | Ing. en Ciencias Computacionales | 2026-10-27 | 4 | 2 | 4 | 2 | 4 | 1 | 5 | 2 | 5 | 1 | **85.0** |
| `EST-2026B-05` | Estudiante | Ing. en Nanotecnología | 2026-10-27 | 5 | 1 | 5 | 1 | 5 | 1 | 5 | 2 | 5 | 2 | **95.0** |
| `EST-2026B-06` | Estudiante | Lic. en Ciencias Computacionales | 2026-10-28 | 4 | 2 | 4 | 2 | 3 | 2 | 4 | 2 | 4 | 3 | **70.0** |
| `EST-2026B-07` | Estudiante | Lic. en Diseño y Artesanía | 2026-10-28 | 4 | 2 | 5 | 2 | 4 | 2 | 4 | 2 | 4 | 2 | **77.5** |
| `EST-2026B-08` | Estudiante | Ing. en Energía | 2026-10-28 | 5 | 1 | 4 | 2 | 4 | 1 | 5 | 2 | 4 | 2 | **85.0** |
| `EST-2026B-09` | Estudiante | Lic. en Ciencias Computacionales | 2026-10-29 | 4 | 2 | 3 | 3 | 3 | 3 | 3 | 2 | 4 | 2 | **62.5** |
| `EST-2026B-10` | Estudiante | Lic. en Administración de Negocios | 2026-10-29 | 4 | 1 | 4 | 2 | 5 | 2 | 4 | 2 | 4 | 2 | **80.0** |
| `EST-2026B-11` | Estudiante | Lic. en Contaduría Pública | 2026-10-30 | 4 | 2 | 3 | 3 | 4 | 2 | 3 | 3 | 4 | 3 | **62.5** |
| `EST-2026B-12` | Estudiante | Lic. en Ciencias Computacionales | 2026-10-30 | 3 | 2 | 3 | 2 | 3 | 1 | 4 | 2 | 4 | 3 | **67.5** |
| `EST-2026B-13` | Estudiante | Ing. en Ciencias Computacionales | 2026-10-30 | 5 | 1 | 5 | 1 | 5 | 1 | 5 | 1 | 5 | 1 | **100.0** |
| `EST-2026B-14` | Estudiante | Lic. en Historia del Arte | 2026-11-03 | 4 | 1 | 5 | 2 | 4 | 2 | 5 | 1 | 5 | 2 | **87.5** |
| `EST-2026B-15` | Estudiante | Lic. en Ciencias Computacionales | 2026-11-03 | 4 | 1 | 4 | 1 | 4 | 1 | 4 | 2 | 4 | 2 | **82.5** |
| `EST-2026B-16` | Estudiante | Ing. en Computación | 2026-11-03 | 4 | 2 | 5 | 2 | 4 | 1 | 5 | 1 | 4 | 1 | **87.5** |
| `EST-2026B-17` | Estudiante | Lic. en Ciencias Computacionales | 2026-11-03 | 4 | 1 | 5 | 1 | 5 | 2 | 4 | 2 | 5 | 1 | **90.0** |
| `EST-2026B-18` | Estudiante | Ing. en Ciencias Computacionales | 2026-11-04 | 4 | 2 | 5 | 1 | 4 | 2 | 4 | 2 | 5 | 2 | **82.5** |
| `EST-2026B-19` | Estudiante | Lic. en Estudios Liberales | 2026-11-04 | 5 | 1 | 5 | 1 | 5 | 2 | 5 | 1 | 5 | 1 | **97.5** |
| `EST-2026B-20` | Estudiante | Lic. en Ciencias Computacionales | 2026-11-04 | 4 | 2 | 3 | 2 | 3 | 2 | 4 | 2 | 4 | 2 | **70.0** |
| `EST-2026B-21` | Estudiante | Ing. en Ciencias Computacionales | 2026-11-04 | 5 | 2 | 5 | 1 | 5 | 1 | 5 | 2 | 5 | 1 | **95.0** |
| `EST-2026B-22` | Estudiante | Lic. en Diseño y Artesanía | 2026-11-05 | 5 | 1 | 5 | 1 | 4 | 1 | 5 | 1 | 5 | 1 | **97.5** |
| `EST-2026B-23` | Estudiante | Lic. en Ciencias Computacionales | 2026-11-05 | 4 | 3 | 4 | 3 | 4 | 2 | 4 | 3 | 4 | 2 | **67.5** |
| `EST-2026B-24` | Estudiante | Lic. en Contaduría Pública | 2026-11-05 | 4 | 2 | 4 | 1 | 5 | 2 | 4 | 1 | 5 | 2 | **85.0** |
| `EST-2026B-25` | Estudiante | Ing. en Computación | 2026-11-05 | 5 | 2 | 4 | 1 | 5 | 1 | 5 | 1 | 4 | 1 | **92.5** |
| `EST-2026B-26` | Estudiante | Lic. en Ciencias Computacionales | 2026-11-05 | 4 | 1 | 4 | 2 | 5 | 2 | 5 | 1 | 5 | 1 | **90.0** |
| `EST-2026B-27` | Estudiante | Lic. en Ciencias Computacionales | 2026-11-06 | 4 | 2 | 3 | 2 | 4 | 2 | 4 | 2 | 4 | 2 | **72.5** |
| `EST-2026B-28` | Estudiante | Ing. en Nanotecnología | 2026-11-06 | 5 | 2 | 4 | 2 | 4 | 2 | 4 | 1 | 4 | 2 | **80.0** |
| `EST-2026B-29` | Estudiante | Lic. en Ciencias Computacionales | 2026-11-06 | 5 | 1 | 5 | 1 | 5 | 1 | 5 | 2 | 5 | 1 | **97.5** |
| `EST-2026B-30` | Estudiante | Ing. en Ciencias Computacionales | 2026-11-06 | 4 | 2 | 4 | 2 | 5 | 2 | 4 | 2 | 4 | 2 | **77.5** |
| `EST-2026B-31` | Estudiante | Lic. en Ciencias Computacionales | 2026-11-06 | 3 | 3 | 4 | 3 | 4 | 2 | 4 | 2 | 3 | 2 | **65.0** |
| `EST-2026B-32` | Estudiante | Lic. en Ciencias Computacionales | 2026-11-06 | 5 | 2 | 5 | 2 | 5 | 2 | 4 | 1 | 5 | 2 | **87.5** |
| `DOC-2026B-01` | Docente | Dpto. de Tecnologías de Información | 2026-10-27 | 4 | 3 | 4 | 2 | 4 | 2 | 4 | 2 | 4 | 2 | **72.5** |
| `DOC-2026B-02` | Docente | Dpto. de Ciencias Computacionales | 2026-10-28 | 5 | 1 | 4 | 1 | 5 | 1 | 5 | 1 | 5 | 1 | **97.5** |
| `DOC-2026B-03` | Docente | Dpto. de Ingenierías | 2026-10-29 | 5 | 2 | 5 | 2 | 5 | 1 | 4 | 2 | 5 | 1 | **90.0** |
| `DOC-2026B-04` | Docente | Dpto. de Tecnologías de Información | 2026-10-30 | 4 | 2 | 4 | 2 | 4 | 2 | 4 | 2 | 4 | 2 | **75.0** |
| `DOC-2026B-05` | Docente | Dpto. de Emprendimiento y Gestión | 2026-11-03 | 5 | 2 | 4 | 2 | 5 | 2 | 5 | 1 | 4 | 1 | **87.5** |
| `DOC-2026B-06` | Docente | Dpto. de Ciencias Computacionales | 2026-11-03 | 4 | 2 | 4 | 2 | 4 | 2 | 4 | 2 | 4 | 2 | **75.0** |
| `DOC-2026B-07` | Docente | Dpto. de Artes y Humanidades | 2026-11-04 | 5 | 2 | 4 | 2 | 5 | 2 | 4 | 2 | 5 | 1 | **85.0** |
| `DOC-2026B-08` | Docente | Dpto. de Tecnologías de Información | 2026-11-04 | 4 | 1 | 5 | 1 | 4 | 1 | 5 | 2 | 5 | 1 | **92.5** |
| `DOC-2026B-09` | Docente | Dpto. de Ciencias Exactas y Metodología | 2026-11-05 | 3 | 2 | 4 | 2 | 4 | 3 | 3 | 3 | 4 | 2 | **65.0** |
| `DOC-2026B-10` | Docente | Dpto. de Ciencias Computacionales | 2026-11-05 | 5 | 2 | 4 | 2 | 5 | 2 | 4 | 2 | 5 | 1 | **85.0** |
| `DOC-2026B-11` | Docente | Dpto. de Ingenierías | 2026-11-06 | 4 | 1 | 4 | 2 | 4 | 2 | 4 | 2 | 5 | 2 | **80.0** |
| `DOC-2026B-12` | Docente | Dpto. de Tecnologías de Información | 2026-11-06 | 4 | 3 | 4 | 3 | 4 | 2 | 4 | 2 | 4 | 2 | **70.0** |
| `ALM-2026B-01` | Operador de Almacén | Ventanilla Almacén General (Edificio A) | 2026-10-26 | 5 | 1 | 5 | 1 | 5 | 1 | 5 | 1 | 4 | 2 | **95.0** |
| `ALM-2026B-02` | Operador de Almacén | Ventanilla Préstamos Cómputo (Laboratorio L3) | 2026-10-28 | 4 | 2 | 4 | 3 | 5 | 2 | 4 | 2 | 4 | 2 | **75.0** |
| `ALM-2026B-03` | Operador de Almacén | Ventanilla Almacén Cineteca y Audiovisual | 2026-10-30 | 3 | 3 | 4 | 3 | 4 | 2 | 4 | 2 | 3 | 3 | **62.5** |
| `ALM-2026B-04` | Operador de Almacén | Ventanilla Almacén General (Edificio B) | 2026-11-03 | 5 | 2 | 4 | 1 | 4 | 1 | 5 | 2 | 5 | 2 | **87.5** |
| `ALM-2026B-05` | Operador de Almacén | Ventanilla Laboratorios de Electrónica | 2026-11-05 | 5 | 1 | 4 | 2 | 4 | 2 | 5 | 2 | 5 | 1 | **87.5** |
| `ALM-2026B-06` | Operador de Almacén | Ventanilla Almacén Deportivo y Recreativo | 2026-11-06 | 5 | 1 | 5 | 1 | 5 | 2 | 5 | 1 | 5 | 2 | **95.0** |

---

## 4. Metodología de Cálculo y Normalización del Puntaje SUS

El cálculo para cada participante $i$ ($i = 1, \dots, 50$) se ejecuta de acuerdo con el algoritmo estándar formulado por Brooke (1996):

1. **Para reactivos impares ($j = 1, 3, 5, 7, 9$):**  
   $$C_{i, j} = R_{i, j} - 1$$
2. **Para reactivos pares ($j = 2, 4, 6, 8, 10$):**  
   $$C_{i, j} = 5 - R_{i, j}$$
3. **Puntaje Compuesto Normalizado:**  
   $$SUS_i = 2.5 \times \sum_{j=1}^{10} C_{i, j}$$

La sumatoria total de contribuciones netas obtenidas por la muestra de 50 sujetos asciende a **1,657 puntos netos**, lo cual arroja un promedio muestral estricto de:

$$\overline{SUS} = \frac{1657 \times 2.5}{50} = \frac{4142.5}{50} = 82.85\text{ puntos}$$
