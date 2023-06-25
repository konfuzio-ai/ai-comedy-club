from interfaces.base_bot_interface import BaseBot
from transformers import pipeline


class Bot(BaseBot):
    name = "Jokeptimus Prime"

    def __init__(self, comedian_model: str = None, critic_model: str = None):

        if comedian_model is not None:
            self.comedian = pipeline(model=comedian_model)
        else:
            self.comedian = pipeline(model="huggingtweets/jokesofthedaydn")

        if critic_model is not None:
            self.critic = pipeline(model=critic_model)
        else:
            self.critic = pipeline(model="mohameddhiab/humor-no-humor")

    def tell_joke(self) -> str:
        return self.comedian("Joke: ")[0]['generated_text'].strip("Joke: ")

    def rate_joke(self, joke: str) -> int:
        res = self.critic(joke)
        if res[0]['label'] == 'HUMOR':
            score = res[0]['score']

            return round(score * 10)

        return 0


if __name__ == "__main__":

    bot = Bot()

    print(bot.rate_joke("Why couldn't the bicycle stand up by itself? Because it was two-tired!"))
    print(bot.rate_joke("Not a joke"))
    print(bot.tell_joke())
