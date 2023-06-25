from transformers import pipeline


TASK: str = "zero-shot-classification"
MODEL: str = "facebook/bart-large-mnli"
CANDIDATE_LABELS: list = ["asks for engagement", "no engagement"]


class EngagementJudge:
    '''
    This class is used to judge the Engagement score of a joke
    '''

    def __init__(self, device: str):
        self.approp_classifier = pipeline(TASK,
                                          model=MODEL, device=device)
        self.candidate_labels = CANDIDATE_LABELS

    def score(self, joke):
        '''
        Returns the User Engagement score of the joke
        '''
        candidate_labels = self.candidate_labels
        output = self.approp_classifier(joke, candidate_labels)
        # get the index of "not dark humour" label
        idx = output['labels'].index(candidate_labels[0])
        # get the appropriateness score
        score = output['scores'][idx]
        # convert score from [0, 1] to [0, 10]
        score *= 10
        return score
