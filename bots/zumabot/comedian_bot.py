import random
import torch
from transformers import pipeline
import requests
import json

url = "https://api.example.com/data"  # Replace with the actual URL you want to request

# Send GET request
# response = requests.get(url)

# Check if the request was successful (status code 200)
# if response.status_code == 200:
# Print the response content
#   print(response.text)
# else:
# print("Request failed with status code:", response.status_code)
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

dataset = "https://datasets-server.huggingface.co/rows?dataset=SocialGrep%2Fone-million-reddit-jokes&config=SocialGrep--one-million-reddit-jokes&split=train&offset=0&limit=100"
CHUCK_API_URL = "https://api.chucknorris.io/jokes/random"


class ComedianBot:
    def __init__(self):
        self.current_joke: str = ""
        self.jokes_rating: dict = {}
        self.current_joke_rating: float = 0
        self.current_city: str = "Berlin"
        self.current_city_context: str = ""
        self.jokes_learned: list = []
        self.current_show_jokes: list = []
        self.dad_joke_generator_pipeline = pipeline('text-generation', model='huggingtweets/dadsaysjokes')
        self.sentiment_pipeline = pipeline(model="finiteautomata/bertweet-base-sentiment-analysis")

    def study_new_jokes(self):
        self._learn_dad_says_jokes()
        self._copy_chuck_norris_jokes()

    def _learn_dad_says_jokes(self):
        generator = self.dad_joke_generator_pipeline
        prompts = ["My dream is", "I don't like", "I want"]
        jokes_generated = generator(random.choice(prompts), num_return_sequences=10)
        jokes = [f"You know when dad says {joke['generated_text']}" for joke in jokes_generated]
        self.jokes_learned += jokes

    def _copy_chuck_norris_jokes(self):

        for i in range(10):
            response = requests.get(CHUCK_API_URL)
            if response.status_code == 200:
                joke_data = json.loads(response.text)
                joke = joke_data["value"]
                self.jokes_learned.append(joke)

    def select_current_show_jokes(self, show_number_of_jokes=20):

        # select 20 jokes from jokes learned taking the last 10 (like if jokes_learned is a LIFO)
        self.current_show_jokes += self.jokes_learned[-show_number_of_jokes // 2:-1]
        jokes_rating_sorted = sorted(self.jokes_rating.items(), key=lambda item: item[1])
        jokes_ranking = [joke for joke, rating in jokes_rating_sorted]
        self.current_show_jokes += jokes_ranking[:show_number_of_jokes // 2]

    def get_city_context(self, city: str):
        pass

    def introduce_comedian(self) -> (str, list):
        introduction = f"Hello everyone, how is people in {self.current_city}"
        feedback = list()
        return introduction, feedback

    def tell_joke(self) -> str:
        joke = random.choice(self.current_show_jokes)
        self.current_joke = joke
        return joke

    def notice_feedback(self, comments: list[str], is_there_applause: bool = None,
                        are_there_laughs: bool = None):
        """Method to notice feedback from the audience"""
        if is_there_applause:
            self.current_joke_rating += 3
        if are_there_laughs:
            self.current_joke_rating += 2
        if comments:
            sentiment_pipeline = self.sentiment_pipeline
            sentiment_data = sentiment_pipeline(comments)
            sentiment_scores = [sentiment["score"] if sentiment["label"] == "POS" else -sentiment["score"] for sentiment
                                in sentiment_data]
            sentiment_rating = 5 * sum(sentiment_scores) / len(sentiment_data)
            self.current_joke_rating += sentiment_rating

    def add_joke_rating(self):
        self.jokes_rating[self.current_joke] = self.current_joke_rating

    def finish_show(self):
        self.current_show_jokes: list = []
        self.current_joke_rating: float = 0



if __name__ == "__main__":
    bot = ComedianBot()
    bot.study_new_jokes()
    bot.select_current_show_jokes()
    print(bot.tell_joke())
    print(bot.current_joke_rating)
    bot.add_joke_rating()
