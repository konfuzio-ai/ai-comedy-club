from abc import ABC, abstractmethod


class BaseBot(ABC):
    name: str

    @abstractmethod
    def tell_joke(self) -> str:
        pass

    @abstractmethod
    def rate_joke(self, joke: str) -> int:
        pass
