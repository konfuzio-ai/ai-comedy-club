"""
Joke Generator Model and Training

This module defines a class for training and fine-tuning a joke generator model based on the GPT-2 architecture.
It includes functions to initialize the model, fine-tune it, and evaluate its performance.

Author: Raigon Augustin
Date: 17.08.2023
"""

# Import necessary modules and classes
from transformers import GPT2LMHeadModel, GPT2Tokenizer, Trainer, DataCollatorForLanguageModeling
import pandas as pd


class ModelJokeGenerator:
    """
    Joke Generator Model

    This class encapsulates a joke generator model based on the GPT-2 architecture.
    It provides methods for fine-tuning the model and evaluating its performance.

    Args:
        modelName (str): The name of the pretrained GPT-2 model to use.

    Attributes:
        tokenizer (GPT2Tokenizer): The tokenizer for the model.
        model (GPT2LMHeadModel): The GPT-2 model for joke generation.
        modelName (str): The name of the model.
        data_collator (DataCollatorForLanguageModeling): The data collator for language modeling.
    """

    def __init__(self, modelName):
        """
        Initialize the Joke Generator Model.

        Args:
             modelName (str): The name of the pretrained GPT-2 model to use.
        """
        self.tokenizer = GPT2Tokenizer.from_pretrained(modelName)
        self.model = GPT2LMHeadModel.from_pretrained(modelName)
        self.modelName = modelName
        self.data_collator = DataCollatorForLanguageModeling(tokenizer=self.tokenizer, mlm=False)

    def fine_tune(self, training_args, train_dataset, eval_dataset, test_dataset):
        """
        Fine-tune the model using the provided datasets.

        Args:
            training_args (TrainingArguments): The training arguments for fine-tuning.
            train_dataset (Dataset): The training dataset.
            eval_dataset (Dataset): The evaluation dataset.
            test_dataset (Dataset): The test dataset.

        Returns:
            pandas.DataFrame: A DataFrame containing the training history.
        """
        trainer = Trainer(
            model=self.model,
            args=training_args,
            data_collator=self.data_collator,
            train_dataset=train_dataset,
            eval_dataset=eval_dataset,
        )

        trainer.train()

        trainer.save_model("models/joke_gen_model")

        train_history_frame = pd.DataFrame(trainer.state.log_history)

        evaluation_results = trainer.evaluate(test_dataset)
        print(evaluation_results)

        return train_history_frame
