"""Class definitions for bond drawing styles.
This is where the main interface with blender should be for bond drawing.
"""
from numbers import Real
from typing import Tuple
from abc import ABC, abstractmethod
import ase.data


class BondStyle(ABC):
    """Abstract base class that bond styles should inherit from
    """
    @abstractmethod
    def spawn_bond_from_atoms(self, atom_start: ase.Atom, atom_end: ase.Atom, offset: Tuple[Real, Real, Real]):
        """This method should call blender to draw a bond between
        the two atoms. The given off-set can be used if the origin
        of the atoms should be shifted before drawing. This is usually
        the position of the 3D cursor.

        Args:
            atom_start (ase.Atom): Atom at the start of the bond.
            atom_end (ase.Atom): Atom at the end of the bond.
            offset (Tuple[Real, Real, Real]): Vector of length 3, which gets
                                              added to each atomic position

        Returns:
            BondStyle: A reference to the class that was called.
        """
        return self


class FrustumBond(BondStyle):
    """Depicts bonds as a frustrum. The radius of the start and end caps are calculated by
    multiplying the respective atomic radius by a constant.
    """
    def __init__(self, scale_factor: Real = 0.8):
        self.scale_factor = scale_factor

    def spawn_bond_from_atoms(self, atom_start: ase.Atom, atom_end: ase.Atom, offset: Tuple[Real, Real,
                                                                                            Real]) -> BondStyle:
        """Draws a frustum. The class's scale_factor attribute is used as
        a multiplier with the atomic radii to generate the radii of each end
        of the frustum.

        Args:
            atom_start (ase.Atom): Atom at the start of the bond.
            atom_end (ase.Atom): Atom at the end of the bond.
            offset (Tuple[Real, Real, Real]): Vector of length 3, which gets
                                              added to each atomic position

        Returns:
            BondStyle: A reference to the class that was called.
        """
        # start_radius = ase.data.covalent_radii[atom_start.number]
        # end_radius = ase.data.covalent_radii[atom_start.number]
        raise NotImplementedError()
