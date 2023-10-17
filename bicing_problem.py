from typing import Generator

from aima.search import Problem

from bicing_operators import BicingOperator
from bicing_estat import Estat


class BicingProblem(Problem):
    def __init__(self, initial_state: Estat, use_entropy: bool = False):
        self.use_entropy = use_entropy
        super().__init__(initial_state)

    def actions(self, state: Estat) -> Generator[BicingOperator, None, None]:
        return state.genera_accions()

    def result(self, state: Estat, action: BicingOperator) -> Estat:
        try:
            furgo = state.ruta[action.num_furgo]
        except:
            furgo = state.ruta[action.num_furgo1]
        return state.aplica_operador(action)

    def value(self, state: Estat) -> float:
        return state.h()

    def goal_test(self, state: Estat) -> bool:
        return False
