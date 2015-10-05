"""
Plot surface velocity streamlines.
"""

from matplotlib import pyplot as plt
from iceplotlib import plot as iplt
from iceplotlib import autoplot as aplt

# load data
nc = iplt.load('pism_plot_sample.nc')

# plot
im = aplt.streamplot(nc, 'velsurf', thkth=1.0)
iplt.icemargin(nc, thkth=1.0)

# show
nc.close()
plt.show()
