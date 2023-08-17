from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer
import evaluate
import pandas as pd
import numpy as np


class ModelJokeRater:

    def __init__(self, modelName, num_labels):
        self.tokenizer = AutoTokenizer.from_pretrained(modelName)
        self.model = AutoModelForSequenceClassification.from_pretrained(modelName, num_labels=num_labels)
        self.modelName = modelName

    @staticmethod
    def compute_metrics(eval_preds):
        metric = evaluate.load("accuracy")
        logits, labels = eval_preds
        predictions = np.argmax(logits, axis=1)
        return metric.compute(predictions=predictions, references=labels)

    def fine_tune(self, training_args, optimizer, scheduler, train_dataset, eval_dataset, test_dataset):
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