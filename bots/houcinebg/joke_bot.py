import random
import csv
import openai
from nltk.sentiment import SentimentIntensityAnalyzer

class Bot:
    name = "HaHa_Too_Funny_Bot"

    def __init__(self, jokes_file, gpt_api_key):
        self.jokes_file = jokes_file
        self.gpt_api_key = gpt_api_key

    def performance(self):
        # Introduction
        print("Welcome to the AI Comedy Club!")
        print("My name is " + self.name)

        # Get user's mood
        mood = input("How are you feeling today? (happy/sad/bored): ").lower()

        while mood not in ["happy", "sad", "bored"]:
            mood = input("Please enter a valid response. How are you feeling today? (happy/sad/bored): ").lower()

        # Perform based on mood
        if mood == "happy":
            # Tell a joke and offer more
            print("Great! Let me tell you a joke.")
            print(self.tell_joke())

            decision = input("Do you want more? (Yes/No): ").lower()
            while decision not in ["yes","no"]:
                decision = input("Please enter a valid response. Do you want more? (Yes/No): ").lower()
            while decision == "yes":
                print("Here's another one:")
                print(self.tell_joke())
                decision = input("Do you want more? (Yes/No): ").lower()

        elif mood == "sad" or mood == "bored":
            # Tell a joke to cheer up
            print("No worries! Here I am to change your mood. Let me tell you a joke.")
            print(self.tell_joke())

            decision = input("Do you want more? (Yes/No): ").lower()
            while decision not in ["yes","no"]:
                decision = input("Please enter a valid response. Do you want more? (Yes/No):  ").lower()
            while decision == "yes":
                print("Here's another one:")
                print(self.tell_joke())
                decision = input("Do you want more? (Yes/No): ").lower()
            
            # Ask the user for their own joke
            othersjoke = input("Can you tell me a joke ? (Yes/No): ").lower()
            while othersjoke not in ["yes","no"]:
                othersjoke = input("Please enter a valid response. Do you want more? (Yes/No):  ").lower()

            while othersjoke == "yes":
                joke=input ("Okay then you can start :")
                while len(joke)<15:
                    joke=input ("too short ! can start again ? : ")

                print("Hmm, I would rate it a "+str(self.rate_joke(joke)) +" out of 10")
                othersjoke = input("can you tell more? (Yes/No): ").lower()

        # Farewell message
        print("Okay, goodbye! Thank you for visiting the AI Comedy Club. Have a great day!")

    def interact_with_crowd(self):
        # Crowd interaction warming up
        print("Now, let's warm up the crowd!")

        # Generate crowd interaction phrases using GPT-3
        gpt_response = self.generate_text("Generate some crowd interaction phrases for a comedy show.")
        phrases = gpt_response['choices'][0]['text'].strip().split("\n")

        random.shuffle(phrases)

        for phrase in phrases:
            input(phrase)
            print("That's a good one!")

    def tell_joke(self):
        # Load jokes from a CSV file
        jokes = []
        with open(self.jokes_file, encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                jokes.append(row[1])

        # Select and return a random joke
        joke = random.choice(jokes)
        return joke

    def rate_joke(self, joke):
        # Rate the humor score of a joke
        sid = SentimentIntensityAnalyzer()
        scores = sid.polarity_scores(joke)
        humor_score = scores["compound"]
        rescaled_rating = (humor_score + 1) * 5  # Scale the rating from -1 to 1 to 0 to 10
        rate = int(round(rescaled_rating, 0))
        return rate

    def generate_text(self, prompt):
        # Generate text using the OpenAI text-davinci-003 model
        openai.api_key = self.gpt_api_key
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=100,
            temperature=0.7,
            n=1,
            stop=None,
            max_completions=1,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )

        return response
    

# Set your OpenAI API key here
gpt_api_key = "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"

# Set the path to your jokes file here
jokes_file = r"D:\Konfuzio\ai-comedy-club\bots\houcinebg\cleanjokes.csv" #(kaggle cleanjokes dataset)

bot = Bot(jokes_file, gpt_api_key)
bot.performance() 