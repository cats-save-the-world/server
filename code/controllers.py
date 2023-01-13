from asyncio import create_task, sleep, Task
from time import time
from uuid import UUID, uuid4

from code.consts import ControlActionTypes, GameEventTypes
from code.utils import generate_degree, generate_radius


class CatController:
    ACCELERATION_SPEED: int = 2
    BRAKING_SPEED: int = 1
    MAX_SPEED: int = 10

    def __init__(self) -> None:
        self._degree: int = 0
        self._speed: int = 0
        self.control_action: str = ControlActionTypes.STOP

    @property
    def state(self) -> dict:
        return {
            'degree': self._degree,
        }

    def _update_speed(self) -> None:
        if self.control_action == ControlActionTypes.RIGHT:
            self._speed = min(self._speed + self.ACCELERATION_SPEED, self.MAX_SPEED)

        elif self.control_action == ControlActionTypes.LEFT:
            self._speed = max(self._speed - self.ACCELERATION_SPEED, -self.MAX_SPEED)

        elif self.control_action == ControlActionTypes.STOP:
            if self._speed > 0:
                self._speed = max(self._speed - self.BRAKING_SPEED, 0)
            else:
                self._speed = min(self._speed + self.BRAKING_SPEED, 0)

    def tick(self) -> None:
        self._update_speed()
        self._degree += self._speed


class EnemyController:
    SPEED: int = 10

    def __init__(self) -> None:
        self.id: UUID = uuid4()
        self.radius: int = generate_radius()
        self._degree: int = generate_degree()

    @property
    def state(self) -> dict:
        return {
            'id': str(self.id),
            'radius': self.radius,
            'degree': self._degree,
        }

    def tick(self) -> None:
        self.radius -= self.SPEED


class EnemiesController:
    SPAWN_INTERVAL: int = 3
    MINIMAL_RADIUS: int = 155

    def __init__(self) -> None:
        # self._enemies: dict[UUID, EnemyController] = {}
        self._enemies: list[EnemyController] = []
        self._last_spawn: float = time()

    def _spawn_enemy(self) -> None:
        enemy: EnemyController = EnemyController()
        self._enemies.append(enemy)
        self._last_spawn = time()

    def tick(self) -> None:
        self._enemies = [enemy for enemy in self._enemies if enemy.radius > self.MINIMAL_RADIUS]

        for enemy in self._enemies:
            enemy.tick()

        if self._last_spawn + self.SPAWN_INTERVAL < time():
            self._spawn_enemy()

    @property
    def state(self) -> list[dict]:
        return [enemy.state for enemy in self._enemies]


class GameController:
    CYCLE_INTERVAL = 0.1

    def __init__(self) -> None:
        self._cat: CatController = CatController()
        self._enemies: EnemiesController = EnemiesController()
        self._cycle_task: Task = create_task(self._cycle())

    async def _cycle(self) -> None:
        while True:
            self._cat.tick()
            self._enemies.tick()
            await sleep(self.CYCLE_INTERVAL)

    def stop_cycle(self) -> None:
        self._cycle_task.cancel()

    @property
    def state(self) -> dict:
        return {
            'cat': self._cat.state,
            'enemies': self._enemies.state,
        }

    def dispatch(self, action: dict) -> None:
        action_type: str = action['type']

        if action_type == GameEventTypes.CONTROL:
            self._cat.control_action = action['payload']
