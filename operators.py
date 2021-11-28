"""
Blender operator classes are in this file
"""
from typing import Set
import sys
import subprocess
import importlib

import bpy
import bpy_extras

import utils.chemical

DEPENDENCIES = ("ase",)


class HYDRIDIC_OT_install_dependencies(bpy.types.Operator):
    """Handles installing Python packages necessary for the addon to run.

    It does this by checking if all of the packages specified in the "DEPENDENCIES"
    variable are installed. If any are missing, pip tries to install them.

    The user accesses this operator via the addon preferences menu.
    """

    bl_idname = "hydridic.install_dependencies"
    bl_label = "Install Dependencies (May take several minutes)"
    bl_description = (
        "Downloads and installs packages required for this add-on to work."
        " An internet connection is required, and Blender may need to run"
        " with elevated permissions.")
    bl_options = {"REGISTER", "INTERNAL"}

    @classmethod
    def dependencies_installed(cls) -> bool:
        """Checks whether the addon's dependencies are installed. These
        are specified by the DEPENDENCIES variable within this file.

        Returns:
            bool: True if (and only if) all dependencies are installed.
        """
        return all(
            importlib.util.find_spec(dependency)
            for dependency in DEPENDENCIES)

    @classmethod
    def poll(cls, context: bpy.types.Context) -> bool:
        """Boolean that determines whether to set the addon install button to active"""
        return not cls.dependencies_installed()

    def execute(self, context: bpy.types.Context) -> Set[str]:
        """Method determining what happens when the user clicks the 'install addon' buttoon'.
        In this case, the addons defined in the DEPENDENCIES variable are installed with the
        pip executable shipped by Blender."""
        subprocess.call(
            [sys.executable, "-m", "pip", "install", *DEPENDENCIES])
        return {"FINISHED"}


class HYDRIDIC_OT_import_chemical_structure(bpy.types.Operator,
                                            bpy_extras.io_utils.ImportHelper):
    """Import a chemical structure into Blender. Supports all ASE-supported formats."""

    bl_idname = "hydridic.import_chemical_structure"
    bl_label = "Import Chemical"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        chemical = utils.chemical.Chemical.from_file(self.properties.filepath, bpy.context)
        chemical.add_structure_to_scene()
        return {"FINISHED"}


classes = (HYDRIDIC_OT_install_dependencies,
           HYDRIDIC_OT_import_chemical_structure)

register, unregister = bpy.utils.register_classes_factory(classes)
