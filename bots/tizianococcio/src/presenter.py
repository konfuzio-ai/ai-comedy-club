from src.languageutils import LanguageUtils
from src.botinterface import BotInterface
from abc import ABC, abstractmethod
import time

class PresenterInterface(ABC):
    """
    This is an abstract base class (ABC) that serves as an interface for presenter classes.
    It enforces the implementation of the play() method in any subclass.
    """
    def __init__(self):
        self.bot = BotInterface()
        self.language_utils = LanguageUtils()
        self.lm = self.bot.load_lm()
        self.rater = self.bot.load_joke_rater()

    @abstractmethod
    def play(self):
        """
        An abstract method that runs the ai comedian. Should be implemented by subclasses.
        """
        pass

    def rate_joke(self, joke: str) -> int:
        """
        Rate a joke.

        Args:
            joke: A string containing the joke to be rated.

        Returns:
            An integer between 1 and 10, inclusive, representing the rating of the joke.
        """
        return self.rater.rate_joke(joke)

class NaivePresenter(PresenterInterface):
    """
    Basic presenter.
    """

    def ask_for_input(self) -> tuple:
        # Ask the user for their preferred joke style and mood
        style = input("Please enter your preferred joke style (puns, tech, sports, etc...): ")
        mood = input("Please enter your preferred mood (happy, sad, etc...): ")

        # Return the user's inputs
        return style, mood

    def generate_joke(self, style: str, mood: str):
        # Generate a joke
        joke = self.lm.generate(style, mood)

        return joke

    def play(self):

        while True:
            # Ask the user for their inputs
            style, mood = self.ask_for_input()

            # Get the most similar style and mood from the bot's list of styles and moods
            style = self.language_utils.get_most_similar_word(style, self.bot.load_styles())
            mood = self.language_utils.get_most_similar_word(mood, self.bot.load_moods())

            # Generate a joke based on the user's inputs
            joke = self.generate_joke(style, mood)

            # Print the generated joke
            print(f"\n{joke}\n")


class NarcissusPresenter(PresenterInterface):

    def generate_joke(self, style: str, mood: str):
        # Generate a joke
        joke = self.lm.generate(style, mood)

        return joke

    def play(self):

        while True:
            # Generate a joke
            joke = self.generate_joke()

            # Print the generated joke
            print(f"\n{joke}\n")

            # wait 5 seconds
            time.sleep(5)