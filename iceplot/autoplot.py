"""iceplot.autoplot

Provide an automatic plotting interface to plot entire figures with title and colorbar.
"""

from matplotlib import pyplot as plt
from iceplot import plot as iplt

def automatize(funcname, clabel=None):
    """Transform a plotting function into an autoplotting function"""

    def autofunc(mapsize, nc, t=0):

      # prepare figure
      fig = iplt.simplefigure(mapsize, cbar_mode='single')
      ax  = fig.grid[0]
      ax.get_xaxis().set_visible(False)
      ax.get_yaxis().set_visible(False)

      # plot
      plt.sca(ax)
      sm = getattr(iplt, funcname)(nc, t)

      # add colorbar
      cb = plt.colorbar(sm, ax.cax, format='%g')
      cb.set_label(clabel)

    return autofunc

icemap     = automatize('icemap',     'ice surface velocity (m/yr)')
bedtempmap = automatize('bedtempmap', 'pressure-adjusted bed temperature (K)')
bedvelmap  = automatize('bedvelmap',  'basal velocity (m/yr)')

