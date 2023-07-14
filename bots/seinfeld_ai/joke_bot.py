import random
from transformers import pipeline
from textblob import TextBlob

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
        
        self.starting_strings = {
            0: "You ever notice how",
            1: "What's the deal with",
            2: "Have you ever wondered why",
            3: "So, I was thinking about",
            4: "Why do they always",
            5: "I don't understand why",
            6: "You know what really bugs me?",
            7: "Why is it that every time",
            8: "You know those things that just make no sense? Like",
            9: "I was at this place the other day, and let me tell you, it was like"
        }
        
        self.joke_generator = pipeline('text-generation', model='lposilovic/Seinfeld_gpt2')
        
        print(hello_string[random.randint(0, len(hello_string)-1)])

    def generate(self, length=None):
        
        starting_idx = random.randint(0, len(self.starting_strings)-1)
        joke = self.starting_strings[starting_idx]
        if not length:
            length = random.randint(200,300)
        
        joke = self.joke_generator(joke, max_length=length, do_sample=False)[0]['generated_text']
        
        return joke


class RateJokes():
    """
    The class for rating jokes.
    """
    
    def __init__(self, min_score=1, max_score=10, integer=True) -> None:
        self.min_score = min_score
        self.max_score = max_score
  
    def rate(self, joke):
        
        
        blob = TextBlob(joke)
        polarity = blob.sentiment.polarity
        rating = (polarity + 1) * 5
        
        return int(rating)


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