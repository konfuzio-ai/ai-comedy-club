import pytest
from joke_bot import Bot

@pytest.fixture
def bot():
    return Bot()

def test_tell_joke(bot):
    joke = bot.tell_joke()
    assert isinstance(joke, str), "Joke is not a string."
    assert len(joke) > 50, "Joke length is not within the correct range."

def test_rate_joke(bot):
    joke = "Why was the computer cold at the office? Because it left its Windows open."
    rating = bot.rate_joke(joke)
    assert isinstance(rating, (int, float)), "Rating is not a number."
    assert 0 <= rating <= 10, "Rating is not within the correct range."
