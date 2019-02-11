import pandas as pd
from nltk.corpus import stopwords
import string
from replacers import RepeatReplacer
from replacers import RegexpReplacer
import tqdm


pd.set_option('display.expand_frame_repr', False)


def cleanup_doc(corpus):
    # correct expanding contractions
    replacer = RegexpReplacer()
    corpus['removed_punctuation'] = corpus.apply(lambda x: replacer.replace(x['FeedbackComment']), axis=1)
    print(corpus)


pos_tweets = [('I love thiiiis car?', 'positive'),
    ('This view is amaaaazing!!@#', 'positive'),
    ('I feel great This morning%$%&', 'positive'),
    ('I am so excited about the concert^*&(&', 'positive'),
    ('He\'s my best Friend)(*', 'positive'), ("can't is a contraction", 'negative')]

data = pd.DataFrame(pos_tweets)
data.columns = ["FeedbackComment", "class"]

comment = pd.DataFrame(data['FeedbackComment'])
comment.columns = ["FeedbackComment"]

cleanup_doc(comment)
