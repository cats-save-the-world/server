from ._base import BaseController


class PlanetController(BaseController):
    MAX_HEALTH: int = 100

    def __init__(self) -> None:
        self._health: int = self.MAX_HEALTH

    def tick(self) -> None:
        pass

    @property
    def state(self) -> dict:
        return {
            'damage': 1 - self._health / self.MAX_HEALTH,
        }
