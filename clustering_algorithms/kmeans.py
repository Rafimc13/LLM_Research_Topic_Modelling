import os

from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, normalized_mutual_info_score, adjusted_rand_score, adjusted_mutual_info_score
from tqdm import tqdm

from utils.plot_clustering import plot_silhouette_values_for_kappas

# Set the number of cores to use
os.environ["LOKY_MAX_CPU_COUNT"] = "4"


def calc_kmeans(transformed_data, max_clusters, true_labels=None):
    """
    Calculates a reasonable number of clusters to use
    based on the optimum value of the specified statistic for the original KMeans.

    Args:
        transformed_data (numpy.ndarray): Transformed data ready for clustering.
        max_clusters (int): The maximum number of clusters.
        true_labels (numpy.ndarray, optional): True labels for the data to calculate NMI, ARI, and AMI scores. Defaults to None.

    Returns:
        k_silhouette (int): Optimal number of clusters based on Silhouette score calculation.
        statistic_values_silhouette (list): Silhouette scores for all the k values.
        statistic_values_nmi (list): NMI scores for all the k values.
        statistic_values_ari (list): ARI scores for all the k values.
        statistic_values_ami (list): AMI scores for all the k values.
    """
    min_clusters = 1

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
            continue
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

    return k_silhouette, statistic_values_silhouette, statistic_values_nmi, statistic_values_ari, statistic_values_ami
