import pytest
from joke_bot import Bot
from custom_pyjokes import get_categories

def test_bot_name():
    bot = Bot()
    assert bot.name == 'flossCoder jokeBot'

def test_tell_joke():
    bot = Bot()
    joke = bot.tell_joke()
    assert isinstance(joke, str), "Joke is not a string."
    for category in [None] + get_categories():
        joke = bot.tell_joke(category)
        assert isinstance(joke, str), "Joke is not a string."

def test_rate_joke():
    bot = Bot()
    joke = "Why was the computer cold at the office? Because it left its Windows open."
    rating = bot.rate_joke(joke)
    assert isinstance(rating, (int, float)), "Rating is not a number."
    assert 0 <= rating <= 10, "Rating is not within the correct range."
