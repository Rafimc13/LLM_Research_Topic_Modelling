import matplotlib.pyplot as plt
import itertools
from bert_score import score as bertscore
from nltk.translate.bleu_score import sentence_bleu
from nltk.translate.bleu_score import SmoothingFunction
from rouge import Rouge


def calc_and_plot_bleu_scores(summaries_df, text_col, title_col):
    """
    Calculate BLEU scores for unique pairs of summaries and plot the results.

    Args:
        summaries_df (pd.DataFrame): DataFrame containing the summarization techniques to compare.
        text_col (str): The name of the column in the DataFrame that contains the summary texts.
        title_col (str): The name of the column in the DataFrame that contains the titles or technique names.

    Returns:
        dict: A dictionary where keys are the comparison names (e.g., "Technique1_vs_Technique2") and values are the
        BLEU scores for each comparison.
    """
    # define BLEU Score smoothing function
    smooth = SmoothingFunction().method4
    bleu_scores = {}

    # Loop through summaries and compate them with the original
    for idx, summary in enumerate(summaries_df.iterrows()):
        if idx == 0:
            if str(summaries_df.loc[idx, title_col]) == 'original_summary':
                continue
            else:
                raise ValueError(
                    'The position of the original summary is not 0. Rebase the original summary. Terminating...')

        column_name = f"{str(summaries_df.loc[0, title_col])}_vs_\n{str(summaries_df.loc[idx, title_col])}"
        bleu_scores[column_name] = sentence_bleu(
            [summaries_df.loc[0, text_col].split()],
            summaries_df.loc[idx, text_col].split(),
            smoothing_function=smooth
        )

    # names of the comparison summaries
    labels = list(bleu_scores.keys())

    # BLEU scores
    scores = [bleu_scores[key] for key in labels]

    # position of the bars on the x-axis
    positions = range(len(labels))

    # Creating the bar plot
    fig, ax = plt.subplots(figsize=(8, 6))
    bars = ax.bar(positions, scores, color='skyblue')

    # Adding labels and title
    ax.set_xlabel('Comparison of Techniques')
    ax.set_ylabel('BLEU Score')
    ax.set_title('BLEU Scores Comparing Summarization Techniques')
    ax.set_xticks(positions)
    ax.set_xticklabels(labels, rotation=45, fontsize=8, ha='right')
    ax.set_ylim(0, 1)

    # Adding the actual value on top of each bar
    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2.0, yval, f"{yval:.3f}", va='bottom', ha='center')

    # Show the plot
    plt.tight_layout()
    plt.show()

    return bleu_scores


def calc_and_plot_rouge_scores(summaries_df, text_col, title_col):
    """
    Calculate ROUGE scores for unique pairs of summaries and plot the results.

    Args:
        summaries_df (pd.DataFrame): DataFrame containing the summarization techniques to compare.
        text_col (str): The name of the column in the DataFrame that contains the summary texts.
        title_col (str): The name of the column in the DataFrame that contains the titles or technique names.

    Returns:
        dict: A dictionary where keys are the comparison names (e.g., "Technique1_vs_Technique2") and values are the
        ROUGE scores for each comparison.
    """
    # ROUGE Score
    rouge = Rouge()
    # define the dict of Rouge scores
    rouge_scores = {}

    # Loop through summaries and compate them with the original
    for idx, summary in enumerate(summaries_df[text_col]):
        if idx == 0:
            if str(summaries_df.loc[idx, title_col]) == 'original_summary':
                continue
            else:
                raise ValueError(
                    'The position of the original summary is not 0. Rebase the original summary. Terminating...')

        column_name = f"{str(summaries_df.loc[0, title_col])}_vs_\n{str(summaries_df.loc[idx, title_col])}"
        rouge_scores[column_name] = rouge.get_scores(summaries_df.loc[0, text_col],
                                                     summaries_df.loc[idx, text_col])
    # Extracting ROUGE-1 and ROUGE-2 scores
    metrics = ['f', 'p', 'r']  # f-measure, precision, recall
    labels = list(rouge_scores.keys())
    rouge_1_data = {metric: [] for metric in metrics}
    rouge_2_data = {metric: [] for metric in metrics}

    for comparison in labels:
        for metric in metrics:
            rouge_1_data[metric].append(rouge_scores[comparison][0]['rouge-1'][metric])
            rouge_2_data[metric].append(rouge_scores[comparison][0]['rouge-2'][metric])

    # Position of the bars on the x-axis
    positions = range(len(labels))

    # Plotting the outputs
    fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(17, 10))  # Two rows (ROUGE-1, ROUGE-2), three columns (f, p, r)
    fig.suptitle('ROUGE Scores Comparing Summarization Techniques')

    for i, metric in enumerate(metrics):
        ax = axes[0, i]
        bars = ax.bar(positions, rouge_1_data[metric], color='skyblue')
        for bar in bars:
            yval = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2.0, yval, f"{yval:.3f}", va='bottom', ha='center')
        ax.set_title(f'ROUGE-1 {metric}')
        ax.set_xticks(positions)
        ax.set_xticklabels(labels, rotation=60, fontsize=8.5, ha='right')
        ax.set_ylabel(metric)
        ax.set_ylim(0, 1)

        ax = axes[1, i]
        bars = ax.bar(positions, rouge_2_data[metric], color='lightgreen')
        for bar in bars:
            yval = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2.0, yval, f"{yval:.3f}", va='bottom', ha='center')
        ax.set_title(f'ROUGE-2 {metric}')
        ax.set_xticks(positions)
        ax.set_xticklabels(labels, rotation=60, fontsize=8.5, ha='right')
        ax.set_ylabel(metric)
        ax.set_ylim(0, 1)

    # Adjust layout to make room for the title
    plt.tight_layout(rect=(0, 0.03, 1, 0.95))
    plt.show()

    return rouge_scores


def calc_and_plot_bert_scores(summaries_df, text_col, title_col, model_to_use='roberta-large', text_lang='en'):
    """
    Calculate BERT scores for unique pairs of summaries and plot the results.

    Args:
        summaries_df (pd.DataFrame): DataFrame containing the summarization techniques to compare.
        text_col (str): The name of the column in the DataFrame that contains the summary texts.
        title_col (str): The name of the column in the DataFrame that contains the titles or technique names.
        model_to_use (str): transformer model to use for the BERT score results.
        text_lang (str): the language of the final summaries.

    Returns:
        dict: A dictionary where keys are the comparison names (e.g., "Technique1_vs_Technique2") and values are the
        BERT scores for each comparison.
    """
    # define the dict with the results
    bert_scores = {}

    # Loop through summaries and compate them with the original
    for idx, summary in enumerate(summaries_df[text_col]):
        if idx == 0:
            if str(summaries_df.loc[idx, title_col]) == 'original_summary':
                continue
            else:
                raise ValueError(
                    'The position of the original summary is not 0. Rebase the original summary. Terminating...')

        column_name = f"{str(summaries_df.loc[0, title_col])}_vs_\n{str(summaries_df.loc[idx, title_col])}"
        # Compute precision, recall, and F1 for each summary comparison
        P, R, F1 = bertscore([summaries_df.loc[idx, text_col]],
                             [summaries_df.loc[0, text_col]],
                             model_type=model_to_use, lang=text_lang)

        bert_scores[column_name] = {'precision': P.mean().item(), 'recall': R.mean().item(), 'f1': F1.mean().item()}

    # Extracting BERT precision, recall, and F1 scores
    metrics = ['precision', 'recall', 'f1']
    labels = list(bert_scores.keys())
    precision_data = []
    recall_data = []
    f1_data = []

    for comparison in labels:
        precision_data.append(bert_scores[comparison]['precision'])
        recall_data.append(bert_scores[comparison]['recall'])
        f1_data.append(bert_scores[comparison]['f1'])

    # Position of the bars on the x-axis
    positions = range(len(labels))

    # Plotting the outputs
    fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(18, 6))
    fig.suptitle('BERT Scores Comparing Summarization Techniques')

    # Precision plot
    ax = axes[0]
    bars = ax.bar(positions, precision_data, color='lightblue')
    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2.0, yval, f"{yval:.3f}", va='bottom', ha='center')
    ax.set_title('BERT Precision')
    ax.set_xticks(positions)
    ax.set_xticklabels(labels, rotation=45, fontsize=9, ha='right')
    ax.set_ylim(0, 1)

    # Recall plot
    ax = axes[1]
    bars = ax.bar(positions, recall_data, color='lightgreen')
    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2.0, yval, f"{yval:.3f}", va='bottom', ha='center')
    ax.set_title('BERT Recall')
    ax.set_xticks(positions)
    ax.set_xticklabels(labels, rotation=45, fontsize=9, ha='right')
    ax.set_ylim(0, 1)

    # F1 plot
    ax = axes[2]
    bars = ax.bar(positions, f1_data, color='salmon')
    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2.0, yval, f"{yval:.3f}", va='bottom', ha='center')
    ax.set_title('BERT F1')
    ax.set_xticks(positions)
    ax.set_xticklabels(labels, rotation=45, fontsize=9, ha='right')
    ax.set_ylim(0, 1)

    # Adjust layout to make room for the title
    plt.tight_layout(rect=(0, 0.03, 1, 0.95))
    plt.show()

    return bert_scores
