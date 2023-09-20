import random
import torch
from transformers import pipeline
import requests
import json

# REDDIT_DATASET is not used, but I would love to use it to train a pretrained LLM
REDDIT_DATASET = "https://datasets-server.huggingface.co/rows?dataset=SocialGrep%2Fone-million-reddit-jokes&config=SocialGrep--one-million-reddit-jokes&split=train&offset=0&limit=100"
CHUCK_API_URL = "https://api.chucknorris.io/jokes/random"


class ComedianBot:
    """
    Class that tell jokes and rate them to improve the quality of the jokes with the experience: Each show bot use 50%
    of the best jokes it has learned and 50% of new jokes.
    """

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
        """This method store the city of the current show"""
        self.current_city = city

    def study_new_jokes(self):
        """This method adds new jokes to jokes learned"""
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
        prompts = ["my dream is", "I don't like", "I want"]  # recommended prompts from the documentation
        prompts_current_city = [f"my dream is to live in {self.current_city}", f"I don't like how {self.current_city}",
                                f"I want {self.current_city}"]  # Adding current city to the prompts
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
        """
        this method select half of the best jokes and half of new jokes and store them in current show jokes
        Args:
            show_number_of_jokes: Optinal

        Returns:

        """

        last_jokes_slice = slice(-show_number_of_jokes // 2, -1)
        first_jokes_slice = slice(0, show_number_of_jokes // 2)
        self.current_show_jokes += self.jokes[
            last_jokes_slice]  # Selecting the jokes from the end
        jokes_rating_sorted = sorted(self.jokes_rating.items(),reverse= True ,key=lambda item: item[1]) # ordering desc
        jokes_ranking :list = [joke for joke, rating in jokes_rating_sorted]
        self.current_show_jokes += jokes_ranking[first_jokes_slice] # adding best jokes
        random.shuffle(self.current_show_jokes)

    def introduce_comedian(self):
        """This method introduce the comedian"""
        introduction = f"Hello everyone! how is people in {self.current_city}?! I'm Zuma and I'm here to make you laught (at least try)"
        return introduction

    def tell_joke(self) -> str:
        """
        This method return a joke based on the current show jokes
        """
        joke = random.choice(self.current_show_jokes)
        self.current_joke = joke
        return joke

    def notice_feedback(self, comments: list[str], is_there_applause: bool = None,
                        are_there_laughs: bool = None):
        """
        This method notice feedback from the audience and rate the current joke
        Args:
            comments: list of comments (strings) from the audience
            is_there_applause: Optional
            are_there_laughs: Optional

        Returns: None

        """

        if is_there_applause:
            self.current_joke_rating += 3
        if are_there_laughs:
            self.current_joke_rating += 2
        if comments:
            sentiment_pipeline = self.sentiment_pipeline
            sentiment_data = sentiment_pipeline(comments)
            sentiment_scores = [sentiment["score"] if sentiment["label"] == "POS" else -sentiment["score"] for sentiment
                                in sentiment_data]  # multiply by -1 if sentiment is negative
            sentiment_rating = 5 * abs(sum(sentiment_scores)) / len(
                sentiment_data)  # mean and multiply by 5 to have rating between 0 and 10
            self.current_joke_rating += sentiment_rating

    def add_joke_rating(self):
        """This method add the joke and rating to joke rating and set the current joke to 0"""
        self.jokes_rating[self.current_joke] = self.current_joke_rating
        self.current_joke_rating = 0

    def finish_show(self):
        """This method remove the current show jokes"""
        self.current_show_jokes = list()


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
