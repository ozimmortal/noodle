from textual.widgets import Static
from textual.containers import Horizontal


class Footer(Static):

    DEFAULT_CSS = """
    Footer{
        width: 100%;
        height: auto;
        align: center middle;
        content-align: center middle;
        border-top: solid #1a1a1a;
        padding-top: 1;
        margin-top: 1;
        dock: bottom;
        padding-bottom: 3;
    }

    #footer-row {
        width: auto;
        height: auto;
        align: center middle;
        
    }

    .footer-item {
        width: auto;
        height: auto;
        color: #2a2a2a;
        margin: 0 3;
        text-style: none;
    }

"""

    def __init__(self, elements=[], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.elements = elements

    def compose(self):
        with Horizontal(id="footer-row"):
            for key, description in self.elements:
                yield Static(
                    f"[#5B5A5A]{key}[/] · [#404040]{description}[/]",
                    classes="footer-item",
                )
