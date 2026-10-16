# ISLAND HOPPER
### Airport Route Optimization with Python

## Introduction
Island Hopper is a Python project that uses airport data, graph theory, and route-finding algorithms to explore routes between airports. The initial journey connects Milan Malpensa (MXP) to Sydney (SYD).

## The Actual Problem
Given a network of airports and possible connections, how can we find a route between two destinations with the minimum total geographic distance?

## Constraints
- Only medium and large airports are considered.
- Routes depend on the airport connections defined in the project.
- Distances are estimated using geographic coordinates, not actual flight paths.
- The shortest-distance route may not be the fastest, cheapest, or a real bookable flight.

## Tech Stack
- **Python** — core development
- **Pandas** — data cleaning and processing
- **Graph Theory** — airport network modelling
- **BFS and DFS** — graph traversal
- **Dijkstra's Algorithm** — shortest-distance routing
- **Streamlit** — interactive dashboard
- **Visualisation Tools** — route and data display

## Development Phases
1. **Data Preparation** — clean and validate airport data.
2. **Distance Calculation** — calculate geographic distances.
3. **Graph Construction** — model airports and connections.
4. **Route Optimization** — implement BFS, DFS, and Dijkstra's algorithm.
5. **Dashboard** — visualise routes and results using Streamlit.

## Project Structure
```text
island-hoppers/
├── Data/
│   ├── airports.csv
│   └── cleaned_airports.csv
├── src/
│   └── data_loader.py
├── .gitignore
└── README.md
```

## Current Status
**Phase 1 — Data Preparation**

The original dataset contains 86,153 records. Filtering for medium and large airports leaves 5,281 records. Column selection, coordinate validation, and duplicate checks are complete. Final dataset saving and subsequent routing phases remain in progress.

---

*Python · Graphs · Algorithms · Route Discovery*