import nltk
from nltk.tokenize import sent_tokenize

from tbt.meta_types.transform import Transform


class SplitSentences(Transform):
    input_type = str
    output_type = list

    def pre_step(self):
        nltk.download("punkt", quiet=True)

    def transform(self, value):
        sentences = sent_tokenize(value)
        return sentences
