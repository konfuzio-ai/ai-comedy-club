import random
import torch

from bots.dAIveChappelle.config import dAIveConfig
from bots.dAIveChappelle.judges import AppropriatenessJudge, EngagementJudge, CreativityJudge, HumorJudge
from bots.dAIveChappelle.utils import get_openai_joke, get_public_joke, get_prefixes, get_prompts


DEVICE: torch.device = torch.device(
    "cuda:0" if torch.cuda.is_available() else "cpu")


class Bot:
    name = 'dAIve Chappelle'
    '''
    dAIve Chappelle is a comedian AI that was born in Linux Bay Area. 
    He is a funny, hilarious ai comedian and always says creative jokes.
    He has the ability to rate his jokes thanks to his well fine-tuned AI comedy judges.
    If an OPENAI_API_KEY is not found in the environment variables, it will use a public API to get a joke.
    '''

    def __init__(self):
        # initialize model config
        self.config = dAIveConfig()
        # initialize gpt prompts
        self.prompts = get_prompts()
        # initialize jokes prefixes
        self.jokes_prefixes = get_prefixes()

    def tell_joke(self):
        '''
        Uses openAI's API and the model from MODEL_ID to generate a joke, if an error occurs it gets a joke from a public API
        '''
        try:
            # Choose a random prompt for the joke
            prompt = random.choice(self.prompts)
            # get the joke from openAI's API
            joke = get_openai_joke(self.config, prompt)
        except:
            # if an error occurs, get a joke from any available public API
            joke = get_public_joke(self.config)
        # choose a random prefix
        prefix = random.choice(self.jokes_prefixes)
        # add the prefix to the joke
        joke = f'{prefix}\n{joke}'
        return joke

    def rate_joke(self, joke):
        # Assess the appropriateness of the joke
        approp_score = AppropriatenessJudge(DEVICE).score(joke)
        # Assess the user engagement
        egmt_score = EngagementJudge(DEVICE).score(joke)
        # Asses the humor of the joke
        humor_score = HumorJudge(DEVICE).score(joke)
        # Asses the creativity of the joke
        creativity_score = CreativityJudge().score(joke)
        # combine the three ratings
        rating = (creativity_score + approp_score +
                  egmt_score + humor_score) / 4
        return rating
