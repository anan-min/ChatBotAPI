import sys
from pathlib import Path


def add_path():
    current_dir = Path(__file__).parent

    # Add the parent directory to sys.path
    sys.path.insert(0, str(current_dir.parent))