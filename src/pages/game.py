from textual.screen import Screen
from textual.widgets import Static
from components.footer import Footer
from components.logo import BrandHeader
from components.countdown import CountDownBlock
from components.stopwatch import StopWatch
from lib.state import settings_path, settings
import json

FOOTER_ELEMENTS = [
    ["ctrl+b", "Back"],
    ["ctrl+q", "quit"],
]


class GameScreen(Screen):
    def __init__(self, name=None, id=None, classes=None):
        super().__init__(name, id, classes)
        self.mode = settings.get("mode")
        self.choice = settings.get("choice")
        self.language = settings.get("language")

    def compose(self):
        yield BrandHeader()
        yield Footer(elements=FOOTER_ELEMENTS)
