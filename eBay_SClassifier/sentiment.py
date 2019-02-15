# from afinn import Afinn
#
#
# afinn = Afinn(language='da')
# print(afinn.score('Hvis ikke det er det mest afskyelige flueknepperi...'))


# from textblob import TextBlob
from textblob_de import TextBlobDE as TextBlob


statement = TextBlob("will nicht zahlen!.")
print(statement.sentiment)

# text1 = TextBlob("Today is a great day, but it is boring")
# text1.sentiment.polarity
#
# from textblob import TextBlob
# ### My input text is a column from a dataframe that contains tweets.
#
# def sentiment(x):
#     sentiment = TextBlob(x)
#     return sentiment.sentiment.polarity
#
# tweetsdf['sentiment'] = tweetsdf['processed_tweets'].apply(sentiment)
# tweetsdf['senti'][tweetsdf['sentiment']>0] = 'positive'
# tweetsdf['senti'][tweetsdf['sentiment']<0] = 'negative'
# tweetsdf['senti'][tweetsdf['sentiment']==0] = 'neutral'