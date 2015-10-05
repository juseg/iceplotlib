"""
Plot an image map of bedrock surface elevation.
"""

from netCDF4 import Dataset
from matplotlib import pyplot as plt
from iceplotlib import plot as iplt
from iceplotlib import autoplot as aplt

# load data
nc = Dataset('pism_plot_sample.nc')

# plot
aplt.contour(nc, 'usurf', thkth=1.0, colors='black')
iplt.icemargin(nc, thkth=1.0)

# show
nc.close()
plt.show()
