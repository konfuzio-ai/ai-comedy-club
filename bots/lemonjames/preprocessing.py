import re
import pandas as pd
import config


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
        self.prompts = {
            10: "Give me a hilarious joke that deserves a perfect 10: ",
            9: "Let's challenge the comedy genius within you. Craft a joke that is an absolute 9 in humor: ",
            8: "Make me smile with a joke worth a solid 8: ",
            7: "Time to test your wit. Create a rib-tickler with a humor rating of 7: ",
            6: "I need a side-splitting joke that's at least an 6 on the humor scale: ",
            5: "Tickle my funny bone with a joke that falls between 5 and 6 on the humor scale:",
            4: "Generate a joke with a humor score of 4:",
            3: "Time for some light-hearted humor, a casual joke ranking around 3 should do:",
            2: "Even the best comedians start somewhere. Share a joke with a humor level around 2:",
            1: "Generate a joke which not that funny:"
        }

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

    def append_prompt(self, row):
        label = row['label']
        prompt = self.prompts[label]
        return prompt + ' ' + row['joke']

    def preprocess_data_for_joke_generator(self):
        """
        Preprocess joke data for joke generator task.
        This method applies a series of preprocessing steps to the input DataFrame containing joke data,
        preparing it for training a joke generator model. The preprocessing steps include removing special characters,
        newlines, and short jokes, and appending prompts to jokes.
        Returns:
            pd.DataFrame: The preprocessed DataFrame containing jokes for joke generation.
        """
        self.frame['joke'] = self.frame['joke'].apply(self.remove_special_characters)
        self.frame['joke'] = self.frame['joke'].apply(self.remove_newlines_and_carriage_returns)
        self.frame = self.create_short_jokes_dataset(10, 50)

        self.frame = self.frame[self.frame['label'] != 0]

        # self.frame = self.get_features_from_perspective_api()         # Commenting this out due to large runtime due to the rate limit of perspective API

        self.frame = pd.read_csv('data/short_jokes_with_toxicity_score.csv')

        self.frame = self.frame[self.frame['SEVERE_TOXICITY'] < 0.7]    # I have set the threshold as 0.7 based on manual inspection of some of the examples
        self.frame = self.frame[self.frame['TOXICITY'] < 0.7]
        self.frame = self.frame[self.frame['PROFANITY'] < 0.7]

        self.frame = self.frame[self.frame['label'] != 11]

        self.frame['joke'] = self.frame.apply(self.append_prompt, axis=1)

        return self.frame

    def preprocess_data_for_joke_rater(self):
        """
            Preprocess joke data for joke rater task.
            This method applies preprocessing steps to the input DataFrame containing joke data,
            preparing it for training a joke rater model. The preprocessing steps include removing newlines,
            short jokes, and balancing the dataset classes.

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