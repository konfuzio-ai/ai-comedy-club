import pytest
from joke_bot import Bot

def test_tell_joke():
    bot = Bot()
    joke = bot.tell_joke()
    assert joke is not None, "Joke is None"
    assert isinstance(joke, str), "Joke is not a string"
    assert len(joke) > 0, "Joke is empty"

def test_rate_joke():
    bot = Bot()
    joke = bot.tell_joke()
    rating = bot.rate_joke(joke)
    assert rating is not None, "Rating is None"
    assert isinstance(rating, int), "Rating is not an integer"
    assert rating >= 5 and rating <= 10, "Rating is not within the expected range (5-10)"

def test_rate_joke_invalid_input():
    bot = Bot()
    rating = bot.rate_joke(123)
    assert rating is None, "Rating is not None for invalid joke input"

if __name__ == "__main__":
    pytest.main()
