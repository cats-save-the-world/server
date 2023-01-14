class PlanetController:
    MAX_HEALTH: int = 100

    def __init__(self) -> None:
        self._health: int = self.MAX_HEALTH

    def get_damage(self, damage: int) -> None:
        self._health -= damage

    @property
    def state(self) -> dict:
        return {
            'damage': round((1 - self._health / self.MAX_HEALTH), 2),
        }
