import random
from textblob import TextBlob


class Bot:
    def __init__(self):
        self.prefix = '-Knock knock\n-Who\'s there?'
        self.whos = ['Nobel', 'Luke', 'Figs', 'Says', 'Orange', 'Annie', 'Iran', 'Dozen', 'Thermos', 'Razor']
        self.who = self.get_who()
        self.endings = [
            'Nobel that’s why I knocked!',
            'Luke through the peep hole and find out.',
            'Figs the doorbell, it’s not working!',
            'Says me!',
            'Orange you going to let me in?',
            'Annie way you can let me in?',
            'Iran here. I’m tired!',
            'Dozen anyone want to let me in?',
            'Thermos be a better way to get to you.',
            'Razor hands, this is a stick up!'
        ]

    def tell_joke(self):
        joke = f'{self.prefix}\n-{self.who}.\n{self.someone_who()}\n-{self.joke_ending()}'
        return joke

    def rate_joke(self, joke: str):
        blob = TextBlob(joke)
        rating = blob.sentiment_assessments
        context = {
            'Polarity': rating.polarity,
            'Subjectivity': rating.subjectivity,
            'Assessments': rating.assessments,
        }

        return context

    def get_who(self):
        return random.choice(self.whos)

    def someone_who(self):
        return f'-{self.who} who?'

    def joke_ending(self):
        key = self.who
        return next((ending for ending in self.endings if ending.startswith(key.title())), '')


jokebot = Bot()
joke = jokebot.tell_joke()
rating = jokebot.rate_joke(joke)
print(f'Joke:\n{joke}\nRating:\n{str(rating)[1:-1]}')
