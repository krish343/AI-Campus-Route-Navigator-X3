"""Search algorithms used by the AI Campus Route Navigator."""

from __future__ import annotations

import heapq
import time
from itertools import count
from math import inf
from typing import Callable

from campus_map import CampusGraph
from models import NodeState, SearchResult


class SearchEngine:
    """Run graph searches while keeping algorithm-specific scoring separate."""

    def __init__(self, graph: CampusGraph):
        self.graph = graph

    def greedy_best_first(self, start: str, goal: str) -> SearchResult:
        """Greedy Best-First Search: priority = h(n)."""
        return self._search(start, goal, lambda state, cost: self.graph.heuristic(state.location, goal))

    def a_star(self, start: str, goal: str) -> SearchResult:
        """A*: priority = g(n) + h(n)."""
        return self._search(
            start,
            goal,
            lambda state, cost: cost + self.graph.heuristic(state.location, goal),
        )

    def _search(
        self,
        start: str,
        goal: str,
        priority: Callable[[NodeState, float], float],
    ) -> SearchResult:
        started_at = time.perf_counter()
        initial = self.graph.initial_state(start)
        self.graph._require_location(goal)

        frontier = []
        sequence = count()
        best_cost = {initial: 0.0}
        parent = {initial: None}

        initial_priority = priority(initial, 0.0)
        heapq.heappush(frontier, (initial_priority, 0.0, next(sequence), initial))
        explored = 0

        while frontier:
            _, current_cost, _, current = heapq.heappop(frontier)

            if current_cost != best_cost.get(current):
                continue

            explored += 1
            if current.location == goal:
                route = self._reconstruct_path(parent, current)
                return SearchResult(
                    tuple(route),
                    current_cost,
                    explored,
                    time.perf_counter() - started_at,
                )

            for neighbor, edge_cost in self.graph.neighbors(current):
                new_cost = current_cost + edge_cost
                if new_cost >= best_cost.get(neighbor, inf):
                    continue

                best_cost[neighbor] = new_cost
                parent[neighbor] = current
                heapq.heappush(
                    frontier,
                    (priority(neighbor, new_cost), new_cost, next(sequence), neighbor),
                )

        return SearchResult((), inf, explored, time.perf_counter() - started_at)

    @staticmethod
    def _reconstruct_path(parent: dict[NodeState, NodeState | None], state: NodeState) -> list[str]:
        route = []
        while state is not None:
            route.append(state.location)
            state = parent[state]
        route.reverse()
        return route


__all__ = ["SearchEngine"]
