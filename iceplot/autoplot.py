"""iceplot.autoplot

Provide an automatic plotting interface to plot entire figures with title and colorbar.
"""

from matplotlib import pyplot as plt
from iceplot import plot as iplt

def icemap(mapsize, nc, t=0):
    """Draw basal topography, surface velocity and elevation contours"""

    # prepare figure
    fig = iplt.simplefigure(mapsize, cbar_mode='single')
    ax  = fig.grid[0]
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)

    # plot
    plt.sca(ax)
    im = iplt.icemap(nc, 0)

    # add colorbar
    cb = plt.colorbar(im, ax.cax, format='%g')
    cb.set_label('ice surface velocity (m/yr)')

