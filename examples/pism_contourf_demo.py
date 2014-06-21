"""
Plot an image map of bedrock surface elevation.
"""

from matplotlib import pyplot as plt
from iceplot import autoplot as aplt

# load data
ncfname = 'pism_plot_sample.nc'

# plot
im = aplt.contourf(ncfname, 'topg')

# show
plt.show()
