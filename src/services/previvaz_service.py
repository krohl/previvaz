from domain.usina_repository import UsinaRepository
from domain.vazao import FonteVazao, TipoVazao, VazaoSemanalFactory
from domain.vazao_repository import VazaoDiariaRepository
from domain.previvaz_parametro import PrevivazParametro


class PrevivazEntradaService:
    def __init__(self, vazao_repository: VazaoDiariaRepository, usina_repository: UsinaRepository):
        self.vazao_repository = vazao_repository
        self.usina_repository = usina_repository

    def create_file(self, parametros_rodada: PrevivazParametro):
        usinas = self.usina_repository.get_all()

        vazoes_observadas = self.vazao_repository.get_by_usina_ids(
            usina_ids=[usina.id for usina in usinas],
            start_date=parametros_rodada.inicio_observado,
            end_date=parametros_rodada.fim_observado,
            tipo_vazao=TipoVazao.NATURAL,  # TODO: analisar se o tipo de vazao e so NATURAL
            fonte_vazao=FonteVazao.ACOMPH,
        )

        vazoes_smap = self.vazao_repository.fetch_from_rodada_smap(
            usina_ids=[usina.id for usina in usinas],
            id_rodada_smap=parametros_rodada.id_rodada_smap,
            start_date=parametros_rodada.inicio_previsto,
            end_date=parametros_rodada.fim_previsto,
        )

        # TODO: validar se tem vazões para todas as datas entre parametros_rodada.start_date e parametros_rodada.end_date

        vazoes_semanais = VazaoSemanalFactory.from_vazoes_diarias(vazoes_observadas + vazoes_smap)

        with open('vazoes_entrada.txt', 'w') as f:
            for vazao_semanal in vazoes_semanais:
                f.write(
                    f'{vazao_semanal.id_usina} {vazao_semanal.op_week.ano} '\
                    f'{vazao_semanal.op_week.numero_semana_previvaz} {round(vazao_semanal.valor)}\n'
                )
