from transformers import pipeline
import random
import openai
import os

os.environ["TOKENIZERS_PARALLELISM"] = "false"


class Bot:
    name = 'Pechonson AI'
    MAX_TOKENS = 100
    # Using a 0.7 value to force logic but more creatives texts.
    # The max value can be 2.0 but this will give some irrational responses.
    # The min value can be 0 but this will make the model very predictable.
    TEMPERATURE = 0.7
    GPT_MODEL = "text-davinci-003"

    def __init__(self):
        openai.api_key = os.getenv('OPENAI_API_KEY')

        joke_evaluator_model_name = 'Reggie/muppet-roberta-base-joke_detector'
        self.joke_evaluator = pipeline(model=joke_evaluator_model_name)

    def get_text_from_chatgpt3sdk(self, messages, max_tokens=MAX_TOKENS, temperature=TEMPERATURE):
        # print(f"Prompt here: {messages}")
        response = openai.Completion.create(
            model=self.GPT_MODEL,
            prompt=messages,
            max_tokens=max_tokens,
            temperature=temperature
        )
        return response.choices[0].text.strip()

    def build_prompt(self, from_country=None, language=None):
        prompt = "Tell me a joke"
        if from_country != None:
            prompt = f"{prompt} about people from {from_country}"

        if language != None:
            prompt = f"{prompt} in {language}"

        return prompt

    def tell_introductory_phrase(self):
        prompt = f"Your name is {self.name}. Tell me a unique and funny introductory phrase for an stand up comedy show"
        intro_phrase = self.get_text_from_chatgpt3sdk(prompt, max_tokens=200)
        print(f"{self.name}: {intro_phrase}")

    def get_country_from_user(self):
        from_country = input(f"{self.name}: Where are you from?\n")
        prompt = self.build_prompt(from_country=from_country)
        joke = self.get_text_from_chatgpt3sdk(prompt, max_tokens=200)
        print(f"{self.name}: {joke}")
        return from_country

    def get_language_from_user(self):
        language = input(
            f"{self.name}: I am really an educated bot, would you like me to entertain you in another language? If so, tell me which one\n")
        prompt = self.build_prompt(
            from_country=self.from_country, language=language)
        print(f"Prompt: {prompt}")
        joke = self.get_text_from_chatgpt3sdk(prompt, max_tokens=200)
        print(f"{self.name}: {joke}")
        return language

    def tell_outro_phrase(self):
        prompt = f"""Tell me a unique and funny parting line for a stand up 
        comedy show in {self.language}
        """
        outro_phrase = self.get_text_from_chatgpt3sdk(prompt, max_tokens=300)
        print(f"{self.name}: {outro_phrase}")

    def tell_joke(self):
        self.tell_introductory_phrase()

        self.from_country = self.get_country_from_user()

        self.language = self.get_language_from_user()

        joke = self.get_main_joke()

        self.tell_outro_phrase()

        return joke

    def rate_joke(self, joke):
        # [{'label': 'LABEL_1', 'score': 0.7313136458396912}]
        result = self.joke_evaluator(joke)
        result = result[0]['score'] if result[0]['label'] == 'LABEL_1' else 1 - \
            result[0]['score']
        return result * 10
