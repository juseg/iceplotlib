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
    im = iplt.contour(nc, varname, t=t, **kwargs)
    cb = mplt.colorbar(im, ax.cax)
    cb.set_label(nc.variables[varname].long_name)

def contourf(nc, varname, t=0, **kwargs):
    ax = _init_figure(nc, cbar_mode='single')
    im = iplt.contourf(nc, varname, t=t, **kwargs)
    cb = mplt.colorbar(im, ax.cax)
    cb.set_label(nc.variables[varname].long_name)

def imshow(nc, varname, t=0, **kwargs):
    ax = _init_figure(nc, cbar_mode='single')
    im = iplt.imshow(nc, varname, t=t, **kwargs)
    cb = mplt.colorbar(im, ax.cax)
    cb.set_label(nc.variables[varname].long_name)

### Specific mapping functions ###

def icemargin(nc, t=0, **kwargs):
    ax = _init_figure(nc, cbar_mode='none')
    im = iplt.icemargin(nc, t=t, **kwargs)

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

def basetempimage(nc, t=0, **kwargs):
    ax = _init_figure(nc, cbar_mode='single')
    im = iplt.basetempimage(nc, t, **kwargs)
    cb = mplt.colorbar(im, ax.cax, format='%g')
    cb.set_label('pressure-adjusted basal temperature (degC)')

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

def basevelimage(nc, t=0, **kwargs):
    ax = _init_figure(nc, cbar_mode='single')
    im = iplt.basevelimage(nc, t, **kwargs)
    cb = mplt.colorbar(im, ax.cax, format='%g')
    cb.set_label('ice basal velocity (m/yr)')

def surfvelimage(nc, t=0, **kwargs):
    ax = _init_figure(nc, cbar_mode='single')
    im = iplt.surfvelimage(nc, t, **kwargs)
    cb = mplt.colorbar(im, ax.cax, format='%g')
    cb.set_label('ice surface velocity (m/yr)')

bedtopoimage.__doc__  = iplt.bedtopoimage.__doc__
surftopoimage.__doc__ = iplt.surftopoimage.__doc__
basetempimage.__doc__ = iplt.basetempimage.__doc__
airtempimage.__doc__  = iplt.airtempimage.__doc__
precipimage.__doc__   = iplt.precipimage.__doc__
basevelimage.__doc__  = iplt.basevelimage.__doc__
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

def basetempcontour(nc, t=0, **kwargs):
    ax = _init_figure(nc, cbar_mode='single')
    im = iplt.basetempcontour(nc, t, **kwargs)
    cb = mplt.colorbar(im, ax.cax, format='%g')
    cb.set_label('pressure-adjusted basal temperature (degC)')

def airtempcontour(nc, t=0, **kwargs):
    ax = _init_figure(nc, cbar_mode='single')
    im = iplt.airtempcontour(nc, t, **kwargs)
    cb = mplt.colorbar(im, ax.cax, format='%g')
    cb.set_label('air temperature (degC)')

def precipcontour(nc, t=0, **kwargs):
    ax = _init_figure(nc, cbar_mode='single')
    im = iplt.precipcontour(nc, t, **kwargs)
    cb = mplt.colorbar(im, ax.cax, format='%g')
    cb.set_label('precipitation rate (m/yr)')

def basevelcontour(nc, t=0, **kwargs):
    ax = _init_figure(nc, cbar_mode='single')
    im = iplt.basevelcontour(nc, t, **kwargs)
    cb = mplt.colorbar(im, ax.cax, format='%g')
    cb.set_label('ice basal velocity (m/yr)')

def surfvelcontour(nc, t=0, **kwargs):
    ax = _init_figure(nc, cbar_mode='single')
    im = iplt.surfvelcontour(nc, t, **kwargs)
    cb = mplt.colorbar(im, ax.cax, format='%g')
    cb.set_label('ice surface velocity (m/yr)')

icemargincontour.__doc__ = iplt.icemargincontour.__doc__
surftopocontour.__doc__  = iplt.surftopocontour.__doc__
basetempcontour.__doc__  = iplt.basetempcontour.__doc__
airtempcontour.__doc__   = iplt.airtempcontour.__doc__
precipcontour.__doc__    = iplt.precipcontour.__doc__
basevelcontour.__doc__    = iplt.basevelcontour.__doc__
surfvelcontour.__doc__   = iplt.surfvelcontour.__doc__

### Quiver mapping functions ###

def basevelquiver(nc, t=0, **kwargs):
    ax = _init_figure(nc, cbar_mode='single')
    im = iplt.basevelquiver(nc, t, **kwargs)
    cb = mplt.colorbar(im, ax.cax, format='%g')
    cb.set_label('ice basal velocity (m/yr)')

def surfvelquiver(nc, t=0, **kwargs):
    ax = _init_figure(nc, cbar_mode='single')
    im = iplt.surfvelquiver(nc, t, **kwargs)
    cb = mplt.colorbar(im, ax.cax, format='%g')
    cb.set_label('ice surface velocity (m/yr)')

basevelquiver.__doc__ = iplt.basevelquiver.__doc__
surfvelquiver.__doc__ = iplt.surfvelquiver.__doc__

### Streamplot mapping functions ###

def basevelstreamplot(nc, t=0, **kwargs):
    ax = _init_figure(nc, cbar_mode='none')
    im = iplt.basevelstreamplot(nc, t, **kwargs)

def surfvelstreamplot(nc, t=0, **kwargs):
    ax = _init_figure(nc, cbar_mode='none')
    im = iplt.surfvelstreamplot(nc, t, **kwargs)

basevelstreamplot.__doc__ = iplt.basevelstreamplot.__doc__
surfvelstreamplot.__doc__ = iplt.surfvelstreamplot.__doc__

### Composite mapping functions ###

def icemap(nc, t=0, **kwargs):
    ax = _init_figure(nc, cbar_mode='single')
    im = iplt.icemap(nc, t=t, **kwargs)
    cb = mplt.colorbar(im, ax.cax)
    cb.set_label('ice surface velocity (m/yr)')

icemap.__doc__ = iplt.icemap.__doc__
