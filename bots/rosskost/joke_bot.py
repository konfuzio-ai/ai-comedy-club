from dataclasses import dataclass, field
import random
from typing import List, Optional
import torch

from bots.rosskost.definitions import Topic, AbstractBot
from bots.rosskost.sbert_space import find_closest_joke_for_topic, jokes_from_file
from bots.rosskost.rating_model import model, predict


REPRODUCIBILITY: bool = False
if REPRODUCIBILITY:
    random.seed(42)
BOT_NAME: str = "Reddit Humour"
MINUMUM_REASONABLE_JOKE_LENGTH: int = 4

# per default, use all jokes:
AMOUNT_AVAILABLE_JOKES: int = len(jokes_from_file)
assert AMOUNT_AVAILABLE_JOKES <= len(
    jokes_from_file), f"You should set AMOUNT_AVAILABLE_JOKES to <= {len(jokes_from_file)}"

available_jokes = random.sample([joke for _, joke in jokes_from_file], AMOUNT_AVAILABLE_JOKES)


class Bot(AbstractBot):
    """Bot class from user rosskost that is based on Reddit Humour.
    -tell_joke() uses jokes from r/cleanjokes and is able to return a random joke or a
    joke about a particular topic. To detect jokes similar to a topic, we use SBERT embeddings and
    return a choice from the n most similar jokes.
    -rate_joke() uses the tiny variant of BERT, that was finetuned by me on scores from r/jokes
    and returns a int rating from 1-10.
    """

    def __init__(self,
                 name: str = BOT_NAME,
                 rating_model: torch.nn.Module = model,
                 topic: Optional[Topic] = None,
                 available_jokes: List[str] = available_jokes) -> None:

        self.name = name
        self.rating_model = rating_model
        self.topic = topic
        self.available_jokes = available_jokes

    def tell_joke(self, topic: Optional[Topic] = None, choice_from_top_n: Optional[int] = 5) -> str:
        if topic is None and self.topic is not None:
            topic = self.topic
        if topic:
            # if a topic is given (either in method-call or class-instance),
            # we return a joke that is semantically similar in meaning to that topic:
            return find_closest_joke_for_topic(topic, self.available_jokes, choice_from_top_n)
        else:
            # if no topic is given/wished, just return a random joke:
            return random.choice(self.available_jokes)

    def rate_joke(self, joke: str) -> int:
        if len(joke.split()) < MINUMUM_REASONABLE_JOKE_LENGTH:
            return 1

        pred = predict(joke, model=self.rating_model)
        if pred < 1:
            return 1
        if pred > 10:
            return 10
        else:
            return round(pred.item())
