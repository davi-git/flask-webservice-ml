# For Spacy
import spacy

#For NLTK
import nltk

#For Flair
from flair.data import Sentence
from flair.models import SequenceTagger
from segtok.segmenter import split_single


# Named Entity Recognition Class
class NER:
    def __init__(self) -> None:
        self._text = ""
        self._tags = None

    # "text" getter function
    @property
    def text(self) -> str:
        return self._text
    
    # "text" setter function
    @text.setter
    def text(self, t) -> None:
        self._text = t
    
    # "tags" getter function
    @property
    def tags(self):
        return self._tags
    
    # "tags" setter function
    @tags.setter
    def tags(self, x: list) -> None:
        self._tags = x
    
    def spacy(self, text, tags=None) -> dict:
        '''
        Perform Named Entity Recognition on specified text using Spacy model.

        - text: string to analyze

        - tags: [Optional] list of labels the function should return. Default: None (in this case return all the labels generated by NER model)

        Return a dictionary with a list of values for each key.
        
        The keys are the labels generated by NER model (limited to 'tags' parameter if passed) and values are the entities the model found in the text 
        to which it assigned a label.
        '''

        self.text = text
        self.tags = tags

        # NER predictor
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(self.text)

        # An empty dict that will contain labels and entities resulting from the model
        spacy_dict = {}
        # Iterate on entities
        for entity in doc.ents:
            # Label assigned by model
            tag = entity.label_
            # Take label and entity when label is in the list passed as parameter or no list was passed
            if self.tags is None or tag in self.tags:
                # Add entity to the list. If key doesn't exist handle the exception
                try:
                    spacy_dict[tag].append(entity.text)
                #Exception handle: if key doesn't exist create it and save entity in a list
                except:
                    spacy_dict.update({tag: [entity.text]})
        return spacy_dict

    def nltk(self, text, tags=None) -> dict:
        '''
        Perform Named Entity Recognition on specified text using NLTK model.

        - text: string to analyze

        - tags: [Optional] list of labels the function should return. Default: None (return all the labels generated by NER model)

        Return a dictionary with a list of values for each key.
        
        The keys are the labels generated by NER model (limited to 'tags' parameter if passed) and values are the entities the model found in the text 
        to which it assigned a label.
        '''

        self.text = text
        self.tags = tags
        
        # NER predictor: generate tuples (label, entity)
        doc = []
        for sent in nltk.sent_tokenize(self.text):
            for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent))):
                if hasattr(chunk, 'label'):
                    doc.append((chunk.label(), ' '.join(c[0] for c in chunk)))
        
        # An empty dict that will contain labels and entities resulting from the model
        nltk_dict = {}
        # Iterate on entities
        for entity in doc:
            # Label assigned by model
            tag = entity[0]
            # Take label and entity when label is in the list passed as parameter or no list was passed
            if self.tags is None or tag in self.tags:
                # Add entity to the list. If key doesn't exist handle the exception
                try:
                    nltk_dict[tag].append(entity[1])
                #Exception handle: if key doesn't exist create it and save entity in a list
                except:
                    nltk_dict.update({tag: [entity[1]]})
        return nltk_dict

    def flair(self, text, tags=None) -> dict:
        '''
        Perform Named Entity Recognition on specified text using Flair model.

        - text: string to analyze

        - tags: [Optional] list of labels the function should return. Default: None (return all the labels generated by NER model)

        Return a dictionary with a list of values for each key.
        
        The keys are the labels generated by NER model (limited to 'tags' parameter if passed) and values are the entities the model found in the text 
        to which it assigned a label.
        '''

        self.text = text
        self.tags = tags

        # NER predictor
        tagger = SequenceTagger.load('flair/ner-english-ontonotes')
        sentence = [Sentence(sent, use_tokenizer=True) for sent in split_single(self.text)]
        tagger.predict(sentence)

        # An empty dict that will contain labels and entities resulting from the model
        flair_dict = {}
        # Iterate on entities
        for sent in sentence:
            for entity in sent.get_spans('ner'):
                # Label assigned by model
                tag = entity.tag
                # Take label and entity when label is in the list passed as parameter or no list was passed
                if self.tags is None or tag in self.tags:
                    # Add entity to the list. If key doesn't exist handle the exception
                    try:
                        flair_dict[tag].append(entity.text)
                    #Exception handle: if key doesn't exist create it and save entity in a list
                    except:
                        flair_dict.update({tag: [entity.text]})
        return flair_dict
