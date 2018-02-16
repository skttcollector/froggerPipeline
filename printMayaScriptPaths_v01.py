import maya.cmds as mc
import os

def run(*args, **kwargs):
	env="MAYA_SCRIPT_PATH"
	print "Printing %s Paths..."%env
	print "-----------"
	for i in os.environ.get(env).split(";"):
		print i