import importlib.util
import pandas as pd
from textblob import TextBlob
import random
import os
from fuzzywuzzy import fuzz 
import spacy
import json
from utilities import category, processing
    

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
        self.joke_categories = set([val['category'] for val in self.long_memory.values()])

        # Initializing the list of joke to be used during the scene
        def convert(tup, di):
            di ={}
            for a, b in tup:
                di[a]=b
            return di
        tup = random.sample(self.long_memory.items(),1000)
        self.jokes ={}
        self.jokes  = convert(tup, self.jokes)
            
        # Initializing short term memory for the scene
        self.short_memory = {}

    def tell_joke(self, category="all"):
        # Choose the joke with highest score among the jokes in self.joke
        def choose_joke():
            """
            Choose a joke with one of the highest score and a specific category among the jokes in self.joke
            dictionnary
            """
            score = 0
            if category != "all":
                for key in self.jokes.keys():
                    if self.jokes[key]['score'] > score and self.jokes[key]['category'] == category:
                        score = self.jokes[key]['score']
                joke_list = [key for key in self.jokes.keys() if self.jokes[key]['score']>=score-2 and self.jokes[key]['category'] == category]
                if len(joke_list)!=0:
                    return random.choice(joke_list)
                else:
                    category_set = set([val['category'] for val in self.jokes.values()])
                    return "Damn, bro! Are you trying to corner me? Please, choose a joke's category among: {}".format(category_set)
            else:
                for key in self.jokes.keys():
                    if self.jokes[key]['score'] > score:
                        score = self.jokes[key]['score']
                joke_list = [key for key in self.jokes.keys() if self.jokes[key]['score']>=score-2]
                if len(joke_list)!=0:
                    return random.choice(joke_list)
                else:
                    category_set = set([val['category'] for val in self.jokes.values()])
                    return "Sorry, I can't find a joke about {} in my mind. What if I tell you a joke about one of these categories: {}".format(category,category_set)
        
        # Tell a random joke from our list taking in consideration the chosen category and the score.
        # At the same time, it make sure it is not yet registered in self.memory
        good_joke = False
        while not good_joke:
            smp = [j["processed_joke"] for j in self.short_memory.values() if "processed_joke" in j]
            joke = choose_joke()
            processed_joke = processing(joke)
            if processed_joke not in smp:
                good_joke = True 

        # Remove the returned joke from  self.joke dictionnary
        try:
            self.jokes.pop(joke)
        except:
            pass

        self.collect_feedback(joke)
        return joke

        
    def rate_joke(self, joke):
        
        def detect_joke(joke):
            """
            The function detect_joke() detects humor in a sentences or group of sentences.
            It return a rating based on probability that the submitted joke is a real joke and its polarity.
            Sumbitted jokes longer than 1000 characters are rated 0.
            """
            temp =joke
            if temp.replace(' ', '')[-1] not in ['.','?','!']:
                return 0

            joke = processing(joke)
            res = self.model(joke)._.cats

            if res['1']>res['0'] and len(joke)<1000:
                # A polarity coefficent of the submitted joke is calculated and added to the probability 
                # to obtain a rating
                blob = TextBlob(joke)
                polarity = 2.5 * blob.sentiment.polarity
                rate = 7.5 + polarity
                return round(rate,2)
            else:
                return 0

        def penalty(joke):
            """
            The function penalty() assesses similarities of the submitted joke with jokes in the short term memory.
            Then it calculates a penalty based on the maximum level of similarity detected.
            """
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
            rate = 0 if rate < 0 else rate
            rate = 10 if rate > 10 else rate
        # collect other bots feedback and save the joke if the rate of 
        # submited joke is > 0
        if rate > 0:
            self.collect_feedback(joke)
        return rate
    
    def collect_feedback(self, joke, rate = -1):
        """
        This function collect feedback (ratings) from all other bots participating 
        to the comedy scene
        """
        if rate != -1:
            # Add submitted joke to short term memory
            processed_joke = processing(joke)
            self.short_memory[joke] = {
                                    "score" : rate,
                                    "category": category(joke),
                                    "initial score": False,
                                    "processed_joke":processed_joke
                                    }
        
            # Add and save short term memory jokes in long term memory jokes (long_memory.txt)
            self.long_memory = {**self.long_memory, **self.short_memory}
            json_object = json.dumps(self.long_memory , indent=4)
            with open("bots/nka-coder/long_memory.json", "w") as file:
                file.write(json_object)

            # Updating to NLP training data sample
            if rate > 8 and joke not in self.training_data["1"]:
                del self.training_data["1"][0]
                self.training_data["1"].append(processed_joke)
                json_object = json.dumps(self.training_data , indent=4)
                with open("bots/nka-coder/training_data.json", "w") as file:
                    file.write(json_object)
        
        else:
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
            processed_joke = processing(joke)
            self.short_memory[joke] = {
                                    "score" : average_score,
                                    "category": category(joke),
                                    "initial score": False,
                                    "processed_joke":processed_joke
                                    }
        
            # Add and save short term memory jokes in long term memory jokes (long_memory.txt)
            self.long_memory = {**self.long_memory, **self.short_memory}
            json_object = json.dumps(self.long_memory , indent=4)
            with open("bots/nka-coder/long_memory.json", "w") as file:
                file.write(json_object)

            # Updating to NLP training data sample
            if average_score > 8 and joke not in self.training_data["1"]:
                del self.training_data["1"][0]
                self.training_data["1"].append(processed_joke)
                json_object = json.dumps(self.training_data , indent=4)
                with open("bots/nka-coder/training_data.json", "w") as file:
                    file.write(json_object)


if __name__ == '__main__':
    bot = Bot()
    joke = bot.tell_joke()
    print(joke)
    print(bot.rate_joke("How does a woman scare a gynecologist? by becoming a ventriloquist."))