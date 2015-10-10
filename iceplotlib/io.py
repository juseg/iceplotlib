""":mod:`iceplotlib.io`

Provide an interface to PISM NetCDF files.
"""

from numpy.ma import masked_where
from netCDF4 import Dataset, MFDataset


class IceDataset(Dataset):
    """NetCDF Dataset with functions for data extraction."""

    def _extract_2d(self, varname, t):
        """Extract two-dimensional array from a netcdf variable."""
        var = self.variables[varname]
        if t == 'djf':
            z = var[[12, 0, 1]].mean(axis=2)
        elif t == 'mam':
            z = var[2:5].mean(axis=2)
        elif t == 'jja':
            z = var[6:8].mean(axis=2)
        elif t == 'son':
            z = var[9:11].mean(axis=2)
        elif t == 'mean':
            z = var[:].mean(axis=2)
        elif t is None:
            z = var[:].squeeze()
        else:
            z = var[t]
        return z.T

    def extract_mask(self, t, thkth=None):
        """Extract ice-cover mask from a netcdf file."""
        t = t or 0  # if t is None use first time slice
        if thkth is not None:
            mask = self._extract_2d('thk', t)
            mask = (mask < thkth)
        else:
            mask = self._extract_2d('mask', t)
            mask = (mask == 0) + (mask == 4)
        return mask

    def extract_xyuvc(self, varname, t, thkth=None):
        """Extract coordinates and vector field from a netcdf file."""
        x = self.variables['x'][:]
        y = self.variables['y'][:]
        u = self._extract_2d('u'+varname, t)
        v = self._extract_2d('v'+varname, t)
        mask = self.extract_mask(t, thkth=thkth)
        u = masked_where(mask, u)
        v = masked_where(mask, v)
        for cname in ['c'+varname.lstrip('vel'), varname+'_mag']:
            if cname in self.variables:
                c = self._extract_2d(cname, t)
                break
        else:
            c = (u**2 + v**2)**0.5
        return x, y, u, v, c

    def extract_xyz(self, varname, t, thkth=None):
        """Extract coordinates and scalar field from a netcdf file."""
        x = self.variables['x'][:]
        y = self.variables['y'][:]
        z = self._extract_2d(varname, t)
        if varname not in ('mask', 'topg') and 'mask' in self.variables:
            mask = self.extract_mask(t, thkth=thkth)
            z = masked_where(mask, z)
        return x, y, z

class MFIceDataset(IceDataset, MFDataset):
    pass
