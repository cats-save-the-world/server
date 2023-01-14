from time import time
from uuid import UUID

from .enemy import EnemyController
from ..consts import EnemyTypes


class EnemiesController:
    SPAWN_INTERVAL: int = 3

    def __init__(self) -> None:
        self._enemies: list[EnemyController] = []
        self._last_spawn: float = time()
        self._start_time: float = time()

    def __iter__(self):
        for enemy in self._enemies:
            yield enemy

    def _spawn_enemy(self) -> None:
        enemy_type: dict = EnemyTypes().get_enemy_by_game_time(self._start_time)
        enemy: EnemyController = EnemyController(**enemy_type)
        self._enemies.append(enemy)
        self._last_spawn = time()

    def remove_enemy(self, enemy_id: UUID) -> None:
        self._enemies = [enemy for enemy in self._enemies if enemy.id != enemy_id]

    def tick(self) -> None:
        for enemy in self._enemies:
            enemy.tick()

        if self._last_spawn + self.SPAWN_INTERVAL < time():
            self._spawn_enemy()

    @property
    def state(self) -> list[dict]:
        return [enemy.state for enemy in self._enemies]
