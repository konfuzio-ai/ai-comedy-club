import pytest
from unittest.mock import Mock, call
from src.presenter import PresenterInterface, NaivePresenter, NarcissusPresenter
from joke_bot import Bot

def test_bot_tell_joke():
    joke_bot = Bot(NaivePresenter(), "Tiziano's Oyster Sandwich")
    result = joke_bot.tell_joke()
    assert isinstance(result, str)

def test_bot_rate_joke():
    joke_bot = Bot(NaivePresenter(), "Tiziano's Oyster Sandwich")
    result = joke_bot.rate_joke("This is a lousy joke.")
    assert result >= 1 and result <= 10