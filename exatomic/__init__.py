# -*- coding: utf-8 -*-
__exatomic_version__ = (0, 2, 2)                  # exatomic VERSION NUMBER
__version__ = '.'.join((str(v) for v in __exatomic_version__))


from exa.relational import Isotope, Length, Energy, Time, Amount, Constant


from exatomic._config import global_config
from exatomic.frame import Frame
from exatomic.atom import Atom
from exatomic.molecule import Molecule
from exatomic.basis import GaussianBasis, BasisSet
from exatomic.universe import Universe
from exatomic.editor import Editor
from exatomic.formula import SimpleFormula
from exatomic.filetypes import XYZ, write_xyz, Cube
from exatomic.algorithms import nearest_molecules, einstein_relation, radial_pair_correlation
from exatomic._install import install
from exatomic import tests

if not global_config['exa_persistent']:
    install()
