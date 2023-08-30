from dataclasses import dataclass
from datetime import date, timedelta

from domain.semana_operativa import SemanaOperativa

@dataclass
class PrevivazParametro:
    id_rodada_smap: int
    data_rodada: date
    data_deck_smap: date

    def __post_init__(self):
        if not isinstance(self.data_rodada, date):
            self.data_rodada = date.fromisoformat(self.data_rodada)

        if not isinstance(self.data_deck_smap, date):
            self.data_deck_smap = date.fromisoformat(self.data_deck_smap)

    @property
    def semana_operativa(self) -> SemanaOperativa:
        return SemanaOperativa.from_date(self.data_deck_smap).next()

    @property
    def inicio_observado(self) -> date:
        """ Retorna a primeira data de dados observados necessários para a rodada Previvaz:
            - cinco semanas antes da última data de dados observados
        """
        return self.semana_operativa.previous(5).start_date

    @property
    def fim_observado(self) -> date:
        """ Retorna a última data de dados observados necessários para a rodada Previvaz:
            - um dia antes do começo da semana operativa da rodada
        """
        return self.data_deck_smap - timedelta(days=1)

    @property
    def inicio_previsto(self) -> date:
        """ Retorna a primeira data de dados previstos necessários para a rodada Previvaz:
            - a partir do começo da semana operativa da rodada
        """
        return self.data_deck_smap

    @property
    def fim_previsto(self) -> date:
        """ Retorna a última data de dados previstos necessários para a rodada Previvaz:
            - cinco semanas após o fim da semana opertiva da rodada
        """
        return self.semana_operativa.next(4).end_date
