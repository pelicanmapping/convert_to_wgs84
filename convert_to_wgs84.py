#!/usr/bin/env python3
import click
import glob
import os
from multiprocessing import Pool
import subprocess
from osgeo import gdal

gdal.UseExceptions()

def get_bounds(filename):
    ds = gdal.Open(filename)
    gt = ds.GetGeoTransform()
    ll = gdal.ApplyGeoTransform(gt, 0, ds.RasterYSize)
    ur = gdal.ApplyGeoTransform(gt, ds.RasterXSize, 0)    
    ds = None
    return (ll[0], ll[1], ur[0], ur[1])

def convert(source, destination):
    print("Converting %s to %s" % (source, destination))

    # Make the directory for the output file if it doesn't exist
    os.makedirs(os.path.dirname(destination), exist_ok=True)    
    
    # Important to keep the output coordinates the same for files that go past -180/180 slightly since gdalwarp will compute the wrong output size and extents
    min_x, min_y, max_x, max_y = get_bounds(source)
    if (min_x < -180): min_x = -180
    if (min_y < -90): min_y = -90
    if (max_x > 180): max_x = 180
    if (max_y > 90): max_y = 90

    subprocess.run(["gdalwarp",
                    "-s_srs", "epsg:4326+5773",
                    "-t_srs", "epsg:4326",
                    "-te", str(min_x), str(min_y), str(max_x), str(max_y),
                    "-co", "TILED=YES",
                    "-co", "COMPRESS=LZW",
                    "-overwrite",                    
                    source, destination                    
                    ], 
                    # Redirect output to devnull to quiet down the console
                    stderr=subprocess.DEVNULL,
                    stdout=subprocess.DEVNULL
                    )

@click.command()
@click.option('--src',  required=True, help="Directory containing files to convert")
@click.option('--dst',  required=True, help="Output directory")
@click.option('--ext',  help="The file extension to search for", default="tif")
@click.option('--cpus', help="The number of cpus to use", default=4)
@click.option('--dryrun', help="Print all the files that will be processed without doing any actual work", is_flag=True, default=False)
def convert_to_wgs84(src, dst, ext, cpus, dryrun):
    jobs = []
    if os.path.isdir(src):
        pattern = os.path.join(src, "**/*.%s" % ext)        
        for file in glob.glob(pattern, recursive=True):
            destination = file.replace(src, dst)
            jobs.append((file, destination))
    else:
        jobs.append([src, dst])

    if dryrun:
        for job in jobs:
            print("Converting %s to %s" % (job[0], job[1]))
    else:
        pool = Pool(cpus)
        pool.starmap(convert, jobs)
    print("Complete")

if __name__ == '__main__':
    convert_to_wgs84()    
