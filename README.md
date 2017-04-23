# lidar-postgis

Import a collection of LiDAR LAZ files into PostGIS as a point cloud.

This project is in a very early stage of development. NOTHING is done yet.

# Import workflow

Figure out where to get your data. Currently I am using data from the NOAA coastal program, specifically using
data from a "Golden Gate" program that collected all of Marin county. It's called "ca2010_ARRA_goldengate"
so I will be using that as the name of the schema. (Except converted to lower case because that's easier in PostGIS.)

https://coast.noaa.gov/htdata/lidar1_z/geoid12b/data/5007/

https://coast.noaa.gov/htdata/lidar1_z/geoid12b/data/5007/supplemental/ca2010_arra_goldengate_m5007_surveyreport.pdf

Figure out what tiles you need. I do this by laying the tile index onto a map and selecting tiles in my study area.
Then I export the selected features to a table and use it in the next step.

Download tiles as LAZ files. See downloader.py

Uncompress the tiles. (.laz -> .las)

Create PostGIS database. I keep all my GIS data in one database so normally this is already done.

Create the schema for this LiDAR dataset.  I keep separate schemas to
organize the data within the database.

Load the tile index shapefile into the schema under the name 'tile_index'.
This is just to keep it around with the rest of the data. Might be useful...

Convert each LAS file into a set of xyz points and load the point data into
the PostGIS server.  This is done in one step using las2ogr using the
tile_loader.py script.

Define the SRS, make sure you know what spatial reference system (SRS)
was used for your LiDAR data, for me it's GCS (unprojected
latlon). You will have to define the SRS when you move from LAS to GIS
in the next step. This just means issuing a SQL UPDATE now.

I am currently thinking there will be a separate table for each tile.
To work with them in groups I should be able to create a VIEW using
UNION statements. The name of each table will be derived from the
filename.

Note that it should not be necessary to load the LAZ files onto the
PostgreSQL server - you could do the download, decompress, load steps
from a desktop machine.  Once you have loaded the LAS data into
PostGIS you can delete the LAZ and LAS files to save space.

# Processing workflow

Now that I have the data formatted as points, I can do additional processing.

The immediate goal is create a DEM raster of the points classified as "bare earth".
Then I can derive slope, hillshade, and contour layers from the raster.

I have to do the testing on a small subset because it's slow.

I have to test the algorithms available in GDAL to determine what is best for this application,
the initial pass was very very bumpy.

Metadata with my Golden Gate data says it can be used to generate a 1 ft contour layer.

I should be able to do the processing directly in PostGIS, but I don't know how yet. First things first.
Getting the import workflow to work and flow. My early tests used shapefiles instead of
PostGIS.

# Classification from the metadata

The attribute asprsclass appears to have the classifications encoded as binary numbers
so it should look like this:

 1 unclassified     00000001
 2 bare earth       00000010
 3 vegetation       00000011
 7 noise (removed)  00000111
 9 water            00001001

# Requirements

Well yes, I do need to think about this soon in more detail.

I am running on the latest version of Ubuntu (17.04 aka "Zesty") for
development.  I deploy to a server running Debian 8.7. I plan to
deploy to Synology Diskstation running Docker but not in the immediate
future.

You have to have a PostGIS server, I am using 2.4 running on PostgreSQL 9.6
I build PostGIS from sources and that process causes all kinds of dependencies to be loaded.
I get PostgreSQL 9.6 by adding the PostgreSQL repository which on Ubuntu I use by adding a file,

 echo "deb http://apt.postgresql.org/pub/repos/apt/ zesty-pgdg main" > /etc/apt/sources.list.d/pgdg.list

I am using either Python 2.7 or 3.5 depending on my mood and what computer I am on.

The scripts use "las2ogr" which I get by the installing 'liblas-bin' package.

# Other information

A suggested workflow for ArcGIS
http://www.uccs.edu/~bvogt/courses/ges4050/helpful_stuff/las_to_dem.html

