"""
Plot an image map of bedrock surface elevation.
"""

from netCDF4 import Dataset
from matplotlib import pyplot as plt
from iceplot import autoplot as aplt

# load data
nc = Dataset('pism_plot_sample.nc')

# plot
im = aplt.contourf(nc, 'topg')

# show
nc.close()
plt.show()
