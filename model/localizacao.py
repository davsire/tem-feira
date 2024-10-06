from exception.campo_obrigatorio_exception import CampoObrigatorioException


class Localizacao:

    def __init__(self, latitude: float, longitude: float):
        self.__validar_campos(latitude, longitude)
        self.__latitude = latitude
        self.__longitude = longitude
        self.__endereco = None

    @property
    def latitude(self) -> float:
        return self.__latitude

    @latitude.setter
    def latitude(self, latitude: float):
        self.__latitude = latitude

    @property
    def longitude(self) -> float:
        return self.__longitude

    @longitude.setter
    def longitude(self, longitude: float):
        self.__longitude = longitude

    @property
    def endereco(self) -> str:
        return self.__endereco

    @endereco.setter
    def endereco(self, endereco: str):
        self.__endereco = endereco

    def to_dict(self):
        return {
            'latitude': self.latitude,
            'longitude': self.longitude,
            'endereco': self.endereco
        }

    def __validar_campos(self, latitude: float, longitude: float):
        if not latitude or not longitude:
            raise CampoObrigatorioException('Localização')
