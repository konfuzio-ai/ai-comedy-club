from transformers import pipeline
from textblob import TextBlob
import random
import spacy
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

from transformers import GPT2Tokenizer, GPT2LMHeadModel

class Bot:
    name = 'Funny Johnnie D.'

    def __init__(self, text=None):
        text = text if text is not None else self.tell_joke()
        self.joke_generator = pipeline('text-generation', model='gpt2')
        self.joke_prefixes = [
            "My best joke is: "
        ]

        # Initialize the NLP components
        self.sentiment_analyzer = TextBlob()
        self.nlp = spacy.load("en_core_web_sm")

    def tell_joke(self):
        # Define the joke attributes
        humor = "funny"
        creativity = "high"
        timeliness = "current"
        audience = "everyone"
        comedian = "Johnnie Depp"

        # Use the GPT-2 model to generate a joke
        # Choose a random prefix for the joke
        prefix = random.choice(self.joke_prefixes)
        generated_joke = self.joke_generator(f'{prefix}', max_length=75, do_sample=True)[0]['generated_text']

        # Analyze the sentiment of the joke
        sentiment = self.analyze_sentiment(generated_joke)

        # Return the formatted joke
        formatted_joke = f"Tell a joke that is {humor}, {creativity}, {timeliness} for {audience} in the style of {comedian}:"
        formatted_joke += f"\n{generated_joke}"
        formatted_joke += f"\nSentiment: {sentiment}"
        return formatted_joke

    def analyze_sentiment(self, text):
        # Use TextBlob for sentiment analysis
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        sentiment = "Positive" if polarity > 0 else "Negative" if polarity < 0 else "Neutral"
        return sentiment

    def rate_joke(self, joke):
        # Rate the joke based on its sentiment polarity
        # This is a simple example and doesn't actually reflect humor
        blob = TextBlob(joke)
        polarity = blob.sentiment.polarity
        rating = (polarity + 1 + 0.5001) * 5  # convert polarity from [-1, 1] to [0, 10]
        return rating
