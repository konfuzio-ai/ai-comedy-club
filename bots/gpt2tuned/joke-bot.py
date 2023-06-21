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
        # Final mark (0-10)
        self.mark = 0

    def text_generation(self):
        text = gpt2.generate(sess, checkpoint_dir=checkpoint_dir, run_name=run_name, length=50, prefix="[JOKE]",
                             return_as_list=True)
        return text[0].replace("[JOKE] : ", "")

    def rate_joke(self, joke):
        result = self.regression_pipeline(joke)[0]
        # Logical evaluation from bert-base-uncased on Regression
        score = result[0]['score']
        logic_score_1 = round(score*3) + 1

        # Logic evaluation based zero-shot classification with two parameters
        result = self.classifier(joke, candidate_labels=["logical", "not logical"])['scores'][0]
        logic_score_2 = round(result*3) + 1

        # average count of words - https://insidegovuk.blog.gov.uk/2014/08/04/sentence-length-why-25-words-is-our-limit/
        if len(joke.split()) in range(5, 16):
            self.mark += 1
        # number of unique words
        joke = joke.lower().split()
        if len(set(joke)) < len(joke):
            self.mark += (len(joke) - len(set(joke)))/10

        self.mark += (logic_score_1 + logic_score_2)
        # print result and logic
        print(f"Logic score 1 : {logic_score_1}/4")
        print(f"Logic score 2:  {logic_score_2}/4")
        print(f"Final score {self.mark}")
        return


def main():
    print(f"Greetings and have a good {datetime.now().strftime('%A')}! Here is a joke: ")


if __name__ == "__main__":
    Bot().rate_joke("I am gay!")
    Bot().rate_joke(Bot().text_generation())
