from .tictoc import *

__doc__ = tictoc.__doc__
if hasattr(tictoc, "__all__"):
    __all__ = tictoc.__all__

t = tictoc.init();
tic = t.tic;
toc = t.toc;
