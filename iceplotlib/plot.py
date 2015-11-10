""":mod:`iceplotlib.plot`

Provide the actual plotting interface.
"""

import glob
from matplotlib.pyplot import *
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


# figure creation functions

def subplots_inches(nrows=1, ncols=1, figsize=None,
                    left=None, bottom=None, right=None, top=None,
                    wspace=None, hspace=None, projection=None, **kwargs):
    from matplotlib.pyplot import rcParams, subplots

    # get figure dimensions from rc params if missing
    figw, figh = figsize or rcParams['figure.figsize']

    # normalize inner spacing to axes dimensions
    if wspace is not None:
        wspace = (((figw-left-right)/wspace+1)/ncols-1)**(-1)
    if hspace is not None:
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
                                 'wspace': wspace, 'hspace': hspace},
                    subplot_kw=subplot_kw, **kwargs)


def subplots_mm(nrows=1, ncols=1, figsize=None,
                left=None, bottom=None, right=None, top=None,
                wspace=None, hspace=None, projection=None, **kwargs):
    mm = 1/25.4  # one millimeter in inches
    figw, figh = figsize
    return subplots_inches(nrows=nrows, ncols=ncols,
                           figsize=(figw*mm, figh*mm),
                           left=left*mm, right=right*mm,
                           bottom=bottom*mm, top=top*mm,
                           wspace=wspace*mm, hspace=hspace*mm,
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
