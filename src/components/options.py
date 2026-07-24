from textual.widgets import Static, Select, Label
from textual.containers import Horizontal, Vertical, Container
from textual.reactive import reactive
from textual import events, on
from textual.widget import Widget
from textual.message import Message


class LanguageSelect(Container):
    DEFAULT_CSS = """
    LanguageSelect {
        layout: vertical;
        content-align: center middle;
        height: auto;
        width: 20;
    }

    LanguageSelect .header {
        color: $text-muted;
        content-align: center middle;
        width: 100%;
        height: auto;
        margin-bottom: 1;
    }

    LanguageSelect .header.selected {
        color: #F5C462;
    }

    Select {
        width: 16;
        height: 1;
        background: transparent;
        border: none;
    }

    Select > SelectCurrent {
        background: transparent;
        border: none;
        padding: 0 1;
        color: $text-muted;
    }

    LanguageSelect.selected Select > SelectCurrent {
        color: #F5C462;
        text-style: bold;
    }

    Select > SelectCurrent .arrow {
        color: #6b5d3a;
    }

    SelectOverlay {
        background: #0f0f0f;
        border: none;
        scrollbar-size: 0 0;
    }

    SelectOverlay > .option-list--option {
        color: #666666;
        background: transparent;
    }

    SelectOverlay > .option-list--option-highlighted {
        color: #e2c27d;
        background: transparent;
        text-style: bold;
    }
    

    """

    class TabClicked(Message):
        def __init__(self, tab_id: int) -> None:
            super().__init__()
            self.tab_id = tab_id

    can_focus = True
    tab_selected = reactive(False)

    def __init__(
        self, tab_id: int, languages: list[str] | None = None, *args, **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.tab_id = tab_id
        self.languages = languages or []

    def compose(self):
        yield Static("language", classes="header")
        yield Select(
            options=[(lang.capitalize(), lang) for lang in self.languages],
            allow_blank=False,
            compact=True,
        )

    def on_click(self, event: events.Click) -> None:
        self.post_message(self.TabClicked(self.tab_id))

    def watch_tab_selected(self, tab_selected: bool) -> None:
        if not self.is_mounted:
            return
        header = self.query_one(".header", Static)
        header.set_class(tab_selected, "selected")
        self.set_class(tab_selected, "selected")
        self.query(Select)[0].focus()

    @on(Select.Changed)
    def select_changed(self, event: Select.Changed) -> None:
        value = event.value
        pass


class Option(Label):

    class OptionClicked(Message):
        def __init__(self, tabid: int, optionid: int) -> None:
            super().__init__()
            self.tabid = tabid
            self.optionid = optionid

    def __init__(
        self, current_tab: int, optionid: int, option: str, cls: str, *args, **kwargs
    ):
        super().__init__(option, classes=cls, *args, **kwargs)
        self.optionid = optionid
        self.option = option
        self.current_tab = current_tab

    def _on_click(self, event):
        self.post_message(
            self.OptionClicked(tabid=self.current_tab, optionid=self.optionid)
        )


class OptionGroup(Container):
    DEFAULT_CSS = """
    OptionGroup {
        layout: vertical;
        content-align: center middle;
        height: auto; 
        width: 30;
        margin-right: 2;
    }
    
    .header {
        color: $text-muted;
        content-align: center middle;
        width: 100%;
        height: auto;
        margin-bottom: 1;
    }
    .header.selected{
        color: #F5C462;
    }
    #option-cont {
        width: 100%;
        height: auto;
        align: center middle;
    }
    
    .option {
        color: $text-muted;
        margin: 0 2; 
        content-align: center middle;
        width:auto;
    }
    
    .option:hover {
        color: $text; 
    }
    
    .option.selected {
        color: #F5C462;
        text-style: underline;
    }
    """

    can_focus = True
    tab_selected = reactive(False)
    option_selected = reactive(0)

    def __init__(
        self,
        tabid: int,
        header: str,
        options: list[str] | None = None,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.header = header
        self.options = options or []
        self.tabid = tabid

    def compose(self):
        yield Static(
            self.header, classes="header selected" if self.tab_selected else "header"
        )
        with Horizontal(id="option-cont"):
            for i, option in enumerate(self.options):
                classes = (
                    "option selected"
                    if self.tab_selected and i == self.option_selected
                    else "option"
                )
                yield Option(
                    current_tab=self.tabid, optionid=i, option=option, cls=classes
                )

    def watch_tab_selected(self, tab_selected: bool) -> None:
        if not self.is_mounted:
            return
        header = self.query_one(".header", Static)
        header.set_class(tab_selected, "selected")
        self._refresh_option_classes()

        if tab_selected:
            self.focus()

    def watch_option_selected(self, option_selected: int) -> None:
        if not self.is_mounted:
            return
        self._refresh_option_classes()

    def _refresh_option_classes(self) -> None:
        options = self.query(".option")
        for i, opt in enumerate(options):
            opt.set_class(i == self.option_selected, "selected")


class OptionsTab(Widget):
    DEFAULT_CSS = """
    OptionsTab {
        height: 50%; 
        content-align: center middle;
    }
    OptionsTab > Horizontal {
        align: center middle;  
        width: 100%;         
        height: 100%;
    }
    """

    can_focus = True
    current_tab = reactive(0)

    def __init__(self, collections: list[dict] | None = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.collections = collections or []
        self.languages = [
            "english",
            "french",
            "spanish",
        ]  # later on move the available languages in settings.json

    def _on_mount(self, event) -> None:
        self.focus()
        if self.collections:
            self.select_tab(self.query(OptionGroup), 0, 0)

    def compose(self):
        with Horizontal():
            for key, collection in enumerate(self.collections):
                header, options = collection["header"], collection["options"]
                yield OptionGroup(header=header, options=options, tabid=key)

            yield LanguageSelect(languages=self.languages, tab_id=len(self.collections))

    def _on_key(self, event: events.Key) -> None:
        groups = list(self.query(OptionGroup)) + list(self.query(LanguageSelect))
        if not groups:
            return

        active_group = groups[self.current_tab]

        if event.key == "tab":
            event.stop()
            old = self.current_tab
            new = (old + 1) % len(groups)
            self.select_tab(groups, new, old)

        elif event.key == "left":
            if (
                isinstance(active_group, OptionGroup)
                and active_group.option_selected > 0
            ):
                active_group.option_selected -= 1

        elif event.key == "right":
            if (
                isinstance(active_group, OptionGroup)
                and active_group.option_selected < len(active_group.options) - 1
            ):
                active_group.option_selected += 1

    @on(LanguageSelect.TabClicked)
    def handle_language_tab_click(self, msg: LanguageSelect.TabClicked) -> None:
        groups = list(self.query(OptionGroup)) + list(self.query(LanguageSelect))
        old = self.current_tab
        new = msg.tab_id

        if old != new:
            groups[old].tab_selected = False

        groups[new].tab_selected = True
        self.current_tab = new

    @on(Option.OptionClicked)
    def handle_option_click(self, msg: Option.OptionClicked) -> None:
        groups = list(self.query(OptionGroup)) + list(self.query(LanguageSelect))
        old = self.current_tab
        new = msg.tabid

        if old != new:
            groups[old].tab_selected = False

        groups[new].tab_selected = True
        groups[new].option_selected = msg.optionid
        self.current_tab = new

        if isinstance(groups[new], OptionGroup):
            groups[new]._refresh_option_classes()

    def select_tab(self, groups, new: int, old: int) -> None:
        groups[old].tab_selected = False
        groups[new].tab_selected = True
        self.current_tab = new
