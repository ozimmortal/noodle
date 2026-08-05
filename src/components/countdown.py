from textual.widgets import Static, Digits
from textual.reactive import reactive


class CountDownBlock(Static):
    DEFAULT_CSS = """

    Digits{
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

    def on_mount(self):
        self.set_interval(1.0, self.update_clock)

    def update_clock(self):
        if self.seconds == 0:
            return

        self.seconds -= 1
        digits = self.query_one("#clock", Digits)
        if self.seconds < 10:
            digits.add_class("warning")

        digits.update(str(self.seconds))
