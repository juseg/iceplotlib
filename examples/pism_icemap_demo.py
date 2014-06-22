"""
Draw the module's canonical icemap.
"""

from matplotlib import pyplot as plt
from iceplot import autoplot as aplt

# load data
filename = 'pism_plot_sample.nc'

# plot
aplt.icemap(filename, velsurf_cmap='CMRmap_r',
            usurf_cmap=None, usurf_colors='k')

# show
plt.show()
