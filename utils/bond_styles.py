"""Class definitions for bond drawing styles.
This is where the main interface with blender should be for bond drawing.
"""

from numbers import Real
from typing import Tuple
from abc import ABC, abstractmethod

import numpy as np
import ase.data

import bpy
import mathutils
from utils import PACKAGE_PREFIX


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

    def __init__(self, scale_factor: Real = 0.25, num_vertices: int = 32):
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
        depth = np.abs(np.linalg.norm(atom_start.position - atom_end.position))

        # The origin of the spawned conic is at the midpoint of the two caps
        location = ((atom_start.position + atom_end.position) / 2) + offset

        # Bond scales
        start_radius = ase.data.covalent_radii[atom_start.number] * self.scale_factor
        end_radius = ase.data.covalent_radii[atom_end.number] * self.scale_factor

        quaternion = self.calculate_track_quaternion(atom_start.position, atom_end.position)
        bpy.ops.mesh.primitive_cone_add(vertices=self.num_vertices,
                                        radius1=start_radius,
                                        radius2=end_radius,
                                        depth=depth,
                                        end_fill_type="TRIFAN",
                                        location=location)

        # Fix rotation
        bpy.context.object.rotation_mode = "QUATERNION"
        bpy.context.object.rotation_quaternion = quaternion

        # Shade smooth
        for poly in bpy.context.object.data.polygons:
            poly.use_smooth = True

        # Rename object
        bpy.context.object.name = f"bond_{atom_start.symbol}-{atom_end.symbol}_frustum"

        # Set material
        glass_shader = generic_glass()
        bpy.context.object.active_material = glass_shader
        return bpy.context.object

    @staticmethod
    def calculate_track_quaternion(start_position, end_position):
        direction = mathutils.Vector(end_position - start_position)
        quaternion = direction.to_track_quat("Z", "Y")

        return quaternion


GLASS_BSDF_INPUTS = {
    "Color": 0,
    "Roughness": 1,
    "IOR": 2,
    "Normal": 3,
}


def generic_glass():
    material_name = f"{PACKAGE_PREFIX}_generic_glass"
    material = bpy.data.materials.get(material_name)
    if material is None:
        # Create the material
        material = bpy.data.materials.new(material_name)
        material.use_nodes = True

        # Find the nodes currently in there
        nodes = material.node_tree.nodes
        bsdf = nodes.get("Principled BSDF")
        output = nodes.get("Material Output")

        # Replace the BSDF node with a glass shader
        nodes.remove(bsdf)
        glass = nodes.new("ShaderNodeBsdfGlass")
        material.node_tree.links.new(output.inputs["Surface"], glass.outputs["BSDF"])

        # Set attributes of glass shader
        glass.inputs[GLASS_BSDF_INPUTS["Color"]].default_value = (0.90126,
                                                                  1.00,
                                                                  0.895707,
                                                                  1.0)  # Very slightly green color
        glass.inputs[GLASS_BSDF_INPUTS["Roughness"]].default_value = 0.250
        glass.inputs[GLASS_BSDF_INPUTS["IOR"]].default_value = 1.450
    return material
