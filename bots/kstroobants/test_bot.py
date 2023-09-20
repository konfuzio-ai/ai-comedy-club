import pytest
from joke_bot import Bot

def test_bot_name():
    ''' Check the bot's name
    '''
    bot = Bot()
    assert bot.name == 'kstroobants'

def test_tell_joke(monkeypatch):
    ''' Check joke specific requirements
    '''
    bot = Bot()
    monkeypatch.setattr('builtins.input', lambda _: "text")
    joke = bot.tell_joke()
    assert isinstance(joke, str)
    assert len(joke) > 1

def test_rate_joke():
    ''' Check rating specific requirements
    '''
    bot = Bot()
    short_joke = "Whats wrong with nature? It has too many bugs."
    assert isinstance(bot.rate_joke(short_joke), int) == True