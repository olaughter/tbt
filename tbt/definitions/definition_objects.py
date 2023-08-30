import os
from dataclasses import dataclass


@dataclass
class Definition:
    """Represents a tbt*.yaml file, defining pipelines"""

    root: str
    file_name: str

    @property
    def path(self):
        """Path to the tbt*.yaml file"""
        return os.path.join(self.root, self.file_name)


class Pipeline:
    """Represents a single pipeline, as defined in a tbt*.yaml file"""

    def __init__(self, label, definition, **kwargs):
        self.label = label
        self.definition = definition
        self.instantiated_steps = []
        self.depends_on = kwargs.get("depends_on")

        self._step_defs = []
        for step_def in kwargs.get("steps"):
            step = Step(step_def=step_def, root_dir=self.definition.root)
            self._step_defs.append(step)

    @property
    def step_defs(self) -> list["Step"]:
        """The step definitions for this pipeline"""
        return self._step_defs


# Type alias for pipeline lookup table
Pipelines = dict[str, Pipeline]


class Step:
    """Represents a single step, as defined within a pipeline within a tbt*.yaml file"""

    def __init__(self, step_def: dict, root_dir: str):
        self._meta_type = self.parse_step_meta_type(step_def)
        self._name = step_def[self.meta_type].get("type")
        self._kwargs = step_def[self.meta_type]
        self._kwargs["root_dir"] = root_dir

    def parse_step_meta_type(self, step_def: dict[str, dict]) -> str:
        """Parse the step meta type from the definition"""
        return list(step_def.keys())[0]

    @property
    def meta_type(self):
        return self._meta_type

    @property
    def name(self):
        return self._name

    @property
    def kwargs(self):
        return self._kwargs
