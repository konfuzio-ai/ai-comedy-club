import random

from profanity_check import predict_prob
from textblob import TextBlob
from transformers import pipeline

# propmts or starters for text/joke generation
# source: https://www.greataiprompts.com/chat-gpt/funny-chat-gpt-prompts/?expand_article=1
JOKE_PROMPTS = ['Knock, knock!',
                'What do you call a fake noodle?',
                'Can February March?',
                'Why don’t scientists trust atoms?',
                'What did one toilet say to the other?',
                'Why did the tomato turn red?',
                'Why don’t oysters share their pearls?',
                'How do you make a tissue dance?',
                'What do you get when you cross a snowman and a shark?',
                'How does a penguin build its house?',
                'Why do seagulls fly over the sea?',
                'What did one hat say to the other?',
                'Why did the chicken cross the road?',
                'What do you call a group of cows playing instruments?',
                'What do you call a bear with no teeth?',
                'Why did the banana go to the doctor?',
                'What do you call an alligator in a vest?',
                'Why was the math book sad?',
                'Why did the coffee file a police report?',
                'How do you make a unicorn float?',
                'What do you get when you cross a snowman and a vampire?',
                'Why was the belt arrested?',
                'What did the left eye say to the right eye?',
                'Why don’t ghosts use elevators?',
                "What do you call a boomerang that doesn't come back?",
                'What do you call a lazy kangaroo?',
                'How does a rabbi make coffee?',
                'What did the grape say when it got stepped on?',
                'Why did the scarecrow win an award?',
                'Why did the fish blush?', 'What do you call a fake noodle?',
                'How do you know if a joke is a dad joke?',
                'Why do bees have sticky hair?',
                'Why did the frog call his insurance company?',
                'Why did the cookie go to the doctor?',
                'Why did the chicken join a band?',
                'What do you call a bear with no teeth and no ears?',
                'What do you call a sheep that can sing?',
                'Why did the turtle cross the road?',
                "Why did the tomato turn red?', 'Why don't ants get sick?",
                'What do you call a dog magician?',
                "Why don't seagulls fly by the bay?",
                'What do you get when you cross a snowman and a bulldozer?',
                'What did one hat say to the other?',
                "Why don't scientists trust atoms?",
                'How do you make a tissue dance?',
                'What do you call a fish wearing a bowtie?',
                'Why did the coffee file a police report?',
                'Why did the man put his money in the freezer?',
                'Why did the toilet paper roll down the hill?',
                'What do you call a dinosaur with an extensive vocabulary?',
                'What did the pirate say on his 80th birthday?',
                'Why did the avocado go to the doctor?',
                'What do you get when you cross a snowman and a refrigerator?',
                'Why did the koala get fired from his job?',
                'Why did the bicycle fall over?',
                'What do you call a boomerang that works every time?',
                'Why did the crab never share his toys?',
                'What do you call a bear with no teeth and a sunburn?',
                'What do you think about Elon Musk?',
                'Explain quantum theory to a kid like Snoop Dog',
                'Describe your perfect day as an AI language model.',
                'Are you sentient?']


class Bot:
    # because the jokes may not be on time
    name = 'DeutscheBahn'

    def __init__(self, JOKE_PROMPTS=JOKE_PROMPTS):
        self.JOKE_PROMPTS = JOKE_PROMPTS
        
        # model : https://huggingface.co/AlekseyKorshuk/gpt2-jokes
        self.joke_generator = pipeline(
            'text-generation', model='AlekseyKorshuk/gpt2-jokes')
        
    # can't control the models output generation
    # without fine tuning it again.
    # checking and filtering is a better option
    def is_nsfw(self, joke):
        nsfw_proba = predict_prob([joke])
        THRESHOLD = 0.35
        
        if nsfw_proba < THRESHOLD:
            return False
        else:
            return True
            
    def tell_joke(self):
        # randomly select a joke prompt
        prompt = random.choice(self.JOKE_PROMPTS)
        joke = self.joke_generator(f'{prompt}', max_length=30, do_sample=True)[
            0]['generated_text']
        
        # check for nsfw
        nsfw = self.is_nsfw(joke)
        if nsfw:
            return prompt + " ****** ."
        else:
            # it's safe
            return joke

    def rate_joke(self, joke):
        # Rate the joke based on its sentiment polarity
        # This is a simple example and doesn't actually reflect humor
        blob = TextBlob(joke)
        polarity = blob.sentiment.polarity  # type: ignore
        rating = (polarity + 1) * 5  # convert polarity from [-1, 1] to [0, 10]
        return int(rating) # integer ratings are nicer to look at
    
if __name__ == "__main__":
    bot = Bot()
    joke = bot.tell_joke()
    
    rating = bot.rate_joke(joke)
    
    print(joke)
    print(rating)
    
