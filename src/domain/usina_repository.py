from abc import ABC, abstractmethod
from domain.usina import Usina


class UsinaRepository(ABC):
    @abstractmethod
    def get_by_id(self, usina_id: str) -> Usina:
        raise NotImplementedError

    @abstractmethod
    def get_all(self) -> list[Usina]:
        raise NotImplementedError
