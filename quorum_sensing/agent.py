from enum import IntEnum


class State(IntEnum):
    SUSCEPTIBLE = 0
    REFRACTORY = 1


class Agent:
    def __init__(self, row: int, col: int):
        self.row = row
        self.col = col
        self.initiated_a_signal = False
        self.est_group_size = 0
        self.state = State.SUSCEPTIBLE
        self.refractory_steps_remaining = 0
        self.steps_since_last_signal = 0

    def __str__(self):
        return f"Agent(initiated={self.initiated_a_signal}, est_group_size={self.est_group_size}, state={self.state}, refractory_steps_remaining={self.refractory_steps_remaining})"
