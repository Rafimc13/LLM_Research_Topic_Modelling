from models.LLM_Classifier import GPT_Classifier
from utils.GPT_Prompting import PromptingGPT
from utils.load_prompts import get_final_prompt


def classify_comments(df, text_col, prompt_name, gpt_model='gpt-4o'):
    """
    Classify comments based on LLM
    """
    pred_labels = GPT_Classifier(df[text_col].to_list(), name_of_prompt=prompt_name, GPT_model=gpt_model)
    df['labels'] = pred_labels

    return df


def summarize_comments_by_label(df, text_col, prompt_name, gpt_model, **kwargs):
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


def final_summary_of_labeled_comments(prompt, gpt_model, **kwargs):
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

