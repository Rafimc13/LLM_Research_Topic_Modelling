import pandas as pd
import os

from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from summary_app.services import detect_language, create_json_output
from summary_app.tasks import (divide_comments_by_time,
                               topic_extraction,
                               create_summary_for_groups_of_comments)
from utils.load_prompts import load_chosen_prompt

app = Flask(__name__, static_folder='./frontend/dist', template_folder='./frontend/dist')

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'csv'}

# Global variable to hold the uploaded comments data and user input
comments_df = pd.DataFrame()
text_column_name = ''
client_topic = ''
number_of_grouped_summaries = None


def allowed_file(filename):
    """
    Function to check allowed file types
    Args:
        filename (str): filename of the data

    Returns:
        complete filename path

    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return send_from_directory(app.template_folder, 'index.html')


@app.route('/<path:path>')
def serve_static_files(path):
    # Serve static files (JS, CSS, etc.) for the Vue.js app
    return send_from_directory(app.static_folder, path)


@app.route('/upload', methods=['POST'])
def upload_file():
    global comments_df, text_column_name, client_topic
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'No file part'})

    file = request.files['file']
    text_column_name = request.form.get('text_column', 'comment')
    client_topic = request.form.get('topic', None)

    if file.filename == '':
        return jsonify({'success': False, 'error': 'No selected file'})

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Load the uploaded CSV into a DataFrame
        comments_df = pd.read_csv(filepath)
        comments_df = comments_df.iloc[:100]  # Limit the size for testing purposes
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'error': 'Invalid file type'})


@app.route('/get_grouped_summaries', methods=['POST'])
def get_summaries_in_groups():
    global comments_df, text_column_name, client_topic
    if comments_df.empty:
        return jsonify({'error': 'No comments data available'}), 400

    # Get the column name from the user's input
    text_col = request.json.get('text_column', text_column_name)
    topic = request.json.get('topic', client_topic)

    # find the language of the comments
    language = detect_language(df=comments_df, column_text=text_col)
    # load the prompt template for summarizing comments grouped by label
    prompt_template_topics = load_chosen_prompt(prompt_name='prompt_for_keyword_extraction')
    # Extract topics and generate summaries for each time window
    comments_df, topics_column = topic_extraction(df=comments_df,
                                                  text_col=text_col,
                                                  prompt_template=prompt_template_topics,
                                                  gpt_model='gpt-4o',
                                                  topic=topic,
                                                  language=language)

    # Load the prompt template
    prompt_template_summaries = load_chosen_prompt(prompt_name='prompt_for_summarizing_multiple_comments')
    comments_df, summaries, final_columns = create_summary_for_groups_of_comments(df=comments_df,
                                                                                  text_column=text_col,
                                                                                  prompt=prompt_template_summaries,
                                                                                  num_of_groups=15,
                                                                                  gpt_model='gpt-4o',
                                                                                  language=language,
                                                                                  topic=topic)
    # create the final columns for extraction
    final_columns['topics'] = topics_column
    # Create JSON output combining summaries and comments data
    json_output = create_json_output(df=comments_df,
                                     summaries=summaries,
                                     columns_for_extraction=final_columns)

    return jsonify({'summaries': json_output})


@app.route('/get_final_summary', methods=['POST'])
def get_final_summary():
    return None


if __name__ == '__main__':
    # Create uploads folder if it doesn't exist
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    app.run(debug=True)
