"""
Bond class, manages the connections between atoms in a system, and how they're drawn.
"""
from __future__ import annotations
from typing import Iterator, List
import copy

import scipy
import ase
import ase.neighborlist
import ase.data

from utils.chemical import Chemical
from utils.bond_styles import BondStyle, FrustumBond


class BondBag:
    """
    A collection of bonds. Because bonds come in bags.
    (Totally not a pun relating to the Bag of Bonds model)
    """
    def __init__(self, chemical: Chemical,
                 bond_style: BondStyle = FrustumBond):
        """
        Init for the bonds object.

        Args:
            chemical ([Chemical]): Chemical species, same as the Chemical class defined in this addon.
        """
        self._chemical: Chemical = chemical
        self._bond_style = bond_style

        self._adjacency_matrix = None
        self._bonds: List[Bond] = []
        self._has_calculated_bonds = False

        self.neighborlist = ase.neighborlist.NeighborList(cutoffs=ase.neighborlist.natural_cutoffs(chemical),
                                                          self_interaction=False,
                                                          primitive=ase.neighborlist.NewPrimitiveNeighborList)

    def __len__(self) -> int:
        return len(self._bonds)
    
    def __repr__(self):
        return f"BondBag with {len(self)} bonds"
    
    @property
    def bond_style(self) -> BondStyle:
        """Getter method for the bond style

        Returns:
            BondStyle: the current style used by bonds in the bag
        """
        return self._bond_style

    @bond_style.setter
    def bond_style(self, new_syle: BondStyle):
        """Setter method for the bond style

        Args:
            new_syle (BondStyle): New bond style to use for all bonds in the bagg
        """
        self._bond_style = new_syle
        if self._has_calculated_bonds:
            for bond in self._bonds:
                bond.bond_style = new_syle

    @property
    def bonds(self) -> List[Bond]:
        """Getter method for the bonds contained in the bag. There is no setter method.

        Returns:
            List[Bond]: List of bonds currently in the bag.
        """
        if not self._has_calculated_bonds:
            index_x, index_y, _ = scipy.sparse.find(self.adjacency_matrix)
            self._bonds = [
                Bond(self._chemical[x], self._chemical[y], self._bond_style) for x, y in zip(index_x, index_y)
            ]
            self._has_calculated_bonds = True
        return self._bonds

    @property
    def adjacency_matrix(self) -> scipy.sparse.dok.dok_matrix:
        """Calculates the adjacency matrix for the given chemical structure.
        Because the adjacency matrix is symmetric, only the upper-triangle is populated by ASE.

        Returns:
            scipy.sparse.dok.dok_matrix: The bond matrix. Can be accssed as matrix[a,b].
        """
        if self._adjacency_matrix is None:
            self.neighborlist.update(self._chemical)
            self._adjacency_matrix = self.neighborlist.get_connectivity_matrix(sparse=True)
        return self._adjacency_matrix

    
    

class Bond:
    """
    A bond between two atoms. Can have a style.
    Might be a banana, but only in the case of cyclopropyl rings.
    """
    def __init__(self, source_atom: ase.Atom,
                 destination_atom: ase.Atom,
                 bond_style: BondStyle = FrustumBond) -> None:
        self.source_atom = source_atom
        self.destination_atom = destination_atom
        self.bond_style = bond_style

    def draw(self) -> Bond:
        self.bond_style.spawn_bond_from_atoms(atom_start=self.source_atom,
                                              atom_end=self.destination_atom)
        return self
    