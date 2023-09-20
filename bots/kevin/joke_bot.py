import random
import requests
from transformers import BertForSequenceClassification, BertTokenizer
import torch
class Bot:
    name = 'KevinBot'
    def __init__(self):

        self.jokes = ["Why don't scientists trust atoms? Because they make up everything!"]


    def tell_joke(self):
        return self.fetch_joke_from_api()

    def rate_joke(self, joke):
        self.model = BertForSequenceClassification.from_pretrained('bert-base-uncased')
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

        inputs = self.tokenizer(joke, return_tensors="pt", padding=True, truncation=True)

        # Get the model's prediction
        with torch.no_grad():
            logits = self.model(**inputs).logits
        probs = torch.nn.functional.softmax(logits, dim=-1)
        positive_rating = probs[0][1].item()
        scaled_rating = round(positive_rating * 10)

        return scaled_rating
        
    def fetch_joke_from_api(self):
        # Fetch a joke from JokeAPI
        url = "https://v2.jokeapi.dev/joke/Any?blacklistFlags=nsfw,religious,political,racist,sexist,explicit"
        response = requests.get(url)
        data = response.json()
        if data['type'] == 'twopart':
            joke_setup = data['setup']
            joke_delivery = data['delivery']
            joke = f"{joke_setup}\n{joke_delivery}"
        else:
            joke = data['joke']
        return joke

