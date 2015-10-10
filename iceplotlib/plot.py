""":mod:`iceplotlib.plot`

Provide the actual plotting interface.
"""

import glob
from matplotlib.pyplot import *
from iceplotlib.axes import MapAxes
from iceplotlib.io import IceDataset, MFIceDataset


# file open function

def load(filename, **kwargs):

    # look for matching files
    # this allows even single files to be matched
    filelist = glob.glob(filename)

    # raise an error if no file was found
    if len(filelist) == 0:
        raise RuntimeError('could not load %s' % filename)

    # open a single file as single file dataset
    elif len(filelist) == 1:
        return IceDataset(filelist[0], **kwargs)

    # open multiple files as multiple file dataset
    else:
        return MFIceDataset(filename, **kwargs)


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
