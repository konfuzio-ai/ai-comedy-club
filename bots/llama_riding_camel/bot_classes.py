from huggingface_hub import InferenceClient
import re
import random
import os
import sys
from textblob import TextBlob

sys.path.append(os.path.join(os.path.dirname(__file__)))
from joke_samples import all_joke_categories, get_joke_sample_from_category
from prompts import JOKE_GENERATE_PROMPT, INTRODUCTION_TEMPLATES, CATEGORY_EXTRACT_PROMPT, \
    INAPPROPRIATE_CONTENT_DETECT_PROMPT, HUMOR_CLASSIFICATION_PROMPT

MODEL_NAME = "mistralai/Mistral-7B-Instruct-v0.1"


class AIComedian:
    def __init__(self, hf_api_token: str, name: str = 'Llama riding Camel'):
        self.name = name
        self.client = InferenceClient(model=MODEL_NAME, token=hf_api_token)
        # make a dummy request to model to validate while initializing
        self._validate_client()

    @staticmethod
    def _clean_whitespaces(text: str):
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        return text

    def _validate_client(self):
        # make a dummy request to client to validate while initializing
        _ = self.detect_category_from_context("something about politics")
        return

    def generate_jokes_from_category(self, category: str, keywords: str = ''):
        joke_sample, joke_keyword = get_joke_sample_from_category(category)
        joke_sample = self._clean_whitespaces(joke_sample)
        joke_len = len(joke_sample.split())

        if keywords == '':
            keywords = joke_keyword

        prompt = JOKE_GENERATE_PROMPT.format(
            self.name, category, keywords, joke_sample
        )

        output = self.client.text_generation(
            prompt, max_new_tokens=joke_len * 10
        )
        return output

    @staticmethod
    def _parse_jokes_from_output(joke_output_gen: str, separator: str = '[END]\n'):
        jokes_list = joke_output_gen.split(separator)
        jokes_list.pop()
        for i in range(len(jokes_list)):
            joke = jokes_list[i]
            joke = joke.replace('\n', '')
            joke = re.sub(r'Joke\s?\d\s?:', '', joke)
            jokes_list[i] = joke

        return jokes_list

    def tell_joke_from_category(self, category: str, keywords: str = ''):
        generated_output = self.generate_jokes_from_category(category, keywords)
        parsed_jokes = self._parse_jokes_from_output(generated_output)
        selected_joke = random.choice(parsed_jokes)
        selected_intro = random.choice(INTRODUCTION_TEMPLATES)
        intro = self._clean_whitespaces(selected_intro.format(self.name, category))

        final_joke = intro + ' ' + selected_joke
        return final_joke

    @staticmethod
    def _parse_category_output(output: str, separator: str = 'Keywords: '):
        output_items = output.split(separator)

        if len(output_items) == 1:
            return output_items, ''

        processed_items = []
        for o in output_items:
            o = o.strip()
            processed_items.append(o)

        return processed_items[0], processed_items[1]

    def detect_category_from_context(self, context: str):
        categories = all_joke_categories()
        categories_joined = ', '.join(categories[:-1]) + ', or ' + categories[-1]

        category_prompt = CATEGORY_EXTRACT_PROMPT.format(categories_joined, context)
        output = self.client.text_generation(
            category_prompt, max_new_tokens=35,
            stop_sequences=['[END]']
        )

        return self._parse_category_output(output)

    def tell_joke(self, context: str = ''):
        categories = all_joke_categories()
        selected_category = random.choice(categories)
        keywords = ''
        if context != '':
            selected_category, keywords = self.detect_category_from_context(context)

        return self.tell_joke_from_category(selected_category, keywords)


class AIJudge:
    def __init__(self, hf_api_token: str):
        self.client = InferenceClient(model=MODEL_NAME, token=hf_api_token)

    @staticmethod
    def rate_sentiment_polarity(joke: str):
        blob = TextBlob(joke)
        polarity = blob.sentiment.polarity
        rating = (polarity + 1) * 5  # convert polarity from [-1, 1] to [0, 10]
        return rating

    @staticmethod
    def detect_if_joke_contains_question(joke: str):
        p = re.compile(r"\w+\?\s*")
        if p.search(joke):
            return True
        return False

    @staticmethod
    def _remove_end_sequence(output: str, end_sequence: str = '[END]'):
        output = output.replace(end_sequence, '')
        output = output.strip()
        return output

    def _parse_true_false_output(self, output: str):
        output = self._remove_end_sequence(output)
        true_strings = ['true', '1', 't', 'y', 'yes', 'yeah', 'yup', 'certainly']
        if output.lower() in true_strings:
            return True
        else:
            return False

    def detect_if_joke_contains_inappropriate_content(self, joke: str):
        inappropriate_prompt = INAPPROPRIATE_CONTENT_DETECT_PROMPT.format(joke)
        output = self.client.text_generation(
            inappropriate_prompt, max_new_tokens=15, stop_sequences=['[END]']
        )

        return self._parse_true_false_output(output)

    @staticmethod
    def _parse_number_output(output: str):
        parsed_ratings = [int(s) for s in re.findall(r'\b\d+\b', output)]
        if len(parsed_ratings) > 0:
            return parsed_ratings[0]
        else:
            return 0

    @staticmethod
    def _convert_humor_class_to_score(output: str):
        humor_class_dict = {
            'very funny': 10,
            'funny': 8,
            'neutral': 5,
            'not funny': 3,
            'sad': 1,
        }

        if output.lower() in humor_class_dict.keys():
            return humor_class_dict[output.lower()]
        else:
            return 0

    def rate_joke_humor(self, joke: str):
        humor_prompt = HUMOR_CLASSIFICATION_PROMPT.format(joke)
        output = self.client.text_generation(
            humor_prompt, max_new_tokens=15, stop_sequences=['[END]']
        )

        output = self._remove_end_sequence(output)
        return self._convert_humor_class_to_score(output)

    @staticmethod
    def rate_by_length(joke: str):
        # Rate the joke based on its length
        # The shorter the joke, the higher the rating
        length = len(joke)
        if length < 50:
            return 10
        elif length < 80:
            return 7
        else:
            return 5

