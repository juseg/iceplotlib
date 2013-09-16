"""
Draw an ice surface velocity streamplot.
"""

from netCDF4 import Dataset
from matplotlib import pyplot as mplt
from iceplot import plot as iplt
from iceplot import autoplot as aplt

# load data
nc = Dataset('pism_plot_sample.nc')

# plot bedrock topography
aplt.bedtopoimage(nc)

# add surface streamplot
iplt.surfvelstreamplot(nc, density=5)

# add an ice margin
iplt.icemargincontour(nc, colors='white', alpha=0.75)

# show
mplt.show()

