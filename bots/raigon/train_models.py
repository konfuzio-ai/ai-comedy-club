"""
This Python file contains the function for training the joke-generator and joke-rater models
"""
from transformers import AdamW, TrainingArguments, get_linear_schedule_with_warmup

import config
import data_util
from model_joke_generator import ModelJokeGenerator
from model_joke_rater import ModelJokeRater


def train_joke_rater(training_config, data_frame):

    model_obj = ModelJokeRater(training_config.model_name, training_config.num_labels)

    tokenized_train_dataset, tokenized_test_dataset, tokenized_val_dataset = data_util.create_datasets_for_training(
        training_config.task, data_frame, model_obj.tokenizer)

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

    optimizer = AdamW(model_obj.model.parameters(), lr=2e-5)

    scheduler = get_linear_schedule_with_warmup(
        optimizer,
        num_warmup_steps=0,
        num_training_steps=len(tokenized_train_dataset) * 5
    )

    train_history_frame = model_obj.fine_tune(training_args, optimizer, scheduler, tokenized_train_dataset, tokenized_val_dataset, tokenized_test_dataset)

    return


def train_joke_generator(training_config, data_frame):

    model_obj = ModelJokeGenerator(training_config.model_name)

    tokenized_train_dataset, tokenized_test_dataset, tokenized_val_dataset = data_util.create_datasets_for_training(training_config.task, data_frame, model_obj.tokenizer)

    tokenized_train_dataset = tokenized_train_dataset.remove_columns(['label'])
    tokenized_test_dataset = tokenized_test_dataset.remove_columns(['label'])
    tokenized_val_dataset = tokenized_val_dataset.remove_columns(['label'])

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

    train_history_frame = model_obj.fine_tune(training_args, tokenized_train_dataset, tokenized_val_dataset, tokenized_test_dataset)

    return


if __name__ == '__main__':
    jokes_data_frame = data_util.load_data()

    jokes_data_frame.columns = ['label', 'joke']
    jokes_data_frame['wc'], jokes_data_frame['joke_len'] = data_util.get_joke_stats(jokes_data_frame['joke'].tolist())

    train_joke_generator(config.JokeGeneratorModelConfig, jokes_data_frame)
    train_joke_rater(config.JokeRaterModelConfig, jokes_data_frame)





