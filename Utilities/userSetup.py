import maya.cmds as mc
import maya.mel as mel
import sys
import setProject as sp

pipelineTools=r"\\caddy\work\current\FROGGER_MAGFL-N400\Frogger\Production\Code\Maya\Tools\PipelineTools\Python"
projectScripts=r"\\caddy\work\current\FROGGER_MAGFL-N400\Frogger\Production\Code\Maya\Scripts\Python"
riggingTools=r"\\caddy\work\current\FROGGER_MAGFL-N400\Frogger\Production\Code\Maya\Tools\RiggingTools\Python"

if pipelineTools not in sys.path:
    sys.path.insert(0, pipelineTools)
if projectScripts not in sys.path:
    sys.path.insert(0, projectScripts)
if riggingTools not in sys.path:
    sys.path.insert(0, riggingTools)
    
#build frogger project menu
def buildFrogger(*args, **kwargs):
    import FroggerMenu_v01 as fm
    reload(fm)
    fm.Menu()

try:
    mc.evalDeferred("buildFrogger()")
except:
    print "\n-----FROGGER MENU FAILED TO LOAD-----\n"