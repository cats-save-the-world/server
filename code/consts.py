from enum import StrEnum, unique


@unique
class GameEventType(StrEnum):
    CONTROL: str = 'control'


@unique
class ControlActionType(StrEnum):
    LEFT: str = 'left'
    RIGHT: str = 'right'
    STOP: str = 'stop'


@unique
class CatStatus(StrEnum):
    IDLE: str = 'idle'
    RUNNING: str = 'running'
    HITTING: str = 'hitting'


@unique
class CatDirection(StrEnum):
    LEFT: str = 'left'
    RIGHT: str = 'right'


PLANET_DISTANCE: int = 160
