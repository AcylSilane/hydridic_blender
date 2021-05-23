import bpy

import os
import sys

sys.path.append(os.path.dirname(__file__))

import operators

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


class HYDRIDIC_UL_preferences(bpy.types.AddonPreferences):
    """
    Preferences menu, giving the user a button to install the dependencies.
    """

    bl_idname = __name__

    def draw(self, context: bpy.types.Context) -> None:
        layout = self.layout
        layout.operator(
            operators.HYDRIDIC_OT_install_dependencies.bl_idname, icon="CONSOLE"
        )


# ==============
# Menu Functions


def menu_func_import(self, context):
    layout = self.layout
    layout.operator(
        operators.HYDRIDIC_OT_import_chemical_structure.bl_idname,
        text="Chemical Structure",
    )


# =======================
# Register those classes!

classes = (HYDRIDIC_UL_preferences,)
modules = (operators,)


def register():
    for module in modules:
        module.register()
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)


def unregister():
    for module in modules:
        module.unregister()
    for cls in classes:
        bpy.utils.unregister_class(cls)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)
