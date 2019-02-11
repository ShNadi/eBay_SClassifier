import pandas as pd
import de_preprocessing

# show all the DataFrame columns
pd.set_option('display.expand_frame_repr', False)


# read stat data set chunks into memory
data_set = pd.read_stata("data/ebay2_indegrees_comments.dta", chunksize=1000000,
                         columns=['FeedbackID', 'FeedbackComment', 'FeedbackStatus'])
for chunk in data_set:
    corpus = pd.DataFrame(chunk['FeedbackStatus'])
    de_preprocessing.cleanup_doc(chunk)







