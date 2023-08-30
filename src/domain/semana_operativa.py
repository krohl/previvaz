from __future__ import annotations

import calendar
from dataclasses import dataclass
from datetime import date, timedelta

@dataclass(frozen=True)
class SemanaOperativa:
    """Representa o conceito de Semana Operativa.

    - A semana operativa começa sempre em um sábado e termina na sexta-feira seguinte.
    - A ela se associada uma data de rodada `round_date`, usualmente na quinta-feira anterior ao começo da semana operativa (essa data pode variar,
    dependendo da presença de feriados na semana)
    - O último dia de uma Semana Operativa define a qual mês ela pertence. Se a semana operativa começa no mês de fevereiro, mas termina no mês de
    março, ela pertence ao mês de março.
    - Há um identificador das semanas operativas, no seguinte formato: 2023031, 2023032, 2023033, ... Ele apresenta o ano, mês e um número associado
    à semana operativa que indica sua 'posição no mês' (a primeira Semana Operativa do mês recebe 'posição no mês' = 1)
    - Há ainda o indicador chamada 'rev'. A primeira Semana Operativa do mês recebe valor 0, sendo a rev0 do mês.
    """
    start_date: date

    def __post_init__(self):
        if self.start_date.weekday() != calendar.SATURDAY:
            raise ValueError("start_date da SemanaOperativa deve ser sábado")

    @property
    def end_date(self):
        return self.start_date + timedelta(days=6)

    @property
    def numero_semana_previvaz(self) -> int:
        """Retorna o número da semana no ano para o previvaz

        Returns:
            int: número da semana no ano
        """
        return self.end_date.isocalendar()[1]

    @property
    def ano(self) -> int:
        return self.end_date.year

    @classmethod
    def from_date(cls, ref_date: date) -> SemanaOperativa:
        while ref_date.weekday() != calendar.SATURDAY:
            ref_date -= timedelta(days=1)
        return SemanaOperativa(ref_date)


    def next(self, quantidade_semanas=1) -> SemanaOperativa:
        """Retorna a próxima SemanaOperativa

        Returns:
            SemanaOperativa: Próxima semana operativa
        """
        end_date = self.end_date
        for _ in range(quantidade_semanas):
            semana_operativa = SemanaOperativa.from_date(end_date + timedelta(days=1))
            end_date = semana_operativa.end_date

        return semana_operativa
    
    def previous(self, quantidade_semanas=1) -> SemanaOperativa:
        """Retorna a SemanaOperativa anterior

        Returns:
            SemanaOperativa: Semana operativa anterior
        """
        start_date = self.start_date
        for _ in range(quantidade_semanas):
            semana_operativa = SemanaOperativa.from_date(start_date - timedelta(days=1))
            start_date = semana_operativa.start_date

        return semana_operativa