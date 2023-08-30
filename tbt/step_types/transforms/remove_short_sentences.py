from tbt.meta_types.transform import Transform


class RemoveShortSentences(Transform):
    input_type = list
    output_type = list

    def transform(self, value):
        return [sentence for sentence in value if len(sentence) > self.min_chars]
