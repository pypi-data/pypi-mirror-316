import matplotlib.pyplot as plt
import numpy as np

from ._common import jitted


class VelocityModel:
    
    def __init__(self, *args):
        if len(args) == 1 and np.ndim(args[0]) == 2:
            d, vp, vs, rho = np.transpose(args[0])

        elif len(args) == 4:
            d, vp, vs, rho = args

        else:
            raise ValueError("invalid velocity model parameters")

        self._thickness = np.asarray(d)
        self._velocity_p = np.asarray(vp)
        self._velocity_s = np.asarray(vs)
        self._density = np.asarray(rho)

    def __len__(self):
        return self.n_layers
    
    def __repr__(self):
        # Table headers
        out = []
        out += [f"{'Velocity model':<40}"]
        out += [f"{40 * '-'}"]
        out += [
            f"{'d'.rjust(10)}{'vp'.rjust(10)}{'vs'.rjust(10)}{'rho'.rjust(10)}"
        ]
        out += [
            f"{'[km]'.rjust(10)}{'[km/s]'.rjust(10)}{'[km/s]'.rjust(10)}{'[g/cm3]'.rjust(10)}"
        ]

        # Tables
        out += [f"{40 * '-'}"]
        out += [
            f"{d:>10.4f}{vp:>10.4f}{vs:>10.4f}{rho:>10.4f}"
            for d, vp, vs, rho in self.to_numpy()
        ]
        out += [f"{40 * '-'}\n"]

        return "\n".join(out)

    def plot(self, parameters=None, zmax=None, plot_args=None, ax=None):
        if parameters is None:
            parameters = ["vp", "vs", "rho"]

        elif isinstance(parameters, str):
            parameters = [parameters]

        d, vp, vs, rho = self.to_numpy().T
        z = d.cumsum()
        n = z.size

        # Plot arguments
        plot_args = plot_args if plot_args is not None else {}
        _plot_args = {"linewidth": 2}
        _plot_args.update(plot_args)

        # Determine zmax
        if zmax is None:
            tmp = d.copy()
            tmp[-1] = tmp[:-1].min()
            zmax = tmp.sum()

        # Build layered model
        zin = np.zeros(2 * n)
        zin[1:-1:2] = z[:-1]
        zin[2::2] = z[:-1]
        zin[-1] = max(z[-1], zmax)

        # Plot
        ax = ax if ax is not None else plt.gca()

        for parameter in parameters:
            if parameter in {"velocity_p", "vp"}:
                x = vp
                label = "$V_p$"

            elif parameter in {"velocity_s", "vs"}:
                x = vs
                label = "$V_s$"

            elif parameter in {"density", "rho"}:
                x = rho
                label = "$\\rho$"

            else:
                raise ValueError(f"invalid parameter '{parameter}'")
            
            xin = np.empty(2 * n)
            xin[1::2] = x
            xin[2::2] = x[1:]
            xin[0] = xin[1]
            ax.plot(xin, zin, label=label, **_plot_args)

        ax.set_ylim(zmax, zin.min())

    def resample(self, dz):
        velocity_model = self.to_numpy()

        # Handle water layer
        if (self._velocity_s[0] <= 0.0).any():
            d0, vp0, vs0, rho0 = velocity_model[0]
            d, vp, vs, rho = velocity_model[1:].T

        else:
            d0, vp0, vs0, rho0 = None, None, None, None
            d, vp, vs, rho = velocity_model.T

        parameters = np.column_stack((vp, vs, rho))
        sizes = np.where(d > dz, np.ceil(d / dz), 1.0).astype(int)
        size = sizes.sum()
        dout = np.empty(size, dtype=np.float64)
        pout = np.empty((size, 3), dtype=np.float64)
        _resample(d, parameters, sizes, dout, pout)

        if d0 is not None:
            dout = np.insert(dout, 0, d0)
            pout = np.row_stack(([[vp0, vs0, rho0], pout]))

        return VelocityModel(dout, *pout.T)
    
    def to_dict(self):
        return {
            "thickness": self._thickness,
            "velocity_p": self._velocity_p,
            "velocity_s": self._velocity_s,
            "density": self._density,
        }

    def to_list(self):
        return [[d, vp, vs, rho] for d, vp, vs, rho in zip(self._thickness, self._velocity_p, self._velocity_s, self._density)]

    def to_numpy(self):
        return np.column_stack((self._thickness, self._velocity_p, self._velocity_s, self._density))
    
    @property
    def n_layers(self):
        return self._thickness.size

    @property
    def thickness(self):
        return self._thickness
    
    @property
    def velocity_p(self):
        return self._velocity_p
    
    @property
    def velocity_s(self):
        return self._velocity_s
    
    @property
    def density(self):
        return self._density
    
    @property
    def d(self):
        return self._thickness
    
    @property
    def vp(self):
        return self._velocity_p
    
    @property
    def vs(self):
        return self._velocity_s
    
    @property
    def rho(self):
        return self._density


@jitted
def _resample(thickness, parameters, sizes, d, par):
    """Compile loop in :meth:`VelocityModel.resample`."""
    mmax = len(thickness)

    j = 0
    for i in range(mmax):
        dzi = thickness[i] / sizes[i]
        
        for _ in range(sizes[i]):
            d[j] = dzi
            par[j] = parameters[i]
            j += 1
