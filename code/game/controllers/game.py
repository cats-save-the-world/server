from code.game.consts import CatStatus, ControlAction, PLANET_DISTANCE
from .cat import CatController
from .enemies import ShapesController
from .enemy import EnemyController, HealController
from .planet import PlanetController


class GameController:
    TICK_INTERVAL = 0.1

    def __init__(self) -> None:
        self._cat = CatController()
        self._shapes = ShapesController()
        self._planet = PlanetController()
        self.score = 0

    def tick(self) -> None:
        self._cat.tick()
        self._shapes.tick()

        self.handle_events()

    def handle_events(self) -> None:
        for shape in self._shapes:
            if self._cat.intersects(shape):
                self._handle_intersect_event(shape)

            if shape.distance < PLANET_DISTANCE:
                self._handle_planet_contact_event(shape)

    def _handle_intersect_event(self, shape: ShapesController) -> None:
        if isinstance(shape, EnemyController):
            shape.alive = False
            self._update_game_score(shape.score)
            self._cat.status = CatStatus.HITTING

        elif isinstance(shape, HealController):
            print('TOUCH')
            self._planet.get_heal(shape.heal)

    def _handle_planet_contact_event(self, shape: ShapesController) -> None:
        if isinstance(shape, EnemyController):
            if shape.alive:
                self._planet.get_damage(shape.damage)

        self._shapes.remove_shape(shape.id)

    def _update_game_score(self, score: int) -> None:
        self.score += score

    @property
    def state(self) -> dict:
        return {
            'cat': self._cat.state,
            'enemies': self._shapes.state,
            'planet': self._planet.state,
            'score': self.score,
        }

    def control(self, control_action: ControlAction) -> None:
        self._cat.control_action = control_action
