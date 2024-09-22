#  Exploratory Research 


## Description

The project has built for an Exploratory Data Analysis (EDA)
on data of OpenGOV. More specifically we are going to make EDA for data of Ministry of Defence.
Main scope of this EDA is to see how a discussion of large organizations such as Ministries is making, and how can be improved via an LLM.  

 


### Techniques that implemented

* Average and max word count of four (4) term_id's (including stopwords)
* Average and max word count of all stopwords in comments
* Check if emojis or special tokens exist in the comments
* Average and max word count of four (4) term_id's (after preprocess - without stopwords and punct.)
* Most frequent words, and stopwords for each term_id
* Lemmatization technique in order to find similarities between the selected term_id's
* NER technique in all the comments
* POS TAGGING technique via pretrained transformer model for all the comments
* Bi-Gram and Tri-Gram counter techniques
* WordCloud for presentation of most common bigram and trigram counters
* GPT-3.5 API for the classification of comments per stance (for/against/generally agree but have some proposals for amendments/generally disagree with the whole philosophy of the intervention)
* Summarization of comments for a specific article, by using GPT-4 


### Installing - Importing

* Please import the .csv "exportministryofdefencetocsv" in the beginning in order to be able to run the rest code.
* Enter to the Jupyter Notebook to check code, descriptions & plots.
* For a quick view open Explanation_Research.pdf to check the plots.

### Executing program

* Each cell of the notebook is executable except for cell [25], [27], [27] and from cell [221] and down which require Nvidia GPU for implementing a transformer model and also OPENAI API key.


## Help

If a problem occurs with the code please check that the files are correctly imported.

## Authors

Research Assistant: Rafail Mpalis