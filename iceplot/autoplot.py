"""iceplot.autoplot

Provide an automatic plotting interface to plot entire figures with title and colorbar.
"""

from matplotlib import pyplot as mplt
from iceplot import plot as iplt

def _init_figure(nc, cbar_mode=None):
    """Prepare figure and return axes for plot"""
    x = len(nc.dimensions['x'])
    y = len(nc.dimensions['y'])
    mapsize = (y*0.4, x*0.4)
    fig = iplt.simplefigure(mapsize, cbar_mode=cbar_mode)
    return mplt.axes(fig.grid[0])

### Image mapping functions ###

def bedtopoimage(nc, t=0, **kwargs):
    ax = _init_figure(nc, cbar_mode='single')
    im = iplt.bedtopoimage(nc, t, **kwargs)
    cb = mplt.colorbar(im, ax.cax, format='%g')
    cb.set_label('bed topography (m)')

def surftopoimage(nc, t=0, **kwargs):
    ax = _init_figure(nc, cbar_mode='single')
    im = iplt.surftopoimage(nc, t, **kwargs)
    cb = mplt.colorbar(im, ax.cax, format='%g')
    cb.set_label('surface topography (m)')

def airtempimage(nc, t=0, **kwargs):
    ax = _init_figure(nc, cbar_mode='single')
    im = iplt.airtempimage(nc, t, **kwargs)
    cb = mplt.colorbar(im, ax.cax, format='%g')
    cb.set_label('air temperature (degC)')

def precipimage(nc, t=0, **kwargs):
    ax = _init_figure(nc, cbar_mode='single')
    im = iplt.precipimage(nc, t, **kwargs)
    cb = mplt.colorbar(im, ax.cax, format='%g')
    cb.set_label('precipitation rate (m/yr)')

def surfvelimage(nc, t=0, **kwargs):
    ax = _init_figure(nc, cbar_mode='single')
    im = iplt.surfvelimage(nc, t, **kwargs)
    cb = mplt.colorbar(im, ax.cax, format='%g')
    cb.set_label('ice surface velocity (m/yr)')

bedtopoimage.__doc__  = iplt.bedtopoimage.__doc__
surftopoimage.__doc__ = iplt.surftopoimage.__doc__
airtempimage.__doc__  = iplt.airtempimage.__doc__
precipimage.__doc__   = iplt.precipimage.__doc__
surfvelimage.__doc__  = iplt.surfvelimage.__doc__

### Contour mapping functions ###

def icemargincontour(nc, t=0, **kwargs):
    ax = _init_figure(nc, cbar_mode=None)
    im = iplt.icemargincontour(nc, t, **kwargs)

def surftopocontour(nc, t=0, **kwargs):
    ax = _init_figure(nc, cbar_mode='single')
    im = iplt.surftopocontour(nc, t, **kwargs)
    cb = mplt.colorbar(im, ax.cax, format='%g')
    cb.set_label('surface topography (m)')

def bedtempcontour(nc, t=0, **kwargs):
    ax = _init_figure(nc, cbar_mode='single')
    im = iplt.bedtempcontour(nc, t, **kwargs)
    cb = mplt.colorbar(im, ax.cax, format='%g')
    cb.set_label('pressure-adjusted basal temperature (K)')

icemargincontour.__doc__ = iplt.icemargincontour.__doc__
surftopocontour.__doc__  = iplt.surftopocontour.__doc__
bedtempcontour.__doc__   = iplt.bedtempcontour.__doc__

### Quiver mapping functions ###

def bedvelquiver(nc, t=0, **kwargs):
    ax = _init_figure(nc, cbar_mode='single')
    im = iplt.bedvelquiver(nc, t, **kwargs)
    cb = mplt.colorbar(im, ax.cax, format='%g')
    cb.set_label('ice basal velocity (m/yr)')

def surfvelquiver(nc, t=0, **kwargs):
    ax = _init_figure(nc, cbar_mode='single')
    im = iplt.surfvelquiver(nc, t, **kwargs)
    cb = mplt.colorbar(im, ax.cax, format='%g')
    cb.set_label('ice surface velocity (m/yr)')

bedvelquiver.__doc__  = iplt.bedvelquiver.__doc__
surfvelquiver.__doc__ = iplt.surfvelquiver.__doc__

### Composite mapping functions ###

def icemap(nc, t=0, **kwargs):
    ax = _init_figure(nc, cbar_mode='single')
    im = iplt.icemap(nc, t, **kwargs)
    cb = mplt.colorbar(im, ax.cax, format='%g')
    cb.set_label('ice surface velocity (m/yr)')

icemap.__doc__ = iplt.icemap.__doc__

