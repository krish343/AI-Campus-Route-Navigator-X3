"""Campus graph loading, validation, heuristic, and routing constraints."""

from __future__ import annotations

import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator, Mapping

from config import CAMPUS_DATA_FILE, CSE_LIFT, CSE_ZONE, HEURISTIC_SCALE, TOWER_ENTRIES
from models import NodeState


@dataclass(frozen=True)
class Edge:
    """An undirected weighted campus connection."""

    source: str
    destination: str
    cost: float


class CampusGraph:
    """Weighted campus graph with the assignment-specific CSE routing rule."""

    def __init__(self, data: Mapping):
        self.nodes = dict(data["nodes"])
        self.edges = tuple(self._parse_edges(data["edges"]))
        self.adjacency = {name: [] for name in self.nodes}
        self._build_adjacency()
        self._validate()

    @classmethod
    def from_json(cls, path: str | Path = CAMPUS_DATA_FILE) -> "CampusGraph":
        path = Path(path)
        with path.open("r", encoding="utf-8") as file:
            return cls(json.load(file))

    @staticmethod
    def _parse_edges(raw_edges) -> Iterator[Edge]:
        for edge in raw_edges:
            yield Edge(edge["from"], edge["to"], float(edge["weight_m"]))

    def _build_adjacency(self) -> None:
        for edge in self.edges:
            self.adjacency[edge.source].append((edge.destination, edge.cost))
            self.adjacency[edge.destination].append((edge.source, edge.cost))

    def _validate(self) -> None:
        if not self.nodes:
            raise ValueError("Campus graph contains no locations.")

        for edge in self.edges:
            if edge.source not in self.nodes or edge.destination not in self.nodes:
                raise ValueError(f"Edge references an unknown location: {edge}")
            if edge.cost <= 0:
                raise ValueError(f"Edge cost must be positive: {edge}")

        if missing := (CSE_ZONE | TOWER_ENTRIES | {CSE_LIFT}) - self.nodes.keys():
            raise ValueError(f"CSE routing metadata references missing locations: {sorted(missing)}")

    def heuristic(self, location: str, goal: str) -> float:
        """Return the scaled Euclidean estimate used by both agents."""
        self._require_location(location)
        self._require_location(goal)
        source = self.nodes[location]
        target = self.nodes[goal]
        return HEURISTIC_SCALE * math.hypot(
            source["x"] - target["x"],
            source["y"] - target["y"],
        )

    def initial_state(self, start: str) -> NodeState:
        """Set routing mode correctly when a route starts inside the CSE zone."""
        self._require_location(start)
        if start in CSE_ZONE:
            return NodeState(start, "cse", None)
        return NodeState(start, "normal", None)

    def neighbors(self, state: NodeState) -> Iterator[tuple[NodeState, float]]:
        """Yield legal successor states under the assignment's CSE constraint."""
        for next_location, cost in self.adjacency[state.location]:
            next_mode = self._next_mode(state, next_location)
            if next_mode is None:
                continue
            yield NodeState(next_location, next_mode, state.location), cost

    def _next_mode(self, state: NodeState, next_location: str) -> str | None:
        if state.mode == "normal":
            if next_location in CSE_ZONE:
                # CSE entry is only valid after Tower Entry -> Lift -> CSE.
                if state.location == CSE_LIFT and state.previous_location in TOWER_ENTRIES:
                    return "cse"
                return None
            return "normal"

        if state.mode == "cse":
            if next_location in CSE_ZONE:
                return "cse"
            if next_location == CSE_LIFT:
                return "cse_exit"
            return None

        if state.mode == "cse_exit":
            # After leaving CSE, the only legal next step is Lift -> Tower Entry.
            if state.location == CSE_LIFT and next_location in TOWER_ENTRIES:
                return "normal"
            return None

        raise ValueError(f"Unknown routing mode: {state.mode}")

    def _require_location(self, location: str) -> None:
        if location not in self.nodes:
            raise KeyError(f"Unknown campus location: {location}")


def load_campus(path: str | Path = CAMPUS_DATA_FILE) -> CampusGraph:
    """Load the campus graph from its JSON data file."""
    return CampusGraph.from_json(path)
