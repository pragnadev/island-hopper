
from src.data_loader import load_airports
from src.distance import haversine_distance

airports = load_airports()

mxp = airports[airports["iata_code"] == "MXP"].iloc[0]
syd = airports[airports["iata_code"] == "SYD"].iloc[0]

distance = haversine_distance(
    mxp["latitude"],
    mxp["longitude"],
    syd["latitude"],
    syd["longitude"]
)

print(f"Distance from MXP to SYD: {distance:.2f} km")
