#!/usr/bin/env bash

echo "Overiding geoserver/helpers.py"
cp /home/web/django_project/core/overrides/geonode/geonode/geoserver/helpers.py /usr/src/geonode/geonode/geoserver/helpers.py
