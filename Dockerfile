FROM ghcr.io/osgeo/gdal:ubuntu-full-latest-amd64
ADD convert_to_wgs84.py /usr/bin/convert_to_wgs84.py
RUN chmod a+x /usr/bin/convert_to_wgs84.py
RUN apt-get update && apt-get install python3-pip -y
RUN pip3 install click==8.1.6
ENTRYPOINT ["/usr/bin/convert_to_wgs84.py" ]