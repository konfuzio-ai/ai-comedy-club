import random
from transformers import GPT2TokenizerFast
import torch
from utils import scale_perplexity
try:
    from mkultra.tuning import GPT2PromptTuningLM
    from mkultra.soft_prompt import SoftPrompt
    from mkultra.tokenizers import GPT2SPTokenizerFast
except ModuleNotFoundError:
    #If Prompt Tuning Libary mkultra not present install
    import subprocess
    import sys
    subprocess.check_call([sys.executable
                              , "-m"
                              , "pip"
                              , "install"
                              , 'git+https://github.com/corolla-johnson/mkultra.git#egg=mkultra '])
    from mkultra.tuning import GPT2PromptTuningLM
    from mkultra.soft_prompt import SoftPrompt
    from mkultra.tokenizers import GPT2SPTokenizerFast

    #I sadly only noticed after setting up the whole training that the generation function of mkultra is not compatible
    #anymore with transformers > 4.15, this is why on first load I downgrade the version manually
    subprocess.check_call([sys.executable
                              , "-m"
                              , "pip"
                              , "install"
                              , 'transformers==4.15.0'])

VOCAB_SIZE_GPT2_SOFT_PROMPT = 50255 #technically 50256 but the end of sentence token is excluded
SOFTPROMPT_PATH = 'data/soft_prompt/johnny.json'

class Bot:
    bot_name ="Jonathan Jokestar"

    def __init__(self,load_soft_prompt,soft_prompt_length=20,soft_prompt_path=None,model_name='gpt2'):
        """
        Init function for the bot. Most parameters are default assigned since they are not needed if the bot is
        initialized with a trained soft prompt.
        @param load_soft_prompt: Boolean
            Indicates whether a pretrained Prompt should be loaded aór a new one should be initialized
        @param soft_prompt_length: Int
            Token length of the soft prompt to be generated
        @param soft_prompt_path: String
            Path to the pretrained sot prompt
        @param model_name: String
            Name of the model architecture (GPT-2 only)
        """
        self.model_name = model_name
        if torch.cuda.is_available():
            self.model = GPT2PromptTuningLM.from_pretrained(model_name).half().to("cuda")
        else:
            self.model = GPT2PromptTuningLM.from_pretrained(model_name).half()
        self.tokenizer = GPT2SPTokenizerFast.from_pretrained(model_name)


        if load_soft_prompt:
            loaded_sp = SoftPrompt.from_file(soft_prompt_path)
            self.model.set_soft_prompt(loaded_sp)
            self.model.eval()

        else:
            #Init new softprompt
            soft_token_ids = self.generate_new_soft_prompt(soft_prompt_length)
            soft_prompt_string = self.tokenizer.decode(soft_token_ids)
            initial_sp = SoftPrompt.from_string(soft_prompt_string, self.model, self.tokenizer)
            self.model.set_soft_prompt(initial_sp)



    def tell_joke(self,temp = 0.2):
        """
        A function which generates a String. Based on the soft prompt trained on jokes with
        which the model has been initalized this String is most likely a joke.

        @param temp: Float
            A preset hyperparameter which controls the randomness in the generated text. Low -> low randomness
        @return: String
            Hopefully a funny Joke
        """
        #Use prompting in addition to soft prompting in order to bias the model to be nice
        _prompt = 'Tell a friendly joke:'
        if torch.cuda.is_available():
            _prompt_token = self.tokenizer(_prompt, return_tensors="pt").input_ids.cuda()
        else:
            _prompt_token = self.tokenizer(_prompt, return_tensors="pt").input_ids

        joke_tokens = self.model.generate(
            input_ids=_prompt_token,
            do_sample=True,
            min_length=_prompt_token.shape[-1] + 20,
            max_length=_prompt_token.shape[-1] + 100,
            temperature=temp,
            repetition_penalty=3.0,
            pad_token_id=self.tokenizer.eos_token_id
        )
        #Hide the inital prompt
        return self.tokenizer.decode(joke_tokens[0][_prompt_token.shape[1]:joke_tokens[0].shape[0]])
    def rate_joke(self,joke):
        """
        A function which rates the joke based on the models average perplexity. The more confused
        the model is the worse the joke. Thereby implying the Bot is most amused by its own jokes.
        @param joke: String
            A string representing a joke
        @return: Int
            A rating between 0 (bad) - 10 (good) based on the models perplexity
        """
        if torch.cuda.is_available():
            joke_ids = self.tokenizer(joke, return_tensors="pt").input_ids.cuda()
        else:
            joke_ids = self.tokenizer(joke, return_tensors="pt").input_ids
        avg_perplexity = self.model(joke_ids, labels=joke_ids).loss.item()
        rating = scale_perplexity(avg_perplexity)
        return rating

    def generate_new_soft_prompt(self,num_tokens):
        """
        Function to sample random tokens in order to generate a trainable soft prompt.
        @param num_tokens: Int
            specifies the number of tokens to be sampled
        @return: list[Int]
            List of sampled tokens
        """
        soft_prompt_token_ids = []
        for i in range(num_tokens):
            soft_prompt_token_ids.append(random.randint(0, VOCAB_SIZE_GPT2_SOFT_PROMPT))
        return soft_prompt_token_ids



if __name__ == "__main__":
    bot = Bot(True,soft_prompt_path=SOFTPROMPT_PATH)
    joke = 'Why did the naive Bayesian suddenly feel patriotic when he heard fireworks? He assumed independence.'
    print(bot.tell_joke())
    print(bot.rate_joke(joke))
