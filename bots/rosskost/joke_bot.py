from dataclasses import dataclass, field
import random
from typing import List, Optional
from transformers import pipeline
from textblob import TextBlob
import os

import pandas as pd
from pathlib import Path
from enum_definitions import Codemian_Style, Topic

REPREDUCABILITY: bool = False
SEED: int = 42
if REPREDUCABILITY:
    random.seed(SEED)
MY_DIR_NAME: str = os.path.basename(Path(__file__).parent.resolve())
JOKES_FILE: str = os.path.join(Path(__file__).parent, "data", "funjokes.csv")
AMOUNT_AVAILABLE_JOKES: int = 100
BOT_NAME: str = "rosskost_bot"

jokes_from_file = pd.read_csv(JOKES_FILE)["Joke"].values.tolist()
available_jokes = random.sample(jokes_from_file, AMOUNT_AVAILABLE_JOKES)


@dataclass
class Bot:
    """Bot class from user rosskost"""
    rating_model: object = None
    style: Codemian_Style = None
    topic: Topic = None
    name: str = BOT_NAME
    available_jokes: List[str] = field(default_factory=lambda: available_jokes)

    @property
    def get_prompt(self) -> str:
        _style_str, _topic_str = "", ""
        if self.style:
            _style_str = f" in the style of {self.style.value}"
        if self.topic:
            _topic_str = f" about {self.topic.value}"
        return "please tell me a joke" + _style_str + _topic_str + ": \n"

    def tell_joke(self, topic: Optional[Topic] = None) -> str:
        if topic is None and self.topic is not None:
            topic = self.topic
        return random.choice(self.available_jokes)

    def rate_joke(self, joke) -> int:
        # Rate the joke based on its sentiment polarity
        # This is a simple example and doesn't actually reflect humor
        blob = TextBlob(joke)
        polarity = blob.sentiment.polarity
        # convert polarity from [-1, 1] to [0, 10]
        rating = round((polarity + 1) * 5)
        return rating
