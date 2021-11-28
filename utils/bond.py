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
    def __init__(self, chemical: Chemical, bond_style: BondStyle = FrustumBond):
        """
        Init for the bonds object.

        Args:
            chemical ([Chemical]): Chemical species, same as the Chemical class defined in this addon.
        """
        self.__chemical: Chemical = chemical
        self._bond_style = bond_style

        self._adjacency_matrix = None
        self._bonds: List[Bond] = []
        self._has_calculated_bonds = False

        self.__cutoffs = ase.neighborlist.natural_cutoffs(chemical)

        self.neighborlist = ase.neighborlist.NeighborList(cutoffs=self.__cutoffs,
                                                          self_interaction=False,
                                                          primitive=ase.neighborlist.NewPrimitiveNeighborList)

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
                Bond(self.__chemical[x], self.__chemical[y], self._bond_style) for x, y in zip(index_x, index_y)
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

    def append(self, value) -> BondBag:
        """Accesses the append method of the list of bonds.
        Nothing fancy, it's just a normal Python list.
        """
        self._bonds.append(value)
        return self

    def extend(self, iterable) -> BondBag:
        """Accesses the extend method of the list of bonds.
        Nothing fancy, it's just a normal Python list.
        """
        self._bonds.extend(iterable)
        return self

    def insert(self, i, x) -> BondBag:
        """Accesses the insert method of the list of bonds.
        Nothing fancy, it's just a normal Python list.
        """
        self._bonds.insert(i, x)
        return self

    def remove(self, x) -> BondBag:
        """Accesses the remove method of the list of bonds.
        Nothing fancy, it's just a normal Python list.
        """
        self._bonds.remove(x)
        return self

    def pop(self, i=-1) -> List[Bond]:
        """Accesses the pop method of the list of bonds.
        Nothing fancy, it's just a normal Python list.
        """
        return self._bonds.pop(i)

    def clear(self) -> BondBag:
        """Accesses the clear method of the list of bonds.
        Nothing fancy, it's just a normal Python list.
        """
        self._bonds.clear()
        return self

    def count(self, x) -> int:
        """Accesses the count method of the list of bonds.
        Nothing fancy, it's just a normal Python list.
        """
        return self._bonds.count(x)

    def sort(self, *args, **kwargs) -> BondBag:
        """Accesses the sort method of the list of bonds.
        Nothing fancy, it's just a normal Python list.
        """
        self._bonds.sort(*args, **kwargs)
        return self

    def reverse(self) -> List[Bond]:
        """Accesses the reverse method of the list of bonds.
        Nothing fancy, it's just a normal Python list.
        """
        return self._bonds.reverse()

    def copy(self) -> BondBag:
        """Accesses the copy method of the list of bonds.
        Nothing fancy, it's just a normal Python list.
        """
        return copy.copy(self)

    def index(self, x, start=0, end=None) -> int:
        """Accesses the index method of the list of bonds.
        Nothing fancy, it's just a normal Python list.
        """
        # Python appears to choose the max unsigned int64 as the default value of "end", but that
        # might be implementation-specific to CPython. So, we'll just do a check and avoid
        # messing with that value.
        if end is None:
            return self._bonds.index(x, start)
        else:
            return self._bonds.index(x, start, end)


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
        self.start_position = source_atom.position
        self.end_position = destination_atom.position

        self.bond_style = bond_style

    def __invert__(self) -> Bond:
        return Bond(source_atom=self.destination_atom, destination_atom=self.source_atom)
    