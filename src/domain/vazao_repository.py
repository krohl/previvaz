from abc import ABC, abstractmethod
from datetime import date

from domain.vazao import FonteVazao, TipoVazao, VazaoDiaria


class VazaoDiariaRepository(ABC):
    @abstractmethod
    def get_by_usina_ids(
        self, usina_ids: int, start_date: date, end_date: date, tipo_vazao: TipoVazao, fonte_vazao: FonteVazao
    ) -> list[VazaoDiaria]:
        raise NotImplementedError

    @abstractmethod
    def fetch_from_rodada_smap(
        self, id_rodada_smap: int, usina_ids: int, start_date: date, end_date: date
    ) -> list[VazaoDiaria]:
        raise NotImplementedError
