import pandas as pd
import SentimentClass
from sklearn.metrics import confusion_matrix
import string
# import translate


pd.set_option('display.expand_frame_repr', False)



def sentiment(preprocess = False, sentiment_de = False, translate_to_en =False, sentiment_en = False, plot = False):
        # ***************** Pre-processing *********************************************************************
        if preprocess==True:
            # Read dataset
            data_set = pd.read_stata("test/sample.dta", columns=['FeedbackID', 'FeedbackComment', 'FeedbackValue'])

            # Change scores to the categorical values
            data_set['FeedbackValue_category'] = data_set.FeedbackValue
            data_set.FeedbackValue_category.replace([1, 2, 8], ['negative', 'positive', 'neutral'], inplace=True)

            # Replace punctuation with space
            text = data_set['FeedbackComment']
            X = SentimentClass.PreProcess(text)
            data_set['Feedback_RemovedPunctuations'] = X.remove_punctuation()

            # Decapitalize characters
            data_set['FeedbackComment_lowercase'] = data_set['Feedback_RemovedPunctuations'].str.lower()
            # Correct misspelled words
            t = data_set['FeedbackComment_lowercase']
            # t = data_set['Feedback_RemovedPunctuations']
            x = SentimentClass.PreProcess(t)
            df_chechspell = x.check()
            data_set = pd.concat([data_set, df_chechspell], axis=1)
            print(data_set)

            # out = 'test/preprocessed.dta'
            # data_set.to_stata(out)

        # ***************** German Sentiment *******************************************************************
        if sentiment_de == True:
            data_set = pd.read_stata("test/preprocessed.dta", columns=['FeedbackID', 'PFeedbackComment', 'FeedbackValue'])
            text = data_set['PFeedbackComment']
            # sentiment_de is an object from SentimentLexDe class
            sentiment_de = SentimentClass.SentimentLexDe(text)
            # Calculate sentiment using textblob_de
            data_set['textblobde_score'], data_set['textblobde_category'] = sentiment_de.sentiment_textblobde()
            # Calculate sentiment using polyglot
            data_set['polyglot_score'], data_set['polyglot_category'] = sentiment_de.sentiment_polyglot()
            print(data_set)
            outfile = 'test/sentiment_de.dta'
            data_set.to_stata(outfile)

        # ****************** Translate to English **************************************************************
        if translate_to_en ==True:
            data_set = pd.read_stata('test/sentiment_de.dta', columns=['FeedbackID', 'PFeedbackComment',
                                                                       'FeedbackValue', 'textblobde_score',
                                                                       'textblobde_category', 'polyglot_score',
                                                                       'polyglot_category'])
            data_set['FeedbackComment_en'] = data_set.apply(lambda y:translate.translate_de(y['PFeedbackComment']), axis=1)
            print(data_set)
            outfile = 'test/english.dta'
            data_set.to_stata(outfile)


        # ****************** English Sentiment ******************************************************************
        if sentiment_en == True:
            data_set = pd.read_stata("test/english.dta",columns=['FeedbackID', 'PFeedbackComment',
                                                                       'FeedbackValue', 'textblobde_score',
                                                                       'textblobde_category', 'polyglot_score',
                                                                       'polyglot_category', 'FeedbackComment_en'])
            text_en = data_set['FeedbackComment_en']
            sentiment_en = SentimentClass.SentimentLexEn(text_en)
            # Calculate sentiment using Afinn lexicon on translated text
            data_set['afinn_scores'], data_set['afinn_category'] = sentiment_en.sentiment_afinn()
            # Calculate sentiment using textblob on translated text
            data_set['textblob_scores'], data_set['textblob_category'] = sentiment_en.sentiment_textblob()
            print(data_set)
            outfile = 'test/sentiment_en.dta'
            data_set.to_stata(outfile)


        # ******************* Plot Confiusion Matrix ************************************************************
        if plot==True:
            data_set = pd.read_stata("test/sentiment_en.dta",columns=['FeedbackID', 'PFeedbackComment',
                                                                       'FeedbackValue', 'textblobde_score',
                                                                       'textblobde_category', 'polyglot_score',
                                                                       'polyglot_category', 'FeedbackComment_en',
                                                                      'afinn_scores', 'afinn_category',
                                                                      'textblob_scores', 'textblob_category'])
            conf1 = confusion_matrix(data_set['FeedbackValue'], data_set['textblobde_category'])
            print('Confusion Matrix:\n', conf1)
            c = SentimentClass.Plot_sentiment()
            c.plot_confusion_matrix('textblobde', cm=conf1, normalize=False, target_names=['negative', 'neutral', 'positive'],
                                    cmap='PuBuGn')

            conf2 = confusion_matrix(data_set['FeedbackValue'], data_set['polyglot_category'])
            print('Confusion Matrix:\n', conf2)
            c = SentimentClass.Plot_sentiment()
            c.plot_confusion_matrix('polyglot', cm=conf2, normalize=False, target_names=['negative', 'neutral', 'positive'],
                                    cmap='BuPu')

            conf3 = confusion_matrix(data_set['FeedbackValue'], data_set['afinn_category'])
            print('Confusion Matrix:\n', conf3)
            c = SentimentClass.Plot_sentiment()
            c.plot_confusion_matrix('afinn', cm=conf3, normalize=False, target_names=['negative', 'neutral', 'positive'],
                                    cmap='GnBu')

            conf4 = confusion_matrix(data_set['FeedbackValue'], data_set['textblob_category'])
            print('Confusion Matrix:\n', conf4)
            c = SentimentClass.Plot_sentiment()
            c.plot_confusion_matrix('textblob', cm=conf4, normalize=False, target_names=['negative', 'neutral', 'positive'],
                                    cmap='Purples')




sentiment(preprocess=True, sentiment_de=False, translate_to_en=False, sentiment_en=False, plot=False)
# data_set = pd.read_stata('data/sentiment2.dta')
# print(data_set)
