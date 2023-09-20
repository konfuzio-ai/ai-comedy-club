
from abc import ABC, abstractmethod
from enum import Enum


class Topic(Enum):
    ANIMALS = "animals"
    SPORTS = "sports"
    POLITICS = "politics"
    WORK = "work"
    PROGRAMMING = "programming"
    RELATIONSHIPS = "relationships"
    RELIGION = "religion"
    ECONOMY = "economy"
    BLONDES = "blondes"


# I am using this ABC only for my bot and I dont touch any code in the default/provided bots,
# but ideally they should inherit from it, too.
class AbstractBot(ABC):
    """Abstract Base Class for Bot interface"""

    @abstractmethod
    def tell_joke(self) -> str:
        pass

    @abstractmethod
    def rate_joke(self, joke: str) -> str:
        pass
