from random import choices
from time import time
from typing import Generator, Type
from uuid import UUID

from code.game.consts import LEVEL_INTERVAL
from .enemy import (
    EnemyController, HeavyEnemyController, LightEnemyController, SimpleEnemyController,
    TwistedEnemyController,
)


class EnemiesController:
    SPAWN_INTERVAL: int = 3

    def __init__(self) -> None:
        self._enemies: list[EnemyController] = []
        self._last_spawn = time()
        self._start_time = time()

    def __iter__(self) -> Generator:
        for enemy in self._enemies:
            yield enemy

    def _spawn_enemy(self) -> None:
        enemy = self._get_enemy()
        self._enemies.append(enemy)
        self._last_spawn = time()

    def remove_enemy(self, enemy_id: UUID) -> None:
        self._enemies = [enemy for enemy in self._enemies if enemy.id != enemy_id]

    def tick(self) -> None:
        for enemy in self._enemies:
            enemy.tick()

        if self._last_spawn + self.SPAWN_INTERVAL < time():
            self._spawn_enemy()

    def _get_enemy(self) -> EnemyController:
        available_enemy_types: list[Type[EnemyController]] = [SimpleEnemyController]
        spawn_probabilities: list[int] = [100]

        if self._start_time + LEVEL_INTERVAL < time():
            available_enemy_types.append(HeavyEnemyController)
            spawn_probabilities = [65, 35]

        if self._start_time + 2 * LEVEL_INTERVAL < time():
            available_enemy_types.append(LightEnemyController)
            spawn_probabilities = [50, 40, 10]

        if self._start_time + 3 * LEVEL_INTERVAL < time():
            available_enemy_types.append(TwistedEnemyController)
            spawn_probabilities = [20, 40, 15, 25]

        enemy = choices(available_enemy_types, weights=spawn_probabilities, k=1)[0]

        return enemy()

    @property
    def state(self) -> list[dict]:
        return [enemy.state for enemy in self._enemies]
