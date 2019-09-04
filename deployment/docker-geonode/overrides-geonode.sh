#!/usr/bin/env bash

echo "Overriding geoserver/helpers.py"
cp /home/web/django_project/core/overrides/geonode/geonode/geoserver/helpers.py /usr/src/geonode/geonode/geoserver/helpers.py

echo "Overriding geonode/geonode/static/geonode/js/utils/utils.js"
cp /home/web/django_project/core/overrides/geonode/geonode/static/geonode/js/utils/utils.js /usr/src/geonode/geonode/static/geonode/js/utils/utils.js

echo "Overriding geonode/geonode/layers/templates/upload/layer_upload.html"
cp /home/web/django_project/core/overrides/geonode/geonode/layers/templates/upload/layer_upload.html /usr/src/geonode/geonode/layers/templates/upload/layer_upload.html

echo "Overriding geonode/geonode/templates/_permissions_form_js.html"
cp /home/web/django_project/core/overrides/geonode/geonode/templates/_permissions_form_js.html /usr/src/geonode/geonode/templates/_permissions_form_js.html
