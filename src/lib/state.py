from pathlib import Path
import os

APP_VERSION = "0.1.0"
current_dir = Path(__file__).parent
settings_path = os.path.join(current_dir.parent, "data/settings.json")
