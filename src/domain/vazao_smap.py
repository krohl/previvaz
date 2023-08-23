from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum

from domain.entity import AggregateRoot
from domain.vazao import VazaoDiaria


@dataclass
class VazaoDiariaSmap(AggregateRoot):
    id_rodada_smap: int
    vazoes_diarias: list[VazaoDiaria]

    #...


class VazaoDiariaSmapRepository(ABC):
    @abstractmethod
    def fetch_from_round(self, id_rodada_smap: int) -> list[VazaoDiariaSmap]:
        pass

    @abstractmethod
    def persist(self, vazao_diaria_smap: VazaoDiariaSmap):
        pass




class FonteVazao(Enum):
    SMAP=1
    ACOMPH=2
    MANUAL=3


@dataclass
class VazaoDiariaAggregate(AggregateRoot):
    source: FonteVazao
    id: int
    vazoes_diarias: list[VazaoDiaria]


class VazaoDiariaAggregateRepository(ABC):
    @abstractmethod
    def fetch_from_source_id(self, source: FonteVazao, id: int) -> VazaoDiariaAggregate:
        pass

    @abstractmethod
    def persist(self, vazao_diaria_smap: VazaoDiariaAggregate):
        pass


# class VazaoAggregate(ABC):
#     vazoes: list[VazaoDiaria]


# class VazaoSmap(VazaoAggregate):
#     id_rodada_smap: int
#     source = VazaoSource.SMAP


# class VazaoAcomph(VazaoAggregate):
#     source = VazaoSource.ACOMPH


# class VazaoManual(VazaoAggregate):
#     id_modelo_mapa: int
#     source = VazaoSource.MANUAL
