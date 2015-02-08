"""pismplot.cm

Provide custom colormaps.
"""

from matplotlib.colors import LinearSegmentedColormap

def _cmap_from_list(name, colors):
    """Create a linear colormap from a non-normalized color list"""
    if len(colors[0]) == 2:
        bounds, colors = zip(*colors)
        bmin = bounds[0]
        bmax = bounds[-1]
        bounds = [(b - bmin) / (bmax - bmin) for b in bounds]
        colors = zip(bounds, colors)
    return LinearSegmentedColormap.from_list(name, colors)

# Topographic colormaps

_sea_topo_clist = [
    (-6000., '#71abd8'),
    (-3000., '#79b2de'),
    (-2000., '#84b9e3'),
    (-1500., '#8dc1ea'),
    (-1000., '#96c9f0'),
    ( -750., '#a1d2f7'),
    ( -500., '#acdbfb'),
    ( -250., '#b9e3ff'),
    ( -100., '#c6ecff'),
    (    0., '#d8f2fe')]

sea_topo = _cmap_from_list('sea_topo', _sea_topo_clist)

_land_topo_clist = [
(   0., '#d8f2fe'),
( 0.01, '#94bf8b'),
(  50., '#acd0a5'),
( 100., '#a8c68f'),
( 250., '#bdcc96'),
( 500., '#d1d7ab'),
( 750., '#e1e4b5'),
(1000., '#efebc0'),
(1250., '#e8e1b6'),
(1500., '#ded6a3'),
(1750., '#d3ca9d'),
(2000., '#cab982'),
(3000., '#c3a76b'),
(4000., '#b9985a'),
(6000., '#aa8753')]

land_topo = _cmap_from_list('land_topo', _land_topo_clist)

_topo_clist = _sea_topo_clist[:-1] + _land_topo_clist

topo = _cmap_from_list('topo', _topo_clist)

# Other colormaps

_velocity_clist = [
  '#ffffff', '#00ffff', '#ffff00', '#ff0000', '#000000']

velocity = _cmap_from_list('velocity', _velocity_clist)

# Transparent shadows colormap

_shades_clist = [(0.0, (0,0,0,0)), (1.0, (0,0,0,1))]

shades = _cmap_from_list('shades', _shades_clist)
