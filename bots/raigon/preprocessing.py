"""
Purpose of this file
"""
import re
from googleapiclient import discovery
import time
from googleapiclient.errors import HttpError
import pandas as pd
import config


class Preprocessing:

    def __init__(self, data_frame):
        self.frame = data_frame
        self.perspective_api_model_version = config.PerspectiveApiConfig.model_version
        self.perspective_api_method = config.PerspectiveApiConfig.method
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
        cleaned_text = re.sub(r'[^\w\s]', '', text)
        return cleaned_text

    @staticmethod
    def remove_newlines_and_carriage_returns(text):
        text = text.strip()
        cleaned_text = text.replace('\n', '').replace('\r', '')
        return cleaned_text

    def create_short_jokes_dataset(self, min_length, max_length):
        """
        This function removes jokes which are below min_length and above max_length
        """
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

    @staticmethod
    def create_perspective_api_client(model_version: str, method: str):
        """
        Creates and returns a perspective API client.
        :param model_version:
        :param method:
        :return: client
        """

        client = discovery.build(
            method,
            model_version,
            developerKey=config.PerspectiveApiConfig.developer_key,
            discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=" + model_version,
            static_discovery=False
        )

        return client

    def get_attributes_from_perspective_api(self, text: str) -> dict:
        """
        Get the attributes of the joke text from the perspective API.
        :param text:
        :return: dictionary of result from the perspective client
        """

        client = self.create_perspective_api_client(self.perspective_api_model_version, self.perspective_api_method)

        analyze_request = {
            'comment': {'text': text},
            'requestedAttributes': {
                'TOXICITY': {},
                'SEVERE_TOXICITY': {},
                'PROFANITY': {}
            }
        }

        return client.comments().analyze(body=analyze_request).execute()

    def get_features_from_perspective_api(self) -> pd.DataFrame:
        """
        This function takes as input the dataframe containing the jokes and returns the
        updated frame with attributes severe_toxicity, toxicity and profanity retrieved from the perspective API.
        :param frame:
        :return: updated_frame
        """

        joke_text_lst = self.frame['joke'].tolist()

        severe_toxicity = []
        toxicity = []
        profanity = []

        counter = 0

        for text in joke_text_lst:

            try:
                result = self.get_attributes_from_perspective_api(text)
            except HttpError:
                severe_toxicity.append(-1)
                toxicity.append(-1)
                profanity.append(-1)
                continue

            severe_toxicity.append(result['attributeScores']['SEVERE_TOXICITY']['summaryScore']['value'])
            toxicity.append(result['attributeScores']['TOXICITY']['summaryScore']['value'])
            profanity.append(result['attributeScores']['PROFANITY']['summaryScore']['value'])

            time.sleep(1)  # Perspective API have a rate limit of 1 query per second.

            counter = counter + 1

        self.frame['SEVERE_TOXICITY'] = severe_toxicity
        self.frame['TOXICITY'] = toxicity
        self.frame['PROFANITY'] = profanity

        return

    def append_prompt(self, row):
        label = row['label']
        prompt = self.prompts[label]
        return prompt + ' ' + row['joke']

    def preprocess_data_for_joke_generator(self):
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
        self.frame['joke'] = self.frame['joke'].apply(self.remove_newlines_and_carriage_returns)
        self.frame = self.create_short_jokes_dataset(10, 1024)

        self.frame = self.frame[self.frame['label'] != 0]
        self.frame = self.frame[self.frame['label'] != 11]

        min_class_count = self.frame['label'].value_counts().min()
        resampled_short_jokes_frame = pd.DataFrame()

        for class_label in self.frame['label'].unique():
            class_rows = self.frame[self.frame['label'] == class_label]
            sampled_rows = class_rows.sample(min_class_count, replace=True)
            resampled_short_jokes_frame = resampled_short_jokes_frame.append(sampled_rows)

        resampled_short_jokes_frame = resampled_short_jokes_frame.sample(frac=1).reset_index(drop=True)

        updated_label = []
        for label in resampled_short_jokes_frame['label'].tolist():
            updated_label.append(label - 1)

        resampled_short_jokes_frame['label'] = updated_label

        return resampled_short_jokes_frame



