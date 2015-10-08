""":mod:`iceplotlib.plot`

Provide the actual plotting interface.
"""

from matplotlib.pyplot import *
from iceplotlib.axes import MapAxes


# file open function

def load(filename):
    from iceplotlib.io import IceDataset
    return IceDataset(filename)


# import all plotting methods locally defined in MapAxes as functions

def _import_mapaxes_method(name):
    def func(*args, **kwargs):
        ax = gca()
        return getattr(ax, name)(*args, **kwargs)
    func.__doc__ = getattr(MapAxes, name).__doc__
    globals()[name] = func

for name, attr in MapAxes.__dict__.iteritems():
    if callable(attr) and not name.startswith("__"):
        _import_mapaxes_method(name)
