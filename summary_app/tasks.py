import pandas as pd
import ast

from tqdm import tqdm
from summary_app.services import detect_timestamp_column, divide_comments_by_time
from utils.GPT_Prompting import PromptingGPT
from utils.load_prompts import get_final_prompt


def topic_extraction(df, text_col, prompt_template, gpt_model, **kwargs):
    """
    Perform topic extraction for each comment using a GPT model.

    Args:
        df (pd.DataFrame): The dataframe containing comments for which topics need to be extracted.
        text_col (str): The column name in the dataframe that contains the text of the comments.
        prompt_template (str): The template to generate the GPT prompt for topic extraction.
        gpt_model (str): The GPT model to be used for topic extraction.
        **kwargs: Additional keyword arguments to be passed to the prompt template.

    Returns:
        pd.DataFrame: The original dataframe with an additional column containing extracted topics for each comment.
        str: The name of the column where the topics are stored.
    """
    topics_column = 'topic'
    df[topics_column] = ""
    for idx, comment in enumerate(tqdm(df[text_col].to_list(), total=len(df))):
        try:
            gpt_prompts = PromptingGPT()  # Create a new instance of GPT model in each iteration
            # define the final prompt based on the prompt template
            kwargs['comment'] = comment
            final_prompt = get_final_prompt(prompt_template, **kwargs)
            response = gpt_prompts.make_prompts(final_prompt, gpt_model=gpt_model).strip()

            _, topics = response.split(":", 1)
            topics = topics.strip()
            df.loc[idx, topics_column] = topics

        except Exception as e:
            print(f"Error processing topics of '{comment}'")
            df.loc[idx, topics_column] = '[]'

    df[topics_column] = df[topics_column].apply(lambda x: ast.literal_eval(x))
    return df, topics_column


def create_summary_for_groups_of_comments(df, text_column, prompt, num_of_groups, gpt_model, **kwargs):
    """
    Generate summaries for multiple groups of comments using a GPT model.

    Args:
        df (pd.DataFrame): The dataframe containing the comments.
        text_column (str): The name of the column contain the comments.
        prompt (str): The prompt template used for generating the summary for each group.
        num_of_groups (int): The desired number of groups in order to create summaries.
        gpt_model (str): The GPT model to use for generating the summaries.
        **kwargs:
            Additional arguments that will be passed into the prompt template.

    Returns:
        df (pd.DataFrame): The updated dataframe containing the comments.
        summaries (list of str):A list of summaries where each summary corresponds to one group of comments.
        final_columns (dict): Final columns for extraction in a json.

    """
    # Detect the most likely timestamp column
    timestamp_column = detect_timestamp_column(df)

    # divide the comments into groups
    df, group_column = divide_comments_by_time(df=df, timestamp_column=timestamp_column, num_groups=num_of_groups)

    summaries = []
    for num_of_group in tqdm(range(num_of_groups), total=num_of_groups):
        try:
            # Create a new instance of GPT model in each iteration
            gpt_prompts = PromptingGPT()
            # keep the comments from the selected group
            df_grouped = df[df[group_column] == num_of_group]
            # Update kwarg of comments with the chosen comments
            kwargs['comments'] = df_grouped[text_column].to_list()
            kwargs['previous_summaries'] = summaries[-5:]
            final_prompt = get_final_prompt(prompt=prompt, **kwargs)
            response = gpt_prompts.make_prompts(final_prompt, gpt_model=gpt_model).strip()
            # store the summaries
            summaries.append(response)

        except Exception as e:
            print(f"Error processing summary: {e}")
            summaries.append(None)
    final_columns = {
        'comments': text_column,
        'groups': group_column,
        'timestamps': timestamp_column,
    }
    return df, summaries, final_columns


def final_summary_of_divided_comments(prompt, gpt_model, **kwargs):
    """
    Generate final summary based on summaries of comments using a GPT model.

    Args:
        prompt (str):
            The prompt template to be used for generating the summary.
        gpt_model (str):
            The GPT model to use for generating the summaries.
        kwargs (list):
            Additional arguments that will be inserted into the prompt template as placeholders.
    Returns:
        final_summary (str): final summary based on the summaries
    """
    try:
        gpt_prompts = PromptingGPT()  # Create a new instance of GPT model in each iteration
        final_prompt = get_final_prompt(prompt=prompt, **kwargs)
        final_summary = gpt_prompts.make_prompts(final_prompt, gpt_model=gpt_model).strip()
        return final_summary
    except Exception as e:
        print(f"Error processing final summary: {e}")
        return None


