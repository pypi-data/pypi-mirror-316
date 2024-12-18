from .base_load import base
from .molgraph import Molecule
from typing import Type

__version__ = "1.0.11"
DEG2RAD = 0.0174532925199432957692
RAD2DEG = 1 / DEG2RAD
H2KC = 627.509474063
KC2H = 1 / H2KC
Confpool: Type[base.Confpool] = base.Confpool
MolProxy: Type[base.MolProxy] = base.MolProxy
