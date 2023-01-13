from asyncio import create_task, sleep, Task

from code.consts import GameEventTypes
from ._base import BaseController
from .cat import CatController
from .enemies import EnemiesController
from .planet import PlanetController


class GameController(BaseController):
    TICK_INTERVAL = 0.1

    def __init__(self) -> None:
        self._cat: CatController = CatController()
        self._enemies: EnemiesController = EnemiesController()
        self._planet: PlanetController = PlanetController()
        self._clock_task: Task = create_task(self._start_clock())

    async def _start_clock(self) -> None:
        while True:
            self.tick()
            await sleep(self.TICK_INTERVAL)

    def stop_clock(self) -> None:
        self._clock_task.cancel()

    def tick(self) -> None:
        self._cat.tick()
        self._enemies.tick()

    @property
    def state(self) -> dict:
        return {
            'cat': self._cat.state,
            'enemies': self._enemies.state,
            'planet': self._planet.state,
        }

    def dispatch(self, action: dict) -> None:
        action_type: str = action['type']

        if action_type == GameEventTypes.CONTROL:
            self._cat.control_action = action['payload']
