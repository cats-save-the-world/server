import random
from time import time


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


class EnemyTypes:
    LEVEL_INTERVAL: int = 20

    DEFAULT = {'radius': 10, 'speed': 10, 'damage': 10, 'angle_shift': 0, 'type': 'DEFAULT'}
    HEAVY = {'radius': 20, 'speed': 5, 'damage': 20, 'angle_shift': 0, 'type': 'HEAVY'}
    FAST = {'radius': 10, 'speed': 20, 'damage': 5, 'angle_shift': 0, 'type': 'FAST'}
    TWIST = {'radius': 10, 'speed': 10, 'damage': 10, 'angle_shift': 0.5, 'type': 'TWIST'}

    def get_enemy_by_game_time(self, start_time: float) -> dict:
        available_enemy_types = [self.DEFAULT]

        if start_time + self.LEVEL_INTERVAL < time():
            available_enemy_types.append(self.HEAVY)

        if start_time + 2 * self.LEVEL_INTERVAL < time():
            available_enemy_types.append(self.FAST)

        if start_time + 3 * self.LEVEL_INTERVAL < time():
            available_enemy_types.append(self.TWIST)

        return random.choice(available_enemy_types)
