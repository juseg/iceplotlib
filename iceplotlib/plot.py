""":mod:`iceplotlib.plot`

Provide the actual plotting interface.
"""

import glob
import matplotlib.figure as mfig
from matplotlib.pyplot import *
from iceplotlib.io import IceDataset, MFIceDataset


# Custom figure class
# -------------------

class IceFigure(mfig.Figure):
    """Custom figure class allowing absolute subplot dimensioning."""

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
        gridspec_kw = dict(left=left/figw, right=1-right/figw,
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


# figure creation functions

def subplots_inches(nrows=1, ncols=1, figsize=None,
                    left=None, bottom=None, right=None, top=None,
                    wspace=None, hspace=None, width_ratios=None,
                    height_ratios=None, projection=None, **kwargs):
    from matplotlib.pyplot import rcParams, subplots

    # get figure dimensions from rc params if missing
    figw, figh = figsize or rcParams['figure.figsize']

    # normalize inner spacing to axes dimensions
    if wspace is not None and wspace != 0.0:
        wspace = (((figw-left-right)/wspace+1)/ncols-1)**(-1)
    if hspace is not None and hspace != 0.0:
        hspace = (((figh-bottom-top)/hspace+1)/nrows-1)**(-1)

    # normalize outer margins to figure dimensions
    if left is not None:
        left = left/figw
    if right is not None:
        right = 1-right/figw
    if bottom is not None:
        bottom = bottom/figh
    if top is not None:
        top = 1-top/figh

    # pass projection argument to subplot keywords
    subplot_kw = kwargs.pop('subplot_kw', {})
    if projection is not None:
        subplot_kw['projection'] = projection

    # return figure and subplot grid
    return subplots(nrows=nrows, ncols=ncols, figsize=figsize,
                    gridspec_kw={'left': left, 'right': right,
                                 'bottom': bottom, 'top': top,
                                 'wspace': wspace, 'hspace': hspace,
                                 'width_ratios': width_ratios,
                                 'height_ratios': height_ratios},
                    subplot_kw=subplot_kw, **kwargs)


def subplots_mm(nrows=1, ncols=1, figsize=None,
                left=None, bottom=None, right=None, top=None,
                wspace=None, hspace=None, width_ratios=None,
                height_ratios=None, projection=None, **kwargs):

    # convert all non null arguments in inches
    mm = 1/25.4
    if figsize is not None:
        figw, figh = figsize
        figsize = (figw*mm, figh*mm)
    if left is not None:
        left*=mm
    if right is not None:
        right*=mm
    if bottom is not None:
        bottom=bottom*mm
    if top is not None:
        top=top*mm
    if wspace is not None:
        wspace=wspace*mm
    if hspace is not None:
        hspace=hspace*mm

    # use inches helper to align subplots
    return subplots_inches(nrows=nrows, ncols=ncols, figsize=figsize,
                           left=left, right=right, bottom=bottom, top=top,
                           wspace=wspace, hspace=hspace,
                           width_ratios=width_ratios,
                           height_ratios=height_ratios,
                           projection=projection, **kwargs)


# import all plotting methods locally defined in IceDataset as functions

def _import_icedataset_method(name):
    def func(nc, *args, **kwargs):
        return getattr(nc, name)(*args, **kwargs)
    func.__doc__ = getattr(IceDataset, name).__doc__
    globals()[name] = func

for name, attr in IceDataset.__dict__.iteritems():
    if callable(attr) and not name.startswith("__"):
        _import_icedataset_method(name)
