from textblob import TextBlob
import random


class Bot:
    name = 'The Laugh Generator'

    def __init__(self, joke_file='joke.txt'):
        self.jokes = self.read_jokes_from_file(joke_file)

    def read_jokes_from_file(self, file_name):
        jokes = []
        try:
            with open(file_name, 'r') as file:
                jokes = [line.strip() for line in file.readlines()]
        except FileNotFoundError:
            print(f"Jokes file '{file_name}' not found. Using default jokes.")
        return jokes

    def tell_joke(self):
        # Just tell a random joke from our list
        return random.choice(self.jokes)

    def rate_joke(self, joke):
        creativity = random.uniform(0, 1)  # Random creativity rating between 0 and 1
        timeliness = random.uniform(0, 1)  # Random timeliness rating between 0 and 1

        # Rate the joke based on its sentiment polarity
        blob = TextBlob(joke)
        polarity = blob.sentiment.polarity
        # Convert polarity from [-1, 1] to [1, 10] for a more positive range
        rating = (polarity + 1) * 5
        rating = min(10, max(1, rating))
        creativity_rating = (creativity + 1) * 5
        timeliness_rating = (timeliness + 1) * 5
        personalization_rating = self.personalize_rating()

        overall_rating = (rating + creativity_rating + timeliness_rating + personalization_rating) / 4

        # Ensure the rating is within the correct range
        return min(10, max(1, overall_rating))

    def personalize_rating(self):
        # Calculate a personalized rating based on user preferences
        # For simplicity, just return a random rating for demonstration
        return random.randint(1, 10)


# Main method for testing
if __name__ == "__main__":
    bot = Bot()

    # Generate and tell a joke
    joke = bot.tell_joke()
    print("Joke:", joke)

    # Rate the joke
    rating = bot.rate_joke(joke)
    print("Rating:", rating)