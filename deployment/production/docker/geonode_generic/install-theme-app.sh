#!/usr/bin/env bash

echo "Checking Geonode custom theme app settings"

if [ ! -z "$GEONODE_THEME_APP_PIP_URL" ]; then

	echo "Install Geonode custom theme: $GEONODE_THEME_APP_PIP_URL"

	pip install --upgrade $GEONODE_THEME_APP_PIP_URL
fi
