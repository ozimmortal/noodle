from enum import Enum
from typing import List
from rich.text import Text
from textual import events
from textual.events import Resize
from textual.widget import Widget
from textual.reactive import reactive
from textual.message import Message


class GameEndReached(Message):
    def __init__(self):
        super().__init__()


class CharacterStatus(Enum):
    CORRECT = "correct"
    INCORRECT = "incorrect"
    UNENTERED = "unentered"


class Character:
    def __init__(self, value: str):
        if len(value) != 1:
            raise ValueError("Character value must be a single character.")
        self.value: str = value
        self.status: CharacterStatus = CharacterStatus.UNENTERED


class Word:
    def __init__(self, text: str):
        self.text: str = text
        self.characters: List[Character] = [Character(ch) for ch in text]

    @property
    def length(self) -> int:
        return len(self.text)

    @property
    def is_correct(self) -> bool:
        return all(ch.status == CharacterStatus.CORRECT for ch in self.characters)


class TypeArea(Widget, can_focus=True):
    DEFAULT_CSS = """
    TypeArea {
        height: auto;
        padding: 1 2;
    }
    TextArea:focus{
        border: none;
    }
    """

    STATUS_STYLES = {
        CharacterStatus.CORRECT: "bold white",
        CharacterStatus.INCORRECT: "bold red ",
        CharacterStatus.UNENTERED: "dim white",
    }

    curr_word_idx = reactive(0)
    curr_char_idx = reactive(0)

    def __init__(self, words: List[Word], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.words: List[Word] = words
        self.lines: List[List[Word]] = []

    def on_mount(self) -> None:
        self.focus()
        self.lines = self.words_to_lines()
        self.refresh()

    def on_resize(self, event: Resize) -> None:
        self.lines = self.words_to_lines()
        self.refresh()

    def on_key(self, event: events.Key) -> None:
        if self.curr_word_idx >= len(self.words):
            return

        current_word = self.words[self.curr_word_idx]

        if event.key == "backspace":
            if self.curr_char_idx > 0:
                self.curr_char_idx -= 1
                current_word.characters[self.curr_char_idx].status = CharacterStatus.UNENTERED
            elif self.curr_word_idx > 0:
                self.curr_word_idx -= 1
                prev_word = self.words[self.curr_word_idx]
                self.curr_char_idx = prev_word.length

        elif event.key == "space":
            if self.curr_char_idx == current_word.length:
                self.curr_word_idx += 1
                self.curr_char_idx = 0

        elif event.character and len(event.character) == 1:
            if self.curr_char_idx < current_word.length:
                char_obj = current_word.characters[self.curr_char_idx]

                if event.character == char_obj.value:
                    char_obj.status = CharacterStatus.CORRECT
                else:
                    char_obj.status = CharacterStatus.INCORRECT

                self.curr_char_idx += 1

                is_last_word = self.curr_word_idx == len(self.words) - 1
                is_last_char = self.curr_char_idx == current_word.length

                if is_last_word and is_last_char:
                    self.post_message(GameEndReached())
                    self.curr_word_idx += 1

    def words_to_lines(self) -> List[List[Word]]:
        width = self.content_size.width or self.container_size.width

        if width <= 0 or not self.words:
            return [self.words] if self.words else []

        lines: List[List[Word]] = []
        curr_line: List[Word] = []
        curr_size = 0

        for word in self.words:
            space_needed = (word.length + 1) if curr_line else word.length

            if curr_size + space_needed <= width:
                curr_line.append(word)
                curr_size += space_needed
            else:
                if curr_line:
                    lines.append(curr_line)
                curr_line = [word]
                curr_size = word.length

        if curr_line:
            lines.append(curr_line)

        return lines

    def get_curr_line_idx(self) -> int:
        word_count = 0
        for idx, line in enumerate(self.lines):
            line_word_count = len(line)
            if word_count <= self.curr_word_idx < word_count + line_word_count:
                return idx
            word_count += line_word_count

        return max(0, len(self.lines) - 1)

    def render(self) -> Text:
        result = Text()

        curr_line_idx = self.get_curr_line_idx()
        if curr_line_idx == 0:
            start_line_idx = 0
        else:
            start_line_idx = (
                curr_line_idx - 1
                if len(self.lines) - curr_line_idx >= 3
                else curr_line_idx - 1
            )

        end_line_idx = start_line_idx + 3
        word_counter = sum(len(line) for line in self.lines[:start_line_idx])
        active_lines = self.lines[start_line_idx:end_line_idx]

        for line_idx, line in enumerate(active_lines):
            for word_idx, word in enumerate(line):
                is_current_word = word_counter == self.curr_word_idx

                if word_idx > 0:
                    prev_is_current = (word_counter - 1) == self.curr_word_idx
                    if prev_is_current and self.curr_char_idx == self.words[word_counter - 1].length:
                        result.append(" ", style="reverse blink")
                    else:
                        result.append(" ")

                for char_idx, ch in enumerate(word.characters):
                    style = self.STATUS_STYLES.get(ch.status, "dim white")

                    if is_current_word and char_idx == self.curr_char_idx:
                        style += " reverse blink"

                    result.append(ch.value, style=style)

                if is_current_word and self.curr_char_idx == word.length:
                    if word_idx == len(line) - 1 or word_counter == len(self.words) - 1:
                        result.append(" ", style="reverse blink")

                word_counter += 1

            if line_idx < len(self.lines) - 1:
                result.append("\n")

        return result