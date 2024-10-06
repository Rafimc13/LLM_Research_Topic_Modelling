from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np


def find_optimal_topics_per_comment(text, min_topics=1, max_topics=10, find_optimal=(True, None)):
    """
    Find the optimal number of topics for a single comment by evaluating LDA models.

    Parameters:
    text (str): The comment text.
    min_topics (int): Minimum number of topics to evaluate.
    max_topics (int): Maximum number of topics to evaluate.
    find_optimal (tuple): Tuple value in order to find the optimal number of topics or manually add a value.

    Returns:
    tuple: Optimal number of topics, the LDA model, and the vectorizer.
    """
    # Step 1: Vectorize the single comment
    vectorizer = CountVectorizer(stop_words='english')
    X = vectorizer.fit_transform([text])

    log_likelihoods = []
    models = []
    if find_optimal[0]:
        # Run LDA for different numbers of topics and evaluate
        for num_topics in range(min_topics, max_topics + 1):
            lda = LatentDirichletAllocation(n_components=num_topics, random_state=42)
            lda.fit(X)

            # Calculate log-likelihood for each model
            log_likelihoods.append(lda.score(X))
            models.append(lda)

        # Find the optimal number of topics based on highest log-likelihood
        optimal_num_topics = range(min_topics, max_topics + 1)[np.argmax(log_likelihoods)]
        best_lda_model = models[np.argmax(log_likelihoods)]
    else:
        lda = LatentDirichletAllocation(n_components=find_optimal[1], random_state=42)
        lda.fit(X)
        # define the optimal number of topics manually
        optimal_num_topics = find_optimal[1]
        best_lda_model = lda

    return optimal_num_topics, best_lda_model, vectorizer


def extract_keywords_per_comment(text, min_topics=1, max_topics=10, find_optimal=(True, None)):
    """
    Extract keywords for a single comment by determining the optimal number of topics.

    Parameters:
    text (str): The comment text.
    num_keywords (int): Number of keywords to extract per topic.
    min_topics (int): Minimum number of topics to evaluate.
    max_topics (int): Maximum number of topics to evaluate.
    find_optimal (tuple): Tuple value in order to find the optimal number of topics or manually add a value.

    Returns:
    tuple: Keywords extracted and the optimal number of topics for the comment.
    """
    # Find the optimal number of topics for the comment
    optimal_num_topics, best_lda_model, vectorizer = find_optimal_topics_per_comment(text,
                                                                                     min_topics,
                                                                                     max_topics,
                                                                                     find_optimal)
    # Extract the keywords from the optimal LDA model
    feature_names = vectorizer.get_feature_names_out()
    topic_keywords = []

    for topic in best_lda_model.components_:
        topic_keywords.append(", ".join([feature_names[i] for i in topic.argsort()[-optimal_num_topics:]]))

    return topic_keywords, optimal_num_topics


def extract_keywords_for_all_comments(df, text_column, min_topics=1, max_topics=10, find_optimal=(True, None)):
    """
    Apply the LDA extraction and optimal topic finding for each comment in the DataFrame.

    Parameters:
    df (DataFrame): DataFrame containing the comments.
    text_column (str): Column name containing the comments.
    min_topics (int): Minimum number of topics to evaluate.
    max_topics (int): Maximum number of topics to evaluate.
    find_optimal (tuple): Tuple value in order to find the optimal number of topics or manually add a value.

    Returns:
    DataFrame: Updated DataFrame with columns for extracted keywords and optimal number of topics.
    """
    # Create lists to store the results
    all_keywords = []
    optimal_topics_list = []

    # Loop over each comment and extract keywords
    for index, comment in df[text_column].items():
        keywords, optimal_num_topics = extract_keywords_per_comment(comment, min_topics, max_topics, find_optimal)
        all_keywords.append(keywords)
        optimal_topics_list.append(optimal_num_topics)

    # Add the results to the DataFrame
    df['lda_keywords'] = all_keywords
    df['optimal_num_topics'] = optimal_topics_list

    return df
