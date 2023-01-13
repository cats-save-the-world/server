from typing import Callable
from uuid import UUID, uuid4

from code.utils import generate_degree, generate_radius
from ._base import BaseController


class EnemyController(BaseController):
    SPEED: int = 10
    MINIMAL_RADIUS: int = 160

    def __init__(self, remove: Callable) -> None:
        self.id: UUID = uuid4()
        self.radius: int = generate_radius()
        self._degree: int = generate_degree()
        self._remove: Callable = remove

    @property
    def state(self) -> dict:
        return {
            'id': str(self.id),
            'radius': self.radius,
            'degree': self._degree,
        }

    def tick(self) -> None:
        self.radius -= self.SPEED

        if self.radius < self.MINIMAL_RADIUS:
            self._remove(self.id)
