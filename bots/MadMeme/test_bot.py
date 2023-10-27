"""MadMeme tests"""

import pytest

from bots.MadMeme.joke_bot import Bot


@pytest.fixture
def bot() -> Bot:
    return Bot()


def test_tell_joke(bot: Bot) -> None:
    joke = bot.tell_joke()
    assert isinstance(
        joke, str
    ), f"The following joke returned by the bot is not a string. Joke: {joke}"
    assert len((joke.split(" "))) >= 2, (
        f"The joke: '{joke}', contains less than two words, which is not a"
        " sentence and hence can't be considered a joke."
    )


def test_rate_joke(bot: Bot) -> None:
    joke = "Why did the edge server go bankrupt? Because it ran out of cache."
    rating = bot.rate_joke(joke)
    assert isinstance(rating, int), f"The rating '{rating}' is not a number."
    assert rating in range(1, 11), (
        "The rating is not within range 1 to 10, which it should be. Instead"
        f" the rating is: {rating}"
    )
