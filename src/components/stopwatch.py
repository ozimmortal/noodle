from textual.widgets import Static, Digits
from textual.message import Message
from textual.reactive import reactive
from textual import on


class StopTimer(Message):
    def __init__(self):
        super().__init__()


class StopWatchBlock(Static):

    ended = reactive(False)
    DEFAULT_CSS = """
    StopWatchBlock {
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

    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.seconds = 0

    def compose(self):
        yield Digits(str(self.seconds), id="clock")

    def on_mount(self) -> None:
        self.set_interval(1.0, self.update_clock)

    def update_clock(self) -> None:
        if self.ended:
            return

        self.seconds += 1
        clock = self.query_one("#clock", Digits)

        clock.update(str(self.seconds))

    @on(StopTimer)
    def handle_stop_timer(self, msg: StopTimer):
        ended = True
