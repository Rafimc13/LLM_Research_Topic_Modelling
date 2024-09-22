import ast

import pandas as pd
from tqdm import tqdm
from sklearn.decomposition import PCA

from clustering_algorithms.kmeans_constrained import get_number_of_clusters_with_statistic_constrained, run_best_kmeans
from utils.GPT_Prompting import PromptingGPT
from utils.load_prompts import load_chosen_prompt, get_final_prompt


def topic_extraction(df, text_col, prompt_template, gpt_model, **kwargs):
    """
     Perform classification of comments using GPT models.

     Parameters:
     - comments: list of str
     List containing comments to classify.
     - name_of_prompt: str
     name of the preferred prompt
     - GPT model: str
     GPT model used for Classification

     Returns:
     - labels_final: list of int
     List of integer labels corresponding to the classification results.
     """
    flattened_topics = []
    for idx, comment in enumerate(tqdm(df[text_col].to_list(), total=len(df))):
        try:
            gpt_prompts = PromptingGPT()  # Create a new instance of GPT model in each iteration
            # define the final prompt based on the prompt template
            kwargs['comment'] = comment
            kwargs['topics'] = flattened_topics[-30:]
            final_prompt = get_final_prompt(prompt_template, **kwargs)
            response = gpt_prompts.make_prompts(final_prompt, gpt_model=gpt_model).strip()

            _, topics = response.split(":", 1)
            topics = ast.literal_eval(topics.strip())
            df.loc[idx, 'topics'] = topics
            for topic in topics:
                flattened_topics.append((idx, topic))

        except Exception as e:
            print(f"Error processing topics of '{comment}'")
        topics_dict = {
            'idx': [item[0] for item in flattened_topics],
            'topic': [item[1] for item in flattened_topics]
        }
        df_topics = pd.DataFrame(topics_dict)

    return df, df_topics


def calc_clusters_with_kmeans(df, text_col, max_token_length=8000, is_pca=(True, 16)):

    # Create a new instance of GPT model
    gpt_embeddings = PromptingGPT()
    # transform sentences in  openai embeddings
    transformed_data = gpt_embeddings.get_embeddings(texts=df[text_col], max_token_length=max_token_length)
    # define maximum number of clusters to be calculated and compared
    max_num_of_clusters = 50

    if is_pca[0]:
        print('Using PCA to transformed embeddings')
        # Reduce the dimensionality of embeddings
        pca = PCA(n_components=is_pca[1])
        final_data = pca.fit_transform(transformed_data)
    else:
        final_data = transformed_data

    # calculate the optimum kappa with KMeans via Silhouette score and using OPENAI embeddings ADA-002
    kmeans_results = get_number_of_clusters_with_statistic_constrained(transformed_data=final_data,
                                                                       max_clusters=max_num_of_clusters,
                                                                       cluster_min_size=5,
                                                                       true_labels=None)

    best_kmeans_results = run_best_kmeans(final_data, best_kappa=kmeans_results['best_kappa'])
    df['labels'] = best_kmeans_results['labels']
    return df, best_kmeans_results


def summarize_comments_by_cluster(df, text_col, prompt_name, gpt_model, **kwargs):
    unique_labels = df.labels.unique()
    summaries = []
    for label in unique_labels:
        df_labeled = df[df['labels'] == label]
        comments = df_labeled[text_col]
        try:
            gpt_prompts = PromptingGPT()  # Create a new instance of GPT model in each iteration
            # Update kwarg of comments with the chosen comments
            kwargs['previous_summaries'] = summaries[-5:]
            kwargs['comments'] = comments
            final_prompt = get_final_prompt(prompt=prompt_name, **kwargs)
            summary = gpt_prompts.make_prompts(final_prompt, gpt_model=gpt_model).strip()
            summaries.append(summary)
        except Exception as e:
            print(f"Error processing summary for label: {label}")
            summaries.append(None)

    return summaries


def final_summary_of_clustered_comments(prompt, gpt_model, **kwargs):
    """
    Generate final summary based on summaries of comments using a GPT model.

    Args:
        prompt (str):
            The prompt template to be used for generating the summary.
        gpt_model (str):
            The GPT model to use for generating the summaries.
        kwargs (dict):
            Additional arguments that will be inserted into the prompt template as placeholders.
    Returns:
        final_summary (str):
            final summary based on the summaries
    """
    try:
        gpt_prompts = PromptingGPT()  # Create a new instance of GPT model in each iteration
        final_prompt = get_final_prompt(prompt=prompt, **kwargs)
        final_summary = gpt_prompts.make_prompts(final_prompt, gpt_model=gpt_model).strip()
        return final_summary
    except Exception as e:
        print(f"Error processing final summary: {e}")
        return None