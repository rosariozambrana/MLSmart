# -*- coding: utf-8 -*-
"""
Script para calcular radios de anillos desde coordenadas reales
"""
from geopy.distance import geodesic

centro = (-17.783929, -63.180793)

anillos = {
    '1er Anillo': {
        'inicio_norte': (-17.774381, -63.181774),
        'inicio_sur': (-17.792283, -63.179191),
        'inicio_este': (-17.782755, -63.171811),
        'inicio_oeste': (-17.784396, -63.189418),
        'fin_norte': (-17.770796, -63.181638),
        'fin_sur': (-17.798361, -63.178183),
        'fin_este': (-17.782310, -63.165139),
        'fin_oeste': (-17.784975, -63.194683)
    },
    '2do Anillo': {
        'inicio_norte': (-17.769718, -63.181996),
        'inicio_sur': (-17.799325, -63.178958),
        'inicio_este': (-17.781799, -63.164067),
        'inicio_oeste': (-17.785372, -63.195219),
        'fin_norte': (-17.760188, -63.179434),
        'fin_sur': (-17.809590, -63.176873),
        'fin_este': (-17.781288, -63.155728),
        'fin_oeste': (-17.785882, -63.204392)
    },
    '3er Anillo': {
        'inicio_norte': (-17.759291, -63.179918),
        'inicio_sur': (-17.811180, -63.178116),
        'inicio_este': (-17.781690, -63.154254),
        'inicio_oeste': (-17.785007, -63.205219),
        'fin_norte': (-17.750239, -63.176215),
        'fin_sur': (-17.821774, -63.178205),
        'fin_este': (-17.780159, -63.148274),
        'fin_oeste': (-17.785772, -63.215750)
    },
    '4to Anillo': {
        'inicio_norte': (-17.749511, -63.175932),
        'inicio_sur': (-17.823307, -63.184796),
        'inicio_este': (-17.778880, -63.146785),
        'inicio_oeste': (-17.788526, -63.217151),
        'fin_norte': (-17.740537, -63.172245),
        'fin_sur': (-17.832708, -63.186496),
        'fin_este': (-17.776635, -63.141860),
        'fin_oeste': (-17.786812, -63.222421)
    },
    '5to Anillo': {
        'inicio_norte': (-17.739884, -63.172443),
        'inicio_sur': (-17.831633, -63.176568),
        'fin_norte': (-17.732498, -63.169144),
        'fin_sur': (-17.842306, -63.175258),
    },
    '6to Anillo': {
        'inicio_norte': (-17.731548, -63.168787),
        'inicio_sur': (-17.845000, -63.181566),
        'fin_norte': (-17.725084, -63.165963),
        'fin_sur': (-17.854231, -63.184963),
    }
}

print("="*80)
print("CÁLCULO DE RADIOS POR SECTOR")
print("="*80)

radios_por_sector = {
    'norte': {},
    'sur': {},
    'este': {},
    'oeste': {}
}

for anillo_num, (anillo_nombre, puntos) in enumerate(anillos.items(), 1):
    print(f"\n{anillo_nombre}:")
    print("-" * 80)

    # Calcular distancias
    distancias = {}
    for direccion, coords in puntos.items():
        dist = geodesic(centro, coords).kilometers
        distancias[direccion] = dist
        print(f"  {direccion:20s}: {dist:.2f} km")

    # Extraer por sector
    if 'inicio_norte' in distancias and 'fin_norte' in distancias:
        radios_por_sector['norte'][anillo_num] = (
            distancias['inicio_norte'],
            distancias['fin_norte']
        )

    if 'inicio_sur' in distancias and 'fin_sur' in distancias:
        radios_por_sector['sur'][anillo_num] = (
            distancias['inicio_sur'],
            distancias['fin_sur']
        )

    if 'inicio_este' in distancias and 'fin_este' in distancias:
        radios_por_sector['este'][anillo_num] = (
            distancias['inicio_este'],
            distancias['fin_este']
        )

    if 'inicio_oeste' in distancias and 'fin_oeste' in distancias:
        radios_por_sector['oeste'][anillo_num] = (
            distancias['inicio_oeste'],
            distancias['fin_oeste']
        )

print("\n" + "="*80)
print("RESUMEN: RADIOS POR SECTOR (inicio, fin)")
print("="*80)

for sector, anillos_dict in radios_por_sector.items():
    print(f"\n{sector.upper()}:")
    for anillo, (inicio, fin) in anillos_dict.items():
        promedio = (inicio + fin) / 2
        print(f"  {anillo}er/do/to Anillo: {inicio:.2f} - {fin:.2f} km (promedio: {promedio:.2f} km)")

print("\n" + "="*80)
print("CÓDIGO PARA GeolocationService.py")
print("="*80)

print("\nANILLOS_RADIOS_POR_SECTOR = {")
for sector, anillos_dict in radios_por_sector.items():
    print(f"    '{sector}': {{")
    for anillo, (inicio, fin) in anillos_dict.items():
        promedio = (inicio + fin) / 2
        print(f"        {anillo}: {promedio:.2f},")
    print("    },")
print("}")
