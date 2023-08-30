import logging

import pytest

from tbt.definitions.definition_objects import Definition, Pipeline, Pipelines
from tbt.meta_types.transform import Transform


@pytest.fixture
def simple_steps():
    return [
        {"source": {"type": "from_file", "path": "data/frankenstein_prologue.txt"}},
        {"transform": {"type": "split_sentences"}},
        {"destination": {"type": "to_stdout"}},
    ]


@pytest.fixture
def valid_pipelines(simple_steps) -> Pipelines:
    pipelines = {
        "one": Pipeline(
            label="one",
            definition=Definition(None, None),
            **{
                "depends_on": ["two"],
                "steps": simple_steps,
            },
        ),
        "two": Pipeline(
            label="two",
            definition=Definition(None, None),
            **{
                "steps": simple_steps,
            },
        ),
    }
    return pipelines


@pytest.fixture
def invalid_pipelines(simple_steps) -> Pipelines:
    pipelines = {
        "one": Pipeline(
            label="one",
            definition=Definition("", ""),
            **{
                "depends_on": ["two"],
                "steps": simple_steps,
            },
        ),
        "two": Pipeline(
            label="two",
            definition=Definition("", ""),
            **{
                "depends_on": ["one"],
                "steps": simple_steps,
            },
        ),
    }
    return pipelines


@pytest.fixture
def spy_pipelines():
    pipelines = {
        "one": Pipeline(
            label="one",
            definition=Definition("", ""),
            **{
                "steps": [{"transform": {"type": "spy_step"}}],
            },
        ),
    }
    return pipelines


class SpyStep(Transform):
    input_type = None
    output_type = None

    def transform(self, value):
        return None

    def __init__(self, **kwargs) -> None:
        logging.info("ran __init__")
        super().__init__(**kwargs)

    def pre_step(self):
        logging.info("ran pre_step")

    def run(self, value):
        logging.info("ran run")

    def post_step(self):
        logging.info("ran post_step")
