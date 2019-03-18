from textblob_de import TextBlobDE as TextBlobDE
import pandas as pd
from polyglot.text import Text
from afinn import Afinn
from textblob import TextBlob

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

# compute sentiment scores (polarity) and labels by afinn on english text
def afinn_lex(text):
    af = Afinn()
    sentiment_scores = [af.score(article) for article in text]
    sentiment_category = ['positive' if score > 0
                          else 'negative' if score < 0
                                else 'neutral'
                                     for score in sentiment_scores]
    return sentiment_scores, sentiment_category


# compute sentiment scores (polarity) and labels by textblob on english text
def sentiment_textblob(text):
    sentiment_scores_tb = [round(TextBlob(article).sentiment.polarity, 3) for article in text]
    sentiment_category_tb = ['positive' if score > 0
                                else 'negative' if score < 0
                                    else 'neutral'
                                        for score in sentiment_scores_tb]
    return sentiment_scores_tb, sentiment_category_tb

# # call sentiment_de and sentiment_polyglot
# data_set = pd.read_stata("data/preprocessed.dta",
#                          columns=['FeedbackID', 'PFeedbackComment', 'FeedbackValue'])
# # for chunk in data_set:
# data_set['sentiment_textblob'] = data_set.apply(lambda x: sentiment_de(x['PFeedbackComment']), axis=1)
# data_set['sentiment_polyglot'] = data_set.apply(lambda y: sentiment_polyglot(y['PFeedbackComment']), axis=1)
# print(data_set)
# outfile = 'data/sentiment2.dta'
# data_set.to_stata(outfile)


# call afinn_lex function
data_set = pd.read_stata("data/sentiment3.dta", columns=['FeedbackID', 'PFeedbackComment', 'FeedbackValue',
                                                         'sentiment_textblob', 'sentiment_polyglot',
                                                         'FeedbackComment_en', 'afinn_score', 'afinn_category'])

# data_set['afinn_score'], data_set['afinn_category'] = afinn_lex(data_set['FeedbackComment_en'])
data_set['textblob_score'], data_set['textblob_category'] = sentiment_textblob(data_set['FeedbackComment_en'])
print(data_set)

outfile = 'data/sentiment4.dta'
data_set.to_stata(outfile)


