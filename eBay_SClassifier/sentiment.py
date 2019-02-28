from textblob_de import TextBlobDE as TextBlobDE
import pandas as pd
from polyglot.text import Text


pd.set_option('display.expand_frame_repr', False)


def sentiment_de(text):
    rate_blob = 0
    blob = TextBlobDE(text)
    for sentence in blob.sentences:
        rate_blob = rate_blob + sentence.sentiment.polarity
    return rate_blob
    # if rate_blob > 0:
    #     return 'Positive'
    # elif rate_blob < 0:
    #     return 'negative'
    # else:
    #     return 'neutral'


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
    return doc_rate
    # if doc_rate > 0:
    #     return 'positive'
    # elif doc_rate < 0:
    #     return 'negative'
    # else:
    #     return 'neutral'


data_set = pd.read_stata("data/preprocessed.dta",
                         columns=['FeedbackID', 'PFeedbackComment', 'FeedbackValue'])
# for chunk in data_set:
data_set['sentiment_textblob'] = data_set.apply(lambda x: sentiment_de(x['PFeedbackComment']), axis=1)
data_set['sentiment_polyglot'] = data_set.apply(lambda y: sentiment_polyglot(y['PFeedbackComment']), axis=1)
print(data_set)
outfile = 'data/sentiment2.dta'
data_set.to_stata(outfile)
