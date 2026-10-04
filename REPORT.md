# Brief Report — AI Campus Route Navigator

## 1. Objective

The project models the CU Technology Campus as a weighted graph and compares two AI routing agents:

- **PATHFINDER:** Greedy Best-First Search.
- **ORBIT:** A* Search.

The comparison records the selected route, path cost, number of explored states, and execution time.

## 2. Graph construction

The graph uses the named locations represented in the supplied campus map. Each node stores approximate map coordinates, while each undirected edge stores an approximate walking cost in metres. The graph is stored in `campus.json`, keeping campus data separate from routing logic.

The loader validates node references and positive edge weights before a search can run.

## 3. Search state and CSE constraint

A physical location alone is insufficient because the assignment imposes special CSE-zone movement rules. The search state is therefore:

`(location, mode, previous_location)`

The three modes are `normal`, `cse`, and `cse_exit`.

The CSE zone contains CSE Laboratory, CSE_AKC Seminar Hall, and CSE_Reflexon Room. Entry is restricted to:

`Tower 2 Front/Rear Entry → Lift Area → CSE location`

Movement inside the zone is limited to CSE locations and the Lift Area. Exit is restricted to:

`CSE location → Lift Area → Tower 2 Front/Rear Entry → ordinary campus`

A route that starts inside CSE is initialized in `cse` mode, so it cannot bypass the required exit sequence.

## 4. Heuristic

Both algorithms use the same scaled Euclidean heuristic:

`h(n) = 0.55 × sqrt((x_n-x_d)^2 + (y_n-y_d)^2)`

The coordinates are approximate map coordinates and the scaling factor is conservative relative to the stored edge costs.

## 5. Algorithms

### PATHFINDER — Greedy Best-First Search

PATHFINDER prioritizes the smallest `h(n)`. It focuses on apparent closeness to the goal and does not include accumulated route cost in its priority.

### ORBIT — A*

ORBIT prioritizes `g(n) + h(n)`, where `g(n)` is the cost already travelled. This balances the route already taken with the estimated remaining cost.

## 6. Refactoring

The original code concentrated graph handling, search, configuration, and routing-agent behaviour in `search.py`. The refactored project separates these responsibilities into small modules:

- `config.py` — constants and project paths.
- `models.py` — immutable search-state/result models.
- `campus_map.py` — graph loading, validation, heuristic, and CSE transition rules.
- `search.py` — generic search engine and scoring strategies.
- `agents.py` — PATHFINDER and ORBIT.
- `experiment.py` — reproducible benchmark generation.
- `main.py` — interactive user interface.
- `test_search.py` — regression tests for key routing behaviour.

This makes the search code easier to read and the CSE rule easier to verify independently.

## 7. Experimental observations

The current `results.csv` contains six source-destination experiments, each evaluated by both agents.

Expected observations are:

- Greedy Best-First Search can reach a goal with relatively few explored states but is not guaranteed to minimize path cost.
- A* accounts for both accumulated cost and estimated remaining cost.
- The two agents can select different routes when a locally attractive route has a worse accumulated cost.
- The CSE rule can force additional movement through the Lift Area and Tower 2 entries.
- Runtime values are very small for this graph and depend on the machine and Python runtime, so they should not be treated as universal performance figures.

## 8. Conclusion

The experiment demonstrates the difference between a heuristic-only strategy and A*. PATHFINDER chooses states primarily according to estimated closeness to the destination, whereas ORBIT considers both the travelled cost and the remaining estimate. The state-based CSE rule demonstrates why a constrained routing problem may require more information than the current physical node alone.

## 9. Modelling note

The graph connectivity, coordinates, and walking costs are modelling estimates derived from the supplied map. They should be verified against the assignment map before submission.
