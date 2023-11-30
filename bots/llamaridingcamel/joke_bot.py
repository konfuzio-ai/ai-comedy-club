import random
import os
import sys
import re
import warnings
from dotenv import load_dotenv, dotenv_values

sys.path.append(os.path.join(os.path.dirname(__file__)))
from joke_samples import get_all_jokes_list
from bot_classes import AIComedian, AIJudge, LlamaRidingCamel

load_dotenv()

# place your huggingface api token here or in env file
# else it will load the HF_API_TOKEN from .env file from the key `HF_API_TOKEN`
HF_API_TOKEN = ""
COMEDIAN_NAME = "LLama riding Camel"


class SmartAgent:
    def __init__(self, name: str = COMEDIAN_NAME):
        self.model = LlamaRidingCamel()
        self.comedian = AIComedian(self.model, name=name)
        self.jokes = get_all_jokes_list()
        self.judge = AIJudge(self.model)

    def tell_joke(self, context: str = ''):
        return self.comedian.tell_joke(context)

    @staticmethod
    def _bool_to_score(value: bool, invert: bool = False):
        if invert:
            value = not value
        return int(value) * 10

    def rate_joke(self, joke: str):
        polarity = self.judge.rate_sentiment_polarity(joke)
        inappropriate_score = self._bool_to_score(
            self.judge.detect_if_joke_contains_inappropriate_content(joke),
            invert=True
        )
        engaging_score = self._bool_to_score(self.judge.detect_if_joke_contains_question(joke))
        humor_rating = self.judge.rate_joke_humor(joke)

        # print(polarity, inappropriate_score, engaging_score, humor_rating)

        # twice weight over humor rating,
        # similarly half weight on inappropriate and engaging scores.
        avg_rating = (polarity*0.5 + inappropriate_score*0.5 + engaging_score*0.5 + humor_rating*2.5) / 4

        return round(avg_rating, 2)


class DumbAgent:
    def __init__(self, name: str):
        self.name = name
        self.jokes = get_all_jokes_list()

    @staticmethod
    def _clean_whitespaces(text: str):
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        return text

    def tell_joke(self, context: str = ''):
        intro = "Here is {} to tell you a joke.".format(self.name)
        # Just select a random joke from our list
        selected_joke = random.choice(self.jokes)
        selected_joke = self._clean_whitespaces(selected_joke)
        return intro + " " + selected_joke

    @staticmethod
    def rate_joke(joke):
        # Rate the joke based on its length
        # The shorter the joke, the higher the rating
        length = len(joke)
        if length < 50:
            return 10
        elif length < 80:
            return 6
        else:
            return 4


class Bot:
    def __init__(self):
        self.name = COMEDIAN_NAME
        self.agent = self.init_agent(COMEDIAN_NAME)

    def init_agent(self, name: str):
        # huggingface api token extraction
        # not relevant for this implementation
        config = dotenv_values()
        hf_token = HF_API_TOKEN
        if HF_API_TOKEN == "" and "HF_API_TOKEN" in config:
            hf_token = config["HF_API_TOKEN"]

        try:
            agent = SmartAgent(name=name)
        except Exception as e:
            warnings.warn('Agents initialization failed.: ' + str(e))
            print('Switching to DumbAgent.')
            agent = DumbAgent(name)

        return agent

    @staticmethod
    def _verify_hf_token(token: str):
        r = re.compile('hf_.*')
        if r.match(token) is not None:
            return True
        return False

    def tell_joke(self, context: str = ''):
        return self.agent.tell_joke(context)

    def rate_joke(self, joke):
        return self.agent.rate_joke(joke)
