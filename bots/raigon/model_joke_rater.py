"""
Joke Rater Model and Training

This module defines a class for training and fine-tuning a joke rater model based on the Hugging Face Transformers library.
It includes functions to initialize the model, fine-tune it, and evaluate its performance.

Author: [Your Name]
Date: [Date]
"""

# Import necessary modules and classes

from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer
import evaluate
import pandas as pd
import numpy as np


class ModelJokeRater:
    """
    Joke Rater Model

    This class encapsulates a joke rater model based on a sequence classification architecture.
    It provides methods for fine-tuning the model and evaluating its performance.

    Args:
        modelName (str): The name of the pretrained model to use.
        num_labels (int): The number of classification labels.

    Attributes:
        tokenizer (AutoTokenizer): The tokenizer for the model.
        model (AutoModelForSequenceClassification): The sequence classification model.
        modelName (str): The name of the model.
    """

    def __init__(self, modelName, num_labels):
        """
        Initialize the Joke Rater Model.

        Args:
            modelName (str): The name of the pretrained model to use.
            num_labels (int): The number of classification labels.
        """
        self.tokenizer = AutoTokenizer.from_pretrained(modelName)
        self.model = AutoModelForSequenceClassification.from_pretrained(modelName, num_labels=num_labels)
        self.modelName = modelName

    @staticmethod
    def compute_metrics(eval_preds):
        """
        Compute classification metrics for evaluation predictions.

        Args:
            eval_preds (tuple): A tuple containing logits and labels.

        Returns:
            float: The computed metric value.
        """
        metric = evaluate.load("accuracy")
        logits, labels = eval_preds
        predictions = np.argmax(logits, axis=1)
        return metric.compute(predictions=predictions, references=labels)

    def fine_tune(self, training_args, optimizer, scheduler, train_dataset, eval_dataset, test_dataset):
        """
        Fine-tune the model using the provided datasets.

        Args:
            training_args (TrainingArguments): The training arguments for fine-tuning.
            optimizer: The optimizer for training.
            scheduler: The scheduler for training.
            train_dataset (Dataset): The training dataset.
            eval_dataset (Dataset): The evaluation dataset.
            test_dataset (Dataset): The test dataset.

        Returns:
            pandas.DataFrame: A DataFrame containing the training history.
        """
        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=train_dataset,
            eval_dataset=eval_dataset,
            optimizers=(optimizer, scheduler),
            compute_metrics=self.compute_metrics,
        )

        trainer.train()

        trainer.save_model("models/joke_rater_model")

        train_history_frame = pd.DataFrame(trainer.state.log_history)

        evaluation_results = trainer.evaluate(test_dataset)
        print(evaluation_results)

        return train_history_frame