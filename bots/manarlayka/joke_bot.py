class Bot:
    def __init__(self):
        self.humor_threshold = 5 
        self.creativity_factor = 0.7 
        self.personalization_factor = 0.3

    def tell_joke(self):
        joke = "There are 10 types of people in the world. Those who understand binary and those who don't."
        return joke

    def rate_joke(self, joke, user_preferences=None):
        joke_rating = 0
        if "binary" in joke:
            joke_rating += 1  # Considered mildly funny

        joke_rating += self.creativity_factor  # Add creativity factor to rating

        if user_preferences:
            if "puns" in user_preferences:
                joke_rating += self.personalization_factor  # Add personalization factor if user prefers puns

        if joke_rating < self.humor_threshold:
            joke_rating = 1  # Not funny

        return joke_rating
