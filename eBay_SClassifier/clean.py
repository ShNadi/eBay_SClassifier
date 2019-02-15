import pandas as pd


pd.set_option('display.expand_frame_repr', False)

read = pd .read_stata("data/ebay2_indegrees_comments.dta", chunksize=100, columns=['FeedbackID', 'FeedbackComment', 'FeedbackStatus'])
for row in read:
    # show the size of chunks and whole dataSet
    print(row.shape)
    # Show the name of columns in dataSet
    print(row.columns.tolist())
    # remove lines without comments
    removed_no_comment = row[row['FeedbackComment'] != "no comment"]
    print(removed_no_comment.shape)
    # change FeedbackStatus field to some meaningful values. 0 -> negative,  1 -> positive, 9-> neutral
    print(row.FeedbackStatus.unique())
    row.loc[row.FeedbackStatus == 0, 'FeedbackStatus'] = "negative"
    row.loc[row.FeedbackStatus == 1, 'FeedbackStatus'] = "positive"
    row.loc[row.FeedbackStatus == 9, 'FeedbackStatus'] = "neutral"
    print(row.FeedbackStatus.unique())
    print(row)

