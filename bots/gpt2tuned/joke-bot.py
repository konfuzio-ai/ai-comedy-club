import gpt_2_simple as gpt2
import os
import configparser
from datetime import datetime
import torch
from transformers import BertTokenizer, BertForSequenceClassification, pipeline

config = configparser.ConfigParser()
config.read(os.path.join("fine-tuning", "conf.ini"))
run_name = config["DEFAULT"]["RunName"]

checkpoint_dir = os.path.join(os.getcwd(), "fine-tuning", "checkpoint")
sess = gpt2.start_tf_sess()
gpt2.load_gpt2(sess, checkpoint_dir=checkpoint_dir, run_name=run_name)


class Bot:
    def __init__(self):
        # Loading models
        self.regression_pipeline = pipeline("text-classification", model='bert-base-uncased', return_all_scores=True)
        self.classifier = pipeline("zero-shot-classification")

    def text_generation(self):
        text = gpt2.generate(sess, checkpoint_dir=checkpoint_dir, run_name=run_name, length=50, prefix="[JOKE]",
                             return_as_list=True)
        return text[0].replace("[JOKE] : ", "")

    def rate_joke(self, joke):
        result = self.regression_pipeline(joke)
        # Range from 1 to 10
        score = result[0]['score']
        scaled_score = (score * 10).round()

        # Logic evaluation
        result = self.classifier(joke, candidate_labels=["logical", "not logical"])
        # pring result and logic
        print(f"logical or not {result}")
        print(f"Logic mark: {scaled_score}/10")
        return


def main():
    print(f"Greetings and have a good {datetime.now().strftime('%A')}! Here is a joke: ")


if __name__ == "__main__":
    Bot().rate_joke("I am gay!")
    Bot().rate_joke(Bot().text_generation())