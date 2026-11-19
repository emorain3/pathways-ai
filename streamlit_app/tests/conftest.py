import os
import sys
from pathlib import Path

# Make `pathways` importable and keep tests fast and offline.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
os.environ["PATHWAYS_BACKEND"] = "mock"
os.environ["PATHWAYS_MOCK_LATENCY"] = "0"
