from domain.usina import Usina
from domain.usina_repository import UsinaRepository


class UsinaInMemoryRepository(UsinaRepository):

    def __init__(self) -> None:
        self.usinas: list[Usina] = []

    def get_by_id(self, usina_id: str) -> Usina:
        return next(u for u in self.usinas if u.id == usina_id)

    def get_all(self) -> list[Usina]:
        return self.usinas

    def add(self, usina: Usina):
        self.usinas.append(usina)