import pyjokes

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
        # Calculate the rating based on various criteria
        rating = 0

        # Criteria 1: Length of the joke
        length = len(joke)
        if length <= 50:
            rating += 5
        elif length < 100:
            rating += 4
        else:
            rating += 3

        
        if 'java' in joke.lower() or 'python' in joke.lower():
            rating += 2

       
        if 'php' in joke.lower() or 'laravel' in joke.lower():
            rating += 1

      
        if 'clever' in joke.lower() or 'smart' in joke.lower():
            rating += 1

        
        if 'windows' in joke.lower() or 'atom' in joke.lower():
            rating += 1

        joke_without_spaces = ''.join(joke.lower().split())
        if joke_without_spaces == joke_without_spaces[::-1]:
            rating = 10

        return rating
