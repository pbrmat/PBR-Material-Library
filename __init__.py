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

from bpy.types import Operator, AddonPreferences
from bpy.props import StringProperty, IntProperty, BoolProperty
from . import (
    ui,
    utils
)


class PBRMatLib_AddonUI(AddonPreferences):
    bl_idname = __name__

    filepath: StringProperty(
        name="PBR Material Library Path",
        subtype='DIR_PATH',
    )

    def draw(self, context):
        layout = self.layout
        layout.label(text="This is a preferences view for our add-on")
        layout.prop(self, "filepath")

        preferences = context.preferences
        addon_prefs = preferences.addons[__name__].preferences
        libPath = addon_prefs.filepath

        addonSettings = 'C:\\ProgramData\\PBRMAT Studio\\Preferences.json'
        
        if os.path.exists(addonSettings) and os.path.exists(libPath):
            with open(addonSettings) as jsonfile:
                data = json.load(jsonfile)
        else:
            data = {}
            # ---------------------------------------------------------
            # Write some code Here, to Rebuild Monifest.json ----------
            # ---------------------------------------------------------
                    
        data['Library-Path'] = libPath
        
        with open(addonSettings, 'w') as jsonfile:
            json.dump(data, jsonfile)


def register():
    bpy.utils.register_class(PBRMatLib_AddonUI)
    ui.register()
    utils.register()


def unregister():
    bpy.utils.unregister_class(PBRMatLib_AddonUI)
    ui.unregister()
    utils.unregister()
