from textual.screen import Screen
from textual.containers import Container
from components.footer import Footer
from components.logo import BrandHeader
from components.countdown import CountDownBlock
from components.type_area import TypeArea, Word, CharacterStatus, GameEndReached
from lib.state import settings
from textual.binding import Binding
from textual import on
from .end_game import EndGameScreen
from textual.message import Message
from lib.generate_words import generate_words
from components.stopwatch import StopWatchBlock, StopTimer

FOOTER_ELEMENTS = [
    ["ctrl+b", "back"],
    ["ctrl+q", "quit"],
]


class GameScreen(Screen):
    DEFAULT_CSS = """
    #body {
        width: 100%;
        height: 1fr;
        align: center middle;
    }

    CountDownBlock{
        width: 80%;
    }
    StopWatchBlock{
        width: 80%;
    }
    TypeArea {
        width: 80%;
        height: auto;
    }
    
"""

    class GameEndResult(Message):
        def __init__(
            self, wpm: int, correct_words: int, test_type: str, time: int, accuracy: int
        ):
            super().__init__()
            self.wpm = wpm
            self.correct_words = correct_words
            self.test_type = test_type
            self.time = time
            self.accuracy = accuracy

    BINDINGS = [Binding("ctrl+b", "go_back", "Go Back Home")]

    def __init__(self, name=None, id=None, classes=None):
        super().__init__(name, id, classes)
        self.mode = settings.get("mode")
        self.choice = settings.get("choice")
        self.language = settings.get("language")
        generated_words = generate_words(
            mode=self.mode,
            language=self.language,
            time=self.choice if self.mode == "time" else 0,
            word_len=self.choice if self.mode == "words" else 0,
            quote_size=self.choice if self.mode == "quote" else "short",
        )
        self.words = [Word(w) for w in generated_words]
        self.type_area = TypeArea(self.words)
        self.timer = (
            CountDownBlock(self.choice) if self.mode == "time" else StopWatchBlock()
        )

    def compose(self):
        yield BrandHeader()
        with Container(id="body"):
            yield self.timer
            yield self.type_area
        yield Footer(elements=FOOTER_ELEMENTS)

    def action_go_back(self) -> None:
        self.app.pop_screen()

    @on(CountDownBlock.Countdown_Ended)
    def handle_countdown_ended(self, msg: CountDownBlock.Countdown_Ended) -> None:
        self.query_one(CountDownBlock).remove()
        results = self.calculate_results()
        self.app.push_screen(
            EndGameScreen(
                wpm=results["wpm"],
                correct_words=results["count_correct_words"],
                test_type=results["test_type"],
                time=results["time"],
                accuracy=results["accuracy"],
                errors=results["errors"],
                total_words=results["total_words"],
            )
        )

    @on(GameEndReached)
    def handle_game_end_reached(self, msg: GameEndReached) -> None:
        self.query_one(StopWatchBlock).post_message(StopTimer())
        results = self.calculate_results()
        self.app.push_screen(
            EndGameScreen(
                wpm=results["wpm"],
                correct_words=results["count_correct_words"],
                test_type=results["test_type"],
                time=results["time"],
                accuracy=results["accuracy"],
                errors=results["errors"],
                total_words=results["total_words"],
            )
        )

    def calculate_results(self) -> dict:
        """
        Calculates the results of the typing test.
        Returns:
            dict: A dictionary containing the results of the typing test.
                contains the following keys:
                - wpm (int): Words per minute.
                - test_type (str): The type of test (time, words, or quote).
                - time (int): The time taken for the test in seconds.
                - accuracy (float): The accuracy percentage of the typing test.
                - count_correct_characters (int): Number of correctly typed characters.
                - total_characters (int): Total number of characters in the test.
                - count_correct_words (int): Number of correctly typed words.
                - total_words (int): Total number of words in the test.
                - mode (str): The mode of the test (time, words, or quote).
        """
        count_correct_words = sum(1 for word in self.words if word.is_correct)
        count_typed_characters = sum(
            sum(
                1
                for char in word.characters
                if char.status != CharacterStatus.UNENTERED
            )
            for word in self.words
        )
        count_correct_characters = sum(
            sum(1 for char in word.characters if char.status == CharacterStatus.CORRECT)
            for word in self.words
        )
        total_characters = sum(word.length for word in self.words)
        total_words = len(self.words)
        accuracy = (
            int(count_correct_characters / count_typed_characters * 100)
            if count_typed_characters > 0
            else 0
        )
        time = (
            self.timer.seconds
            if isinstance(self.timer, StopWatchBlock)
            else self.choice
        )
        time_in_minutes = time / 60

        wpm = int(count_correct_words / time_in_minutes) if time_in_minutes > 0 else 0
        return {
            "wpm": wpm,
            "test_type": self.mode,
            "time": time,
            "accuracy": accuracy,
            "count_correct_characters": count_correct_characters,
            "total_characters": total_characters,
            "count_correct_words": count_correct_words,
            "total_words": total_words,
            "mode": self.mode,
            "errors": count_typed_characters - count_correct_characters,
        }
