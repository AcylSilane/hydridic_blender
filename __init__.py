import bpy

import os, sys

sys.path.append(os.path.dirname(__file__))

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

classes = []

# =================
# Addon Preferences

# The below code is gross. Because it uses exec.
# Why am I doing this? Because the blender addon API appears to be broken for the addon prefs screen.
# This is the only way I could get the "install dependencies" button to work.
# Specifically, none of the following result in the presence of the "Install Dependencies" button:
#     - The "register_module" helper functions were removed after 2.80
#     - Creating register/unregister functions via the bpy.utils.register_class_factory() method
#         at the module level, and running them inside of __init__'s register() function
#     - Directly importing the classes inside addon_prefs, and registering them inside __init__.py.
#
# For some unknown reason, the only way I can get the button to show up, is to run exec on thing I
# want to import. One thing I am not going to do is shove all of these class definitions into __init__
# to create a file that's several hundred lines long.
#
# TODO: There has to be a better way to register these classes than running import+exec

import addon_prefs  # Needed to get the module's __file__
from addon_prefs import (
    HYDRIDIC_OT_install_dependencies,
    HYDRIDIC_UL_preferences,
)  # Needed for linting

with open(addon_prefs.__file__, "r") as inp:
    exec(inp.read())
classes += (HYDRIDIC_UL_preferences, HYDRIDIC_OT_install_dependencies)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
