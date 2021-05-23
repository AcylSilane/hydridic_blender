import bpy
import bpy_extras

import os
import sys
import subprocess
import importlib

sys.path.append(os.path.dirname(__file__))

bl_info = {
    "name": "Hydridic Blender",
    "author": "James Dean",
    "description": "Import and manipulate molecules, crystals, and other chemical species in an efficient manner",
    "blender": (2, 80, 0),
    "version": (0, 1, 0),
    "location": "File > Import > Chemical Structure",
    "warning": "",
    "tracker_url": "https://github.com/AcylSilane/hydridic_blender/issues",
    "category": "Import-Export",
}

# =================
# Addon Preferences

# For some reason, the only way to get the "Install Dependencies" button to show up on the
# preferences menu is to inline it here. Definining the install_dependencies and preferences
# classes in a separate file and importing them is not enough. They *have* to be defined in
# here for them to register.
#
# An alternative I explored here was defining them in a separate file, importing them (for the
# benefit of my IDE's linter), and then running exec on the file they were originally defined
# in. My aversion to exec exceeds my aversion to defining random things in a package's __init__.

DEPENDENCIES = ("ase",)


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
        " with elevated permissions."
    )
    bl_options = {"REGISTER", "INTERNAL"}

    @classmethod
    def dependencies_installed(cls) -> bool:
        return all(importlib.util.find_spec(dependency) for dependency in DEPENDENCIES)

    @classmethod
    def poll(self, context: bpy.types.Context) -> bool:
        return not self.dependencies_installed()

    def execute(self, context: bpy.types.Context):
        subprocess.call([sys.executable, "-m", "pip", "install", *DEPENDENCIES])
        return {"FINISHED"}


class HYDRIDIC_UL_preferences(bpy.types.AddonPreferences):
    """
    Preferences menu, giving the user a button to install the dependencies.
    """

    bl_idname = __name__

    def draw(self, context: bpy.types.Context) -> None:
        layout = self.layout
        layout.operator(HYDRIDIC_OT_install_dependencies.bl_idname, icon="CONSOLE")


classes = (HYDRIDIC_OT_install_dependencies, HYDRIDIC_UL_preferences)

# ==============
# Menu Functions


class HYDRIDIC_OT_import_chemical_structure(
    bpy.types.Operator, bpy_extras.io_utils.ImportHelper
):
    """Import a chemical structure into Blender. Supports all ASE-supported formats."""

    bl_idname = "hydridic.import_chemical_structure"
    bl_label = "Import Chemical"

    filename_ext = ".xyz"

    @classmethod
    def poll(self, context):
        return True

    def execute(self, context):
        print(self.properties.filepath)
        return {"FINISHED"}


classes += (HYDRIDIC_OT_import_chemical_structure,)


def menu_func_import(self, context):
    layout = self.layout
    layout.operator(
        HYDRIDIC_OT_import_chemical_structure.bl_idname, text="Chemical Structure"
    )


# =======================
# Register those classes!


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)
