import pandas as pd

from src.data_loader import load_airports
from src.analysis import run_range_sensitivity_analysis


def main():
    print("\n=======================================================")
    print("      ISLAND HOPPER: RANGE SENSITIVITY ANALYSIS       ")
    print("=======================================================\n")

    airports = load_airports()

    ranges = [1500, 2000, 2500, 3000, 3500, 4000, 5000, 6000, 7000, 8000]

    print("Analyzing flight ranges from 1,500 km to 8,000 km...\n")

    df = run_range_sensitivity_analysis(
        airports=airports,
        origin_code="MXP",
        destination_code="SYD",
        ranges=ranges
    )

    display_df = df[[
        "range_km",
        "destination_reachable",
        "min_legs",
        "min_stops",
        "fastest_time_hours",
        "reachable_airports",
        "farthest_distance_km"
    ]].copy()

    display_df.columns = [
        "Range (km)",
        "SYD Reachable?",
        "Min Legs",
        "Min Stops",
        "Fastest (hrs)",
        "Reachable Airports",
        "Farthest Dist (km)"
    ]

    print(display_df.to_string(index=False))

    print("\n-------------------------------------------------------")
    print("Fastest Routes by Aircraft Range:")
    print("-------------------------------------------------------")
    for _, row in df.iterrows():
        r = row["range_km"]
        if row["destination_reachable"]:
            print(f"[{r} km] ({row['fastest_time_hours']} hrs, {row['min_stops']} stops):")
            print(f"   {row['fastest_route']}\n")
        else:
            print(f"[{r} km]: Sydney is NOT reachable within 10 stops.\n")

    print("=======================================================\n")


if __name__ == "__main__":
    main()
