""":mod:`iceplotlib.figure`

Provide GridFigure class and derivatives, where the figure size is computed from a given map size and an axes grid.
"""

from matplotlib.figure import Figure
from mpl_toolkits.axes_grid1.axes_grid import ImageGrid

mm = 1/25.4

### GridFigure class ###

class GridFigure(Figure):
  """Gridded figure with arbitrary cols and rows and optional colorbars"""

  def __init__(self,
      mapsize, nrows_ncols, axes_pad=5*mm,
      cbar_mode=None, cbar_location='right',
      cbar_pad=5*mm, cbar_size=5*mm,
      sideplot=False, **kwargs):
    """Compute figure size and initialize axes grid"""

    # compute axes grid size
    (mapw, maph) = mapsize
    maph *= mm
    mapw *= mm
    (rows, cols) = nrows_ncols
    gridw = cols*(mapw+axes_pad) - axes_pad
    gridh = rows*(maph+axes_pad) - axes_pad

    # compute figure size
    figw = gridw + 2*axes_pad
    figh = gridh + 2*axes_pad
    if sideplot:
      figw = figw + figh - 2*axes_pad

    # additional space for colorbars
    # TODO: allow 'bottom' and 'left' colorbar locations
    if cbar_mode is 'each' and cbar_location is 'right':
      gridw += cols*(cbar_size + cbar_pad)
      figw  += cols*(cbar_size + cbar_pad) + 10.*mm
    if cbar_mode is 'each' and cbar_location is 'top':
      gridh += rows*(cbar_size + cbar_pad)
      figh  += rows*(cbar_size + cbar_pad) + 10.*mm
    if cbar_mode is 'single' and cbar_location is 'right':
      gridw += cbar_size + cbar_pad
      figw  += cbar_size + cbar_pad + 10.*mm
    if cbar_mode is 'single' and cbar_location is 'top':
      gridh += cbar_size + cbar_pad
      figh  += cbar_size + cbar_pad + 10.*mm

    # initialize figure
    Figure.__init__(self, **kwargs)
    self.set_size_inches(figw,figh)
    rect = (axes_pad/figw, axes_pad/figh, gridw/figw, gridh/figh)

    # create axes grid
    self.grid = ImageGrid(self, rect,
      nrows_ncols=nrows_ncols, axes_pad=axes_pad,
      cbar_mode=cbar_mode, cbar_location=cbar_location,
      cbar_pad=cbar_pad, cbar_size=cbar_size)

    # remove ticks
    for ax in self.grid:
      ax.get_xaxis().set_visible(False)
      ax.get_yaxis().set_visible(False)

    # add more axes
    if sideplot:
      self.add_axes([(gridw+4*axes_pad)/figw, 2*axes_pad/figh,
        (maph-2*axes_pad)/figw, (maph-2*axes_pad)/figh])

### Derivative classes ###

class SimpleFigure(GridFigure):
  """Simple figure with optional colorbar"""

  def __init__(self, mapsize, **kwargs):
    GridFigure.__init__(self, mapsize, (1,1), **kwargs)

class DoubleInlineFigure(GridFigure):
  """Double inline figure with optional colorbar"""

  def __init__(self, mapsize, **kwargs):
    GridFigure.__init__(self, mapsize, (1,2), **kwargs)
