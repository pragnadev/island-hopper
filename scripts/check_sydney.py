from src.data_loader import load_airports
from src.routing import (
    find_route_bfs, find_route_dijkstra
)


def main():
    airports = load_airports()

    origin = "MXP"
    destination = "SYD"

    max_range_km = 4000
    max_stops = 10

    speed_kmh = 500
    refuel_hours = 1
    customs_hours = 2

    print("\n===================================")
    print("       ISLAND HOPPER ANALYSIS")
    print("===================================")

    print(f"Origin: {origin}")
    print(f"Destination: {destination}")
    print(f"Maximum aircraft range: {max_range_km} km")
    print(f"Maximum intermediate stops: {max_stops}")

    shortest_route = find_route_bfs(
        airports,
        origin,
        destination,
        max_range_km,
        max_stops=max_stops
    )

    print("\n--- MINIMUM STOPS ROUTE (BFS) ---")

    if shortest_route is None:
        print("Sydney is not reachable within the stop limit.")

    else:
        print("Route:", " -> ".join(shortest_route))

        flight_legs = len(shortest_route) - 1
        intermediate_stops = max(0, flight_legs - 1)

        print("Flight legs:", flight_legs)
        print("Intermediate stops:", intermediate_stops)

    fastest_route, total_time = find_route_dijkstra(
        airports,
        origin,
        destination,
        max_range_km,
        speed_kmh=speed_kmh,
        refuel_hours=refuel_hours,
        customs_hours=customs_hours,
        max_stops=max_stops
    )

    print("\n--- MINIMUM TIME ROUTE (DIJKSTRA) ---")

    if fastest_route is None:
        print("Sydney is not reachable within the stop limit.")

    else:
        print("Route:", " -> ".join(fastest_route))

        flight_legs = len(fastest_route) - 1
        intermediate_stops = max(0, flight_legs - 1)

        print("Flight legs:", flight_legs)
        print("Intermediate stops:", intermediate_stops)

        print(
            "Total travel time:",
            round(total_time, 2),
            "hours"
        )

        print(
            "Total travel time:",
            round(total_time / 24, 2),
            "days"
        )

    print("\n===================================")


if __name__ == "__main__":
    main()
