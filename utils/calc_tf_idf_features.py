from sklearn.feature_extraction.text import TfidfVectorizer

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
