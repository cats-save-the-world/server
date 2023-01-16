from enum import StrEnum, unique


@unique
class EventType(StrEnum):
    AUTH = 'auth'
    STATE = 'state'
    CONTROL = 'control'


@unique
class ControlAction(StrEnum):
    LEFT = 'left'
    RIGHT = 'right'
    STOP = 'stop'


@unique
class CatStatus(StrEnum):
    IDLE = 'idle'
    RUNNING = 'running'
    HITTING = 'hitting'


@unique
class CatDirection(StrEnum):
    LEFT = 'left'
    RIGHT = 'right'


PLANET_DISTANCE = 160
CAT_RADIUS = 15
LEVEL_INTERVAL = 20
