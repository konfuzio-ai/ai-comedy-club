# User interraction with entertAIn bot. You can start to chat with your comedian bot in CLI ...

from textblob import TextBlob
from joke_bot import RateJokes
from joke_bot import GenerateJokes

def split_joke(joke):
    if "?" not in joke:
        return "", ""
    parts = joke.split("?", 1)
    question = parts[0] + "?" 
    answer = parts[1]
    return question, answer

def rate_my_joke(joke):
    joke_rate = rate.predict(joke)
    if joke_rate > 0.5:
        print("Haha, that's funny...")
    else:
        print("You can do it better..")
    
print("Waiting for the AI comedian to step on a stage ...")

bot = GenerateJokes()
rate = RateJokes()


# Introduction
import time
introduction = ["Hello everyone! This is the first AI standup comedy ever!", 
                "My name is entertAIn - AI bot designed to entertain you :D",
                "Tell me how are you today?"
    ]
for sentence in introduction:
    print(sentence)
    time.sleep(2)
    
answer = input("Me: ")
blob = TextBlob(answer)
polarity = blob.sentiment.polarity
time.sleep(1)
if polarity > 0.5:
    print("That's awesome. I'll try to make you even more happier!")
elif  -0.5 < polarity < 0.5:
    print("Looks like you are not very enthusiastic, but I'll make you very soon!")
else:
    print("Don't worry, you'll be better in a minute :D")
print('\n')
        
# Jokes with beginning
time.sleep(2)
print('Lets start with some jokes!')
joke = bot.predict("How do you know", 64, 1)
print(joke)
time.sleep(2)
joke = bot.predict("Do you like when", 64, 1)
print(joke)
print('\n')

# Try tu guess
time.sleep(2)
print('I will ask you some funny questions, and you can try tu guess the answer:')
beginnings = ["Why would you", "When is the perfect time", "How do you know"]

for i in range(3):
    joke = bot.predict(beginnings[i], 64, 1)
    question, answer = split_joke(joke)
    print(question)
    my_answer = input("Answer: ")
    rate_my_joke(question + ' ' + my_answer)
    print("Here's my answer:")
    print(answer)
print('\n')

# Give me topic
time.sleep(2)
print('Give me some interesting topic you want me to make joke about:')
beginnings = ["Why do you think about ", "Do you like when ", "It's very funny how you imagine "]

for i in range(3):
    answer = input("Topic: ")
    joke = bot.predict(beginnings[i] + answer, 64, 1)
    print(joke)
print('\n')

# Mix to things
time.sleep(2)
print('Give me two thing you want to mix (example: AI bot and funny people)')
for i in range(3):
    answer = input("Two things: ")
    joke = bot.predict("What do you get when you mix " + answer, 64, 1)
    print(joke)
print('\n')

# Rate my jokes
time.sleep(2)
print("You can also rate my jokes. After every joke you can give me rate from 0 to 10. Let's go:")
for i in range(5):
    joke = bot.predict("Joke: ", 64, 1)
    print(joke)
    answer = input("Rate: ")
    try:
        int(answer)
        if int(answer) > 5:
            print("I told you I'm good!")
        else:
            print("Wait for a next one, it's gonna be better!")
    except ValueError:
        print("That's not valid rate")