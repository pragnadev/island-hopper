import matplotlib.pyplot as plt
import pandas as pd


def _lookup_airport(airports, label):
    label = str(label).strip().upper()

    for column in ["iata_code", "ident", "name"]:
        if column not in airports.columns:
            continue

        matches = airports[
            airports[column].fillna("").astype(str).str.upper() == label
        ]

        if not matches.empty:
            return matches.iloc[0]

    raise ValueError(f"Airport label {label!r} not found in the data.")


def plot_route_map(airports, route, title="Island Hopper route", figsize=(12, 8)):
    fig, ax = plt.subplots(figsize=figsize)

    ax.scatter(
        airports["longitude"],
        airports["latitude"],
        s=5,
        alpha=0.25,
        c="#b0d8f0",
        label="Airports",
    )

    points = [_lookup_airport(airports, label) for label in route]
    lats = [float(point["latitude"]) for point in points]
    lons = [float(point["longitude"]) for point in points]

    for i in range(len(lats) - 1):
        ax.plot(
            [lons[i], lons[i + 1]],
            [lats[i], lats[i + 1]],
            color="#d62728",
            lw=1.6,
        )

    ax.scatter([lons[0]], [lats[0]], color="#2e7d32", s=70, zorder=5,
               label="Origin")

    if len(lats) > 2:
        ax.scatter(lons[1:-1], lats[1:-1], color="#9e9e9e", s=25, zorder=5,
                   label="Intermediate stops")

    ax.scatter([lons[-1]], [lats[-1]], color="#d62728", s=70, zorder=5,
               label="Destination")

    ax.set_xlim(-180, 180)
    ax.set_ylim(-90, 90)
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.set_title(title)
    ax.legend(loc="upper left", fontsize="small")
    ax.grid(alpha=0.3)
    fig.tight_layout()

    return fig


def plot_farthest_airport_map(airports, origin_label, farthest_label,
                              title="Farthest reachable airport",
                              figsize=(10, 6)):
    fig, ax = plt.subplots(figsize=figsize)

    origin = _lookup_airport(airports, origin_label)
    farthest = _lookup_airport(airports, farthest_label)

    lons = [float(origin["longitude"]), float(farthest["longitude"])]
    lats = [float(origin["latitude"]), float(farthest["latitude"])]

    ax.plot(lons, lats, color="#d62728", alpha=0.5, lw=1)
    ax.scatter([lons[0]], [lats[0]], color="#2e7d32", s=80, zorder=5,
               label=f"Origin: {origin_label}")
    ax.scatter([lons[1]], [lats[1]], color="#d62728", s=80, zorder=5,
               label=f"Farthest: {farthest_label}")
    ax.annotate(farthest["name"], xy=(lons[1], lats[1]),
                xytext=(8, 8), textcoords="offset points",
                fontsize="small")

    ax.set_xlim(-180, 180)
    ax.set_ylim(-90, 90)
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.set_title(title)
    ax.legend()
    ax.grid(alpha=0.3)
    fig.tight_layout()

    return fig


def plot_reachability_vs_range(df, figsize=(10, 5)):
    df = df.sort_values("range_km")

    gaps = df["range_km"].diff().dropna()
    bar_width = 0.45 * gaps.min() if not gaps.empty else 100

    fig, ax = plt.subplots(figsize=figsize)
    ax.bar(df["range_km"], df["reachable_airports"], width=bar_width,
           color="#4C72B0")
    ax.set_xlabel("Aircraft range (km)")
    ax.set_ylabel("Reachable airports")
    ax.set_title("Reachable airports vs. aircraft range")
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()

    return fig


def plot_min_stops_vs_range(df, figsize=(10, 5)):
    df = df.sort_values("range_km")

    mask = df["destination_reachable"].fillna(False).astype(bool)
    stops = pd.to_numeric(df["min_stops"], errors="coerce")

    fig, ax = plt.subplots(figsize=figsize)
    ax.plot(df.loc[mask, "range_km"], stops[mask],
            marker="o", color="#4C72B0")
    ax.set_xlabel("Aircraft range (km)")
    ax.set_ylabel("Minimum intermediate stops")
    ax.set_title("Minimum stops vs. aircraft range")
    ax.set_ylim(bottom=-0.5)
    ax.grid(alpha=0.3)
    fig.tight_layout()

    return fig


def plot_fastest_time_vs_range(df, figsize=(10, 5)):
    df = df.sort_values("range_km")

    times = pd.to_numeric(df["fastest_time_hours"], errors="coerce")
    mask = times.notna()

    fig, ax = plt.subplots(figsize=figsize)
    ax.plot(df.loc[mask, "range_km"], times[mask],
            marker="o", color="#DD8452")
    ax.set_xlabel("Aircraft range (km)")
    ax.set_ylabel("Fastest travel time (hours)")
    ax.set_title("Fastest travel time vs. aircraft range")
    ax.grid(alpha=0.3)
    fig.tight_layout()

    return fig
