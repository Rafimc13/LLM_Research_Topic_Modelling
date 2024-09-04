from gensim.models import FastText
import numpy as np


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
