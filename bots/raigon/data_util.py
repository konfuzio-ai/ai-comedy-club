"""
This Python file contains necessary functions to load data and to explore the data
"""
import shutil
import requests
import config
import gzip
import os
import pandas as pd
from preprocessing import Preprocessing
from sklearn.model_selection import train_test_split
from datasets import load_dataset, Dataset


def load_data():

    if os.path.exists(config.FileConfig.uncompressed_data_file):
        return pd.read_csv(config.FileConfig.uncompressed_data_file, delimiter='\t', error_bad_lines=False)
    response = requests.get(config.FileConfig.data_file_url)
    if response.status_code == 200:

        # Saving the compressed file
        with open(config.FileConfig.compressed_data_file, 'wb') as fp:
            for chunk in response.iter_content(chunk_size=8192):
                fp.write(chunk)

        # Extracting the compressed file
        with gzip.open(config.FileConfig.compressed_data_file, 'rb') as f_in:
            with open(config.FileConfig.uncompressed_data_file, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)

        print('File downloaded and decompressed successfully!')

        return pd.read_csv(config.FileConfig.uncompressed_data_file, delimiter='\t', error_bad_lines=False)

    else:
        print('Failed to download the file.')
        exit(0)

    return


def get_joke_stats(list_of_jokes):
    word_count = []
    joke_length = []
    for joke in list_of_jokes:
        word_count.append(len(joke.split()))
        joke_length.append(len(joke))

    return word_count, joke_length


def remove_newlines_and_carriage_returns(self, text):
    text = text.strip()
    cleaned_text = text.replace('\n', '').replace('\r', '')
    return cleaned_text


def create_short_jokes_dataset(self, frame, min_length, max_length):
    """
    This function removes jokes which are below min_length and above max_length
    """
    frame = frame[frame['joke_len'] > min_length]
    frame = frame[frame['joke_len'] < max_length]

    return frame


def create_datasets_for_training(task: str, frame: pd.DataFrame, tokenizer):
    preprocess_obj = Preprocessing(frame)
    if task == 'generation':
        frame_after_preprocessing = preprocess_obj.preprocess_data_for_joke_generator()
        tokenizer.pad_token = '<|pad|>'
    else:
        frame_after_preprocessing = preprocess_obj.preprocess_data_for_joke_rater()

    train_data, temp_data = train_test_split(frame_after_preprocessing, test_size=1 - config.DataSetConfig.train_ratio, random_state=45)
    val_data, test_data = train_test_split(temp_data, test_size=config.DataSetConfig.test_ratio / (config.DataSetConfig.test_ratio + config.DataSetConfig.val_ratio), random_state=45)

    train_dataset = Dataset.from_pandas(train_data[['joke', 'label']])
    test_dataset = Dataset.from_pandas(test_data[['joke', 'label']])
    val_dataset = Dataset.from_pandas(val_data[['joke', 'label']])

    def tokenize_text(data_item):
        return tokenizer(data_item['joke'], padding="max_length", truncation=True)

    tokenized_train_dataset = train_dataset.map(tokenize_text, batched=True)
    tokenized_test_dataset = test_dataset.map(tokenize_text, batched=True)
    tokenized_val_dataset = val_dataset.map(tokenize_text, batched=True)

    return tokenized_train_dataset, tokenized_test_dataset, tokenized_val_dataset


if __name__ == '__main__':
    load_data()
