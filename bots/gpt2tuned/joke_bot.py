import gpt_2_simple as gpt2
import os
from transformers import pipeline
import logging

logging.disable(logging.WARNING)


class Bot:
    name = "GPT2Tuned"
    checkpoint_dir = os.path.join(os.getcwd(), "fine-tuning", "checkpoint")

    def __init__(self):
        # Loading models
        self.regression_pipeline = pipeline("text-classification", model='bert-base-uncased')
        self.classifier = pipeline("zero-shot-classification", model='bert-base-uncased')
        # Final mark (0-10)
        self.mark = 0

    def tell_joke(self):
        if "gpt2tuned" not in self.checkpoint_dir:
            self.checkpoint_dir = os.path.join(os.getcwd(), "bots", "gpt2tuned", "fine-tuning", "checkpoint")
        if os.path.isdir(self.checkpoint_dir):
            sess = gpt2.start_tf_sess()
            gpt2.load_gpt2(sess, checkpoint_dir=self.checkpoint_dir, run_name="shortjokes")
            text = gpt2.generate(sess, checkpoint_dir=self.checkpoint_dir, run_name="shortjokes", length=50,
                                 prefix="[JOKE]",
                                 return_as_list=True)
            text = text[0].replace("[JOKE] : ", "")
            if "[EOS]" in text:
                text = text[:text.index('[') - 1]
            return text
        else:
            # if we didn't fine-tune dataset use already learned model
            short_joke_pipe = pipeline(
                'text-generation', model='AlekseyKorshuk/gpt2-jokes')
            return short_joke_pipe( max_length=50, do_sample=True)[0]['generated_text']

    def rate_joke(self, joke):
        self.mark = 0
        print(joke)
        result = self.regression_pipeline(joke)
        # Logical evaluation from bert-base-uncased on Regression
        score = result[0]['score']
        logic_score_1 = round(score*10)

        # Logic evaluation based zero-shot classification with two parameters
        result = self.classifier(joke, candidate_labels=["logical", "not logical"])['scores'][0]
        logic_score_2 = round(result*10)

        # average count of words - https://insidegovuk.blog.gov.uk/2014/08/04/sentence-length-why-25-words-is-our-limit/
        if len(joke.split()) in range(5, 16):
            print("One point for length criteria")
            self.mark += 1

        self.mark += (logic_score_1 + logic_score_2) // 2
        # print result and logic
        print(f"Logic score 1 : {logic_score_1}/10")
        print(f"Logic score 2:  {logic_score_2}/10")
        print(f"Final score {self.mark}")
        return int(self.mark)

