from transformers import GPT2LMHeadModel, GPT2Tokenizer, Trainer, DataCollatorForLanguageModeling
import pandas as pd


class ModelJokeGenerator:

    def __init__(self, modelName):
        self.tokenizer = GPT2Tokenizer.from_pretrained(modelName)
        self.model = GPT2LMHeadModel.from_pretrained(modelName)
        self.modelName = modelName
        self.data_collator = DataCollatorForLanguageModeling(tokenizer=self.tokenizer, mlm=False)

    def fine_tune(self, training_args, train_dataset, eval_dataset, test_dataset):
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
