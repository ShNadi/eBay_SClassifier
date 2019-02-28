import pandas as pd
import de_preprocessing

# show all the DataFrame columns
pd.set_option('display.expand_frame_repr', False)


# read stat data set chunks into memory
data_set = pd.read_stata("data/ebay2_indegrees_comments.dta", chunksize=100,
                         columns=['FeedbackID', 'FeedbackComment', 'FeedbackValue'])
i = 1
df_final = pd.DataFrame()
for chunk in data_set:

    if i < 2:
        # corpus = de_preprocessing.clean(chunk)
        preprocessed_corpus = de_preprocessing.pre_process(chunk)
        # print(chunk)
        df_final = pd.concat([df_final, chunk])
        i = i + 1
        print()
    outfile = 'data/preprocessed.dta'
    df_final.to_stata(outfile)

# d = pd.read_stata('data/preprocessed.dta')
# print(d)



