from .state import LANGUAGE_CODES, languages_dir
import os, json, random, math
from pathlib import Path


def load_content(language: str) -> list[str]:
    """
    Load content from a JSON file based on the specified language.
    Args:
        language (str): The language for which to load content.
    """

    language_file = os.path.join(
        languages_dir, f"{LANGUAGE_CODES.get(language, language)}.json"
    )
    if not os.path.exists(language_file):
        raise FileNotFoundError(f"Language file '{language_file}' not found.")

    with open(language_file, "r", encoding="utf-8") as f:
        content = json.load(f)

    return content


def generate_words(
    mode: str,
    language: str,
    time: int = 0,
    word_len: int = 0,
    quote_size: int = "short",
) -> list[str]:
    """
    Generate a list of words based on the specified game mode, time, and language.
    Args:
        mode (str): The mode of the game (e.g., "time", "words", "quote").
        language (str): The language for which to generate words.
        time (int): The time limit for the game.
        word_len (int): The length of each word to generate.
        quote_size (str): The size of the quote to generate (e.g., "short", "medium", "long").
    Returns:
        list[str]: A list of randomly generated words.
    """
    content = load_content(language)
    if mode == "time":
        """
        Generating words based on the specified time limit and language.

        """
        CEILING_WPM = 360  # humanly impossible typing speed, but we can use it as a threshold for generating words
        THRESHOLD = 1.2  # just a threshold to make sure we don't generate too many words or too little words for the given time limit
        ceiling_wps = CEILING_WPM / 60
        gen_words_len = math.ceil(ceiling_wps * time * THRESHOLD)

        words = content["words"]
        start_index = random.randint(0, len(words) - gen_words_len)
        return random.sample(
            words[start_index:], min(gen_words_len, len(words) - start_index)
        )

    elif mode == "words":
        """
        Generating a specified number of words based on the given language.
        """
        words = content["words"]
        return random.sample(words, min(word_len, len(words)))

    elif mode == "quote":
        """
        Generating a quote based on the specified size and language.
        short -> 0 - 150
        medium -> 150 - 300
        long -> > 300
        """
        quotes = content["quotes"]
        if quote_size == "short":
            filtered_quotes = [
                quote["text"] for quote in quotes if quote["length"] <= 150
            ]
        elif quote_size == "medium":
            filtered_quotes = [
                quote["text"] for quote in quotes if 150 < quote["length"] <= 300
            ]
        elif quote_size == "long":
            filtered_quotes = [
                quote["text"] for quote in quotes if quote["length"] > 300
            ]
        else:
            raise ValueError(
                "Invalid quote size. Choose from 'short', 'medium', or 'long'."
            )

        return random.choice(filtered_quotes).split() if filtered_quotes else []
