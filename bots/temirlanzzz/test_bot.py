import pytest

from joke_bot import Bot

@pytest.fixture
def bot() -> Bot:
    return Bot()

def test_tell_joke(bot):
    joke = bot.tell_joke()
    print ("JOKE: "+joke)
    assert isinstance(joke, str), "Joke is not a string."
    assert len(joke) > 30, "Joke length is not within the correct range."

def test_rate_joke(bot):
    medium_joke = "Why was the computer cold? It left its Windows open."
    rating = bot.rate_joke(medium_joke)
    print ("rating: "+rating)
    assert isinstance(rating, int), "Rating is not a number."
    assert 0 <= rating <= 10, "Incorrect rating range."
