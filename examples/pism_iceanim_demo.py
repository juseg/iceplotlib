"""
Animation demo.
"""

from netCDF4 import Dataset
from matplotlib import pyplot as plt
from iceplotlib import animation as iani

# load data
nc = Dataset('pism_anim_sample.nc')

# animate
ani = iani.iceanim(nc, thkth=1.0)

# show
plt.show()

# to save the animation:
#ani.save('iceanim.mp4')
