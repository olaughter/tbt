import os

from tbt.meta_types.source import Source


class FromFile(Source):
    """Read from a file"""

    input_type = None
    output_type = str

    def pre_step(self):
        self.full_path = os.path.abspath(os.path.join(self.root_dir, self.path))
        assert os.path.exists(self.full_path), f"File not found: {self.full_path}"

    def run(self, value):
        with open(self.full_path) as f:
            content = f.read()
        return content
