from sentence_transformers import SentenceTransformer, util


class JudgeBot:
    def __init__(self):
        self.jokes = list()
        self.current_comedian_jokes = list()
        self.current_joke_rating = 0
        self.sentence_transformer_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        # I would love to use current news from any API, but they are not available without api key
        self.trending_topics = ["Usage of chatgpt", "Artificial intelligence", "Inflation rates", "War", "World war"]
        self.judgement_similarity_criteria = ["Diversity of Jokes", "Creativity", "Timeliness", "Personalization"]
        self.users_preferences_and_geography = []

    def get_users_preferences_and_geography(self, users_preference: list[str], geography: list[str]

                                            ):
        self.users_preferences_and_geography += users_preference
        self.users_preferences_and_geography += geography

    def rate_joke(self, current_joke):
        self.current_joke_rating = 0
        if len(current_joke) > 1000:
            # This joke is too long
            self.current_joke_rating -= 1

        # I wish I would have found a LLM that can rate jokes base on humor

        for similarity_criteria in self.judgement_similarity_criteria:
            self._rate_with_similarity(current_joke, similarity_criteria)
        # I would use a simple function that append only if it is not yet in the list
        self.jokes.append(current_joke)
        self.current_joke_rating = max(0, min(10, self.current_joke_rating))  # To ensure the rating is between 0 and 10
        return self.current_joke_rating
    def _rate_with_similarity(self, current_joke, judgement_criteria):

        # I could use match case to better readability, but I don't know if you are using python >=3.10
        # I do this to avoid writing the same loop in 3 different methods
        is_negative_similarity = True
        if judgement_criteria == "Diversity of Jokes":
            list_to_compare_with = self.current_comedian_jokes
        elif judgement_criteria == "Creativity":
            list_to_compare_with = self.jokes
        elif judgement_criteria == "Timeliness":
            list_to_compare_with = self.trending_topics
            is_negative_similarity = False
        elif judgement_criteria == "Personalization":
            list_to_compare_with = self.users_preferences_and_geography
            is_negative_similarity = False
        else:
            list_to_compare_with = list()

        current_joke_embedding = self.sentence_transformer_model.encode(current_joke, convert_to_tensor=True)
        for sentence in list_to_compare_with:
            sentence_embedding = self.sentence_transformer_model.encode(sentence, convert_to_tensor=True)
            similarity = util.pytorch_cos_sim(current_joke_embedding, sentence_embedding)
            if similarity > 0.3:
                if is_negative_similarity:
                    self.current_joke_rating -= 2 * is_negative_similarity
                    break  # found similarity with previous jokes (from the same comedian or from all jokes)
                else:
                    self.current_joke_rating += 2  # Found similarity with a trending topic or personalization
                    # The loop doesn't break, we can get more points if we combine them
        self.current_joke_rating += 2 * is_negative_similarity  # Not found similarity with any previous jokes

    def finish_this_comedian_judgement(self):
        self.current_comedian_jokes = list()  # remove jokes to start with next comedian


if __name__ == "__main__":
    bot = JudgeBot()
    bot.get_users_preferences_and_geography(["questions", "scientist"], ["Madrid", "Berlin"])
    joke = "Why don't scientists trust atoms? Because they make up everything!"
    bot.rate_joke(joke)
    print(bot.current_joke_rating)
