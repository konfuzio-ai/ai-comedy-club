import pytest
from joke_bot import Bot

@pytest.fixture
def bot():
    return Bot()

def test_tell_joke(bot):
    joke = bot.tell_joke()
    assert isinstance(joke, str), "Joke is not a string."


def test_rate_joke(bot):
    joke = "Why did the programmer go on a diet? He had too many bytes."
    rating = bot.rate_joke(joke)
    assert isinstance(rating, (int, float)), "Rating is not a number."
    assert 0 <= rating <= 10, "Rating is not within the correct range."

def test_small_talk(bot):
    assert bot.small_talk("Hi") == "Hello! How can I help you today?"

