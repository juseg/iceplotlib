"""
Draw the module's canonical icemap.
"""

from matplotlib import pyplot as plt
from iceplotlib import autoplot as aplt

# load data
nc = aplt.load('pism_plot_sample.nc')

# plot
aplt.icemap(nc, thkth=1.0, velsurf_cmap='CMRmap_r',
            usurf_cmap=None, usurf_colors='k')

# show
nc.close()
plt.show()
