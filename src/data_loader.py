
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DATA_PATH = PROJECT_ROOT / "data" / "airports.csv"
CLEAN_DATA_PATH = PROJECT_ROOT / "data" / "cleaned_airports.csv"


def load_raw_airports(path=RAW_DATA_PATH):
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"Dataset not found: {path}")

    return pd.read_csv(path)


def clean_airports(df):
    required_columns = [
        "id", "ident", "type", "name",
        "latitude_deg", "longitude_deg",
        "iso_country", "iata_code",
        "icao_code", "municipality"
    ]

    missing = set(required_columns) - set(df.columns)

    if missing:
        raise ValueError(f"Missing columns: {missing}")

    airports = df[required_columns].copy()

    airports = airports[
        airports["type"].isin(
            ["medium_airport", "large_airport"]
        )
    ].copy()

    airports = airports.rename(columns={
        "latitude_deg": "latitude",
        "longitude_deg": "longitude"
    })

    airports = airports.dropna(
        subset=["latitude", "longitude"]
    )

    airports = airports[
        airports["latitude"].between(-90, 90)
        & airports["longitude"].between(-180, 180)
    ].copy()

    airports = airports.drop_duplicates(
        subset=["id"]
    )

    return airports.reset_index(drop=True)


def load_airports():
    if CLEAN_DATA_PATH.exists():
        return pd.read_csv(CLEAN_DATA_PATH)

    raw = load_raw_airports()
    cleaned = clean_airports(raw)

    CLEAN_DATA_PATH.parent.mkdir(
        parents=True, exist_ok=True
    )

    cleaned.to_csv(CLEAN_DATA_PATH, index=False)

    return cleaned
  