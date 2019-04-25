#!/usr/bin/env bash

echo "Checking ScanAgroEmpresa custom theme app settings"

# Check if we need to install private key

if [ ! -z "$SCANAGROEMPRESA_THEME_APP_SSH_KEY" ]; then

	echo "Install SSH key for theme app"

	mkdir -p ~/.ssh
	chmod 700 ~/.ssh
	cat ${SCANAGROEMPRESA_THEME_APP_SSH_KEY} > ~/.ssh/id_rsa
	chmod 600 ~/.ssh/id_rsa

fi

if [ ! -z "$SCANAGROEMPRESA_THEME_APP_PIP_URL" ]; then

	echo "Install ScanAgroEmpresa custom theme: $SCANAGROEMPRESA_THEME_APP_PIP_URL"

	pip install --upgrade $SCANAGROEMPRESA_THEME_APP_PIP_URL
fi
