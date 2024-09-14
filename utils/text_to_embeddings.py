from sklearn.feature_extraction.text import TfidfVectorizer
from transformers import AutoTokenizer, AutoModel
import torch
import torch.nn.functional as F
from gensim.models import FastText
import numpy as np


def tokenizer(document, nlp):
    """
    Tokenizer that removes punctuation and spaces using the spaCy model.
    :param document: string which is a text
    :param nlp: spaCy language model to process the document
    :return: tokenized text
    """
    return [token.text for token in nlp(document) if not token.is_space]


def calc_tf_idf_vectors(corpus, sentences, nlp):
    """
    Calculates TF-IDF vectors for the input sentences using a custom tokenizer.

    Args:
        corpus (np.array): The corpus of text documents to fit the TF-IDF vectorizer.
        sentences (np.array): Sentences to be transformed using the fitted vectorizer.
        nlp (spacy.lang.*): SpaCy language model for tokenization.

    Returns:
        transformed_data_tfidf: The TF-IDF vectorized form of the input sentences.
    """

    # Define the tokenizer function that will use the passed nlp model
    def custom_tokenizer(doc):
        return tokenizer(doc, nlp)

    # Initialize TfidfVectorizer with the custom tokenizer
    vectorizer_news = TfidfVectorizer(
        tokenizer=custom_tokenizer,  # Custom tokenizer using the provided nlp model
        max_df=0.9,
        min_df=5,
        max_features=20000,
        stop_words='english'
    )

    # Fit the vectorizer on the entire corpus
    vectorizer_news.fit(corpus)

    # Now transform only the sample (sentences) using the fitted vectorizer
    transformed_data_tfidf = vectorizer_news.transform(sentences)

    print('Sentences transformed successfully via TF-IDF vectorizer')
    return transformed_data_tfidf


def mean_pooling(model_output, attention_mask):
    """
    Mean Pooling - Take attention mask into account for correct averaging
    """
    token_embeddings = model_output[0]
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)


def calc_embeddings(sentences):
    """
    Calculates embeddings with a transformer model

    Args:
        sentences (np.array): Sentences to be transformed as embeddings.

    Returns:
        embeddings (np.array): calculated embeddings.
    """

    # Load model from HuggingFace Hub
    # tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')
    # model = AutoModel.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')
    tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/paraphrase-mpnet-base-v2')
    model = AutoModel.from_pretrained('sentence-transformers/paraphrase-mpnet-base-v2')

    # Set up the correct device for the transformer
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f"Available device for the model is: '{device}'")
    model.to(device)
    # Tokenize sentences
    encoded_input = tokenizer(sentences, padding=True, truncation=True, return_tensors='pt')
    encoded_input.to(device)
    # Compute token embeddings
    with torch.no_grad():
        model_output = model(**encoded_input)

    # Perform pooling
    transform_data_embeddings = mean_pooling(model_output, encoded_input['attention_mask'])

    # Normalize embeddings
    transform_data_embeddings = F.normalize(transform_data_embeddings, p=2, dim=1)

    transform_data_embeddings = transform_data_embeddings.cpu().detach().numpy().tolist()
    print('Calculation of embeddings completed succesfully')
    return transform_data_embeddings


def train_fasttext_and_transform(corpus, sentences, text_col, vector_size=256, window=10):
    """
    Trains a FastText model on the provided corpus and transforms the sentences into embeddings.

    Args:
        corpus (pandas.DataFrame): DataFrame containing the text data for training the FastText model.
        sentences (pandas.Series): Series containing the sentences to be transformed.
        text_col (str): The name of the column in the corpus containing the text.
        vector_size (int): Dimensionality of the FastText vectors.
        window (int): Maximum distance between the current and predicted word within a sentence.

    Returns:
        transformed_data_fasttext (np.array): Array of sentence embeddings.
    """
    # Prepare the data by tokenizing sentences (split by whitespace for simplicity)
    tokenized_corpus = [comment.split() for comment in corpus]

    # Train the FastText model
    model = FastText(sentences=tokenized_corpus,
                     vector_size=vector_size,
                     window=window,
                     min_count=1,
                     workers=4)

    def get_mean_vector(sentence, ft_model):
        """
        Function to get the average vector for each comment
        (ignoring words not in the model's vocabulary)

        """
        words = sentence.split()  # Tokenize the sentence
        word_vectors = [ft_model.wv[word] for word in words if word in model.wv]
        if word_vectors:
            return np.mean(word_vectors, axis=0)
        else:
            return np.zeros(vector_size)

    # Transform the input sentences
    transformed_data_fasttext = np.array([get_mean_vector(comment, model) for comment in sentences])

    print('Sentences transformed successfully via pretrained FastText language model')
    return transformed_data_fasttext