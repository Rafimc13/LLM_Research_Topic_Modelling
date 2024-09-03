import os

from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import silhouette_score
from tqdm import tqdm
from scipy.sparse import issparse

from utils.plot_clustering import plot_silhouette_values_for_agglomerative

# Set the number of cores to use
os.environ["LOKY_MAX_CPU_COUNT"] = "4"


def calc_agglomerative(transformed_data, n_clusters_values):
    """
    Calculates the number of clusters and the corresponding Silhouette scores
    for different values of the n_clusters parameter using the AgglomerativeClustering algorithm.

    Args:
        transformed_data (numpy.ndarray): Transformed data ready for clustering.
        n_clusters_values (list): A list of n_clusters values to evaluate.

    Returns:
        optimal_n_clusters (int): The n_clusters value that results in the highest Silhouette score.
        silhouette_scores (list): Silhouette scores for each n_clusters value.
    """

    silhouette_scores = []

    # Check if the data is sparse and convert to dense if necessary
    if issparse(transformed_data):
        transformed_data = transformed_data.toarray()

    for n_clusters in tqdm(n_clusters_values, total=len(n_clusters_values)):
        # initialize the AgglomerativeClustering algorithm
        ac = AgglomerativeClustering(n_clusters=n_clusters)
        # fit the clustering algorithm
        labels = ac.fit_predict(transformed_data)

        # calculate the Silhouette score (only if there are at least 2 clusters)
        if n_clusters > 1:
            silhouette_avg = silhouette_score(transformed_data, labels)
        else:
            silhouette_avg = 0

        silhouette_scores.append(silhouette_avg)

    # determine the optimal n_clusters value based on the maximum Silhouette score
    optimal_n_clusters_idx = silhouette_scores.index(max(silhouette_scores))
    optimal_n_clusters = n_clusters_values[optimal_n_clusters_idx]

    # print the results
    print(f'The optimal number of clusters based on Silhouette score is: {optimal_n_clusters}')

    # Plot the Silhouette scores for different n_clusters values
    plot_silhouette_values_for_agglomerative(silhouette_scores, n_clusters_values)

    return optimal_n_clusters, silhouette_scores
