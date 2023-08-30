from typing import List
import types

from tbt.meta_types.tbt_step import tbtStep
from tbt.meta_types import *
from tbt.step_types.sources import *
from tbt.step_types.destinations import *
from tbt.step_types.transforms import *


class Loader:
    def __init__(self, meta_type: str) -> None:
        """gets the class for the given meta type on instantiation"""
        meta_type_options = self.load_available(tbtStep)
        if meta_type not in meta_type_options:
            raise ValueError(f"Unknown meta type {meta_type}, expected one of: {meta_type_options}")
        self.meta_type_cls = meta_type_options[meta_type]

    def load_available(self, tbt_step_cls: types.ModuleType) -> dict[str, type(tbtStep)]:
        """Builds a lookup table of all imported subclasses for the given module."""
        available_step_types = {}
        for cls in tbt_step_cls.__subclasses__():
            available_step_types[cls.ref] = cls
        return available_step_types

    def step(self, step):
        """gets the class for the given step definition"""
        available_steps = self.load_available(self.meta_type_cls)
        if step not in available_steps:
            raise ValueError(f"Unknown step type {step}, expected one of: {available_steps}")
        step_cls = available_steps[step]
        return step_cls


if __name__ == "__main__":
    step = Loader("source").step("from_file")
    step()
