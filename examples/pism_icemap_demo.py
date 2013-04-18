"""
Draw the module's canonical icemap.
"""

from netCDF4 import Dataset
from matplotlib import pyplot as mplt
from iceplot import autoplot as aplt

# load data
nc = Dataset('pism_plot_sample.nc')

# plot
im = aplt.icemap((60, 120), nc)

# show
mplt.show()

