import pytest

from joke_bot import Bot

@pytest.fixture
def bot():
    return Bot()

def test_joker(bot):
    joke = bot.tell_joke()
    
    assert isinstance(joke, str), "Joke is not a string"

def test_rater(bot):
    joke = "Why do they call it rush hour when nothing moves?"
    rating = bot.rate_joke(joke)
    
    assert isinstance(rating, int), "Rating is not an integer"
    assert 1 <= rating <= 10, "Rating is not witih the 1-10 range"