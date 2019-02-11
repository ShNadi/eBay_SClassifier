import pandas as pd
import pickle


# load stata dataset into memory
c_size = 1000000
reader = pd.read_stata("data/ebay2_indegrees_comments.dta", 'r', columns=['FeedbackID', 'FeedbackComment', 'FeedbackStatus'], chunksize=c_size)
print(reader.shape)

# i = 1
# for chunk in reader:
#     out_file = "C:\Github\eBay_SClassifier\eBay_SClassifier\chunk" + "/data_{}.csv".format(i)
#     chunk.to_csv(out_file, chu, columns=['FeedbackID', 'FeedbackComment', 'FeedbackStatus'])
#     i = i + 1
#     # out_file = "C:\Github\eBay_SClassifier\eBay_SClassifier\chunk" + "/data_{}.csv".format(i)
#     # with open(out_file, "wb") as f:
#     #     pickle.dump(chunk, f, pickle.HIGHEST_PROTOCOL)
#     # i = i + 1



