import random
import os
import sys

get_file_path = lambda : os.path.split(os.path.realpath(__file__))[0]
sys.path.insert(0, get_file_path())

from custom_pyjokes import get_categories, get_joke
from train_rate_joke import rate_joke, load_model

class Bot:
    name = 'flossCoder jokeBot'
    def __init__(self, filename = "joke_model", wd = None):
        """
        Set up our flossCoder jokeBot.

        Parameters
        ----------
        filename : string, optional
            The filename of the jester ratings dataset. The default is "joke_model".
        wd : string, optional
            The working directory of the model.
            The default is FILE_PATH_TRAIN_RATE_JOKE. Which is the path of this script.
            The default is indicated by None.

        Returns
        -------
        None.

        """
        self.joke_categories = get_categories()
        self.model = load_model(filename, wd)
    
    def interactive_joking(self):
        """
        This function implements some kind of interactive joking.

        Returns
        -------
        None.

        """
        print("Hi mate, I'm " + self.name)
        hear_joke = input("Do you wanne hear a joke? (y / n) ")
        while hear_joke == "y":
            question_category = random.randint(0,3)
            if question_category == 0:
                question = input("Are you happy today? (y / n) ")
                if question == "y":
                    print(self.tell_joke("all"))
                else:
                    print(self.tell_joke("chuck"))
            elif question_category == 1:
                question = input("Are you a programmer? (y / n) ")
                if question == "y":
                    print(self.tell_joke("programmer"))
                else:
                    print(self.tell_joke("computer"))
            elif question_category == 2:
                question = input("Do you like Java? (y / n) ")
                if question == "y":
                    print(self.tell_joke("Java"))
                else:
                    print(self.tell_joke("error"))
            elif question_category == 3:
                question = input("Do you like Chuck Norris? (y / n) ")
                if question == "y":
                    print(self.tell_joke("chuck"))
                else:
                    print(self.tell_joke("neutral"))
            hear_joke = input("Do you wanne hear a joke? (y / n) ")
        

    def tell_joke(self, category = None):
        """
        This function tells jokes. And can be used by the main program and the test_bot.
        The whole interaction with the user will be done seperately.

        Parameters
        ----------
        category : String, optional
            The category states the category, from which the joke shall be taken.
            In case None is given, the category will be drawn randomly.
            The default is None.

        Returns
        -------
        joke : string
            The joke, that I want to tell.

        """
        if category is None:
            category = random.choices(self.joke_categories)[0]
        joke = get_joke(self, category)
        return joke

    def rate_joke(self, joke):
        """
        Rate the given joke.

        Parameters
        ----------
        joke : string
            The given joke, that should be rated.

        Returns
        -------
        rating : float
            The rating of the bot.

        """
        rating = rate_joke(self.model, joke)
        return rating
    
if __name__ == "__main__":
    bot = Bot()
    bot.interactive_joking()