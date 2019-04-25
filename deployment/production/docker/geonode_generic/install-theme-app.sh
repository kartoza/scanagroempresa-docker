#!/usr/bin/env bash

echo "Checking Geonode custom theme app settings"

if [ ! -z "$GEONODE_THEME_APP_SSH_KEY" ]; then

	echo "Install SSH key for theme app"

	mkdir -p ~/.ssh
	chmod 700 ~/.ssh
	cat ${GEONODE_THEME_APP_SSH_KEY} > ~/.ssh/id_rsa
	chmod 600 ~/.ssh/id_rsa

fi

if [ ! -z "$GEONODE_THEME_APP_PIP_URL" ]; then

	echo "Install Geonode custom theme: $GEONODE_THEME_APP_PIP_URL"

	pip install --upgrade $GEONODE_THEME_APP_PIP_URL
fi
