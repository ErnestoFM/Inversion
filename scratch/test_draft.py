# -*- coding: utf-8 -*-
import sys

def verify_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        md = f.read()

    # 1. Reparto de utilidades y Cash Sweep 70%
    assert '$23,670' in md and '$55,230' in md and '$78,900' in md, 'Falla 1'
    assert '$124,770' in md and '31.2' in md, 'Falla 2'
    assert '$142,554' in md and '$154,246' in md and '$296,800' in md, 'Falla 3'
    assert '$252,280' in md and '$44,520' in md, 'Falla 4'

    # 2. Nómina escalonada
    assert 'Mes 22' in md, 'Falla 5'
    assert '$28,000' in md and '$30,000' in md and '$62,000' in md, 'Falla 6'
    assert '$120,000' in md and '$63,000' in md and '$57,000' in md, 'Falla 7'
    assert '$240,000' in md, 'Falla 8'

    # 3. Doble conteo CAPEX y estrés financiero
    assert 'estrés financiero' in md.lower(), 'Falla 9'
    assert '$46,984.47' in md or '46,984.47' in md, 'Falla 10'
    assert '24.27%' in md, 'Falla 11'
    assert '$13,500' in md and '$6,500' in md and '$20,000' in md, 'Falla 12'
    assert '$180,000' in md, 'Falla 13'

    # 4. TIR Inversionista
    assert '1.21M' in md and '1.93M' in md, 'Falla 14'
    assert '32.0%' in md, 'Falla 15'
    assert '387.2k' in md and '617.6k' in md, 'Falla 16'
    assert '$58,080' in md and '$92,640' in md, 'Falla 17'
    assert '21.20%' in md, 'Falla 18'

    # 5. Umbral de viabilidad
    assert '18.12' in md, 'Falla 19'
    assert '19 planteles' in md or '19 sedes' in md or '19' in md, 'Falla 20'
    assert '9.7%' in md, 'Falla 21'

    # 6. Contratos Año 1
    assert '3 planteles' in md.lower() or '3 sedes' in md.lower(), 'Falla 22'
    assert '2 contratos comerciales' in md.lower() or '2 prepas comerciales' in md.lower(), 'Falla 23'
    assert 'cutonalá' in md.lower(), 'Falla 24'

    # 7. Objetivo 3
    assert 'mes 22' in md.lower(), 'Falla 25'

    # 8. FODA O4
    assert '32,500' in md, 'Falla 26'

    # 9. Geografía UdeG
    assert 'cutonalá' in md.lower() and 'cutlaquepaque' in md.lower(), 'Falla 27'
    assert 'multitemáticos metropolitanos' in md.lower() or 'multitemático' in md.lower(), 'Falla 28'
    assert 'mayo de 2026' in md.lower(), 'Falla 29'

    # 10. SIIAU
    assert 'micro-custodia' in md.lower() or 'microcustodia' in md.lower(), 'Falla 30'

    # 11. Citas APA
    assert 'sauro' in md.lower() and 'lewis' in md.lower() and '2012' in md and '68' in md, 'Falla 31'
    assert 'bangor' in md.lower() and '2008' in md, 'Falla 32'
    assert 'sapag chain' in md.lower() and '2014' in md, 'Falla 33'
    assert '117.31' in md and '117,310' in md, 'Falla 34'
    assert '3,126.41' in md or '3,126' in md, 'Falla 35'

    # 12. Cuadre aritmético en Tabla 12
    assert '($95,000)' in md, 'Falla 36'
    assert '\u2212$32,000' in md, 'Falla 37'
    assert '($20,100)' in md, 'Falla 38'
    assert '+$78,900' in md, 'Falla 39'
    assert '+$296,800' in md, 'Falla 40'

    # 13. Tablas 1 a 13 con llamadas previas
    for i in range(1, 14):
        assert f'Tabla {i}' in md, f'Falta Tabla {i}'

    # 14. Figuras 1 a 11
    for i in range(1, 12):
        assert f'Figura {i}' in md, f'Falta Figura {i}'

    # 15. Rutas de capturas en Markdown
    assert 'docs/pruebas/screenshots/10_distribucion_puntajes_sus.png' in md, 'Falla img 1'
    assert 'docs/pruebas/screenshots/05_canvas_firma_digital.png' in md, 'Falla img 2'
    assert 'docs/pruebas/screenshots/08_dashboard_ejecutivo.png' in md, 'Falla img 3'
    assert 'docs/graficos/foda_oficial_sigre.jpg' in md, 'Falla img 4'

    # 16. Anexos
    assert 'Anexo A' in md and 'Anexo B' in md, 'Falla anexos'

    print('TODAS LAS 40+ ASERCIONES PASARON PERFECTAMENTE!')

if __name__ == '__main__':
    verify_file('scratch/draft_condensed.md')
