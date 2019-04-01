from textblob_de import TextBlobDE
from polyglot.text import Text
from afinn import Afinn
from textblob import TextBlob
import string
from spellchecker import SpellChecker
import pandas as pd
from textblob_de import TextBlobDE as TextBlobDE
from googletrans import Translator
import pydeepl
import matplotlib.pyplot as plt
import numpy as np
import itertools
import matplotlib.pyplot as plt
import numpy as np
import itertools
from langdetect import detect

# expand DataFrame in output
pd.set_option('display.expand_frame_repr', False)


class PreProcess(object):
    def __init__(self, feedbackcomment):
        self.feedbackcomment = feedbackcomment

    # Correct misspelling
    def check_spell(self, row, i=[0]):
        i[0] += 1
        print(i[0])
        misspelled_count = 0
        try:
            lang = detect(row)
        except:
            return row, misspelled_count
        word = row.split()
        e = pd.Series([])

        checked = ""
        ch = pd.Series([])
        if lang == 'de':
            spell = SpellChecker(language='de')
            misspelled = spell.unknown(word)
            misspelled_count = len(misspelled)
            for x in word:
                if x in misspelled:
                    checked = checked + " " + spell.correction(x)
                else:
                    checked = checked + " " + x

            return checked, misspelled_count
        else:
            return row, misspelled_count

    def check(self):
        df =pd.DataFrame([self.check_spell(row) for row in self.feedbackcomment], columns=['FbComment_checkedspell',
                                                                                           'misspelled_count'])
        return df

    # Remove punctuation
    def remove_punc(self, row):
        str_punc = ''
        for i in row:
            if i not in string.punctuation:
                str_punc = str_punc + i
            else:
                str_punc = str_punc + ' '

        return str_punc

    def remove_punctuation(self):
        df = [self.remove_punc(row) for row in self.feedbackcomment]
        return df

    # Remove Stopwords from corpus
    def remove_stop_words(self, stop):
        removed_stop_words = []
        for review in self.feedbackcomment:
            removed_stop_words.append(
                ' '.join([word for word in review.split()
                          if word not in stop])
            )
        return removed_stop_words

    # Normalization
    def get_stemmed_text(self):
        from nltk.stem.snowball import SnowballStemmer
        stemmer = SnowballStemmer("german")
        return [' '.join([stemmer.stem(word) for word in review.split()]) for review in self.feedbackcomment]


class TranslateEn(object):
    def __init__(self, feedbackcomment):
        self.feedbackcomment = feedbackcomment

    def deepl_translate(self):
        for row in self.feedbackcomment:
            translation = pydeepl.translate(row, 'DE', from_lang='EN')
            print(translation)

    # translate German text to English by google translate
    def google_translate_de(self):
        str = ''
        for row in self.feedbackcomment:
            translator = Translator(row)
            txt = translator.translate(row, 'en')
            str = str + txt.text
        return str

    def translate_de(self):
        str = ''
        for row in self.feedbackcomment:
            blob = TextBlobDE(row)
            if blob.detect_language() == "en":
                blob_en = blob
            else:
                blob_en = blob.translate(to="en")
            str = str + blob_en.string
        return str


class SentimentLexDe(object):
    def __init__(self, feedbackcomment):
        self.feedbackcomment = feedbackcomment

    # Uses Textblob_de to calculate comments polarity
    def sentiment_textblobde(self):
        textblobde_score = [round(TextBlobDE(article).sentiment.polarity, 3) for article in self.feedbackcomment]
        textblobde_category = ['positive' if score > 0
                               else 'negative' if score < 0
                               else 'neutral'
                               for score in textblobde_score]
        return textblobde_score, textblobde_category

    # Uses Polyglot to calculate comments polarity
    def sentiment_polyglot(self):
        polyglot_score = [round(Text(comment, hint_language_code='de').polarity, 3) for comment in self.feedbackcomment]
        polyglot_category = ['positive' if score > 0
                             else 'negative' if score < 0
                             else 'neutral'
                             for score in polyglot_score]
        return polyglot_score, polyglot_category


# compute polarity for English translated comments
class SentimentLexEn(object):
    def __init__(self, feedbackcomment):
        self.feedbackcomment = feedbackcomment

    # compute sentiment scores (polarity) and labels by afinn on English text
    def sentiment_afinn(self):
        af = Afinn()
        afinn_scores = [af.score(article) for article in self.feedbackcomment]
        afinn_category = ['positive' if score > 0
                          else 'negative' if score < 0
                          else 'neutral'
                          for score in afinn_scores]
        return afinn_scores, afinn_category

    # compute sentiment scores (polarity) and labels by textblob on english text
    def sentiment_textblob(self):
        textblob_scores = [round(TextBlob(article).sentiment.polarity, 3) for article in self.feedbackcomment]
        textblob_category = ['positive' if score > 0
                             else 'negative' if score < 0
                             else 'neutral'
                             for score in textblob_scores]
        return textblob_scores, textblob_category

class Plot_sentiment(object):
    def __init__(self):
        pass


    def plot_confusion_matrix(self, x, cm, target_names, title='Confusion matrix', cmap=None, normalize=False):

        accuracy = np.trace(cm) / float(np.sum(cm))
        misclass = 1 - accuracy

        if cmap is None:
            cmap = plt.get_cmap('Blues')

        plt.figure(figsize=(8, 6))
        plt.imshow(cm, interpolation='nearest', cmap=cmap)
        plt.title(title)
        plt.colorbar()

        if target_names is not None:
            tick_marks = np.arange(len(target_names))
            plt.xticks(tick_marks, target_names, rotation=45)
            plt.yticks(tick_marks, target_names)

        if normalize:
            cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]

        thresh = cm.max() / 1.5 if normalize else cm.max() / 2
        for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
            if normalize:
                plt.text(j, i, "{:0.4f}".format(cm[i, j]),
                         horizontalalignment="center",
                         color="white" if cm[i, j] > thresh else "black")
            else:
                plt.text(j, i, "{:,}".format(cm[i, j]),
                         horizontalalignment="center",
                         color="white" if cm[i, j] > thresh else "black")

        plt.tight_layout()
        plt.ylabel('FeedbackValue')
        plt.xlabel(x + '\naccuracy={:0.4f}; misclass={:0.4f}'.format(accuracy, misclass))
        plt.show()



