import unittest
import pandas as pd
from joke_bot_1 import Bot  # Import your Bot class from your actual code

class TestBot(unittest.TestCase):
    def setUp(self):
        # Initialize a Bot instance for testing
        self.bot = Bot()

    def test_preprocess_data(self):
        # Ensure that preprocess_data returns a DataFrame
        combined_df = self.bot.preprocess_data()
        self.assertIsInstance(combined_df, pd.DataFrame)
        # Ensure that the sorted dataframes are initialized
        self.assertIsNotNone(self.bot.sorted_happy_jokes)
        self.assertIsNotNone(self.bot.sorted_sad_jokes)
        self.assertIsNotNone(self.bot.sorted_neutral_jokes)

    def test_sort_jokes(self):
        # Create a sample combined_df for testing
        mock_data = {
            'Cleaned_Text': ['why did the chicken cross the road? To get to the otherside', 'Joke 2', 'Joke 3'],
            'Tokenized_Joke_Text': [1, 2, 3],
            'Joke_ID': [12, 13, 14],
            'Polarity': [0.1, -0.2, 0],
            'Rating': [8.0, 7.5, 9.0]
        }
        combined_df = pd.DataFrame(mock_data)
        self.bot.sort_jokes(combined_df)
        # Ensure that sorted_happy_jokes and others are DataFrames
        self.assertIsInstance(self.bot.sorted_happy_jokes, pd.DataFrame)
        self.assertIsInstance(self.bot.sorted_sad_jokes, pd.DataFrame)
        self.assertIsInstance(self.bot.sorted_neutral_jokes, pd.DataFrame)

    def test_train_model(self):
        # Create a sample combined_df for testing
        mock_data = {
            'Cleaned_Text': ['why did the chicken cross the road? To get to the otherside', 'Joke 2', 'Joke 3'],
            'Tokenized_Joke_Text': [1, 2, 3],
            'Joke_ID': [12, 13, 14],
            'Polarity': [0.1, -0.2, 0],
            'Joke_Length': [5, 8, 6],
            'Rating': [8.0, 7.5, 9.0]
        }
        combined_df = pd.DataFrame(mock_data)
        model = self.bot.train_model(combined_df)
        # Ensure that the model is not None
        self.assertIsNotNone(model)

    def test_tell_joke(self):
        # Ensure that the method returns a string
        self.test_sort_jokes()
        joke = self.bot.tell_joke('happy')
        self.assertIsInstance(joke, str)

    def test_rate_joke(self):
        # Ensure that the method returns a float
        rating = self.bot.rate_joke("This is a funny joke.")
        self.assertIsInstance(rating, float)

if __name__ == '__main__':
    unittest.main()
