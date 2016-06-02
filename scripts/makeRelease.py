#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Append gluon to path
import sys
import os
# Must be valid web2py path!!!
HOME = os.path.expanduser("~")
WEB2PY_PATH=os.path.join( HOME, "workspace", "web2py" )
sys.path.insert(0, WEB2PY_PATH)

from gluon.admin import *

class dummy(object):
    """Dummy class for emulate request: request.folder
    """
    pass

class MakeRelease(object):
    """Utilities for compile, clean and pack web2py app
    """
    def __init__(self, appName, purge=True):
        self.appName = appName
        self.purge = purge
        request = dummy()
        request.folder = "%s/applications/%s" % (WEB2PY_PATH, appName)
        self.request = request
        # Standard
        self.cleanApp()
        self.deleteDatabaseDef()
        self.compileApp()
        self.packageCompiledApp()

    def cleanApp(self):
        # Delete session, cache and errors
        app_cleanup(self.appName, self.request)

    def compileApp(self):
        app_compile(self.appName, self.request)

    def packageCompiledApp(self):
        app_pack_compiled(self.appName, self.request)

    def packageApp(self):
        app_pack(self.appName, self.request)

    def __cleanOthersDir__(self, dirName):
        import os
        if dirName=="/":
            return
        print("Deleteing: %s" % dirName)
        for root, dirs, files in os.walk(dirName, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))

    def deleteDatabaseDef(self):
        self.__cleanOthersDir__( dirName=os.path.join(WEB2PY_PATH, "applications", self.appName,"databases") )


if __name__ == "__main__":
    mr = MakeRelease('lifn')

