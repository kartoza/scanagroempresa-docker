#!/usr/bin/env bash

echo "Checking ScanAgroEmpresa custom theme app settings"

if [ ! -z "$SCANAGROEMPRESA_THEME_APP_PIP_URL" ]; then

	echo "Install ScanAgroEmpresa custom theme: $SCANAGROEMPRESA_THEME_APP_PIP_URL"

	pip install --upgrade $SCANAGROEMPRESA_THEME_APP_PIP_URL
fi
