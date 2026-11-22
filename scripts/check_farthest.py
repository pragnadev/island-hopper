from src.data_loader import load_airports
from src.routing import reachable_within, find_airport
from src.distance import haversine_distance


def main():
    airports = load_airports()

    origin_code = "MXP"
    max_range_km = 4000
    max_stops = 10

    origin = find_airport(airports, origin_code)

    reachable = reachable_within(
        airports,
        origin_code=origin_code,
        max_range_km=max_range_km,
        max_stops=max_stops
    )

    reachable.pop(origin_code, None)

    candidates = airports[
        airports["iata_code"].isin(reachable.keys())
    ].copy()

    candidates["distance_from_mxp_km"] = haversine_distance(
        origin["latitude"],
        origin["longitude"],
        candidates["latitude"].to_numpy(),
        candidates["longitude"].to_numpy()
    )

    candidates["flight_legs"] = (
        candidates["iata_code"].map(reachable)
    )

    candidates = candidates.sort_values(
        by="distance_from_mxp_km",
        ascending=False
    )

    farthest = candidates.iloc[0]

    print("\n--- Farthest Reachable Airport ---")
    print("Origin:", origin_code)
    print("Farthest airport:", farthest["name"])
    print("IATA code:", farthest["iata_code"])
    print(
        "Distance from MXP:",
        round(farthest["distance_from_mxp_km"], 2),
        "km"
    )
    print("Flight legs:", int(farthest["flight_legs"]))
    print(
        "Intermediate stops:",
        int(farthest["flight_legs"]) - 1
    )

    print("\nTotal reachable airports:", len(candidates))


if __name__ == "__main__":
    main()
