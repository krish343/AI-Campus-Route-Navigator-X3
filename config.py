"""Application constants for the AI Campus Route Navigator."""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
CAMPUS_DATA_FILE = PROJECT_ROOT / "campus.json"
RESULTS_FILE = PROJECT_ROOT / "results.csv"

CSE_ZONE = frozenset(
    {
        "CSE Laboratory",
        "CSE_AKC Seminar Hall",
        "CSE_Reflexon Room",
    }
)

TOWER_ENTRIES = frozenset(
    {
        "Tower 2 Front Entry",
        "Tower 2 Rear Entry",
    }
)

CSE_LIFT = "Lift Area"
HEURISTIC_SCALE = 0.55

PROJECT_TITLE = "AI Campus Route Navigator"
