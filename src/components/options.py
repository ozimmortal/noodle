from textual.widgets import Static, Select, Label
from textual.containers import Horizontal, Vertical, Container
from textual.reactive import reactive
from textual import events, on
from textual.widget import Widget
from textual.message import Message
from lib.state import settings_path, settings
import os, json


def update_game_setting(key: str, value: str, choice=""):
    settings[key] = value
    if key == "mode":
        settings["choice"] = choice


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

    can_focus = False

    def __init__(self, languages: list[str] | None = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.languages = languages or []

    def compose(self):
        yield Static("language", classes="header")
        yield Select(
            options=[(lang.capitalize(), lang) for lang in self.languages],
            allow_blank=False,
            compact=True,
        )

    @on(events.DescendantFocus)
    def on_focus_in(self, event: events.DescendantFocus) -> None:
        self.query_one(".header", Static).add_class("selected")
        self.add_class("selected")

    @on(events.DescendantBlur)
    def on_focus_out(self, event: events.DescendantBlur) -> None:
        self.query_one(".header", Static).remove_class("selected")
        self.remove_class("selected")

    def on_click(self, event: events.Click) -> None:
        self.query_one(Select).focus()

    @on(Select.Changed)
    def select_changed(self, event: Select.Changed) -> None:
        key, value = "language", event.value
        update_game_setting(key, value)


class ModeSelect(Container):
    DEFAULT_CSS = """
    ModeSelect {
        layout: vertical;
        content-align: center middle;
        height: auto;
        width: 20;
    }

    ModeSelect .header {
        color: $text-muted;
        content-align: center middle;
        width: 100%;
        height: auto;
        margin-bottom: 1;
    }

    ModeSelect .header.selected {
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

    ModeSelect.selected Select > SelectCurrent {
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

    class ModeChanged(Message):
        def __init__(self, mode: str):
            super().__init__()
            self.mode = mode

    can_focus = False

    def __init__(self, modes: dict, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.modes = modes

    def compose(self):
        options = self.modes.keys()
        yield Static("mode", classes="header")
        yield Select(
            options=[(mode.capitalize(), mode) for mode in options],
            allow_blank=False,
            compact=True,
        )

    @on(events.DescendantFocus)
    def on_focus_in(self, event: events.DescendantFocus) -> None:
        self.query_one(".header", Static).add_class("selected")
        self.add_class("selected")

    @on(events.DescendantBlur)
    def on_focus_out(self, event: events.DescendantBlur) -> None:
        self.query_one(".header", Static).remove_class("selected")
        self.remove_class("selected")

    def on_click(self, event: events.Click) -> None:
        self.query_one(Select).focus()

    @on(Select.Changed)
    def select_changed(self, event: Select.Changed) -> None:
        key, mode = "mode", event.value
        update_game_setting(key, mode, self.modes[mode][0])
        self.post_message(self.ModeChanged(mode))


class Option(Label):
    class OptionClicked(Message):
        def __init__(self, optionid: int) -> None:
            super().__init__()
            self.optionid = optionid

    def __init__(self, optionid: int, option: str, cls: str, *args, **kwargs):
        super().__init__(str(option), classes=cls, *args, **kwargs)
        self.optionid = optionid
        self.option = option

    def on_click(self, event):
        self.post_message(self.OptionClicked(optionid=self.optionid))


class OptionList(Container):
    DEFAULT_CSS = """
    OptionList {
        layout: vertical;
        content-align: center middle;
        height: auto; 
        width: 30;
        margin-right: 3;
        background: transparent;
        border: none;
    }
    OptionList:focus{
        border: none;
    }
    .header {
        color: $text-muted;
        content-align: center middle;
        width: 100%;
        height: auto;
        margin-bottom: 1;
    }
    .header.selected {
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
        width: auto;
    }
    
    .option:hover {
        color: $text; 
    }
    
    .option.selected {
        color: #F5C462;
        text-style: underline;
    }
    """

    class OptionChanged(Message):
        def __init__(self, optionid: int):
            super().__init__()
            self.optionid = optionid

    can_focus = True
    tab_selected = reactive(False)
    option_selected = reactive(0)
    current_mode_index = reactive(0)

    def __init__(self, modes: dict, mode_coll: list, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.modes = modes
        self.mode_coll = mode_coll

    @property
    def current_header(self) -> str:
        return self.mode_coll[self.current_mode_index]

    @property
    def current_options(self) -> list:
        return self.modes.get(self.current_header, [])

    def compose(self):
        yield Static(
            self.current_header,
            classes="header selected" if self.tab_selected else "header",
        )
        with Horizontal(id="option-cont"):
            for i, option in enumerate(self.current_options):
                classes = (
                    "option selected"
                    if self.tab_selected and i == self.option_selected
                    else "option"
                )
                yield Option(optionid=i, option=str(option), cls=classes)

    def on_focus(self, event: events.Focus) -> None:
        self.tab_selected = True

    def on_blur(self, event: events.Blur) -> None:
        self.tab_selected = False

    def on_key(self, event: events.Key) -> None:
        if event.key == "left":
            event.stop()
            if self.option_selected > 0:
                self.option_selected -= 1
                self.post_message(self.OptionChanged(self.option_selected))
        elif event.key == "right":
            event.stop()
            if self.option_selected < len(self.current_options) - 1:
                self.option_selected += 1
                self.post_message(self.OptionChanged(self.option_selected))

    @on(Option.OptionClicked)
    def handle_option_click(self, msg: Option.OptionClicked) -> None:
        self.focus()  # Pull focus if clicked
        self.option_selected = msg.optionid
        self.post_message(self.OptionChanged(msg.optionid))

    def watch_tab_selected(self, tab_selected: bool) -> None:
        if not self.is_mounted:
            return
        header = self.query_one(".header", Static)
        header.set_class(tab_selected, "selected")
        self._refresh_option_classes()

    def watch_option_selected(self) -> None:
        if not self.is_mounted:
            return
        self._refresh_option_classes()

    async def watch_current_mode_index(self) -> None:
        if not self.is_mounted:
            return

        header = self.query_one(".header", Static)
        header.update(self.current_header)

        container = self.query_one("#option-cont", Horizontal)
        await container.remove_children()

        new_options = []
        for i, option in enumerate(self.current_options):
            classes = (
                "option selected"
                if self.tab_selected and i == self.option_selected
                else "option"
            )
            new_options.append(Option(optionid=i, option=option, cls=classes))

        await container.mount(*new_options)

    def _refresh_option_classes(self) -> None:
        options = self.query(Option)
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

    can_focus = False
    current_mode = reactive(0)

    def __init__(self, modes: dict, languages: list, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.modes = modes
        self.languages = languages
        self.mode_coll = []

        if self.modes:
            self.mode_coll = list(self.modes.keys())

    def _on_mount(self, event) -> None:
        self.query_one(ModeSelect).query_one(Select).focus()

    def compose(self):
        with Horizontal():
            yield ModeSelect(modes=self.modes)
            yield OptionList(modes=self.modes, mode_coll=self.mode_coll)
            yield LanguageSelect(languages=self.languages)

    @on(OptionList.OptionChanged)
    def handle_option_changed(self, msg: OptionList.OptionChanged) -> None:
        self.update_option_settings(msg.optionid)

    @on(ModeSelect.ModeChanged)
    def handle_mode_changed(self, msg: ModeSelect.ModeChanged) -> None:
        for i, mode in enumerate(self.mode_coll):
            if mode == msg.mode:
                self.current_mode = i
                option_list = self.query_one(OptionList)
                option_list.current_mode_index = i
                option_list.option_selected = 0
                self.update_option_settings(0)

    def update_option_settings(self, optionid: int) -> None:
        mode = self.mode_coll[self.current_mode]
        option_list = self.query_one(OptionList)
        choices = option_list.current_options
        if 0 <= optionid < len(choices):
            choice = choices[optionid]
            update_game_setting("mode", mode, choice)
