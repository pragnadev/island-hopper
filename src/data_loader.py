
from pathlib import Path
import pandas as pd

# main project folder
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# path to the airport CSV
DATA_PATH = PROJECT_ROOT / "Data" / "airports.csv"

# Load the dataset
airports = pd.read_csv(DATA_PATH)

# Display basic information
print("Dataset shape:", airports.shape)
print("\nFirst five rows:")
print(airports.head())

print("\nAirport types:")
print(airports["type"].value_counts())
