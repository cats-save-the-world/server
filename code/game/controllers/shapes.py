from random import choices
from time import time
from typing import Generator, Type
from uuid import UUID

from code.game.consts import LEVEL_INTERVAL
from .shape import (
    EnemyController,
    HeavyEnemyController,
    HeavyHealController,
    HelperController,
    LightEnemyController,
    ShapeController,
    SimpleEnemyController,
    SimpleHealController,
    TwistedEnemyController,
)


class ShapesController:
    SPAWN_INTERVAL: int = 3

    def __init__(self) -> None:
        self._shapes: list[ShapeController] = []
        self._last_spawn = time()
        self._start_time = time()

    def __iter__(self) -> Generator:
        for shape in self._shapes:
            yield shape

    def _spawn_enemy(self) -> None:
        enemy = self._get_enemy()
        self._shapes.append(enemy)

    def _spawn_helper(self) -> None:
        helper = self._get_helper()

        if helper:
            self._shapes.append(helper)

    def remove_shape(self, shape_id: UUID) -> None:
        self._shapes = [shape for shape in self._shapes if shape.id != shape_id]

    def tick(self) -> None:
        for shape in self._shapes:
            shape.tick()

        if self._last_spawn + self.SPAWN_INTERVAL < time():
            self._spawn_enemy()
            self._spawn_helper()
            self._last_spawn = time()

    def _get_enemy(self) -> EnemyController:
        available_enemy_types: list[Type[EnemyController]] = [SimpleEnemyController]
        spawn_probabilities = [100]

        if self._start_time + LEVEL_INTERVAL < time():
            available_enemy_types.append(HeavyEnemyController)
            spawn_probabilities = [70, 30]

        if self._start_time + 2 * LEVEL_INTERVAL < time():
            available_enemy_types.append(LightEnemyController)
            spawn_probabilities = [60, 20, 20]

        if self._start_time + 3 * LEVEL_INTERVAL < time():
            available_enemy_types.append(TwistedEnemyController)
            spawn_probabilities = [40, 20, 20, 20]

        enemy = choices(available_enemy_types, weights=spawn_probabilities, k=1)[0]

        return enemy()

    def _get_helper(self) -> HelperController | None:
        available_healers = [None]
        spawn_probabilities = [100]

        if self._start_time + 2 * LEVEL_INTERVAL < time():
            available_healers.append(SimpleHealController)
            available_healers.append(HeavyHealController)
            spawn_probabilities = [85, 10, 5]

        helper = choices(available_healers, weights=spawn_probabilities, k=1)[0]

        return helper() if helper else None

    @property
    def state(self) -> list[dict]:
        return [shape.state for shape in self._shapes]
