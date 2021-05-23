import bpy
from typing import Set
import importlib, sys, subprocess

from . import auto_load

bl_info = {
    "name": "Hydridic Blender",
    "author": "James Dean",
    "description": "Import and manipulate molecules, crystals, and other chemical species in an efficient manner",
    "blender": (2, 80, 0),
    "version": (0, 1, 0),
    "location": "File -> Import -> Chemical",
    "warning": "",
    "tracker_url": "https://github.com/AcylSilane/hydridic_blender/issues",
    "category": "Import-Export",
}

auto_load.init()


class HYDRIDIC_install_dependencies(bpy.types.Operator):
    """
    Handles installing Python packages necessary for this to run.
    """

    dependencies = ("ase",)

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
        return all(
            importlib.util.find_spec(dependency) for dependency in cls.dependencies
        )

    @classmethod
    def poll(self, context: bpy.types.Context) -> bool:
        return not self.dependencies_installed()

    def execute(self, context: bpy.types.Context) -> Set:
        subprocess.call([sys.executable, "-m", "pip", "install", *self.dependencies])
        return {"FINISHED"}


class HYDRIDIC_preferences(bpy.types.AddonPreferences):
    """
    Preferences pane, giving the user a button to install the dependencies.
    """

    bl_idname = __name__

    def draw(self, context: bpy.types.Context) -> None:
        layout = self.layout
        layout.operator(HYDRIDIC_install_dependencies.bl_idname, icon="CONSOLE")


def register():
    for item in (HYDRIDIC_install_dependencies, HYDRIDIC_preferences):
        bpy.utils.register_class(item)

    auto_load.register()


def unregister():
    for item in (HYDRIDIC_install_dependencies, HYDRIDIC_preferences):
        bpy.utils.unregister_class(item)

    auto_load.unregister()
