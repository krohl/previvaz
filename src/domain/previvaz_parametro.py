from dataclasses import dataclass
from datetime import date, timedelta

from domain.semana_operativa import SemanaOperativa

@dataclass
class PrevivazParametro:
    id_rodada_smap: int
    data_rodada: date

    def __post_init__(self):
        if not isinstance(self.data_rodada, date):
            self.data_rodada = date.fromisoformat(self.data_rodada)

    @property
    def semana_operativa(self) -> SemanaOperativa:
        return SemanaOperativa.from_date(self.data_rodada)

    @property
    def inicio_observado(self) -> date:
        """ Retorna a primeira data de dados observados necessários para a rodada Previvaz:
            - cinco semanas antes da última data de dados observados
        """
        return SemanaOperativa.from_date(self.fim_observado - timedelta(days=34)).start_date

    @property
    def fim_observado(self) -> date:
        """ Retorna a última data de dados observados necessários para a rodada Previvaz:
            - um dia antes do começo da semana operativa da rodada
        """
        return self.inicio_previsto - timedelta(days=1)

    @property
    def inicio_previsto(self) -> date:
        """ Retorna a primeira data de dados previstos necessários para a rodada Previvaz:
            - a partir do começo da semana operativa da rodada
        """
        return self.semana_operativa.start_date

    @property
    def fim_previsto(self) -> date:
        """ Retorna a última data de dados previstos necessários para a rodada Previvaz:
            - cinco semanas após o fim da semana opertiva da rodada
        """
        return self.semana_operativa.end_date + timedelta(days=35)
