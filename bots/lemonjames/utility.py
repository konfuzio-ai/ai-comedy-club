import shutil
import requests
import config
import gzip
import os
import pandas as pd
from preprocessing import Preprocessing
from sklearn.model_selection import train_test_split
from datasets import load_dataset, Dataset
import numpy as np

def choose_from_top(probs, n=5):
    """
        Function to first select top N tokens from the probability list and then
        based on the selected N word distribution get random token ID

        Args:
            probs (List): list of probablities for a given token
            n (int): the number of tokens to consider

        Returns:
            idx the chosen token
    """
    ind = np.argpartition(probs, -n)[-n:]
    top_prob = probs[ind]
    top_prob = top_prob / np.sum(top_prob) # Normalize
    choice = np.random.choice(n, 1, p = top_prob)
    token_id = ind[choice][0]
    return int(token_id)

def find_string_between_occurrences(main_string, substring):
    """
        Returns the string enclosed by the first two occurences of the substring
        in the main_string.

        Args:
            main_string (str): The bigger string to traverse
            substring (str): The substring that we are using as a start and end token

        Returns:
            result_string (str): The string enclosed by the first two occurences of
            the substring
    """
    first_occurrence = main_string.find(substring)
    
    if first_occurrence != -1:
        second_occurrence = main_string.find(substring, first_occurrence + len(substring))
        
        if second_occurrence != -1:
            start_index = first_occurrence + len(substring)
            end_index = second_occurrence
            result_string = main_string[start_index:end_index]
            return result_string

def get_joke_stats(list_of_jokes):
    """
        Compute statistics (word count and length) for a list of jokes.
        Args:
            list_of_jokes (list): A list of jokes.
        Returns:
            tuple: A tuple containing lists of word counts and joke lengths.
    """
    word_count = []
    joke_length = []
    for joke in list_of_jokes:
        word_count.append(len(joke.split()))
        joke_length.append(len(joke))

    return word_count, joke_length

def create_train_dataset(df: pd.DataFrame, tokenizer):
    """
        Args:
            df (DataFrame): Input DataFrame containing jokes and labels.
            tokenizer (Tokenizer): The tokenizer for tokenizing sequences
        Returns:
            tuple: A tuple containing tokenized training, test, and validation datasets.
    """

    preprocesser = Preprocessing(df)

    frame_after_preprocessing = preprocesser.preprocess_data_for_joke_rater()
    tokenizer.pad_token = '<|pad|>'

    train_data, test_data = train_test_split(frame_after_preprocessing, train_size=config.DataSetConfig.train_ratio, random_state=45)

    train_dataset = Dataset.from_pandas(train_data[['joke', 'label']])
    test_dataset = Dataset.from_pandas(test_data[['joke', 'label']])

    tokenized_train_dataset = train_dataset.map(lambda df: tokenizer(df['joke'], padding="max_length", truncation=True), batched=True)
    tokenized_test_dataset = test_dataset.map(lambda df: tokenizer(df['joke'], padding="max_length", truncation=True), batched=True)

    return tokenized_train_dataset, tokenized_test_dataset