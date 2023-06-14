from transformers import pipeline
from textblob import TextBlob
import random

class Bot:
    name = 'Try AI to funny'
    def __init__(self):
        self.joke_generator = pipeline('text-generation', model='gpt2')
        self.joke_prefixes = [
            "My best joke is: "
        ]

    def tell_joke(self):
        # Use the GPT-2 model to generate a joke
        # Choose a random prefix for the joke
        prefix = random.choice(self.joke_prefixes)
        joke = self.joke_generator(f'{prefix}', max_length=25, do_sample=True)[0]['generated_text']
        return joke

    def rate_joke(self, joke):
        # Rate the joke based on its sentiment polarity
        # This is a simple example and doesn't actually reflect humor
        blob = TextBlob(joke)
        polarity = blob.sentiment.polarity
        rating = (polarity + 1) * 5  # convert polarity from [-1, 1] to [0, 10]
        return rating
