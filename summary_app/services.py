import pandas as pd
from langdetect import detect, DetectorFactory, LangDetectException
from collections import Counter


def detect_timestamp_column(df):
    """
    Detect the most likely timestamp column in the dataframe based on column name or data type.

    Args:
        df (pd.DataFrame): The dataframe to search for timestamp columns if exist.

    Returns:
        str: The name of the detected timestamp column, or None if no timestamp column is found.
    """
    # Common timestamp-related terms to look for
    timestamp_keywords = ['time', 'timestamp', 'date']

    # First, check if there's a column with a name containing timestamp-related keywords
    for col in df.columns:
        if any(keyword in col.lower() for keyword in timestamp_keywords):
            return col

    # Second, check if there's a column with a datetime type
    for col in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            return col

    # If no timestamp-like column is found, return None
    return None


def detect_language(df, column_text):
    """
    Detect the most common language in a given text.

    Args:
        df (pd.DataFrame): The dataframe containing the text data.
        column_text (str): The name of the column containing the text to be analyzed.

    Returns:
        str: The detected language code (e.g., 'en' for English, 'gr' for Greek).
             Returns 'unknown' if language detection fails.
    """

    def detect_language_per_comment(text):
        try:
            return detect(text)
        except LangDetectException:
            # Handle specific language detection failure (e.g., ambiguous or too short text)
            return "unknown"
        except Exception as e:
            # Handle any other unforeseen exceptions and return 'unknown'
            print(f"An error occurred: {e}")
            return "unknown"

    # Ensure consistent results across different runs
    DetectorFactory.seed = 0

    # Apply the language detection function to each row
    df['language'] = df[column_text].apply(detect_language_per_comment)

    # Find the most common language in the dataset
    language = Counter(df['language']).most_common(1)[0][0]

    return language


def divide_comments_by_time(df, timestamp_column=None, num_groups=15):
    """
    Divide comments into groups based on timestamp or randomly if no timestamp is available.
    Adds a new column 'group_number' indicating the assigned group number for each comment.

    Args:
        df (pd.DataFrame): The dataframe containing the comments and optionally timestamps.
        timestamp_column (str): The name of column that contain the timestamp if exists.
        num_groups (int): The number of groups to divide the comments into. Default is 15.

    Returns:
        pd.DataFrame: The original dataframe with an additional 'group_number' column.
        str: The name of the timestamp column if it exists, else None.
    """

    if timestamp_column is None:
        print('No timestamp column detected. Grouping comments by shuffling them randomly.')
        df = df.sample(frac=1).reset_index(drop=True)  # Shuffle the rows if no timestamp
    else:
        print(f'Grouping comments by the timestamp column: {timestamp_column}')
        df = df.sort_values(by=timestamp_column)  # Sort by the detected timestamp

    # Calculate the size of each group
    group_size = len(df) // num_groups
    remainder = len(df) % num_groups

    # Assign group numbers
    group_numbers = []
    start_idx = 0
    for i in range(num_groups):
        end_idx = start_idx + group_size + (1 if i < remainder else 0)  # Handle remainder
        group_numbers.extend([i] * (end_idx - start_idx))  # Assign group number to the current group
        start_idx = end_idx
    # define the name of the column for groups
    col_for_groups = 'group_number'
    # Add the group number column to the dataframe
    df[col_for_groups] = group_numbers

    return df, col_for_groups


def create_json_output(df, summaries, columns_for_extraction):
    """
    Create a JSON structure with summaries, comments, topics, and timestamps for each group.

    Args:
        df (pd.DataFrame): The dataframe containing the comments, topics, and timestamps.
        summaries (list of str): The list of summaries, where each summary corresponds to a group of comments.
        columns_for_extraction (dict): The columns that will be extracted in the final json.

    Returns:
        list of dict: A JSON-like list of dictionaries containing summaries and the respective grouped comments.
    """
    json_output = []
    # define the columns for extraction in the json
    group_col = columns_for_extraction['groups']
    text_col = columns_for_extraction['comments']
    timestamp_col = columns_for_extraction['timestamps']
    topic_col = columns_for_extraction['topics']
    # Ensure group numbers are unique
    unique_groups = df[group_col].unique()

    # Loop through each unique group and generate the output for each group
    for group_number, summary in zip(unique_groups, summaries):
        group_data = {
            "summary": summary,
            "comments": []
        }

        # Filter dataframe for the current group
        group_df = df[df[group_col] == group_number]

        # Add each comment's details to the 'comments' list for this group
        for _, row in group_df.iterrows():
            group_data["comments"].append({
                "comment": row[text_col],
                "topics": row[topic_col],
                "timestamp": row[timestamp_col] if timestamp_col else None  # Handle missing timestamp column
            })

        # Append the group data (summary and comments) to the final JSON output
        json_output.append(group_data)

    return json_output
