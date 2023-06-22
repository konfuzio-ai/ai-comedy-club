import pytest
from joke_bot import Bot


def test_tell_joke():
    bot = Bot()
    joke = bot.tell_joke()
    assert isinstance(joke, str)


def test_rate_joke():
    bot = Bot()
    joke = "Why don't scientists trust atoms? Because they make up everything!"
    rating = bot.rate_joke(joke)
    assert isinstance(rating, int)
    assert 1 <= rating <= 10
