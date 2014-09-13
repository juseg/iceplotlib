"""iceplot.autoplot

Provide an automatic plotting interface to plot entire figures with title and colorbar.
"""

from netCDF4 import Dataset
from matplotlib import pyplot as mplt
from iceplot import plot as iplt

def _init_figure(nc, cbar_mode=None):
    """Prepare figure and return axes for plot"""
    x = len(nc.dimensions['x'])
    y = len(nc.dimensions['y'])
    mapsize = (x*0.4, y*0.4)
    fig = iplt.simplefigure(mapsize, cbar_mode=cbar_mode)
    return mplt.axes(fig.grid[0])

### Generic mapping functions ###

def contour(nc, varname, t=0, **kwargs):
    ax = _init_figure(nc, cbar_mode='single')
    im = iplt.contour(nc, varname, t=t, ax=ax, **kwargs)
    cb = mplt.colorbar(im, ax.cax)
    cb.set_label(nc.variables[varname].long_name)

def contourf(nc, varname, t=0, **kwargs):
    ax = _init_figure(nc, cbar_mode='single')
    im = iplt.contourf(nc, varname, t=t, ax=ax, **kwargs)
    cb = mplt.colorbar(im, ax.cax)
    cb.set_label(nc.variables[varname].long_name)

def imshow(nc, varname, t=0, **kwargs):
    ax = _init_figure(nc, cbar_mode='single')
    im = iplt.imshow(nc, varname, t=t, ax=ax, **kwargs)
    cb = mplt.colorbar(im, ax.cax)
    cb.set_label(nc.variables[varname].long_name)

def quiver(nc, varname, t=0, **kwargs):
    ax = _init_figure(nc, cbar_mode='single')
    im = iplt.quiver(nc, varname, t=t, ax=ax, **kwargs)
    cb = mplt.colorbar(im, ax.cax)
    for cname in ['c'+varname.lstrip('vel'), varname+'_mag']:
        if cname in nc.variables:
            cb.set_label(nc.variables[cname].long_name)
            break

def streamplot(nc, varname, t=0, **kwargs):
    ax = _init_figure(nc, cbar_mode='none')
    im = iplt.streamplot(nc, varname, t=t, ax=ax, **kwargs)

### Specific mapping functions ###

def icemargin(nc, t=0, **kwargs):
    ax = _init_figure(nc, cbar_mode='none')
    im = iplt.icemargin(nc, t=t, ax=ax, **kwargs)

### Composite mapping functions ###

def icemap(nc, t=0, **kwargs):
    ax = _init_figure(nc, cbar_mode='single')
    im = iplt.icemap(nc, t=t, ax=ax, **kwargs)
    cb = mplt.colorbar(im, ax.cax)
    cb.set_label('ice surface velocity (m/yr)')

icemap.__doc__ = iplt.icemap.__doc__
