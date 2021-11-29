"""
Factory controlling whether materials are singleton or not. This is to help deal with two scenarios:
1) The default behhavior where all atoms of one element type in the scene share the same materials
2) A scenario where a user wants to generate one set of materials per new chemical species
"""
import ase
import bpy
import typing
if typing.TYPE_CHECKING:
    import bpy.types
    import ase.data.colors

from utils import PACKAGE_PREFIX
GENERIC_CHEMICAL_ID = "Generic"
METALS = [3, 4, 11, 12, 13] + [*range(19, 31 + 1)] + [*range(37, 50 + 1)] + [*range(55, 83 + 1)] + [*range(87, 116 + 1)]
BSDF_SHADER_INPUTS = {
    "Base Color": 0,
    "Subsurface": 1,
    "Subsurface Radius": 2,
    "Subsurface Color": 3,
    "Metallic": 4,
    "Specular": 5,
    "Specular Tint": 6,
    "Roughness": 7,
    "Anisotropic": 8,
    "Anisotropic Rotation": 9,
    "Sheen": 10,
    "Sheen Tint": 11,
    "Clearcoat": 12,
    "Clearcoat Roughness": 13,
    "IOR": 14,
    "Transmission": 15,
    "Transmission Roughness": 16,
    "Emission": 17,
    "Emission Strength": 18,
    "Alpha": 19,
    "Normal": 20,
    "Clearcoat Normal": 21,
    "Tangent": 22,
}


def lazy_ase_import():
    import ase.data.colors


class MaterialFactory:
    """Factory controlling access to Blender materials (i.e. shaders)."""

    def __init__(self, materials_are_singleton=True):
        self.materials_are_singleton = materials_are_singleton
        lazy_ase_import()

    def get_material(self, symbol: str, chemical_id: str = GENERIC_CHEMICAL_ID) -> bpy.types.Material:
        """Gets a material, making it if it has not been made yet

        Args:
            symbol (str): Chemical symbol for the material.
            chemical_id (str): A unique identifier for a material.

        Notes:
            The factory will look up the material in its existing_materials dict to see whether
            the material has been created yet. If materials_are_singleton is set to true, this
            check is performed without regard for how many different chemicals are using it. If
            materials_are_singleton is set to false, the check is only performed against materials
            that are associated with the given chemical_id.

        Returns:
            bpy.types.Material: A material for the given chemical symbol.
        """
        key = self._get_material_key(chemical_id, symbol)
        material = bpy.data.materials.get(key)
        if material is None:
            material = self._create_material(symbol, key)
        return material

    def _get_material_key(self, chemical_id: str, symbol: str) -> str:
        """Creates a unique human-readable key for a material

        Args:
            symbol (str): Chemical symbol for the material.
            chemical_id (str): A unique identifier for a material.

        Returns:
            str: A unique human-readable key for the material
        """
        if self.materials_are_singleton:
            key = f"{PACKAGE_PREFIX}_{symbol}"
        else:
            key = f"{PACKAGE_PREFIX}_{symbol}_{chemical_id}"
        return key

    def _create_material(self, symbol: str, key: str) -> bpy.types.Material:
        """Creates a material given a symbol and chemical id. Uses JMol colors.

        Args:
            symbol (str): Chemical symbol for the material.
            chemical_id (str): A unique identifier for a material.

        Returns:
            bpy.types.Material: A material for the given chemical symbol.
        """

        color = [i for i in ase.data.colors.jmol_colors[ase.data.atomic_numbers[symbol]]] + [1]
        # TODO: Find a more generic place for color overrides
        if symbol == "C":
            color = [0.0, 0.0, 0.0, 1.0]

        material: bpy.types.Material = bpy.data.materials.new(key)

        # Find the principled node
        material.use_nodes = True
        shader: bpy.types.ShaderNodeBsdfPrincipled = material.node_tree.nodes.get('Principled BSDF')

        # Set some general material properties
        shader.inputs[BSDF_SHADER_INPUTS["Base Color"]].default_value = color
        if ase.data.atomic_numbers[symbol] in METALS:
            shader.inputs[BSDF_SHADER_INPUTS["Metallic"]].default_value = 1.0
            shader.inputs[BSDF_SHADER_INPUTS["Roughness"]].default_value = 0.2
            shader.inputs[BSDF_SHADER_INPUTS["Clearcoat"]].default_value = 0.0
        else:
            shader.inputs[BSDF_SHADER_INPUTS["Metallic"]].default_value = 0.0
            shader.inputs[BSDF_SHADER_INPUTS["Roughness"]].default_value = 1.0
            shader.inputs[BSDF_SHADER_INPUTS["Clearcoat"]].default_value = 1.0

        return material
