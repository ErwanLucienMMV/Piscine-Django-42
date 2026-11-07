#!/bin/sh
curl --silent --show-error --location --output /dev/null --write-out '%{url_effective}\n' "$1"
