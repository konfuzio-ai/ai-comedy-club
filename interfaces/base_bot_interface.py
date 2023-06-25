from abc import ABC, abstractmethod


class BaseBot(ABC):
    name: str

    @abstractmethod
    def tell_joke(self) -> str:
        """
        This method should generate and return a string containing a joke.
        """
        pass

    @abstractmethod
    def rate_joke(self, joke: str) -> int:
        """
        This method should take a string (representing the joke to be rated) and return an integer from 1 to 10, which
        represents the rating of the joke.
        """
        pass
