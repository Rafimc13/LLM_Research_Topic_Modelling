from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


def compare_keyword_embeddings(df, original_column, column_for_comparison, final_column_suffix):
    """
    Compare the embeddings of the LDA keywords with the original keywords using cosine similarity.

    Parameters:
    df (DataFrame): Input dataframe containing the extracted and original keyword embeddings.
    lda_column (str): Column name containing LDA extracted keyword embeddings.
    original_column (str): Column name containing the original keyword embeddings.

    Returns:
    DataFrame: Updated DataFrame with cosine similarity scores.
    """
    final_df = df.copy()

    # Calculate cosine similarity between original and LDA embeddings
    cosine_similarities = []
    for i in range(len(df)):
        # Extract the embeddings for both original and LDA keywords
        original_embedding = df[original_column].iloc[i].reshape(1, -1)
        embedding = df[column_for_comparison].iloc[i].reshape(1, -1)

        # Compute cosine similarity between the two embeddings
        similarity = cosine_similarity(original_embedding, embedding)[0][0]
        cosine_similarities.append(similarity)

    # Add cosine similarity scores to the DataFrame
    column_name = 'cosine_similarity_' + final_column_suffix
    final_df[column_name] = cosine_similarities

    return final_df, column_name


