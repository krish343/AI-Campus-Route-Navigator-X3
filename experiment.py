"""Run the assignment's comparison experiments and write results.csv."""

from __future__ import annotations

import csv
from pathlib import Path

from agents import Agent, Orbit, Pathfinder
from campus_map import load_campus
from config import RESULTS_FILE

EXPERIMENTS = (
    ("Reception of Calcutta University", "Library"),
    ("Canteen, CU Technology Campus", "New Building 2 (Workshop Building)"),
    ("Entry Gate 1 (G1)", "CSE Laboratory"),
    ("Auditorium Hall", "CSE_AKC Seminar Hall"),
    ("Library", "Canteen, CU Technology Campus"),
    ("CSE_Reflexon Room", "Entry Gate 4 (G4)"),
)

FIELDNAMES = (
    "start",
    "destination",
    "agent",
    "route",
    "path_cost_m",
    "nodes_explored",
    "time_seconds",
)


def run_experiments(output_path: str | Path = RESULTS_FILE) -> list[dict]:
    """Run every experiment for both agents and save a CSV report."""
    graph = load_campus()
    agents: tuple[Agent, ...] = (Pathfinder(graph), Orbit(graph))
    rows = []

    for start, goal in EXPERIMENTS:
        for agent in agents:
            result = agent.solve(start, goal)
            rows.append(
                {
                    "start": start,
                    "destination": goal,
                    "agent": agent.name,
                    "route": " -> ".join(result.route),
                    "path_cost_m": round(result.cost, 2),
                    "nodes_explored": result.explored,
                    "time_seconds": round(result.elapsed, 6),
                }
            )

    output_path = Path(output_path)
    with output_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)

    return rows


if __name__ == "__main__":
    run_experiments()
    print(f"Saved results to {RESULTS_FILE}")
