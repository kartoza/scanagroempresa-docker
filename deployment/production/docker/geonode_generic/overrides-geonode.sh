#!/usr/bin/env bash

echo "Overiding geoserver/helpers.py"
cp /usr/src/scanagroempresa-docker/core/overrides/geonode/geonode/geoserver/helpers.py /usr/src/geonode/geonode/geoserver/helpers.py
