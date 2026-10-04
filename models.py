"""Small data models shared by the graph and search modules."""

from dataclasses import dataclass
from typing import Optional, Tuple


@dataclass(frozen=True)
class NodeState:
    """A search state, including routing context required by the CSE rule."""

    location: str
    mode: str = "normal"
    previous_location: Optional[str] = None


@dataclass(frozen=True)
class SearchResult:
    """Outcome and metrics produced by a routing algorithm."""

    route: Tuple[str, ...]
    cost: float
    explored: int
    elapsed: float

    @property
    def found(self) -> bool:
        return bool(self.route)
