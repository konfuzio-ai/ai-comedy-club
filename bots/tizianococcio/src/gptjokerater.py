from src.rater import JokeRaterInterface

class GPTJokeRater(JokeRaterInterface):
    def rate_joke(self, joke):
        # For demonstration purposes, this returns a constant
        return 2