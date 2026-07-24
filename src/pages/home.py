from textual.containers import Horizontal
from textual.screen import Screen
from components.footer import Footer
from components.logo import BrandHeader
from components.options import OptionsTab
from textual.widgets import Label 
from textual.widget import Widget
from textual.binding import Binding
import webbrowser

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

    .label:hover{
        opacity: 60%;
    }
    """

    def __init__(self, label: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label = label

    def compose(self):
        with Horizontal():
            yield Label(self.label, classes="label")

    def _on_click(self, event):
        pass

TABS_DATA = [
    {
        "header" : "mode",
        "options" : ["time", "words", "quote"]
    },
    {
        "header" : "duration",
        "options" : ["15", "30", "60", "120"]
    }
]

footer_elements = [["tab", "cycle options"], ["← →", "change value"],  ["ctrl+q", "quit"]]        



class HomeScreen(Screen):

    BINDINGS = [
        Binding("ctrl+l", "redirect_link", "Redirect Link"),
    ]

    def compose(self):
       
        yield BrandHeader()
        yield OptionsTab(collections=TABS_DATA)
        with Horizontal(id="start-prompt"):
            yield Label("press", classes="prompt-text")
            yield Button("space")
            yield Label("to start", classes="prompt-text")
        yield Footer(elements=footer_elements)

    def _on_key(self, event):
        if event.key == "space":
            pass

    def action_redirect_link(self) -> None:
        webbrowser.open("https://github.com/ozimmortal/belly")