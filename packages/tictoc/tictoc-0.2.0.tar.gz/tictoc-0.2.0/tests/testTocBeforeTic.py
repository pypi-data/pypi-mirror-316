import pytest
import tictoc

def testTocBeforeTic():
    with pytest.raises(Exception):
        t = tictoc.init()
        t.toc()
