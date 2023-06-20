from dataclasses import dataclass
import random
from transformers import pipeline
from textblob import TextBlob

import pathlib
import os
from styles_and_topics import Codemian_Style, Topics

MY_DIR_NAME: str = os.path.basename(pathlib.Path(__file__).parent.resolve())


@dataclass
class Bot:
    """Bot class from user rosskost"""
    rating_model: object = None
    style: Codemian_Style = None
    topic: Topics = None
    name: object = "rosskost_bot"
    joke_generator = pipeline("text-generation", model="gpt2")

    @property
    def get_prompt(self) -> str:
        style_str, topic_str = "", ""
        if self.style:
            style_str = f" in the style of {self.style.value}"
        if self.topic:
            topic_str = f" about {self.topic.value}"
        return "please tell me a joke:" + style_str + topic_str + "\n"

    @property
    def tell_joke(self) -> str:
        # Use the GPT-2 model to generate a joke
        # Choose a random prefix for the joke
        prompt = self.get_prompt
        joke = self.joke_generator(f"{prompt}", max_length=25, do_sample=True)[0][
            "generated_text"
        ].replace(prompt, "")
        return joke

    def rate_joke(self, joke) -> int:
        # Rate the joke based on its sentiment polarity
        # This is a simple example and doesn't actually reflect humor
        blob = TextBlob(joke)
        polarity = blob.sentiment.polarity
        # convert polarity from [-1, 1] to [0, 10]
        rating = round((polarity + 1) * 5)
        return rating
