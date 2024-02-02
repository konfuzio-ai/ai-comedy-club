import json
from datetime import datetime
from better_profanity import profanity
from pathlib import Path
from random import randint, choice
from time import sleep
from numpy import mean
import re
from transformers import pipeline
from sentence_transformers import SentenceTransformer, util
from sys import exit

jokesFilePath = Path(__file__).with_name("jokes.json")
retortsFilePath = Path(__file__).with_name("retorts.json")
whosTherePattern = re.compile(r'\bwho(\'?s)? there\b', re.IGNORECASE)
jokeGenerator = pipeline("text-generation", model="gpt2")
classifier = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
comparationModel = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

        
class Bot:
    def __init__(self):
        self.jokes = json.load(open(jokesFilePath, "r"))
        self.retorts = json.load(open(retortsFilePath, "r"))
        self.knockKnockRetorts = [self.retorts[i]["Retort"] for i in range(0, len(self.retorts)) if self.retorts[i]["Type"] == "Knock Knock"]
        self.positiveRetorts = [self.retorts[i]["Retort"] for i in range(0, len(self.retorts)) if self.retorts[i]["Type"] == "Positive"]
        self.negativeRetorts = [self.retorts[i]["Retort"] for i in range(0, len(self.retorts)) if self.retorts[i]["Type"] == "Negative"]
        self.incorrectRatingRetorts = [self.retorts[i]["Retort"] for i in range(0, len(self.retorts)) if self.retorts[i]["Type"] == "Incorrect rating"]
        self.toldJokes = []
        self.jokeCount = -1
        
        
    def tell_joke(self, category=""):

        if not category:
            index = randint(0, len(self.jokes)-1)

            print(self.jokes[index]["setup"])
            sleep(mean(self.jokes[index]["wait"]))
            print(self.jokes[index]["punchline"])
            self.toldJokes.append(self.jokes[index])
            self.jokes.remove(self.jokes[index])
            self.jokeCount += 1

        else:
            if category.lower() == "generate":
                print("I will generate a joke for you. Please bear with me as I do this.")
                allJokes = self.jokes + self.toldJokes
                index = randint(0, len(allJokes)-1)
                randomSetup = allJokes[index]["setup"]
                
                prompt = f"An example of a joke setup is: {randomSetup} Another example of a setup is: "

                generatedResponse = jokeGenerator(prompt, num_return_sequences=1, max_length=50, return_text=True, pad_token_id=jokeGenerator.tokenizer.eos_token_id)
                
                generatedText = generatedResponse[0]["generated_text"]
                generatedSetup = generatedText[generatedText.rfind(": ") + 2:]

                generatedResponse = jokeGenerator(f"An example of how to finish the joke setup {generatedSetup} is : ", num_return_sequences=1, max_length=50, return_text=True, pad_token_id=jokeGenerator.tokenizer.eos_token_id)
                generatedText = generatedResponse[0]["generated_text"]
                generatedPunchline = generatedText[generatedText.rfind(": ") + 2:]

                print(generatedSetup)
                sleep(3)
                print(generatedPunchline)

                return

            requestedJokes = [self.jokes[i] for i in range(0, len(self.jokes)) if self.jokes[i]["category"].lower() == category.lower()]

            if not requestedJokes:
                print("I'm sorry, I haven't learned any {category} jokes yet. I'll let you add some before you leave if you want! In the meantime here's another joke!".format(category=category))
                self.tell_joke()
                return
            
            index = randint(0, len(requestedJokes)-1)

            print(requestedJokes[index]["setup"])
            sleep(mean(requestedJokes[index]["wait"]))
            print(requestedJokes[index]["punchline"])
            self.toldJokes.append(requestedJokes[index])
            self.jokes.remove(requestedJokes[index])
            self.jokeCount += 1

        return


    def rate_joke(self, joke: str):

        allJokes = self.jokes + self.toldJokes
        jokeSimilarities = []

        for knownJoke in allJokes:

            knownSetupAndPunchline = knownJoke["setup"] + " " + knownJoke["punchline"]

            receivedJoke = comparationModel.encode(joke,convert_to_tensor=True)
            storedJoke = comparationModel.encode(knownSetupAndPunchline,convert_to_tensor=True)
            similarity = util.pytorch_cos_sim(receivedJoke, storedJoke).item()
            jokeSimilarities.append({"rating": mean(knownJoke["ratings"]), "similarity": similarity})
        
        return int(max(jokeSimilarities, key=lambda item: mean(item["similarity"]))["rating"])
    
    def opener(self):
        print("""Welcome to the show! I'll be your entertainer for tonight!
        I'll try my best to make you laugh, but keep in mind I was I can only accept one word inputs, as I am still in my cave painting phase.
        I have some material prepared for you tonight, but if at any time you feel like hearing something new let me know by typing "generate".
        Whenever you feel that you've had a good enough time and decide to stop being happy, please type "leave".""")

        return

    def closer(self):
        now = datetime.now().hour

        match now:
            case now if 0 <= now < 8:
                closeMsg = "night! Consider getting some beauty sleep"
            
            case now if 8 <= now < 12:
                closeMsg = "morning"
            
            case now if 12 <= now < 19:
                closeMsg = "afternoon"
            
            case now if now > 19:
                closeMsg = "night"
            
            case _:
                closeMsg = "one"
            
        print(f"Thank you very much for coming, I hope you enjoyed the show, have a good {closeMsg}!")
        exit()
    
    def checkMessage(self, msg: str):
        return profanity.contains_profanity(msg)
    
    def saveJoke(self):
        newJoke = {
                    "setup": "",
                    "punchline": "",
                    "category": "",
                    "ratings": [],
                    "wait": [2]
                }
        
        category = input("What kind of joke is this?")

        if self.checkMessage(category):
            print("I'm afraid this joke isn't quite the kind of joke I'm able to tell but thank you anyway!")
            return
        
        newJoke["category"] = category
        
        setup = input("What is the setup to your joke?")

        if self.checkMessage(setup):
            print("I'm afraid this joke isn't quite the kind of joke I'm able to tell but thank you anyway!")
            return
        
        newJoke["setup"] = setup
        
        punchline = input("What is the punchline to your joke?")

        if self.checkMessage(punchline):
            print("I'm afraid this joke isn't quite the kind of joke I'm able to tell but thank you anyway!")
            return
        
        newJoke["punchline"] = punchline
        
        rating = input("How would you rate this joke from 1 to 10?")

        if not rating.isnumeric() or not 1 <= int(rating) <= 10:
            print("I'm afraid that isn't quite within the scale so I'll just give it a 5 for now!")
            newJoke["ratings"].append(5)
            self.toldJokes.append(newJoke)
            return
        
        newJoke["ratings"].append(rating)
        self.toldJokes.append(newJoke)
        


if __name__ == "__main__":
    
    rickyGervAI = Bot()
    
    rickyGervAI.opener()
    rickyGervAI.rate_joke("What animal has the softest bite?")

    msg = input("With that said how are you doing tonight?")

    if msg.lower() == "leave":
        rickyGervAI.closer()

    if rickyGervAI.checkMessage(msg):
        print("While some people might enjoy different brands of humor, we should try and keep things a bit cleaner here. How about a joke?")
        rickyGervAI.tell_joke()
        category = ""

    else:
        sentiment = classifier(msg)

        match sentiment:
            case sentiment if sentiment[0]["score"] > 0.9 and sentiment[0]["label"] == "POSITIVE":
                print("Great! Let's keep that up and get into the fun then!")
            
            case sentiment if sentiment[0]["score"] > 0.9 and sentiment[0]["label"] == "NEGATIVE":
                print("Sorry to hear that, let's see if can't turn that frown upside down with some jokes!")
            
            case _:
                print("As a program I'm having a hard time relating, but it sounds like you could use some jokes!")

        category = input("Do you have any joke type preference? Just press Enter for a random one!")

        if category.lower() == "leave":
            rickyGervAI.closer()

        if rickyGervAI.checkMessage(category):
            print("While some people might enjoy different brands of humor, we should try and keep things a bit cleaner here. How about a joke?")
            rickyGervAI.tell_joke()
        
        rickyGervAI.tell_joke(category)

    while True:

        if category.lower() == "generate":
            print("That may have been a bit weird, but I hope you liked it! ")
            category = input("In the mood for any particular joke type? Just press Enter for a random one!")

            if category.lower() == "leave":
                break

            if rickyGervAI.checkMessage(category):
                print("While some people might enjoy different brands of humor, we should try and keep things a bit cleaner here. How about a joke?")
                rickyGervAI.tell_joke()

            rickyGervAI.tell_joke(category)
            continue
        
        msg = input("How was that?")

        if msg.lower() == "leave":
            break

        if rickyGervAI.checkMessage(msg):
            print("While some people might enjoy different brands of humor, we should try and keep things a bit cleaner here. How about another joke?")
            rickyGervAI.tell_joke()
            continue

        sentiment = classifier(msg)

        match sentiment:
            case sentiment if sentiment[0]["score"] > 0.9 and sentiment[0]["label"] == "POSITIVE":
                print(choice(rickyGervAI.positiveRetorts))
            
            case sentiment if sentiment[0]["score"] > 0.9 and sentiment[0]["label"] == "NEGATIVE":
                print(choice(rickyGervAI.negativeRetorts))
            
            case _:
                print("I couldn't quite tell if that landed or not.")

        rating = input("How would you rate that joke from 1 to 10?")

        if rating.lower() == "leave":
            break

        if not rating.isnumeric() or not 1 <= int(rating) <= 10:
            print(choice(rickyGervAI.incorrectRatingRetorts))
            rickyGervAI.tell_joke()
            continue

        rickyGervAI.toldJokes[rickyGervAI.jokeCount]["ratings"].append(int(rating))

        wait = input("Do you feel the timing was ok? If you would have waited longer or less please state the number of seconds, if not we can move to the next joke!")

        if wait.lower() == "leave":
            break

        if wait.isnumeric() and 1 <= int(wait) <= 6:
            rickyGervAI.toldJokes[rickyGervAI.jokeCount]["wait"].append(int(wait))
            
        category = input("In the mood for any particular joke type? Just press Enter for a random one!")

        if category.lower() == "leave":
            break

        if rickyGervAI.checkMessage(category):
            print("While some people might enjoy different brands of humor, we should try and keep things a bit cleaner here. How about a joke?")
            rickyGervAI.tell_joke()

        rickyGervAI.tell_joke(category)


    msg = input("Before you leave, would you like to teach me any jokes of your own? Type ""yes"" if you want to get started! If not we can call it a day!")

    while msg.lower() == "yes":
        rickyGervAI.saveJoke()
        print("Thank you for teaching me that joke!")
        msg = input("Would you like to teach me another?")


    with open(jokesFilePath, "w") as file:
        file.write(json.dumps(rickyGervAI.jokes + rickyGervAI.toldJokes))

    rickyGervAI.closer()