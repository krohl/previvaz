from datetime import date

from domain.vazao import FonteVazao, TipoVazao, VazaoDiaria, VazaoDiariaSmap
from domain.vazao_repository import VazaoDiariaRepository


class VazaoDiariaInMemoryRepository(VazaoDiariaRepository):
    def __init__(self):
        self.vazoes: list[VazaoDiaria] = []

    def get_by_usina_ids(
        self, usina_ids: int, start_date: date, end_date: date, tipo_vazao: TipoVazao, fonte_vazao: FonteVazao
    ) -> list[VazaoDiaria]:
        return [
            vazao
            for vazao in self.vazoes
            if vazao.data >= start_date
            and vazao.data <= end_date
            and vazao.id_usina in usina_ids
            and vazao.tipo == tipo_vazao
            and vazao.fonte == fonte_vazao
        ]

    def fetch_from_rodada_smap(
        self, id_rodada_smap: int, usina_ids: int, start_date: date, end_date: date
    ) -> list[VazaoDiaria]:
        return [
            vazao
            for vazao in self.vazoes
            if vazao.data >= start_date
            and vazao.data <= end_date
            and vazao.id_usina in usina_ids
            and isinstance(vazao, VazaoDiariaSmap)
            and vazao.id_rodada_smap == id_rodada_smap
        ]

    def add(self, vazao: VazaoDiaria | list[VazaoDiariaSmap]):
        if isinstance(vazao, list):
            self.vazoes.extend(vazao)
        else:
            self.vazoes.append(vazao)
