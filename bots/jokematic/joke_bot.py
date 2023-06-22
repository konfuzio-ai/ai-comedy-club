import openai
import numpy as np
import spacy
import csv
import subprocess

class Bot:
    name = "Jokematic"
    openai.api_key = "your_api_key"

    def __init__(self):
        self.download_spacy_model()

    def download_spacy_model(self):
        command = "python -m spacy download en_core_web_lg"
        subprocess.run(command, shell=True)

    '''Make the bot Flexible + Contemporary'''

    def generate_promp_improvement(self):
        prompt = "Genrate a trending word"
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=50,
            temperature=0.95,
            n=1,
            stop=None
        )
        improvement_prompt = response.choices[0].text.strip()
        print("Improvement: ", improvement_prompt)
        return improvement_prompt

    """Generates response given a prompt using an OpenAI model."""

    def tell_joke(self):
        prompt = "Tell me a joke about " + self.generate_promp_improvement()
        print("Prompt: ", prompt)
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=50,
            temperature=0.8,  # after some experimentation, 0.8 appears to be appropriate
            n=1,
            stop=None
        )

        joke = response.choices[0].text.strip()

        if self.filter_joke(joke):
            return joke
        else:
            return "JOKE WAS OFFENSIVE (WARNING): I'm sorry, I didn't come up with an appropriate joke. But if you like, we can try again."

    """RISK MANAGEMENT
    Checks if the joke is offensive (returns TRUE) or not (returns FALSE), using OpenAI's moderation API.
    Multiple dimensions are considered, such as hate, self-harm, sexual, etc."""

    def filter_joke(self, joke):
        response = openai.Moderation.create(
            model="text-moderation-latest",
            input=[joke]
        )

        if response['results'][0]['flagged']:
            return False
        else:
            return True

    def rate_joke(self, joke: str):
        # Path to the CSV file
        csv_file = "shortjokes.csv"

        # Load spacy with GloVe embeddings
        nlp = spacy.load("en_core_web_lg")

        # Read the first 200 jokes from the CSV file
        # Reading all 200 000 jokes will be computationally demanding
        jokes = []
        with open(csv_file, "r", encoding="utf-8") as file:
            csv_reader = csv.reader(file)
            next(csv_reader)  # Skip the first line

            for i in range(200):
                try:
                    row = next(csv_reader)
                    joke = row[1]  # Retrieving the current joke
                    jokes.append(joke)
                except StopIteration:
                    break

        # Get word embeddings for example set of jokes
        jokes_embeddings = [nlp(joke).vector for joke in jokes]

        # Get word embeddings for the new joke
        new_joke_embedding = nlp(joke).vector

        # Calculate cosine similarities between the new joke and existing jokes
        similarities = np.dot(jokes_embeddings, new_joke_embedding) / (
                np.linalg.norm(jokes_embeddings, axis=1) * np.linalg.norm(new_joke_embedding)
        )

        # Calculate the average similarity score
        average_similarity = np.mean(similarities)

        # Print the average similarity score
        return int(round(average_similarity * 10))
