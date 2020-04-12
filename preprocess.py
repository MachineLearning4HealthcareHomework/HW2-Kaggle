import os
import json
import spacy
from string import punctuation
from nltk import ngrams
from gensim.corpora.dictionary import Dictionary


preprocessor = spacy.load("en_core_web_sm")
translator = str.maketrans('','', punctuation)

def text_prep(text, preprocessor, translator, num_grams=2):
    """
    Returns a list of n-grams of a given a piece of text.
    ========
    Input:
        text:string, a piece of text
        preprocessor: spacy nlp preprocessor
        translator: used to remove punctuation
        num_grams:int, n in n-grams
    """
    # remove punctuation
    text = text.translate(translator)
    tokens = preprocessor(text)
    # lemmatization and stopwords, space, number&symbol removal
    tokens = [token.lemma_ for token in tokens \
                            if token.is_stop == False \
                            and token.pos_ != "NUM" \
                            and token.pos_ != "SYM"
                            and token.pos_ != "SPACE"]
    # n-grams
    tokens = ["_".join(t) for t in list(ngrams(tokens, n=num_grams))]
    return tokens

def paper_preprocess(paper):
    """
    Prepare a paper into paragraph-level samples, each sample is a list of n-grams
    """
    paragraphs = paper['text'].split("\n") #split into paragraphs
    paragraphs = [text_prep(p, preprocessor, translator) for p in paragraphs if p] # remove empty strings
    return paragraphs

direc = "./parsed_documents/"
for f in os.listdir(direc):
    paragraphs = []
    ids = []
    if f.endswith(".json"):
        with open(os.path.join(direc, f)) as paper:
            p = json.load(paper)
            paragraphs += paper_preprocess(p)
            ids += [paper['paper_id']]*len(paragraphs)
