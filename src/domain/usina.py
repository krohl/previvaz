from dataclasses import dataclass


@dataclass(frozen=True)
class Usina:
    id: str
    nome: str
    lat: float
    lon: float
