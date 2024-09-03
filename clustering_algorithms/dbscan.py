import os
import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.metrics import silhouette_score
from tqdm import tqdm
from sklearn.neighbors import NearestNeighbors

from utils.plot_clustering import plot_silhouette_values_for_dbscan

# Set the number of cores to use
os.environ["LOKY_MAX_CPU_COUNT"] = "4"


def generate_eps_values_via_nearest_neighbors(data, num_values=100):
    """
    Generates a range of `eps` values for DBSCAN clustering by examining the nearest neighbor distances
    within the dataset. The function computes the distance to the nearest neighbor for each data point, and
    then determines the eps values across a range of percentiles of these distances.

    Args:
        data (numpy.ndarray): The dataset for which nearest neighbor distances are calculated. This data should
                              be preprocessed as required for your clustering (e.g., scaled if necessary).
        num_values (int, optional): The number of eps values to generate. These values are spread over
                                    the 10th to 90th percentiles of the nearest neighbor distances. Defaults to 100.

    Returns:
        eps_values (np.array): An array of eps values determined by the specified percentiles of the nearest neighbor
        distances.
                  These values can be used as parameters for the DBSCAN clustering algorithm to explore the
                  best setting.
    """
    nn = NearestNeighbors(n_neighbors=2)
    nn.fit(data)
    distances, _ = nn.kneighbors(data)
    nearest_distances = distances[:, 1]  # distance to the nearest neighbor

    percentiles = np.linspace(10, 90, num_values)  # Generate percentiles between 10th and 90th
    eps_values = np.percentile(nearest_distances, percentiles)  # Find eps values at these percentiles
    print(f'Suggested eps values:{eps_values}')
    return eps_values


def calc_dbscan(transformed_data, eps_values):
    """
    Calculates the number of clusters and the corresponding Silhouette scores
    for different values of the eps parameter using the DBSCAN algorithm.

    Args:
        transformed_data (numpy.ndarray): Transformed data ready for clustering.
        eps_values (list): A list of eps values to evaluate.

    Returns:
        optimal_eps (float): The eps value that results in the highest Silhouette score.
        num_clusters (int): The number of clusters found using the optimal eps value.
        silhouette_scores (list): Silhouette scores for each eps value.
    """

    silhouette_scores = []
    num_clusters_list = []

    for eps in tqdm(eps_values, total=len(eps_values)):
        # initialize the DBSCAN clustering algorithm
        db = DBSCAN(eps=eps, min_samples=20)
        # fit the clustering algorithm
        labels = db.fit_predict(transformed_data)

        # calculate the number of clusters (ignoring noise points)
        num_clusters = len(set(labels)) - (1 if -1 in labels else 0)
        num_clusters_list.append(num_clusters)

        # calculate the Silhouette score (only if there are at least 2 clusters)
        if num_clusters > 1:
            silhouette_avg = silhouette_score(transformed_data, labels)
        else:
            silhouette_avg = 0

        silhouette_scores.append(silhouette_avg)

    # determine the optimal eps value based on the maximum Silhouette score
    optimal_eps_idx = silhouette_scores.index(max(silhouette_scores))
    optimal_eps = eps_values[optimal_eps_idx]
    num_clusters = num_clusters_list[optimal_eps_idx]  + 1

    # print the results
    print(f'The optimal eps based on Silhouette score is: {optimal_eps}')
    print(f'The number of clusters for optimal eps is: {num_clusters}')

    # plot the Silhouette scores for different eps values
    plot_silhouette_values_for_dbscan(silhouette_scores, eps_values)

    return optimal_eps, num_clusters, silhouette_scores
