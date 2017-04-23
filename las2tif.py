#!/usr/bin/env python
#
#  Batch convert LAS files to SHP files.
#  This is dead code pretty much,
#  just left around for posterity.
#
from __future__ import print_function
from glob import glob
import os
from shutil import copyfile

prj = "GCS_WGS_1984.prj"

# Create combined shapefiles

lasfiles = glob("*.las")
todo = []
for src in lasfiles:
    (f,e) = os.path.splitext(src)
    dst = f + '.shp'
    if os.path.exists(dst):
        print("Have '%s' already." % dst)
    else:
        todo.append((src,dst))

count = 0
total = len(todo)
for src,dst in todo:
    count += 1
    print("LAS to SHP on %d of %d." % (count, total))
    # convert las to points
    cmd = "las2ogr -i %s -o %s" % (src,dst)
    os.system(cmd)
    # define projection
    copyfile(prj,dst)
del todo

# Selecting asprsclass=00000010 should be "class=bare earth".
# Smoothing laps over the edges of each tile
# so for it to work I have to use a mosaic instead

print("Merge point data.")

# Building the final raster using a guess at a smoothing algorithm

src = "all.vrt"
dst = "bare_earth.tif"
print("VRT(%s) to DEM(%s) This will take a long time." % (src,dst))
cmd = "gdal_grid -a invdist:power=2.0:smoothing=1.0 -where \"asprsclass='00000010'\" %s %s" % (src,dst)
print(cmd)
#os.system(cmd)


