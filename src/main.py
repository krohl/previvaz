from datetime import timedelta
from random import random

from domain.previvaz_parametro import PrevivazParametro
from domain.usina import Usina
from domain.vazao import FonteVazao, TipoVazao, VazaoDiaria, VazaoDiariaSmap
from repository.usina_in_memory_repository import UsinaInMemoryRepository
from repository.vazao_in_memory_repository import VazaoDiariaInMemoryRepository
from services.previvaz_service import PrevivazEntradaService


def main(event):
    parametros_rodada = PrevivazParametro(**event)

    usina_repository = UsinaInMemoryRepository()
    vazao_repository = VazaoDiariaInMemoryRepository()

    usina_1 = Usina('1', 'usina1', 25.25, 25.25)
    usina_repository.add(usina_1)

    vazoes_acomph = [
        VazaoDiaria(
            usina_1.id,
            parametros_rodada.inicio_observado + timedelta(days=num_days),
            100 * random(),
            TipoVazao.NATURAL,
            FonteVazao.ACOMPH,
        )
        for num_days in range(50)
    ]
    vazao_repository.add(vazoes_acomph)
    vazoes_smap = [
        VazaoDiariaSmap(
            usina_1.id,
            parametros_rodada.inicio_previsto + timedelta(days=num_days),
            100 * random(),
            TipoVazao.NATURAL,
            FonteVazao.SMAP,
            id_rodada_smap=parametros_rodada.id_rodada_smap,
        )
        for num_days in range(50)
    ]
    vazao_repository.add(vazoes_smap)

    input_file = PrevivazEntradaService(vazao_repository, usina_repository).create_file(parametros_rodada)

    print(input_file)


if __name__ == "__main__":
    event = {
        'id_rodada_smap': 1,
        'data_rodada': '2023-08-16',
        'data_deck_smap': '2023-08-17'
    }
    main(event)
