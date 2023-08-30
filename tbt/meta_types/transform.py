from abc import abstractmethod

from tbt.meta_types.tbt_step import tbtStep


class Transform(tbtStep):
    @property
    @abstractmethod
    def input_type(self):
        pass

    @property
    @abstractmethod
    def output_type(self):
        pass

    @abstractmethod
    def transform(self, value):
        pass

    def run(self, value):
        assert isinstance(
            value, self.input_type
        ), f"{self.name} expected input type {self.input_type}, got {type(value)}"
        result = self.transform(value)
        assert isinstance(
            result, self.output_type
        ), f"{self.name} expected output type {self.output_type}, got {type(result)}"
        return result

    def pre_step(self):
        pass

    def post_step(self):
        pass
