
import numpy as np

from src.distance import haversine_distance


def test_same_airport():
    distance = haversine_distance(
        45.63, 8.72,
        45.63, 8.72
    )

    assert distance == 0


def test_distance_is_symmetric():
    distance1 = haversine_distance(
        45.63, 8.72,
        51.47, -0.45
    )

    distance2 = haversine_distance(
        51.47, -0.45,
        45.63, 8.72
    )

    assert np.isclose(distance1, distance2)


def test_vectorised_distance():
    distances = haversine_distance(
        45.63, 8.72,
        np.array([45.63, 51.47]),
        np.array([8.72, -0.45])
    )

    assert distances.shape == (2,)
    assert np.isclose(distances[0], 0)
    assert distances[1] > 900
    assert distances[1] < 1000
