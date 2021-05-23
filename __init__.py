# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name": "Hydrogen-Blender",
    "author": "James Dean",
    "description": "Import and manipulate molecules, crystals, and other chemical species in an efficient manner",
    "blender": (2, 80, 0),
    "version": (0, 1, 0),
    "location": "File -> Import -> Chemical",
    "warning": "",
    "tracker_url": "https://github.com/AcylSilane/hydrogen_blender/issues",
    "category": "Import-Export",
}

import bpy
from typing import Set
from . import auto_load

auto_load.init()

dependencies = ("ASE",)


class HYDROGEN_install_dependencies(bpy.types.Operator):
    """
    Handles installing Python packages necessary for this to run.
    """

    bl_idname = "hydrogen.install_dependencies"
    bl_label = "Install Dependencies"
    bl_description = (
        "Downloads and installs packages required for this add-on to work."
        " An internet connection is required, and Blender may need to run"
        " with elevated permissions."
    )
    bl_options = {"REGISTER", "INTERNAL"}

    @staticmethod
    def dependencies_installed() -> bool:
        return False

    @classmethod
    def poll(self, context: bpy.types.Context) -> bool:
        return not self.dependencies_installed()

    def execute(self, context: bpy.types.Context) -> Set:
        print("Button Pressed")
        return {"FINISHED"}


class HYDROGEN_preferences(bpy.types.AddonPreferences):
    """
    Preferences pane, giving the user a button to install the dependencies.
    """

    bl_idname = __name__

    def draw(self, context: bpy.types.Context) -> None:
        layout = self.layout
        layout.operator(HYDROGEN_install_dependencies.bl_idname, icon="CONSOLE")


def register():
    for item in (HYDROGEN_install_dependencies, HYDROGEN_preferences):
        bpy.utils.register_class(item)

    auto_load.register()


def unregister():
    for item in (HYDROGEN_install_dependencies, HYDROGEN_preferences):
        bpy.utils.unregister_class(item)

    auto_load.unregister()
