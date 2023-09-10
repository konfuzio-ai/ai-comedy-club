import pytest
from joke_bot import Bot

@pytest.fixture
def bot():
    return Bot()

def test_tell_joke(bot):
    joke = bot.tell_joke()
    assert isinstance(joke, str), "Joke is not a string."

def test_rate_joke(bot):
    joke = "What do you call fake spaghetti? An impasta!"
    rating = bot.rate_joke(joke)
    assert isinstance(rating, int), "Rating is not a number." 
