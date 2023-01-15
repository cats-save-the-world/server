class GameEventTypes:
    CONTROL: str = 'control'


class ControlActionTypes:
    LEFT: str = 'left'
    RIGHT: str = 'right'
    STOP: str = 'stop'


class CatStatus:
    IDLE: str = 'idle'
    RUNNING: str = 'running'
    HITTING: str = 'hitting'


class CatDirection:
    LEFT: str = 'left'
    RIGHT: str = 'right'


PLANET_DISTANCE: int = 160
CAT_RADIUS: int = 15
LEVEL_INTERVAL: int = 20
