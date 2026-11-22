import heapq
from collections import deque

import numpy as np
import pandas as pd

from src.distance import haversine_distance


def find_airport(airports, iata_code):
    matches = airports[
        airports["iata_code"]
        .fillna("")
        .astype(str)
        .str.upper()
        == iata_code.upper()
    ]

    if matches.empty:
        raise ValueError(f"Airport with IATA code {iata_code} not found.")

    return matches.iloc[0]


def get_neighbours(airports, airport, max_range_km):
    current_position = airports.index.get_loc(airport.name)

    distances = haversine_distance(
        airport["latitude"],
        airport["longitude"],
        airports["latitude"].to_numpy(),
        airports["longitude"].to_numpy()
    )

    neighbours = np.where(
        (distances <= max_range_km)
        & (np.arange(len(airports)) != current_position)
    )[0]

    return neighbours.tolist()


def _airport_label(airport):
    for column in ["iata_code", "ident", "name"]:
        value = airport.get(column)

        if pd.notna(value) and str(value).strip():
            return str(value).strip()

    return "Unknown airport"


def _reconstruct_route(airports, parents, destination_state):
    route = []
    current_state = destination_state

    while current_state is not None:
        if isinstance(current_state, tuple):
            airport_position = current_state[0]
        else:
            airport_position = current_state

        airport = airports.iloc[int(airport_position)]
        route.append(_airport_label(airport))

        current_state = parents.get(current_state)

    return route[::-1]


def find_route_bfs(
    airports,
    origin_code,
    destination_code,
    max_range_km,
    max_stops=10
):
    origin = find_airport(airports, origin_code)
    destination = find_airport(airports, destination_code)

    start_idx = airports.index.get_loc(origin.name)
    destination_idx = airports.index.get_loc(destination.name)

    if start_idx == destination_idx:
        return [_airport_label(origin)]

    max_legs = max_stops + 1

    queue = deque([start_idx])
    parents = {start_idx: None}
    legs_to_airport = {start_idx: 0}

    while queue:
        current_idx = queue.popleft()
        current_legs = legs_to_airport[current_idx]

        if current_idx == destination_idx:
            return _reconstruct_route(
                airports,
                parents,
                current_idx
            )

        if current_legs >= max_legs:
            continue

        current_airport = airports.iloc[current_idx]

        neighbours = get_neighbours(
            airports,
            current_airport,
            max_range_km
        )

        for neighbour_idx in neighbours:
            if neighbour_idx in parents:
                continue

            parents[neighbour_idx] = current_idx
            legs_to_airport[neighbour_idx] = current_legs + 1

            queue.append(neighbour_idx)

    return None


def find_route_dijkstra(
    airports,
    origin_code,
    destination_code,
    max_range_km,
    speed_kmh=500,
    refuel_hours=1,
    customs_hours=2,
    max_stops=10
):
    if speed_kmh <= 0:
        raise ValueError("speed_kmh must be greater than zero.")

    if max_stops < 0:
        raise ValueError("max_stops cannot be negative.")

    origin = find_airport(airports, origin_code)
    destination = find_airport(airports, destination_code)

    start_idx = airports.index.get_loc(origin.name)
    destination_idx = airports.index.get_loc(destination.name)

    if start_idx == destination_idx:
        return [_airport_label(origin)], 0.0

    max_legs = max_stops + 1

    latitudes = airports["latitude"].to_numpy()
    longitudes = airports["longitude"].to_numpy()
    countries = airports["iso_country"].to_numpy()
    n_airports = len(airports)
    all_indices = np.arange(n_airports)

    start_state = (start_idx, 0)
    distances = {start_state: 0.0}
    parents = {start_state: None}

    min_legs_popped = {}

    priority_queue = [(0.0, start_idx, 0)]

    while priority_queue:
        current_time, current_idx, legs = heapq.heappop(priority_queue)

        if current_time > distances.get((current_idx, legs), float("inf")):
            continue

        if legs >= min_legs_popped.get(current_idx, float("inf")):
            continue
        min_legs_popped[current_idx] = legs

        current_state = (current_idx, legs)

        if current_idx == destination_idx:
            route = _reconstruct_route(airports, parents, current_state)
            return route, current_time

        if legs >= max_legs:
            continue

        cur_lat = latitudes[current_idx]
        cur_lon = longitudes[current_idx]
        cur_country = countries[current_idx]

        leg_distances = haversine_distance(
            cur_lat,
            cur_lon,
            latitudes,
            longitudes
        )

        in_range_mask = (leg_distances <= max_range_km) & (all_indices != current_idx)
        neighbours = all_indices[in_range_mask]

        new_legs = legs + 1

        for neighbour_idx in neighbours:
            if new_legs >= min_legs_popped.get(neighbour_idx, float("inf")):
                continue

            distance_km = leg_distances[neighbour_idx]
            flight_time = distance_km / speed_kmh
            additional_time = flight_time

            if legs > 0:
                additional_time += refuel_hours

            neighbour_country = countries[neighbour_idx]
            if (
                pd.notna(cur_country)
                and pd.notna(neighbour_country)
                and cur_country != neighbour_country
            ):
                additional_time += customs_hours

            new_time = current_time + additional_time
            neighbour_state = (neighbour_idx, new_legs)

            if new_time < distances.get(neighbour_state, float("inf")):
                distances[neighbour_state] = new_time
                parents[neighbour_state] = current_state
                heapq.heappush(
                    priority_queue,
                    (new_time, neighbour_idx, new_legs)
                )

    return None, float("inf")


def reachable_within(
    airports,
    origin_code,
    max_range_km,
    max_stops=10
):
    origin = find_airport(airports, origin_code)

    start_idx = airports.index.get_loc(origin.name)
    max_legs = max_stops + 1

    queue = deque([start_idx])

    legs_to_airport = {start_idx: 0}

    while queue:
        current_idx = queue.popleft()
        current_legs = legs_to_airport[current_idx]

        if current_legs >= max_legs:
            continue

        current_airport = airports.iloc[current_idx]

        neighbours = get_neighbours(
            airports,
            current_airport,
            max_range_km
        )

        for neighbour_idx in neighbours:
            if neighbour_idx in legs_to_airport:
                continue

            legs_to_airport[neighbour_idx] = current_legs + 1
            queue.append(neighbour_idx)

    reachable = {}

    for airport_idx, legs in legs_to_airport.items():
        airport = airports.iloc[airport_idx]
        label = _airport_label(airport)

        reachable[label] = legs

    return reachable
