from typing import Generator

from aima.search import Problem
from bicing_operators import Operadors
from bicing_estat import Estat

class BicingProblem(Problem):
    def __init__(self, initial_state: Estat, use_entropy: bool = False):
        self.use_entropy = use_entropy
        super().__init__(initial_state)

    def actions(self, state: Estat) -> Generator[Operadors, None, None]:
        return state.genera_accions()

    def result(self, state: Estat, action: Operadors) -> Estat:
        return state.aplica_accions(action)

    def value(self, state: Estat) -> float:
        return state.heuristica1()

    def goal_test(self, state: Estat) -> bool:
        return False
