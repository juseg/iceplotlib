"""
Plot surface velocity vectors.
"""

from netCDF4 import Dataset
from matplotlib import pyplot as plt
from iceplotlib import plot as iplt
from iceplotlib import autoplot as aplt

# load data
nc = Dataset('pism_plot_sample.nc')

# plot
im = aplt.quiver(nc, 'velsurf', thkth=1.0)
iplt.icemargin(nc, thkth=1.0)

# show
nc.close()
plt.show()
