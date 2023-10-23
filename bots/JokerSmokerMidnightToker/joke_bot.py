import random

class Bot:
    def __init__(self):
        self.jokes = [
            "Why don't scientists trust atoms? Because they make up everything!",
            "Why did the chicken go to the seance? To talk to the other side.",
            "Why don't some animals play cards? Because they're afraid of cheetahs.",
            "What do you call fake spaghetti? An impasta!",
            "Why did the scarecrow win an award? Because he was outstanding in his field!"
        ]

    def tell_joke(self):
        return random.choice(self.jokes)

    def rate_joke(self, joke):
        # Rate the joke based on its length, up to a maximum of 10
        return min(len(joke) // 10, 10)