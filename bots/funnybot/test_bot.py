import unittest
from unittest import mock

from joke_bot import Bot


class BotTest(unittest.TestCase):
    def setUp(self):
        self.bot = Bot()
        self.patcher = mock.patch("builtins.input")
        self.mocked_input = self.patcher.start()
        self.no_soup_for_you = (
            "Sorry, I don't have any other jokes. That's just Awkward."
        )

    def tearDown(self):
        self.patcher.stop()

    def test_tells_joke_to_a_easy_going_user(self):
        self.mocked_input.side_effect = ["yes"]

        joke = self.bot.tell_joke()
        assert isinstance(joke, str), "Joke is not a string."
        assert joke != self.no_soup_for_you

    def test_tells_joke_to_a_bit_fussy_user(self):
        self.mocked_input.side_effect = ["no", "yes"]

        joke = self.bot.tell_joke()
        assert isinstance(joke, str), "Joke is not a string."
        assert joke != self.no_soup_for_you

    def test_tells_joke_to_a_fussy_user(self):
        self.mocked_input.side_effect = ["no", "no"]

        joke = self.bot.tell_joke()
        assert isinstance(joke, str), "Joke is not a string."
        assert joke == self.no_soup_for_you

    def test_rates_joke(self):
        joke = """
            It is the ultimate joke. 
            Humans make comedy, humans build robot, robot ends all life on earth, robot feels awkward.
        """

        assert self.bot.rate_joke(joke) >= 1
        assert self.bot.rate_joke(joke) <= 10
