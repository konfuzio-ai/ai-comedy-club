import pytest
from joke_bot import Bot


def test_bot_name():
    bot = Bot()
    assert bot.name == 'Ammar'


def test_tell_joke():
    bot = Bot()
    joke = bot.tell_joke("programming")
    assert joke is not None
    assert len(joke) > 0
    assert isinstance(joke, str), "Joke is not a string."
    assert len(joke) > 50, "Joke length is not within the correct range."


def test_rate_joke():
    bot = Bot()
    # Test case for the rate_joke method
    joke = "Why don't programmers like nature? It has too many bugs.",
    # Generate a joke and simulate a user rating
    rating = bot.rate_joke('Programming', 'Not funny', joke)
    # Assert that the result is a valid rating value
    assert isinstance(rating, (int, float)), "Rating is not a number."
    assert 1 <= rating <= 10
