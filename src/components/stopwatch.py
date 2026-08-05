from textual.widgets import Static, Digits
from textual.reactive import reactive


class StopWatch(Static):
    DEFAULT_CSS = """

    Digits{
        color: #F5C462;
        text-style: bold;
    }

"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.seconds = 0

    def compose(self):
        yield Digits(str(self.seconds), id="clock")

    def on_mount(self):
        self.set_interval(1.0, self.update_clock)

    def update_clock(self):
        self.seconds += 1
        digits = self.query_one("#clock", Digits)
        digits.update(str(self.seconds))
