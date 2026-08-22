from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Container, Horizontal
from textual.screen import Screen
from textual.widgets import Static, Rule
from components.footer import Footer
from components.logo import BrandHeader
from rich.text import Text

FOOTER_ITEMS = [
    ["ctrl+r", "restart"],
    ["ctrl+b", "home"],
    ["ctrl+q", "quit"],
]

DIGIT_FONT = {
    "0": [" ██ ", "█  █", "█  █", "█  █", " ██ "],
    "1": [" █  ", "██  ", " █  ", " █  ", "███ "],
    "2": ["███ ", "   █", " ██ ", "█   ", "████"],
    "3": ["███ ", "   █", " ██ ", "   █", "███ "],
    "4": ["█  █", "█  █", "████", "   █", "   █"],
    "5": ["████", "█   ", "███ ", "   █", "███ "],
    "6": [" ██ ", "█   ", "███ ", "█  █", " ██ "],
    "7": ["████", "   █", "  █ ", " █  ", " █  "],
    "8": [" ██ ", "█  █", " ██ ", "█  █", " ██ "],
    "9": [" ██ ", "█  █", " ███", "   █", " ██ "],
    " ": ["    ", "    ", "    ", "    ", "    "],
}


def render_big_number(text: str, color: str) -> str:
    """Render a string of digits as multi-line ASCII block art."""
    rows = []
    for i in range(5):
        row_str = "  ".join(DIGIT_FONT.get(ch, DIGIT_FONT[" "])[i] for ch in text)
        rows.append(row_str)

    body = "\n".join(rows)
    return f"[{color}]{body}[/]"


class EndGameScreen(Screen):
    DEFAULT_CSS = """
    EndGameScreen {
        align: center middle;
        background: #0d0d0d;
        overflow: hidden;
    }

    #results-card {
        width: auto;
        min-width: 70;
        height: auto;
        padding: 1 2;
        overflow: hidden;
    }

    .divider {
        text-align: center;
        color: #555555;
        margin-bottom: 2;
    }

    #hero-container {
        width: 100%;
        height: 9;
        margin-bottom: 1;
    }

    .hero-stat {
        width: 1fr;
        height: 100%;
        layout: vertical;
        align: center middle;
    }

    .hero-label {
        text-align: center;
        color: #555555;
        margin-bottom: 1;
        width: 100%;
    }
    
    .hero-value {
        text-align: center;
        width: 100%;
    }

    Rule {
        margin: 1 0;
        color: #202020;
    }

    #details-row {
        height: 1;
        margin-bottom: 1;
    }

    .detail-stat {
        width: 1fr;
        text-align: center;
        color: #666666;
    }

    #best-badge {
        text-align: center;
        margin-bottom: 1;
    }
    """

    BINDINGS = [
        Binding("ctrl+r", "restart_test", "Restart Test"),
        Binding("ctrl+b", "go_home", "Go Home"),
    ]

    def __init__(
        self,
        wpm: int,
        correct_words: int,
        test_type: str,
        time: int,
        accuracy: int,
        errors: int,
        total_words: int = 0,
        is_personal_best: bool = False,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.wpm = wpm
        self.correct_words = correct_words
        self.test_type = test_type
        self.time = time
        self.accuracy = accuracy
        self.errors = errors
        self.total_words = total_words
        self.is_personal_best = (
            is_personal_best  # add later to show a badge if this is a personal best
        )

    def compose(self) -> ComposeResult:
        yield BrandHeader()
        with Container(id="results-card"):
            yield Static("[#F5C462]── test complete ──", classes="divider")

            with Horizontal(id="hero-container"):
                with Container(classes="hero-stat"):
                    yield Static("wpm", classes="hero-label")
                    yield Static(
                        render_big_number(str(self.wpm), "bold #e2c27d"),
                        classes="hero-value",
                    )

                with Container(classes="hero-stat"):
                    yield Static("accuracy", classes="hero-label")
                    # Reverted to just the number, no percentage sign
                    yield Static(
                        render_big_number(str(self.accuracy), "bold #cccccc"),
                        classes="hero-value",
                    )

                with Container(classes="hero-stat"):
                    yield Static("errors", classes="hero-label")
                    yield Static(
                        render_big_number(str(self.errors), "bold #e26060"),
                        classes="hero-value",
                    )

            yield Rule(line_style="solid")
            with Horizontal(id="details-row"):
                yield Static(
                    f"mode • [#F5C462]{self.test_type}[/]", classes="detail-stat"
                )
                yield Static(f"time • [#F5C462]{self.time}s[/]", classes="detail-stat")

                words_text = (
                    f"words • [#F5C462]{self.correct_words}/{self.total_words}[/]"
                    if self.total_words
                    else f"words • [#F5C462]{self.correct_words}[/]"
                )
                yield Static(words_text, classes="detail-stat")
            if self.is_personal_best:
                yield Static("[#4caf6a]▲ new personal best[/]", id="best-badge")

        yield Footer(elements=FOOTER_ITEMS)

    def action_restart_test(self) -> None:
        from .game import GameScreen

        self.app.switch_screen(GameScreen())

    def action_go_home(self) -> None:
        from .home import HomeScreen

        self.app.switch_screen(HomeScreen())
