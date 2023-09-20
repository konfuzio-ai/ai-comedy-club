"""
Joke Model Training Utilities

This module provides utility functions for training joke-related machine learning models.
It includes functions to train both joke rater and joke generator models.

Author: Raigon Augustin
Date: 17.08.2023
"""

# Import necessary modules and classes

from transformers import AdamW, TrainingArguments, get_linear_schedule_with_warmup
import config
import data_util
from model_joke_generator import ModelJokeGenerator
from model_joke_rater import ModelJokeRater


def train_joke_rater(training_config, data_frame):
    """
        Train a joke rater model using the provided configuration and data.

        Args:
            training_config (TrainingConfig): An object containing training configuration settings.
            data_frame (pandas.DataFrame): A DataFrame containing the training data.

        Returns:
            pandas.DataFrame: A DataFrame containing the training history.
    """

    # Initialize joke rater model
    model_obj = ModelJokeRater(training_config.model_name, training_config.num_labels)

    # Tokenize datasets for training
    tokenized_train_dataset, tokenized_test_dataset, tokenized_val_dataset = data_util.create_datasets_for_training(
        training_config.task, data_frame, model_obj.tokenizer)

    # Set up training arguments
    training_args = TrainingArguments(
        output_dir=training_config.output_dir,
        num_train_epochs=training_config.num_train_epochs,
        per_device_train_batch_size=training_config.per_device_train_batch_size,
        per_device_eval_batch_size=training_config.per_device_eval_batch_size,
        save_steps=training_config.save_steps,
        save_total_limit=training_config.save_total_limit,
        evaluation_strategy=training_config.evaluation_strategy,
        logging_steps=training_config.logging_steps,
        learning_rate=training_config.learning_rate,
        logging_dir=training_config.logging_dir,
        report_to=training_config.report_to
    )

    # Create optimizer and scheduler
    optimizer = AdamW(model_obj.model.parameters(), lr=2e-5)

    scheduler = get_linear_schedule_with_warmup(
        optimizer,
        num_warmup_steps=0,
        num_training_steps=len(tokenized_train_dataset) * 5
    )

    # Fine-tune the model
    train_history_frame = model_obj.fine_tune(training_args, optimizer, scheduler, tokenized_train_dataset, tokenized_val_dataset, tokenized_test_dataset)

    return train_history_frame


def train_joke_generator(training_config, data_frame):
    """
        Train a joke generator model using the provided configuration and data.

        Args:
            training_config (TrainingConfig): An object containing training configuration settings.
            data_frame (pandas.DataFrame): A DataFrame containing the training data.

        Returns:
            pandas.DataFrame: A DataFrame containing the training history.
    """

    # Initialize joke generator model
    model_obj = ModelJokeGenerator(training_config.model_name)

    # Tokenize datasets for training and remove 'label' column
    tokenized_train_dataset, tokenized_test_dataset, tokenized_val_dataset = data_util.create_datasets_for_training(training_config.task, data_frame, model_obj.tokenizer)

    tokenized_train_dataset = tokenized_train_dataset.remove_columns(['label'])
    tokenized_test_dataset = tokenized_test_dataset.remove_columns(['label'])
    tokenized_val_dataset = tokenized_val_dataset.remove_columns(['label'])

    # Set up training arguments
    training_args = TrainingArguments(
        output_dir=training_config.output_dir,
        num_train_epochs=training_config.num_train_epochs,
        per_device_train_batch_size=training_config.per_device_train_batch_size,
        per_device_eval_batch_size=training_config.per_device_eval_batch_size,
        save_steps=training_config.save_steps,
        save_total_limit=training_config.save_total_limit,
        evaluation_strategy=training_config.evaluation_strategy,
        logging_steps=training_config.logging_steps,
        learning_rate=training_config.learning_rate,
        logging_dir=training_config.logging_dir,
        report_to=training_config.report_to
    )

    # Fine-tune the model
    train_history_frame = model_obj.fine_tune(training_args, tokenized_train_dataset, tokenized_val_dataset, tokenized_test_dataset)

    return train_history_frame


if __name__ == '__main__':
    jokes_data_frame = data_util.load_data()

    jokes_data_frame.columns = ['label', 'joke']
    jokes_data_frame['wc'], jokes_data_frame['joke_len'] = data_util.get_joke_stats(jokes_data_frame['joke'].tolist())

    train_joke_generator(config.JokeGeneratorModelConfig, jokes_data_frame)
    train_joke_rater(config.JokeRaterModelConfig, jokes_data_frame)





