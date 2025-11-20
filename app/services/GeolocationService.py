# -*- coding: utf-8 -*-
"""
Geolocation Service - Similar a Laravel Service
Calcula anillos y zonas especiales automticamente
"""
from geopy.distance import geodesic
from app.config.settings import settings


class GeolocationService:
    """Servicio para clculos de geolocalizacin"""

    # Centro de Santa Cruz de la Sierra (actualizado con datos reales)
    CENTRO_SCZ = (-17.783929, -63.180793)

    # Radios de los anillos POR SECTOR (basados en mediciones reales)
    # Los anillos en Santa Cruz NO son círculos perfectos
    ANILLOS_RADIOS_POR_SECTOR = {
        'norte': {
            1: 1.26, 2: 2.10, 3: 3.24, 4: 4.37,
            5: 5.39, 6: 6.32, 7: 7.37, 8: 8.43,
            9: 9.48, 10: 10.53
        },
        'sur': {
            1: 1.28, 2: 2.29, 3: 3.61, 4: 4.91,
            5: 5.89, 6: 7.28, 7: 8.49, 8: 9.71,
            9: 10.92, 10: 12.13
        },
        'este': {
            1: 1.32, 2: 2.23, 3: 3.15, 4: 3.93,
            5: 5.39, 6: 6.49, 7: 7.57, 8: 8.65,
            9: 9.73, 10: 10.82
        },
        'oeste': {
            1: 1.20, 2: 2.02, 3: 3.15, 4: 4.16,
            5: 5.19, 6: 6.25, 7: 7.29, 8: 8.33,
            9: 9.38, 10: 10.42
        },
    }

    # Zonas especiales con bounding boxes
    ZONAS_ESPECIALES = {
        'Equipetrol': {
            'bbox': {
                'lat_min': -17.774,
                'lat_max': -17.762,
                'lon_min': -63.200,
                'lon_max': -63.188
            },
            'zona_id': 101,
            'multiplicador_precio': 1.5  # 50% ms caro que promedio
        },
        'Urubo': {
            'bbox': {
                'lat_min': -17.68,
                'lat_max': -17.65,
                'lon_min': -63.25,
                'lon_max': -63.22
            },
            'zona_id': 102,
            'multiplicador_precio': 1.3  # 30% ms caro
        },
        'Norte': {
            'bbox': {
                'lat_min': -17.76,
                'lat_max': -17.74,
                'lon_min': -63.20,
                'lon_max': -63.17
            },
            'zona_id': 103,
            'multiplicador_precio': 1.2  # 20% ms caro
        }
    }

    @classmethod
    def calcular_distancia(cls, lat: float, lon: float) -> float:
        """
        Calcula distancia en kilmetros desde el centro de Santa Cruz

        Args:
            lat: Latitud del inmueble
            lon: Longitud del inmueble

        Returns:
            Distancia en kilmetros
        """
        punto_inmueble = (lat, lon)
        distancia = geodesic(cls.CENTRO_SCZ, punto_inmueble).kilometers
        return round(distancia, 2)

    @classmethod
    def detectar_sector(cls, lat: float, lon: float) -> str:
        """
        Detecta en qué sector cardinal está el punto

        Args:
            lat: Latitud del inmueble
            lon: Longitud del inmueble

        Returns:
            Sector: 'norte', 'sur', 'este', 'oeste'
        """
        centro_lat, centro_lon = cls.CENTRO_SCZ

        # Calcular diferencias
        diff_lat = lat - centro_lat
        diff_lon = lon - centro_lon

        # Determinar sector principal basándose en la mayor diferencia
        if abs(diff_lat) > abs(diff_lon):
            # Mayor diferencia en latitud -> Norte o Sur
            return 'norte' if diff_lat > 0 else 'sur'
        else:
            # Mayor diferencia en longitud -> Este o Oeste
            return 'este' if diff_lon > 0 else 'oeste'

    @classmethod
    def detectar_anillo(cls, lat: float, lon: float):
        """
        Detecta el anillo basado en la distancia del centro y el sector

        Args:
            lat: Latitud del inmueble
            lon: Longitud del inmueble

        Returns:
            Nmero de anillo (int) o 0 para el centro
        """
        distancia_km = cls.calcular_distancia(lat, lon)

        # Si está dentro del centro de la ciudad (< 1.0 km), considerarlo como "Centro" (anillo 0)
        # Radio calculado desde puntos reales: Norte=0.95km, Este=0.85km, Oeste=0.81km, Sur=0.86km
        if distancia_km < 1.0:
            return 0

        sector = cls.detectar_sector(lat, lon)

        # Obtener radios del sector correspondiente
        radios_sector = cls.ANILLOS_RADIOS_POR_SECTOR[sector]

        # Iterar por los anillos en orden
        for anillo in sorted(radios_sector.keys()):
            radio = radios_sector[anillo]
            if distancia_km <= radio:
                return anillo

        # Si está más allá del 10mo anillo
        return 10

    @classmethod
    def obtener_nombre_anillo(cls, anillo, distancia_km: float) -> str:
        """
        Convierte el nmero de anillo a nombre descriptivo

        Args:
            anillo: Nmero de anillo detectado
            distancia_km: Distancia real al centro

        Returns:
            Nombre descriptivo del anillo
        """
        # Simplemente devolver nombre del anillo
        return cls._formatear_nombre_anillo(anillo)

    @classmethod
    def _formatear_nombre_anillo(cls, anillo) -> str:
        """Helper para formatear el nombre de un anillo"""
        if anillo == 0:
            return "Centro"
        elif anillo == 1:
            return "1er Anillo"
        elif anillo == 2:
            return "2do Anillo"
        elif anillo == 3:
            return "3er Anillo"
        elif anillo == 4:
            return "4to Anillo"
        elif anillo == 5:
            return "5to Anillo"
        elif anillo == 6:
            return "6to Anillo"
        elif anillo == 7:
            return "7mo Anillo"
        elif anillo == 8:
            return "8vo Anillo"
        elif anillo == 9:
            return "9no Anillo"
        elif anillo == 10:
            return "10mo Anillo"
        else:
            return f"{int(anillo)}to Anillo"

    @classmethod
    def detectar_zona_especial(cls, lat: float, lon: float) -> dict | None:
        """
        Detecta si el inmueble est en una zona especial

        Args:
            lat: Latitud del inmueble
            lon: Longitud del inmueble

        Returns:
            Diccionario con info de zona o None
        """
        for zona_nombre, config in cls.ZONAS_ESPECIALES.items():
            bbox = config['bbox']

            # Verificar si est dentro del bounding box
            if (bbox['lat_min'] <= lat <= bbox['lat_max'] and
                bbox['lon_min'] <= lon <= bbox['lon_max']):

                return {
                    'nombre': zona_nombre,
                    'zona_id': config['zona_id'],
                    'multiplicador': config['multiplicador_precio']
                }

        return None

    @classmethod
    def analizar_ubicacion(cls, lat: float, lon: float) -> dict:
        """
        Anlisis completo de ubicacin

        Args:
            lat: Latitud del inmueble
            lon: Longitud del inmueble

        Returns:
            Diccionario con toda la informacin de ubicacin
        """
        anillo = cls.detectar_anillo(lat, lon)
        zona_especial = cls.detectar_zona_especial(lat, lon)
        distancia = cls.calcular_distancia(lat, lon)

        # Obtener nombre descriptivo del anillo (puede incluir "Entre X y Y")
        nombre_anillo = cls.obtener_nombre_anillo(anillo, distancia)

        resultado = {
            'anillo': anillo,
            'anillo_descripcion': nombre_anillo,
            'distancia_centro_km': distancia,
            'zona_especial': zona_especial['nombre'] if zona_especial else None,
            'zona_id': zona_especial['zona_id'] if zona_especial else anillo,
            'multiplicador_precio': zona_especial['multiplicador'] if zona_especial else 1.0
        }

        return resultado
