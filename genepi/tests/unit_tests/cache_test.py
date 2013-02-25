import unittest
from nose.tools import assert_raises, raises
from genepi.cache.base import BaseCache, NoCache, DictCache

class CacheTest(unittest.TestCase):

    def setUp(self):
        pass
        
        
    def tearDown(self):
        pass
        
    
    def test_base_cache(self):
        c = BaseCache()
        assert_raises(NotImplementedError, c.initialize)
        assert_raises(NotImplementedError, c.get_score, "abc")
        assert_raises(NotImplementedError, c.set_score, "abc", 12)
        

    def test_no_cache(self):
        c = NoCache()
        c.initialize()
        v = c.get_score("abc")
        assert v is None
        c.set_score("ss",12)
        v = c.get_score("ss")
        assert v is None
        
        
    def test_dict_cache(self):
        c = DictCache()
        c.initialize()
        v = c.get_score("abc")
        assert v is None
        c.set_score("ss",12)
        v = c.get_score("ss")
        assert v is 12
        

        
