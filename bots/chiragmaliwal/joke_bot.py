import torch
import random
import logging
from transformers import GPT2Tokenizer, GPT2LMHeadModel
from textblob import TextBlob

class Bot:
    def __init__(self):
        self.tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
        self.model = GPT2LMHeadModel.from_pretrained('gpt2')
        self.joke_prefixes = ["Why did the chicken cross the road?", "Knock, knock.", "Why was the computer cold?"]
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        logging.basicConfig(filename='joke_bot.log', level=logging.INFO)
        
    def generate_joke(self, prefix, max_length=500):
        if not isinstance(prefix, str) or not isinstance(max_length, int):
            logging.error("Invalid input type")
            return None
        if max_length <= 0:
            logging.error("Invalid input: max_length should be positive")
            return None

        input_ids = self.tokenizer.encode(prefix, return_tensors='pt').to(self.device)
        with torch.no_grad():
            joke_ids = self.model.generate(input_ids, max_length=max_length, do_sample=True, 
                                           pad_token_id=50256, 
                                           attention_mask=torch.ones(input_ids.shape).to(self.device))
        joke = self.tokenizer.decode(joke_ids[0], skip_special_tokens=True)
        return joke

    def tell_joke(self):
        prefix = random.choice(self.joke_prefixes)
        return self.generate_joke(prefix)

    def rate_joke(self, joke):
        if not isinstance(joke, str):
            logging.error("Invalid input type")
            return None
        
        # Determine sentiment polarity of the joke (-1.0 to 1.0)
        sentiment = TextBlob(joke).sentiment.polarity
        
        # Rate the joke based on its length and sentiment
        length = len(joke)
        if length < 50 and sentiment > 0:
            rating = 10
        elif length < 100 and sentiment > -0.1:
            rating = 7
        else:
            rating = 5
        return rating
