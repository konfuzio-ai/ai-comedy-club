import re
import numpy as np
import tensorflow as tf
from textblob import TextBlob
import pandas as pd

START_TOKEN = '<|im_start|>'
END_TOKEN = ' <|end|>'


def get_optimal_token_with_exploration(token_probabilities, num_explore=5):
    """
    Get the optimal token with exploration. This will be a random choice from 
    the top most probable tokens.

    Parameters:
    token_probabilities (numpy array): Array of token probabilities.
    num_explore (int): Number of tokens to explore.

    Returns:
    optimal_token_id (int): ID of the optimal token.
    """
    top_token_indices = np.argpartition(token_probabilities, -num_explore)[-num_explore:]
    normalized_probabilities = token_probabilities[top_token_indices]
    normalized_probabilities /= np.sum(normalized_probabilities)
    random_choice = np.random.choice(num_explore, 1, p=normalized_probabilities)
    optimal_token_id = int(top_token_indices[random_choice][0])
    return optimal_token_id


def clean_text(text):
    """
    Clean the model output text.

    Parameters:
    text (str): Input text to clean.

    Returns:
    text (str): Cleaned text.
    """
    text = text.replace(START_TOKEN, '').strip()
    text = text.rstrip('<').strip()
    text = re.sub('^[^a-zA-Z0-9]*', '', text)
    return text


def create_joke(initial_joke, joke_max_length, model, tokenizer):
    """
    Create a joke using a model and tokenizer.

    Parameters:
    initial_joke (str): Initial part of the joke.
    joke_max_length (int): Maximum length of the joke.
    model (TFGPT2LMHeadModel): Pre-trained model.
    tokenizer (GPT2Tokenizer): Tokenizer.

    Returns:
    joke (str): Generated joke.
    """
    for position in range(joke_max_length):
        model_output = model(initial_joke)
        output_logits = model_output[0]
        softmax_output_logits = tf.nn.softmax(output_logits[0, -1], axis=0).numpy()
        if position == 0:
            explore_len = 50
        elif position < 4:
            explore_len = 15
        else:
            explore_len = 4
        next_token = get_optimal_token_with_exploration(softmax_output_logits, explore_len)
        initial_joke = tf.concat([initial_joke, tf.ones((1, 1), dtype=tf.int32)*next_token], axis=1)
        if next_token in tokenizer.encode(END_TOKEN):
            return tokenizer.decode(list(tf.squeeze(initial_joke).numpy()))
    return ''


def preprocess_text(text, tokenizer, model):
    """
    Preprocess the input text.

    Parameters:
    text (str): Input text to preprocess.
    tokenizer (AutoTokenizer): Tokenizer.
    model (TFAutoModel): Pre-trained model.

    Returns:
    df_text (DataFrame): Preprocessed text.
    """
    inputs = tokenizer([text], return_tensors='tf', truncation=True, padding=True, max_length=512)
    outputs = model(inputs)
    text_embeddings = outputs.last_hidden_state[:, 0, :].numpy()
    sentiment = TextBlob(text).sentiment
    polarity = sentiment.polarity
    subjectivity = sentiment.subjectivity
    df_text = pd.DataFrame(text_embeddings)
    df_text['polarity'] = polarity
    df_text['subjectivity'] = subjectivity

    return df_text