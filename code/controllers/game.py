from asyncio import create_task, sleep, Task

from code.consts import CatStatus, ControlActionType, GameEventType, PLANET_DISTANCE
from .cat import CatController
from .enemies import EnemiesController
from .planet import PlanetController


class GameController:
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

        self.handle_events()

    def handle_events(self) -> None:
        for enemy in self._enemies:
            if self._cat.intersects(enemy):
                self._cat.status = CatStatus.HITTING
                self._enemies.remove_enemy(enemy.id)

            elif enemy.distance < PLANET_DISTANCE:
                self._planet.get_damage(enemy.damage)
                self._enemies.remove_enemy(enemy.id)

    @property
    def state(self) -> dict:
        return {
            'cat': self._cat.state,
            'enemies': self._enemies.state,
            'planet': self._planet.state,
        }

    def dispatch(self, action: dict) -> None:
        action_type: GameEventType = action['type']

        if action_type == GameEventType.CONTROL:
            control_action: ControlActionType = action['payload']
            self._cat.control_action = control_action
