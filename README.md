# convert_to_wgs84
Utilities to process elevation files from EGM96 heights to WGS84 heights.

Basic usage
```
docker run -v /data:/data --rm -it pelicanmapping/convert_to_wgs84 --src INPUT_FILE_OR_DIRECTORY --dst OUTPUT_FILE_OR_DIRECTORY
```


If you pass in a directory for src, pass in a directory for dst as well.

Other arguments:

**--dryrun** :  Prints out the files that will be processed

**--cpus**: The number of cpus to use (default 4)

**--ext**: The file extension to search for if src is a directory (default tif).
