# -*- coding: utf-8 -*-
'''
Two Body Properties DataFrame
===============================
Two body properties are interatomic distances.
'''
from sklearn.neighbors import NearestNeighbors
from exa import _np as np
from exa import _pd as pd
from exa.config import Config
from exa.frames import DataFrame, ManyToMany
if Config.numba:
    from exa.jitted.iteration import repeat_i8, repeat_i8_array
    from exa.jitted.indexing import unordered_pairing_function
else:
    import numpy.repeat as repeat_i8
    import numpy.repeat as repeat_i8_array
    from exa.algorithms.indexing import unordered_pairing_function
from atomic import Isotope


bond_extra = 0.45
dmin = 0.3
dmax = 8.3


class TwoBase:
    '''
    '''
    __fk__ = ['frame']
    __groupby__ = 'frame'


class Two(TwoBase, DataFrame):
    '''
    '''
    __pk__ = ['two']


class ProjectedTwo(TwoBase, DataFrame):
    '''
    '''
    __pk__ = ['prjd_two']


class AtomTwo(ManyToMany):
    '''
    '''
    __fks__ = ['atom', 'two']


class ProjectedAtomTwo(ManyToMany):
    '''
    '''
    __fks__ = ['prjd_atom', 'prjd_two']


def get_two_body(universe, k=None, dmax=dmax, dmin=dmin,
                 bond_extra=bond_extra, inplace=False):
    '''
    Compute two body information given a universe.

    For non-periodic systems the only required argument is the table of atom
    positions and symbols. For periodic systems, at a minimum, the atoms and
    frames dataframes must be provided.

    Bonds are computed semi-empirically and exist if:

    .. math::

        distance(A, B) < covalent\_radius(A) + covalent\_radius(B) + bond\_extra

    Args:
        atoms (:class:`~atomic.atom.Atom`): Table of nuclear positions and symbols
        frames (:class:`~pandas.DataFrame`): DataFrame of periodic cell dimensions (or False if )
        k (int): Number of distances (per atom) to compute
        dmax (float): Max distance of interest (larger distances are ignored)
        dmin (float): Min distance of interest (smaller distances are ignored)
        bond_extra (float): Extra distance to include when determining bonds (see above)

    Returns:
        df (:class:`~atomic.twobody.TwoBody`): Two body property table
    '''
    two = None
    atomtwo = None
    periodic = universe.is_periodic()
    if periodic:
        if len(universe.projected_atom) == 0:
            two, atomtwo = _periodic_from_unit_in_mem(universe, k, dmax, dmin, bond_extra)
        else:
            two, atomtwo = _periodic_from_projected_in_mem(universe, k, dmax, dmin, bond_extra)
    else:
        two = _free_in_mem(universe, dmax, dmin, bond_extra)
    if inplace and periodic:
        universe._prjd_two = two
        universe._prjd_atomtwo = atomtwo
    elif inplace:
        universe._two = two
        universe._atomtwo = atomtwo
    else:
        return (two, atomtwo)


def _free_in_mem(universe, dmax=12.3, dmin=0.3, bond_extra=bond_extra):
    '''
    Free boundary condition two body properties computed in memory.

    Args:
        universe (:class:`~atomic.universe.Universe`): The atomic universe
        dmax (float): Max distance of interest
        dmin (float): Minimum distance of interest
        bond_extra (float): Extra distance to add when determining bonds

    Returns:
        twobody (:class:`~atomic.twobody.TwoBody`)
    '''
    raise NotImplementedError()


def _free_memmap():    # Same as _free_in_mem but using numpy.memmap
    raise NotImplementedError()


def _periodic_from_atom_in_mem(universe, k=None, dmax=dmax, dmin=dmin, bond_extra=bond_extra):
    '''
    Compute periodic two body properties given only the absolute positions and
    the cell dimensions.

    Args:
        universe (:class:`~atomic.universe.Universe`): The atomic universe
        k (int): Number of distances (per atom) to compute
        dmax (float): Max distance of interest
        dmin (float): Minimum distance of interest
        bond_extra (float): Extra distance to add when determining bonds

    Returns:
    '''
    raise NotImplementedError()


def _periodic_from_unit_in_mem(universe, k=None, dmax=dmax, dmin=dmin, bond_extra=bond_extra):
    '''
    Compute periodic two body properties given only the absolute positions and
    the cell dimensions.

    Args:
        universe (:class:`~atomic.universe.Universe`): The atomic universe
        k (int): Number of distances (per atom) to compute
        dmax (float): Max distance of interest
        dmin (float): Minimum distance of interest
        bond_extra (float): Extra distance to add when determining bonds

    Returns:
        periodic_twobody (:class:`~atomic.twobody.PeriodicTwoBody`): Periodic two body properties
    '''
    raise NotImplementedError()


def _periodic_from_projected_in_mem(universe, k=None, dmax=12.3, dmin=0.3, bond_extra=0.5):
    '''
    '''
    k = universe.frame['atom_count'].max() if k is None else k
    prjd_grps = universe.projected_atom.groupby('frame')
    unit_grps = universe.unit_atom.groupby('frame')
    n = prjd_grps.ngroups
    distances = np.empty((n, ), dtype='O')
    index1 = np.empty((n, ), dtype='O')
    index2 = np.empty((n, ), dtype='O')
    frames = np.empty((n, ), dtype='O')
    for i, (frame, prjd) in enumerate(prjd_grps):                    # Per frame, compute the distances,
        pxyz = DataFrame(prjd)._get_column_values('x', 'y', 'z')     # also saving the associated indices
        uxyz = DataFrame(unit_grps.get_group(frame))._get_column_values('x', 'y', 'z')
        dists, idxs = NearestNeighbors(n_neighbors=k, metric='euclidean').fit(pxyz).kneighbors(uxyz)
        distances[i] = dists.ravel()
        index1[i] = prjd.iloc[repeat_i8_array(idxs[:, 0], k)].index.values
        index2[i] = prjd.iloc[idxs.ravel()].index.values
        frames[i] = repeat_i8(frame, len(index1[i]))
    distances = np.concatenate(distances)
    index1 = np.concatenate(index1)
    index2 = np.concatenate(index2)
    frames = np.concatenate(frames)
    two = pd.DataFrame.from_dict({'distance': distances, 'frame': frames,
                                 'prjd_atom1': index1, 'prjd_atom2': index2})  # We will use prjd_atom1/2 to deduplicate data
    two = two[(two['distance'] > dmin) & (two['distance'] < dmax)]
    two['id'] = unordered_pairing_function(two['prjd_atom1'].values, two['prjd_atom2'].values)
    print(len(two))
    two = two.drop_duplicates('id').reset_index(drop=True)
    print(len(two))
    del two['id']
    symbols = universe.projected_atom['symbol']
    two['symbol1'] = two['prjd_atom1'].map(symbols)
    two['symbol2'] = two['prjd_atom2'].map(symbols)
    two['symbols'] = two['symbol1'] + two['symbol2']
    del two['symbol1']
    del two['symbol2']
    two['mbl'] = two['symbols'].map(Isotope.lookup_sum_radii_by_symbols)
    two['mbl'] += bond_extra
    two['bond'] = two['distance'] < two['mbl']
    del two['mbl']
    two.index.names = ['prjd_two']
    prjd_two = two.index.tolist() * 2
    prjd_atom = two['prjd_atom1'].tolist() + two['prjd_atom2'].tolist()
    del two['prjd_atom1']
    del two['prjd_atom2']
    atomtwo = pd.DataFrame.from_dict({'prjd_two': prjd_two, 'prjd_atom': prjd_atom})
    return ProjectedTwo(two), ProjectedAtomTwo(atomtwo)
