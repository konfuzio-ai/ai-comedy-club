import pytest
from joke_bot import Bot


@pytest.fixture
def bot():
    return Bot()


def test_tell_joke_about_harry_potter(bot):
    joke_topic = "harry potter"
    joke = bot.tell_joke(joke_topic)

    assert isinstance(joke, str), "Joke is not a string."
    assert len(joke) > 50, "Joke length is not within the correct range."


def test_tell_joke_about_cillian_murphy(bot):
    joke_topic = "cillian_murphy"
    joke = bot.tell_joke(joke_topic)

    assert isinstance(joke, str), "Joke is not a string."
    assert len(joke) > 50, "Joke length is not within the correct range."


def test_tell_joke_about_giraffe(bot):
    joke_topic = "giraffe"
    joke = bot.tell_joke(joke_topic)

    assert isinstance(joke, str), "Joke is not a string."
    assert len(joke) > 50, "Joke length is not within the correct range."


def test_rate_joke_1(bot):
    joke = "Why was the computer cold at the office? Because it left its Windows open."
    rating = bot.rate_joke(joke)
    assert isinstance(rating, (int, float)), "Rating is not a number."
    assert 0 <= rating <= 10, "Rating is not within the correct range."


def test_rate_joke_2(bot):
    joke = "What would bears be without bees? Ears."
    rating = bot.rate_joke(joke)
    assert isinstance(rating, (int, float)), "Rating is not a number."
    assert 0 <= rating <= 10, "Rating is not within the correct range."
