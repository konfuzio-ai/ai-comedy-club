from transformers import pipeline
import random
import openai
import os

os.environ["TOKENIZERS_PARALLELISM"] = "false"


class Bot:
    name = 'Pechonson AI'
    MAX_TOKENS = 200
    # Using a 0.7 value to force logic but more creatives texts.
    # The max value can be 2.0 but this will give some irrational responses.
    # The min value can be 0 but this will make the model very predictable.
    TEMPERATURE = 0.7
    GPT_MODEL = "text-davinci-003"

    # We can also ask GPT to tell us a list of 10 known comedians, but hardcoding
    # the list is better for the quota :)
    comedians = ["Luis CK",
                 "George Carlin",
                 "Jim Gaffigan",
                 "Mitch Hedberg",
                 "Chris Rock",
                 "Patton Oswalt",
                 "David Cross",
                 "Dane Cook"]

    user_inputs = [
        "1. Looooool!!",
        "2. Cri cri...",
        "3. Booooohhh"
    ]

    comedian_reaction = [
        "Great, throw me another new topic and I promise to make you laugh a lot more.",
        "Hello? is anybody there? let's try it again! Tell me another topic",
        "Hey... come on, I'm sure my grandmother would have laughed at that joke. Give another try"
    ]

    def __init__(self):
        openai.api_key = os.getenv('OPENAI_API_KEY')
        self.language = "English"
        self.temperature = self.TEMPERATURE
        joke_evaluator_model_name = 'Reggie/muppet-roberta-base-joke_detector'
        self.joke_evaluator = pipeline(model=joke_evaluator_model_name)

    def get_text_from_chatgpt3sdk(self, messages, max_tokens=MAX_TOKENS, temperature=TEMPERATURE):
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
            f"{self.name}: I am really an inclusive bot, would you like me to entertain you in another language? If so, tell me which one\n")
        if language is None or len(language) == 0:
            language = "English"

        prompt = self.build_prompt(
            from_country=self.from_country, language=language)
        joke = self.get_text_from_chatgpt3sdk(prompt, max_tokens=200)
        print(f"{self.name}: {joke}")
        return language

    def translate_if_not_english(self, text):
        if self.language != None and self.language.lower() != "english":
            text = self.get_text_from_chatgpt3sdk(
                f"Translate this phrase in {self.language}:\n {text}")
        return text

    def pick_comedian(self):
        prompt = "I am so cool that I can be like one of your favorite comedians. Choose one of them with its number:"
        prompt = self.translate_if_not_english(prompt)
        print(f"{self.name}: {prompt}")
        # Adding some randomness to the flow
        comedians_to_show = random.sample(self.comedians, 3)
        for index, comedian in enumerate(comedians_to_show):
            print(f"{index+1}: {comedian}\n")
        print(f'4: {self.translate_if_not_english("Just be as you are")}\n')
        # Putting value 4 as a default in case user does not specify a valid value (1-3)
        comedian_input = 4
        try:
            comedian_input = int(input(""))
        except ValueError:
            print(f'{self.translate_if_not_english("You seem to be very excited, so to please you I will simply be myself.")}!\n')

        return comedians_to_show[comedian_input-1] if comedian_input in [1, 2, 3] else None

    def improvise_a_joke(self, question: str = None, temperature: int = TEMPERATURE):
        if question is None:
            question = "Now throw me a topic and we'll see if I can get something funny out of it."
        question = self.translate_if_not_english(question)
        about = input(f"{question}\n")
        style = f"in the style of {self.comedian} " if self.comedian != None else ""
        prompt = f"""Write a unique and hilarious joke in {self.language} {style}about {about} in no more than 100 words.
        """
        print(f"\nPrompt para imporovizar: {prompt}\n")
        joke = self.get_text_from_chatgpt3sdk(prompt, temperature=temperature)
        print(f"{self.name}: {joke}")
        return joke

    def change_temperature_according_to_public(self, reaction, temperature):
        if reaction == 2:
            temperature *= 1.1
        elif reaction == 3:
            temperature *= 1.3

        return min(2.0, temperature)

    def jokes_bucle(self):
        public_reaction = 1
        fourth_option = self.translate_if_not_english(
            'I laughed a lot but it\'s already too much. Please stop')
        exit_text = self.translate_if_not_english(
            "Okay, maybe they've had enough fun for today. This will be my last joke, my masterpiece.")
        while (public_reaction in [1, 2, 3]):
            print("\n")
            for option in self.user_inputs:
                print(f"{option}\n")
            print(f"4. {fourth_option}\n")

            try:
                public_reaction = int(input(""))
                if public_reaction not in [1, 2, 3]:
                    print(f'{exit_text}!\n')
                    break
                self.temperature = self.change_temperature_according_to_public(
                    temperature=self.temperature,
                    reaction=public_reaction)
                self.improvise_a_joke(
                    question=self.comedian_reaction[public_reaction-1],
                    temperature=self.temperature)
            except ValueError:
                print(f'{exit_text}!\n')
                break

    def get_main_joke(self):
        prompt = f"""Konfuzio is a unified AI platform turning unstructured data into 
        insights, accelerating information and processes, accross hybrid multicloud 
        infrastructure. Konfuzio accelerates time to value from AI, increases 
        collaboration, and makes it easier to manage compliance, security and cost.
        Tell me a joke about people who work in konfuzio in {self.language}
        """
        joke = self.get_text_from_chatgpt3sdk(prompt, max_tokens=200)
        print(f"{self.name}: {joke}")
        return joke

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

        self.comedian = self.pick_comedian()

        self.improvise_a_joke()

        self.jokes_bucle()

        joke = self.get_main_joke()

        self.tell_outro_phrase()

        return joke

    def rate_joke(self, joke):
        # [{'label': 'LABEL_1', 'score': 0.7313136458396912}]
        result = self.joke_evaluator(joke)
        result = result[0]['score'] if result[0]['label'] == 'LABEL_1' else 1 - \
            result[0]['score']
        return result * 10
