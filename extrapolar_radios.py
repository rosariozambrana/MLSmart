# -*- coding: utf-8 -*-
"""
Extrapola radios Este/Oeste para 5to y 6to anillo
basándose en patrones de los anillos 1-4
"""

# Radios calculados de anillos 1-4
radios_completos = {
    'norte': {1: 1.26, 2: 2.10, 3: 3.24, 4: 4.37},
    'sur': {1: 1.28, 2: 2.29, 3: 3.61, 4: 4.91},
    'este': {1: 1.32, 2: 2.23, 3: 3.15, 4: 3.93},
    'oeste': {1: 1.20, 2: 2.02, 3: 3.15, 4: 4.16},
}

# Radios parciales de 5to y 6to
radios_parciales = {
    'norte': {5: 5.39, 6: 6.32},
    'sur': {5: 5.89, 6: 7.28},
}

print("="*80)
print("ANÁLISIS DE PATRONES (Anillos 1-4)")
print("="*80)

# Calcular ratios promedio de Este/Oeste respecto a Norte/Sur
ratios_este_norte = []
ratios_este_sur = []
ratios_oeste_norte = []
ratios_oeste_sur = []

for anillo in [1, 2, 3, 4]:
    norte = radios_completos['norte'][anillo]
    sur = radios_completos['sur'][anillo]
    este = radios_completos['este'][anillo]
    oeste = radios_completos['oeste'][anillo]

    ratios_este_norte.append(este / norte)
    ratios_este_sur.append(este / sur)
    ratios_oeste_norte.append(oeste / norte)
    ratios_oeste_sur.append(oeste / sur)

    print(f"\nAnillo {anillo}:")
    print(f"  Este/Norte: {este/norte:.3f}")
    print(f"  Este/Sur:   {este/sur:.3f}")
    print(f"  Oeste/Norte: {oeste/norte:.3f}")
    print(f"  Oeste/Sur:   {oeste/sur:.3f}")

# Promedios
avg_este_norte = sum(ratios_este_norte) / len(ratios_este_norte)
avg_este_sur = sum(ratios_este_sur) / len(ratios_este_sur)
avg_oeste_norte = sum(ratios_oeste_norte) / len(ratios_oeste_norte)
avg_oeste_sur = sum(ratios_oeste_sur) / len(ratios_oeste_sur)

print("\n" + "="*80)
print("RATIOS PROMEDIO")
print("="*80)
print(f"Este/Norte promedio:  {avg_este_norte:.3f}")
print(f"Este/Sur promedio:    {avg_este_sur:.3f}")
print(f"Oeste/Norte promedio: {avg_oeste_norte:.3f}")
print(f"Oeste/Sur promedio:   {avg_oeste_sur:.3f}")

print("\n" + "="*80)
print("EXTRAPOLACIÓN PARA 5TO Y 6TO ANILLO")
print("="*80)

radios_finales = {
    'norte': {**radios_completos['norte'], **radios_parciales['norte']},
    'sur': {**radios_completos['sur'], **radios_parciales['sur']},
    'este': {**radios_completos['este']},
    'oeste': {**radios_completos['oeste']},
}

for anillo in [5, 6]:
    norte = radios_parciales['norte'][anillo]
    sur = radios_parciales['sur'][anillo]

    # Estimar Este (promedio de este/norte y este/sur)
    este_desde_norte = norte * avg_este_norte
    este_desde_sur = sur * avg_este_sur
    este_estimado = (este_desde_norte + este_desde_sur) / 2

    # Estimar Oeste (promedio de oeste/norte y oeste/sur)
    oeste_desde_norte = norte * avg_oeste_norte
    oeste_desde_sur = sur * avg_oeste_sur
    oeste_estimado = (oeste_desde_norte + oeste_desde_sur) / 2

    radios_finales['este'][anillo] = round(este_estimado, 2)
    radios_finales['oeste'][anillo] = round(oeste_estimado, 2)

    print(f"\n{anillo}to Anillo:")
    print(f"  Norte: {norte:.2f} km (real)")
    print(f"  Sur:   {sur:.2f} km (real)")
    print(f"  Este:  {este_estimado:.2f} km (estimado)")
    print(f"  Oeste: {oeste_estimado:.2f} km (estimado)")

print("\n" + "="*80)
print("CONFIGURACIÓN FINAL PARA GeolocationService.py")
print("="*80)

print("\nANILLOS_RADIOS_POR_SECTOR = {")
for sector in ['norte', 'sur', 'este', 'oeste']:
    print(f"    '{sector}': {{")
    for anillo in sorted(radios_finales[sector].keys()):
        radio = radios_finales[sector][anillo]
        print(f"        {anillo}: {radio:.2f},")
    print("    },")
print("}")

# Agregar anillos 7-10 con estimación simple (proporcional)
print("\n# Anillos 7-10 (estimación proporcional)")
print("# Puedes ajustar estos valores más adelante")
for anillo in [7, 8, 9, 10]:
    factor = anillo / 6  # Factor de crecimiento
    for sector in ['norte', 'sur', 'este', 'oeste']:
        base = radios_finales[sector][6]
        estimado = base * factor
        print(f"# {anillo}to Anillo {sector}: ~{estimado:.2f} km")
