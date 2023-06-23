import os
import pytest
from joke_bot import Bot
from dotenv import load_dotenv
import mock
import builtins


@pytest.fixture
def bot():
    return Bot()


class TestBot:

    load_dotenv()

    def test_get_text_from_chatgpt3sdk(self, bot: Bot):
        # Using temperature 0 to force the model to give always the same answer with the same prompt
        text = bot.get_text_from_chatgpt3sdk(
            "Give me always the same text", max_tokens=150, temperature=0)
        assert isinstance(text, str), "Text is not a string."
        # Although this comparisson could not always be true (depending on the model)
        # would be a good idea to check other approach
        assert text == "The same text is: \"Hello, how are you today?\""

    @pytest.mark.parametrize(
        "country, result_prompt", ((
            None, "Tell me a joke"), ("Peru", "Tell me a joke about people from Peru")),
    )
    def test_build_prompt(self, bot: Bot, country: str, result_prompt):
        prompt = bot.build_prompt(from_country=country)
        assert prompt == result_prompt

    def test_tell_joke(self, bot: Bot):
        with mock.patch.object(builtins, 'input', lambda _: 'Peru'):
            # assert Bot.function() == 'expected_output'
            joke = bot.tell_joke()
            assert isinstance(joke, str), "Joke is not a string."
        # assert len(joke) > 200, "Joke length is not within the correct range."

    def test_rate_joke(self, bot: Bot):
        joke = "Why was the computer cold at the office? Because it left its Windows open."
        rating = bot.rate_joke(joke)
        assert isinstance(rating, (int, float)), "Rating is not a number."
        assert 0 <= rating <= 10, "Rating is not within the correct range."
