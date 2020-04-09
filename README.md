# Kaggle Competition
For the task I want to achieve I choose the [ethical sub-question](https://www.kaggle.com/allen-institute-for-ai/CORD-19-research-challenge/tasks?taskId=563).

There are different questions:
   1. Efforts to articulate and translate existing ethical principles and standards to salient issues in COVID-2019
   2. Efforts to embed ethics across all thematic areas, engage with novel ethical issues that arise and coordinate to minimize duplication of oversight
    3. Efforts to support sustained education, access, and capacity building in the area of ethics
    4. Efforts to establish a team at WHO that will be integrated within multidisciplinary research and operational platforms and that will connect with existing and expanded global networks of social sciences.
    5. Efforts to develop qualitative assessment frameworks to systematically collect information related to local barriers and enablers for the uptake and adherence to public health measures for prevention and control. This includes the rapid identification of the secondary impacts of these measures. (e.g. use of surgical masks, modification of health seeking behaviors for SRH, school closures)
    6. Efforts to identify how the burden of responding to the outbreak and implementing public health measures affects the physical and psychological health of those providing care for Covid-19 patients and identify the immediate needs that must be addressed.
    7. Efforts to identify the underlying drivers of fear, anxiety and stigma that fuel misinformation and rumor, particularly through social media.


## Model Idea
As a primary workhorse I will rely on a latent variable model with different priors/queries, which are specific to each question, so there are at least 7 different topics.
I try to find documents which match the priors as good as possible and the process can be expanded to any document and take that mix of topics as the search parameter. In theory the document could be a single word or if it is a longer text, it would be even better. 

I choose this method, because I think the unsupervised nature of it is needed to correctly explore such a task and it does not need as complex and resource hungry algorithms as transformers for a homework that probably fails. Yet, I can still try something new and use some NLP practices.

## Preprocessing
First, I want to use part of speech to get better tokens with less ambiguity, then I will lemmatize, since for this task, I see no benefit in discriminating between the same word group. Afterwards, I will remove stopwords, before making bigrams and then give them over as tokens to the model.

## The different priors
1. Find ethical principles in other literature
2. Same embedding as old problems, but how to differ?
3. SexEd in Africa?
4. NER (AllenNLP-thing) with entitites that are in the same context as WHO and have WHO in their context. 
5. Find other frameworks?
6. Is there also research done in this area? Otherwise use the semantic parsing, where a patient is the patient/object of an actor.
7. There is enough psychological research done in that field that could be used as a prior 
