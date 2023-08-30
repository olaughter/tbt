from tbt.meta_types.transform import Transform


class SplitWords(Transform):
    input_type = str
    output_type = list

    def transform(self, value):
        return value.split()
