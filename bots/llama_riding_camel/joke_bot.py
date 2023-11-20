import random
import os
import sys
import re
import warnings
from dotenv import load_dotenv, dotenv_values

sys.path.append(os.path.join(os.path.dirname(__file__)))
from joke_samples import get_all_jokes_list
from bot_classes import AIComedian, AIJudge

load_dotenv()

# place your huggingface api token here or in env file
# else it will load the HF_API_TOKEN from .env file from the key `HF_API_TOKEN`
HF_API_TOKEN = ""
COMEDIAN_NAME = "LLama riding Camel"


class SmartAgent:
    def __init__(self, hf_api_token: str, name: str = COMEDIAN_NAME):
        self.comedian = AIComedian(hf_api_token, name=name)
        self.jokes = get_all_jokes_list()
        self.judge = AIJudge(hf_api_token)

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
        self.bot = self.init_agent(COMEDIAN_NAME)

    def init_agent(self, name: str):
        config = dotenv_values()
        hf_token = HF_API_TOKEN
        if HF_API_TOKEN == "" and "HF_API_TOKEN" in config:
            hf_token = config["HF_API_TOKEN"]

        agent = DumbAgent(name)
        if self._verify_hf_token(hf_token):
            try:
                agent = SmartAgent(hf_token, name=name)
            except Exception as e:
                print("Huggingface API authentication failed. Switching back to dumb agent")
                warnings.warn('Huggingface API authentication failed: ' + str(e))
        else:
            print("Invalid Huggingface hub api token provided. Can\'t initialize smart agent. \
Switching to DumbAgent")
            warnings.warn("Invalid Huggingface hub api token")
        return agent

    @staticmethod
    def _verify_hf_token(token: str):
        r = re.compile('hf_.*')
        if r.match(token) is not None:
            return True
        return False

    def tell_joke(self, context: str = ''):
        return self.bot.tell_joke(context)

    def rate_joke(self, joke):
        return self.bot.rate_joke(joke)


'''
loading quantized model
loading quantized models code demo

from transformers import AutoTokenizer
from auto_gptq import AutoGPTQForCausalLM
from huggingface_hub import snapshot_download

self.model_name_or_path = "TheBloke/Llama-2-13B-chat-GPTQ"
self.model_basename = "gptq_model-4bit-128g"
local_folder = "./models/test-llama-2"

snapshot_download(repo_id=self.model_name_or_path, local_dir=local_folder, local_dir_use_symlinks=False)

self.tokenizer = AutoTokenizer.from_pretrained(self.model_name_or_path, use_fast=True)

self.model = AutoGPTQForCausalLM.from_quantized(local_folder,
                                                model_basename=self.model_basename,
                                                use_safetensors=True,
                                                trust_remote_code=True,
                                                device="cpu",
                                                use_triton=False,
                                                quantize_config=None)
'''
