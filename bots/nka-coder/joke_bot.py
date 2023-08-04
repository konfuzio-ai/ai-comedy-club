import importlib.util
import random
import os
import subprocess
import json
import ast 

class Bot:
    def __init__(self):

        self.name = "nka-coder"
        f = open("bots"+"/nka-coder/"+"long_memory.txt", "r")

        self.long_memory = ast.literal_eval(f.read())
        print(len(list(self.long_memory.keys())))

        if list(self.long_memory.keys()) != []:
            self.jokes = self.long_memory
        else:
            self.jokes = {"Why don't scientists trust atoms? Because they make up everything!":
                          {'score': 10, 'type': 'middle', 'category': 'no style'}}

        self.short_memory = {}

    def tell_joke(self):
        # Just tell a random joke from our list 
        # making sure it is not yet registered in self.memory

        joke = self.choose_joke()
        good_joke = False
        while not good_joke:
            if joke not in list(self.short_memory.keys()):
                joke = self.choose_joke()
                good_joke = True 
        self.jokes.pop(joke)
        self.collect_feedback(joke)
        return joke

    # Choose the joke with highest score among the jokes in self.joke
    def choose_joke(self):
        joke = ''
        score = 0
        for key in self.jokes.keys():
            if self.jokes[key]['score'] > score:
                joke = key
                score = self.jokes[key]['score']
        
        return joke
        

    def rate_joke(self, joke):
        # Rate the joke based on its length
        # The shorter the joke, the higher the rating
        # This is just a simple example and doesn't actually reflect humor
        length = len(joke)
        if joke in self.short_memory.keys():
            rate = 0
        elif length < 50:
            rate = 10
        elif length < 80:
            rate = 7
        else:
            rate = 5
        
        self.collect_feedback(joke)

        return rate
        
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


        # Add joke to short term memory
        self.short_memory[joke] = {"score" : average_score, "type" : self.joke_type(joke),
                             "category" : self.joke_style(joke)}
        
        # Add save short term memory jokes in long term memory jokes (long_memory.txt)
        f = open(bots_dir+"/nka-coder/"+"long_memory.txt", "w")
        self.long_memory = {**self.long_memory, **self.short_memory}
        f.write(str(self.long_memory))
        f.close()

    def joke_style(self, joke):
        joke=0
        return "no style"
    
    def joke_type(self, joke):
        length = len(joke)
        if length < 50:
            return "short"
        elif length < 80:
            return "middle"
        else:
            return "long"    