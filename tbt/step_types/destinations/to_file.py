import logging
from tempfile import NamedTemporaryFile
import os

from tbt.meta_types.destination import Destination


class ToFile(Destination):
    """Write a value to a file"""
    input_type = str
    output_type = str

    def pre_step(self):
        """Sets the full path variable and tests it is writable"""
        self.full_path = os.path.join(self.root_dir, self.path)
        out_dir, out_file_name = os.path.split(self.full_path)
        with NamedTemporaryFile("w", dir=out_dir, suffix=out_file_name) as f:
            f.write("")

    def run(self, value):
        """Write the value to the file
        
        Also returns value for other uses"""
        with open(self.full_path, "w") as f:
            f.write(f"{value}")
        logging.info(f"Wrote to {self.full_path}")
        return value
