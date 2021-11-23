"""
Bond class, manages the connections between atoms in a system, and how they're drawn.
"""
from __future__ import annotations
from functools import cached_property
from typing import Iterator, List, Tuple
import copy

import scipy
import numpy as np
import ase, ase.neighborlist, ase.data

from utils import Chemical
from utils.bond_styles import BondStyle, ConicBond


class BondBag:
    """
    A collection of bonds. Because bonds come in bags.
    (Totally not a pun relating to the Bag of Bonds model)
    """
    def __init__(self, chemical: Chemical,
                 bond_style: BondStyle = ConicBond):
        """
        Init for the bonds object.

        Args:
            chemical ([Chemical]): Chemical species, same as the Chemical class defined in this addon.
        """
        self._adjacency_matrix = None
        self.__cutoffs = ase.neighborlist.natural_cutoffs(chemical)
        self.__chemical = chemical
        self.neighborlist = ase.neighborlist.NeighborList(cutoffs=self.__cutoffs,
                                                          self_interaction=False,
                                                          primitive=ase.neighborlist.NewPrimitiveNeighborList)
        self._bond_style = bond_style
        self._bonds: List[Bond] = []
        self._has_calculated_bonds = False     
    
    @property
    def bond_style(self) -> BondStyle:
        return self._bond_style
    
    @bond_style.setter
    def bond_style(self, new_syle:  BondStyle):
        self._bond_style = new_syle
        if self._has_calculated_bonds:
            for bond in self._bonds:
                bond.bond_style = new_syle
        
    @property
    def bonds(self) -> List[Bond]:
        if not self._has_calculated_bonds:
            index_x, index_y, order = scipy.sparse.find(self.get_adjacency_matrix())           
            self._bonds = [Bond(self.__chemical[x], self.__chemical[y], self._bond_style) for x, y in zip(index_x, index_y)]
            self._has_calculated_bonds = True
        return self._bonds
        

    @property
    def adjacency_matrix(self) -> scipy.sparse.dok.dok_matrix:
        """
        Calculates the adjacency matrix for the given chemical structure.
        Because the adjacency matrix is symmetric, only the upper-triangle is populated by ASE.

        Returns:
            scipy.sparse.dok.dok_matrix: The bond matrix. Can be accssed as matrix[a,b].
        """
        if self._adjacency_matrix is None:
            self.neighborlist.update(self.__chemical)
            self._adjacency_matrix = self.neighborlist.get_connectivity_matrix(sparse=True)
        return self._adjacency_matrix
    
    # Magic Methods being copied from Bonds. Could probably reduce repetitious code here with some metaprogramming
    # incantation, but decided against that in the interest of making this easier for my IDE.
    # Can't just subclass UserList; that breaks some methods because our constructor takes more than one argument.
    def __len__(self) -> int:
        return len(self._bonds)
    def __getitem__(self, key) -> Bond:
        return self._bonds[key]
    def __setitem__(self, key, value):
        self._bonds[key] = value
    def __delitem__(self, key):
        del self._bonds[key]
    def __iter__(self) -> Iterator:
        return iter(self._bonds)
    def __reversed__(self) -> List:
        return reversed(self._bonds)
    def __contains__(self, item) -> bool:
        return item in self._bonds
    
    def __add__(self, other: List[Bond]) -> List[Bond]:
        return self._bonds + other
    def __iadd__(self, other):
        self._bonds += other
    def __mul__(self, other) -> List[Bond]:
        return self._bonds * other
    def __imul__(self, other):
        self._bonds *= other
    def __rmul__(self, other) -> List[Bond]:
        return other * self
    
    def __eq__(self, other) -> bool:
        return self._bonds == other
    def __ne__(self, other) -> bool:
        return self._bonds != other
    def __lt__(self, other) -> bool:
        return self._bonds < other
    def __gt__(self, other) -> bool:
        return self._bonds > other
    def __le__(self, other) -> bool:
        return self._bonds <= other
    def __ge__(self, other) -> bool:
        return self._bonds >= other
        
    
    # Could do some metaprogramming magic here to just assign all methods of self._bonds to this class. But that would
    # make things a lot harder for the IDE to interpret. So doing the repetitious stuff here.
    def append(self, value) -> BondBag:
        self._bonds.append(value)
        return self
    def extend(self, iterable) -> BondBag:
        self._bonds.extend(iterable)
        return self
    def insert(self, i, x) -> BondBag:
        self._bonds.insert(i, x)
        return self
    def remove(self, x) -> BondBag:
        self._bonds.remove(x)
        return self
    def pop(self, i=-1) -> List[Bond]:
        return self._bonds.pop(i)
    def clear(self) -> BondBag:
        self._bonds.clear()
        return self
    def index(self, x, start=0, end=None) -> int:
        # Python appears to choose the max unsigned int64 as the default value of "end", but that
        # might be implementation-specific to CPython. So, we'll just do a check and avoid
        # messing with that value.
        if end is None:
            return self._bonds.index(x, start)
        else:
            return self._bonds.index(x, start, end)
    def count(self, x) -> int:
        return self._bonds.count(x)
    def sort(self, *args, **kwargs) -> BondBag:
        self._bonds.sort(*args, **kwargs)
        return self
    def reverse(self) -> BondBag:
        return self._bonds.reverse()
    def copy(self) -> BondBag:
        return copy.copy(self)

class Bond:
    """
    A bond between two atoms. Can have a style.
    Might be a banana, but only in the case of cyclopropyl rings.
    """
    def __init__(self,
                 source_atom: ase.Atom, destination_atom: ase.Atom,
                 bond_style: BondStyle = ConicBond) -> None:
        self.source_atom = source_atom
        self.destination_atom = destination_atom
        self.start_position = source_atom.position
        self.end_position = destination_atom.position
        
        self.bond_style = bond_style
        
    def __invert__(self) -> Bond:
        return Bond(source_atom=self.destination_atom, destination_atom=self.source_atom)