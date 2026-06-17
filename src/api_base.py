from abc import ABC, abstractmethod


class APIBase(ABC):
    @abstractmethod
    def get_aeroplanes(self, country: str) -> None:
        """Получение данных из API."""
        pass