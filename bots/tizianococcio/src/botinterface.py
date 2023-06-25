import pandas as pd
import os
import yaml
from src.gpttrainer import LanguageModelInterface, GPTTrainer
from src.lstmjokerater import LSTMJokeRaterImproved
from src.rater import JokeRaterInterface, Rater


class BotInterface:
    def __init__(self, config_file='config.yaml'):
        # Get the absolute path to the directory containing the current file
        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        self.moods = None
        self.styles = None
        self.lm = None
        self.joke_rater = None
        self.config = self.load_config(os.path.join('..', config_file))
        self.moods = self.load_moods()
        self.styles = self.load_styles()
        self.lm = self.load_lm(model=self.config['language_model'])

    def load_config(self, config_file: str):
        """
        Loads configurations from a YAML file.

        Args:
            config_file: str: Relative path to the YAML configuration file.
        
        Returns:
            dict: Dictionary containing the configurations.
        """
        with open(os.path.join(self.dir_path, config_file)) as file:
            config = yaml.safe_load(file)
        return config

    def load_moods(self) -> list:
        """
        Loads moods from csv file.

        Returns:
            list: List of moods.
        """
        if self.moods is None:
            df = pd.read_csv(os.path.join(self.dir_path, '..', 'data/tweet_emotions_balanced.csv'))
            self.moods = df['sentiment'].unique().tolist()

        return self.moods

    def load_styles(self) -> list:
        """
        Loads styles from csv file.

        Returns:
            list: List of styles.
        """
        if self.styles is None:
            df = pd.read_csv(os.path.join(self.dir_path, '..', 'data/200k/data_merge_moods.csv'))
            self.styles = df['Joke'].unique().tolist()

        return self.styles
    
    def load_lm(self, model: str = "merge-v3", data: str = "data_merge_moods.csv") -> LanguageModelInterface:
        """
        Loads language model.

        Returns:
            LanguageModelInterface: Language model.
        """
        if self.lm is None:
            data = os.path.join(self.dir_path, '..', 'data', '200k', data)
            model = os.path.join(self.dir_path, '..', 'models', model)
            self.lm = GPTTrainer(model, data)
            self.lm.load_model()
        return self.lm
    
    def load_joke_rater(self) -> JokeRaterInterface:
        """
        Loads joke rater.

        Returns:
            JokeRaterInterface: Joke rater.
        """
        if self.joke_rater is None:
            rating_model = os.path.join(self.dir_path, '..', 'models/lstm_joke_rater_improved/model')
            rating_tokenizer = os.path.join(self.dir_path, '..', 'models/lstm_joke_rater_improved/tokenizer')
            lstm_rater = LSTMJokeRaterImproved(model_path=rating_model, tokenizer_path=rating_tokenizer, max_length=256)

            self.joke_rater = Rater()
            self.joke_rater.add_rater(lstm_rater)
        return self.joke_rater