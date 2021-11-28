"""Class definitions for bond drawing styles.
This is where the main interface with blender should be for bond drawing.
"""

from numbers import Real
from typing import Tuple
from abc import ABC, abstractmethod

import numpy as np
import ase.data

import bpy


class BondStyle(ABC):
    """Abstract base class that bond styles should inherit from
    """

    @abstractmethod
    def spawn_bond_from_atoms(self,
                              atom_start: ase.Atom,
                              atom_end: ase.Atom,
                              offset: Tuple[Real, Real, Real]) -> bpy.types.Object:
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
            bpy.types.Object: A reference to the object that was created.
        """
        return None


class FrustumBond(BondStyle):
    """Depicts bonds as a frustrum. The radius of the start and end caps are calculated by
    multiplying the respective atomic radius by a constant according to the following equation.

    drawn_radius = atomic_radius * scale_factor

    Attributes:
        scale_factor (Real): Multiplier describing the bond's radius, relative to the atomic radius
        num_vertices (Real): Number of vertices used to draw each cap of the frustum.

    """

    def __init__(self, scale_factor: Real = 0.8, num_vertices: Real = 32):
        self.scale_factor = scale_factor
        self.num_vertices = num_vertices

    def spawn_bond_from_atoms(self,
                              atom_start: ase.Atom,
                              atom_end: ase.Atom,
                              offset: Tuple[Real, Real, Real] = (0, 0, 0)) -> bpy.types.Object:
        """Draws a frustum. The class's scale_factor attribute is used as
        a multiplier with the atomic radii to generate the radii of each end
        of the frustum. End caps are filled with triangle fans.

        Args:
            atom_start (ase.Atom): Atom at the start of the bond.
            atom_end (ase.Atom): Atom at the end of the bond.
            offset (Tuple[Real, Real, Real]): Vector of length 3, which gets
                                              added to each atomic position

        Returns:
            BondStyle: A reference to the class that was called.
        """
        # The origin of the spawned conic is at the midpoint of the two caps
        start_location = atom_start.position
        end_location = atom_end.position
        location = ((start_location + end_location) / 2) + offset

        # Bond scales
        start_radius = ase.data.covalent_radii[atom_start.number] * self.scale_factor
        end_radius = ase.data.covalent_radii[atom_start.number] * self.scale_factor

        # Figure out euler rotation
        deltas = start_location - end_location
        dx, dy, dz = deltas
        rotation_alpha = 0
        rotation_beta = np.arctan2(dx, dy)
        rotation_gamma = np.arccos(dz, np.linalg.norm(deltas))

        bpy.ops.mesh.primitive_cone_add(vertices=self.num_vertices,
                                        radius1=start_radius,
                                        radius2=end_radius,
                                        end_fill_type="TRIFAN",
                                        location=location)

        # TODO: See if this rotation can just be supplied directly to the primitve cone function
        bpy.context.object.rotation_euler[0] = rotation_alpha
        bpy.context.object.rotation_euler[1] = rotation_beta
        bpy.context.object.rotation_euler[2] = rotation_gamma

        return bpy.context.object
