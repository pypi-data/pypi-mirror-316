import os
import sys
import numpy as np
from typing import Generator, Tuple

MAIN_PACKAGE = True

if MAIN_PACKAGE:
    sys.path.insert(0, os.path.dirname(__file__))
    from .cpppart import cpppart as base
else:
    from ..cpppart import cpppart as base


def _rmsd_interval(
    self, start_rmsd: float, end_rmsd: float, matr: np.ndarray
) -> Generator[Tuple[base.MolProxy, base.MolProxy, float], None, None]:
    """Iterate over all pairs of conformers whose RMSD fits a given range [start_rmsd, end_rmsd].
    If start_rmsd < end_rmsd, then conformers are yielded in the order of increasing RMSD. Otherwise, in the order of decreasing RMSD.

    Args:
        start_rmsd (float): start of RMSD range for iteration
        end_rmsd (float): end of RMSD range for iteration
        matr (np.ndarray): RMSD matrix

    Yields:
        Generator[Tuple[base.MolProxy, base.MolProxy, float], None, None]: Generator of conformer pairs with respective RMSD values
    """
    min_rmsd = min(start_rmsd, end_rmsd)
    max_rmsd = max(start_rmsd, end_rmsd)
    ascending = 1 if start_rmsd < end_rmsd else -1
    assert matr.ndim == 2
    assert matr.shape[0] == len(self) and matr.shape[1] == len(self)

    df = {'molA': [], 'molB': [], 'rmsd': []}
    for i in range(matr.shape[0]):
        for j in range(i):
            if matr[i, j] > min_rmsd and matr[i, j] < max_rmsd:
                df['molA'].append(i)
                df['molB'].append(j)
                df['rmsd'].append(matr[i, j])

    df['molA'], df['molB'], df['rmsd'] = zip(
        *sorted(zip(df['molA'], df['molB'], df['rmsd']),
                key=lambda x: ascending * x[2]))

    for indexA, indexB, rmsd in zip(df['molA'], df['molB'], df['rmsd']):
        yield self[indexA], self[indexB], float(rmsd)


base.Confpool.rmsd_fromto = _rmsd_interval

# def _center_single_coords(self) -> None:
#     """Center coordinates of a single conformation by subtracting centroid (the mean of each coordinate).

# .. code-block:: python
#     >>> p[0].xyz
#     array([[1., 0., 0.],
#            [2., 0., 0.]])
#     >>> p[0].make_centered()
#     >>> p[0].xyz
#     array([[-0.5,  0. ,  0. ],
#            [ 0.5,  0. ,  0. ]])

#     """
#     coords: np.ndarray = self.xyz
#     coords -= coords.mean(axis=0)
#     self.xyz = coords

# base.MolProxy.make_centered = _center_single_coords

# def _center_all_coords(self) -> None:
#     """Center coordinates of all conformations in the ensemble by subtracting centroids (the mean of each coordinate).

# .. code-block:: python
#     >>> p.make_centered()
#     >>> # Equivatent to this:
#     >>> for m in p:
#     ...     m.make_centered()
#     """
#     for m in self:
#         m.make_centered()

# base.Confpool.make_centered = _center_all_coords
