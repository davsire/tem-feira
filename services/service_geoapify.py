import os
import requests
from dotenv import load_dotenv, find_dotenv


class ServiceGeoapify:
    __instancia = None

    def __init__(self):
        load_dotenv(find_dotenv())
        self.__api_key = os.environ.get("GEOAPIFY_KEY")
        self.__base_url = 'https://api.geoapify.com/v1'

    def __new__(cls):
        if ServiceGeoapify.__instancia is None:
            ServiceGeoapify.__instancia = object.__new__(cls)
        return ServiceGeoapify.__instancia

    def obter_endereco_por_lat_long(self, latitude: float, longitude: float) -> str | None:
        try:
            data = requests.get(f'{self.__base_url}/geocode/reverse?lat={latitude}&lon={longitude}&format=json&lang=pt&apiKey={self.__api_key}').json()
            return data['results'][0]['address_line2']
        except:
            return None
