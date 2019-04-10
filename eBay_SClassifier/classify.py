from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from nltk.corpus import stopwords
import SentimentClass
from sklearn.svm import LinearSVC
from pprint import pprint
from sklearn.naive_bayes import MultinomialNB
from sklearn.multiclass import OneVsRestClassifier
from sklearn.pipeline import Pipeline
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import classification_report


pd.set_option('display.expand_frame_repr', False)

class SClassifier(object):

    def __init__(self, corpus, target):
        """Initialize the object with training data and setting.
        :param corpus: Data for training
        :type corpus: list
        :param target: Target binary values
        :type target: list
        """
        self.corpus = corpus   # train data
        self.target = target
        self.categories = ['positive', 'negative', 'neutral']

    def train(self, **kwargs):
        """Train classifier.
        :param kwargs: Arbitrary keyword arguments: classifier='LR'
        :type kwargs: str
        :return: Object
        """
        vectorizer = CountVectorizer(binary=False, ngram_range=(1, 2))
        # vectorizer = TfidfVectorizer(binary=False, ngram_range=(1,2))
        self.Doc_term_matrix = vectorizer.fit_transform(self.corpus)
        # Build Classifier
        X_train, X_val, y_train, y_val = train_test_split(self.Doc_term_matrix, self.target, train_size=0.75,
                                                          test_size=0.25, random_state = 0)
        if kwargs is not None and 'classifier' in kwargs:
            # Logistic regression
            if kwargs['classifier'] == 'LR':
                final_model = OneVsRestClassifier(LogisticRegression(C=0.25, solver='lbfgs', multi_class='multinomial'))
                final_model.fit(X_train, y_train)
                LR_predictions = final_model.predict(X_val)
                print("Final Accuracy for LR: %s"
                      % accuracy_score(y_val, LR_predictions))
                # print("classification reports:\n", classification_report(y_val, LR_predictions))
                print(LR_predictions)

            # Support vector machine
            elif kwargs['classifier'] == 'SVM':
                final_svm_ngram =OneVsRestClassifier(LinearSVC(C=0.01))
                final_svm_ngram.fit(X_train, y_train)
                svm_predictions = final_svm_ngram.predict(X_val)
                print("Final Accuracy for SVM: %s"
                      % accuracy_score(y_val, svm_predictions ))
                # print("classification reports:\n", classification_report(y_val, svm_predictions))

                print(svm_predictions )

            # Naive Bayes
            elif kwargs['classifier'] == 'NB':
                naive_model = OneVsRestClassifier(MultinomialNB(fit_prior=True, class_prior=None))
                naive_model = MultinomialNB()
                naive_model.fit(X_train, y_train)
                gnb_predictions = naive_model.predict(X_val)
                print("Final Accuracy for NB: %s"
                      % accuracy_score(y_val, gnb_predictions))
                # print("classification reports:\n", classification_report(y_val, gnb_predictions))

                print(gnb_predictions)

            # training a DescisionTreeClassifier
            elif kwargs['classifier'] == 'DT':
                dtree_model = DecisionTreeClassifier(max_depth=2).fit(X_train, y_train)
                dtree_predictions = dtree_model.predict(X_val)
                print("Final Accuracy for DT: %s"
                      % accuracy_score(y_val, dtree_predictions))
                # print("classification reports:\n", classification_report(y_val, dtree_predictions))

                print(dtree_predictions)

            elif kwargs['classifier'] == 'KNN':
                knn = KNeighborsClassifier(n_neighbors=7).fit(X_train, y_train)
                # accuracy on X_test
                accuracy = knn.score(X_val, y_val)
                print(accuracy)
                knn_predictions = knn.predict(X_val)
                print("Final Accuracy for KNN: %s"
                      % accuracy_score(y_val, knn_predictions))
                # print("classification reports:\n", classification_report(y_val, knn_predictions))

                print(knn_predictions)




# data_set = pd.read_stata('data/New folder/eng.dta', columns=['PFeedbackComment', 'FeedbackValue'])
data_set = pd.read_stata('data/random_sample3.dta', columns=['FeedbackComment', 'FeedbackValue'])
print(data_set.shape)
#
corpus = data_set['FeedbackComment']
target = data_set['FeedbackValue']

stop = stopwords.words('german')
x = SentimentClass.PreProcess(corpus)
data_set['removed_stopwords'] = x.remove_stop_words(stop)
corpus = data_set['removed_stopwords']
x = SentimentClass.PreProcess(corpus)
data_set['normalized_text'] = x.get_stemmed_text()
corpus = data_set['normalized_text']

y = SClassifier(corpus, target)
y.train(classifier = 'NB')
y.train(classifier = 'LR')
y.train(classifier = 'SVM')
y.train(classifier = 'DT')
y.train(classifier = 'KNN')

