import bpy

import os, sys

sys.path.append(os.path.dirname(__file__))

import addon_prefs
from addon_prefs import HYDRIDIC_preferences, HYDRIDIC_install_dependencies

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

# TODO: It is utterly ridiculous that exec is the only way to get Blender to actually register the contents of this module...
for module in (addon_prefs,):
    with open(module.__file__, "r") as inp:
        contents = inp.read()
        exec(contents)


classes = (HYDRIDIC_install_dependencies, HYDRIDIC_preferences)

def register():
    for cls in classes:
      bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
      bpy.utils.unregister_class(cls)