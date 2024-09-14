import os

from sklearn.cluster import HDBSCAN
from sklearn.metrics import silhouette_score
from tqdm import tqdm

from utils.plot_clustering import plot_silhouette_values_for_dbscan  # Assuming you have this utility function

# Set the number of cores to use
os.environ["LOKY_MAX_CPU_COUNT"] = "4"


def calc_hdbscan(transformed_data):
    """
    Calculates the number of clusters and the corresponding Silhouette scores
    for different values of the min_cluster_size parameter using the HDBSCAN algorithm.

    Args:
        transformed_data (numpy.ndarray): Transformed data ready for clustering.

    Returns:
        optimal_min_cluster_size (int): The min_cluster_size value that results in the highest Silhouette score.
        num_clusters (int): The number of clusters found using the optimal min_cluster_size value.
        silhouette_scores (list): Silhouette scores for each min_cluster_size value.
    """

    silhouette_scores = []
    num_clusters_list = []

    for max_cluster_size in tqdm(max_cluster_size_values, total=len(max_cluster_size_values)):
        # initialize the HDBSCAN clustering algorithm
        clusterer = HDBSCAN(min_cluster_size=min_cluster_size, min_samples=min_samples, metric='euclidean')
        # fit the clustering algorithm
        labels = clusterer.fit_predict(transformed_data)

        # calculate the number of clusters (ignoring noise points)
        num_clusters = len(set(labels)) - (1 if -1 in labels else 0)
        num_clusters_list.append(num_clusters)

        # calculate the Silhouette score (only if there are at least 2 clusters)
        if num_clusters > 1:
            silhouette_avg = silhouette_score(transformed_data, labels)
        else:
            silhouette_avg = 0

        silhouette_scores.append(silhouette_avg)

    # determine the optimal min_cluster_size based on the maximum Silhouette score
    optimal_min_cluster_size_idx = silhouette_scores.index(max(silhouette_scores))
    optimal_min_cluster_size = max_cluster_size_values[optimal_min_cluster_size_idx]
    num_clusters = num_clusters_list[optimal_min_cluster_size_idx] + 1

    # print the results
    print(f'The optimal min_cluster_size based on Silhouette score is: {optimal_min_cluster_size}')
    print(f'The number of clusters for optimal min_cluster_size is: {num_clusters}')

    # plot the Silhouette scores for different min_cluster_size values
    plot_silhouette_values_for_dbscan(silhouette_scores, max_cluster_size_values)

    return optimal_min_cluster_size, num_clusters, silhouette_scores
