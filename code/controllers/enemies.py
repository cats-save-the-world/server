from time import time
from typing import Callable
from uuid import UUID

from .cat import CatController
from .enemy import EnemyController


class EnemiesController:
    SPAWN_INTERVAL: int = 3

    def __init__(self, hit: Callable) -> None:
        self._enemies: list[EnemyController] = []
        self._last_spawn: float = time()
        self._hit: Callable = hit

    def _spawn_enemy(self) -> None:
        enemy: EnemyController = EnemyController(self._remove_enemy)
        self._enemies.append(enemy)
        self._last_spawn = time()

    def _remove_enemy(self, enemy_id: UUID) -> None:
        self._enemies = [enemy for enemy in self._enemies if enemy.id != enemy_id]

    def tick(self, cat: CatController) -> None:
        for enemy in self._enemies:
            if cat.intersect(enemy):
                self._hit(enemy.id)

            enemy.tick()

        if self._last_spawn + self.SPAWN_INTERVAL < time():
            self._spawn_enemy()

    @property
    def state(self) -> list[dict]:
        return [enemy.state for enemy in self._enemies]
