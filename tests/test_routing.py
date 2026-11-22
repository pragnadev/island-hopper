from src.data_loader import load_airports
from src.routing import (
    find_airport,
    find_route_bfs,
    find_route_dijkstra,
    get_neighbours,
)


def test_find_mxp():
    airports = load_airports()

    mxp = find_airport(airports, "MXP")

    assert mxp["iata_code"] == "MXP"


def test_find_syd():
    airports = load_airports()

    syd = find_airport(airports, "SYD")

    assert syd["iata_code"] == "SYD"


def test_neighbours_within_range():
    airports = load_airports()

    mxp = find_airport(airports, "MXP")

    neighbours = get_neighbours(
        airports,
        mxp,
        max_range_km=4000
    )

    assert len(neighbours) > 0


def test_bfs_same_origin_and_destination():
    airports = load_airports()

    route = find_route_bfs(
        airports, "MXP", "MXP", 4000
    )

    assert route == ["MXP"]


def test_bfs_returns_valid_route():
    airports = load_airports()

    route = find_route_bfs(
        airports, "MXP", "LHR", 4000
    )

    assert route is not None
    assert route[0] == "MXP"
    assert route[-1] == "LHR"


def test_dijkstra_same_origin_and_destination():
    airports = load_airports()

    route, total_time = find_route_dijkstra(
        airports,
        "MXP",
        "MXP",
        max_range_km=4000
    )

    assert route == ["MXP"]
    assert total_time == 0


def test_dijkstra_returns_valid_route():
    airports = load_airports()

    route, total_time = find_route_dijkstra(
        airports,
        "MXP",
        "LHR",
        max_range_km=4000
    )

    assert route is not None
    assert route[0] == "MXP"
    assert route[-1] == "LHR"
    assert total_time > 0
