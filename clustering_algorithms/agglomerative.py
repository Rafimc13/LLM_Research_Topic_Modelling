import os
import numpy as np
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import (silhouette_score,
                             normalized_mutual_info_score,
                             adjusted_rand_score,
                             adjusted_mutual_info_score)
from tqdm import tqdm
from scipy.sparse import issparse

from utils.plot_clustering import plot_silhouette_values_for_agglomerative

# Set the number of cores to use
os.environ["LOKY_MAX_CPU_COUNT"] = "4"


def calc_agglomerative(transformed_data, n_clusters_values, true_labels=None):
    """
    Calculates the number of clusters and the corresponding Silhouette scores
    for different values of the n_clusters parameter using the Agglomerative Clustering algorithm.

    Args:
        transformed_data (numpy.ndarray): Transformed outputs ready for clustering.
        n_clusters_values (list): A list of n_clusters values to evaluate.
        true_labels (numpy.ndarray, optional): True labels for the outputs to calculate NMI, ARI, and AMI scores.

    Returns:
        results (dict): Dictionary containing all the results.
    """

    silhouette_scores = []
    statistic_values_nmi = []
    statistic_values_ari = []
    statistic_values_ami = []

    # Check if the outputs is sparse and convert to dense if necessary
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
            silhouette_scores.append(silhouette_avg)
        else:
            pass

        # Calculate and append NMI, ARI, AMI scores (only if true labels are provided)
        if true_labels is not None:
            statistic_values_nmi.append(normalized_mutual_info_score(true_labels, labels))
            statistic_values_ari.append(adjusted_rand_score(true_labels, labels))
            statistic_values_ami.append(adjusted_mutual_info_score(true_labels, labels))

    # determine the optimal n_clusters value based on the maximum Silhouette score
    optimal_n_clusters_idx = silhouette_scores.index(max(silhouette_scores))
    optimal_n_clusters = n_clusters_values[optimal_n_clusters_idx] + 1

    # print the results
    print(f'The optimal number of clusters based on Silhouette score is: {optimal_n_clusters}')

    # Plot the Silhouette scores for different n_clusters values
    plot_silhouette_values_for_agglomerative(silhouette_scores)

    # print the scores NMI, AMI, ARI
    if true_labels is not None:
        best_nmi = statistic_values_nmi[optimal_n_clusters-1]
        best_ami = statistic_values_ami[optimal_n_clusters-1]
        best_ari = statistic_values_ari[optimal_n_clusters-1]
        print(
            f'The NMI score is: {best_nmi} for the best Kappa {optimal_n_clusters}')
        print(
            f'The AMI score is: {best_ami} for the best Kappa {optimal_n_clusters}')
        print(
            f'The ARI score is: {best_ari} for the best Kappa {optimal_n_clusters}')

    # store the results into a dictionary to return it
    results = {
        'best_kappa': optimal_n_clusters,
        'silhouette_score_values': silhouette_scores,
        'nmi_score_values': statistic_values_nmi,
        'ami_score_values': statistic_values_ami,
        'ari_score_values': statistic_values_ari,
    }
    return results
