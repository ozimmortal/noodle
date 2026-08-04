from textual.widget import Widget
from textual.widgets import Static, Link
from textual.containers import Horizontal, Vertical
from lib import state


class BellyLogo(Static):
    def __init__(self, letter="n-", **kwargs):
        super().__init__(letter, **kwargs)


class TitleBlock(Vertical):
    def compose(self):
        yield Link(
            "noodle...", url="https://github.com/ozimmortal/belly", id="app-title"
        )
        yield Static(f"v{state.APP_VERSION}", id="app-version")


class BrandHeader(Horizontal):
    DEFAULT_CSS = """
    BrandHeader{
        content-align: center middle;
        margin-left: 2;
        height: 6;
    }
    .gold-card {
        width: 5;
        height: 3;
        color: #F5C462;
        border: round #F5C462;
        text-style: bold;
        content-align: center middle;
        margin-top: 1;
    }

    #title-stack {
        height: 4;
        width: 10;
        margin-top: 2;
        margin-left:1;

    }

    #app-title {
        color: #f2f2f2;
        text-style: bold;
    }
    #app-title:hover {
        background: #969696 50%;
    }

    #app-version {
        color: #555555;
    }
"""

    def compose(self):
        yield BellyLogo(classes="gold-card")
        yield TitleBlock(id="title-stack")
