import random
from transformers import pipeline
from textblob import TextBlob
from difflib import SequenceMatcher

class SeinfeldAI:    
    """
    The class for generating new Seinfeld style jokes.
    """
    
    def __init__(self) -> None:
        
        hello_string = {
            0: "Hi, I'm a Seinfeld bot, trying to be as funny as my idol, let me tell you a joke!",
            1: "Hey there, I'm Jerry Seinfeld, the master of observational comedy!",
            2: "What's the deal? It's Jerry Seinfeld, your resident funnyman!",
            3: "Welcome to the virtual stage, folks! I'm Jerry Seinfeld, your comedy companion.",
            4: "In a world full of ordinary bots, I'm Jerry Seinfeld, bringing you extraordinary humor!",
            5: "Knock, knock! It's Jerry Seinfeld, here to deliver jokes that'll have you rolling.",
            6: "They say laughter is the best medicine, so allow me, Jerry Seinfeld, to be your comedic doctor!",
            7: "Hey, funny bones! Jerry Seinfeld at your service, ready to tickle your funny bone.",
            8: "Get ready to laugh, because I'm Jerry Seinfeld, the chatbot that guarantees a comedic punchline!",
            9: "Buckle up, chat enthusiasts! I'm Jerry Seinfeld, here to entertain you with my witty banter and sharp humor!"
            }
        
        # Standard begginings of the Seinfeld jokes
        self.starting_strings = {
            0: "You ever notice how",
            1: "What's the deal with",
            2: "Have you ever wondered why",
            3: "So, I was thinking about",
            4: "Why do they always",
            5: "I don't understand why",
            6: "I find it funny how",
            7: "Why is it that every time",
            8: "You know those things that just make no sense? Like",
            9: "I was at this place the other day, and let me tell you, it was like"
        }
        
        # Downloading and loading a custom trained model
        self.joke_generator = pipeline('text-generation', model='lposilovic/Seinfeld_gpt2')
        
        # Saying hello to the crowd
        print()
        print(hello_string[random.randint(0, len(hello_string)-1)])

    def generate(self, max_length=None):
        
        starting_idx = random.randint(0, len(self.starting_strings)-1)
        joke = self.starting_strings[starting_idx]
        if not max_length:
            max_length = random.randint(100,400)
        
        joke = self.joke_generator(joke, max_length=max_length, do_sample=False)[0]['generated_text']
        
        return joke


class RateJokes():
    """
    The class for rating jokes.
    """
    
    def __init__(self, max_score=10, integer_score=True, cache_size=5) -> None:
        
        # Defining the score range (1-10 or 1-5), score dtype and cache size
        self.max_score = max_score
        self.integer_score = integer_score
        self.cache_size = cache_size
        
        # Hardcoded values for the weights of each joke evaluation category. Here for future upgrades.
        self.sentiment_weight = 3
        self.originality_weight = 2
        self.humor_weight = 5
        
        # Loading models for rating 
        self.pipeline_sentiment = pipeline(model="lvwerra/distilbert-imdb")
        self.pipeline_humor = pipeline(model="mohameddhiab/humor-no-humor")
        
        self.fifo = []
  
    def rate(self, joke):
        
        # Let's see if it the general feeling is positive
        result = self.pipeline_sentiment(joke)
        sentiment = 0
        for s in result:
            if s["label"] == "POSITIVE":
                sentiment = result[0]["score"]

        # Did we already hear this joke?
        original = 0
        original_max = 0
        for last_joke in self.fifo:
            original = SequenceMatcher(None, last_joke, joke).ratio()
            original = max(original, original_max)
        if len(self.fifo) >= self.cache_size:
            self.fifo.pop(0)
        self.fifo.append(joke)
        
        # Let's evaluate the humor
        result = self.pipeline_humor(joke)
        humor = 0
        for s in result:
            if s["label"] == "HUMOR":
                humor = result[0]["score"]
        
        print("How positive is it: ", sentiment)
        print("Did I hear this one already?", original)
        print("Is this funny?", humor)
        
        if self.integer_score:
            rating = round(sentiment*self.sentiment_weight) + round((1 - original)*self.originality_weight) + round(humor*self.humor_weight)
            rating = round(rating/10 * self.max_score)
        else:
            rating = sentiment*self.sentiment_weight + (1 - original)*self.originality_weight + humor*self.humor_weight
            rating = rating/10 * self.max_score
            
        return rating


class Bot:
    
    """
    A comedic Seinfeld bot class that generates jokes and rates other jokes.
    """
    
    def __init__(self) -> None:
        self.joker = SeinfeldAI()
        self.rater = RateJokes()
        
        pass
    
    def tell_joke(self):
        
        return self.joker.generate()
    
    def rate_joke(self, joke):
        
        return self.rater.rate(joke)