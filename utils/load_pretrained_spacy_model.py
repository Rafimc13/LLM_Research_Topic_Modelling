from langdetect import detect, DetectorFactory, LangDetectException
from collections import Counter


def detect_language(text):
    """
    Detect the most common language in a given text.

    Args:
        text (str): The text to be analyzed for language detection.

    Returns:
        str: The detected language code (e.g., 'en' for English, 'gr' for Greek).
             Returns 'unknown' if language detection fails.
    """
    try:
        return detect(text)
    except LangDetectException:
        # Handle specific language detection failure (e.g., ambiguous or too short text)
        return "unknown"
    except Exception as e:
        # Handle any other unforeseen exceptions and return 'unknown'
        print(f"An error occurred: {e}")
        return "unknown"


def load_pretrained_model(df, text_col):
    """
    Load a pretrained language model based on the most common language in a sampled dataset.

    Args:
        df (pandas.DataFrame): The dataframe containing text outputs.
        text_col (str): The name of the column in the dataframe that contains the text outputs.

    Returns:
        df (pandas.DataFrame): The final dataframe.
        name_of_pretrained_model (str): name of the spacy pretrained model.


    Example:
        df_sampled, nlp_model = load_pretrained_model(df, 100, 'text_column')
    """

    # ensure consistent results across different runs
    DetectorFactory.seed = 0

    # apply the language detection function to each row
    df['language'] = df[text_col].apply(detect_language)

    # find the most common language in the dataset
    most_common_lang = Counter(df['language']).most_common(1)[0][0]

    # assign the most common language to the variable
    lang_of_dataset = most_common_lang

    print(f"The language of the dataset is: {lang_of_dataset}")

    # load the proper model based on the language of the dataset
    if lang_of_dataset == 'el':
        name_of_pretrained_model = 'el_core_news_sm'
    else:
        name_of_pretrained_model = 'en_core_web_sm'

    return df, name_of_pretrained_model
