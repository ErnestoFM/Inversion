import pypdf

reader = pypdf.PdfReader('docs/2026B_Equipo4_Protocolo.pdf')
page_texts = [p.extract_text() for p in reader.pages]

toc_items = [
    ('2. Planteamiento', '2. Planteamiento del Problema'),
    ('2.1 Antecedentes', '2.1 Antecedentes'),
    ('2.2 Diagnóstico', '2.2 Diagnóstico'),
    ('2.3 Causas', '2.3 Causas fundamentales'),
    ('2.4 Consecuencias', '2.4 Consecuencias'),
    ('2.5 Formulación', '2.5 Formulación de las preguntas'),
    ('3. Justificación', '3. Justificación'),
    ('3.1 Relevancia', '3.1 Relevancia institucional'),
    ('3.2 Pertinencia', '3.2 Pertinencia en la disciplina'),
    ('3.3 Vinculación', '3.3 Vinculación con los Objetivos'),
    ('4. Objetivos', '4. Objetivos de la Investigación'),
    ('4.1 Criterio', '4.1 Criterio metodológico'),
    ('4.2 Objetivo General', '4.2 Objetivo General'),
    ('4.3 Objetivos Específicos', '4.3 Objetivos Específicos Secuenciales'),
    ('4.4 Matriz', '4.4 Matriz de Coherencia'),
    ('5. Marco Teórico', '5. Marco Teórico Conceptual'),
    ('5.1 Gestión', '5.1 Gestión patrimonial'),
    ('5.2 Gobierno', '5.2 Gobierno de Tecnologías'),
    ('5.3 Arquitecturas', '5.3 Arquitecturas Web Distribuidas'),
    ('5.4 Concurrencia', '5.4 Concurrencia y Transaccionalidad'),
    ('5.5 Seguridad', '5.5 Seguridad, Identidad'),
    ('5.6 Trazabilidad', '5.6 Trazabilidad de activos'),
    ('5.7 Modelos', '5.7 Modelos de Aceptación'),
    ('6. Hipótesis', '6. Hipótesis y Sistema de Variables'),
    ('6.1 Hipótesis General', '6.1 Hipótesis General'),
    ('6.2 Hipótesis Nula', '6.2 Hipótesis Nula'),
    ('6.3 Hipótesis Alternativa', '6.3 Hipótesis Alternativa'),
    ('6.4 Hipótesis Específicas', '6.4 Hipótesis Específicas'),
    ('6.5 Operacionalización', '6.5 Operacionalización de Variables'),
    ('7. Metodología', '7. Metodología de Investigación'),
    ('7.1 Metodología de la Investigación', '7.1 Metodología de la Investigación'),
    ('7.1.1 Enfoque', '7.1.1 Enfoque epistemológico'),
    ('7.1.2 Alcance', '7.1.2 Alcance y diseño experimental'),
    ('7.1.3 Población', '7.1.3 Población, muestra'),
    ('7.1.4 Técnicas', '7.1.4 Técnicas e instrumentos'),
    ('7.1.5 Análisis de datos', '7.1.5 Análisis de datos'),
    ('7.1.6 Análisis e interpretación', '7.1.6 Análisis e interpretación de gráficos'),
    ('7.1.7 Validez', '7.1.7 Validez, confiabilidad'),
    ('7.1.8 Evidencia', '7.1.8 Evidencia y Resultados de la Evaluación'),
    ('7.2 Metodología para el Desarrollo', '7.2 Metodología para el Desarrollo'),
    ('7.2.1 Selección', '7.2.1 Selección del marco ágil'),
    ('7.2.2 Fases', '7.2.2 Fases del ciclo de vida'),
    ('8. Presupuesto', '8. Presupuesto, Requerimientos'),
    ('8.1 Requerimientos Físicos', '8.1 Requerimientos Físicos'),
    ('8.2 Requerimientos Lógicos', '8.2 Requerimientos Lógicos'),
    ('8.3 Capital Humano', '8.3 Capital Humano'),
    ('8.4 Tabla Maestra', '8.4 Tabla Maestra de Presupuesto'),
    ('8.5 Costos de Operación', '8.5 Costos de Operación'),
    ('8.6 Reconciliación', '8.6 Reconciliación Financiera'),
    ('9. Evidencias', '9. Evidencias del Proyecto'),
    ('9.1 Descripción Profunda', '9.1 Descripción Profunda'),
    ('9.2 Verificación del Despliegue', '9.2 Verificación del Despliegue'),
    ('9.3 Manual de Usuario', '9.3 Manual de Usuario'),
    ('9.4 Catálogo de Evidencias', '9.4 Catálogo de Evidencias'),
    ('9.5 Verificación Automatizada', '9.5 Verificación Automatizada'),
    ('10. Conclusiones', '10. Conclusiones del Proyecto'),
    ('10.1 Ernesto', '10.1 Conclusiones y Balance Individual: Ernesto'),
    ('10.2 Carlos', '10.2 Conclusiones y Balance Individual: Carlos'),
    ('10.3 Josue', '10.3 Conclusiones y Balance Individual: Josue'),
    ('10.4 Cumplimiento', '10.4 Cumplimiento de objetivos'),
    ('10.5 Contribución', '10.5 Contribución a la Ingeniería'),
    ('10.6 Impacto', '10.6 Impacto institucional'),
    ('10.7 Limitaciones', '10.7 Limitaciones observadas'),
    ('10.8 Recomendaciones', '10.8 Recomendaciones'),
    ('11. Cronograma', '11. Cronograma del Proyecto'),
    ('11.1 Estructura', '11.1 Estructura de Desglose'),
    ('11.2 Tabla de Actividades', '11.2 Tabla de Actividades'),
    ('11.3 Matriz de Tiempos', '11.3 Matriz de Tiempos'),
    ('11.4 Diagrama de Gantt', '11.4 Diagrama de Gantt'),
    ('12. Glosario', '12. Glosario de Términos'),
    ('13. Referencias', '13. Referencias Bibliográficas')
]

results = {}
for prefix, label in toc_items:
    for idx in range(4, len(page_texts)):
        if prefix in page_texts[idx]:
            results[prefix] = idx + 1
            break

for prefix, label in toc_items:
    print(f"{label} -> Pág. {results.get(prefix, 'NO ENCONTRADA')}")
