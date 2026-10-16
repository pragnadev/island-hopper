from pathlib import Path
import pandas as pd
Project_root = Path(__file__).resolve().parent.parent
Data_path = Project_root / "Data" / "airports.csv"
airports = pd.read_csv(Data_path)
# dataset info
print("\n Dataset size")
print("rows and columns",airports.shape)
print("Total rows:",airports.shape[0])
print("total columns :", airports.shape[1])
#col names
print("\n column names")
print(airports.columns.tolist())
#first five rows
print("\n first five rows")
print(airports.head())
#data types and non missing values
print("\n dataset inforamtion")
airports.info()
#count missing values
print("\n missing values")
print(airports.isnull().sum())
# cols with only missing values
print("/n missing value summart")
missing =  airports.isnull().sum()
print(missing[missing>0].sort_values(ascending = False))
#airport types
print("\n airport types")
print(airports["type"].value_counts())
# coords
print("\n coords sumamry")
print(airports[["latitude_deg","longitude_deg"]].describe())
#--filter--
#only med and large aiports
print("\n- BEFORE FILTERING -")
print("Rows:", len(airports))
print(airports["type"].value_counts())

airports = airports[
    airports["type"].isin(["medium_airport", "large_airport"])
].copy()

print("\n - AFTER FILTERING -")
print("Rows:", len(airports))
print(airports["type"].value_counts())

#cols needed
requried_columns = [
    "id",
    "ident",
    "type",
    "name",
    "latitude_deg",
    "longitude_deg",
    "iso_country",
    "iata_code",
    "icao_code",
    "municipality"
]
airports = airports[requried_columns].copy()
#reanme
airports = airports.rename(columns ={
    "latitude_deg" : "latitude",
    "longitude_deg" : "longitude"
})
#reset index
airports = airports.reset_index(drop=True)
print("\nFirst five cleaned rows:")
print(airports.head())
#missing values after this
print(airports.isnull().sum())
print(airports[["latitude", "longitude"]].isnull().sum())
#co ord range
invalid_coords = airports[
    (~airports["latitude"].between(-90,90)) |
    (~airports["longitude"].between(-180,180))
]
print("no.of airports with invalid coords",len(invalid_coords))
print(invalid_coords[["id","name","latitude","longitude"]].head())
#remove duplicates
#check
print("dup rows",airports.duplicated().sum())
print("dup airport ids",airports["id"].duplicated().sum())
print("dup airport identifers",airports["ident"].duplicated().sum())
#verifying if milan and sydney is present
source_airport = airports[airports["iata_code"] == "MXP"]
destination_airport = airports[airports["iata_code"] == "SYD"]

columns_to_display = [
    "id",
    "name",
    "iata_code",
    "latitude",
    "longitude"
]
print("\nSource airport (MXP):")
print(source_airport[columns_to_display])
print("\nDestination airport (SYD):")
print(destination_airport[columns_to_display])
#save this dataset
output_path = Project_root / "Data" / "cleaned_airports.csv"
airports.to_csv(output_path,index=False)
print("Saved to:", output_path)
print("Total rows saved:", len(airports))
print("Total columns saved:", len(airports.columns))
