"""
Blender operator classes are in this file
"""
import sys
import subprocess
import importlib

import bpy, bpy_extras

import utils

DEPENDENCIES = ("ase", )


class HYDRIDIC_OT_install_dependencies(bpy.types.Operator):
    """
    Handles installing Python packages necessary for the addon to run.

    It does this by checking if all of the packages specified in the "dependencies"
    class attribute are installed. If any are missing, pip tries to install them.

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
        return all(
            importlib.util.find_spec(dependency)
            for dependency in DEPENDENCIES)

    @classmethod
    def poll(self, context: bpy.types.Context) -> bool:
        return not self.dependencies_installed()

    def execute(self, context: bpy.types.Context):
        subprocess.call(
            [sys.executable, "-m", "pip", "install", *DEPENDENCIES])
        return {"FINISHED"}


class HYDRIDIC_OT_import_chemical_structure(bpy.types.Operator,
                                            bpy_extras.io_utils.ImportHelper):
    """Import a chemical structure into Blender. Supports all ASE-supported formats."""

    bl_idname = "hydridic.import_chemical_structure"
    bl_label = "Import Chemical"

    @classmethod
    def poll(self, context):
        return True

    def execute(self, context):
        chemical = utils.Chemical.from_file(self.properties.filepath, bpy.context)
        chemical.add_structure_to_scene()
        return {"FINISHED"}


classes = (HYDRIDIC_OT_install_dependencies,
           HYDRIDIC_OT_import_chemical_structure)

register, unregister = bpy.utils.register_classes_factory(classes)
