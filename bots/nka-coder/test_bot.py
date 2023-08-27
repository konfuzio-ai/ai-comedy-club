import pytest
from joke_bot import Bot

@pytest.fixture
def bot():
    return Bot()

def test_bot_name():
    bot = Bot()
    assert bot.name == 'nka-coder'

def test_tell_joke():
    bot = Bot()
    joke = bot.tell_joke()
    assert joke in bot.long_memory


def test_rate_joke():
    bot = Bot()
    joke = "I'm not a fan of computer jokes. Not one bit. I tried to catch some fog earlier. Mist. I'm reading a book about anti-gravity. It's impossible to put down."
    assert bot.rate_joke(joke) >= 0 and bot.rate_joke(joke) <= 10

