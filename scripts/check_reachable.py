from src.data_loader import load_airports
from src.routing import reachable_within


def main():
    airports = load_airports()

    reachable = reachable_within(
        airports,
        origin_code="MXP",
        max_range_km=4000,
        max_stops=10
    )

    reachable.pop("MXP", None)

    print("Number of reachable airports:", len(reachable))

    if not reachable:
        print("No airports are reachable.")
        return

    max_legs = max(reachable.values())

    farthest_by_legs = [
        code
        for code, legs in reachable.items()
        if legs == max_legs
    ]

    print("Maximum flight legs:", max_legs)
    print("Maximum intermediate stops:", max_legs - 1)

    print("Airports requiring the most flight legs:")
    for code in farthest_by_legs:
        print("-", code)


if __name__ == "__main__":
    main()
