import sys
import webbrowser as browser
import os
from functools import partial

import maya.cmds as cmds

import Utilities.assetInfo as ai
reload(ai)
import Utilities.versionFile_v02 as vf
reload(vf)
import openSceneFile_v02 as of
reload(of)
import Utilities.utilityFunctions as uf
reload(uf)
import saveNewWindows as snw
reload(snw)


# TODO
# image?  
# right click on item to open browser at that folder

proj = ai.AssetInfo()
widgets = {}

def file_UI_create(*args):
    """
    ui
    """
    if cmds.window("fileWin", exists=True):
        cmds.deleteUI("fileWin")

    w = 740
    h = 480
    widgets["win"] = cmds.window("fileWin", t="File Manager", w=w, h=h, s=False)
    widgets["menu"] = cmds.menuBarLayout()
    widgets["menuFile"] = cmds.menu(label="Presets")
    cmds.menuItem(l='Save Layout', c=save_layout)
    cmds.menuItem(l="Delete Layout", c=delete_layout)

    cmds.setParent(widgets["win"])
    widgets["mainCLO"] = cmds.columnLayout(w=w, h=h)
    widgets["mainFLO"] = cmds.formLayout(w=w, h=h, bgc=(.2,.2,.2))

    aw = 220
    widgets["assetsFLO"] = cmds.formLayout(w=aw, h=430)
    widgets["assetsTab"] = cmds.tabLayout(w=aw,h=430, cc=change_stage_tab)
    widgets["charCLO"] = cmds.columnLayout("CHARS", w=aw, h=400)
    widgets["charTSL"] = cmds.textScrollList(w=aw, h=400)
    cmds.setParent(widgets["assetsTab"])
    widgets["propCLO"] = cmds.columnLayout("PROPS", w=aw, h=400)
    widgets["propTSL"] = cmds.textScrollList(w=aw, h=400)
    cmds.setParent(widgets["assetsTab"])
    widgets["setCLO"] = cmds.columnLayout("SETS", w=aw, h=400)
    widgets["setTSL"] = cmds.textScrollList(w=aw, h=400)
    cmds.setParent(widgets["assetsTab"])
    widgets["stageCLO"] = cmds.columnLayout("STGS", w=aw, h=400)
    widgets["stageTSL"] = cmds.textScrollList(w=aw, h=400)       
    cmds.formLayout(widgets["assetsFLO"], e=True, af = [(widgets["assetsTab"], "top", 10), (widgets["assetsTab"], "left", 0),
        ])
    
    cmds.setParent(widgets["mainFLO"])
    widgets["filesFLO"] = cmds.formLayout(w=350,h=450)

    widgets["filesTSL"] = cmds.textScrollList(w=350, h=400)
    widgets["phaseOM"] = cmds.optionMenu( label='Phase: ', changeCommand=populate_files)
    cmds.menuItem(label="Modeling")
    cmds.menuItem(label="Rigging")
    cmds.menuItem(label="Animation")
    cmds.menuItem(label="Lighting")
    cmds.menuItem(label="Texturing")
    cmds.formLayout(widgets["filesFLO"], e=True, af = [
        (widgets["filesTSL"], "top", 23), (widgets["filesTSL"], "left", 0),
        (widgets["phaseOM"], "top", 0), (widgets["phaseOM"], "left", 10)
        ])

    cmds.setParent(widgets["mainFLO"])

    widgets["openBut"] = cmds.button(l="Open Selected", w=125, h=30, bgc=(.3, .3, .3), c=open_selected)
    widgets["versionBut"] = cmds.button(l="Version Up Current", w=125, h=30, bgc=(.3, .3, .3), c=version_up)
    widgets["saveAsBut"] = cmds.button(l="Save As New File", w=125, h=30, bgc=(.3, .3, .3), c=save_as_new)
    widgets["refreshBut"] = cmds.button(l="Refresh Window", w=125, h=30, bgc=(.3, .3, .3), c=load_asset_info)


    cmds.formLayout(widgets["mainFLO"], e=True, af = [(widgets["assetsFLO"], "top", 25), (widgets["assetsFLO"], "left", 5),
        (widgets["filesFLO"], "top", 35), (widgets["filesFLO"], "left", 240),
        (widgets["openBut"], "top", 60),(widgets["openBut"], "left", 600),
        (widgets["versionBut"], "top", 110),(widgets["versionBut"], "left", 600),
        (widgets["saveAsBut"], "top", 365),(widgets["saveAsBut"], "left", 600),
        (widgets["refreshBut"], "top", 415),(widgets["refreshBut"], "left", 600),
        ])


    cmds.window(widgets["win"], e=True, w=5, h=5, rtf=True)
    cmds.showWindow(widgets["win"])

    load_asset_info()


def save_layout(*args):

    phaseValue = "{0}\n".format(cmds.optionMenu(widgets["phaseOM"], q=True, value=True))
    #stageValue = "{0}\n".format(cmds.tabLayout(widgets["assetsTab"], q=True, st=True))
    #write to file
    userDir = cmds.internalVar(upd=True) + "frogger_fileManagerLayout.txt"
    file = open(userDir, "w")

    file.write(phaseValue)
    #file.write(stageValue)

    file.close()


def load_layout(*args):
    """
    RETURNS:
        string: the value to set in the phaseOM option menu
    """
    userDir = cmds.internalVar(upd=True) + "frogger_fileManagerLayout.txt"
    if os.path.isfile(userDir):
        file = open(userDir, "r")
        values = []

        for line in file:
            values.append(line.rstrip("\n"))
        file.close()

        cmds.optionMenu(widgets["phaseOM"], e=True, value=values[0])
        # cmds.tabLayout(widgets["assetsTab"], e=True, st=values[1])
    return(values[0])


def delete_layout(*args):
    userDir = cmds.internalVar(upd=True) + "frogger_fileManagerLayout.txt"
    if os.path.isfile(userDir):
        os.remove(userDir)
        print "Deleted saved layout for fileManager"


def load_asset_info(*args):

    clear_asset_lists()

    proj = ai.AssetInfo()
    assetNames = proj.get_asset_name_list()

    for asset in assetNames[0]:
        cmds.textScrollList(widgets["charTSL"], e=True, a=asset, sc=populate_files)
    for asset in assetNames[1]:
        cmds.textScrollList(widgets["propTSL"], e=True, a=asset, sc=populate_files)
    for asset in assetNames[2]:
        cmds.textScrollList(widgets["setTSL"], e=True, a=asset, sc=populate_files)
    for asset in assetNames[3]:
        cmds.textScrollList(widgets["stageTSL"], e=True, a=asset, sc=populate_files)

    select_initial()


def select_initial(*args):
    """
    tries to select the first item in chars, if not, then props, etc. If no item, pass
    !! finish this later
    """

    # if we're in a scene with a name
    filename = cmds.file(q=True, sn=True)

    if filename:
        fileObj = uf.PathParser(filename)
        # if that scene is compatible
        if fileObj.compatible:
            # get the asset type - select the tab
            if fileObj.assetType == "Character":
                assType, assTab = "CHARS", "charTSL"
            if fileObj.assetType == "Props":
                assType, assTab = "PROPS", "propTSL"
            if fileObj.assetType == "Sets":
                assType, assTab = "SETS", "setTSL"              
            if fileObj.assetType == "Stages":
                assType, assTab = "STGS", "stageTSL"
            cmds.tabLayout(widgets["assetsTab"], e=True, st=assType)
            # get the phase - select the menu
            cmds.optionMenu(widgets["phaseOM"], e=True, value=fileObj.phase)  
            cmds.textScrollList(widgets[assTab], e=True, si=fileObj.name)
        else:
            cmds.textScrollList(widgets["charTSL"], e=True, sii=1)
    else:
        cmds.textScrollList(widgets["charTSL"], e=True, sii=1)

    populate_files()


def clear_asset_lists(*args):
    """
    clears all the asset text scroll lists
    """
    cmds.textScrollList(widgets["charTSL"], e=True, ra=True)
    cmds.textScrollList(widgets["propTSL"], e=True, ra=True)
    cmds.textScrollList(widgets["setTSL"], e=True, ra=True)
    cmds.textScrollList(widgets["stageTSL"], e=True, ra=True)


def clear_file_list(*args):
    """
    clears file text scroll list
    """
    cmds.textScrollList(widgets["filesTSL"], e=True, ra=True)


def change_stage_tab(*args):
    """
    when tab changes, just select first in the list
    """
    currTab = cmds.tabLayout(widgets["assetsTab"], q=True, st=True)
    currScene = cmds.file(q=True, sn=True)
    if currTab == "CHARS":
        tsl = "char"
    if currTab == "PROPS":
        tsl = "prop"
    if currTab == "SETS":
        tsl = "set"
    if currTab == "STGS":
        tsl = "stage"   
    if currScene:
        # try to find in the current scene
        pp = uf.PathParser(currScene)
        if pp.compatible:
            if pp.name in cmds.textScrollList(widgets["{0}TSL".format(tsl)], q=True, allItems=True):
                cmds.textScrollList(widgets["{0}TSL".format(tsl)], e=True, si=pp.name)
            else:
                cmds.textScrollList(widgets["{0}TSL".format(tsl)], e=True, sii=1)
        else:
            cmds.textScrollList(widgets["{0}TSL".format(tsl)], e=True, sii=1)
    else:
        cmds.textScrollList(widgets["{0}TSL".format(tsl)], e=True, sii=1)

    populate_files()


def populate_files(*args):
    """
    clears the file list, then populates based on the phase and the selected asset in the asset TSL
    """
    clear_file_list()
    selTab = cmds.tabLayout(widgets["assetsTab"], q=True, st=True)

    tab, phase, assetPath, assetFiles = [None, None, None, None]

    if selTab != "STGS":
        tab, phase, assetPath, assetFiles = get_asset_info()
    else:
        tab, phase, assetPath, assetFiles = get_stage_info()

    if assetFiles:
        for file in assetFiles:
            a = cmds.textScrollList(widgets["filesTSL"], e=True, a=os.path.basename(file))
    else:
        cmds.textScrollList(widgets["filesTSL"], e=True, a="No Files")

# add popmenu to the list object to go to explorer
    # cmds.popupMenu(p=widgets["filesTSL"])
    # cmds.menuItem(l="Open Folder in Explorer", c=get_path_explorer)

    # try to line up the current scene in the file list
    currFile = cmds.file(q=True, sn=True)
    if currFile:
        fileObj = uf.PathParser(currFile)
        if fileObj.compatible and (os.path.basename(currFile) in assetFiles):
            cmds.textScrollList(widgets["filesTSL"], e=True, si=os.path.basename(currFile))
    else:
        # get the last file and select that
        numItems = cmds.textScrollList(widgets["filesTSL"], q=True, ni=True)
        cmds.textScrollList(widgets["filesTSL"], e=True, sii=numItems)


def get_path_explorer(*args):
    # construct path from ui
    currTab = cmds.tabLayout(widgets["assetsTab"], q=True, st=True)
    if currTab == "CHARS":
        tsl = "char"
    if currTab == "PROPS":
        tsl = "prop"
    if currTab == "SETS":
        tsl = "set"
    if currTab == "STGS":
        tsl = "stage"

def open_explorer(path, *args):
    """takes in path and opens it in os folder"""
    if os.path.isdir(path):
        if sys.platform == "win32":
            winPath = path.replace("/", "\\")
            browser.open(winPath)
        elif sys.platform == "darwin":
            pass
        elif sys.platform == "linux" or sys.platform=="linux2":
            pass


def get_asset_info(*args):
    """
    gets info from state of the ui
    Returns:
        tab (string) - which tab is selected ("CHARS", "SETS", "PROPS")
        phase (string) - which phase we're in ("Modeling", "Rigging", etc)
        assetPath (string) - the path to the asset folder ("x://.../Assets/Character/Fish") based on above
        assetFiles (list) - list of asset file paths based on above
    """

    asset = None
    assetFiles = None
    tab = cmds.tabLayout(widgets["assetsTab"], q=True, st=True)
    phase = cmds.optionMenu(widgets["phaseOM"], q=True, value=True)

    if tab == "CHARS":
        asset = cmds.textScrollList(widgets["charTSL"], q=True, si=True)[0]
        assetPath = os.path.join(proj.charPath, asset)
    if tab == "PROPS":
        asset = cmds.textScrollList(widgets["propTSL"], q=True, si=True)[0]
        assetPath = os.path.join(proj.propPath, asset)
    if tab == "SETS":
        asset = cmds.textScrollList(widgets["setTSL"], q=True, si=True)[0]
        assetPath = os.path.join(proj.setPath, asset)

    proj.get_asset_contents(assetPath)
    if phase == "Modeling":
        assetPath = proj.mdlPath
        assetFiles = sorted(proj.mdlWorkFiles)
    if phase == "Rigging":
        assetPath = proj.rigPath
        assetFiles = sorted(proj.rigWorkFiles)
    if phase == "Animation":
        assetPath = proj.anmPath
        assetFiles = sorted(proj.anmWorkFiles)
    if phase == "Lighting":
        assetPath = proj.lgtPath
        assetFiles = sorted(proj.lgtWorkFiles)
    if phase == "Texturing":
        assetPath = proj.txtPath
        assetFiles = sorted(proj.txtWorkFiles)

    return(tab, phase, assetPath, assetFiles)


def get_stage_info(*args):
    """
    gets info from state of the ui
    Returns:
        tab (string) - which tab is selected ("CHARS", "SETS", "PROPS")
        phase (string) - which phase we're in ("Modeling", "Rigging", etc)
        assetPath (string) - the path to the asset folder ("x://.../Assets/Character/Fish") based on above
        assetFiles (list) - list of asset file paths based on above
    """
    asset = None
    assetFiles = None
    asset = cmds.textScrollList(widgets["stageTSL"], q=True, si=True)[0]
    assetPath = os.path.join(proj.stagePath, asset)  
    tab = "STGS"
    phase = "Animation"
    proj.get_stage_contents(assetPath)
    assetPath = proj.stageAnmPath
    assetFiles = proj.stageAnmWorkFiles

    return(tab, phase, assetPath, assetFiles)    


def open_selected(*args):
    # if no file then warn and skip
    selFile = cmds.textScrollList(widgets["filesTSL"], q=True, si=True)[0]
    if selFile == "No Files":
        cmds.warning("No files available to open!")
        return()

    # construct the paths
    tab, phase, assetPath, assetFiles = [None, None, None, None]
    selTab = cmds.tabLayout(widgets["assetsTab"], q=True, st=True)
    if selTab != "STGS":
        tab, phase, assetPath, assetFiles = get_asset_info()
    else:
        tab, phase, assetPath, assetFiles = get_stage_info()
    selIndex = cmds.textScrollList(widgets["filesTSL"], q=True, sii=True)[0]
    filePath = os.path.join(assetPath, assetFiles[selIndex - 1])

    # check mods, if so then. . 
    changed = cmds.file(q=True, modified=True)
    svState = True
    if changed:
        svState = save_current_dialog()

    of.run(filePath)


def save_current_dialog(*args):
    save = cmds.confirmDialog(title="Save Confirmation", message = "Save current scene?", button = ("Save", "Don't Save", "Cancel"), defaultButton = "Save", cancelButton = "Cancel", dismissString = "Cancel")
    if save == "Save":
        cmds.file(save=True)
        return(True)
    elif save == "Don't Save":
        return(True)
    else:
        return(False)


def version_up(*args):
    """
    versions the current file based on Zed's class/modules
    """
    filePath = cmds.file(q=True, sn=True)
    ver = vf.versionClass()
    ver.versionUp(filePath)

    load_asset_info()


def save_as_new(*args):

    # construct the paths
    filePath = None
    selTab = cmds.tabLayout(widgets["assetsTab"], q=True, st=True)
    if selTab != "STGS":
        tab, phase, assetPath, assetFiles = get_asset_info()
    else:
        tab, phase, assetPath, assetFiles = get_stage_info()

    selItem = None
    if cmds.textScrollList(widgets["filesTSL"], q=True, sii=True):
        selIndex = cmds.textScrollList(widgets["filesTSL"], q=True, sii=True)[0]
        selItem = cmds.textScrollList(widgets["filesTSL"], q=True, si=True)[0]
    else:
# if there is no file present, create the path based on asset and phase and "main"
        cmds.warning("You need to select either a file OR 'No Files' in the file lister on the right.")

    if not selItem or selItem == "No Files":
        if tab == "CHARS":
            asset = cmds.textScrollList(widgets["charTSL"], q=True, si=True)[0]
        if tab == "PROPS":
            asset = cmds.textScrollList(widgets["propTSL"], q=True, si=True)[0]
        if tab == "SETS":
            asset = cmds.textScrollList(widgets["setTSL"], q=True, si=True)[0]
        if tab == "STGS":
            asset = cmds.textScrollList(widgets["stageTSL"], q=True, si=True)[0]

        filename = "{0}_main_{1}_Work_v0001.mb".format(asset, phase)
        filePath = fix_path(os.path.join(assetPath, filename))

    # or use the path from selections
    else:
        filePath = fix_path(os.path.join(assetPath, assetFiles[selIndex - 1]))

    savenewdata = snw.SaveNewAssetUI(filePath)
    return()

    # if file already exists then bail out
    if os.path.isfile(filePath):
        cmds.confirmDialog(title="File Exists!", message = "This file type already exists, you should use the version up instead!", button = ("OK"))
        return()

    confirm = cmds.confirmDialog(title="Save Confirmation", message = "You are about to create:\n{0}\n\nShould we continue?".format(filePath), button = ("Create", "Cancel"), defaultButton = "Save", cancelButton = "Cancel", dismissString = "Cancel", bgc = (.6, .5, .5))
    if confirm == "Create":
        write=True
    else:
        write=False

    if write:
        ver = vf.versionClass()
        ver.versionUp(filePath)

    populate_files()


def fix_path(path, *args):
    newPath = path.replace("\\", "/")
    return(newPath)


def fileManager(*args):
    file_UI_create()