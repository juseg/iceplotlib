"""
Draw an ice surface velocity quiver.
"""

from netCDF4 import Dataset
from matplotlib import pyplot as mplt
from iceplot import plot as iplt
from iceplot import autoplot as aplt

# load data
nc = Dataset('pism_plot_sample.nc')

# plot bed temperature contour
aplt.surfvelquiver(nc)

# add an ice margin
iplt.icemargincontour(nc)

# show
mplt.show()

