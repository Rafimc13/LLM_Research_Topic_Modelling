import os

from scipy.sparse import issparse
import numpy as np
from k_means_constrained import KMeansConstrained
from sklearn.metrics import (silhouette_score,
                             normalized_mutual_info_score,
                             adjusted_rand_score,
                             adjusted_mutual_info_score)
from tqdm import tqdm

from utils.plot_clustering import plot_silhouette_values_for_kappas

# Set the number of cores to use
os.environ["LOKY_MAX_CPU_COUNT"] = "4"


def calc_penalty_factor(k, max_clusters):
    """
    Defines a dynamic penalty factor for increasing number of clusters.
    The penalty increases as kappa increases.
    """
    penalty_factor = np.log(1 + k) / max_clusters
    return penalty_factor


def get_number_of_clusters_with_statistic_constrained(
        transformed_data,
        max_clusters,
        true_labels=None,
):
    """
    Calculates a reasonable number of clusters to use
    based on the optimum value of the silhouette score for KMeansConstrained,
    while applying a penalty as kappa increases.

    Args:
        transformed_data (numpy.ndarray or sparse): Transformed data ready for clustering.
        max_clusters (int): The maximum number of clusters.
        true_labels (numpy.ndarray, optional): True labels for the data to calculate NMI, ARI, and AMI scores.
    Returns:
        kappa (int): Optimal number of clusters based on Silhouette score.
        statistic_values (list): Silhouette values of the algorithm for all the kappas.
    """

    min_clusters = 2  # Silhouette score requires at least 2 clusters

    # Check if the data is sparse and convert to dense if necessary
    if issparse(transformed_data):
        transformed_data = transformed_data.toarray()

    # initialize variables
    best_silhouette = -1  # Silhouette score ranges from -1 to 1
    best_kappa = None
    statistic_values = []
    cluster_min_size = 2
    statistic_values_nmi = []
    statistic_values_ari = []
    statistic_values_ami = []

    for kappa in tqdm(range(min_clusters, max_clusters + 1), total=(max_clusters - min_clusters + 1)):
        # initialize the clustering algorithm
        km_cv = KMeansConstrained(
            n_clusters=kappa, size_min=min(cluster_min_size, len(transformed_data))
        )
        # fit the clustering algorithm
        km_cv.fit(transformed_data)

        # Calculate silhouette score
        silhouette_avg = silhouette_score(transformed_data, km_cv.labels_)

        # Apply the penalty as kappa increases
        penalty = calc_penalty_factor(kappa, max_clusters)
        penalized_silhouette = silhouette_avg - penalty
        statistic_values.append(penalized_silhouette)

        # Track the best penalized silhouette score
        if penalized_silhouette > best_silhouette:
            best_silhouette = penalized_silhouette
            best_kappa = kappa

        # Calculate and append NMI, ARI, AMI scores (only if true_labels are provided)
        if true_labels is not None:
            statistic_values_nmi.append(normalized_mutual_info_score(true_labels, km_cv.labels_))
            statistic_values_ari.append(adjusted_rand_score(true_labels, km_cv.labels_))
            statistic_values_ami.append(adjusted_mutual_info_score(true_labels, km_cv.labels_))

    print(f'The optimum kappa based on Penalized Silhouette score is: {best_kappa}')
    plot_silhouette_values_for_kappas(statistic_values)

    # print the scores NMI, AMI, ARI
    if true_labels is not None:
        best_kappa_nmi = statistic_values_nmi[best_kappa - 1]
        best_kappa_ami = statistic_values_ami[best_kappa - 1]
        best_kappa_ari = statistic_values_ari[best_kappa - 1]
        print(
            f'The NMI score is: {best_kappa_nmi} for the best Kappa {best_kappa}')
        print(
            f'The AMI score is: {best_kappa_ami} for the best Kappa {best_kappa}')
        print(
            f'The ARI score is: {best_kappa_ari} for the best Kappa {best_kappa}')

    return best_kappa, statistic_values, statistic_values_nmi, statistic_values_ari, statistic_values_ami
