from pprint import pprint

from tbt.meta_types.destination import Destination


class ToStdout(Destination):
    """Write a value to stdout"""
    input_type = str
    output_type = str

    def run(self, value):
        pprint(value)
        return value
