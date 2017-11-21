""":mod:`iceplotlib.plot`

Provide the actual plotting interface.
"""

import glob
import matplotlib.pyplot as plt
import matplotlib.figure as mfig
from matplotlib.pyplot import *
from iceplotlib.io import IceDataset, MFIceDataset


# Custom figure class
# -------------------

class IceFigure(mfig.Figure):
    """Custom figure class allowing absolute subplot dimensioning."""

    def get_size_mm():
        """Returns the current size of the figure in mm as an numpy array."""
        return fig.get_size_inches()*25.4

    def subplots_inches(self, nrows=1, ncols=1, gridspec_kw=None, **kw):
        """Create subplots with dimensions in inches."""

        # get figure dimensions in inches
        figw, figh = self.get_size_inches()

        # get default gridspec params
        if gridspec_kw is None:
            gridspec_kw = {}
        left = gridspec_kw.pop('left', self.subplotpars.left)
        right = gridspec_kw.pop('right', self.subplotpars.right)
        bottom = gridspec_kw.pop('bottom', self.subplotpars.bottom)
        top = gridspec_kw.pop('top', self.subplotpars.top)
        wspace = gridspec_kw.pop('wspace', self.subplotpars.wspace)
        hspace = gridspec_kw.pop('hspace', self.subplotpars.hspace)

        # normalize inner spacing to axes dimensions
        if wspace != 0.0:
            wspace = (((figw-left-right)/wspace+1)/ncols-1)**(-1)
        if hspace != 0.0:
            hspace = (((figh-bottom-top)/hspace+1)/nrows-1)**(-1)

        # normalize outer margins to figure dimensions
        gridspec_kw.update(left=left/figw, right=1-right/figw,
                           bottom=bottom/figh, top=1-top/figh,
                           wspace=wspace, hspace=hspace)

        # create subplots
        return mfig.Figure.subplots(self, nrows=nrows, ncols=ncols,
                                    gridspec_kw=gridspec_kw, **kw)

    def subplots_mm(self, gridspec_kw=None, **kw):
        """Create subplots with dimensions in mm."""

        # convert all non null arguments to inches
        mm = 1/25.4
        if gridspec_kw is not None:
            for dim in ['left', 'right', 'bottom', 'top', 'wspace', 'hspace']:
                if dim in gridspec_kw:
                    gridspec_kw[dim] *= mm

        # create subplots
        return self.subplots_inches(gridspec_kw=gridspec_kw, **kw)


# File open function
# ------------------

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


# Figure helper functions
# -----------------------

def figure(**kw):
    """Create a new figure with dimensions in inches."""

    # by default select custom figure class
    FigureClass = kw.pop('FigureClass', IceFigure)

    # create new figure
    fig = plt.figure(FigureClass=FigureClass, **kw)
    return fig


def figure_mm(figsize=None, **kw):
    """Create a new figure with dimensions in mm."""

    # convert figure size to mm
    mm = 1/25.4
    if figsize is not None:
        figw, figh = figsize
        figsize = (figw*mm, figh*mm)

    # create new figure
    fig = figure(figsize=figsize, **kw)
    return fig


# Subplot helper functions
# ------------------------

def subplots(nrows=1, ncols=1, sharex=False, sharey=False, squeeze=True,
             subplot_kw=None, gridspec_kw=None, **fig_kw):
    """Same as matplotlib function but allow a projection argument."""

    # pass projection argument to subplot keywords
    if subplot_kw is None:
        subplot_kw = {}
    if projection is not None:
        subplot_kw['projection'] = projection

    # create new figure and axes
    fig = figure(**fig_kw)
    axs = fig.subplots(nrows=nrows, ncols=ncols, sharex=sharex, sharey=sharey,
                       squeeze=squeeze, subplot_kw=subplot_kw,
                       gridspec_kw=gridspec_kw)
    return fig, axs


def subplots_inches(nrows=1, ncols=1, sharex=False, sharey=False, squeeze=True,
                    subplot_kw=None, gridspec_kw=None, projection=None,
                    **fig_kw):
    """Create figure and subplots with dimensions in inches."""

    # pass projection argument to subplot keywords
    if subplot_kw is None:
        subplot_kw = {}
    if projection is not None:
        subplot_kw['projection'] = projection

    # create new figure and axes
    fig = figure(**fig_kw)
    axs = fig.subplots_inches(nrows=nrows, ncols=ncols, sharex=sharex,
                              sharey=sharey, squeeze=squeeze,
                              subplot_kw=subplot_kw, gridspec_kw=gridspec_kw)
    return fig, axs


def subplots_mm(nrows=1, ncols=1, sharex=False, sharey=False, squeeze=True,
                subplot_kw=None, gridspec_kw=None, projection=None, **fig_kw):
    """Create figure and subplots with dimensions in mm."""

    # pass projection argument to subplot keywords
    if subplot_kw is None:
        subplot_kw = {}
    if projection is not None:
        subplot_kw['projection'] = projection

    # create new figure and axes
    fig = figure_mm(**fig_kw)
    axs = fig.subplots_mm(nrows=nrows, ncols=ncols, sharex=sharex,
                          sharey=sharey, squeeze=squeeze,
                          subplot_kw=subplot_kw, gridspec_kw=gridspec_kw)
    return fig, axs


# Plotting functions
# ------------------

# import all plotting methods locally defined in IceDataset as functions

def _import_icedataset_method(name):
    def func(nc, *args, **kwargs):
        return getattr(nc, name)(*args, **kwargs)
    func.__doc__ = getattr(IceDataset, name).__doc__
    globals()[name] = func


for name, attr in IceDataset.__dict__.iteritems():
    if callable(attr) and not name.startswith("__"):
        _import_icedataset_method(name)
