"""Routing agents built on top of the shared search engine."""

from campus_map import CampusGraph
from models import SearchResult
from search import SearchEngine


class Agent:
    """Base class for a named routing strategy."""

    name = "AGENT"

    def __init__(self, graph: CampusGraph):
        self.engine = SearchEngine(graph)

    def solve(self, start: str, goal: str) -> SearchResult:
        raise NotImplementedError


class Pathfinder(Agent):
    """PATHFINDER uses Greedy Best-First Search."""

    name = "PATHFINDER"

    def solve(self, start: str, goal: str) -> SearchResult:
        return self.engine.greedy_best_first(start, goal)


class Orbit(Agent):
    """ORBIT uses A*."""

    name = "ORBIT"

    def solve(self, start: str, goal: str) -> SearchResult:
        return self.engine.a_star(start, goal)


__all__ = ["Agent", "Pathfinder", "Orbit"]
