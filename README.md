# Kaggle Competition
For the task I want to achieve I choose the [ethical sub-question](https://www.kaggle.com/allen-institute-for-ai/CORD-19-research-challenge/tasks?taskId=563).

There are different questions:
   1. Efforts to articulate and translate existing ethical principles and standards to salient issues in COVID-2019
   2. Efforts to embed ethics across all thematic areas, engage with novel ethical issues that arise and coordinate to minimize duplication of oversight.
   3. Efforts to support sustained education, access, and capacity building in the area of ethics
   4. Efforts to establish a team at WHO that will be integrated within multidisciplinary research and operational platforms and that will connect with existing and expanded global networks of social sciences.
   5. Efforts to develop qualitative assessment frameworks to systematically collect information related to local barriers and enablers for the uptake and adherence to public health measures for prevention and control. This includes the rapid identification of the secondary impacts of these measures. (e.g. use of surgical masks, modification of health seeking behaviors for SRH, school closures)
   6. Efforts to identify how the burden of responding to the outbreak and implementing public health measures affects the physical and psychological health of those providing care for Covid-19 patients and identify the immediate needs that must be addressed.
   7. Efforts to identify the underlying drivers of fear, anxiety and stigma that fuel misinformation and rumor, particularly through social media.

## Model Idea
As a primary workhorse we will rely on a latent variable model with different priors/queries, which are specific to each question.
With LDA, one can find similar documents, which have a similar topic distribution as the search queries.

The problem with this approach is to *get fitting topics* and also expressing a *good search query*.
A way to get specific topics is by initializing them with good priors. E.g. if we want a sports topic, we can use some sports articles as priors and train our model with those priors.

We see that some sub-questions can be rather easily expressed with possible search results. E.g. for the 7th sub-question there has been done a lot of research concerning fear, anxiety and stigma by psychologists and intersected with the COVID-19 topic, that we supply with our data, we get the answers to this sub-question.

If we would use those texts directly as our query, we probably get bad results, since our topics are most likely rather biological/academical and there is none which is specialised in psychology. But we can enforce a psychology topic using the psychology texts as prior.
Also in this easy case, we have a simple distribution of hits, those with the maximal probability of that psychology-topic.

Unfortunately, not every of those cases is as easy, we can not easily think of well fitting texts that match the problem and could be used as a prior. We have to resort to using the listed question text as query. If we were to just utilize the prior-induced topics, we might get bad results for those rather general queries, since those topics should only consist of their niche and nothing generally useful; it is pretty hard to explain chocolate only using words describing eggs and bunnies.

This is why we need some vanilla/general LDA-topics, without priors. As a good side-effect these general topics will soak up the general words, which should not get in in the specialized topics.

## Model example
As an example we might have the following topics:
   1. specialized for sub-question 1
   2. specialized for sub-question 3
   3. specialized for sub-question 5
   4. specialized for sub-question 7
   5. general/vanilla topic without prior
   6. general/vanilla topic without prior
   7. general/vanilla topic without prior
   8. general/vanilla topic without prior
   9. general/vanilla topic without prior
   10. general/vanilla topic without prior

For the sub-questions with a specialized topic, our best solution would be the documents with the highest score in "their" topic, e.g. sub-question 3 gives the query [0,1,0,0,0,0,0,0,0,0].

For the other sub-questions we have to get the topic distribution of their query text, e.g. the query text for subquestion 4 is "education", this would give the distribution [0,0,0.1,0.2,0.2,0.1,0,0.3,0.1,0]. We now search the documents which best match that distribution.

## Motivation
I choose this method, because I think the unsupervised nature of it is needed to correctly explore such a task and it does not need as complex and resource hungry algorithms as transformers for an attempt that probably fails. Yet, I can still try something new and use some NLP practices.

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
