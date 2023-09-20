import pytest
from joke_bot import Bot


@pytest.fixture
def bot() -> Bot:
    return Bot()


def test_tell_joke(bot: Bot) -> None:
    joke = bot.tell_joke()
    assert isinstance(joke, str), "Joke is not a string."
    criteria1 = joke[-1] == '.'
    criteria2 = 0 < joke.count('.') + joke.count('!') + joke.count('?') >= 2
    assert criteria1 or criteria2, "Joke sentence creation criterias not met."


def test_rate_joke(bot: Bot) -> None:
    joke = "Why was the computer cold at the office? Because it left its Windows open."  # noqa
    rating = bot.rate_joke(joke)
    assert isinstance(rating, (int, float)), "Rating is not a number."
    assert 0 <= rating <= 10, "Rating is not within the correct range."
