#Open scene file and set project based on file selection
import maya.cmds as mc
import maya.mel as mel
import os

import Utilities.projectGlobals as pg
import Utilities.getFilePath_v01 as gfp

reload(pg)
reload(gfp)

#main execution fuction
def run(*args, **kwargs):
    #required scenes folder
    folder=pg.filefolder
    
    #run file dialog query 1=open file
    path=gfp.getFilePath(1)
    
    if path:
        #derive new workspace from selected file path
        if "/%s/"%folder in path:
            workspace=path.split(folder)[0]
        else:
            workspace="/".join(path.split("/")[:-2])
        #try to list subdirectories
        subDir=[]
        try:
            subDir=os.listdir(workspace)
        except:
            mc.warning("%s is not valid file directory"%workspace)
        #check for required file
        if folder not in subDir:
            mc.confirmDialog(m="Selected File Not In Project Directory. Please Save Version Into Project Directory.", b="Ok")
        else:
            #open selected file
            print "SETTING PROJECT: %s"%workspace
            mc.workspace(workspace, o=1)
            mc.workspace(dir=workspace)

        #check if scene has been modified
        if mc.file(q=1, modified=1):
            confirm=mc.confirmDialog(t="Save Scene?", m="Save Changes?", b=['Yes','No','Cancel'], db="Yes", ds="Dismissed", cb="Cancel")
            if confirm=="Yes":
                mc.SaveScene()
                mc.file(path, o=1, iv=1)
            elif confirm=="No":
                mc.file(path, o=1, f=1, iv=1)
            else:
                print "Nothing Saved"
        else:
            #open selected file if it exists
            if mc.file(path, q=1, ex=1):
                mc.file(path, o=1, iv=1)
                #enable autosave on scene open
                setAutoSave()
            else:
                pass
    else:
        pass

    """
    #debug printing
    print "FILE PATH: %s"%path
    print "WORKSPACE: %s"%workspace
    """

def setAutoSave(*args, **kwargs):
    #set up autosave in username subfolder
    currentWorkspace=mc.workspace(q=1, dir=1)
    localUser=mel.eval("getenv userName")
    autosavePath="%s%s/autosave/%s"%(currentWorkspace, pg.filefolder, localUser)
    mc.autoSave(en=1, int=300, lim=1, max=3, dst=1, fol=autosavePath)
    print "AUTOSAVE SET TO: %s"%autosavePath