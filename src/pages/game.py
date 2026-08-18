from textual.screen import Screen
from textual.containers import Container
from components.footer import Footer
from components.logo import BrandHeader
from components.countdown import CountDownBlock
from components.type_area import TypeArea, Word
from lib.state import settings
from textual.binding import Binding

FOOTER_ELEMENTS = [
    ["ctrl+b", "Back"],
    ["ctrl+q", "quit"],
]


class GameScreen(Screen):
    DEFAULT_CSS = """
    #body {
        width: 100%;
        height: 1fr;
        align: center middle;
    }

    CountDownBlock{
        width: 80%;
    }

    TypeArea {
        width: 80%;
        height: auto;
    }
    
"""

    BINDINGS = [Binding("ctrl+b", "go_back", "Go Back Home")]

    def __init__(self, name=None, id=None, classes=None):
        super().__init__(name, id, classes)
        self.mode = settings.get("mode")
        self.choice = settings.get("choice")
        self.language = settings.get("language")
        sample_text = (
            "the quick brown fox jumps over the lazy dog "
            "textual python terminal user interface library"
            "the quick brown fox jumps over the lazy dog "
            "textual python terminal user interface library"
            "textual python terminal user interface library"
            "textual python terminal user interface library"
            "textual python terminal user interface library"
            "textual python terminal user interface library"
            "textual python terminal user interface library"
        )  # replace these by generating random words from the store
        self.words = [Word(w) for w in sample_text.split()]
        self.type_area = TypeArea(self.words)

    def compose(self):
        yield BrandHeader()
        with Container(id="body"):
            yield CountDownBlock(self.choice)
            yield self.type_area
        yield Footer(elements=FOOTER_ELEMENTS)

    def action_go_back(self) -> None:
        self.app.pop_screen()
