import pandas as pd


pd.set_option('display.expand_frame_repr', False)

read = pd .read_stata("data/ebay2_indegrees_comments.dta", chunksize=10, columns=['FeedbackComment', 'FeedbackValue'])


def clean(corpus):
    i = 1
    for row in corpus:
        if i < 2:
            # show the size of chunks and whole dataSet
            print("Size of DataSet:", row.shape)
            # Show the name of columns in dataSet
            print("column names: ", row.columns.tolist())
            # show the DataSet values
            print("DataSet values:\n", row)
            # remove lines without comments
            row.drop(row[row.FeedbackComment == 'no comment'].index, inplace=True)
            print(row.shape)
            # change FeedbackStatus field to some meaningful values. 1 -> negative,  2 -> positive, 8-> neutral
            print(row.FeedbackValue.unique())
            row.FeedbackValue.replace([1, 2, 8], ['negative', 'positive', 'neutral'], inplace=True)
            print(row.FeedbackValue.unique())
            print(row)
            i = i + 1
            return row


d = pd.DataFrame()
d = clean(read)
print(d)

