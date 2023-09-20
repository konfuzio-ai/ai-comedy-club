from transformers import pipeline
from textblob import TextBlob
import random

class Bot:
    name = 'AnotherBot'
    def __init__(self):
        self.jokes = [
            # Science/Computer themed
            "Why don't scientists trust atoms? Because they make up everything!",
            "Why don't we tell secrets on a farm? Because the potatoes have eyes, the corn has ears, and the beans stalk.",
            "I would tell you a joke about time travel, but you didn't like it.",
            "Why don't programmers like nature? It has too many bugs.",
            "Why do programmers always mix up Christmas and Halloween? Because Oct 31 == Dec 25!",
            "Why did the programmer go broke? Because he used up all his cache.",
            "Why do programmers prefer dark mode? Because light attracts bugs.",
            "Why was the computer cold? It left its Windows open.",
            "Why did the programmer refuse to play cards with the jungle cat? Because he was afraid of Cheetahs.",
            "Why was the developer unhappy at their job? They wanted arrays.",
            # Miscellaneous themes
            "What's the best thing about Switzerland? I don't know but the flag is a big plus.",
            "What do you call a fake noodle? An impasta!",
            "What did the pirate say when he turned 80? Aye matey.",
            "What do you call an apology written in dots and dashes? Re-Morse code.",
            "What do you get from a pampered cow? Spoiled milk.",
            "I got my daughter a fridge for her birthday. I can't wait to see her face light up when she opens it.",
            "Rest in peace to boiling water. You will be mist.",
        ]
        self.joke_critic = pipeline('text-generation', model='gpt2')

    def tell_joke(self):
        # Just tell a random joke from our list
        return random.choice(self.jokes)

    def rate_joke(self, joke):
        """
        A very self-centered bot, it rates jokes that itself would tell the highest.
        
        For other jokes, use the joke as a prompt for a GPT2 model and take its 
        output as the model's reaction. Using sentiment analysis, use the reaction's 
        polarity to generate the rating.
        """
        if joke in self.jokes:
            return 10
        
        reaction = self.joke_critic(joke, max_new_tokens=25, do_sample=True)[0]['generated_text']
        blob = TextBlob(reaction)
        polarity = blob.sentiment.polarity
        rating = (polarity + 1) * 5  # convert polarity from [-1, 1] to [0, 10]
        return max(rating, 1)  # ensure the scale is obeyed (min score is 1)
