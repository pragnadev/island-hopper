import numpy as np
import pandas as pd

from src.distance import haversine_distance
from src.routing import (
    find_airport,
    find_route_bfs,
    find_route_dijkstra,
    reachable_within,
)


def find_farthest_reachable_airport(
    airports,
    origin_code,
    max_range_km,
    max_stops=10,
    reachable=None
):
    origin = find_airport(airports, origin_code)

    if reachable is None:
        reachable = reachable_within(
            airports,
            origin_code=origin_code,
            max_range_km=max_range_km,
            max_stops=max_stops
        )
        reachable = dict(reachable)
        reachable.pop(origin_code, None)

    if not reachable:
        return None

    reachable_keys = set(reachable.keys())
    mask = (
        airports["iata_code"].isin(reachable_keys)
        | airports["ident"].isin(reachable_keys)
    )
    candidates = airports[mask].copy()

    if candidates.empty:
        return None

    candidates["distance_km"] = haversine_distance(
        origin["latitude"],
        origin["longitude"],
        candidates["latitude"].to_numpy(),
        candidates["longitude"].to_numpy()
    )

    candidates = candidates.sort_values(
        by="distance_km",
        ascending=False
    )

    farthest = candidates.iloc[0]
    iata = farthest.get("iata_code")
    ident = farthest.get("ident")

    legs = reachable.get(iata)
    if legs is None:
        legs = reachable.get(ident)

    stops = int(legs) - 1 if legs is not None else None

    return {
        "name": farthest["name"],
        "iata_code": iata if pd.notna(iata) else None,
        "ident": ident if pd.notna(ident) else None,
        "distance_km": round(float(farthest["distance_km"]), 2),
        "flight_legs": int(legs) if legs is not None else None,
        "intermediate_stops": stops
    }


def analyze_route_options(
    airports,
    origin_code,
    destination_code,
    max_range_km,
    speed_kmh=500,
    refuel_hours=1.0,
    customs_hours=2.0,
    max_stops=10
):
    bfs_route = find_route_bfs(
        airports,
        origin_code,
        destination_code,
        max_range_km,
        max_stops=max_stops
    )

    destination_reachable = bfs_route is not None

    if destination_reachable:
        bfs_legs = len(bfs_route) - 1
        bfs_stops = max(0, bfs_legs - 1)

        fastest_route, total_time = find_route_dijkstra(
            airports,
            origin_code,
            destination_code,
            max_range_km,
            speed_kmh=speed_kmh,
            refuel_hours=refuel_hours,
            customs_hours=customs_hours,
            max_stops=max_stops
        )

        if fastest_route is not None:
            fastest_legs = len(fastest_route) - 1
            fastest_stops = max(0, fastest_legs - 1)
            fastest_time_h = round(total_time, 2)
            fastest_time_days = round(total_time / 24, 2)
        else:
            fastest_legs = None
            fastest_stops = None
            fastest_time_h = None
            fastest_time_days = None
    else:
        bfs_legs = None
        bfs_stops = None
        fastest_route = None
        fastest_legs = None
        fastest_stops = None
        fastest_time_h = None
        fastest_time_days = None

    return {
        "destination_reachable": destination_reachable,
        "bfs_route": bfs_route,
        "bfs_legs": bfs_legs,
        "bfs_stops": bfs_stops,
        "fastest_route": fastest_route,
        "fastest_legs": fastest_legs,
        "fastest_stops": fastest_stops,
        "fastest_time_hours": fastest_time_h,
        "fastest_time_days": fastest_time_days,
    }


def run_range_sensitivity_analysis(
    airports,
    origin_code="MXP",
    destination_code="SYD",
    ranges=None,
    speed_kmh=500,
    refuel_hours=1.0,
    customs_hours=2.0,
    max_stops=10
):
    if ranges is None:
        ranges = [1500, 2000, 2500, 3000, 3500, 4000, 5000, 6000, 7000, 8000]

    records = []

    for max_range_km in ranges:
        reachable = reachable_within(
            airports,
            origin_code,
            max_range_km,
            max_stops=max_stops
        )
        reachable = dict(reachable)
        reachable.pop(origin_code, None)
        reachable_count = len(reachable)

        farthest_info = find_farthest_reachable_airport(
            airports,
            origin_code,
            max_range_km,
            max_stops=max_stops,
            reachable=reachable
        )

        route_info = analyze_route_options(
            airports,
            origin_code,
            destination_code,
            max_range_km,
            speed_kmh=speed_kmh,
            refuel_hours=refuel_hours,
            customs_hours=customs_hours,
            max_stops=max_stops
        )

        records.append({
            "range_km": max_range_km,
            "destination_reachable": route_info["destination_reachable"],
            "min_legs": route_info["bfs_legs"],
            "min_stops": route_info["bfs_stops"],
            "fastest_time_hours": route_info["fastest_time_hours"],
            "fastest_legs": route_info["fastest_legs"],
            "fastest_stops": route_info["fastest_stops"],
            "reachable_airports": reachable_count,
            "farthest_airport_name": farthest_info["name"] if farthest_info else None,
            "farthest_airport_iata": farthest_info.get("iata_code") if farthest_info else None,
            "farthest_distance_km": farthest_info["distance_km"] if farthest_info else None,
            "bfs_route": " -> ".join(route_info["bfs_route"]) if route_info["bfs_route"] else None,
            "fastest_route": " -> ".join(route_info["fastest_route"]) if route_info["fastest_route"] else None,
        })

    return pd.DataFrame(records)
