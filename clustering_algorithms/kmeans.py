import os

from sklearn.cluster import KMeans
from sklearn.metrics import (silhouette_score,
                             normalized_mutual_info_score,
                             adjusted_rand_score,
                             adjusted_mutual_info_score)
from sklearn.preprocessing import normalize
from tqdm import tqdm
import numpy as np

from utils.plot_clustering import plot_silhouette_values_for_kappas

# Set the number of cores to use
os.environ["LOKY_MAX_CPU_COUNT"] = "4"


def calc_kmeans(transformed_data, max_clusters, true_labels=None):
    """
    Calculates a reasonable number of clusters to use
    based on the optimum value of the specified statistic for the original KMeans.

    Args:
        transformed_data (numpy.ndarray): Transformed outputs ready for clustering.
        max_clusters (int): The maximum number of clusters.
        true_labels (numpy.ndarray, optional): True labels for the outputs to calculate NMI, ARI, and AMI scores.

    Returns:
        k_means_results(dict): Dictionary containing all the results.
    """
    min_clusters = 1

    # Normalize the outputs to apply cosine similarity via normalization
    transformed_data = normalize(transformed_data)  # Normalize the outputs to use cosine similarity

    # Initialize lists to hold Silhouette and other scores
    statistic_values_silhouette = []
    statistic_values_nmi = []
    statistic_values_ari = []
    statistic_values_ami = []

    for kappa in tqdm(range(min_clusters, max_clusters + 1), total=(max_clusters - min_clusters + 1)):
        # Initialize the KMeans clustering algorithm
        km = KMeans(n_clusters=kappa, random_state=42, n_init=10)
        # Fit the clustering algorithm
        km.fit(transformed_data)

        # Append Silhouette score values
        if kappa == 1:
            pass
        else:
            statistic_values_silhouette.append(silhouette_score(transformed_data, km.labels_))

        # Calculate and append NMI, ARI, AMI scores (only if true labels are provided)
        if true_labels is not None:
            statistic_values_nmi.append(normalized_mutual_info_score(true_labels, km.labels_))
            statistic_values_ari.append(adjusted_rand_score(true_labels, km.labels_))
            statistic_values_ami.append(adjusted_mutual_info_score(true_labels, km.labels_))

    # Determine the optimal number of clusters
    # For Silhouette, we want the maximum value
    k_silhouette = statistic_values_silhouette.index(max(statistic_values_silhouette)) + min_clusters + 1

    # Print the results
    print(f'The optimum kappa based on Silhouette score is: {k_silhouette}')

    # Plot the Silhouette values
    plot_silhouette_values_for_kappas(statistic_values_silhouette)

    # print the scores NMI, AMI, ARI
    if true_labels is not None:
        best_kappa_nmi = statistic_values_nmi[k_silhouette-1]
        best_kappa_ami = statistic_values_ami[k_silhouette-1]
        best_kappa_ari = statistic_values_ari[k_silhouette-1]
        print(
            f'The NMI score is: {best_kappa_nmi} for the best Kappa {k_silhouette}')
        print(
            f'The AMI score is: {best_kappa_ami} for the best Kappa {k_silhouette}')
        print(
            f'The ARI score is: {best_kappa_ari} for the best Kappa {k_silhouette}')

    # store the results into a dictionary to return it
    k_means_results = {
        'best_kappa': k_silhouette,
        'silhouette_score_values': statistic_values_silhouette,
        'nmi_score_values': statistic_values_nmi,
        'ami_score_values': statistic_values_ami,
        'ari_score_values': statistic_values_ari,
    }
    return k_means_results


def run_best_kmeans(data, best_kappa):
    """
    Run the best performing kmeans clustering based on the calculations of best kappa
    Args:
        data (numpy.ndarray): Transformed outputs ready for clustering.
        best_kappa (int): Best kappa to run the kmeans.

    Returns:
        results(dict): Dictionary containing all the results.
    """
    km = KMeans(n_clusters=best_kappa, random_state=42, n_init=10)
    # Fit the clustering algorithm
    if best_kappa == 1:
        best_kappa = 2

    km.fit(data)
    silhouette_final_score = silhouette_score(data, km.labels_)
    # Print the results
    print(f'Silhouette score for best kappa: { silhouette_final_score:.3f}')

    results = {
        'clusterer': km,
        'labels': km.labels_,
        'centroids': km.cluster_centers_,
    }
    return results
