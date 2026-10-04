"""Interactive command-line interface for the campus route navigator."""

from __future__ import annotations

from agents import Orbit, Pathfinder
from campus_map import CampusGraph, load_campus
from config import PROJECT_TITLE


def print_result(agent_name: str, result) -> None:
    print(f"\n{agent_name}")
    print("Route:", " -> ".join(result.route) if result.found else "No route found")
    print(f"Cost: {result.cost:.2f} m" if result.found else "Cost: unavailable")
    print(f"Nodes explored: {result.explored}")
    print(f"Time: {result.elapsed:.6f} s")


def display_locations(graph: CampusGraph) -> None:
    print("Available locations:")
    for index, name in enumerate(sorted(graph.nodes), start=1):
        print(f"{index:2}. {name}")


def main() -> None:
    graph = load_campus()
    pathfinder = Pathfinder(graph)
    orbit = Orbit(graph)

    print(PROJECT_TITLE)
    print("=" * len(PROJECT_TITLE))
    display_locations(graph)

    start = input("\nEnter starting location: ").strip()
    goal = input("Enter destination: ").strip()

    invalid = [name for name in (start, goal) if name not in graph.nodes]
    if invalid:
        print("\nInvalid location. Choose a name exactly as listed above.")
        return

    print_result(pathfinder.name, pathfinder.solve(start, goal))
    print_result(orbit.name, orbit.solve(start, goal))


if __name__ == "__main__":
    main()
