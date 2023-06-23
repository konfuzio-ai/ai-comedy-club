import random
import torch
from transformers import pipeline
import requests
import json

# REDDIT_DATASET is not used, but I would love to use it to train a pretrained LLM
REDDIT_DATASET = "https://datasets-server.huggingface.co/rows?dataset=SocialGrep%2Fone-million-reddit-jokes&config=SocialGrep--one-million-reddit-jokes&split=train&offset=0&limit=100"
CHUCK_API_URL = "https://api.chucknorris.io/jokes/random"


class ComedianBot:
    def __init__(self):
        self.jokes: list = list()
        self.current_joke: str = ""
        self.jokes_rating: dict = dict()
        self.current_joke_rating: float = 0
        self.current_city: str = "Berlin"
        self.jokes_learned: list = list()
        self.current_show_jokes: list = list()
        self.dad_joke_generator_pipeline = pipeline('text-generation', model='huggingtweets/dadsaysjokes')
        self.short_joke_generator = pipeline('text-generation', model='AlekseyKorshuk/gpt2-jokes')
        self.sentiment_pipeline = pipeline(model="finiteautomata/bertweet-base-sentiment-analysis")

    def get_next_show_city(self, city: str):
        self.current_city = city

    def study_new_jokes(self):
        self._learn_dad_says_jokes()
        self._copy_chuck_norris_jokes()
        self._learn_short_jokes()
        random.shuffle(self.jokes_learned)
        self.jokes += self.jokes_learned
        self.jokes_learned = list()

    def _learn_short_jokes(self):
        jokes_generated = self.short_joke_generator("What's", num_return_sequences=4)
        jokes = [joke['generated_text'] for joke in jokes_generated]
        self.jokes_learned += jokes

    def _learn_dad_says_jokes(self):
        generator = self.dad_joke_generator_pipeline
        prompts = ["my dream is", "I don't like", "I want"]
        prompts_current_city = [f"my dream is to live in {self.current_city}", f"I don't like how {self.current_city}",
                                f"I want {self.current_city}"]
        jokes_generated = generator(random.choice(prompts), num_return_sequences=8)
        jokes_generated_with_current_city = generator(random.choice(prompts_current_city), num_return_sequences=3)
        jokes_current_city = [f"You know when dad says {joke['generated_text']}" for joke in
                              jokes_generated_with_current_city]
        jokes = [f"You know when dad says {joke['generated_text']}" for joke in
                 jokes_generated]
        self.jokes_learned += jokes + jokes_current_city

    def _copy_chuck_norris_jokes(self):

        for _ in range(10):
            response = requests.get(CHUCK_API_URL)
            if response.status_code == 200:
                joke_data = json.loads(response.text)
                joke = joke_data["value"]
                self.jokes_learned.append(joke)

    def select_current_show_jokes(self, show_number_of_jokes=20):

        # select 20 jokes from jokes learned taking the last 10 (like if jokes is a LIFO)
        last_jokes_slice = slice(-show_number_of_jokes // 2, -1)
        first_jokes_slice = slice(0, show_number_of_jokes // 2)
        self.current_show_jokes += self.jokes[last_jokes_slice]
        jokes_rating_sorted = sorted(self.jokes_rating.items(), key=lambda item: item[1])
        jokes_ranking = [joke for joke, rating in jokes_rating_sorted]
        self.current_show_jokes += jokes_ranking[first_jokes_slice]
        random.shuffle(self.current_show_jokes)

    def introduce_comedian(self) -> (str, list):
        introduction = f"Hello everyone, how is people in {self.current_city}?! I'm Zuma and I'm here to make you laught (at least try)"
        return introduction

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
        self.current_joke_rating = 0

    def finish_show(self):
        self.current_show_jokes: list = list()


if __name__ == "__main__":
    bot = ComedianBot()
    bot.study_new_jokes()

    # Show simulation 1
    bot.select_current_show_jokes()

    bot.introduce_comedian()
    for i in range(10):
        print(bot.tell_joke())
        comment = random.choice(["really good", "bad", "amazing"])
        bot.notice_feedback(comments=[comment])
        print(bot.current_joke_rating)
        bot.add_joke_rating()

    bot.finish_show()
    print(bot.jokes_rating)

    bot.study_new_jokes()
    # show simulation 2
    bot.select_current_show_jokes()

    bot.introduce_comedian()
    for i in range(10):
        print(bot.tell_joke())
        comment = random.choice(["Hahahaha good", "no so good", "more or less"])
        bot.notice_feedback(comments=[comment])
        print(bot.current_joke_rating)
        bot.add_joke_rating()

    print("Jokes in both shows")
    print(set(bot.current_show_jokes) and set(bot.jokes_rating.keys()))
