import torch
import os
from transformers import GPT2LMHeadModel, GPT2Tokenizer, AutoModelForSequenceClassification, DataCollatorForLanguageModeling, Trainer, pipeline, AutoTokenizer

from utility import choose_from_top, find_string_between_occurrences
from config import JokeTellerModelConfig, JokeRaterModelConfig

class Bot:
    name = 'LeMonJames'
    def __init__(self):
        self.torch_device = "cuda" if torch.cuda.is_available() else "cpu"

        self.model_gen = GPT2LMHeadModel.from_pretrained('gpt2').to(self.torch_device)
        self.model_rate = AutoModelForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=10)

        self.tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased')
        self.tokenizer_teller = GPT2Tokenizer.from_pretrained('gpt2')

        state_dict_tell = torch.load(JokeTellerModelConfig.model_path, map_location=torch.device(self.torch_device))
        self.model_tell_tuned = GPT2LMHeadModel.from_pretrained('gpt2').to(self.torch_device)
        self.model_tell_tuned.load_state_dict(state_dict_tell)

        self.model_rater_pipe = pipeline('text-classification',
                                        model=JokeRaterModelConfig.model_path,
                                        tokenizer=self.tokenizer)

    def tell_joke(self):
        print("Give LeMon James you request for a joke!")
        prompt = input()

        joke = bot.generate_some_text(prompt)

        return joke

    def rate_joke(self, joke: str):
        return self.model_rater_pipe(joke)[0]['label'][-1]


    def generate_some_text(self, prompt, text_len = 150):

        cur_ids = torch.tensor(self.tokenizer_teller.encode(prompt)).unsqueeze(0).long().to(self.torch_device)

        self.model_tell_tuned.eval()
        with torch.no_grad():

            for _ in range(text_len):
                outputs = self.model_tell_tuned(cur_ids, labels=cur_ids)
                _, logits = outputs[:2]
                softmax_logits = torch.softmax(logits[0,-1], dim=0) # Take the first(only one) batch and the last predicted embedding
                
                # Randomly(from the given probability distribution) choose the next word from the top n words
                next_token_id = choose_from_top(softmax_logits.to('cpu').numpy(), n=10)
                
                cur_ids = torch.cat([cur_ids, torch.ones((1,1)).long().to(self.torch_device) * next_token_id], dim = 1) # Add the last word

            output_list = list(cur_ids.squeeze().to('cpu').numpy())
            output_text = self.tokenizer_teller.decode(output_list)

            return find_string_between_occurrences(output_text, "<|endoftext|>")
        
    def tune_rater(self, args, optimizer, scheduler, train_dataset, test_dataset):
        """
            Tune the Joke Rating model to give ratings between 1-10.
        """

        rater_trainer = Trainer(
            model=self.model_rate,
            args=args,
            train_dataset=train_dataset,
            optimizers=(optimizer, scheduler),
            eval_dataset=test_dataset
        )

        rater_trainer.train()

        rater_trainer.save_model("trained_models/gpt2_rater_model")

        evaluation_score = rater_trainer.evaluate(eval_dataset=test_dataset)

        return evaluation_score

if __name__ == "__main__":
    bot = Bot()

    joke = bot.tell_joke()
    print(joke)
    
    rating = bot.rate_joke(joke)
    print(f"Rating: {rating}/10")