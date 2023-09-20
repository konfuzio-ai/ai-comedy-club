import pytest
from joke_bot import Bot


@pytest.fixture
def bot():
    return Bot()

@pytest.mark.parametrize("joke", [
    "It turns out you're not the first one to think I'm a racist. I was the first to think you're a racist.",
    "      "
])
def test_rate_joke(bot, joke):
    rating = bot.rate_joke(joke)
    assert isinstance(rating, (int, float)), "Rating must be numerical."
    assert 0 <= rating <= 10, "Rating must be within 0 and 10."

def test_rate_joke_empty_string(bot):
    with pytest.raises(ValueError):
        bot.rate_joke("")
def test_rate_joke_non_string(bot):
    with pytest.raises(ValueError):
        bot.rate_joke(9)

def test_tell_joke(bot):
    joke = bot.tell_joke()
    print(f"Generated joke: {joke}")
    assert isinstance(joke, str), "Joke must be a String"