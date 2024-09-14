import matplotlib.pyplot as plt
import seaborn as sns


def no_of_words(text):
    """
    Calculate the number of words in a given text.

    Args:
        text (str): The input text to be processed.

    Returns:
        int: The number of words in the given text.
    """
    return len(str(text).split())


def plot_distribution_of_words(df, column_to_plot):
    """
    Plots a histogram showing the distribution of word counts for comments in a given dataframe column.

    Args:
        df (pandas.DataFrame): The dataframe containing the text data.
        column_to_plot (str): The column of interest in the dataframe where the comments are stored.

    Returns:
        None: Displays a plot showing the word count distribution.
    """
    # Create a histogram plot for the word distribution
    fig, ax = plt.subplots(figsize=(12, 6))

    # Apply the function to calculate word counts in the specified column
    df['word_count'] = df[column_to_plot].apply(lambda x: no_of_words(x) if isinstance(x, str) else 0)

    # Plot the histogram for word counts with a Kernel Density Estimate (KDE)
    sns.histplot(
        x='word_count',
        data=df,
        stat='count',
        bins=20,
        kde=True,
        color='blue',
        ax=ax,
    )

    # Set labels and title for the plot
    ax.set_xlabel("Number of Words", fontsize=12)
    ax.set_ylabel('Number of Comments', fontsize=12)
    ax.set_title("Word Count Distribution of Comments", fontsize=12)

    # Adjust the layout and display the plot
    plt.tight_layout()
    plt.show()
