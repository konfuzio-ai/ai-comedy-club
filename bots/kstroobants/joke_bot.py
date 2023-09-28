from transformers import pipeline, GPT2LMHeadModel, GPT2Tokenizer
import torch
from pathlib import Path


class Bot:

    name = 'kstroobants'

    def __init__(self):
        ''' Initialise the bot.
        '''
        # set gpu/cpu
        self.device = 0 if torch.cuda.is_available() else -1

        # Init model to create jokes. A fine-tuned version of gpt2 is used which is trained to generate jokes instead of just gpt2
        # If a locally trained model exists made by train_joke_bot.py script then use it, otherwise use one from HuggingFace
        self.model_path = Path('./bots/kstroobants/ks-gpt2-jokes')
        if Path.exists(self.model_path):
            self.text_gen_model = GPT2LMHeadModel.from_pretrained(self.model_path, local_files_only=True)
            self.text_gen_tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
        else:
            self.text_gen_pipe = pipeline('text-generation', model='AlekseyKorshuk/gpt2-jokes',
                                          device=self.device, return_full_text=False)
            self.text_gen_pipe.model.config.pad_token_id = self.text_gen_pipe.model.config.eos_token_id

        # Init model to rate jokes
        self.rate_pipe = pipeline(model='Reggie/muppet-roberta-base-joke_detector',
                                  device=self.device, truncation=True, max_length=510)

    def tell_joke(self):
        ''' This method should generate and return a string containing a joke.
        '''
        # User engagement input
        # I deactivated the input because it is not practical for our main.py script, especially scoreboard is blocked by this input.
        mood: str = "fun"  # mood = input('How do you feel?') # deactivated
        theme: str = "work"  # theme = input('what do you like?') # deactivated

        # Rate your own jokes before saying them. Keep track of the best one
        best_rating = -1
        best_joke = ""
        for i in range(10):
            if Path.exists(self.model_path):
                input_data_joke = f"Tell me a {mood} joke that involves {theme}."
                ids = self.text_gen_tokenizer.encode(input_data_joke, return_tensors='pt')
                final_outputs = self.text_gen_model.generate(
                    ids,
                    max_length=len(input_data_joke) + 50,
                    pad_token_id=self.text_gen_model.config.eos_token_id
                )
                joke = self.text_gen_tokenizer.decode(final_outputs[0], skip_special_tokens=True)
                joke = joke[len(input_data_joke)+1:]
            else:
                input_data_joke = f"{theme} and {mood}, tell me:"
                joke = self.text_gen_pipe(input_data_joke, max_length=len(input_data_joke) + 300)[0]['generated_text']

            rating = self.rate_joke(joke)
            if rating > best_rating:
                best_joke = joke
                best_rating = rating
            if rating >= 7:
                break

        # Case when model cannot generate an output
        if len(best_joke) == 1:
            best_joke = "I could not find an appropriate joke, bye."

        return best_joke

    def rate_joke(self, joke):
        ''' This method should take a string (representing the joke to be rated) and return an integer from 1 to 10, which represents the rating of the joke.
        '''
        # Rate joke
        result = self.rate_pipe(joke)

        # Find the score with the probability of the classification
        return round(result[0]['score']*10) if result[0]['label'] == 'LABEL_1' else round((1-result[0]['score'])*10)
