import pytest
from joke_bot import JokeBot

def test_bot_name():
    bot = JokeBot()
    assert bot.name == 'etexaco123'

def test_tell_joke(category,prompt):
    bot = JokeBot()
    joke = bot.tell_joke(prompt)
    assert joke in bot.jokes_by_type[category], "Invalid Choice"
    assert isinstance(joke, str), "Not a string" # to make sure its a string

def test_rate_joke():
    bot = JokeBot()
    short_joke = "Whats wrong with nature? It has too many bugs."
    medium_joke = "Why was the computer cold? It left its Windows open."
    long_joke = "I'm not a fan of computer jokes. Not one bit. I tried to catch some fog earlier. Mist. I'm reading a book about anti-gravity. It's impossible to put down."

    # assert bot.rate_joke(short_joke) == 10 , "Not very good"
    # assert bot.rate_joke(medium_joke) == 7
    # assert bot.rate_joke(long_joke) == 5
    result = bot.rate_joke()
    assert isinstance(result, int), "Expected an integer return value"


test_bot_name()
test_tell_joke("Animal", "Why don't scientists trust atoms? Because they make up everything!")
test_rate_joke()