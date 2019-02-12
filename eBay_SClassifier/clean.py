import pandas as pd

#
# r = pd.read_stata("data/ebay2_indegrees_comments.dta", chunksize=1000000, columns=['FeedbackComment'])
# i = 0
# for row in r:
#     c = row[row['FeedbackComment'] != "no comment"]
#     print(c.shape)
#

read = pd .read_stata("data/ebay2_indegrees_comments.dta", chunksize=10000)
for row in read:
    # show the size of chunks and whole dataSet
    print(row.shape)
    # Show the name of columns in dataSet
    print(row.columns.tolist())
    # remove lines without comments
    removed_no_comment = row[row['FeedbackComment'] != "no comment"]
    print(removed_no_comment.shape)
    # change FeedbackStatus field to some meaningful values. 0 -> negative,  1 -> positive, 9-> neutral
