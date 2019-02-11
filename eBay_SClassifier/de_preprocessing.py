import pandas as pd
from nltk.corpus import stopwords
import string
from replacers import RepeatReplacer
from replacers import RegexpReplacer
import tqdm


pd.set_option('display.expand_frame_repr', False)


def cleanup_doc(corpus):

    # correct expanding contractions
    # replacer = RegexpReplacer()
    # corpus['removed_punctuation'] = corpus.apply(lambda x: replacer.replace(x['FeedbackComment']), axis=1)
    # print(corpus)

    # correct repeating characters
    repeater = RepeatReplacer()
    corpus['removed_repetition'] = corpus.apply(lambda y: repeater.repeat(y['FeedbackComment']), axis=1)
    print(corpus)






