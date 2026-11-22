# ISLAND HOPPER
### Airport Route Optimization with Python

## Introduction

Island Hopper is a Python project that uses OurAirports data, geographic distance calculations and graph algorithms to explore routes between airports around the world. The original journey is **Milan Malpensa (MXP), Italy → Sydney Kingsford Smith (SYD), Australia**.

The project answers:

1. Is Sydney reachable from Milan under a given aircraft range?
2. What is the route with the minimum number of intermediate stops?
3. What is the fastest route — flight time, refuelling and customs delays included?
4. What is the geographically farthest airport reachable from Milan?

It also compares different aircraft ranges from 1,500 km to 8,000 km.

## Assumptions

| Parameter | Value |
|---|---:|
| Origin | MXP – Milan Malpensa (45.6306, 8.72811) |
| Destination | SYD – Sydney Kingsford Smith (-33.946098, 151.177) |
| Maximum aircraft range | 4,000 km |
| Aircraft speed | 500 km/h |
| Refuelling time | 1 hour, at intermediate airports |
| Customs delay | 2 hours per cross-border landing |
| Maximum intermediate stops | 10 (maximum 11 flight legs) |
| Flight time calculation | Distance / speed |

Additional assumptions:

- Only medium and large airports are considered.
- Transit airports without an IATA code are usable as graph nodes: routes may use their `ident` or name.
- Every flight leg must be within the aircraft's maximum range.
- Refuelling is required at intermediate airports; it is not required at the origin or the final destination.
- A cross-border landing adds the customs delay; the destination counts as a cross-country landing for customs purposes.
- The customs delay (2 h) is an explicit modelling assumption, not a verified universal customs-processing time.
- Distances are great-circle distances via the Haversine formula, using an Earth radius of 6,371 km.

## Results at 4,000 km (MXP → SYD)

- **Sydney is reachable.** Minimum number of flight legs: **5** (intermediate stops: 4).
- **Minimum-stops route (BFS):** `MXP -> ZXT -> CN-0132 -> CN-0053 -> FKQ -> SYD`
- **Fastest route (Dijkstra):** `MXP -> LWN -> NAG -> VO94 -> KTA -> SYD`
  - 5 flight legs (4 intermediate stops), about **43.5 hours** of travel time (≈ 1.8 days).
- **Reachable airports from Milan:** 5,280
- **Farthest reachable airport:** **CHT** — Inia William Tuuta Memorial Airport, 19,557.77 km from Milan, reachable with 5 flight legs.

Note: the previous routing implementation reported 4,567 reachable airports; the current code reports 5,280 (verified with `scripts/check_reachable.py`).

## Range sensitivity (MXP → SYD)

`python3 -m scripts.check_analysis` prints the following table (reproduced by `analysis.ipynb`):

| Range (km) | SYD Reachable? | Min Legs | Min Stops | Fastest (hrs) | Reachable Airports | Farthest Dist (km) |
|---|---|---|---|---|---|---|
| 1500 | False | – | – | – | 4,971 | 15,879.13 |
| 2000 | True | 9 | 8 | 49.94 | 5,235 | 19,557.77 |
| 2500 | True | 7 | 6 | 48.46 | 5,273 | 19,557.77 |
| 3000 | True | 6 | 5 | 46.23 | 5,280 | 19,557.77 |
| 3500 | True | 5 | 4 | 44.76 | 5,280 | 19,557.77 |
| 4000 | True | 5 | 4 | 43.45 | 5,280 | 19,557.77 |
| 5000 | True | 4 | 3 | 41.92 | 5,280 | 19,557.77 |
| 6000 | True | 3 | 2 | 40.20 | 5,280 | 19,557.77 |
| 7000 | True | 3 | 2 | 39.19 | 5,280 | 19,557.77 |
| 8000 | True | 3 | 2 | 39.18 | 5,280 | 19,557.77 |

Fastest routes by aircraft range (from `scripts/check_analysis.py`):

- 2,000 km: `MXP -> RU-0240 -> OSW -> YIN -> YUS -> CN-0057 -> TRK -> LUV -> CNJ -> SYD` (49.94 hrs, 8 stops)
- 2,500 km: `MXP -> RU-8363 -> OSW -> KRL -> CN-0041 -> BKI -> GPN -> BQL -> SYD` (48.46 hrs, 6 stops)
- 3,000 km: `MXP -> UG22 -> BKB -> IXZ -> KTG -> HCQ -> SYD` (46.23 hrs, 5 stops)
- 3,500 km: `MXP -> URA -> ALA -> DIN -> VCS -> BRT -> SYD` (44.76 hrs, 4 stops)
- 4,000 km: `MXP -> LWN -> NAG -> VO94 -> KTA -> SYD` (43.45 hrs, 4 stops)
- 5,000 km: `MXP -> BRI -> HQL -> JHG -> BRT -> SYD` (41.92 hrs, 3 stops)
- 6,000 km: `MXP -> IXL -> IXH -> KNX -> SYD` (40.20 hrs, 2 stops)
- 7,000 km: `MXP -> IXD -> HCQ -> SYD` (39.19 hrs, 2 stops)
- 8,000 km: `MXP -> VEPH -> BVI -> SYD` (39.18 hrs, 2 stops)

Interpretation: Sydney is not reachable at 1,500 km; it becomes reachable from 2,000 km onward, and the minimum number of stops drops as the range grows.

## Algorithms

- **BFS** — finds the route with the minimum number of flight legs: every leg counts as one step.
- **Dijkstra** — finds the fastest route. The state is `(airport_position, number_of_legs)` because the same airport can be reached with different numbers of legs. The cost of a leg is its flight time (`distance / speed`), plus refuelling time (1 hour) when departing an intermediate airport, plus the customs delay when landing in a different country. The search stops when the destination is reached or the leg limit (11) is reached.

## Data and data validation

- Source: OurAirports `airports.csv`, cleaned into `cleaned_airports.csv` by `src/data_loader.py`.
- Validation results (from `scripts/check_data.py`):
  - Medium airports: 4,106
  - Large airports: 1,175
  - Total airports: 5,281
  - Missing latitude/longitude: 0
  - Duplicate airport IDs: 0
- Columns used: `id`, `ident`, `type`, `name`, `latitude`, `longitude`, `iso_country`, `iata_code`, `icao_code`, `municipality`.

## Installation

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Scripts

```bash
python3 -m scripts.check_data       # validate the airport data
python3 -m scripts.check_distance   # Haversine distance checks
python3 -m scripts.check_sydney     # Sydney reachability and routes
python3 -m scripts.check_reachable  # reachable airports at 4,000 km
python3 -m scripts.check_farthest   # farthest reachable airport
python3 -m scripts.check_analysis   # range sensitivity table
python3 -m pytest -v                # run the test suite
```

## Tests

`python3 -m pytest -v` — **14 passed**:

- `tests/test_distance.py` — Haversine (same point, symmetry, vectorisation)
- `tests/test_routing.py` — airport lookup, neighbours within range, BFS and Dijkstra routes
- `tests/test_analysis.py` — farthest airport, route options, reachability at 1,500 and 4,000 km

## Notebook

```bash
jupyter notebook analysis.ipynb
```

The notebook covers data validation, the Sydney routes, reachability, the farthest airport, the range sensitivity analysis and the visualisations.

## Visualisations (`src/visualization.py`)

- **World route map** — all airports (light blue) and the route legs; the origin is green, intermediate stops are grey and the destination is orange.
- **World farthest-airport map** — origin and the geographically farthest reachable airport.
- **Bar chart:** number of reachable airports vs aircraft range.
- **Line chart:** minimum stops to Sydney vs aircraft range.
- **Line chart:** fastest travel time vs aircraft range.

## Streamlit app (`app.py`)

```bash
streamlit run app.py
```

The app lets you:

- Choose origin and destination airports.
- Change the maximum aircraft range, cruise speed, refuelling time and customs delay.
- Set the maximum number of intermediate stops.
- See reachability, the minimum-stops route, the fastest route and travel time.
- View the farthest reachable airport.
- View the range sensitivity table and the three charts.
- View the route map.

## Project structure

```text
island hoppers/
├── Data/                       # OurAirports CSVs (also aliased as data/)
│   ├── airports.csv
│   └── cleaned_airports.csv
├── src/
│   ├── __init__.py
│   ├── config.py               # default parameters (MXP/SYD, 4,000 km, 500 km/h, ...)
│   ├── data_loader.py          # load + clean airport data
│   ├── distance.py             # Haversine distance
│   ├── routing.py              # BFS + Dijkstra route finding
│   ├── analysis.py             # farthest airport, route options, range sweep
│   └── visualization.py        # matplotlib route maps and charts
├── scripts/
│   ├── check_data.py
│   ├── check_distance.py
│   ├── check_sydney.py
│   ├── check_reachable.py
│   ├── check_farthest.py
│   ├── check_analysis.py
│   └── download_data.py
├── tests/
│   ├── test_distance.py
│   ├── test_routing.py
│   ├── test_analysis.py
│   └── check_analysis.py
├── analysis.ipynb              # analysis notebook
├── app.py                      # Streamlit interactive app
├── requirements.txt
└── README.MD
```

## Development phases

1. Data Preparation — clean and validate airport data. ✅
2. Distance Calculation — geographic distances. ✅
3. Route Optimization — BFS and Dijkstra. ✅
4. Reachability and farthest-airport analysis. ✅
5. Range sensitivity analysis. ✅
6. Visualisations. ✅
7. Dashboard — Streamlit app. ✅

---

*Python · Graphs · Algorithms · Route Discovery · Data Visualisation*
