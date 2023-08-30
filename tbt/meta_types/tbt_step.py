from abc import ABC, abstractmethod

from tbt.utils import camel_to_snake


class tbtStep(ABC):
    @classmethod
    @property
    def ref(cls):
        return camel_to_snake(cls.__name__)

    @classmethod
    @property
    def name(cls):
        return cls.__name__

    @property
    @abstractmethod
    def input_type(self):
        pass

    @property
    @abstractmethod
    def output_type(self):
        pass

    def __init__(self, **kwargs) -> None:
        """Not intended to be overridden, use pre_step() instead"""
        for k in kwargs:
            setattr(self, k, kwargs[k])

    @abstractmethod
    def pre_step(self):
        """Override with validations, setup, or any other pre-step actions

        Runs at the start of the pipeline before any other step runs.

        This could include downloading extra dependencies, confirming
        a file exists, or checking environment requirements.
        """
        pass

    @abstractmethod
    def run(self, value):
        """Override with the main logic of the step

        Should take and return a value
        """
        return value

    @abstractmethod
    def post_step(self):
        """Override with cleanup, or any other post-step actions

        Runs at the end of the pipeline after every step has run.

        This could include additional validation, cleaning up temporary
        files, or closing an external connection.
        """
        pass
