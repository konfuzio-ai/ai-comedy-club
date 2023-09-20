from transformers import pipeline
from typing import List, Dict, Union
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

class JokeRaterHelper:
    """
    This class is designed to rate jokes based on sentiment analysis. 
    It utilizes the pretrained DistilBERT model and the VADER sentiment analysis tool from NLTK.
    """
    
    def __init__(self):
        """
        Initializes the JokeRaterHelper class. Two class properties are declared,
        self.distilbert and self.vader, which will be initialized when their respective 
        methods are called for the first time.
        """
        self.distilbert = None
        self.vader = None

    def rate_distilbert(self, joke: str) -> float:
        """
        Rates a joke using a pretrained DistilBERT model for emotion classification.

        :param joke: The joke to be rated, as a string.
        :return: The rating of the joke, as a float between 0 and 1.
        """
        if not self.distilbert:
            self.distilbert = pipeline("text-classification",model='bhadresh-savani/distilbert-base-uncased-emotion', return_all_scores=True)
        scores = self.distilbert(joke)[0]
        return self.compute_score_distilbert(scores)

    def compute_score_distilbert(self, scores: List[Dict[str, float]]) -> float:
        """
        Computes a final joke rating from the scores provided by the DistilBERT model.
        The final score favors positive emotions.

        :param scores: A list of dictionaries containing emotion labels and scores.
        :return: The final joke rating, as a float between 0 and 1.
        """
        scores = {result['label']: result['score'] for result in scores}  

        weights = {
            'sadness': 0.2,
            'joy': 0.4,
            'love': 0.4,
            'anger': 0.2,
            'fear': 0.2,
            'surprise': 0.2
        }

        positive_emotions = sum(scores[emotion] * weights[emotion] for emotion in ['joy', 'love', 'surprise'])
        negative_emotions = sum(scores[emotion] * weights[emotion] for emotion in ['anger', 'fear', 'sadness'])

        score = positive_emotions + (1 - negative_emotions)
        score = min(1, max(0, score))

        return score
    
    def rate_vader(self, joke: str) -> float:
        """
        Rates a joke using the VADER sentiment analysis tool from NLTK.

        :param joke: The joke to be rated, as a string.
        :return: The rating of the joke, as a float between 0 and 1.
        """
        if not self.vader:
            nltk.download('vader_lexicon')
            self.vader = SentimentIntensityAnalyzer()
        
        compound_score = self.vader.polarity_scores(joke)['compound']
        score = (compound_score + 1) / 2
        return score
    
    def rate_bert_vader(self, joke: str) -> float:
        """
        Computes an overall joke rating by averaging the ratings from DistilBERT and VADER.

        :param joke: The joke to be rated, as a string.
        :return: The overall rating of the joke, as a float between 0 and 1.
        """
        score_distilbert = self.rate_distilbert(joke)
        score_vader = self.rate_vader(joke)
        return (score_distilbert + score_vader) / 2
