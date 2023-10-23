import pytest
from joke_bot import Bot

def test_tell_joke():
    bot = Bot()
    joke = bot.tell_joke()
    assert joke in bot.jokes

def test_rate_joke():
    bot = Bot()
    for joke in bot.jokes:
        rating = bot.rate_joke(joke)
        assert 1 <= rating <= 10