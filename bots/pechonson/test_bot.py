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
        "country, result_prompt, language", (
            (None, "Tell me a joke", None),
            (None, "Tell me a joke in Deutsch", "Deutsch"),
            ("Peru", "Tell me a joke about people from Peru", None),
            ("Peru", "Tell me a joke about people from Peru in Spanish", "Spanish")),
    )
    def test_build_prompt(self, bot: Bot, country: str, result_prompt: str, language: str):
        prompt = bot.build_prompt(from_country=country, language=language)
        assert prompt == result_prompt

    @pytest.mark.parametrize(
        "reaction, temperature, new_temperature", (
            (1, 0.7, 0.7),
            (2, 1.0, 1.1),
            (3, 1.0, 1.3),
            (3, 1.9, 2.0)),
    )
    def test_change_temperature_according_to_public(self, bot: Bot, reaction, temperature, new_temperature):
        changed_temperature = bot.change_temperature_according_to_public(
            reaction=reaction, temperature=temperature)
        assert new_temperature == changed_temperature

    def test_tell_introductory_phrase(self, bot: Bot, capfd):
        bot.tell_introductory_phrase()
        out, err = capfd.readouterr()
        assert isinstance(out, str), "There is no output in console"

    def test_get_country_from_user(self, bot: Bot):
        with mock.patch.object(builtins, 'input', lambda _: 'Peru'):
            country = bot.get_country_from_user()
            assert country == "Peru"

    def test_get_language_from_user(self, bot: Bot):
        with mock.patch.object(builtins, 'input', lambda _: 'Spanish'):
            bot.from_country = "Peru"
            language = bot.get_language_from_user()
            assert language == "Spanish"

    def test_translate_if_not_english(self, bot: Bot):
        bot.language = "Spanish"
        text = "Translate this text"
        translated_text = bot.translate_if_not_english(text)
        assert text != translated_text

    def test_translate_if_english(self, bot: Bot):
        bot.language = "English"
        text = "Translate this text"
        translated_text = bot.translate_if_not_english(text)
        assert text == translated_text

    def test_get_default_language_from_user(self, bot: Bot):
        with mock.patch.object(builtins, 'input', lambda _: ''):
            bot.from_country = "Peru"
            language = bot.get_language_from_user()
            # English is the language by default
            assert language == "English"

    def test_pick_comedian(self, bot: Bot):
        with mock.patch.object(builtins, 'input', lambda _: '2'):
            comedian = bot.pick_comedian()
            assert isinstance(comedian, str), "No comedian has been chosen"

    def test_pick_no_comedian(self, bot: Bot):
        with mock.patch.object(builtins, 'input', lambda _: '10'):
            comedian = bot.pick_comedian()
            assert comedian == None

    def test_improvise_a_joke(self, bot: Bot, capfd):
        with mock.patch.object(builtins, 'input', lambda _: 'Peru'):
            bot.comedian = None
            joke = bot.improvise_a_joke()
            assert isinstance(joke, str), "Joke is not a string."
            out, err = capfd.readouterr()
            assert isinstance(out, str), "There is no output in console"

    def test_tell_outro_phrase(self, bot: Bot, capfd):
        bot.tell_outro_phrase()
        out, err = capfd.readouterr()
        assert isinstance(out, str), "There is no output in console"


    def test_tell_joke(self, bot: Bot, capfd):
        with mock.patch.object(builtins, 'input', lambda _: 'Peru'):
            joke = bot.tell_joke()
            assert isinstance(joke, str), "Joke is not a string."
            out, err = capfd.readouterr()
            assert isinstance(out, str), "There is no output in console"

    def test_rate_joke(self, bot: Bot):
        joke = "Why was the computer cold at the office? Because it left its Windows open."
        rating = bot.rate_joke(joke)
        assert isinstance(rating, (int, float)), "Rating is not a number."
        assert 0 <= rating <= 10, "Rating is not within the correct range."
