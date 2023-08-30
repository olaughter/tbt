from tbt.meta_types.transform import Transform

class CountUniqueList(Transform):
    input_type = list
    output_type = int

    def transform(self, value):
        return len(set(value))
