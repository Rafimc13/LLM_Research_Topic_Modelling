import ast

import pandas as pd
from tqdm import tqdm

from utils.GPT_Prompting import PromptingGPT
from utils.load_prompts import get_final_prompt


def topic_extraction(df, text_col, prompt_template, gpt_model, target_column_name, **kwargs):
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
    df[target_column_name] = ""
    for idx, comment in enumerate(tqdm(df[text_col].to_list(), total=len(df))):
        try:
            gpt_prompts = PromptingGPT()  # Create a new instance of GPT model in each iteration
            # define the final prompt based on the prompt template
            kwargs['comment'] = comment
            final_prompt = get_final_prompt(prompt_template, **kwargs)
            response = gpt_prompts.make_prompts(final_prompt, gpt_model=gpt_model).strip()

            _, topics = response.split(":", 1)
            topics = topics.strip()
            df.loc[idx, target_column_name] = topics

        except Exception as e:
            print(f"Error processing topics of '{comment}'")

    df[target_column_name] = df[target_column_name].apply(lambda x: ast.literal_eval(x))
    return df
