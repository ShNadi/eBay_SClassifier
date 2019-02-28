from textblob_de import TextBlobDE
import pandas as pd
from textblob_de import TextBlobDE as TextBlobDE
from googletrans import Translator
import pydeepl


pd.set_option('display.expand_frame_repr', False)


def deepl_translate(text):
    translation = pydeepl.translate(text, 'DE', from_lang='EN')
    print(translation)


# translate German text to English by google translate
def google_translate_de(text):
    translator = Translator(text)
    txt = translator.translate(text, 'en')
    return txt.text


def translate_de(text):
    blob = TextBlobDE(text)
    if blob.detect_language() == "en":
        blob_en = blob
    else:
        blob_en = blob.translate(to="en")
    return blob_en.string

dd = pd.read_stata('data/sentiment1')


# # read DataSet
# d1 = pd.read_stata("data/sentiment2.dta")
# d1['FeedbackComment_en'] = d1.apply(lambda y: translate_de(y['PFeedbackComment']), axis=1)
# OutPath = 'data/english2.dta'
# d1.to_stata(OutPath)
# # d1 = pd.read_stata("data/english.dta")
# # print(d1)
#

# for chunk in data_set:
#     # chunk['FeedbackComment_en'] = chunk.apply(lambda y: translate_de(y['FeedbackComment']), axis=1)
#     chunk['FeedbackComment_en'] = chunk.apply(lambda y: google_translate_de(y['FeedbackComment']), axis=1)
#     # out_file = "C:\Github\eBay_SClassifier\eBay_SClassifier\data\english" + "/data_{}.dta".format(i)
#     # chunk.to_stata(outfile)
#
#     print(chunk)
# # outfile = 'data/en.dta'
# # data_set.to_stata(outfile)
#
#
