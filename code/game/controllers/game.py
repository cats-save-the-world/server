from asyncio import create_task, sleep

from code.game.consts import CatStatus, ControlAction, PLANET_DISTANCE
from code.game.exceptions import GameOver
from .cat import CatController
from .enemies import EnemiesController
from .planet import PlanetController


class GameController:
    TICK_INTERVAL = 0.1

    def __init__(self) -> None:
        self._cat = CatController()
        self._enemies = EnemiesController()
        self._planet = PlanetController()
        self._clock_task = create_task(self._start_clock())
        self.score = 0

    async def _start_clock(self) -> None:
        while True:
            try:
                self.tick()
            except GameOver:
                break

            await sleep(self.TICK_INTERVAL)

    def stop_clock(self) -> None:
        self._clock_task.cancel()

    @property
    def game_over(self) -> bool:
        return self._clock_task.done()

    def tick(self) -> None:
        self._cat.tick()
        self._enemies.tick()

        self.handle_events()

    def handle_events(self) -> None:
        for enemy in self._enemies:
            if self._cat.intersects(enemy):
                self._cat.status = CatStatus.HITTING
                self._enemies.remove_enemy(enemy.id)
                self._update_game_score(enemy.score)

            elif enemy.distance < PLANET_DISTANCE:
                self._planet.get_damage(enemy.damage)
                self._enemies.remove_enemy(enemy.id)

    def _update_game_score(self, score: int) -> None:
        self.score += score

    @property
    def state(self) -> dict:
        return {
            'cat': self._cat.state,
            'enemies': self._enemies.state,
            'planet': self._planet.state,
            'score': self.score,
        }

    def control(self, control_action: ControlAction) -> None:
        self._cat.control_action = control_action
