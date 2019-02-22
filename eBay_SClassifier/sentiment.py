from textblob_de import TextBlobDE as TextBlobDE
import pandas as pd
from polyglot.text import Text


pd.set_option('display.expand_frame_repr', False)


def sentiment_de(text):
    rate_blob = 0
    blob = TextBlobDE(text)
    for sentence in blob.sentences:
        rate_blob = rate_blob + sentence.sentiment.polarity
    if rate_blob > 0:
        return 'Positive'
    elif rate_blob < 0:
        return 'negative'
    else:
        return 'neutral'


def sentiment_polyglot(txt):
    doc_rate = 0
    text = Text(txt, hint_language_code='de')
    for sentence in text.sentences:
        word_rate = 0
        for word in sentence.words:
            try:
                word_rate = word_rate + word.polarity
            except:
                word_rate = word_rate + 0
        doc_rate = doc_rate + word_rate
    if doc_rate > 0:
        return 'positive'
    elif doc_rate < 0:
        return 'negative'
    else:
        return 'neutral'


data_set = pd.read_stata("data/ebay2_indegrees_comments.dta", chunksize=10,
                         columns=['FeedbackID', 'FeedbackComment', 'FeedbackValue'])
for chunk in data_set:
    # chunk['sentiment_textblob'] = chunk.apply(lambda x: sentiment_de(x['FeedbackComment']), axis=1)
    chunk['sentiment_polyglot'] = chunk.apply(lambda y: sentiment_polyglot(y['FeedbackComment']), axis=1)
    print(chunk)

