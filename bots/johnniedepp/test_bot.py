import pytest
from joke_bot import Bot

@pytest.fixture
def bot():
    return Bot()

def test_bot_name(bot):
    assert bot.name == 'Not funny'

def test_tell_joke(bot):
    joke = bot.tell_joke()
    assert  joke in bot.jokes
    assert isinstance(joke, str), "Joke is not a string."
    assert len(joke) > 15, "Joke length is not within the correct range."

def test_rate_joke(bot):
    short_joke = "Whats wrong with nature? It has too many bugs."
    medium_joke = "Why don't scientists trust atoms? Because they make up everything!"
    long_joke = "I'm not a fan of computer jokes. Not one bit. I tried to catch some fog earlier. I'm reading a book about anti-gravity. It's impossible to put down."

    assert bot.rate_joke(short_joke) == 5
    assert bot.rate_joke(medium_joke) == 10
    assert bot.rate_joke(long_joke) == 3

    rating = bot.rate_joke(joke)
    assert isinstance(rating, (int, float)), "Rating is not a number."
    assert 0 <= rating <= 10, "Rating is not within the correct range."
