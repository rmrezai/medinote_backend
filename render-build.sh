#!/usr/bin/env bash
set -o errexit  # Exit on error

echo "Installing from prebuilt wheels..."
pip install --upgrade pip wheel
pip install --no-index --find-links=wheels -r requirements.txt

