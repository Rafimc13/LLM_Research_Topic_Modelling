import matplotlib.pyplot as plt
import seaborn as sns


def plot_silhouette_values_for_kappas(silhouette_scores):
    """
    Plots the Silhouette Scores for different numbers of clusters (k values).

    Args:
        silhouette_scores (list): A list of Silhouette scores corresponding to different numbers of clusters.

    Returns:
        None: The function displays a plot of Silhouette scores against the number of clusters.
    """
    # adjusted to match k-values with silhouette scores
    k_values = range(1, len(silhouette_scores) + 1)

    # plotting the Silhouette Score
    sns.set(style="whitegrid")
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(k_values, silhouette_scores, marker='o', color='blue', label='Silhouette Score')
    ax.set_xlabel('Number of Clusters (k)')
    ax.set_ylabel('Silhouette Score')
    ax.set_title('Silhouette Scores by Number of Clusters')
    ax.legend()
    plt.show()
    plt.close(fig)


def plot_sse_values_for_kappas(sse_scores):
    """
    Plots the SSE Scores for different numbers of clusters (k values).

    Args:
        sse_scores (list): A list of SSE scores corresponding to different numbers of clusters.

    Returns:
        None: The function displays a plot of SSE scores against the number of clusters.
    """
    # adjusted to match k-values with SSE scores
    k_values = range(1, len(sse_scores) + 1)

    # plotting the SSE Score
    sns.set(style="whitegrid")
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(k_values, sse_scores, marker='o', color='orange', label='SSE Score')
    ax.set_xlabel('Number of Clusters (k)')
    ax.set_ylabel('SSE Score')
    ax.set_title('SSE Scores by Number of Clusters')
    ax.legend()
    plt.show()
    plt.close(fig)


def plot_silhouette_values_for_dbscan(silhouette_scores, min_cluster_size):
    """
    Plots the Silhouette Scores for different eps values for DBSCAN algorithm.

    Args:
        silhouette_scores (list): A list of Silhouette scores corresponding to different eps values.
        min_cluster_size (list): A list of size values of clusters that were evaluated.

    Returns:
        None: The function displays a plot of Silhouette scores against the eps values.
    """
    sns.set(style="whitegrid")
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(min_cluster_size, silhouette_scores, marker='o', color='blue', label='Silhouette Score')
    ax.set_xlabel('eps Value')
    ax.set_ylabel('Silhouette Score')
    ax.set_title('Silhouette Scores by eps Value for DBSCAN algorithm')
    ax.legend()
    plt.show()
    plt.close(fig)


def plot_silhouette_values_for_agglomerative(silhouette_scores):
    """
    Plots the Silhouette Scores for different n_clusters values for Agglomerative algorithm.

    Args:
        silhouette_scores (list): A list of Silhouette scores corresponding to different n_clusters values.

    Returns:
        None: The function displays a plot of Silhouette scores against the n_clusters values.
    """
    # adjusted to match k-values with silhouette scores
    n_clusters_values = range(1, len(silhouette_scores) + 1)
    sns.set(style="whitegrid")
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(n_clusters_values, silhouette_scores, marker='o', color='blue', label='Silhouette Score')
    ax.set_xlabel('Number of Clusters')
    ax.set_ylabel('Silhouette Score')
    ax.set_title('Silhouette Scores by Number of Clusters for Agglomerative algorithm')
    ax.legend()
    plt.show()
    plt.close(fig)
