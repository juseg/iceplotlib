"""iceplot.autoplot

Provide an automatic plotting interface to plot entire figures with title and colorbar.
"""

from matplotlib import pyplot as plt
from iceplot import plot as iplt

def _automatize(funcname, clabel=None):
    """Transform a plotting function into an autoplotting function"""

    def autofunc(nc, t=0, **kwargs):

      # get mapsize from nc file
      x = len(nc.dimensions['x'])
      y = len(nc.dimensions['y'])
      mapsize = (y*0.4, x*0.4)

      # prepare figure
      cbar_mode = 'single' if clabel else None
      fig = iplt.simplefigure(mapsize, cbar_mode=cbar_mode)
      ax  = fig.grid[0]

      # plot
      plt.sca(ax)
      sm = getattr(iplt, funcname)(nc, t, **kwargs)

      # add colorbar
      if clabel is not None:
        cb = plt.colorbar(sm,ax.cax, format='%g')
        cb.set_label(clabel)

    autofunc.__doc__ = getattr(iplt, funcname).__doc__

    return autofunc

_bedtoponame  = 'bed ropography (m)'
_surftoponame = 'surface topography (m)'
_airtempname  =u'air temperature (degC)'
_precname     = 'precipitation rate (m/yr)'
_bedtempname  = 'pressure-adjusted basal temperature (K)'
_bedvelname   = 'ice basal velocity (m/ yr)'
_surfvelname  = 'ice surface velocity (m/ yr)'

bedtopoimage    = _automatize('bedtopoimage',  _bedtoponame)
surftopoimage   = _automatize('surftopoimage', _surftoponame)
airtempimage    = _automatize('airtempimage',  _airtempname)
precipimage     = _automatize('precipimage',   _precname)
surfvelimage    = _automatize('surfvelimage',  _surfvelname)

icemargincontour= _automatize('icemargincontour')
surftopocontour = _automatize('surftopocontour', _surftoponame)
bedtempcontour  = _automatize('bedtempcontour', _bedtempname)

bedvelquiver    = _automatize('bedvelquiver',   _bedvelname)
surfvelquiver   = _automatize('surfvelquiver',  _surfvelname)
icemap          = _automatize('icemap',         _surfvelname)

