#!/usr/bin/env bash

xvfb-run -a /usr/lib/node_modules/orca/bin/orca.js "$@"
