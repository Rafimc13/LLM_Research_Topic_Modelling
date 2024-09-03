from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer


def prepare_data_LR(x_train, x_test):
    """
    Prepare the data for Logistic Regression Classifier
    :param x_train: training dataset with comments
    :param x_test: Training dataset with labels
    :return x_train, x_test vectorized
    """

    # Tokenize text data and convert to matrix of token counts
    vectorizer = CountVectorizer()
    x_train = vectorizer.fit_transform(x_train)
    x_test = vectorizer.transform(x_test)

    return x_train, x_test


def train_logistic_regression(x_train, y_train):
    """
    Train a logistic regression model using the provided training data.

    Parameters:
    - x_train: numpy array or sparse matrix, shape (n_samples, n_features)
      Training input samples.

    - y_train: numpy array, shape (n_samples,)
      Target values (class labels) for training.

    Returns:
    - model: LogisticRegression object
      Trained logistic regression model.
    """

    # Initialize Logistic Regression model
    model = LogisticRegression(max_iter=1000)

    # Train the model
    model.fit(x_train, y_train)

    return model


def evaluate_logistic_regression(model, x_test, y_test):
    """
    Evaluate the LR model with the test set
    :param model: Logistic Regression model trained
    :param x_test: comments for evaluating the model
    :param y_test: labels for evaluating the model
    :return: Classification Report
    """
    # Predict on test data
    y_pred = model.predict(x_test)

    # Print classification report
    cls_report = classification_report(y_test, y_pred)
    print(cls_report)
    return cls_report
