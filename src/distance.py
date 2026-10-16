
from pathlib import Path
import pandas as pd
from math import radians , sin , cos ,sqrt, atan2
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_ROOT / "Data" / "cleaned_airports.csv"
airports = pd.read_csv(DATA_PATH)
#calculate distance
def haversine_distance(lat1,lon1,lat2,lon2):
    #deg to radians
    lat1,lon1,lat2,lon2 = map(
        radians, [lat1,lon1,lat2,lon2]
    )
    #difference in coords
    dlat = lat2-lat1
    dlon= lon2-lon1
    #formula
    a = (
         sin(dlat / 2) ** 2
        + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    )
    # central angle
    c =  2 * atan2(sqrt(a), sqrt(1 - a))
    # angles to km
    earth_radius_km = 6371
    distance = earth_radius_km * c

    return distance

#cal mxp and syd dis
mxp = airports[airports["iata_code"] == "MXP"].iloc[0]
syd = airports[airports["iata_code"] == "SYD"].iloc[0]
distance = haversine_distance(
    mxp["latitude"],
    mxp["longitude"],
    syd["latitude"],
    syd["longitude"]
)
print("Starting airport:", mxp["name"], "(MXP)")
print("Destination airport:", syd["name"], "(SYD)")
print(f"Geographic distance: {distance:,.2f} km")
#test
# Test the function with the same airport
same_airport_distance = haversine_distance(
    mxp["latitude"],
    mxp["longitude"],
    mxp["latitude"],
    mxp["longitude"]
)
print(f"Distance from MXP to MXP: {same_airport_distance:.2f} km")