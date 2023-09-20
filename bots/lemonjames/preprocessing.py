import re
import pandas as pd

class Preprocessing:
    """
        Joke Data Preprocessing and Perspective API
        This class encapsulates various preprocessing steps for joke data and provides methods for utilizing the Perspective API
        to extract attributes from the jokes.
        Args:
            data_frame (pd.DataFrame): Input DataFrame containing joke data.
        Attributes:
            frame (pd.DataFrame): The DataFrame containing joke data.
            perspective_api_model_version (str): The Perspective API model version.
            perspective_api_method (str): The Perspective API method.
            prompts (dict): A dictionary mapping label values to prompts for joke generation.
    """

    def __init__(self, data_frame):
        """
            Initialize the Preprocessing class.
            Args:
                data_frame (pd.DataFrame): Input DataFrame containing joke data.
        """
        self.frame = data_frame

    @staticmethod
    def remove_special_characters(text):
        """
        Remove special characters from the given text.
        Args:
            text (str): Input text containing special characters.
        Returns:
            str: Cleaned text with special characters removed.
        """
        cleaned_text = re.sub(r'[^\w\s]', '', text)
        return cleaned_text

    @staticmethod
    def remove_newlines_and_carriage_returns(text):
        """
        Remove new lines and carraige returns.
        Args:
            text (str): Input text containing special characters.
        Returns:
            str: Cleaned text with special characters removed.
        """
        text = text.strip()
        cleaned_text = text.replace('\n', '').replace('\r', '')
        return cleaned_text

    def create_short_jokes_dataset(self, min_length, max_length):

        self.frame = self.frame[self.frame['joke_len'] > min_length]
        self.frame = self.frame[self.frame['joke_len'] < max_length]

        return self.frame

    @staticmethod
    def remove_emoji(text_lst):
        emoji_pattern = re.compile("["
                                   u"\U0001F600-\U0001F64F"  # emoticons
                                   u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                   u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                   u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                   "]+", flags=re.UNICODE)
        clean_txt = []
        for tx in text_lst:
            clean_txt.append(emoji_pattern.sub(r'', tx))

        return clean_txt

    def preprocess_data_for_joke_rater(self):
        """
            Returns:
                DataFrame: The preprocessed DataFrame containing jokes for joke rating.
        """
        self.frame['joke'] = self.frame['joke'].apply(self.remove_newlines_and_carriage_returns)

        # Get rid of too short and too long jokes
        self.frame = self.frame[self.frame['joke_len'] > 10]
        self.frame = self.frame[self.frame['joke_len'] < 500]

        # Get rid of too stupid jokes
        self.frame = self.frame[self.frame['label'] != 0]
        self.frame = self.frame[self.frame['label'] != 1]

        # Perform undersampling to address class imbalances
        min_class_count = self.frame['label'].value_counts().min()
        resampled_short_jokes_frame = []

        for class_label in self.frame['label'].unique():
            class_rows = self.frame[self.frame['label'] == class_label]
            sampled_rows = class_rows.sample(min_class_count, replace=True)
            resampled_short_jokes_frame.append(sampled_rows)

        resampled_short_jokes_frame = pd.concat(resampled_short_jokes_frame, ignore_index=True)
        resampled_short_jokes_frame = resampled_short_jokes_frame.sample(frac=1).reset_index(drop=True)

        updated_label = list(map(lambda x: x - 2, resampled_short_jokes_frame['label'].tolist()))

        resampled_short_jokes_frame['label'] = updated_label
        return resampled_short_jokes_frame