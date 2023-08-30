from tbt.meta_types.destination import Destination
from tbt.meta_types.source import Source
from tbt.meta_types.transform import Transform
from tbt.step_types.destinations import *
from tbt.step_types.sources import *
from tbt.step_types.transforms import *


def test_source_types():
    for cls in Source.__subclasses__():
        cls()


def test_destination_types():
    for cls in Destination.__subclasses__():
        cls()


def test_transform_types():
    for cls in Transform.__subclasses__():
        cls()
