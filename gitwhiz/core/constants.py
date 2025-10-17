from pathlib import Path

TEMPLATES = ["bugfix", "feature", "docs"]
BASE_DIR = Path(__file__).resolve().parent.parent

print(BASE_DIR)