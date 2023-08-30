from abc import abstractmethod

from tbt.meta_types.tbt_step import tbtStep

class Source(tbtStep):
    @abstractmethod
    def run(self, value):
        pass

    def pre_step(self):
        pass
    
    def post_step(self):
        pass
