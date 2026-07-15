from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

CONFIG_FILE = BASE_DIR / "config" / "config.json"
STATE_FILE = BASE_DIR / "data" / "state.json"