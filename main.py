import json
import os
import spacy
from string import punctuation
from nltk import ngrams
from gensim.corpora.dictionary import Dictionary

paths=['Cord-19-research-challenge/noncomm_use_subset/noncomm_use_subset/pmc_json','Cord-19-research-challenge/noncomm_use_subset/noncomm_use_subset/pdf_json','Cord-19-research-challenge/custom_license/custom_license/pmc_json','Cord-19-research-challenge/custom_license/custom_license/pdf_json','Cord-19-research-challenge/comm_use_subset/comm_use_subset/pmc_json','Cord-19-research-challenge/comm_use_subset/comm_use_subset/pdf_json','Cord-19-research-challenge/biorxiv_medrxiv/biorxiv_medrxiv/pdf_json']
paths=['Cord-19-research-challenge/biorxiv_medrxiv/biorxiv_medrxiv/pdf_json']

return_path='parsed_documents'

#conda install -c conda-forge spacy-model-en_core_web_sm 
preprocessor = spacy.load("en_core_web_sm")
translator = str.maketrans('','', punctuation)

def prep(text, preprocessor, translator, num_grams=2):
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

allWords=Dictionary()
for path in paths:
    for file in os.listdir(path):
        counter=0
        file_info=dict()
        data = json.load(open(path+'/'+file))
        file_info['paper_id']=data['paper_id']
        file_info['title']=data['metadata']['title']
        paragraphs=data['abstract']+data['body_text']
        for paragraph in paragraphs:
            paragraph_info=file_info
            content=paragraph['text']
            paragraph_info['text']=content
            tokens=prep(content,preprocessor,translator)
            allWords.add_documents(tokens)
            paragraph_info['tokens']=tokens
            json.dump(paragraph_info, open(return_path+'/'+file_info['paper_id']+str(counter).zfill(3)+'.json', 'w'))
            counter+=1
        break #still in training phase
        
#have to add the words of the prior with frequency+=0.
#how much frequency should frequencies of priors add up to? 0.5 of just priors and the rest is the standard 1/num_words?

#https://jacopofarina.eu/posts/gensim-generator-is-not-iterator/
class BoBIterator():
    def __init__(self, generator_function):
        self.generator_function = generator_function
        self.generator = self.generator_function()

    def __iter__(self):
        # reset the generator
        self.generator = self.generator_function()
        return self

    def __next__(self):
        result = next(self.generator)
        if result is None:
            raise StopIteration
        else:
            return result

def BoB_generator():
    for file in os.listdir('parsed_documents'):
        yield(json.load(open('parsed_documents'+'/'+file))['text'])#change to BoW