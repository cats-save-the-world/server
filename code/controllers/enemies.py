from time import time
from uuid import UUID

from ._base import BaseController
from .enemy import EnemyController


class EnemiesController(BaseController):
    SPAWN_INTERVAL: int = 3

    def __init__(self) -> None:
        self._enemies: list[EnemyController] = []
        self._last_spawn: float = time()

    def _spawn_enemy(self) -> None:
        enemy: EnemyController = EnemyController(self._remove_enemy)
        self._enemies.append(enemy)
        self._last_spawn = time()

    def _remove_enemy(self, enemy_id: UUID) -> None:
        self._enemies = [enemy for enemy in self._enemies if enemy.id != enemy_id]

    def tick(self) -> None:
        for enemy in self._enemies:
            enemy.tick()

        if self._last_spawn + self.SPAWN_INTERVAL < time():
            self._spawn_enemy()

    @property
    def state(self) -> list[dict]:
        return [enemy.state for enemy in self._enemies]
