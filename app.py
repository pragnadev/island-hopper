import matplotlib.pyplot as plt
import streamlit as st

from src import visualization
from src.analysis import (
    analyze_route_options,
    find_farthest_reachable_airport,
    run_range_sensitivity_analysis,
)
from src.config import DEFAULT_DESTINATION, DEFAULT_ORIGIN, MAX_STOPS, RANGE_KM
from src.data_loader import load_airports
from src.routing import reachable_within

ST_RANGES = [1500, 2000, 2500, 3000, 3500, 4000, 5000, 6000, 7000, 8000]


@st.cache_data
def range_sensitivity(origin_code, destination_code, speed_kmh,
                      refuel_h, customs_h, max_stops):
    airports = load_airports()

    return run_range_sensitivity_analysis(
        airports,
        origin_code=origin_code,
        destination_code=destination_code,
        ranges=list(ST_RANGES),
        speed_kmh=speed_kmh,
        refuel_hours=refuel_h,
        customs_hours=customs_h,
        max_stops=max_stops,
    )


def main():
    st.set_page_config(page_title="Island Hopper", layout="wide")

    airports = load_airports()

    codes = sorted(
        airports["iata_code"].dropna().astype(str).unique().tolist()
    )

    if not codes:
        st.error("No airports found in the dataset.")
        return

    st.title("Island Hopper — Route Analysis")
    st.markdown(
        "Analyse routes between airports around the world using OurAirports "
        "data. Adjust the aircraft parameters and compare routes for "
        "different maximum ranges."
    )

    with st.sidebar:
        origin = st.selectbox(
            "Origin airport", codes,
            index=codes.index(DEFAULT_ORIGIN) if DEFAULT_ORIGIN in codes else 0,
        )
        destination = st.selectbox(
            "Destination airport", codes,
            index=(codes.index(DEFAULT_DESTINATION)
                   if DEFAULT_DESTINATION in codes else len(codes) - 1),
        )
        max_range_km = st.slider(
            "Maximum aircraft range (km)", 1500, 8000, RANGE_KM, 250,
        )
        speed_kmh = st.number_input("Cruise speed (km/h)", 100, 1000, 500, 10)
        refuel_h = st.number_input("Refuelling time (hours)", 0.0, 10.0, 1.0, 0.5)
        customs_h = st.number_input("Customs delay (hours)", 0.0, 10.0, 2.0, 0.5)
        max_stops = st.slider("Maximum intermediate stops", 0, 20, MAX_STOPS, 1)

    if origin == destination:
        st.warning("Please choose different origin and destination airports.")
        return

    options = analyze_route_options(
        airports,
        origin,
        destination,
        max_range_km,
        speed_kmh=speed_kmh,
        refuel_hours=refuel_h,
        customs_hours=customs_h,
        max_stops=max_stops,
    )

    reachable = reachable_within(airports, origin, max_range_km, max_stops=max_stops)
    reachable.pop(origin, None)
    st.metric("Reachable airports from origin", len(reachable))

    st.write("### Route")

    if options["destination_reachable"]:
        st.success(
            f"{destination} is reachable from {origin} within {max_stops} stops."
        )
        st.write("**Minimum-stops route (BFS)**")
        st.write("`" + " -> ".join(options["bfs_route"]) + "`")
        st.write(f"- Flight legs: {options['bfs_legs']}")
        st.write(f"- Intermediate stops: {options['bfs_stops']}")
        st.write("**Fastest route (Dijkstra)**")
        st.write("`" + " -> ".join(options["fastest_route"]) + "`")
        st.write(f"- Flight legs: {options['fastest_legs']}")
        st.write(f"- Intermediate stops: {options['fastest_stops']}")
        st.write(f"- Fastest travel time: {options['fastest_time_hours']} hours")
    else:
        st.error(
            f"{destination} is not reachable from {origin} within {max_stops} stops."
        )

    farthest = find_farthest_reachable_airport(
        airports, origin, max_range_km, max_stops=max_stops,
    )
    if farthest:
        st.write(
            f"Farthest reachable airport: **{farthest['name']} "
            f"({farthest['iata_code']})**, {farthest['distance_km']} km from "
            f"{origin}, {farthest['flight_legs']} legs."
        )

    if options["bfs_route"]:
        st.pyplot(visualization.plot_route_map(
            airports,
            options["bfs_route"],
            title=f"{origin} → {destination} — range {max_range_km} km",
        ))
        plt.close("all")

    st.write("### Range sensitivity (default ranges, 1,500–8,000 km)")
    sensitivity = range_sensitivity(
        origin, destination, speed_kmh, refuel_h, customs_h, max_stops,
    )

    display_cols = [
        "range_km", "destination_reachable", "min_legs", "min_stops",
        "fastest_time_hours", "reachable_airports",
        "farthest_airport_iata", "farthest_distance_km",
    ]
    st.dataframe(sensitivity[display_cols], width="stretch")

    st.pyplot(visualization.plot_reachability_vs_range(sensitivity))
    plt.close("all")
    st.pyplot(visualization.plot_min_stops_vs_range(sensitivity))
    plt.close("all")
    st.pyplot(visualization.plot_fastest_time_vs_range(sensitivity))
    plt.close("all")

    farthest_label = (
        (farthest["iata_code"] or farthest["ident"] or farthest["name"])
        if farthest else None
    )
    if farthest_label:
        st.pyplot(visualization.plot_farthest_airport_map(
            airports, origin, farthest_label,
            title=f"Farthest reachable airport from {origin}",
        ))
        plt.close("all")


if __name__ == "__main__":
    main()
