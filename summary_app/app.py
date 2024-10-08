import pandas as pd
import os

from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from summary_app.tasks import divide_comments_by_time, topic_extraction, create_summary_for_groups_of_comments
from utils.load_prompts import load_chosen_prompt

app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'csv'}

# Global variable to hold the uploaded comments data and user input
comments_df = pd.DataFrame()
text_column_name = ''
client_topic = ''


# Function to check allowed file types
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template('index.html')


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
        comments_df = comments_df.iloc[:100]
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'error': 'Invalid file type'})


@app.route('/get_summary', methods=['POST'])
def get_summary():
    global comments_df, text_column_name, client_topic
    if comments_df.empty:
        return jsonify({'error': 'No comments data available'}), 400

    # Get the column name from the user's input
    text_col = request.json.get('text_column', text_column_name)
    topic = request.json.get('topic', client_topic)
    language = 'English'
    # Extract topics and generate summaries for each time window
    groups = divide_comments_by_time(comments_df, text_column=text_col, timestamp_column='timestamp', num_groups=15)
    # load the prompt template
    prompt_template = load_chosen_prompt(prompt_name='prompt_for_summarizing_multiple_comments')
    summaries = create_summary_for_groups_of_comments(groups=groups,
                                                      prompt=prompt_template,
                                                      gpt_model='gpt-4o',
                                                      language=language,
                                                      topic=topic)

    return jsonify({'summaries': summaries})


@app.route('/get_topics', methods=['POST'])
def get_topics():
    # global comments_df, client_topic, text_column_name
    # if comments_df.empty:
    #     return jsonify({'error': 'No comments data available'}), 400
    #
    # # Get the topic from the user's input
    # topic = request.json.get('topic', client_topic)
    #
    # # Load the prompt template for topic extraction
    # prompt_template_topics = load_chosen_prompt(prompt_name='prompt_for_topic_extraction')
    # topics_df, df_topics = topic_extraction(df=comments_df,
    #                                         text_col=text_column_name,
    #                                         prompt_template=prompt_template_topics,
    #                                         gpt_model='gpt-4o',
    #                                         topic=topic)
    return None
    # return jsonify(df_topics.to_dict(orient='records'))


if __name__ == '__main__':
    # Create uploads folder if it doesn't exist
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
