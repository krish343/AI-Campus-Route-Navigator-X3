## 1. Project objective

This project models the supplied CU Technology Campus map as a weighted graph and compares two AI routing agents:

- **PATHFINDER** — Greedy Best-First Search, using `f(n) = h(n)`.
- **ORBIT** — A*, using `f(n) = g(n) + h(n)`.

The implementation also enforces the assignment-specific CSE-zone routing constraint.

The project is intentionally implemented from scratch without an external pathfinding library.

## 2. Project structure

```text
campus-navigator/
├── agents.py          # PATHFINDER and ORBIT agent classes
├── campus.json        # Campus nodes, edges, coordinates and costs
├── campus_map.py      # Graph loading, validation and CSE routing rules
├── config.py          # Shared paths and routing constants
├── experiment.py      # Reproducible algorithm comparison
├── main.py            # Interactive command-line interface
├── models.py          # Search-state and result data models
├── search.py          # Greedy Best-First Search and A*
├── test_search.py     # Standard-library regression tests
├── requirements.txt   # Dependency declaration
├── results.csv        # Latest experiment output
├── REPORT.md          # Short technical report
└── README.md          # Project documentation
```

Generated Python cache files are deliberately excluded from the project distribution.

## 3. Requirements

- Python **3.9 or newer**.
- No third-party Python package is required.

The implementation uses only the Python standard library.

## 4. Running the project

### Interactive navigator

```bash
python main.py
```

The program lists all available locations and asks for a start and destination.

### Run the experiments

```bash
python experiment.py
```

This regenerates `results.csv` using the six assignment test cases and both agents.

### Run regression tests

```bash
python -m unittest -v
```

## 5. Graph representation

`campus.json` contains three pieces of information:

1. **Nodes** — named campus locations and approximate `(x, y)` map coordinates.
2. **Edges** — walkable connections and their approximate costs in metres.
3. **Routing metadata** — the locations used by the CSE-zone rule.

The graph is loaded at runtime, so campus data is separated from the search implementation.

`CampusGraph` also validates that every edge references a known location and that all edge costs are positive.

## 6. Search state

A normal graph node is not enough to represent the assignment's CSE constraint. The search therefore uses:

```text
(location, mode, previous_location)
```

where `mode` is one of:

- `normal` — ordinary campus traversal.
- `cse` — currently inside the CSE zone.
- `cse_exit` — at the Lift Area after leaving CSE and waiting to reach a Tower 2 entry.

This prevents the same physical location from being treated identically when the required routing context is different.

## 7. CSE-zone routing rule

The CSE zone contains:

- CSE Laboratory
- CSE_AKC Seminar Hall
- CSE_Reflexon Room

### Entering CSE

A route from the ordinary campus can enter CSE only through:

```text
Tower 2 Front/Rear Entry → Lift Area → CSE location
```

### Moving inside CSE

While inside the zone, only other CSE locations or the Lift Area may be entered.

### Leaving CSE

Leaving follows:

```text
CSE location → Lift Area → Tower 2 Front/Rear Entry → ordinary campus
```

The initial search state is also important: if the requested start location is already inside CSE, the search starts in `cse` mode rather than incorrectly treating that location as an ordinary campus node.

## 8. Heuristic

For node `n` and destination `d`, the common heuristic is:

```text
h(n) = 0.55 × sqrt((x_n - x_d)^2 + (y_n - y_d)^2)
```

The coordinates come from the approximate campus-map model. The scale factor is deliberately conservative relative to the stored edge costs.

Both agents use exactly the same heuristic, making the comparison about their search strategies rather than different heuristic functions.

## 9. Algorithms

### PATHFINDER — Greedy Best-First Search

PATHFINDER prioritizes the state with the smallest:

```text
f(n) = h(n)
```

It therefore focuses on apparent closeness to the destination and ignores the route cost already accumulated when choosing its next state.

### ORBIT — A*

ORBIT prioritizes:

```text
f(n) = g(n) + h(n)
```

where `g(n)` is the actual cost from the start to the current state.

A* therefore balances the cost already travelled against the estimated remaining cost.

## 10. Result interpretation

`results.csv` records:

- source location,
- destination,
- agent,
- selected route,
- route cost in metres,
- number of explored search states,
- execution time.

Execution time is machine-dependent and should be treated as an indicative measurement rather than a fixed benchmark.

A Greedy search may explore fewer states while still returning a more expensive route. A* considers accumulated path cost and is designed to find a least-cost route when its assumptions hold.

## 11. Refactoring decisions

The original implementation mixed graph representation, routing constraints, search logic, configuration, and data models in one module. The refactored version separates these responsibilities:

- `campus_map.py` owns graph behaviour and routing constraints.
- `search.py` owns search algorithms.
- `agents.py` provides the two named AI agents.
- `models.py` provides immutable search/result models.
- `config.py` centralizes shared constants and project paths.
- `experiment.py` handles repeatable evaluation and CSV output.
- `main.py` contains only the interactive CLI layer.
- `test_search.py` protects the key routing behaviour against regressions.

The refactor also removes wildcard-style compatibility exports, reduces duplicated logic, adds type hints and validation, uses `pathlib` for file handling, and avoids hard-coded project-relative output paths.

## 12. Academic modelling note

The campus graph, coordinates, connectivity, and walking costs are modelling choices derived from the supplied map. They are not a survey of actual walking distances. They should be checked against the map and the student's own campus knowledge before final submission.
