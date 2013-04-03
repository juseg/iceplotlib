"""iceplot.animation

Draw animations
"""

from matplotlib import pyplot as plt
from matplotlib.animation import FFMpegFileWriter, FuncAnimation
from iceplot import autoplot as aplt
from iceplot import plot as iplt

### Customized MovieWriter class ###

class IceWriter(FFMpegFileWriter):

  def __init__(self, temp_prefix='_tmp', clear_temp=True, *args, **kwargs):

    FFMpegFileWriter.__init__(self, *args, **kwargs)
    self.temp_prefix=temp_prefix
    self.clear_temp=clear_temp

  def setup(self, fig, outfile, dpi):

    return FFMpegFileWriter.setup(self, fig, outfile, dpi,
      frame_prefix=self.temp_prefix,
      clear_temp=self.clear_temp)

### Animations ###

def iceanim(mapsize, nc, t=None):
    """Draw basal topography, surface velocity and elevation contours"""

    def animate(i):
      plt.cla()
      iplt.icemap(nc, i)

    im = aplt.icemap(mapsize, nc, 0)
    return FuncAnimation(plt.gcf(), animate, t)

