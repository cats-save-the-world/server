class PlanetController:
    MAX_HEALTH: int = 100

    def __init__(self) -> None:
        self._health: int = self.MAX_HEALTH

    @property
    def state(self) -> dict:
        return {
            'damage': 1 - self._health / self.MAX_HEALTH,
        }
