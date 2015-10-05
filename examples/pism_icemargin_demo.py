"""
Plot an image map of bedrock surface elevation.
"""

from matplotlib import pyplot as plt
from iceplotlib import autoplot as aplt

# load data
nc = aplt.load('pism_plot_sample.nc')

# plot
im = aplt.icemargin(nc, thkth=1.0)

# show
nc.close()
plt.show()
