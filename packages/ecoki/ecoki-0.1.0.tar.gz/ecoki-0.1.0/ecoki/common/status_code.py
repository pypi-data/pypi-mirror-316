from enum import Enum


class Status(Enum):
    WAITING = -1
    RUNNING = 0
    FINISHED = 1
    FAILURE = 2

