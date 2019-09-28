import pickle

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from stop_words import get_stop_words


def main():
    df = pd.read_csv('../../resources/lenta-ru-news.csv', nrows=100000)
    df = df.dropna()
    df = df[df['tags'] != 'Все']

    X = df['text']
    y = df['tags']

    token_pattern = r"(?u)\b\w\w+\b"
    vectorizer = CountVectorizer(
        token_pattern=token_pattern,
        stop_words=get_stop_words('russian')
    )
    classifier = SGDClassifier(
        loss="log", class_weight='balanced',
        penalty='l1', alpha=0.0000009, n_jobs=-1
    )
    text_clf = Pipeline([('vect', vectorizer),
                         ('tfidf', TfidfTransformer()),
                         ('clf', classifier)])
    # train and dave
    # text_clf.fit(X, y)
    # pickle.dump(text_clf, open("../../storage/model.ml", 'wb'))

    # test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)
    text_clf = text_clf.fit(X_train, y_train)
    predicted = text_clf.predict(X_test)
    print(np.mean(predicted == y_test))


if __name__ == "__main__":
    main()
