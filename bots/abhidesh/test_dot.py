import pytest
from joke_bot import Bot

@pytest.fixture
def bot_instance():
    return Bot()

def test_tell_joke(bot_instance):
    joke = bot_instance.tell_joke()
    assert isinstance(joke, str)
    assert joke != ""

def test_rate_joke(bot_instance):
    joke = "Why did the chicken cross the road? To get to the other side!"
    rating = bot_instance.rate_joke(joke)
    assert isinstance(rating, int)
    assert 1 <= rating <= 10

