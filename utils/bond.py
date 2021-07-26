"""
Bond class, manages the connections between atoms in a system, and how they're drawn.
"""
from __future__ import annotations
from functools import cached_property
from typing import List, Tuple

import scipy
import numpy as np
import ase, ase.neighborlist, ase.data
import bpy

from utils import Chemical


class Bonds:
    """
    A collection of bonds
    """
    def __init__(self, chemical: Chemical, cylinder_radius: float = 0.1, bond_end_expansion: float = 0.01):
        """
        Init for the bonds object.

        Args:
            chemical ([Chemical]): Chemical species, same as the Chemical class defined in this addon.
        """
        self.__cutoffs = ase.neighborlist.natural_cutoffs(chemical)
        self.__chemical = chemical
        self.neighborlist = ase.neighborlist.NeighborList(cutoffs=self.__cutoffs,
                                                          self_interaction=False,
                                                          primitive=ase.neighborlist.NewPrimitiveNeighborList)
        self.cylinder_radius = cylinder_radius
        self.bond_end_expansion = bond_end_expansion

    def __iter__(self):
        return iter(self.get_bonds())

    @cached_property
    def get_adjacency_matrix(self) -> scipy.sparse.dok.dok_matrix:
        """
        Calculates the adjacency matrix for the given chemical structure.
        Because the adjacency matrix is symmetric, only the upper-triangle is populated by ASE.

        Returns:
            scipy.sparse.dok.dok_matrix: The bond matrix. Can be accssed as matrix[a,b].
        """
        self.neighborlist.update(self.__chemical)
        bond_matrix = self.neighborlist.get_connectivity_matrix(sparse=True)
        return bond_matrix

    @cached_property
    def get_bonds(self) -> List[List[int]]:
        """
        Creates a list of bonds present in the system.

        Returns:
            List[List[int]]: List of bonds present in the system. Given as a list containing the
                             indices in the Chemical object that was passed in of each bond in the
                             system. Double counting is disabled, so only a single set of bonds
                             is shown.
        """
        index_x, index_y, order = scipy.sparse.find(self.get_adjacency_matrix())
        bonds = [(x, y) for x, y in zip(index_x, index_y)]
        return bonds

    def __calculate_bond_start_ends(self, atom_start: ase.Atom, atom_end: ase.Atom,
                                    offset: List[float, float, float]) -> Tuple[float, float, float, float]:
        """
        Calculates where the bond starts and where it ends. Also gives points to start the flares on the ends of the bond.

        The bond's penetration into either atom is calculated such that the fully flared-out bond cylinder, with radius equal to
        self.cylinderr_radius * self.bond_end_expansion, exactly touches the sphere when it ends.

        Args: 
            atom_start (ase.Atom): Atom at the start of the bond.
            atom_end (ase.Atom): Atom at the end of the bond.
            offset (List[float, float, float]): A coordinate describing the chemical's offset (usually the 3D cursor)

        Returns:
            Tuple[float, float, float, float]: A tuple containing four values. The first is the coordinate where the bond
            should start. Second is where the flare to the starting atom begins. Third is where the flare to the ending atom
            begins. Fourth is where the bond ends.
        """
        # Do some initial geometry
        start_radius = ase.data.covalent_radii[atom_start.number]
        end_radius = ase.data.covalent_radii[atom_end.number]

        start_center = atom_start.position + offset
        end_center = atom_end.position + offset

        distance_between_surfaces = np.linalg.norm(start_center - end_center) - start_radius - end_radius

        # Find a vector between the two points
        vec = end_center - start_center
        unit_vec = vec / np.linalg.norm(vec)

        # For looks, penetrate a bit into the spheres
        start_penetration_radius = np.sqrt(start_radius**2 - (self.cylinder_radius * self.bond_end_expansion)**2)
        end_penetration_radius = np.sqrt(end_radius**2 - (self.cylinder_radius * self.bond_end_expansion)**2)

        # Also, flare the ends of the bonds a bit
        bond_flare_percent = 0.1
        flare_distance = distance_between_surfaces * bond_flare_percent
        bond_flare_start = start_center + unit_vec * (start_radius + flare_distance)
        bond_flare_end = start_center + unit_vec * (start_radius + distance_between_surfaces - flare_distance)

        # Calculate bond start and end locations
        bond_start = start_center + unit_vec * start_penetration_radius
        bond_end = start_center + unit_vec * (start_radius + distance_between_surfaces +
                                              (end_radius - end_penetration_radius))

        return bond_start, bond_flare_start, bond_flare_end, bond_end

    def spawn_bond_from_atoms(self, atom_start: ase.Atom, atom_end: ase.Atom, offset: List[float]) -> Bonds:
        """
        Given a pair of atoms and an origin, will spawn a cylinder (flared at both ends) to represent a bond.

        Args:
            atom_start (ase.Atom): The atom at the start of the bond.
            atom_end (ase.Atom): The atom at the end of the bond.
            offset (List[float]): An origin for the local coordinate system, used for the vector math. Usually the 3D cursor.

        Returns:
            Bonds: A reference to this object.
        """
        # Do some initial geometry
        bond_start, bond_flare_start, bond_flare_end, bond_end = self.__calculate_bond_start_ends(
            atom_start, atom_end, offset)

        # TODO: Actually draw the curve here

        return self
