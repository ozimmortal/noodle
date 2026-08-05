from pathlib import Path
import os

APP_VERSION = "0.1.0"
current_dir = Path(__file__).parent
settings_path = os.path.join(current_dir.parent, "data/settings.json")


settings = {"mode": "time", "choice": 30, "language": "english"}

game_options = {
    "modes": {
        "time": [15, 30, 60, 120],
        "words": [15, 25, 50, 100],
        "quote": ["short", "medium", "long"],
    },
    "languages": ["english", "french"],
}
