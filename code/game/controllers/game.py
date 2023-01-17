from asyncio import create_task, sleep

from code.game.consts import CatStatus, ControlAction, GameStatus, PLANET_DISTANCE
from code.game.exceptions import GameEndException, PlanedDiedException
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
        self._status = GameStatus.RUN

    async def _start_clock(self) -> None:
        while True:
            self.tick()

            await sleep(self.TICK_INTERVAL)

    def stop_clock(self) -> None:
        self._clock_task.cancel()

    def tick(self) -> None:
        self._cat.tick()
        self._enemies.tick()

        self.handle_events()

    def handle_events(self) -> None:
        for enemy in self._enemies:
            if self._cat.intersects(enemy):
                self._cat.status = CatStatus.HITTING
                self._enemies.remove_enemy(enemy.id)

            elif enemy.distance < PLANET_DISTANCE:
                try:
                    self._planet.get_damage(enemy.damage)
                    self._enemies.remove_enemy(enemy.id)
                except PlanedDiedException:
                    self._status = GameStatus.END

    @property
    def state(self) -> dict:
        if self._status == GameStatus.END:
            raise GameEndException

        return {
            'cat': self._cat.state,
            'enemies': self._enemies.state,
            'planet': self._planet.state,
        }

    def control(self, control_action: ControlAction) -> None:
        self._cat.control_action = control_action
