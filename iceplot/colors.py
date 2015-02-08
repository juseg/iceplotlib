"""iceplot.colors

Provide default color preferences for each variable.
"""

from matplotlib.colors import LinearSegmentedColormap, LogNorm, Normalize
from iceplot.cm import land_topo, topo, velocity, shades

default_cmaps = {
    'air_temp':         'Spectral_r',
    'precipitation':    'YlGnBu',
    'temppabase':       'Blues_r',
    'topg':             topo,
    'thk':              'Blues_r',
    'usurf':            land_topo,
    'cbase':            velocity,
    'csurf':            velocity,
    'shading':          shades,
}

default_norms = {
    'air_temp':         Normalize(-30,30),
    'precipitation':    LogNorm(0.1,10),
    'temppabase':       Normalize(-10, 0),
    'topg':             Normalize(-6000,6000),
    'cbase':            LogNorm(10, 10000),
    'csurf':            LogNorm(10, 10000),
    'usurf':            Normalize(0,6000),
    'shading':          Normalize(0.0, 1.0),
}
