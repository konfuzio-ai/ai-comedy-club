import pytest
from .joke_bot import Bot

def test_tell_joke():
    bot = Bot()
    main_context = "tell me a joke about the country that is the current winner of men's football world cup"
    joke_reply = bot.tell_joke(main_context)
    assert len(joke_reply) > 10
    assert isinstance(joke_reply, str)
    assert isinstance(bot.verify_context(main_context, joke_reply), bool)

def test_tell_joke_with_memory():
    bot = Bot()
    main_context = "tell me a joke about birds and trees"
    joke_reply_1 = bot.tell_joke(main_context)
    joke_reply_2 = bot.tell_joke("tell me another one")    
    assert len(joke_reply_2) > 10
    assert isinstance(joke_reply_2, str)
    assert isinstance(bot.verify_context(main_context, joke_reply_2), bool)

def test_rate_joke():
    bot = Bot()
    rating = bot.rate_joke("Why didn't Argentina bring a map to the World Cup? Because they already knew the way to the final!")
    assert isinstance(rating, int)
    assert rating >= 0 and rating <= 10


