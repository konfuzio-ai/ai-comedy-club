import pyjokes
import os 
import importlib.util

class Bot:
    name = 'Funny'

    def small_talk(self, message):
        if message.lower() in ["hi", "hello", "hey"]:
            response = "Hello! How can I help you today?"
            return response

    def tell_joke(self):
        # Select a random joke from the pyjokes where language is english and category neutral (programming, geeks jokes)
        joke = pyjokes.get_joke(language="en", category="neutral")
        return joke
    
    def rate_joke(self, joke):
     
        bots_dir = './bots/'
        rating = 0
        bot_directories = [d for d in os.listdir(bots_dir) if os.path.isdir(os.path.join(bots_dir, d))]

        total_rating = 0
        i = 0
        for bot_dir in bot_directories:
            if bot_dir != "benjo":
               
                spec = importlib.util.spec_from_file_location("bot", os.path.join(bots_dir, bot_dir, "joke_bot.py"))
                bot_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(bot_module)

                bot = bot_module.Bot()

                bot_rating = bot.rate_joke(joke)
                total_rating += bot_rating
                i += 1

        rating = total_rating / i
        if rating < 9:
            rating += 1
        if rating > 10:
            rating = 10

        return rating