import pandas as pd
import de_preprocessing

# show all the DataFrame columns
pd.set_option('display.expand_frame_repr', False)


# read stat data set chunks into memory
data_set = pd.read_stata("data/ebay2_indegrees_comments.dta", chunksize=1000000,
                         columns=['FeedbackID', 'FeedbackComment', 'FeedbackValue'])
for chunk in data_set:
    # corpus = pd.DataFrame(chunk['FeedbackStatus'])
    corpus = de_preprocessing.cleanup_document(chunk)
    preprocessed_corpus = de_preprocessing.pre_process(corpus)







