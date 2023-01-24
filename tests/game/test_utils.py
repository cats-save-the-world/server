import pytest

from code.game.structures import Point
from code.game.utils import get_distance_between_points


@pytest.mark.parametrize(
    'a, b, output',
    [
        (Point(x=0, y=0), Point(x=3, y=4), 5.0),
        (Point(x=3, y=7), Point(x=-11, y=12), 14.87),
        (Point(x=-5, y=-8), Point(x=44, y=85), 105.12),
    ],
)
def test_get_distance_between_points(a: Point, b: Point, output: float):
    assert round(get_distance_between_points(a, b), 2) == output
