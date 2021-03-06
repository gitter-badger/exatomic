# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
'''
The Atomic Universe
#########################
The :class:`~exatomic.container.Universe` object is a subclass of
:class:`~exa.container.Container` that stores data coming from computational
chemistry experiments in a unified and systematic way. Data is organized into
"frames". A frame is an axis that can represent time (e.g. molecular dynamics
simulations), step number (e.g. geometry optimization), or an arbitrary index
like density functional theory exchange correlation functional.
'''
import pandas as pd
import numpy as np
from exa.container import TypedMeta, Container
from exatomic.atom import Atom
from exatomic.widget import UniverseWidget
from exatomic.field import AtomicField
from exatomic.orbital import Orbital, MOMatrix, DensityMatrix
from exatomic.basis import (SphericalGTFOrder, CartesianGTFOrder, Overlap,
                            BasisSetSummary, GaussianBasisSet, BasisSetOrder)
from exatomic.frame import Frame, compute_frame_from_atom


class UniverseTypedMeta(TypedMeta):
    '''
    Defines strongly typed attributes of the :class:`~exatomic.universe.Universe`
    and :class:`~exatomic.editor.AtomicEditor` objects.
    '''
    atom = Atom
    frame = Frame
    orbital = Orbital
    overlap = Overlap
    momatrix = MOMatrix
    field = AtomicField
    density = DensityMatrix
    basis_set_order = BasisSetOrder
    basis_set_summary = BasisSetSummary
    gaussian_basis_set = GaussianBasisSet
    spherical_gtf_order = SphericalGTFOrder
    cartesian_gtf_order = CartesianGTFOrder
#    two_free = Two
#    two_periodic = PeriodicTwo
#    field = AtomicField


class Universe(Container, metaclass=UniverseTypedMeta):
    '''
    The atomic container is called a universe because it represents everything
    known about the atomistic simulation (whether quantum or classical). This
    includes data such as atomic coordinates, molecular orbital energies, as
    well as (classical phenomena) such as two body distances, etc.

    Attributes:
        atom (:class:`~exatomic.atom.Atom`): Atomic coordinates, symbols, forces, etc.
    '''
    _widget_class = UniverseWidget

    @property
    def two(self):
        if self.is_periodic:
            return self.two_periodic
        return self.two_free

    # Compute functions
    def compute_frame(self):
        '''
        Compute a minmal frame table.
        '''
        self.frame = compute_frame_from_atom(self.atom)

    def __len__(self):
        return len(self.frame)
        return len(self.frame) if self._is('_frame') else 0



#from exatomic.frame import minimal_frame, Frame
#from exatomic.atom import Atom, ProjectedAtom, UnitAtom, VisualAtom
#from exatomic.two import Two, PeriodicTwo
#from exatomic.field import AtomicField
#from exatomic.atom import compute_unit_atom as _cua
#from exatomic.atom import compute_projected_atom as _cpa
#from exatomic.atom import compute_visual_atom as _cva
#from exatomic.two import max_frames_periodic as mfp
#from exatomic.two import max_atoms_per_frame_periodic as mapfp
#from exatomic.two import max_frames as mf
#from exatomic.two import max_atoms_per_frame as mapf
#from exatomic.two import compute_two_body as _ctb
#from exatomic.two import compute_bond_count as _cbc
#from exatomic.two import compute_projected_bond_count as _cpbc
#from exatomic.molecule import Molecule
#from exatomic.molecule import compute_molecule as _cm
#from exatomic.molecule import compute_molecule_com as _cmcom
#from exatomic.basis import lmap


##    @property
##    def unit_atom(self):
##        '''
##        Updated atom table using only in-unit-cell positions.
##
##        Note:
##            This function returns a standard :class:`~pandas.DataFrame`
##        '''
##        if not self._is('_unit_atom'):
##            self.compute_unit_atom()
##        atom = self.atom.copy()
##        atom.update(self._unit_atom)
##        return Atom(atom)
##
##    @property
##    def visual_atom(self):
##        '''
##        Visually pleasing atomic coordinates (useful for periodic universes).
##        '''
##        if self.is_periodic:
##            if self._visual_atom is None:
##                self.compute_visual_atom()
##            atom = self.atom.copy()
##            atom.update(self._visual_atom)
##            return atom
##        else:
##            return self.atom
##
##    @property
##    def projected_atom(self):
##        '''
##        Projected (unit) atom positions into a 3x3x3 supercell.
##        '''
##        if self._projected_atom is None:
##            self.compute_projected_atom()
##        return self._projected_atom
##
##    @property
##    def molecule(self):
##        if not self._is('_molecule'):
##            self.compute_molecule()
##        return self._molecule
##
##    @property
##    def field(self):
##        return self._field
##
##    @property
##    def orbital(self):
##        return self._orbital
##
##    @property
##    def basis_set(self):
##        return self._basis_set
##
##    @property
##    def momatrix(self):
##        return self._momatrix
#
#    @property
#    def is_periodic(self):
#        return self.frame.is_periodic
#
#    @property
#    def is_vc(self):
#        return self.frame.is_vc
#
##    @property
##    def basis_set(self):
##        return self._basis_set
##
##    @property
##    def basis_set_order(self):
##        return self._basis_set_order
##
##    @property
##    def basis_set_meta(self):
##        return self._basis_set_meta
##
##    @property
##    def basis_set_summary(self):
##        return self._basis_set_summary
##
##    @property
##    def overlap(self):
##        return self._overlap
##
##    @property
##    def density_matrix(self):
##        return self._density_matrix
##
##    @property
##    def spherical_gtf_order(self):
##        if self._is('_spherical_gtf_order'):
##            return self._spherical_gtf_order
##        else:
##            raise Exception('Compute spherical_gtf_order first!')
##
##    @property
##    def cartesian_gtf_order(self):
##        if self._is('_cartesian_gtf_order'):
##            return self._cartesian_gtf_order
##        else:
##            raise Exception('Compute cartesian_gtf_order first!')
##
#    # Compute
#    # ==============
#    # Compute methods create and attach new dataframe objects to the container
#    def compute_frame(self):
#        '''
#        Create a minimal frame using the atom table.
#        '''
#        self.frame = minimal_frame(self.atom)
#
#    def compute_unit_atom(self):
#        '''
#        Compute the sparse unit atom dataframe.
#        '''
#        self._unit_atom = _cua(self)
#
#    def compute_projected_atom(self):
#        '''
#        Compute the projected supercell from the unit atom coordinates.
#        '''
#        self._projected_atom = _cpa(self)
#
#    def compute_bond_count(self):
#        '''
#        Compute the bond count and update the atom table.
#
#        Returns:
#            bc (:class:`~pandas.Series`): :class:`~exatomic.atom.Atom` bond counts
#            pbc (:class:`~pandas.Series`): :class:`~exatomic.atom.PeriodicAtom` bond counts
#
#        Note:
#            If working with a periodic universe, the projected atom table will
#            also be updated; an index of minus takes the usual convention of
#            meaning not applicable or not calculated.
#        '''
#        self.atom['bond_count'] = _cbc(self)
#        self.atom['bond_count'] = self.atom['bond_count'].fillna(0).astype(np.int64)
#        self.atom['bond_count'] = self.atom['bond_count'].astype('category')
#
#    def compute_projected_bond_count(self):
#        '''
#        See Also:
#            :func:`~exatomic.two.compute_projected_bond_count`
#        '''
#        self.projected_atom['bond_count'] = _cpbc(self)
#        self.projected_atom['bond_count'] = self.projected_atom['bond_count'].fillna(-1).astype(np.int64)
#        self.projected_atom['bond_count'] = self.projected_atom['bond_count'].astype('category')
#
#    def compute_molecule(self, com=False):
#        '''
#        Compute the molecule table.
#        '''
#        if com:
#            self._molecule = _cm(self)
#            self.compute_visual_atom()
#            self._molecule = Molecule(pd.concat((self._molecule, _cmcom(self)), axis=1))
#        else:
#            self._molecule = _cm(self)
#
##    def compute_spherical_gtf_order(self, ordering_func):
##        '''
##        Compute the spherical Gaussian type function ordering dataframe.
##        '''
##        lmax = universe.basis_set['shell'].map(lmap).max()
##        self._spherical_gtf_order = SphericalGTFOrder.from_lmax_order(lmax, ordering_func)
##
##    def compute_cartesian_gtf_order(self, ordering_func):
##        '''
##        Compute the cartesian Gaussian type function ordering dataframe.
##        '''
##        lmax = universe.basis_set['shell'].map(lmap).max()
##        self._cartesian_gtf_order = SphericalGTFOrder.from_lmax_order(lmax, ordering_func)
##
#    def compute_two_free(self, *args, **kwargs):
#        self.compute_two_body(*args, **kwargs)
#
#    def compute_two_periodic(self, *args, **kwargs):
#        self.compute_two_body(*args, **kwargs)
#
#    def compute_two_body(self, *args, truncate_projected=True, **kwargs):
#        '''
#        Compute two body properties for the current universe.
#
#        For arguments see :func:`~exatomic.two.get_two_body`. Note that this
#        operation (like all compute) operations are performed in place.
#
#        Args:
#            truncate_projected (bool): Applicable to periodic universes - decreases the size of the projected atom table
#        '''
#        if self.is_periodic:
#            self.two_periodic = _ctb(self, *args, **kwargs)
#            if truncate_projected:
#                self.truncate_projected_atom()
#        else:
#            self.two_free = _ctb(self, *args, **kwargs)
#
#    def compute_visual_atom(self):
#        '''
#        Create visually pleasing coordinates (useful for periodic universes).
#        '''
#        self._visual_atom = _cva(self)
#
#    def classify_molecules(self, *args, **kwargs):
#        '''
#        Add classifications (of any form) for molecules.
#
#        .. code-block:: Python
#
#            universe.classify_molecules(('Na', 'solute'), ('H(2)O(1)', 'solvent'))
#
#        Args:
#            \*classifiers: ('identifier', 'classification', exact)
#
#
#        Warning:
#            Will attempt to compute molecules if they haven't been computed.
#        '''
#        self.molecule.classify(*args, **kwargs)
#
#    def slice_by_molecules(self, identifier):
#        '''
#        String, list of string, index, list of indices, slice
#        '''
#        raise NotImplementedError()
#
#    def truncate_projected_atom(self):
#        '''
#        When first generated, the projected_atom table contains many atomic
#        coordinates that are not used when computing two body properties. This
#        function will truncate this table, keeping only useful coordinates.
#        Projected coordinates can always be generated using
#        :func:`~exatomic.atom.compute_projected_atom`.
#        '''
#        pa = self.periodic_two['prjd_atom0'].astype(np.int64)
#        pa = pa.append(self.periodic_two['prjd_atom1'].astype(np.int64))
#        self._projected_atom = ProjectedAtom(self._projected_atom[self._projected_atom.index.isin(pa)])
#
