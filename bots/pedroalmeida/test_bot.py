import pytest
from joke_bot import Bot

def test_bot_name():
    bot = Bot()
    assert bot.name == 'AnotherBot'

def test_tell_joke():
    bot = Bot()
    joke = bot.tell_joke()
    assert isinstance(joke, str), "Joke is not a string."
    assert joke in bot.jokes, "Joke is not in the repertoire"

def test_rate_joke():
    bot = Bot()
    outside_joke = "Why did the programmer go on a diet? He had too many bytes."
    outsite_rating = bot.rate_joke(outside_joke)
    inside_joke = "Why was the computer cold? It left its Windows open."
    inside_rating = bot.rate_joke(inside_joke)

    assert isinstance(inside_rating, (int, float)), "Rating is not a number."
    assert inside_rating == 10, "A joke in the bot's repertoire did not get max rating"
    assert isinstance(outsite_rating, (int, float)), "Rating is not a number."
    assert 0 <= outsite_rating <= 10, "Rating is not within the correct range."
