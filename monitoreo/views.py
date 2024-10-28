from django.shortcuts import render
import requests


def obtener_info_ip(ip):
    try:
        response = requests.get(f"https://ipinfo.io/{ip}/json")
        if response.status_code == 200:
            datos = response.json()
            return {
                'ciudad': datos.get('city', ''),
                'region': datos.get('region', ''),
                'pais': datos.get('country', ''),
                'organizacion': datos.get('org', '')
            }
    except requests.RequestException:
        pass  # En caso de error de red, retornamos valores vacíos
    
    # Retorna valores vacíos si no se puede obtener la información
    return {'ciudad': '', 'region': '', 'pais': '', 'organizacion': ''}