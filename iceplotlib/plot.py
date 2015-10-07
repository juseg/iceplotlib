""":mod:`iceplotlib.plot`

Provide the actual plotting interface.
"""

from matplotlib.pyplot import *
from iceplotlib.axes import MapAxes
from iceplotlib.figure import GridFigure, SimpleFigure, DoubleInlineFigure


# file open function

def load(filename):
    from iceplotlib.io import IceDataset
    return IceDataset(filename)


# figure functions

def gridfigure(mapsize, nrows_ncols, **kwargs):
    """Create a new figure and return an :class:iceplotlib.figure.GridFigure instance"""
    return figure(FigureClass=GridFigure,
      mapsize=mapsize, nrows_ncols=nrows_ncols, **kwargs)

def simplefigure(mapsize, **kwargs):
    """Create a new figure and return a :class:iceplotlib.figure.SimpleFigure instance"""
    return figure(FigureClass=SimpleFigure,
      mapsize=mapsize, **kwargs)

def doubleinlinefigure(mapsize, **kwargs):
    """Create a new figure and return a :class:iceplotlib.figure.DoubleInlineFigure instance"""
    return figure(FigureClass=DoubleInlineFigure,
      mapsize=mapsize, **kwargs)


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
