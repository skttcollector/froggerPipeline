import maya.cmds as cmds

import os
from functools import partial

widgets = {}

def set_project_UI(*args):
	if cmds.window("setProjectWin", exists=True):
		cmds.deleteUI("setProjectWin")

	widgets["win"] = cmds.window("setProjectWin", t="Set Project", w=200, h=100)
	widgets["mainCLO"] = cmds.columnLayout(w=300, h=200)
	cmds.text("Click the project you'll be working in", al="left")
	cmds.separator(h=10)
	widgets["frog"] = cmds.button(l="OutOfBoxExperience Project", w=300, h=40, bgc=(.7, .7, .5), c=partial(set_project_env_variables, "OutOfBoxExperience"))
	widgets["fit"] = cmds.button(l="FitAndSetup Project", w=300, h=40, bgc=(.5, .7, .7), c=partial(set_project_env_variables, "FitAndSetup"))

	cmds.window(widgets["win"], e=True, w=5, h=5, rtf=True)
	cmds.showWindow(widgets["win"])


def set_project_env_variables(proj = None, *args):
	"""
	sets two environment variables: MAYA_CURRENT_PROJECT and MAYA_PROJ_PATH, which we'll use in doing some pipeline stuff
	ARGS:
		proj (string) - the shortcut for the project we're using. Currently only "frog" and "fit", which stand for OutOfBoxExperience and FitAndSetup

	"""
	if not proj:
		return()

	currProj = None
	projPath = None

	if proj == "OutOfBoxExperience":
		currProj = "OutOfBoxExperience"
		projPath = "X:/Production"
	if proj == "FitAndSetup":
		currProj = "FitAndSetup"
		projPath = "Y:/Production"

	os.environ["MAYA_CURRENT_PROJECT"] = currProj
	os.environ["MAYA_PROJECT_PATH"] = projPath

	cmds.warning("Set current project (MAYA_CURRENT_PROJECT env var) to {0}\nSet current project path (MAYA_PROJECT_PATH env var) to {1} ".format(currProj, projPath))

	if cmds.window("setProjectWin", exists=True):
		cmds.deleteUI(widgets["win"])

	if cmds.window("fileWin", exists=True):
		cmds.deleteUI("fileWin")


def setProject(*args):
	set_project_UI()


