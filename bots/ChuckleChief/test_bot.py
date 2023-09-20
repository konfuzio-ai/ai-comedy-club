import pytest

from joke_bot import Bot


@pytest.fixture
def bot():
    return Bot()


def test_joke_teller(bot):
    joke = bot.tell_joke()
    assert isinstance(joke, str), "The joke is not a string."
    assert len(joke) > 30, "The joke length exceeds the correct range."


def test_joke_rater(bot):
    joke = "Why did the scarecrow win an award? Because he was outstanding in his field."
    rating = bot.rate_joke(joke)
    assert isinstance(rating, int), "The rating is not an integer."
    assert 1 <= rating <= 10, "The rating exceeds the correct range."
