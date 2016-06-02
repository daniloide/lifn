#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Este archivo sincroniza la fuente de la aplicación con el
de la raiz de web2py. Se ejecuta desde el propio directorio,
es decir: app/scrips/este_script.py

Mi árbol:
 src: workspace/app_source
 web2py: workspace/web2py_tree
"""

import os
import re
import sys
import time
import commands

THIS_APP_DIR = os.path.abspath("../.")
WEB2PY_APP_DIR  = os.path.abspath("../../web2py/applications")
# Carpetas que NO queremos copiar..
EXCLUDE_SYNC_SUB_DIRS = [
    '.git',
    'backup',
    'export',
    'kml',
    'scripts',
    'tests',
    'uploads',
    'xml',
]

excl = ""
for d in EXCLUDE_SYNC_SUB_DIRS:
    excl += "--exclude %s " % d

print '\nrsync with web2py:\n'
## No delete: --delete 
rsyncCommand = "rsync -a --progress --stats -l -z -v -r -p %s %s %s" % (excl, THIS_APP_DIR, WEB2PY_APP_DIR)
[status,output]=commands.getstatusoutput(rsyncCommand)
print "%s" % rsyncCommand