"""
Animation demo.
"""

from netCDF4 import Dataset
from matplotlib import pyplot as mplt
from iceplot import animation as iani

# load data
nc = Dataset('pism_anim_sample.nc')

# animate
ani = iani.iceanim(nc)

# show
mplt.show()

# to save the animation:
#ani.save('iceanim.mp4')

