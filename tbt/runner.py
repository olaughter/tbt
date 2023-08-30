import logging

from tbt.definitions.definition_parser import Pipelines
from tbt.loader import Loader


class Runner:
    def __init__(self, pipelines: Pipelines) -> None:
        self.pipelines = pipelines

    def prep(self):
        self.instantiate_steps()
        self.run_pre_steps()

    def run(self):
        self.instantiate_steps()
        self.run_pre_steps()
        self.run_steps()
        self.run_post_steps()

    def instantiate_steps(self):
        """Initialise all step classes

        Runs for all steps referenced in each pipeline using the kwargs
        from that definition. Stores instantiated steps in the pipeline object.
        """
        for _, pipeline in self.pipelines.items():
            for step_def in pipeline.step_defs:
                step_cls = Loader(step_def.meta_type).step(step_def.name)
                pipeline.instantiated_steps.append(step_cls(**step_def.kwargs))

    def run_pre_steps(self):
        """Run all pre_steps across all pipelines"""
        for label, pipeline in self.pipelines.items():
            logging.info(f"Running pre-steps for pipeline: '{label}'")
            for step in pipeline.instantiated_steps:
                logging.debug(f"Running pre-step: {step.name}")
                step.pre_step()

    def run_steps(self):
        """Run all steps across all pipelines"""
        for label, pipeline in self.pipelines.items():
            logging.info(f"Running steps for pipeline: '{label}'")
            value = None
            for step in pipeline.instantiated_steps:
                logging.debug(f"Running step: {step.name}")
                value = step.run(value)

    def run_post_steps(self):
        """Run all post_steps across all pipelines"""
        for label, pipeline in self.pipelines.items():
            logging.info(f"Running post-steps for pipeline: '{label}'")
            for step in pipeline.instantiated_steps:
                logging.debug(f"Running post-step: {step.name}")
                step.post_step()
