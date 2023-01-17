from code.game.exceptions import DamageLimitException


class PlanetController:
    MAX_HEALTH = 100

    def __init__(self) -> None:
        self._health = self.MAX_HEALTH

    def get_damage(self, damage: int) -> None:
        if self._health - damage <= 0:
            raise DamageLimitException

        self._health -= damage

    @property
    def state(self) -> dict:
        return {
            'damage': round((1 - self._health / self.MAX_HEALTH), 2),
        }
