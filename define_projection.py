#
#   Define projection for every LAS file in this folder.
#

from __future__ import print_function
from glob import glob
import os
from shutil import copyfile

prj = "../GCS_WGS_1984.prj"

lasfiles = glob("2*.shp")
for lf in lasfiles:
    (f,e) = os.path.splitext(lf)
    dst = f + '.prj'
    copyfile(prj,dst)
