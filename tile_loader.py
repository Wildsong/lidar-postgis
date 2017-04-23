#!/usr/bin/env python
#
#  Load LAS data into PostGIS
#
from __future__ import print_function
import os

def las_load_file(lasfile):
    """ Use las2ogr to load a point cloud into PostGIS """
   
    # TODO define database connection, potentially I need user,passwd,hostname,port,database,schema

    dst = 'PG:"user=postgres dbname=ca2010_arra_goldengate"'

    # TODO use subprocess and watch return code

    cmd = "las2ogr -i %s -o %s -f PostgreSQL" % (src,dst)
    os.system(cmd)

    # TODO define projection by talking to PostGIS.

    return

def las_load(lasfiles):
    count = 0
    total = len(lasfiles)
    for src in lasfiles:
        count += 1
        # TODO Might want to use logger here.
        # TODO Be nice to collect some stats here since this is slow process.
        print("LAS to PG on %d of %d." % (count, total))
        las_load_file(src)
    return

if __name__ == '__main__':

    # TODO accept a list of LAS files instead of globbing
    
    from glob import glob
    las_load(glob("*.las"))

    exit(0)
