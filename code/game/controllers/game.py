from code.game.consts import ControlAction
from .cat import CatController
from .enemies import EnemiesController
from .planet import PlanetController


class GameController:
    TICK_INTERVAL = 0.1

    def __init__(self) -> None:
        self._cat = CatController()
        self._enemies = EnemiesController()
        self._planet = PlanetController()
        self.score = 0

    def tick(self) -> None:
        self._cat.tick()
        self._enemies.tick(self._cat, self._planet, self)

    def update_game_score(self, score: int) -> None:
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
