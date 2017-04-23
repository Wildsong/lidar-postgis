#!/usr/bin/env python
#
#  Build a DEM from LAS files using PostGIS
#
from __future__ import print_function
from glob import glob
import os
from shutil import copyfile

def las_load(lasfiles):
    """ Use las2ogr to load the entire point cloud into PostGIS """

    count = 0
    total = len(lasfiles)
    for src in lasfiles:
        count += 1
        print("LAS to PG on %d of %d." % (count, total))
        # convert las to points
        dst = 'PG:"user=postgres dbname=ca2010_arra_goldengate"'
        cmd = "las2ogr -i %s -o %s -f PostgreSQL" % (src,dst)
        os.system(cmd)

las_load(glob("2*.las"))

exit(0)

# Selecting asprsclass=00000010 should be "class=bare earth".

# Building the final raster using a guess at a smoothing algorithm

src = "all.vrt"
dst = "bare_earth.tif"
print("VRT(%s) to DEM(%s) This will take a long time." % (src,dst))
cmd = "gdal_grid -a invdist:power=2.0:smoothing=1.0 -where \"asprsclass='00000010'\" %s %s" % (src,dst)
print(cmd)
#os.system(cmd)


