import maya.cmds as mc
import maya.mel as mel

#import utility fuctions
import Utilities.projectGlobals as pg

from functools import partial
import os 

import openSceneFile_v02 as osf
import saveSceneVersion_v02 as ssv
import saveSceneAsVersion_v02 as sav
import fileManager_v06 as fileMgr
import assetManager as assMgr
import Publishing.AssetPublish_v06 as assPub
import updateAllReferences as upd
import Publishing.multiRefAnimExport_v07 as mre
import setProject as sp

#import anim tools
import Publishing.zbRigExport as zbre
import Publishing.zbRigExport_Cm as zbre_cm
import Publishing.zbRigExport_Meters as zbre_meters
import Publishing.zbRigExport_singleFrame as zbresf
import Anim.zb_spaceMatching as zbsm

#import rigging tools
import importTemplate_v01 as it

#set UI version
global uiVersion
uiVersion=1.0

#main menu building function
def Menu(*args, **kwargs):
    #project prefix for unique UI names and basic naming variables
    proj=pg.project
    menuName="%s Menu"%proj
    pMainMenu="%s_MainMenu"%proj

    MainMayaWindow=mel.eval("$tempVar=$gMainWindow")

    if mc.menu(pMainMenu, q=1, ex=1):
        mc.deleteUI(pMainMenu)
    else:
        pass

    #build menu to main menu
    mc.menu(pMainMenu, to=1, l=menuName, p=MainMayaWindow)
    mc.menuItem(l="Refresh", c=rebuild, p=pMainMenu)

    #pipeline tools submenu
    pPipelineMenu=mc.menuItem(sm=1, l="Pipeline Tools", p=pMainMenu)
    mc.menuItem(l="Change Project", c=setProject, p=pPipelineMenu)    
    mc.menuItem(l="File Manager", c=fileManager, p=pPipelineMenu)
    mc.menuItem(l="Asset Manager", c=assetManager, p=pPipelineMenu)
    mc.menuItem(l="Update All References", c=updateRefs, p=pPipelineMenu)
    mc.menuItem(l="Version Up Current", c=saveVersion, p=pPipelineMenu)
    mc.menuItem(l="Asset Publish And Version Up", c=partial(assPublishVersion, True), p=pPipelineMenu)
    mc.menuItem(l="Asset Publish Don't Version Up", c=partial(assPublishVersion, False), p=pPipelineMenu)
    mc.menuItem(l="Stage Publish (multi reference)", c=partial(stagePublish, False), p=pPipelineMenu)

    #anim tools submenu
    animMenu=mc.menuItem(sm=1, l="Anim Tools", p=pMainMenu)
    mc.menuItem(l="Space Matching", c=spaceMatching, p=animMenu)

    #rigging tools submenu
    riggingMenu=mc.menuItem(sm=1, l="Rigging Tools", p=pMainMenu)
    mc.menuItem(l="Import Template", c=importTemplate, p=riggingMenu)

    #lookDev tools submenu
    lookdevMenu=mc.menuItem(sm=1, l="Look Dev Tools", p=pMainMenu)
    mc.menuItem(l="Collect Textures", c=collectTextures, p=lookdevMenu)

    # run project setter
    os.environ["MAYA_PROJECT_PATH"] = "X:/Production"
    os.environ["MAYA_CURRENT_PROJECT"] = "Frogger"
    # set project window
    sp.setProject()

#assembly functions for menu buttons
    
def rebuild(*args, **kwargs):
    print "----- REBUILDING FROGGER MENU v%s -----"%uiVersion
    import FroggerMenu_v01 as fm
    reload(fm)
    fm.Menu()

#PIPELINE MENU ITEMS#===========================================================
def setProject(*args):
    reload(sp)
    sp.setProject()

def openFile(*args, **kwargs):
    reload(osf)
    osf.run()

def saveVersion(*args, **kwargs):
    reload(ssv)
    ssv.run()

def saveAsVersion(*args, **kwargs):
    reload(sav)
    sav.run()

def assPublishVersion(versionUp, *args, **kwargs):
    reload(assPub)
    assPub.assetPublish(versionUp)

def stagePublish(versionUp, *args):
    reload(mre)
    mre.stagePublish(versionUp)

def fileManager(*args):
    reload(fileMgr)
    fileMgr.fileManager()

def assetManager(*args):
    reload(assMgr)
    assMgr.assetManager()

def updateRefs(*args):
    reload(upd)
    upd.update_all_references()

#ANIM MENU ITEMS#=================================================================
def exportAnimFBX(*args, **kwargs):
    reload(zbre)
    export=zbre.rigExport()
    export.run()

def exportAnimFBX_Cm(*args, **kwargs):
    reload(zbre_cm)
    export=zbre_cm.rigExport()
    export.run()

def exportAnimFBX_Meters(*args, **kwargs):
    reload(zbre_meters)
    export=zbre_meters.rigExport()
    export.run()

def exportPoseFBX(*args, **kwargs):
    reload(zbresf)
    exportsf=zbresf.rigExport()
    exportsf.run()

def spaceMatching(*args, **kwargs):
    reload(zbsm)
    zbsm.uiWindow()

#RIGGING MENU ITEMS#===============================================================
def importTemplate(*args, **kwargs):
    reload(it)
    it.run()

#LOOK DEV MENU ITEMS#======================================================
def collectTextures(*args, **kwargs):
    mel.eval('source "X:/Production/Code/Maya/Scripts/Mel/collectTextures.mel";')
    mel.eval("collectTextures;")