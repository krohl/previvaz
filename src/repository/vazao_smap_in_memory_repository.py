from domain.vazao_smap import VazaoDiariaSmap, VazaoDiariaSmapRepository


class VazaoDiariaSmapInMemoryRepository(VazaoDiariaSmapRepository):
    def __init__(self):
        self.vazoes: list[VazaoDiariaSmap] = []

    def fetch_from_round(self, id_rodada_smap: int) -> VazaoDiariaSmap:
        return next(v for v in self.vazoes if v.id_rodada_smap == id_rodada_smap)

    def persist(self, vazao_diaria_smap: VazaoDiariaSmap):
        self.vazoes.append(vazao_diaria_smap)
