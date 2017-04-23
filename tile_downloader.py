#!/usr/bin/env python
#
#  Using a file that tells me which images I want (Export_Output.txt),
#  generate a list of commands to download those files that don't already exist.
#
from __future__ import print_function
import sys, os

tile_file = sys.argv[1]

# sources
# baseurl = "http://marinmapims.marinmap.org/PublicRecords/data/RasterData/Orthos_CompressedSID"
# orthos in TIFF format
#baseurl = "http://www.marinmap.org/PublicRecords/data/RasterData/Ortho2014_ZIP"
# elevations
#baseurl = "http://www.marinmap.org/PublicRecords/data/rasterdata/DigitalElevation"
# lidar
baseurl = "ftp://coast.noaa.gov/pub/DigitalCoast/lidar1_z/geoid12b/data/5007"

with open(tile_file) as f:
    lines = f.readlines()
    total = len(lines)
    count = 0
    for line in lines:
      count += 1
      line = line.rstrip() # remove newline
      if not line: continue

      # input like "2014/foo.tif"
      #(path,fileext) = os.path.split(line)
      #(file,ext) = os.path.splitext(fileext)
      # file = "foo"

      # input like "foo"
      #os.path.join('2014',line + '.tif')

      (file,ext) = os.path.splitext(line)
      y = file[0:4]
      inx = file[-4:]

      basefile = "ARRA-CA_GoldenGate_%s_00%s" % (y,inx)
      lasfile = basefile + '.las' # old name scheme
      zipfile = file + '.laz' # new name scheme

      print("%d of %d : %s" % (count, total, lasfile),end="")
      if os.path.exists(lasfile):
          print(' have "%s".' % lasfile)
          os.unlink(lasfile)
#          continue
      if os.path.exists(zipfile):
          print(' have "%s".' % zipfile)
          continue

      cmd = "wget %s/%s" % (baseurl, zipfile)
      print(cmd)
      try:
          os.system(cmd)
          pass
      except Exception as e:
          print("Failed.",e)

# gdalbuildvrt 
