"""
File containing classes related to addon preferences
"""
import importlib, sys, subprocess


import bpy


class HYDRIDIC_install_dependencies(bpy.types.Operator):
    """
    Handles installing Python packages necessary for the addon to run.

    It does this by checking if all of the packages specified in the "dependencies"
    class attribute are installed. If any are missing, pip tries to install them.

    The user accesses this operator via the addon preferences menu.
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

    def execute(self, context: bpy.types.Context):
        subprocess.call([sys.executable, "-m", "pip", "install", *self.dependencies])
        return {"FINISHED"}


class HYDRIDIC_preferences(bpy.types.AddonPreferences):
    """
    Preferences menu, giving the user a button to install the dependencies.
    """

    bl_idname = __name__

    def draw(self, context: bpy.types.Context) -> None:
        layout = self.layout
        layout.operator(HYDRIDIC_install_dependencies.bl_idname, icon="CONSOLE")


classes = (HYDRIDIC_preferences,)

register, unregister = bpy.utils.register_classes_factory(classes)

if __name__ == "__main__":
    register()
