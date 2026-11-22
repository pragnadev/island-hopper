
from src.data_loader import load_airports

airports = load_airports()

print("Dataset shape:", airports.shape)

print("\nAirport types:")
print(airports["type"].value_counts())

print("\nMissing coordinates:")
print(airports[["latitude", "longitude"]].isnull().sum())

print("\nDuplicate IDs:")
print(airports["id"].duplicated().sum())

print("\nMXP:")
print(
    airports[airports["iata_code"] == "MXP"][
        ["name", "latitude", "longitude"]
    ]
)

print("\nSYD:")
print(
    airports[airports["iata_code"] == "SYD"][
        ["name", "latitude", "longitude"]
    ]
)
