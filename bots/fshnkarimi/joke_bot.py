from transformers import GPT2LMHeadModel, GPT2Tokenizer, pipeline

class Bot:
    def __init__(self):
        self.tokenizer = GPT2Tokenizer.from_pretrained("gpt2-medium")
        self.model = GPT2LMHeadModel.from_pretrained("gpt2-medium")
        self.classifier = pipeline("sentiment-analysis")
        self.user_mood = ""
        self.joke_preference = ""

    def ask_user(self):
        # Gather user mood and joke preferences
        moods = ['happy', 'sad', 'tired', 'amused', 'bored', 'curious', 'relaxed', 'stressed', 'anxious']
        joke_types = ['observational', 'anecdotal', 'situational', 'character', 'one-liner', 'ironic', 'deadpan', 'farcical', 'self-deprecating', 'slapstick']

        print("Choose a mood from the following options:", ", ".join(moods))
        self.user_mood = input().strip().lower()

        print("What type of joke are you in the mood for?", ", ".join(joke_types))
        self.joke_preference = input().strip().lower()

    def tailor_joke(self):
        # Use the mood to tailor the beginning of the prompt for GPT-2
        mood_based_prompts = {
            "happy": "Why did the cheerful",
            "sad": "Why was the sorrowful",
            "tired": "Why did the weary",
            "amused": "Why did the amused",
            "bored": "Why was the uninterested",
            "curious": "Why was the inquisitive",
            "relaxed": "Why did the laid-back",
            "stressed": "Why was the tense",
            "anxious": "Why did the nervous"
        }

        # Default prompt if the mood is not recognized
        prompt = mood_based_prompts.get(self.user_mood, "Why did the")

        # Incorporate joke type into the prompt
        joke_type_prompts = {
            "observational": " character observe that",
            "anecdotal": " character recall a funny event when",
            "situational": " character find themselves in a situation where",
            "character": " peculiar character once said",
            "one-liner": " character quickly remark",
            "ironic": " character find it ironic that",
            "deadpan": " character, with a monotone voice, state",
            "farcical": " character tell an exaggerated tale of",
            "self-deprecating": " self-conscious character humorously admit",
            "slapstick": " clumsy character, in a goofy scenario, accidentally"
        }

        # Append to the prompt based on joke type
        prompt += joke_type_prompts.get(self.joke_preference, " character say")

        # Generate joke based on tailored prompt
        input_ids = self.tokenizer.encode(prompt, return_tensors="pt")
        sample_output = self.model.generate(input_ids, do_sample=True, max_length=100, top_k=30, temperature=0.9)
        joke = self.tokenizer.decode(sample_output[0], skip_special_tokens=True)
        return joke


    def tell_joke(self):
        self.ask_user()
        return self.tailor_joke()

    def rate_joke(self, joke: str) -> int:
        # Setup sentiment analysis and content moderation pipelines
        sentiment_analyzer = pipeline("sentiment-analysis")
        content_moderator = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

        # 1. Humor Rating
        sentiment = sentiment_analyzer(joke)[0]
        humor_score = 5 if sentiment['label'] == 'POSITIVE' and sentiment['score'] > 0.5 else 3

        # 2. Current events or popular culture awareness
        current_events = ["chatgpt", "woman", "life", "freedom", "apple", "netflix"]  
        awareness_score = 2 if any(term in joke for term in current_events) else 0

        # 3. Content appropriateness
        categories = ["offensive", "racist", "sexist", "inappropriate"]
        moderation_results = content_moderator(joke, categories)
        inappropriate_score = -5 if any(score > 0.5 for score in moderation_results['scores']) else 0

        # 4. Delivery effectiveness (A very simplistic approach)
        delivery_score = 2 if 20 < len(joke.split()) < 50 else 0

        # Aggregating the scores
        total_score = humor_score + awareness_score + inappropriate_score + delivery_score
        total_score = max(1, min(10, total_score))  # Ensure score is between 1 and 10

        return total_score
    
    # def rate_joke(self, joke: str):
    #     sentiment = self.classifier(joke)[0]
    #     if sentiment["label"] == "POSITIVE":
    #         rating = max(1, min(10, int(5 + (sentiment["score"] * 5))))
    #     else:
    #         rating = max(1, min(10, int(5 - (sentiment["score"] * 5))))
    #     return rating


bot = Bot()
joke = bot.tell_joke()
rating = bot.rate_joke(joke)
print("joke: ", joke)
print("rating: ", rating)