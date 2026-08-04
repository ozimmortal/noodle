from textual.containers import Horizontal
from textual.screen import Screen
from components.footer import Footer
from components.logo import BrandHeader
from components.options import OptionsTab
from textual.widgets import Label
from textual.widget import Widget
from textual.binding import Binding
from .game import GameScreen
import json, webbrowser
from lib.state import settings_path


class Button(Widget):
    DEFAULT_CSS = """
    Button {
        width: auto;
        height: auto;
        margin: 0 1;
        align: center middle
    }

    Button > Horizontal {
        width: auto;
        height: auto;
        padding: 0 1;
        align: center middle;
    }

    .label{
        color: #e2c27d;
        text-style: bold underline;
        width: auto;
        height: auto;
    }

    .label:hover {
        background: #969696 50%;
    }
    """

    def __init__(self, label: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label = label

    def compose(self):
        with Horizontal():
            yield Label(self.label, classes="label")

    def _on_click(self, event):
        self.app.push_screen(GameScreen())


with open(settings_path, "r") as f:
    data = json.load(f)

options = data["game_options"]
MODES = options["modes"]

AVAILABLE_LANGUAGES = options["languages"]
footer_elements = [
    ["tab", "cycle options"],
    ["← →", "change value"],
    ["ctrl+q", "quit"],
]


class HomeScreen(Screen):

    BINDINGS = [
        Binding("ctrl+l", "redirect_link", "Redirect Link"),
    ]

    def compose(self):

        yield BrandHeader()
        yield OptionsTab(modes=MODES, languages=AVAILABLE_LANGUAGES)
        with Horizontal(id="start-prompt"):
            yield Label("press", classes="prompt-text")
            yield Button("space")
            yield Label("to start", classes="prompt-text")
        yield Footer(elements=footer_elements)

    def _on_key(self, event):
        if event.key == "space":
            self.app.push_screen(GameScreen())

    def action_redirect_link(self) -> None:
        webbrowser.open("https://github.com/ozimmortal/belly")
