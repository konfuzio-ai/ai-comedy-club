import pytest
import warnings

from joke_bot import Bot

def test_bot_name():
    bot = Bot()
    assert bot.name == 'KevinBot'

def test_tell_joke():
    
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")

        bot = Bot()
        joke = bot.tell_joke()
        assert joke in bot.jokes or len(joke.split('\n')) == 2

        rating = bot.rate_joke(joke)
        assert isinstance(rating, (int, float)), "Rating is not a number."
        assert 0 <= rating <= 10, "Rating is not within the correct range."
