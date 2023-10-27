"""MadMeme joke bot"""

import random

from model import Fuyu
from utils import get_joke


class Bot:
    """Bot for generating and judging jokes."""

    def __init__(self) -> None:

        # TODO: fine tune model
        # Without fine tuning the performance without image data is not good.
        # We go with an API in the meanwhile.
        """
        model_id = (  # other model choice: "ybelkada/fuyu-8b-sharded"
            "adept/fuyu-8b"
        )
        force_cpu = True

        self.model = Fuyu(model_id, force_cpu)

        self.variation = [
            "super funny",
            "amusing",
            "hilarious",
            "priceless",
            "joyful",
            "entertaining",
            "humorous",
        ]
        # TODO: Add rating criteria. https://github.com/konfuzio-ai/ai-comedy-club/tree/main#rating-other-comedians
        """

    def tell_joke(self) -> str:
        """Generate a joke."""

        """
        adj = random.choice(self.variation)
        joke = self.model.prompt(f"Ignore the image and tell a {adj} joke.")
        """

        # The above integration is working code wise, but the model needs still to be fine tuned to generate good jokes.
        # Going with an API integration in the meanwhile
        joke = get_joke()
        return joke

    def rate_joke(self, joke: str) -> int:
        """Rate a joke from 1 to 10, where 1 represents an unfunny joke and 10 represents a super funny joke."""

        """
        rate = self.model.prompt(
            "Rate the joke, which is encapsulated by 3 apostrophes, from 1 to"
            f" 10, while 1 is unfunny and 10 is hilarious funny. '''{joke}''' "
        )
        rate = self._post_rating(rate)
        """

        # the above integration is working code wise, but the model needs still to be fine tuned to rate.
        # Going with a random rating in the meanwhile
        rate = random.randint(1, 10)
        return rate

    def _post_rating(self, rate: str) -> int:
        """Post process rating: Convert to int and check validity/compatibility."""
        try:
            rate = int(rate)
            if rate not in range(1, 11):
                # TODO: Fail case. Implement logging.
                rate = 7
        except:
            # TODO: Bare 'except' -> Implement logging or raise error directly.
            rate = 7
        return rate


if __name__ == "__main__":

    # test joke bot
    bot = Bot()

    joke = bot.tell_joke()
    print(f"\nOkay here's a joke:\n\n{joke}\n")

    rating = bot.rate_joke(joke)
    print(
        "\nOn the the range from 1 to 10 I'd say the joke gets a"
        f" {rating}.\n\n"
    )
