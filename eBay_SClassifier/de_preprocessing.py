import pandas as pd
from nltk.corpus import stopwords
import string
from replacers import RepeatReplacer
from replacers import RegexpReplacer
import tqdm
from spellchecker import SpellChecker

pd.set_option('display.expand_frame_repr', False)


# def check_spell4(text, i=[0]):
#     i[0] += 1
#     print(i[0])
#     print("still working")
#     word = text.split()
#     strc = ""
#     spell = SpellChecker(language='de')
#     misspelled = spell.unknown(word)
#     for w in word:
#         if w in misspelled:
#             strc = strc + " " + spell.correction(w)
#         else:
#             strc = strc + " " + w
#     return strc
def check_spell4(text, i=[0]):
    i[0] += 1
    print(i[0])
    word = text.split()
    strc = ""
    spell = SpellChecker(language='de')
    misspelled = spell.unknown(word)
    for w in word:
        if w in misspelled:
            strc = strc + " " + spell.correction(w)
        else:
            strc = strc + " " + w
    return strc


# def clean(corpus):
#     for row in corpus:
#         # remove lines without comments
#         print("Removing empty rows...")
#         row.drop(row[row.FeedbackComment == 'no comment'].index, inplace=True)
#         print("empty rows are removed!")
#         print("Renaming FeedbackValue...")
#         # change FeedbackValue field to some meaningful values. 1 -> negative,  2 -> positive, 8-> neutral
#         row.FeedbackValue.replace([1, 2, 8], ['negative', 'positive', 'neutral'], inplace=True)
#         print("FeedbackValue column is updated!")
#         return corpus


# def clean(corpus):
#
#     # # remove lines without comments
#     # print("Removing empty rows...")
#     # corpus.drop(corpus[corpus.FeedbackComment == 'no comment'].index, inplace=True)
#     # print("empty rows are removed!")
#     print("Renaming FeedbackValue...")
#     # change FeedbackValue field to some meaningful values. 1 -> negative,  2 -> positive, 8-> neutral
#     corpus.FeedbackValue.replace([1, 2, 8], ['negative', 'positive', 'neutral'], inplace=True)
#     print("FeedbackValue column is updated!")
#     return corpus


def pre_process(corpus):

    # change FeedbackValue field to some meaningful values. 1 -> negative,  2 -> positive, 8-> neutral
    corpus.FeedbackValue.replace([1, 2, 8], ['negative', 'positive', 'neutral'], inplace=True)
    print("FeedbackValue column is updated!")

    # correct expanding contractions
    # replacer = RegexpReplacer()
    # corpus['removed_punctuation'] = corpus.apply(lambda x: replacer.replace(x['FeedbackComment']), axis=1)
    # print(corpus)

    # correct repeating characters
    # repeater = RepeatReplacer()
    # corpus['removed_repetition'] = corpus.apply(lambda y: repeater.repeat(y['removed_punctuation']), axis=1)
    # print(corpus)

    # correct spelling
    corpus['FeedbackComment_CorrectSelling'] = corpus.apply(lambda y: check_spell4(y['FeedbackComment']), axis=1)
    print("correct spelling is done")

    # Remove stop words
    # stop_set = stopwords.words('german')
    # corpus['FeedbackComment_without_stopwords'] = \
    #     corpus['FeedbackComment'].apply(lambda x: ' '.join([word for word in x.split() if word not in stop_set]))
    # print(corpus)

    # Remove punctuations
    corpus['FeedbackComment_without_punctuations'] = corpus['FeedbackComment_CorrectSelling'].apply(
        lambda x: ''.join([i for i in x
                           if i not in string.punctuation]))
    print("punctuations are removed")

    # convert all characters to lowercase
    corpus['FeedbackComment_lowercase'] = corpus['FeedbackComment_without_punctuations'].str.lower()
    print("turned to lowercase")

    corpus['PFeedbackComment'] = corpus['FeedbackComment_lowercase']
    return corpus




