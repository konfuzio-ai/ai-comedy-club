from transformers import pipeline


MAX_LEN_SEQ: int = 510
MODEL: str = "mohameddhiab/humor-no-humor"
MODEL_RATING: str = "mohameddhiab/rate-jokes-bert-v5"


class HumorJudge:
    '''
    This class is used to judge if the joke is funny or not.
    It uses a fine-tuned DistilBERT model to extract a humor score.
    It was pretrained on a dataset composed of jokes and non-jokes.
    The kaggle notebook used for training can be found here:
    https://www.kaggle.com/code/mohamedaminedhiab/humor-no-humor-train (Which got liked by Kaggle's 20th notebook's Grandmaster @vencerlanz09)

    If humor is detected, it will use another fine-tuned DistilBERT model to rate the joke. 
    '''

    def __init__(self, device: str):
        self.humor_classifier = pipeline(
            model=MODEL, device=device, truncation=True, max_length=MAX_LEN_SEQ)
        self.humor_rater = pipeline(
            model=MODEL_RATING, device=device, truncation=True, max_length=MAX_LEN_SEQ, return_all_scores=True)

    def score(self, joke):
        '''
        Returns the Humor score of the joke
        '''
        output = self.humor_classifier(joke)
        # check if the joke contains humor (it ain't a joke if it ain't funny)
        is_humor = True if output[0]['label'] == 'HUMOR' else False
        # if humor is detected then rate it
        if is_humor:
            rater_output = self.humor_rater(joke)
            # get the rating score by summing the products of the probabilities and the labels
            rating_score = sum([label_score_pair['score']*int(label_score_pair['label'])
                                for label_score_pair in rater_output[0]])
            return (rating_score)
        return 0
