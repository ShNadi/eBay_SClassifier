import re
from nltk.corpus import wordnet
import language_check
from tqdm import tqdm


# remove repeated characters
class RepeatReplacer(object):
    def __init__(self):
        self.repeat_regexp = re.compile(r'(\w*)(\w)\2(\w*)')
        self.repl = r'\1\2\3'

    def repeat(self, word):
        if wordnet.synsets(word):
            return word
        repl_word = self.repeat_regexp.sub(self.repl, word)

        if repl_word != word:
            return self.repeat(repl_word)
        else:
            return repl_word


# replacer = RepeatReplacer()
# print(replacer.replace('looove'))


# expanding contractions
replacement_patterns = [
 (r'won\'t', 'will not'),
 (r'can\'t', 'cannot'),
 (r'i\'m', 'i am'),
 (r'ain\'t', 'is not'),
 (r'(\w+)\'ll', '\g<1> will'),
 (r'(\w+)n\'t', '\g<1> not'),
 (r'(\w+)\'ve', '\g<1> have'),
 (r'(\w+)\'s', '\g<1> is'),
 (r'(\w+)\'re', '\g<1> are'),
 (r'(\w+)\'d', '\g<1> would')
]


class RegexpReplacer(object):
    def __init__(self, patterns=replacement_patterns):
        self.patterns = [(re.compile(regex), repl) for (regex, repl) in patterns]

    def replace(self, text):
        s = text
        for (pattern, repl) in self.patterns:
            s = re.sub(pattern, repl, s)
        return s


# replacer = RegexpReplacer()
# print(replacer.replace("can't is a contraction"))

#
# def spell_correction(dataFrame, language="nl"):
#     """Spell correction for the selected language.
#     :param X: Matrix of raw documents
#     :type X: list
#     :param language: Language of text
#     :type language: str
#     :return: Spell-corrected data
#     :rtype: list
#     """
#     tool = language_check.LanguageTool(language)
#     print("Spell correction: ")
#     for i in tqdm(range(dataFrame.__len__())):
#         matches = tool.check(dataFrame[i].content)
#         dataFrame[i].content = language_check.correct(dataFrame[i].content, matches)
#
#     return dataFrame
#
#
# txt = ['this is wong']
# t = spell_correction(txt)
# print()
