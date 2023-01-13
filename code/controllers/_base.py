from abc import ABC, abstractmethod
from typing import Any


class BaseController(ABC):
    @abstractmethod
    def tick(self) -> None: ...

    @abstractmethod
    def state(self) -> Any: ...
