import pytest
from joke_bot import Bot

def test_bot_name():
    bot = Bot()
    assert bot.name == 'First attempt'

def test_tell_joke():
    bot = Bot()
    joke = bot.tell_joke()
    assert joke in bot.jokes

def test_rate_joke():
    bot = Bot()
    outside_joke = "Why did the programmer go on a diet? He had too many bytes."
    inside_joke = "Why was the computer cold? It left its Windows open."
    
    assert bot.rate_joke(inside_joke) == 10
    assert bot.rate_joke(outside_joke) == 7.5
