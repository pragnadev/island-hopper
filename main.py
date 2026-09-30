import pandas as pd
airports = pd.read_csv("Data/airports.csv")
#print(airports.shape)
#print(airports.columns)
#print(airports.head())
#print(airports.info())
#print(airports.describe(include="all"))
#print(airports["type"].value_counts())
# only medium and large airports
airports = airports[airports["type"].isin(["medium_airport","large_airport"])]
#print(airports.shape)
#only columns we need
airports = airports[
    ["id","ident","name","latitude_deg","longitude_deg",
    "iso_country","iata_code","icao_code"
    ]
]
#resetting index cause it maintained original data frame
airports = airports.reset_index(drop=True)
print(airports.head())
#missing values
print(airports[["latitude_deg","longitude_deg"]].isna().sum())