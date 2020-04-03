
import bpy
import os
import json
import platform

from bpy.types import Operator, AddonPreferences
from bpy.props import StringProperty, IntProperty, BoolProperty


def PBRMatLib_getJSON():
    if platform.system() is 'Windows':
        prefPath = 'C:\\ProgramData\\PBRMAT Studio\\Preferences.json'
    if os.path.exists(prefPath):
        return prefPath
    else:
        return False


def is_valid_Library(libraryPath) -> bool:
    for folderName in os.listdir(libraryPath):
        if os.path.isdir(os.path.join(libraryPath, folderName)):
            for FileName in os.listdir(os.path.join(libraryPath, folderName)):
                if os.path.isfile(os.path.join(libraryPath, folderName, FileName)) and FileName.lower().endswith(".json"):
                    with open(os.path.join(libraryPath, folderName, FileName)) as jsonfile:
                        data = json.load(jsonfile)
                        keyList = {'Name', 'Substance', 'Material', 'Tags', 'Shaders', 'Preview'}
                        if set(keyList) <= set(data):
                            return True
    return False


def rebuild_Library(libraryPath):

    matLibData = {}

    for folderName in os.listdir(libraryPath):
        if os.path.isdir(os.path.join(libraryPath, folderName)):
            for FileName in os.listdir(os.path.join(libraryPath, folderName)):
                if os.path.isfile(os.path.join(libraryPath, folderName, FileName)) and FileName.lower().endswith(".json"):
                    with open(os.path.join(libraryPath, folderName, FileName)) as jsonfile:

                        data = json.load(jsonfile)
                        keyList = {'Name', 'Substance', 'Material', 'Tags', 'Shaders', 'Preview'}

                        if set(keyList) <= set(data):
                            Name = data['Name']
                            Substance = data['Substance']
                            Material = data['Material']
                            Tags = data['Tags']
                            Shaders = data['Shaders']
                            Preview = data['Preview']

                            if not Substance in matLibData:
                                matLibData[Substance] = {}
                            if not Material in matLibData[Substance]:
                                matLibData[Substance][Material] = {}
                            if not Name in matLibData[Substance][Material]:
                                matLibData[Substance][Material][Name] = {}
                                
                            matLibData[Substance][Material][Name]['Tags'] = Tags
                            matLibData[Substance][Material][Name]['Shaders'] = Shaders
                            matLibData[Substance][Material][Name]['Preview'] = Preview

    matLibData['Library-Path'] = libraryPath

    if platform.system() is 'Windows':
        prefPath = 'C:\\ProgramData\\PBRMAT Studio'
        if not os.path.exists(prefPath):
            os.mkdir(prefPath)
    
    with open(os.path.join(prefPath, 'Preferences.json'), 'w') as jsonfile:
        json.dump(matLibData, jsonfile)

