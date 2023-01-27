from random import choices
from time import time
from typing import Generator, Type
from uuid import UUID

from code.game.consts import CatStatus, LEVEL_INTERVAL
from code.game.exceptions import EnemyKilled, EnemyReachedPlanet
from .cat import CatController
from .enemy import (
    EnemyController, HealingEnemyController, HeavyEnemyController, LightEnemyController,
    SimpleEnemyController, TwistedEnemyController,
)
from .planet import PlanetController


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
        if self._last_spawn + self.SPAWN_INTERVAL < time():
            enemy = self._get_enemy()
            self._enemies.append(enemy)
            self._last_spawn = time()

    def remove_enemy(self, enemy_id: UUID) -> None:
        self._enemies = [enemy for enemy in self._enemies if enemy.id != enemy_id]

    def tick(  # type: ignore[no-untyped-def]
        self, cat: CatController, planet: PlanetController, game,
    ) -> None:
        for enemy in self._enemies:
            try:
                enemy.tick(cat)

            except EnemyKilled:
                enemy.alive = False
                game.update_game_score(enemy.score)
                cat.status = CatStatus.HITTING

                if isinstance(enemy, HealingEnemyController):
                    planet.get_heal(enemy.damage)

            except EnemyReachedPlanet:
                self.remove_enemy(enemy.id)

                if enemy.alive:
                    planet.get_damage(enemy.damage)

        self._spawn_enemy()

    def _get_enemy(self) -> EnemyController:
        available_enemy_types: list[Type[EnemyController]] = [SimpleEnemyController]
        spawn_probabilities = [100]

        if self._start_time + LEVEL_INTERVAL < time():
            available_enemy_types.append(HeavyEnemyController)
            spawn_probabilities = [70, 30]

        if self._start_time + 2 * LEVEL_INTERVAL < time():
            available_enemy_types.extend([LightEnemyController, HealingEnemyController])
            spawn_probabilities = [50, 20, 20, 10]

        if self._start_time + 3 * LEVEL_INTERVAL < time():
            available_enemy_types.append(TwistedEnemyController)
            spawn_probabilities = [30, 20, 20, 10, 20]

        enemy = choices(available_enemy_types, weights=spawn_probabilities, k=1)[0]

        return enemy()

    @property
    def state(self) -> list[dict]:
        return [enemy.state for enemy in self._enemies]
