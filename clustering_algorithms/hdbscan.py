import os

from sklearn.cluster import HDBSCAN
from sklearn.metrics import silhouette_score
from tqdm import tqdm

from utils.plot_clustering import plot_silhouette_values_for_dbscan  # Assuming you have this utility function

# Set the number of cores to use
os.environ["LOKY_MAX_CPU_COUNT"] = "4"


def calc_hdbscan(transformed_data, min_cluster_size_values, min_samples=10):
    """
    Calculates the number of clusters and the corresponding Silhouette scores
    for different values of the min_cluster_size parameter using the HDBSCAN algorithm.

    Args:
        transformed_data (numpy.ndarray): Transformed outputs ready for clustering.
        min_cluster_size_values (list): List of min_cluster_size values to test.
        min_samples (int): The min_samples value for HDBSCAN. Default is 5.

    Returns:
        results(dict): Dictionary containing all the results.
    """

    silhouette_scores = []
    num_clusters_list = []

    for min_cluster_size in tqdm(min_cluster_size_values, total=len(min_cluster_size_values)):
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
    optimal_min_cluster_size = min_cluster_size_values[optimal_min_cluster_size_idx]
    num_clusters = num_clusters_list[optimal_min_cluster_size_idx]

    # print the results
    print(f'The optimal min_cluster_size based on Silhouette score is: {optimal_min_cluster_size}')
    print(f'The number of clusters for optimal min_cluster_size is: {num_clusters}')

    # plot the Silhouette scores for different min_cluster_size values
    plot_silhouette_values_for_dbscan(silhouette_scores, min_cluster_size_values)
    # store the results into a dictionary to return it
    results = {
        'best_min_cluster_size': optimal_min_cluster_size,
        'best_num_clusters': num_clusters,
        'sillhouette_scores': silhouette_scores
    }
    return results
