from textual.screen import Screen
from textual.widgets import Static
from lib.state import settings_path
import json


class GameScreen(Screen):

    def compose(self):
        game_settings = self.get_settings()
        yield Static(
            f"mode - {game_settings["mode"]}\nchoice - {game_settings["choice"]}\nlanguage - {game_settings["language"]}"
        )

    def get_settings(self):
        with open(settings_path, "r") as f:
            data = json.load(f)
        return data["game_settings"]
