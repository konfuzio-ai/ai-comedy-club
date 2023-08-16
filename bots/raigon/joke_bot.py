import random
from transformers import pipeline
import json
import sys
import os

script_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, script_dir)

from joke_api import get_joke
import config


class Bot:
    name = 'raigon'

    def __init__(self):
        self.christmas_joke_api_url = config.JokeApiConfig.christmas_joke_api_url
        self.programming_joke_api_url = config.JokeApiConfig.programming_joke_api_url
        self.joke_generator_model = config.JokeModelConfig.path_to_joke_generator_model
        self.joke_rater_model = config.JokeModelConfig.path_to_joke_rater_model
        self.joke_prompts = [
            "Give me a hilarious joke that deserves a perfect 10: ",
            "Let's challenge the comedy genius within you. Craft a joke that is an absolute 9 in humor: ",
            "Make me smile with a joke worth a solid 8: ",
            "Let's challenge the comedy genius within you. Craft a joke that is an absolute 9 in humor: ",
            "Time to test your wit. Create a rib-tickler with a humor rating of 7: ",
            "I need a side-splitting joke that's at least an 6 on the humor scale: "
        ]
        self.joke_generator_pipeline = pipeline('text-generation',
                                                model=self.joke_generator_model,
                                                tokenizer="gpt2",
                                                )
        self.joke_rater_pipeline = pipeline('text-classification',
                                            model=self.joke_rater_model,
                                            tokenizer='bert-base-uncased')
        with open(os.path.join(script_dir, config.FileConfig.user_feedback_file), 'r') as json_file:
            self.user_feedback = json.load(json_file)
        self.joke_type = 'programming'

    def rate_joke(self, joke: str) -> int:
        joke_rating = self.joke_rater_pipeline(joke)[0]['label'][-1]
        return int(joke_rating) + 1

    def tell_joke(self):
        if self.joke_type == 'christmas':
            return get_joke(self.christmas_joke_api_url)
        elif self.joke_type == 'programming':
            return get_joke(self.programming_joke_api_url)
        else:
            prompt = random.choice(self.joke_prompts)
            generated_joke = self.joke_generator_pipeline(prompt,
                                                          max_length=50,
                                                          do_sample=True,
                                                          early_stopping=True,
                                                          repetition_penalty=2.2
                                                          )[0]['generated_text']

            generated_joke = generated_joke.lstrip(prompt)
            return generated_joke

    def user_interaction(self):
        user_mood = input('How are you feeling today? (good/bad)')
        if user_mood == 'good':
            user_input = input('Great!! Would you like to hear a Christmas joke? (y/n)')
            if user_input == 'y':
                self.joke_type = 'christmas'
                joke = self.tell_joke()
            else:
                user_input = input('Would you prefer a programming joke? (y/n)')
                if user_input == 'y':
                    self.joke_type = 'programming'
                    joke = self.tell_joke()
                else:
                    self.joke_type = 'rjokes'
                    joke = self.tell_joke()
        else:
            print('Let me cheer you up with a joke :)')
            self.joke_type = 'rjokes'
            joke = self.tell_joke()

        print(joke)
        user_joke_rating = input('How will you rate this joke out of 1 to 10:')
        self.user_feedback.append({'joke': joke, 'user_rating': user_joke_rating})

        return

    def save_user_feedback(self):
        with open(os.path.join(script_dir, config.FileConfig.user_feedback_file), 'w') as json_file:
            json.dump(self.user_feedback, json_file, indent=4)


if __name__ == '__main__':
    bot = Bot()
    bot.user_interaction()
    bot.save_user_feedback()
