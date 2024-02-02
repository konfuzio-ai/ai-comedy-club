import pytest
from joke_bot import Bot
import sys

@pytest.fixture
def bot():
    return Bot()

def test_tell_joke_without_category(bot):
    bot.tell_joke()
    assert isinstance(sys.stdout.read(), str)

def test_tell_joke_with_category(bot):
    bot.tell_joke("Pun")
    assert isinstance(sys.stdout.read(), str)

def test_tell_joke_with_non_existing_category(bot):
    bot.tell_joke("ABCD")
    assert isinstance(sys.stdout.read(), str)

def test_tell_generated_joke(bot):
    bot.tell_joke("generate")
    assert isinstance(sys.stdout.read(), str)

def test_rate_joke(bot):
    assert isinstance(bot.rate_joke("Random joke"), int)

def test_opener(bot):
    bot.opener()
    assert isinstance(sys.stdout.read(), str)

def test_closer(bot):
    with pytest.raises(SystemExit) as e:
        bot.closer()
    assert e.type == SystemExit

def test_check_message_without_profanity(bot):
    assert bot.checkMessage("Hello!") is False

def test_check_message_with_profanity(bot):
    assert bot.checkMessage("Stupid") is True