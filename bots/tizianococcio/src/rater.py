from abc import ABC, abstractmethod
from typing import List

class JokeRaterInterface(ABC):
    """ 
    This is an abstract base class (ABC) that serves as an interface for joke rating classes.
    It enforces the implementation of the rate_joke() method in any subclass.
    """
    
    @abstractmethod
    def rate_joke(self, joke: str) -> float:
        """
        An abstract method that will rate a joke. Should be implemented by subclasses.

        :param joke: The joke to be rated, as a string.
        :return: The rating of the joke, as a float.
        """
        pass


class Rater:
    """
    This class aggregates multiple joke raters. Each joke rater must be an instance of a subclass
    of JokeRaterInterface. The final rating is a weighted average of the ratings from each rater.
    """
    def __init__(self):
        """
        Initializes the Rater class. Two lists are initialized to store the joke raters and their
        respective weights.
        """
        self.joke_raters: List[JokeRaterInterface] = []
        self.weights: List[float] = []
        self.total_weight: float = 0

    def add_rater(self, joke_rater: JokeRaterInterface, weight: float = None) -> None:
        """
        Adds a joke rater to the list of raters, with an associated weight. If no weight is
        provided, a uniform weight of 1 is assigned.

        :param joke_rater: An instance of a subclass of JokeRaterInterface.
        :param weight: The weight assigned to the rater's ratings, as a float. Defaults to 1 if not provided.
        :return: None
        """
        assert isinstance(joke_rater, JokeRaterInterface), "joke_rater must implement JokeRaterInterface"
        if weight is None:
            weight = 1
        self.joke_raters.append(joke_rater)
        self.weights.append(weight)
        self.total_weight += weight

        # Normalize the weights to sum to 1
        self.weights_norm = [w / self.total_weight for w in self.weights]

    def get_rating(self, joke: str) -> int:
        """
        Computes the final rating of a joke by taking a weighted average of the ratings from each
        rater.

        :param joke: The joke to be rated, as a string.
        :return: The final rating of the joke.
        """
        rating = 0
        for rater, weight in zip(self.joke_raters, self.weights_norm):
            rating += rater.rate_joke(joke) * weight
        return round(rating)
