import random

import torch
from transformers import (AutoModelForSequenceClassification,
                          AutoModelForCausalLM, AutoTokenizer)


class Bot:
    name = "ChuckleChief"

    def __init__(self):
        self.max_length = 30
        self.joke_prefixes = [
            "My best joke is: ",
            "Here is a joke filled with harmless humour: "
        ]

        generator_model = "botbrain/ChuckleWhiz"
        rater_model = "mohameddhiab/rate-jokes-bert"

        self.generator = AutoModelForCausalLM.from_pretrained(
            generator_model).eval()
        self.generator_tokeniser = AutoTokenizer.from_pretrained(
            generator_model)

        self.rater = AutoModelForSequenceClassification.from_pretrained(
            rater_model).eval()
        self.rater_tokeniser = AutoTokenizer.from_pretrained(rater_model)

    def tell_joke(self) -> str:
        prefix = random.choice(self.joke_prefixes)
        input_ids = self.generator_tokeniser.encode(
            prefix, return_tensors="pt")
        with torch.no_grad():
            joke = self.generator.generate(
                input_ids,
                max_length=self.max_length,
                repetition_penalty=1.2,
                temperature=0.75,
                do_sample=True
            )

        joke = self.generator_tokeniser.decode(
            joke[0], skip_special_tokens=True)

        # Find the last sentence-ending punctuation mark.
        end_marks = [".", "!", "?"]
        end_pos = max([joke.rfind(m) for m in end_marks])

        # If there is no sentence-ending punctuation mark, return the whole joke.
        if end_pos == -1:
            return joke

        # Otherwise, return the joke up to the last sentence-ending punctuation mark.
        return joke[:end_pos + 1]

    def rate_joke(self, joke: str) -> int:
        inputs = self.rater_tokeniser.encode_plus(
            joke,
            add_special_tokens=True,
            truncation=True,
            padding="longest",
            return_tensors="pt"
        )
        logits = self.rater(**inputs).logits
        rating = int(logits.argmax())

        # Map the rating to a range of 1 to 10.
        rating = min(max(rating, 1), 10)
        return rating
