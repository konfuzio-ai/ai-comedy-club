import pytest
from joke_bot import Bot

def test_bot_name():
    bot = Bot()
    assert bot.name == 'Not funny'

def test_tell_joke():
    bot = Bot()
    joke = bot.tell_joke()
    assert joke in bot.jokes

def test_rate_joke():
    bot = Bot()
    short_joke = "Whats wrong with nature? It has too many bugs."
    medium_joke = "Why was the computer cold? It left its Windows open."
    long_joke = "I'm not a fan of computer jokes. Not one bit. I tried to catch some fog earlier. Mist. I'm reading a book about anti-gravity. It's impossible to put down."

    assert bot.rate_joke(short_joke) == 10
    assert bot.rate_joke(medium_joke) == 7
    assert bot.rate_joke(long_joke) == 5
