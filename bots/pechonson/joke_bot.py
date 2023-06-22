from transformers import pipeline
import random
import openai
import os

os.environ["TOKENIZERS_PARALLELISM"] = "false"


class Bot:
    name = 'Pechonson AI'
    MAX_TOKENS = 100
    TEMPERATURE = 0.7

    def __init__(self):
        openai.api_key = os.getenv('OPENAI_API_KEY')

        joke_evaluator_model_name = 'Reggie/muppet-roberta-base-joke_detector'
        self.joke_evaluator = pipeline(model=joke_evaluator_model_name)

    def get_text_from_chatgpt3sdk(self, messages, max_tokens=MAX_TOKENS, temperature=TEMPERATURE):
        print(f"Prompt here: {messages}")
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=messages,
            max_tokens=max_tokens, 
            temperature=temperature
        )
        return response.choices[0].text.strip()

    def tell_joke(self):
        prompt = "Tell me a joke about developers"
        joke = self.get_text_from_chatgpt3sdk(prompt, max_tokens=200)
        return joke

    def rate_joke(self, joke):
        # [{'label': 'LABEL_1', 'score': 0.7313136458396912}]
        result = self.joke_evaluator(joke)
        return result[0]['score'] if result[0]['label'] == 'LABEL_1' else 1 - result[0]['score']
