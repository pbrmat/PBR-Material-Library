
bl_info = {
    "name": "PBR Material Library",
    "author": "PBRMAT Studio",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > UI > PBRMAT Studio > PBR Material Library",
    "description": "A Powerful PBR Material Library. Powered by PBRMAT Studio",
    "warning": "",
    "tracker_url": "https://www.pbrmat.com/index.php?route=information/contact",
    "wiki_url": "https://www.pbrmat.com/pbr-material-library",
    "category": "Material",
    "support": "OFFICIAL"
}

import bpy
import os
import json
import platform

from bpy.types import Operator, AddonPreferences
from bpy.props import StringProperty, IntProperty, BoolProperty

from . import utils


class PBRMatLib_AddonUI(AddonPreferences):
    bl_idname = __name__

    filepath: StringProperty(
        name="Library Path",
        subtype='DIR_PATH',
    )

    def draw(self, context):
        layout = self.layout
        layout.label(text="This is a preferences view for our add-on")
        layout.prop(self, "filepath")
    
        preferences = context.preferences
        addon_prefs = preferences.addons[__name__].preferences
        libPath = addon_prefs.filepath
        
        if libPath.endswith("\\"):
            libPath = libPath[:-1]
        
        if os.path.exists(libPath) and is_valid_Library(libPath):
            rebuild_Library(libPath)
        else:
            if PBRMatLib_getJSON():
                os.remove(PBRMatLib_getJSON())


class PBRMatLib_PanelUI(bpy.types.Panel):
    bl_label = 'PBR Material Library'
    bl_idname = 'PBRMatLib_Ob_PanelUI'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'PBRMAT Studio'

    def draw(self, context):
        
        layout = self.layout
        wm = context.window_manager

        if PBRMatLib_getJSON():
            self.layout.label(text="Main Panel")
        else:
            self.layout.label(text="Download Panel")


def register():
    bpy.utils.register_class(PBRMatLib_AddonUI)
    bpy.utils.register_class(PBRMatLib_PanelUI)


def unregister():
    if PBRMatLib_getJSON():
        os.remove(PBRMatLib_getJSON())
    bpy.utils.unregister_class(PBRMatLib_AddonUI)
    bpy.utils.unregister_class(PBRMatLib_PanelUI)