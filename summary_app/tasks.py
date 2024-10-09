import pandas as pd
import random
import ast

from tqdm import tqdm
from utils.GPT_Prompting import PromptingGPT
from utils.load_prompts import get_final_prompt


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
    df['topics'] = ""
    for idx, comment in enumerate(tqdm(df[text_col].to_list(), total=len(df))):
        try:
            gpt_prompts = PromptingGPT()  # Create a new instance of GPT model in each iteration
            # define the final prompt based on the prompt template
            kwargs['comment'] = comment
            final_prompt = get_final_prompt(prompt_template, **kwargs)
            response = gpt_prompts.make_prompts(final_prompt, gpt_model=gpt_model).strip()

            _, topics = response.split(":", 1)
            topics = topics.strip()
            df.loc[idx, 'topics'] = topics

        except Exception as e:
            print(f"Error processing topics of '{comment}'")

    df['topics'] = df['topics'].apply(lambda x: ast.literal_eval(x))
    return df


def divide_comments_by_time(df, text_column='text', timestamp_column='timestamp', num_groups=15):
    """
    Divide comments into groups based on timestamp or randomly if no timestamp is available.

    This function first checks if the dataframe contains a timestamp column. If the timestamp
    column is present, it sorts the comments by timestamp before dividing them into the specified
    number of groups. If no timestamp column exists, the comments are shuffled randomly and then divided.

    Args:
        df (pd.DataFrame): The dataframe containing the comments and optionally timestamps.
        text_column (str): The column name where the comments are stored. Default is 'text'.
        timestamp_column (str): The column name where the timestamps are stored. Default is 'timestamp'.
        num_groups (int): The number of groups to divide the comments into. Default is 15.

    Returns:
        list of lists: A list where each element is a list containing the comments for each group.
    """
    # Check if the timestamp column exists
    if timestamp_column not in df.columns:
        print('Comments do not contain timestamp. Continue the group by shuffle them.')
        # Shuffle the sorted comments randomly
        comments = df[text_column].tolist()
        random.shuffle(comments)
    else:
        # Sort the dataframe by the timestamp column
        df = df.sort_values(by=timestamp_column)
        comments = df[text_column].to_list()

    # Calculate the size of each group
    group_size = len(comments) // num_groups
    remainder = len(comments) % num_groups

    # Split comments into groups
    groups = []
    start_idx = 0
    for i in range(num_groups):
        end_idx = start_idx + group_size + (1 if i < remainder else 0)  # Handle remainder
        groups.append(comments[start_idx:end_idx])
        start_idx = end_idx

    return groups


def create_summary_for_groups_of_comments(groups, prompt, gpt_model, **kwargs):
    """
    Generate summaries for multiple groups of comments using a GPT model.

    Args:
        groups (list):
            A list of groups where each group contains a list of comments to be summarized.
        prompt (str):
            The prompt template to be used for generating the summary.
        gpt_model (str):
            The GPT model to use for generating the summaries.
        kwargs (dict):
            Additional arguments that will be inserted into the prompt template as placeholders.
    Returns:
        list of str:
            A list of summaries where each summary corresponds to one group of comments. If an error occurs,
            'None' will be returned in place of the summary for the group.
    """
    summaries = []
    for group in tqdm(groups, total=len(groups)):
        try:
            gpt_prompts = PromptingGPT()  # Create a new instance of GPT model in each iteration
            # Update kwarg of comments with the chosen comments
            kwargs['comments'] = group
            kwargs['previous_summaries'] = summaries[-5:]
            final_prompt = get_final_prompt(prompt=prompt, **kwargs)
            response = gpt_prompts.make_prompts(final_prompt, gpt_model=gpt_model).strip()
            # store the summaries
            summaries.append(response)

        except Exception as e:
            print(f"Error processing summary: {e}")
            summaries.append(None)

    return summaries


def final_summary_of_divided_comments(prompt, gpt_model, **kwargs):
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


