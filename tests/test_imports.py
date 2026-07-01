import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


def test_app_modules_import():
    import config  # noqa: F401
    import legal_agent_team  # noqa: F401
