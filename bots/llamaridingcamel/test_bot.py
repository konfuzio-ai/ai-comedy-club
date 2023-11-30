import pytest
from joke_bot import Bot


bot = Bot()


def test_bot_name():
    assert bot.name == 'LLama riding Camel'


def test_tell_joke():
    joke = bot.tell_joke()
    assert len(joke) > 0
    assert bot.name in joke


def test_rate_joke():
    # appropriate joke with proper user question. should score high.
    short_joke = "Whats wrong with nature? It has too many bugs."

    # racist joke should have a lower rating
    medium_joke = "What happens if a Asian with an erection walks into a wall? He breaks his nose."

    # long sentences. Does not mean a joke. Should score low.
    long_joke = "I'm not a fan of computer jokes. Not one bit. I tried to catch some fog earlier. Mist. \
    I'm reading a book about anti-gravity. It's impossible to put down."

    assert bot.rate_joke(short_joke) > 7
    assert bot.rate_joke(medium_joke) < 7
    assert bot.rate_joke(long_joke) < 5
