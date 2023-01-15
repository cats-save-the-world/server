import random
from time import time
from uuid import UUID

from code.consts import LEVEL_INTERVAL
from .enemy import EnemyController, DefaultEnemy, HeavyEnemy, FastEnemy, TwistEnemy


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
        enemy: EnemyController = self.get_enemy_by_start_time()
        self._enemies.append(enemy)
        self._last_spawn = time()

    def remove_enemy(self, enemy_id: UUID) -> None:
        self._enemies = [enemy for enemy in self._enemies if enemy.id != enemy_id]

    def tick(self) -> None:
        for enemy in self._enemies:
            enemy.tick()

        if self._last_spawn + self.SPAWN_INTERVAL < time():
            self._spawn_enemy()

    def get_enemy_by_start_time(self) -> EnemyController:
        available_enemy_types = [DefaultEnemy]

        if self._start_time + LEVEL_INTERVAL < time():
            available_enemy_types.append(HeavyEnemy)

        if self._start_time + 2 * LEVEL_INTERVAL < time():
            available_enemy_types.append(FastEnemy)

        if self._start_time + 3 * LEVEL_INTERVAL < time():
            available_enemy_types.append(TwistEnemy)

        return random.choice(available_enemy_types)()

    @property
    def state(self) -> list[dict]:
        return [enemy.state for enemy in self._enemies]
