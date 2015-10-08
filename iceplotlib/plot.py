""":mod:`iceplotlib.plot`

Provide the actual plotting interface.
"""

from matplotlib.pyplot import *
from iceplotlib.axes import MapAxes


# file open function

def load(filename):
    from iceplotlib.io import IceDataset
    return IceDataset(filename)


# import plotting functions not defined in matplotlib.pyplot

def _import_mapaxes_method(name):
    def func(*args, **kwargs):
        ax = gca()
        return getattr(ax, name)(*args, **kwargs)
    func.__doc__ = getattr(MapAxes, name).__doc__
    globals()[name] = func

_import_mapaxes_method('icemargin')
_import_mapaxes_method('icemarginf')
_import_mapaxes_method('icemap')
_import_mapaxes_method('shading')
_import_mapaxes_method('streamplot')
