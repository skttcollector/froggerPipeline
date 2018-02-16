#save file with automatic versioning
import maya.cmds as mc
import os

import maya.cmds as mc
import os

import Utilities.versionFile_v02 as vf
import Utilities.getFilePath_v01 as gfp
reload(vf)
reload(gfp)
ver=vf.versionClass()

def run(*args, **kwargs):
    #0=save file for the get file fucntion
    filePath=gfp.getFilePath(0)
    if mc.file(filePath, q=1, ex=1):
        ver.versionUp(filePath)
    else:
        mc.file(rn=filePath)
        mc.file(s=1,f=1)