"""
Draw the module's canonical icemap.
"""

from netCDF4 import Dataset
from matplotlib import pyplot as plt
from iceplotlib import autoplot as aplt

# load data
nc = Dataset('pism_plot_sample.nc')

# plot
aplt.icemap(nc, velsurf_cmap='CMRmap_r',
            usurf_cmap=None, usurf_colors='k')

# show
nc.close()
plt.show()
