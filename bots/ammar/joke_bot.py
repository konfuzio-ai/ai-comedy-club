import openai
import random
from nltk.sentiment import SentimentIntensityAnalyzer
import pandas as pd
import numpy as np
import re

# Set up your OpenAI API credentials
openai.api_key = "YOUR API KEY"


def preprocess_result(df):
    df_sorted = df.sort_values(by="Time")
    # Initialize an empty DataFrame to store the extracted entries
    extracted_df = pd.DataFrame(columns=["Bot Name", "Joke", "Rating", "Time"])
    # Group the DataFrame by bot name and time
    grouped = df_sorted.groupby(["Bot Name", "Time"])
    average_rating = grouped['Rating'].mean()
    for (bot_name, time), rating in average_rating.items():
        joke = df[(df['Bot Name'] == bot_name) & (df['Time'] == time)]['Joke'].values[0]
        extracted_df = pd.concat([extracted_df, pd.DataFrame([[bot_name, joke, rating, time]], columns=df.columns)])
    extracted_df = extracted_df.reset_index().drop("index", axis=1)
    return extracted_df


def perform_sentiment_analysis(joke):
    # Initialize the sentiment intensity analyzer
    sid = SentimentIntensityAnalyzer()

    # Get the polarity scores for the text
    sentiment_scores = sid.polarity_scores(str(joke))

    # Extract the compound rating
    compound_score = sentiment_scores['compound']
    rating = round((compound_score + 1) * 5, 1)

    return rating


def GPT3_generator(prompt, max_tokens, temperature):
    # Generate the completion using GPT-3
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=prompt,
        max_tokens=max_tokens,
        n=1,
        stop=None,
        temperature=temperature
    )
    return response


def Scores_calculator(prompt):
    # Generate the completion using GPT-3
    response = GPT3_generator(prompt, 20, 0.5)
    # Get the generated response and extract the rating
    generated_text = response.choices[0].text.strip()
    score = generated_text.split(":")[-1].strip()
    match = re.search(r'\d+', score)
    if match:
        # Extract and return the first number found
        # Convert the score to a floating-point number
        return float(int(match.group()))
    else:
        # Return a default value if no number is found
        return None


def compute_tone_score(joke, previous_jokes):
    prompt = f"Joke: {joke}\nPrevious Jokes:\n"
    # Concatenate previous jokes
    for i, prev_joke in enumerate(previous_jokes):
        prompt += f"{i + 1}. {prev_joke}\n"
    # Add rating prompt
    prompt += "\nOnly give a single number to rate the bot's comedic style on a scale of 1 to 10:"
    score = Scores_calculator(prompt)
    return score


def compute_adaptability_score(previous_ratings):
    # Define the window size
    window_size = 3
    # Calculate the sliding average of ratings
    sliding_average = []
    for i in range(len(previous_ratings) - window_size + 1):
        window_ratings = previous_ratings[i:i + window_size]
        average_rating = sum(window_ratings) / len(window_ratings)
        sliding_average.append(average_rating)

    # Assign a rating based on adaptability
    rating = max(min(round(max(sliding_average) * 10), 10), 1)
    return rating


def compute_diversity_score(joke, previous_jokes):
    prompt = f"Joke: {joke}\nPrevious Jokes:\n"
    # Concatenate previous jokes
    for i, prev_joke in enumerate(previous_jokes):
        prompt += f"{i + 1}. {prev_joke}\n"
    # Add rating prompt
    prompt += "\nOnly give a single number as output to rate the bot's diversity style based " \
              f"on how much the jokes are distinct on a scale of 1 to 10:"
    score = Scores_calculator(prompt)
    return score


class Bot:
    name = 'Ammar'

    def __init__(self):
        # Define the results dataframe and extract list of jokes and ratings
        self.df = pd.read_csv("results/result.csv")
        self.extracted_df = preprocess_result(self.df)
        self.my_ratings = self.extracted_df.loc[self.extracted_df['Bot Name'] == self.name, 'Rating'].tolist()

    # Function to generate jokes using GPT-3 language model
    def tell_joke(self, preference):
        prompt = ["Tell me an introductory phrase comedian say before joke:",
                  f"Tell me a short and appropriate joke on \n\"{preference}\"\n and "
                  f"get better rating than \n\"{self.my_ratings[-1]}\"\n :"]

        prefix = GPT3_generator(prompt[0], 20, 0.5)
        joke = GPT3_generator(prompt[1], 30, 0.5)
        joke = f'{prefix.choices[0].text.strip()}' + joke.choices[0].text.strip()
        return joke

    # Function to rate jokes based on sentiment analysis
    def rate_joke(self, preference, bot_name, joke):
        prompt = [
            f"Only give a number to rate the funniness of the following joke on a scale of "
            f"1 to 10:\n\"{joke}\"\nScore:",
            f"Only give a number to rate  the creativity score of the following joke based on its uniqueness and "
            f"variation from 1 to 10:\n\"{joke}\"\nScore:",
            f"Only give a number to rate  the timeliness score of the following joke based on its relatedness to "
            f"current events or popular culture from 1 to 10:\n\"{joke}\"\nScore:",
            f"Only give a number to rate the personalization score of the following joke on a scale of 1 to 10 based "
            f"on user preferences: {preference}\nJoke: {joke}\nScore:",
            f"Only give a number to rate  the user engagement score based on following joke's encouragement of "
            f"interaction from 1 to 10:\n\"{joke}\"\nScore:",
            f"Only give a number to rate  the appropriation score based on if the following joke is work appropriate "
            f"from 1 to 10:\n\"{joke}\"\nScore:",
            f"Only give a number to rate  the delivery score based on if the following joke delivered in an engaging "
            f"way from 1 to 10:\n\"{joke}\"\nScore:",
        ]
        previous_jokes = self.extracted_df.loc[self.extracted_df['Bot Name'] == bot_name, 'Joke'].tolist()
        previous_ratings = self.extracted_df.loc[self.extracted_df['Bot Name'] == bot_name, 'Rating'].tolist()

        humor_score = Scores_calculator(prompt[0])
        creativity_score = Scores_calculator(prompt[1])
        timeliness_score = Scores_calculator(prompt[2])
        personalization_score = Scores_calculator(prompt[3])
        tone_and_style_score = compute_tone_score(joke, previous_jokes)
        adaptability_score = compute_adaptability_score(previous_ratings)
        user_engagement_score = Scores_calculator(prompt[4])
        appropriate_content_score = Scores_calculator(prompt[5])
        diversity_score = compute_diversity_score(joke, previous_jokes)
        delivery_score = Scores_calculator(prompt[6])
        sentiment_score = perform_sentiment_analysis(joke)
        # Calculate an overall rating out of 11
        overall_rating = (humor_score + creativity_score + timeliness_score + personalization_score
                          + tone_and_style_score + adaptability_score + user_engagement_score
                          + appropriate_content_score + diversity_score + delivery_score + sentiment_score) / 11.0

        # Return the overall rating
        return overall_rating
