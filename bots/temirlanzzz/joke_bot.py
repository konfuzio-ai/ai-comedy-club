from transformers import pipeline
import random

class Bot:

    humor: str = random.choice(["Funny", "Boring", "Hallarious", "Strange"])
    creativity: str = random.choice(["Unique", "Common", "Rare"])
    timeliness:  str = random.choice(["Old", "New"])
    comedian:  str = random.choice(["Patrice O'Neal", "Kevin Hart", "Tig Notaro", "Chris Rock", "Dave Chappelle", "Louis C. K."])
    audience:  str = random.choice(["everyone", "old people", "kids", "teens", "middle age people"])
    model = pipeline('text-generation', model='gpt2')
    
    def tell_joke(self) -> str:
        promt = "Tell a joke that is "+ self.humor + " " + self.creativity + " " + self.timeliness + " for "+ self.audience + " in style of "+self.comedian 
        return self.model(
            f'{promt}',
            max_length=30,
            do_sample=True)[0]['generated_text']
    
    def rate_joke(self, joke) -> int:
        promt = "Rate the following joke from 0 to 10:" + joke
        rating = self.model(
            f'{promt}',
            max_length=30,
            do_sample=True)[0]['generated_text']
        return [int(x) for x in rating.split() if x.isdigit()][0]