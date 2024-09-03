import os

from scipy.sparse import issparse
import numpy as np
from k_means_constrained import KMeansConstrained
from sklearn.metrics import silhouette_score
from tqdm import tqdm

from utils.plot_clustering import plot_silhouette_values_for_kappas, plot_sse_values_for_kappas

# Set the number of cores to use
os.environ["LOKY_MAX_CPU_COUNT"] = "4"


def get_number_of_clusters_with_statistic_constrained(
        transformed_data,
        max_clusters,
        statistic_metric='SSE',
):
    """
    Calculates a reasonable number of clusters to use
    based on the optimum value of the specified statistic for KMeansConstrained

    Args:
        transformed_data (numpy.ndarray or sparse): Transformed data ready for clustering.
        max_clusters (int): The maximum number of clusters.
        statistic_metric (str): Statistic to be optimized. Options: SSE (minimized), Silhouette (maximized).
    Returns:
        kappa (int): Optimal number of clusters with SSE or Silhouette calculation.
        statistic_values (list): SSE or Silhouette values of the algorithm for all the kappas.
    """

    min_clusters = 1

    # Check if the data is sparse and convert to dense if necessary
    if issparse(transformed_data):
        transformed_data = transformed_data.toarray()

    # initialize variables
    best_statistic = None
    starting_inertia = None
    statistic_values = []
    cluster_min_size = 10

    def calc_penalty_factor(k):
        # Define the dynamic penalty factor
        cluster_number_penalty_factor = np.log(1 + k) / max_clusters
        return cluster_number_penalty_factor

    for kappa in tqdm(range(min_clusters, max_clusters + 1), total=(max_clusters - min_clusters + 1)):
        # initialize the clustering algorithm
        km_cv = KMeansConstrained(
            n_clusters=kappa, size_min=min(cluster_min_size, len(transformed_data))
        )
        # fit the clustering algorithm
        km_cv.fit(transformed_data)
        if statistic_metric == 'SSE':
            if kappa == min_clusters:
                starting_inertia = km_cv.inertia_
            else:
                current_statistic = (
                        km_cv.inertia_ / starting_inertia + calc_penalty_factor(kappa) * kappa
                )
                if current_statistic > best_statistic:
                    break
            # update best_statistic
            best_statistic = (
                    km_cv.inertia_ / starting_inertia + calc_penalty_factor(kappa) * kappa
            )
            # append best_statistic values
            statistic_values.append(best_statistic)
        else:
            if kappa == 1:
                continue
            # append silhouette_score values
            statistic_values.append(silhouette_score(transformed_data, km_cv.labels_))

    # select best-kappa (n_clusters) value based on the optimum obtained value
    if statistic_metric == 'SSE':
        # we care about the index of the minimum value for SSE
        kappa = statistic_values.index(min(statistic_values)) + min_clusters

        print(f'The optimum kappa based on SSE is: {kappa}')
        plot_sse_values_for_kappas(statistic_values)
    else:
        # we care about the index of the maximum value for Silhouette score
        kappa = statistic_values.index(max(statistic_values)) + min_clusters + 1
        print(f'The optimum kappa based on Silhouette score is: {kappa}')
        plot_silhouette_values_for_kappas(statistic_values)
    return kappa, statistic_values
