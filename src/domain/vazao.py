from dataclasses import dataclass
from datetime import date
from enum import Enum
from itertools import groupby

from domain.semana_operativa import SemanaOperativa


class TipoVazao(Enum):
    NATURAL = 'natural'
    INCREMENTAL = 'incremental'


class FonteVazao(Enum):
    ACOMPH = 'acomph'
    SMAP = 'smap'
    CALCULATED_WEEKLY = 'semanal_calculada'


@dataclass(frozen=True)
class VazaoDiaria:
    id_usina: str
    data: date
    valor: float
    tipo: TipoVazao
    fonte: FonteVazao

    def __post_init__(self):
        if not isinstance(self.valor, float):
            raise TypeError(f'Invalid type <{type(self.valor)}> for attribute <valor>.')
        if self.valor < 0:
            raise ValueError(f'Invalid value <{self.valor}> for attribute <valor>.')


@dataclass(frozen=True)
class VazaoDiariaSmap(VazaoDiaria):
    id_rodada_smap: int


@dataclass(frozen=True)
class VazaoSemanal:
    id_usina: str
    op_week: SemanaOperativa
    valor: float
    tipo: TipoVazao
    fonte: FonteVazao


class VazaoSemanalFactory:
    @classmethod
    def from_vazoes_diarias(cls, vazoes_diarias: list[VazaoDiaria]) -> list[VazaoSemanal]:
        vazoes_semanais = []
        for (id_usina, tipo_vazao, op_week), vazoes_diarias_agrupadas in groupby(vazoes_diarias, cls._unique_key):
            vazoes_diarias_agrupadas = list(vazoes_diarias_agrupadas)
            if len({v.data for v in vazoes_diarias_agrupadas}) != 7:
                raise ValueError(f'Não há dados de vazão diária para todos os dias da semana operativa: {op_week}.')

            if len(vazoes_diarias_agrupadas) > 7:
                raise ValueError(
                    f'Quantidade de vazões inválida para a semana operativa: {op_week}.'
                )  # TODO: podemos fazer uma lógica de priorização, para ficar com apenas 7

            valor = sum(vazao.valor for vazao in vazoes_diarias_agrupadas) / 7

            vazoes_semanais.append(VazaoSemanal(id_usina, op_week, valor, tipo_vazao, FonteVazao.CALCULATED_WEEKLY))

        return vazoes_semanais

    @staticmethod
    def _unique_key(vazao: VazaoDiaria):
        return (vazao.id_usina, vazao.tipo, SemanaOperativa.from_date(vazao.data))
