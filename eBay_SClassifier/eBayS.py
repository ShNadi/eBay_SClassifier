import SentimentClass
from sklearn.metrics import confusion_matrix
import pandas as pd
import string
import numpy as np
from pandas_ml import ConfusionMatrix


# Read German DataSet
data_set = pd.read_stata("data/preprocessed.dta", columns=['FeedbackID', 'FeedbackComment', 'FeedbackValue',
                                                           'PFeedbackComment'])
def senti_eBay(data_set):
    # ***************** Pre-processing *********************************************************************
    # Do Preprocess
    text = data_set['FeedbackComment']
    # change FeedbackValue field to some meaningful values. 1 -> negative,  2 -> positive, 8-> neutral
    data_set.FeedbackValue.replace([1, 2, 8], ['negative', 'positive', 'neutral'], inplace=True)
    print("FeedbackValue column is updated!")

    proc = SentimentClass.PreProcess()
    data_set['FeedbackComment_CorrectSelling']= proc.check_spell()

    # Remove punctuations
    data_set['FeedbackComment_without_punctuations'] = data_set['FeedbackComment_CorrectSelling'].apply(
        lambda x: ''.join([i for i in x
                           if i not in string.punctuation]))
    print("punctuations are removed")

    # convert all characters to lowercase
    data_set['FeedbackComment_lowercase'] = data_set['FeedbackComment_without_punctuations'].str.lower()
    print("turned to lowercase")

    data_set['PFeedbackComment'] = data_set['FeedbackComment_lowercase']

    # ***************** German Sentiment *******************************************************************
    # Do sentiment analysis for German Text
    text = data_set['PFeedbackComment']
    # sentiment_de is an object from SentimentLexDe class
    sentiment_de = SentimentClass.SentimentLexDe(text)
    # Calculate sentiment using textblob_de
    data_set['textblobde_score'], data_set['textblobde_category'] = sentiment_de.sentiment_textblobde()
    # Calculate sentiment using polyglot
    data_set['polyglot_score'], data_set['polyglot_category'] = sentiment_de.sentiment_polyglot()

    # ****************** Translate to English **************************************************************
    text = data_set['PFeedbackComment']
    # translate Deutsch to English
    translate = SentimentClass.TranslateEn(text)
    data_set['FeedbackComment_en'] = translate.google_translate_de()
    # data_set['FeedbackComment_en'] = data_set.apply(lambda y: translate.translate_de(), axis=1)
    text_en = data_set['FeedbackComment_en']

    # ****************** English Sentiment ******************************************************************
    sentiment_en = SentimentClass.SentimentLexEn(text_en)
    # Calculate sentiment using Afinn lexicon on translated text
    data_set['afinn_scores'], data_set['afinn_category'] = sentiment_en.sentiment_afinn()
    # Calculate sentiment using textblob on translated text
    data_set['textblob_scores'], data_set['textblob_category'] = sentiment_en.sentiment_textblob()

    # ******************* Write Data_set ********************************************************************
    outfile = 'data/sentiment2.dta'
    data_set.to_stata(outfile)

    # ******************* Plot Confiusion Matrix ************************************************************
    conf = confusion_matrix(data_set['FeedbackValue'], data_set['textblobde_category'])
    print('Confusion Matrix:\n',conf)
    c = SentimentClass.Plot_sentiment()
    c.plot_confusion_matrix(cm=conf, normalize=False, target_names=['negative', 'neutral', 'positive'], cmap='PuBuGn')

    conf = confusion_matrix(data_set['FeedbackValue'], r['polyglot_category'])
    print('Confusion Matrix:\n', conf)
    c = SentimentClass.Plot_sentiment()
    c.plot_confusion_matrix(cm=conf, normalize=False, target_names=['negative', 'neutral', 'positive'], cmap='Bupu')

    conf = confusion_matrix(data_set['FeedbackValue'], data_set['afinn_category'])
    print('Confusion Matrix:\n', conf)
    c = SentimentClass.Plot_sentiment()
    c.plot_confusion_matrix(cm=conf, normalize=False, target_names=['negative', 'neutral', 'positive'], cmap='GnBu')

    conf = confusion_matrix(data_set['FeedbackValue'], data_set['textblob_category'])
    print('Confusion Matrix:\n', conf)
    c = SentimentClass.Plot_sentiment()
    c.plot_confusion_matrix(cm=conf, normalize=False, target_names=['negative', 'neutral', 'positive'], cmap='Purples')


#
# data_set = pd.read_stata('data/eng.dta', columns=['FeedbackID', 'FeedbackValue', 'PFeedbackComment', 'textblobde_score',
#                                                   'textblobde_category', 'polyglot_score', 'polyglot_category',
#                                                   'FeedbackComment_en'])
# print(data_set)
# text = data_set['PFeedbackComment']
# # translate Deutsch to English
# translate = SentimentClass.TranslateEn(text)
# data_set['FeedbackComment_en'] = translate.google_translate_de()
# # data_set['FeedbackComment_en'] = data_set.apply(lambda y: translate.translate_de(), axis=1)
# text_en = data_set['FeedbackComment_en']
# print(data_set)
#
#
# sentiment_en = SentimentClass.SentimentLexEn(text_en)
# # Calculate sentiment using Afinn lexicon on translated text
# data_set['afinn_scores'], data_set['afinn_category'] = sentiment_en.sentiment_afinn()
# # Calculate sentiment using textblob on translated text
# data_set['textblob_scores'], data_set['textblob_category'] = sentiment_en.sentiment_textblob()
#
# outfile = 'data/sentiment2.dta'
# data_set.to_stata(outfile)
#
#
# r = pd.read_stata('data/sentiment2.dta')
# print(r)
# # conf_matrix1 = ConfusionMatrix(r['FeedbackValue'], r['textblobde_category'])
# # conf = confusion_matrix(r['FeedbackValue'], r['textblobde_category'])
# conf = confusion_matrix(r['FeedbackValue'], r['textblob_category'])
# print(conf)
# c = SentimentClass.Plot_sentiment()
#
#
# c.plot_confusion_matrix(cm= conf, normalize=False, target_names=['negative', 'neutral', 'positive'], cmap='PuBuGn')
#
# def sentiment_eBay(data_set, language = 'de', preprocess = False, translate = False, sentiment = True, plot = False):
#     if language== 'de':
#
#         if preprocess == 'True':
#             text = data_set['FeedbackComment']
#             # call pre_processing
#
#             outfile = 'data/preprocessed.dta'
#             data_set.to_stata(outfile)
#
#         text = data_set['PFeedbackComment']
#
#         if translate == 'True':
#             translate = SentimentClass.TranslateEn(text)
#             data_set['FeedbackComment_en'] = translate.google_translate_de()
#
#         if sentiment == True:
#             text = data_set['PFeedbackComment']
#             sentiment_de = SentimentClass.SentimentLexDe(text)
#             # Calculate sentiment using textblob_de
#             data_set['textblobde_score'], data_set['textblobde_category'] = sentiment_de.sentiment_textblobde()
#             # Calculate sentiment using polyglot
#             data_set['polyglot_score'], data_set['polyglot_category'] = sentiment_de.sentiment_polyglot()
#             outfile = 'data/sentiment2.dta'
#             data_set.to_stata(outfile)
#         if plot==True:
#             pass
#
#     elif language=='en':
#         text_en = data_set['FeedbackComment_en']
#         if translate == 'True':
#             print('The text is already written in English')
#         if preprocess == 'True':
#             print('Preprocessing is only defined for German text.')
#         if sentiment == True:
#             sentiment_en = SentimentClass.SentimentLexEn(text_en)
#             # Calculate sentiment using Afinn lexicon on translated text
#             data_set['afinn_scores'], data_set['afinn_category'] = sentiment_en.sentiment_afinn()
#             # Calculate sentiment using textblob on translated text
#             data_set['textblob_scores'], data_set['textblob_category'] = sentiment_en.sentiment_textblob()
#             outfile = 'data/sentiment2.dta'
#             data_set.to_stata(outfile)
#         if plot == True:
#             pass
#
#
#     else:
#         print("This language is not supported by this code.")
