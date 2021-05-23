import bpy
from . import ui

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

def register():
    for item in (ui.settings.HYDRIDIC_install_dependencies,
                 ui.settings.HYDRIDIC_preferences):
        bpy.utils.register_class(item)


def unregister():
    for item in (ui.settings.HYDRIDIC_install_dependencies,
                 ui.settings.HYDRIDIC_preferences):
        bpy.utils.unregister_class(item)
