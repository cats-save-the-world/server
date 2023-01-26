from code.game.consts import CatStatus, ControlAction, PLANET_DISTANCE
from .cat import CatController
from .enemies import EnemiesController
from .enemy import HealEnemyController
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
        self._enemies.tick()

        self.handle_events()

    def handle_events(self) -> None:
        for enemy in self._enemies:
            if enemy.alive and self._cat.intersects(enemy):
                enemy.alive = False
                self._update_game_score(enemy.score)
                self._cat.status = CatStatus.HITTING

                if isinstance(enemy, HealEnemyController):
                    self._planet.get_heal(enemy.damage)

            if enemy.distance < PLANET_DISTANCE:
                self._enemies.remove_enemy(enemy.id)

                if enemy.alive:
                    self._planet.get_damage(enemy.damage)

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
