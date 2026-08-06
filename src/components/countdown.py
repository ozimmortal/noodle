from textual.widgets import Static, Digits


class CountDownBlock(Static):
    DEFAULT_CSS = """
    CountDownBlock {
        height: auto;
        align: center middle;
        content-align: center middle;
    }

    Digits {
        width: auto;
        height: auto;
        color: #F5C462;
        text-style: bold;
    }

    Digits.warning {
        color: #E00324;
    }
    """

    def __init__(self, seconds: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.seconds = seconds

    def compose(self):
        yield Digits(str(self.seconds), id="clock")

    def on_mount(self) -> None:
        self.set_interval(1.0, self.update_clock)

    def update_clock(self) -> None:
        if self.seconds <= 0:
            return

        self.seconds -= 1
        clock = self.query_one("#clock", Digits)

        if self.seconds < 10:
            clock.add_class("warning")

        clock.update(str(self.seconds))