from transformers import pipeline


MAX_LEN_SEQ: int = 510
MODEL: str = "mohameddhiab/humor-no-humor"


class HumorJudge:
    '''
    This class is used to judge if the joke is funny or not.
    It uses a fine-tuned DistilBERT model to extract a humor score.
    It was pretrained on a dataset composed of jokes and non-jokes.
    The kaggle notebook used for training can be found here:
    https://www.kaggle.com/code/mohamedaminedhiab/humor-no-humor-train (Which got liked by Kaggle's 20th notebook's Grandmaster @vencerlanz09)
    '''

    def __init__(self, device: str):
        self.humor_classifier = pipeline(
            model=MODEL, device=device, truncation=True, max_length=MAX_LEN_SEQ)

    def score(self, joke):
        '''
        Returns the Humor score of the joke
        '''
        output = self.humor_classifier(joke)
        # get the humor score if the joke is classified as a joke else the score should be 0 (no humor)
        score = output[0]['score'] if output[0]['label'] == 'HUMOR' else 0
        # convert score from [0, 1] to [0, 10]
        score *= 10
        return score
