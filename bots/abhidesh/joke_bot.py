import random

class Bot:
    def __init__(self):
        self.joke_templates = [
            "Why did the {animal} {action}? Because {reason}!",
            "Why don't eggs tell jokes? Because they might crack up.",
            "Why do programmers prefer dark mode? Because light attracts bugs.",
        ]

    def tell_joke(self):
        return self.generate_joke()

    def rate_joke(self, joke):
        return self.generate_rating()

    def generate_joke(self):
        animal = random.choice(["donkey", "frog", "elephant", "monkey"])
        action = random.choice(["dance", "sing", "jump", "sleep"])
        reason = random.choice(["it was fun", "it was hungry", "it was bored"])
        return random.choice(self.joke_templates).format(animal=animal, action=action, reason=reason)

    def generate_rating(self):
        return random.randint(1, 10)

if __name__ == "__main__":
    bot = Bot()

    joke_to_tell = bot.tell_joke()
    print("Bot's Joke:", joke_to_tell)

    joke_to_rate = "Why did the chicken cross the road? To get to the other side!"
    rating = bot.rate_joke(joke_to_rate)
    print("Rating for the Joke:", rating)
