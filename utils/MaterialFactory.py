"""
Factory controlling whether materials are singleton or not. This is to help deal with two scenarios:
1) The default behhavior where all atoms of one element type in the scene share the same materials
2) A scenario where a user wants to generate one set of materials per new chemical species
"""
from typing import Dict

import bpy


class MaterialFactory:
    def __init__(self, materials_are_singleton=True):
        self.materials_are_singleton = materials_are_singleton

        self.existing_materials = {}

    # ======
    # Public
    # ======

    def get_material(symbol: str, chemical_hash: str) -> bpy.types.Material:
        """Controls getting and creating materials. Uses JMol colors.

        Args:
            symbol (str): Chemical symbol for the material.
            chemical_hash (str): A unique identifier for a material.

        Note:
            The factory will look up the material in its existing_materials dict to see whether
            the material has been created yet. If materials_are_singleton is set to true, this
            check is performed without regard for how many different chemicals are using it. If
            materials_are_singleton is set to false, the check is only performed against materials
            that are associated with the given chemical_hash.

        Returns:
            bpy.types.Material: A material for the given chemical symbol.
        """
        # TODO: Implement get_material in the material factory
        ...

    # =======
    # Private
    # =======