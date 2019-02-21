from textblob_de import TextBlobDE as TextBlobDE
import pandas as pd


pd.set_option('display.expand_frame_repr', False)


def sentiment_de(text):
    rate_blob = 0
    blob = TextBlobDE(text)
    for sentence in blob.sentences:
        rate_blob = rate_blob + sentence.sentiment.polarity
    if rate_blob > 0:
        return 'Positive'
    if rate_blob < 0:
        return 'negative'
    if rate_blob == 0:
        return 'neutral'


data_set = pd.read_stata("data/ebay2_indegrees_comments.dta", chunksize=10,
                         columns=['FeedbackID', 'FeedbackComment', 'FeedbackValue'])
for chunk in data_set:
    chunk['sentiment_textblob'] = chunk.apply(lambda x: sentiment_de(x['FeedbackComment']), axis=1)
    print(chunk)

