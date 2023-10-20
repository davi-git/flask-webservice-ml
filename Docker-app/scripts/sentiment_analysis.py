# For Vader
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# For TextBlob
from textblob import TextBlob

# For Flair
import flair


# Sentiment Analysis class
class SA:
    def __init__(self) -> None:
        self._text = ""
        self._pos_threshold = None
        self._neg_threshold = None
        self._threshold = None
    
    # "text" getter function
    @property
    def text(self) -> None:
        return self._text
    
    # "text" setter function
    @text.setter
    def text(self, t) -> None:
        self._text = t

    # "pos_threshold" getter function
    @property
    def pos_threshold(self) -> None:
        return self._pos_threshold
    
    # "pos_threshold" setter function
    @pos_threshold.setter
    def pos_threshold(self, x) -> None:
        try:
            self._pos_threshold = float(x)
        except:
            self._pos_threshold = None
    
    # "neg_threshold" getter function
    @property
    def neg_threshold(self) -> None:
        return self._neg_threshold
    
    # "neg_threshold" setter function
    @neg_threshold.setter
    def neg_threshold(self, x) -> None:
        try:
            self._neg_threshold = float(x)
        except:
            self._neg_threshold = None
    
    # "threshold" getter function
    @property
    def threshold(self) -> None:
        return self._threshold
    
    # "threshold" setter function
    @threshold.setter
    def threshold(self, x) -> None:
        try:
            self._threshold = float(x)
        except:
            self._threshold = None
    
    def vader(self, text, pos_threshold=0.3, neg_threshold=-0.3):
        '''
        Perform Sentiment Analysis on specified text using Vader model.

        - text: string to analyze

        - pos_threshold [Optional]: threshold used to classify positive cases (score upper than pos_threshold). Default: 0.3

        - neg_threshold [Optional]: threshold used to classify negative cases (score lower than neg_threshold). Default: -0.3

        Return a tuple of the form (label, score).
        The label is a string representing the sentiment of the text as either "positive", "negative" or "neutral".
        The compound score is a normalized, weighted composite score that ranges from -1 (most negative) to 1 (most positive).
        '''

        self.text = text
        self.pos_threshold = pos_threshold
        self.neg_threshold = neg_threshold

        analyzer = SentimentIntensityAnalyzer()
        try:
            scores = analyzer.polarity_scores(self.text)
        except:
            return ""
        
        # 'scores' variable contains a dictionary of scores for four different sentiment categories: neg, neu, pos, and compound.
        # The neg and pos scores represent the negative and positive sentiment of the text, respectively, and range from 0 to 1.
        # The neu score represents the neutral sentiment and ranges from 0 to 1.
        # The compound score is a normalized, weighted composite score that ranges from -1 (most negative) to 1 (most positive).

        comp = scores['compound']

        if comp > self.pos_threshold:
            sentiment = 'positive'
        elif comp < self.neg_threshold:
            sentiment = 'negative'
        else:
            sentiment = 'neutral'

        return (sentiment, comp)
    

    def textBlob(self, text, pos_threshold=0.2, neg_threshold=-0.1):
        '''
        Perform Sentiment Analysis on specified text using TextBlob model.

        - text: string to analyze

        - pos_threshold [Optional]: threshold used to classify positive cases (score upper than pos_threshold). Default: 0.2

        - neg_threshold [Optional]: threshold used to classify negative cases (score lower than neg_threshold). Default: -0.1

        Return a tuple of the form (label, polarity).
        The label is a string representing the sentiment of the text as either "positive", "negative" or "neutral".
        The polarity score is a float within the range [-1.0, 1.0].
        '''

        self.text = text
        self.pos_threshold = pos_threshold
        self.neg_threshold = neg_threshold

        try:
            blob = TextBlob(self.text)
            scores = blob.sentiment
        except:
            return ""
        
        # 'scores' variable contains a namedtuple of the form Sentiment(polarity, subjectivity).
        # The polarity score is a float within the range [-1.0, 1.0].
        # The subjectivity is a float within the range [0.0, 1.0] where 0.0 is very objective and 1.0 is very subjective.

        pol = scores.polarity
        subj = scores.subjectivity

        if pol > self.pos_threshold:
            sentiment = 'positive'
        elif pol < self.neg_threshold:
            sentiment = 'negative'
        else:
            sentiment = 'neutral'
        
        return (sentiment, pol)


    def flair(self, text, threshold=0.65):
        '''
        Perform Sentiment Analysis on specified text using Flair model.

        - text: string to analyze

        - threshold [Optional]: threshold used to classify 3 classes. Default: 0.65

        Return a tuple of the form (label, score).
        The label is a string representing the sentiment of the text as either "positive", "negative" or "neutral".
        The score is a number between 0 and 1, the higher the score the higher the sentiment.
        '''

        self.text = text
        self.threshold = threshold

        flair_sentiment = flair.models.TextClassifier.load('en-sentiment')

        try:
            s = flair.data.Sentence(self.text)
            flair_sentiment.predict(s)
        except:
            return ""
        
        # 's' variable contains attributes tag and score.
        # Tag is the sentiment of the text as either "POSITIVE" or "NEGATIVE".
        # Score is a number between 0 and 1, the higher the score the higher the sentiment.

        tag = s.tag.lower()
        score = s.score

        if tag == 'positive' and score > self.threshold:
            sentiment = 'positive'
        elif tag == 'negative' and score > self.threshold:
            sentiment = 'negative'
        else:
            sentiment = 'neutral'

        return (sentiment, score)
