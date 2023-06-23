import random

class Bot:
    name = 'Not funny'
    def __init__(self):
        self.jokes = [
            "Why don't scientists trust atoms? Because they make up everything!",
            "Why did the chicken go to the seance? To talk to the other side!",
            "Why don't we tell secrets on a farm? Because the potatoes have eyes, the corn has ears, and the beans stalk.",
            "I would tell you a joke about time travel, but you didn't like it.",
            "Why don't programmers like nature? It has too many bugs.",
            "Why do programmers always mix up Christmas and Halloween? Because Oct 31 == Dec 25!",
            "Why do programmers prefer iOS development? It's less Java to spill.",
            "Why did the programmer go broke? Because he used up all his cache.",
            "Why did the programmer get kicked out of school? Because he kept breaking the class.",
            "Why did the programmer go on a diet? He had too many bytes.",
            "Why do programmers prefer dark mode? Because light attracts bugs.",
            "Why was the computer cold? It left its Windows open.",
            "Why did the web developer go broke? Because he didn't get enough cache.",
            "Why did the programmer refuse to play cards with the jungle cat? Because he was afraid of Cheetahs.",
            "Why was the developer unhappy at their job? They wanted arrays."
        ]

    def tell_joke(self):
        # Just tell a random joke from our list
        return random.choice(self.jokes)

    def rate_joke(self, joke):
        # Rate the joke based on its length
        # The shorter the joke, the higher the rating
        # This is just a simple example and doesn't actually reflect humor
        length = len(joke)
        if length < 50:
            return 10
        elif length < 80:
            return 7
        else:
            return 5
