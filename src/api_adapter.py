from requests import get

from src.api_base import APIBase


class APIAdapter(APIBase):
    """Адаптер для получения данных о странах и самолетах через внешние API."""

    def __init__(self) -> None:
        self.openstreetmap_url = "https://nominatim.openstreetmap.org/search"
        self.opensky_url = "https://opensky-network.org/api/states/all"

    def get_aeroplanes(self, country: str) -> dict:
        """
        Получает список самолетов, находящихся в воздушном пространстве указанной страны.

        :param country: Название страны.
        :return: Ответ OpenSky API в формате словаря.
        """

        # Headers с user-agent - обязательный параметр при запросе к nominatim.openstreetmap.
        # Вы можете использовать любое название вместо test-app/1.0, например просто test-app.
        headers = {
            "User-Agent": "test-app/1.0",
        }

        # Указываем параметры: в каком формате возвращать данные и максимальную длину списка стран в ответе.
        params = {
            "country": country,
            "format": "json",
            "limit": 1,
        }

        response = get(url=self.openstreetmap_url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()

        # Страна не найдена или API вернул пустой ответ.
        if not data:
            return {"states": []}

        geo_coordinates = data[0].get("boundingbox")

        # Параметры для фильтрации самолетов по их географическим координатам.
        params = {
            "lamin": geo_coordinates[0],
            "lamax": geo_coordinates[1],
            "lomin": geo_coordinates[2],
            "lomax": geo_coordinates[3],
        }

        response = get(url=self.opensky_url, params=params)
        response.raise_for_status()
        return response.json()

    def get_country(self, country: str):
        """
        Получает границы страны.
        """

        headers = {"User-Agent": "test-app/1.0"}

        params = {
            "country": country,
            "format": "json",
            "limit": 1,
        }

        response = get(url=self.openstreetmap_url, params=params, headers=headers)

        response.raise_for_status()
        data = response.json()

        if not data:
            return None

        return data[0].get("boundingbox")
