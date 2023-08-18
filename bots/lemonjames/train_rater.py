import pandas as pd
import torch

from transformers import AdamW, TrainingArguments, get_linear_schedule_with_warmup

from joke_bot import Bot
from config import JokeRaterModelConfig
from utility import create_train_dataset

def train_rater(training_config, dataset):
    """
        Train the rater model of the Joker Bot

        Args:
            training_config (TrainingConfig): Configuration settings for training
            data_frame (pandas.DataFrame): Training Dataset
    """

    joking_bot = Bot()
    model = joking_bot.model_rate

    tokenized_train_dataset, tokenized_test_dataset = create_train_dataset(dataset, joking_bot.tokenizer)

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
    )

    # Create optimizer and scheduler
    optimizer = torch.optim.AdamW(model.parameters(), lr=2e-5)

    scheduler = get_linear_schedule_with_warmup(
        optimizer,
        num_warmup_steps=0,
        num_training_steps=len(tokenized_train_dataset) * 5
    )

    evaluation_rating = joking_bot.tune_rater(training_args, optimizer, scheduler, tokenized_train_dataset, tokenized_test_dataset)

    return evaluation_rating

if __name__ == "__main__":
    jokes_df = pd.read_csv("dataset/train.tsv", delimiter='\t', on_bad_lines='skip')

    jokes_df.columns = ['label', 'joke']

    joke_len = []
    for joke in jokes_df['joke'].tolist():
        joke_len.append(len(joke))
    
    jokes_df['joke_len'] = joke_len

    train_rater(JokeRaterModelConfig, jokes_df)