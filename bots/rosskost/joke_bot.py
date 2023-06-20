from dataclasses import dataclass, field
import random
from typing import List, Optional
from textblob import TextBlob
import os
from pathlib import Path

from enum_definitions import Topic
from sbert_space import find_closest_joke_for_topic, jokes_from_file

REPRODUCIBILITY: bool = False
SEED: int = 42
if REPRODUCIBILITY:
    random.seed(SEED)
MY_DIR_NAME: str = os.path.basename(Path(__file__).parent.resolve())

AMOUNT_AVAILABLE_JOKES: int = 999
BOT_NAME: str = "rosskost_bot"


assert AMOUNT_AVAILABLE_JOKES <= len(
    jokes_from_file), f"You should set AMOUNT_AVAILABLE_JOKES to <= {len(jokes_from_file)}"

available_jokes = random.sample([joke for _, joke in jokes_from_file], AMOUNT_AVAILABLE_JOKES)


@dataclass
class Bot:
    """Bot class from user rosskost"""
    rating_model: Optional[object] = None
    topic: Optional[Topic] = None
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
        if topic:
            # if a topic is given (either in method-call or class-instance), we return a joke that is close to that topic:
            return find_closest_joke_for_topic(topic)
        else:
            # if no topic is given, just return a random joke:
            print("returning random joke due to no given topic")
            return random.choice(self.available_jokes)

    def rate_joke(self, joke) -> int:
        # Rate the joke based on its sentiment polarity
        # This is a simple example and doesn't actually reflect humor
        blob = TextBlob(joke)
        polarity = blob.sentiment.polarity
        # convert polarity from [-1, 1] to [0, 10]
        rating = round((polarity + 1) * 5)
        return rating
