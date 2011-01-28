#!/usr/bin/env python

import os
import sys
import subprocess
import shutil

pwd = os.getcwd()
vedir = os.path.join(pwd,"ve")

#if os.path.exists(vedir):
#    shutil.rmtree(vedir)
#
#subprocess.call(['virtualenv', vedir])
#subprocess.call(["pip","install",
#                 "-E", os.path.join(pwd,"ve"),
#                 "--requirement", os.path.join(pwd,"req.txt")])
subprocess.call(["pip","install", '-U',
                 "-E", os.path.join(pwd,"ve"),
                 "-e", '../../'])
