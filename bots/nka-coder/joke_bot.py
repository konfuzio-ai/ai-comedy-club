import importlib.util
import pandas as pd
from math import floor, ceil
import random
import os
from fuzzywuzzy import fuzz 
import spacy
import json
import re
import unidecode

class Bot:

    def __init__(self):
        bot_path = "bots/nka-coder/"
        self.name = "nka-coder"

        # creating the NLP pipeline for joke classication
        # json_data.json contains 100 training sample which is enought to obtain
        # a good accuracy in classificaton in a short training duration
        with open(bot_path+'training_data.json') as json_training_data:
            self.training_data = json.load(json_training_data)
        nlp = spacy.blank("en")
        nlp.add_pipe(
            "text_categorizer", 
            config={
                "data": self.training_data, 
                "model": "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
                "device": "cpu"
            }
        )
        self.model = nlp

        # Loading the list of jokes saved in long term memory
        with open(bot_path+"long_memory.json") as json_long_memory:
            self.long_memory = json.load(json_long_memory)

        # Initializing the list of joke to be used during the scene
        self.jokes = self.long_memory
            
        # Initializing short term memory for the scene
        self.short_memory = {}

    def tell_joke(self):
        # Choose the joke with highest score among the jokes in self.joke
        def choose_joke():
            score = 0
            for key in self.jokes.keys():
                if self.jokes[key]['score'] > score:
                    score = self.jokes[key]['score']
            joke_list = [key for key in self.jokes.keys() if self.jokes[key]['score']>=score-2]
            return random.choice(joke_list)
        
        # Just tell a random joke from our list 
        # making sure it is not yet registered in self.memory
        good_joke = False
        while not good_joke:
            smp = [j["processed_joke"] for j in self.short_memory.values() if "processed_joke" in j]
            joke = choose_joke()
            processed_joke = self.processing(joke)
            if processed_joke not in smp:
                good_joke = True 
        self.jokes.pop(joke)
        self.collect_feedback(joke)
        return joke

        
    def collect_feedback(self, joke):

        bots_dir = 'bots'
        bot_directories = [d for d in os.listdir(bots_dir) if os.path.isdir(os.path.join(bots_dir, d)) and d!='nka-coder']
        bots = []
        for bot_dir in bot_directories:
            # Dynamically load the bot's module
            spec = importlib.util.spec_from_file_location("bot", os.path.join(bots_dir, bot_dir, "joke_bot.py"))
            bot_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(bot_module)

            # Create an instance of the bot and add it to the list
            bot = bot_module.Bot()
            bots.append(bot)

        # Calculate te average score of the joke
        sum_score = 0
        number_score = 0
        for other_bot in bots:
            sum_score = sum_score + other_bot.rate_joke(joke)
            number_score+=1
        average_score = sum_score / number_score

        # Add submitted joke to short term memory
        processed_joke = self.processing(joke)
        self.short_memory[joke] = {
                                    "score" : average_score, 
                                    "initial score": False,
                                    "processed_joke":processed_joke
                                    }
        
        # Add and save short term memory jokes in long term memory jokes (long_memory.txt)
        with open(bots_dir+"/nka-coder/"+"long_memory.json", "w") as file:
            self.long_memory = {**self.long_memory, **self.short_memory}
            json.dump(self.long_memory, file)

        # Updating to NLP training data sample
        if average_score > 8 and joke not in self.training_data["1"]:
            del self.training_data["1"][0]
            self.training_data["1"].append(processed_joke)
        
    def rate_joke(self, joke):
        # This function detects humor in a sentences.
        # Sumbitted jokes longer than 150 characters are not considered being a joke.
        def detect_joke(joke):
            joke = self.processing(joke)
            res = self.model(joke)._.cats
            if res['1']<res['0'] or len(joke)>1000:
                return res['1']*10
            else:
                return 0

        # This function detect similarity between submitted joke and jokes in the memory.
        # Then it calculate a penalty based on the level of similarity.
        def penalty(joke):
            penalty = 0
            for key in self.short_memory.keys():
                temp = fuzz.token_set_ratio(joke, key)
                temp = -temp/(110-temp)
                if temp < penalty:
                    penalty = temp
            return penalty
        
        # If the submitted joke is a joke it gets 10 points then the penalty based on
        # similarities with jokes submitted earlier is applied.
        # if submitted joke is not a joke it get 0 point.
        rate = detect_joke(joke)
        if rate!=0:
            rate = rate + penalty(joke)
        self.collect_feedback(joke)
        return rate
    
    def processing(self, joke):
        data = pd.DataFrame([joke], columns=['text'])
        data = case_convert(data)
        data = remove_links(data)
        data = remove_shorthands(data)
        data = remove_accents(data)
        data = remove_specials(data)
        data = normalize_spaces(data)
        return data.text[0]
    

#Utilities functions

def case_convert(data):
    data.text = [i.lower() for i in data.text.values]
    return data

def remove_specials(data):
    data.text =  [re.sub(r"[^a-zA-Z]"," ",text) for text in data.text.values]
    return data

def remove_shorthands(data):
    CONTRACTION_MAP = {
    "ain't": "is not",
    "aren't": "are not",
    "can't": "cannot",
    "can't've": "cannot have",
    "'cause": "because",
    "could've": "could have",
    "couldn't": "could not",
    "couldn't've": "could not have",
    "didn't": "did not",
    "doesn't": "does not",
    "don't": "do not",
    "hadn't": "had not",
    "hadn't've": "had not have",
    "hasn't": "has not",
    "haven't": "have not",
    "he'd": "he would",
    "he'd've": "he would have",
    "he'll": "he will",
    "he'll've": "he he will have",
    "he's": "he is",
    "how'd": "how did",
    "how'd'y": "how do you",
    "how'll": "how will",
    "how's": "how is",
    "i'd": "i would",
    "i'd've": "i would have",
    "i'll": "i will",
    "i'll've": "i will have",
    "i'm": "i am",
    "i've": "i have",
    "isn't": "is not",
    "it'd": "it would",
    "it'd've": "it would have",
    "it'll": "it will",
    "it'll've": "it will have",
    "it's": "it is",
    "let's": "let us",
    "ma'am": "madam",
    "mayn't": "may not",
    "might've": "might have",
    "mightn't": "might not",
    "mightn't've": "might not have",
    "must've": "must have",
    "mustn't": "must not",
    "mustn't've": "must not have",
    "needn't": "need not",
    "needn't've": "need not have",
    "o'clock": "of the clock",
    "oughtn't": "ought not",
    "oughtn't've": "ought not have",
    "shan't": "shall not",
    "sha'n't": "shall not",
    "shan't've": "shall not have",
    "she'd": "she would",
    "she'd've": "she would have",
    "she'll": "she will",
    "she'll've": "she will have",
    "she's": "she is",
    "should've": "should have",
    "shouldn't": "should not",
    "shouldn't've": "should not have",
    "so've": "so have",
    "so's": "so as",
    "that'd": "that would",
    "that'd've": "that would have",
    "that's": "that is",
    "there'd": "there would",
    "there'd've": "there would have",
    "there's": "there is",
    "they'd": "they would",
    "they'd've": "they would have",
    "they'll": "they will",
    "they'll've": "they will have",
    "they're": "they are",
    "they've": "they have",
    "to've": "to have",
    "wasn't": "was not",
    "we'd": "we would",
    "we'd've": "we would have",
    "we'll": "we will",
    "we'll've": "we will have",
    "we're": "we are",
    "we've": "we have",
    "weren't": "were not",
    "what'll": "what will",
    "what'll've": "what will have",
    "what're": "what are",
    "what's": "what is",
    "what've": "what have",
    "when's": "when is",
    "when've": "when have",
    "where'd": "where did",
    "where's": "where is",
    "where've": "where have",
    "who'll": "who will",
    "who'll've": "who will have",
    "who's": "who is",
    "who've": "who have",
    "why's": "why is",
    "why've": "why have",
    "will've": "will have",
    "won't": "will not",
    "won't've": "will not have",
    "would've": "would have",
    "wouldn't": "would not",
    "wouldn't've": "would not have",
    "y'all": "you all",
    "y'all'd": "you all would",
    "y'all'd've": "you all would have",
    "y'all're": "you all are",
    "y'all've": "you all have",
    "you'd": "you would",
    "you'd've": "you would have",
    "you'll": "you will",
    "you'll've": "you will have",
    "you're": "you are",
    "you've": "you have"
    }
    texts = []
    for text in data.text.values:
        string = ""
        for word in text.split(" "):
            if word.strip() in list(CONTRACTION_MAP.keys()):
                string = string + " " + CONTRACTION_MAP[word]
            else:
                string = string + " " + word
        texts.append(string.strip())
    data.text = texts
    return data

#def remove_stopwords():
    #texts = []
    #stopwords_list = nltk.stopwords.words('english')
    #for item in data.text.values:
        #string = ""
        #for word in item.split(" "):
            #if word.strip() in stopwords_list:
                #continue
            #else:
                #string = string + " " + word
        #texts.append(string)
                
def remove_links(data):
    texts = []
    for text in data.text.values:
        remove_https = re.sub(r'http\S+', '', text)
        remove_com = re.sub(r"\ [A-Za-z]*\.com", " ", remove_https)
        texts.append(remove_com)
    data.text = texts
    return data

def remove_accents(data):
    data.text = [unidecode.unidecode(text) for text in data.text.values]
    return data

def normalize_spaces(data):
    data.text = [re.sub(r"\s+"," ",text) for text in data.text.values]
    return data
 
