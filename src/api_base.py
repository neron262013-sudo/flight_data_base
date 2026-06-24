from abc import ABC, abstractmethod


class APIBase(ABC):
    """Базовый абстрактный класс для работы с внешними API."""

    @abstractmethod
    def get_aeroplanes(self, country: str) -> None:
        """Получение данных из API."""
        pass
