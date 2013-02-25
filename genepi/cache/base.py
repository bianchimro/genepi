class BaseCache(object):
    """Base cache class. Cannot be used directly. All methods must be implemented."""

    def initialize(self):
        raise NotImplementedError()
        
    def get_score(self, hash):
        raise NotImplementedError()
        
    def set_score(self, hash, value):
        raise NotImplementedError()


class NoCache((BaseCache):
    """Implements the cache interface without doing nothing"""

    def initialize(self):
        pass
        
    def get_score(self, hash):
        return None
        
    def set_score(self, hash, value):
        pass
        
        
class DictCache(BaseCache):
    """Simple Dictionary cache"""
    def initialize(self):
        self.data = {}
        
    def get_score(self, hash):
        return self.data.get(hash, None)
        
    def set_score(self, hash, value):
        self.data[hash] = value