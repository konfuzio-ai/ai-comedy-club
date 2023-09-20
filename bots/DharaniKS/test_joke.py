import unittest
from unittest.mock import patch
from io import StringIO
import random
import emoji
from textblob import TextBlob
from joke import Bot

class TestBotInit(unittest.TestCase):
    def test_init(self):
        # Initialize the Bot object
        bot = Bot()
        
        # Check if the attributes are set correctly
        self.assertIn(bot.random_greeting, bot.greetings)

    @patch('builtins.input', side_effect=['John', 'Good', '1'])
    def test_intro(self, mock_input):
        bot = Bot()
        bot.intro()

        self.assertEqual(bot.aud_name, 'John')
        self.assertEqual(bot.feel, 'Good')

    @patch('builtins.input', side_effect=["Dharani","Great",9,2])
    def test_get_language_en(self, mock_input):
        print("from test_get_language_en")
        bot = Bot()
        bot.intro()  # Call intro to set aud_name and feel
        bot.get_language()
        print("bot.l_choice.. in test",bot.l_choice)

    @patch('builtins.input', side_effect=["Dharani","Great",9,1])
    @patch('pyjokes.get_joke', return_value='A funny joke')
    def test_tell_joke(self, mock_get_joke, mock_input):
        #print("from test_tell_joke")
        bot = Bot()
        bot.intro()  # Call intro to set aud_name and feel
        bot.get_language()  # Call get_language to set l_choice

        joke = bot.tell_joke()

        self.assertEqual(joke, 'A funny joke')

    def test_rate_joke_positive(self):
        bot = Bot()
        joke = "This is a great joke!"
        rating = bot.rate_joke(joke)
        self.assertGreaterEqual(rating, 6)
        self.assertLessEqual(rating, 10)

    def test_rate_joke_negative(self):
        bot = Bot()
        joke = "This is a terrible joke!"
        rating = bot.rate_joke(joke)
        self.assertGreaterEqual(rating, 1)
        self.assertLessEqual(rating, 5)

if __name__ == '__main__':
    unittest.main()              

