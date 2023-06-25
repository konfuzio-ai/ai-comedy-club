import os
from src.presenter import NaivePresenter
from joke_bot import Bot
import pytest


@pytest.mark.incremental
class TestBot:
    def test_models_available(self):
        assert os.path.exists("models/merge-v2/trained_model/") == True or os.path.exists("models/merge-v3/trained_model/") == True, "LLM Models not found"

    def test_bot_tell_joke(self):
        joke_bot = Bot(NaivePresenter(), "Tiziano's Oyster Sandwich")
        result = joke_bot.tell_joke()
        assert isinstance(result, str)

    def test_bot_rate_joke(self):
        joke_bot = Bot(NaivePresenter(), "Tiziano's Oyster Sandwich")
        result = joke_bot.rate_joke("This is a lousy joke.")
        assert result >= 1 and result <= 10