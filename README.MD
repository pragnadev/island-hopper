# Island Hopper
### Airport Route Optimization with Python

## Overview

Island Hopper is a Python project that explores how airports can be connected in a network and how graph algorithms can help find routes between destinations. The initial case study is a journey from Milan Malpensa Airport (MXP) to Sydney Airport (SYD).

## Problem Statement

Can a journey from a chosen starting airport to a destination airport be completed within the project’s flight constraints? The planned system will compare possible routes, estimate travel time and stops, and identify airports reachable within a maximum of 10 stops.

## Constraints

- Only medium and large airports are included.
- Each possible flight leg must be within a configurable aircraft range.
- Estimated flight time is calculated at 500 km/h.
- Each intermediate refuelling stop adds 1 hour.
- A configurable customs delay applies when crossing country borders.
- Distances are calculated from airport coordinates using the Haversine formula. They are geographic estimates, not actual flight paths.

## Tech Stack

- **Python** — core development
- **Pandas** — data cleaning and processing
- **Graph Theory** — airport network modelling
- **BFS and DFS** — planned graph traversal and route exploration
- **Dijkstra’s Algorithm** — planned route optimization using weighted distances or travel times
- **Streamlit** — planned interactive dashboard
- **Git and GitHub** — version control

## Progress So Far

### Completed
- Loaded and inspected the original `Data/airports.csv` dataset (86,153 rows and 19 columns).
- Filtered the data to medium and large airports.
- Selected the required airport identifiers and location fields.
- Checked coordinates and removed airports with missing latitude or longitude.
- Saved the cleaned dataset as `Data/cleaned_airports.csv` (5,281 airports, 10 columns).
- Implemented the Haversine distance calculation.
- Calculated the estimated geographic distance from MXP to SYD: **16,591.87 km**.
- Checked the distance calculation for the same airport as both origin and destination: **0 km**.

### In Progress / Planned
1. Validate and use a source of airport-to-airport flight connections, or clearly define simulated connections if required.
2. Build the airport graph using the aircraft-range constraint.
3. Implement BFS, DFS, and Dijkstra’s algorithm for route search and optimization.
4. Apply flight-time, refuelling, customs, and stop-count constraints.
5. Test reachable and unreachable journeys, then build a Streamlit dashboard with route results and visualizations.

**Current stage:** Airport data preparation and geographic distance calculation. Graph construction, route-finding algorithms, and the dashboard are not yet complete.

## Project Structure

```text
island-hopper/
├── Data/
│   ├── airports.csv
│   └── cleaned_airports.csv
├── src/
│   ├── data_loader.py
│   └── distance.py
├── .gitignore
└── README.md
```

*The file list above reflects the expected files used so far; update it if the repository structure changes.*

## Run

Run commands from the project root. The exact command depends on the current script entry point.

Install the main data-processing dependency:

```bash
pip install pandas
```

## Project Goal

Build a working, testable airport route-finding application that combines data cleaning, geographic distance calculations, graph algorithms, and an interactive dashboard.
