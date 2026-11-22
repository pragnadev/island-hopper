from src.data_loader import load_airports
from src.analysis import (
    find_farthest_reachable_airport,
    analyze_route_options,
    run_range_sensitivity_analysis,
)


def test_farthest_reachable_from_mxp():
    airports = load_airports()
    farthest = find_farthest_reachable_airport(
        airports,
        origin_code="MXP",
        max_range_km=4000,
        max_stops=10
    )

    assert farthest is not None
    assert farthest["iata_code"] == "CHT"
    assert round(farthest["distance_km"]) == 19558


def test_analyze_route_options_syd():
    airports = load_airports()
    res = analyze_route_options(
        airports,
        origin_code="MXP",
        destination_code="SYD",
        max_range_km=4000,
        max_stops=10
    )

    assert res["destination_reachable"] is True
    assert res["bfs_legs"] == 5
    assert res["bfs_stops"] == 4
    assert res["fastest_time_hours"] is not None
    assert res["fastest_time_hours"] > 0


def test_syd_not_reachable_at_1500km():
    airports = load_airports()
    res = analyze_route_options(
        airports,
        origin_code="MXP",
        destination_code="SYD",
        max_range_km=1500,
        max_stops=10
    )

    assert res["destination_reachable"] is False
    assert res["bfs_route"] is None
    assert res["fastest_route"] is None


def test_run_range_sensitivity_analysis():
    airports = load_airports()
    df = run_range_sensitivity_analysis(
        airports,
        origin_code="MXP",
        destination_code="SYD",
        ranges=[1500, 4000]
    )

    assert len(df) == 2
    assert "range_km" in df.columns
    assert "destination_reachable" in df.columns
    assert not df.loc[df["range_km"] == 1500, "destination_reachable"].values[0]
    assert df.loc[df["range_km"] == 4000, "destination_reachable"].values[0]
