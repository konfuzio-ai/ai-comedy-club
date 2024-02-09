import pytest

from joke_bot import Bot


@pytest.fixture
def bot():
    return Bot()


jokes = [
    "Why don't eggs tell jokes? They'd crack each other up.",
    "I'm reading a book on anti-gravity. It's impossible to put down!",
    "I ordered a chicken and an egg from Amazon. I’ll let you know which comes first.",
    "What do you call fake spaghetti? An impasta.",
    "Why did the scarecrow win an award? Because he was outstanding in his field.",
    "I would tell you a joke about an unfinished painting, but it’s not finished yet.",
    "What do you call a belt made out of watches? A waist of time.",
    "How do you make holy water? You boil the hell out of it.",
    "I've got a great joke about construction, but I'm still working on it.",
    "Why don't skeletons fight each other? They don't have the guts."
]


def test_tell_joke(bot):
    start_phrase = "Hello! Give me some dad's joke"
    joke = bot.tell_joke(start_phrase)
    assert isinstance(joke, str), f"Output not string, current type is {type(joke)}"


def test_rate_joke_conversation(bot):
    joke = "Why did the scarecrow win an award? Because he was outstanding in his field."
    rating = bot.rate_joke(joke, str)
    assert isinstance(rating, str), f"Output not string, current type is {type(rating)}"


@pytest.mark.parametrize("joke", jokes)
def test_rate_joke_0(bot, joke):
    rating = bot.rate_joke(joke)
    assert isinstance(rating, int), f"The rating is not an integer. Rating {rating} type is {type(rating)}"
    assert 1 <= rating <= 10, f"The rating is not in range from 1 to 10. Rating is {rating}"
