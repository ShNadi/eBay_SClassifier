import pandas as pd
from nltk.corpus import stopwords
import string
from replacers import RepeatReplacer
from replacers import RegexpReplacer
import tqdm
from spellchecker import SpellChecker


pd.set_option('display.expand_frame_repr', False)


def clean(corpus):
    for row in corpus:
        # remove lines without comments
        print("Removing empty rows...")
        row.drop(row[row.FeedbackComment == 'no comment'].index, inplace=True)
        print("empty rows are removed!")
        print("Renaming FeedbackValue...")
        # change FeedbackValue field to some meaningful values. 1 -> negative,  2 -> positive, 8-> neutral
        row.FeedbackValue.replace([1, 2, 8], ['negative', 'positive', 'neutral'], inplace=True)
        print("FeedbackValue column is updated!")
        return corpus


def pre_process(corpus):

    # correct expanding contractions
    replacer = RegexpReplacer()
    corpus['removed_punctuation'] = corpus.apply(lambda x: replacer.replace(x['FeedbackComment']), axis=1)
    # print(corpus)

    # correct repeating characters
    repeater = RepeatReplacer()
    corpus['removed_repetition'] = corpus.apply(lambda y: repeater.repeat(y['removed_punctuation']), axis=1)
    print(corpus)

    # # correct spelling
    # spell = SpellChecker(language='de')
    # misspelled = spell.unknown(['somthing', 'is', 'hapenning', 'hee'])
    # for word in misspelled:
    #     # Get the one `most likely` answer
    #     print(spell.correction(word))
    #
    #     # Get a list of `likely` options
    #     print(spell.candidates(word))

    # Remove stop words
    stop_set = stopwords.words('german')
    corpus['FeedbackComment_without_stopwords'] = \
        corpus['FeedbackComment'].apply(lambda x: ' '.join([word for word in x.split() if word not in stop_set]))
    # print(corpus)

    # Remove punctuations
    corpus['FeedbackComment_without_punctuations'] = corpus['FeedbackComment_without_stopwords'].apply(
        lambda x: ''.join([i for i in x
                           if i not in string.punctuation]))

    # convert all characters to lowercase
    corpus['FeedbackComment_lowercase'] = corpus['FeedbackComment_without_punctuations'].str.lower()
    print(corpus)

    return corpus





